from __future__ import annotations

import asyncio
import json
import re
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlsplit, urlunsplit

from fastapi import WebSocket, WebSocketDisconnect
import websockets

from app.config import get_settings
from app.db import repository
from app.schemas.tools import AnalyzeOfficialPageRequest
from app.services.integration_logger import log_step
from app.services.local_call_output import save_local_call_summary
from app.services.official_page_research import analyze_official_page
from app.services.realtime_tool_dispatcher import execute_realtime_tool
from app.services.xai_realtime import get_tool_registry
from app.services.prompt_loader import load_grok_system_prompt


class TwilioXaiBridge:
    def __init__(self, twilio_ws: WebSocket) -> None:
        self.twilio_ws = twilio_ws
        self.settings = get_settings()
        self.stream_sid: str | None = None
        self.call_sid: str | None = None
        self.call_session_id: str | None = None
        self._closed = asyncio.Event()
        self._transcript_segments: list[str] = []
        self._assistant_transcript_parts: dict[str, list[str]] = {}
        self._assistant_speaking = False
        self._current_response_id: str | None = None
        self._tool_results: list[dict[str, Any]] = []
        self._analyzed_urls: set[str] = set()
        self._xai_send_lock = asyncio.Lock()

    async def run(self) -> None:
        await self.twilio_ws.accept()
        if not self.settings.xai_api_key:
            await self.twilio_ws.close(code=1011, reason="XAI_API_KEY is not configured.")
            return

        headers = {"Authorization": f"Bearer {self.settings.xai_api_key}"}
        try:
            async with websockets.connect(self._xai_realtime_url(), additional_headers=headers) as xai_ws:
                await self._configure_xai_session(xai_ws)
                await asyncio.gather(
                    self._twilio_to_xai(xai_ws),
                    self._xai_to_twilio(xai_ws),
                )
        except WebSocketDisconnect:
            return
        except Exception as exc:
            log_step("xAI realtime bridge result", status="failed", error=str(exc), call_session_id=self.call_session_id)
            try:
                await self.twilio_ws.close(code=1011)
            except RuntimeError:
                pass

    def _xai_realtime_url(self) -> str:
        parts = urlsplit(self.settings.xai_realtime_url)
        query = dict(parse_qsl(parts.query))
        query.setdefault("model", self.settings.xai_realtime_model)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    async def _configure_xai_session(self, xai_ws) -> None:
        # Twilio streams raw G.711 mulaw at 8kHz. xAI accepts audio/pcmu directly,
        # which keeps the live path thin and avoids transcoding in the bridge.
        tools = get_tool_registry()
        await xai_ws.send(
            json.dumps(
                {
                    "type": "session.update",
                    "session": {
                        "voice": self.settings.xai_voice,
                        "instructions": load_grok_system_prompt(),
                        "turn_detection": {
                            "type": "server_vad",
                            "threshold": 0.5,
                            "silence_duration_ms": 750,
                            "prefix_padding_ms": 300,
                        },
                        "audio": {
                            "input": {"format": {"type": "audio/pcmu"}},
                            "output": {"format": {"type": "audio/pcmu"}},
                        },
                        "tools": tools,
                    },
                }
            )
        )
        log_step(
            "xAI realtime session result",
            status="configured",
            model=self.settings.xai_realtime_model,
            voice=self.settings.xai_voice,
        )

    async def _twilio_to_xai(self, xai_ws) -> None:
        while not self._closed.is_set():
            message_text = await self.twilio_ws.receive_text()
            message = json.loads(message_text)
            event = message.get("event")
            if event == "start":
                start = message.get("start") or {}
                self.stream_sid = start.get("streamSid") or message.get("streamSid")
                self.call_sid = start.get("callSid")
                custom_parameters = start.get("customParameters") or {}
                self.call_session_id = custom_parameters.get("call_session_id")
                log_step("call start", twilio_call_sid=self.call_sid, call_session_id=self.call_session_id)
                await self._request_initial_greeting(xai_ws)
            elif event == "media":
                payload = (message.get("media") or {}).get("payload")
                if payload:
                    await xai_ws.send(json.dumps({"type": "input_audio_buffer.append", "audio": payload}))
            elif event == "stop":
                self._persist_realtime_transcript()
                self._persist_local_call_output()
                if self.call_session_id:
                    repository.update_call_session_status(
                        call_session_id=self.call_session_id,
                        session_status="completed",
                        ended_at=repository.utc_now_iso(),
                    )
                log_step("call end", twilio_call_sid=self.call_sid, call_session_id=self.call_session_id)
                self._closed.set()
                return

    async def _request_initial_greeting(self, xai_ws) -> None:
        await xai_ws.send(
            json.dumps(
                {
                    "type": "conversation.item.create",
                    "item": {
                        "type": "message",
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": (
                                    "The inbound phone call is now connected. Greet the caller warmly as the "
                                    "ClientIQ AI discovery agent, keep it brief, and ask for their first name."
                                ),
                            }
                        ],
                    },
                }
            )
        )
        await xai_ws.send(json.dumps({"type": "response.create"}))
        log_step("xAI realtime greeting result", status="requested", call_session_id=self.call_session_id)

    async def _xai_to_twilio(self, xai_ws) -> None:
        async for message_text in xai_ws:
            if self._closed.is_set():
                return
            event = json.loads(message_text)
            event_type = event.get("type")
            if event_type in {"response.output_audio.delta", "response.audio.delta"}:
                delta = event.get("delta")
                if delta and self.stream_sid:
                    self._assistant_speaking = True
                    self._current_response_id = event.get("response_id") or self._current_response_id
                    await self.twilio_ws.send_text(
                        json.dumps({"event": "media", "streamSid": self.stream_sid, "media": {"payload": delta}})
                    )
            elif event_type in {"input_audio_buffer.speech_started", "conversation.item.input_audio_buffer.speech_started"}:
                await self._handle_caller_barge_in(xai_ws)
            elif event_type in {"response.done", "response.output_audio.done", "response.audio.done"}:
                self._assistant_speaking = False
                self._current_response_id = None
            elif event_type in {"response.function_call_arguments.done", "response.tool_call_arguments.done"}:
                await self._handle_tool_call(xai_ws, event)
            elif event_type == "conversation.item.input_audio_transcription.completed":
                await self._capture_caller_transcript(xai_ws, event)
            elif event_type == "response.output_audio_transcript.delta":
                self._capture_assistant_transcript_delta(event)
            elif event_type == "response.output_audio_transcript.done":
                self._capture_assistant_transcript_done(event)
            elif event_type in {"error", "response.failed"}:
                log_step("xAI realtime event", status="error", event=event)
            elif event_type in {"session.created", "session.updated"}:
                log_step("xAI realtime event", status="ok", event_type=event_type)
            elif self._is_tool_or_search_event(event_type):
                log_step(
                    "xAI realtime tool/search event",
                    event_type=event_type,
                    tool_name=event.get("name") or event.get("tool_name") or event.get("type"),
                    call_id=event.get("call_id") or event.get("item_id"),
                    call_session_id=self.call_session_id,
                )

    async def _handle_caller_barge_in(self, xai_ws) -> None:
        if not self._assistant_speaking:
            return
        try:
            await xai_ws.send(json.dumps({"type": "response.cancel"}))
        except Exception as exc:
            log_step("xAI realtime barge-in result", status="cancel_failed", error=str(exc))
        if self.stream_sid:
            await self.twilio_ws.send_text(json.dumps({"event": "clear", "streamSid": self.stream_sid}))
        self._assistant_speaking = False
        self._current_response_id = None
        log_step("xAI realtime barge-in result", status="interrupted", call_session_id=self.call_session_id)

    def _is_tool_or_search_event(self, event_type: str | None) -> bool:
        if not event_type:
            return False
        searchable = event_type.lower()
        return "tool" in searchable or "search" in searchable or "function_call" in searchable

    async def _capture_caller_transcript(self, xai_ws, event: dict[str, Any]) -> None:
        transcript = event.get("transcript")
        if isinstance(transcript, str) and transcript.strip():
            clean_transcript = transcript.strip()
            self._transcript_segments.append(f"Caller: {clean_transcript}")
            log_step(
                "transcript capture result",
                status="caller_segment",
                call_session_id=self.call_session_id,
            )
            asyncio.create_task(self._auto_analyze_detected_official_page(xai_ws, clean_transcript))

    def _capture_assistant_transcript_delta(self, event: dict[str, Any]) -> None:
        key = event.get("response_id") or event.get("item_id") or "assistant"
        delta = event.get("delta")
        if isinstance(delta, str) and delta:
            self._assistant_transcript_parts.setdefault(str(key), []).append(delta)

    def _capture_assistant_transcript_done(self, event: dict[str, Any]) -> None:
        key = str(event.get("response_id") or event.get("item_id") or "assistant")
        transcript = event.get("transcript")
        if not isinstance(transcript, str) or not transcript.strip():
            transcript = "".join(self._assistant_transcript_parts.pop(key, [])).strip()
        else:
            self._assistant_transcript_parts.pop(key, None)
        if transcript:
            self._transcript_segments.append(f"Agent: {transcript.strip()}")
            log_step(
                "transcript capture result",
                status="agent_segment",
                call_session_id=self.call_session_id,
            )

    def _persist_realtime_transcript(self) -> None:
        if not self.call_session_id or not self._transcript_segments:
            return
        raw_transcript = "\n".join(self._transcript_segments)
        transcript = repository.create_transcript(
            call_session_id=self.call_session_id,
            raw_transcript=raw_transcript,
            summary=None,
            extracted_fields={"source": "xai_realtime_transcript_events"},
        )
        log_step(
            "transcript save result",
            call_session_id=self.call_session_id,
            transcript_id=transcript["id"],
            source="xai_realtime",
        )

    async def _handle_tool_call(self, xai_ws, event: dict[str, Any]) -> None:
        name = event.get("name") or event.get("tool_name")
        call_id = event.get("call_id") or event.get("item_id")
        arguments = event.get("arguments") or "{}"
        if not name or not call_id:
            return
        log_step(
            "xAI realtime function call",
            tool_name=name,
            call_id=call_id,
            call_session_id=self.call_session_id,
        )
        if name == "web_search":
            self._tool_results.append(
                {
                    "tool_name": name,
                    "call_id": call_id,
                    "arguments": arguments,
                    "result": {"status": "native_web_search_requested"},
                }
            )
            return
        arguments_for_execution = _json_arguments(arguments)
        if name in {"save_dashboard_data", "save_call_transcript"} and self.call_session_id:
            arguments_for_execution.setdefault("call_session_id", self.call_session_id)
        result = execute_realtime_tool(name, arguments_for_execution)
        self._tool_results.append(
            {
                "tool_name": name,
                "call_id": call_id,
                "arguments": arguments_for_execution,
                "result": result,
            }
        )
        await xai_ws.send(
            json.dumps(
                {
                    "type": "conversation.item.create",
                    "item": {
                        "type": "function_call_output",
                        "call_id": call_id,
                        "output": json.dumps(result),
                    },
                }
            )
        )
        await xai_ws.send(json.dumps({"type": "response.create"}))

    async def _auto_analyze_detected_official_page(self, xai_ws, transcript: str) -> None:
        url = _extract_public_url(transcript)
        if not url or url in self._analyzed_urls:
            return
        self._analyzed_urls.add(url)
        result = analyze_official_page(AnalyzeOfficialPageRequest(official_url=url))
        self._tool_results.append(
            {
                "tool_name": "analyze_official_page",
                "call_id": f"auto:{len(self._tool_results) + 1}",
                "arguments": {"official_url": url, "source": "caller_transcript_auto_detect"},
                "result": result,
            }
        )
        if result.get("status") != "analyzed":
            return
        observations = result.get("public_observations") or []
        live_hooks = result.get("live_conversation_hooks") or []
        context = {
            "official_url": result.get("official_url"),
            "title": result.get("title"),
            "summary": result.get("summary"),
            "public_observations": observations[:3],
            "live_conversation_hooks": live_hooks[:3],
        }
        async with self._xai_send_lock:
            if self._closed.is_set():
                return
            await xai_ws.send(
                json.dumps(
                    {
                        "type": "conversation.item.create",
                        "item": {
                            "type": "message",
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": (
                                        "INTERNAL LIVE RESEARCH RESULT. The caller did not say this; it came from "
                                        "their public official website. In your next spoken response, briefly surprise "
                                        "the caller with ONE grounded observation from this result, then connect it to "
                                        "their pain point or business model, then ask ONE short follow-up question. "
                                        "Do not sound generic. Do not list data. Do not mention scraping. Say it like: "
                                        "'I took a quick public look, and one thing that stands out is ...' "
                                        f"Result JSON: {json.dumps(context, ensure_ascii=True)}"
                                    ),
                                }
                            ],
                        },
                    }
                )
            )
            await xai_ws.send(json.dumps({"type": "response.create"}))
        log_step(
            "official page realtime injection result",
            status="sent_to_agent",
            call_session_id=self.call_session_id,
            url=result.get("official_url"),
        )

    def _persist_local_call_output(self) -> None:
        if not self.call_session_id:
            return
        try:
            save_local_call_summary(
                call_session_id=self.call_session_id,
                twilio_call_sid=self.call_sid,
                caller_number=None,
                called_number=None,
                transcript_segments=self._transcript_segments,
                tool_results=self._tool_results,
            )
        except Exception as exc:
            log_step("local call output result", status="failed", call_session_id=self.call_session_id, error=str(exc))


def _extract_public_url(text: str) -> str | None:
    spoken_url = _extract_spoken_url(text)
    if spoken_url and _is_allowed_company_url(spoken_url):
        return _normalize_detected_url(spoken_url)

    direct_match = re.search(r"\b(?:https?://)?(?:www\.)?[a-z0-9-]+(?:\.[a-z0-9-]+)+\b", text, re.IGNORECASE)
    if direct_match and _is_allowed_company_url(direct_match.group(0)):
        return _normalize_detected_url(direct_match.group(0))
    return None


def _normalize_detected_url(url: str) -> str:
    normalized = url.lower().strip(" .,!?:;")
    if not normalized.startswith(("http://", "https://")):
        normalized = f"https://{normalized}"
    return normalized


def _is_allowed_company_url(url: str) -> bool:
    host = urlparse(_normalize_detected_url(url)).netloc.lower().removeprefix("www.")
    labels = host.split(".")
    blocked_hosts = {
        "gmail.com",
        "googlemail.com",
        "yahoo.com",
        "outlook.com",
        "hotmail.com",
        "icloud.com",
        "mail.com",
    }
    blocked_domains = {"gmail", "googlemail", "yahoo", "outlook", "hotmail", "icloud", "mail"}
    if host in blocked_hosts or (labels and labels[0] in blocked_domains):
        return False
    if len(labels) < 2:
        return False
    tld = labels[-1]
    return bool(re.fullmatch(r"[a-z]{2,12}", tld))


def _json_arguments(arguments: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(arguments, dict):
        return dict(arguments)
    try:
        parsed = json.loads(arguments) if arguments else {}
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        return {}


def _extract_spoken_url(text: str) -> str | None:
    normalized = text.lower().replace("double u", "w")
    tokens = re.findall(r"[a-z0-9]+|dot|period|point", normalized)
    dot_words = {"dot", "period", "point"}
    candidates: list[str] = []
    for start in range(len(tokens)):
        labels: list[str] = []
        current = ""
        saw_dot = False
        index = start
        while index < len(tokens):
            token = tokens[index]
            if token in dot_words:
                if not current:
                    break
                labels.append(current)
                current = ""
                saw_dot = True
                index += 1
                continue
            if saw_dot and _looks_like_tld(current) and not (current == "co" and token == "m"):
                break
            if len(token) == 1 and token.isalnum():
                current += token
                index += 1
                continue
            if token == "www" or re.fullmatch(r"[a-z0-9-]{2,}", token):
                current += token
                index += 1
                continue
            break
        if saw_dot and current:
            labels.append(current)
        if len(labels) >= 2 and len(labels[-1]) >= 2:
            domain = ".".join(labels)
            if "." in domain and not domain.startswith("."):
                candidates.append(domain)
    if not candidates:
        return None
    www_candidate = next((candidate for candidate in candidates if candidate.startswith("www.")), None)
    if www_candidate:
        return www_candidate
    clean_candidates = [
        candidate
        for candidate in candidates
        if not candidate.startswith(("website", "address", "url", "site"))
    ]
    if clean_candidates:
        return min(clean_candidates, key=len)
    return min(candidates, key=len)


def _looks_like_tld(value: str) -> bool:
    common_tlds = {
        "com",
        "net",
        "org",
        "io",
        "ai",
        "co",
        "biz",
        "info",
        "lk",
        "us",
        "uk",
        "ca",
        "au",
        "in",
        "edu",
        "gov",
    }
    return value in common_tlds
