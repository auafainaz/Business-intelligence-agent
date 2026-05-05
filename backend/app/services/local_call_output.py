from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

from app.config import get_settings
from app.db import repository
from app.graph.workflow import run_intelligence_workflow
from app.services.auto_dashboard_service import create_dashboard_from_call_output
from app.services.integration_logger import log_step


def save_local_call_summary(
    *,
    call_session_id: str,
    twilio_call_sid: str | None,
    caller_number: str | None,
    called_number: str | None,
    transcript_segments: list[str],
    tool_results: list[dict[str, Any]],
) -> Path:
    settings = get_settings()
    settings.local_call_output_dir.mkdir(parents=True, exist_ok=True)
    call_session = repository.get_call_session(call_session_id) or {}
    transcript = "\n".join(transcript_segments).strip()
    workflow_state = run_intelligence_workflow(
        {
            "call_session_id": call_session_id,
            "transcript": transcript,
            "transcript_summary": _short_summary(transcript),
            "extracted_fields": {
                "tool_names": [item.get("tool_name") for item in tool_results],
                "official_page_urls": _official_page_urls(tool_results),
            },
        }
    )
    payload = {
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "call": {
            "call_session_id": call_session_id,
            "twilio_call_sid": twilio_call_sid or call_session.get("twilio_call_sid"),
            "caller_number": caller_number or call_session.get("caller_number"),
            "called_number": called_number or call_session.get("called_number"),
            "started_at": call_session.get("started_at"),
            "ended_at": call_session.get("ended_at"),
        },
        "summary": {
            "transcript_summary": workflow_state.get("transcript_summary"),
            "tool_names": [item.get("tool_name") for item in tool_results],
            "official_page_urls": _official_page_urls(tool_results),
            "dashboard_saved": _dashboard_saved(tool_results),
            "delivery_attempted": False,
        },
        "transcript": {
            "raw": transcript,
            "segments": transcript_segments,
        },
        "research": {
            "official_page_analyses": _official_page_analyses(tool_results),
            "all_tool_results": tool_results,
        },
        "dashboard": _latest_dashboard_result(tool_results),
    }
    existing_dashboard = payload.get("dashboard") or {}
    auto_dashboard = existing_dashboard if existing_dashboard.get("dashboard_slug") else create_dashboard_from_call_output(payload)
    if auto_dashboard.get("status") in {"created", "existing"} or auto_dashboard.get("dashboard_slug"):
        payload["dashboard"] = {
            **(payload.get("dashboard") or {}),
            **auto_dashboard,
            "dashboard_url": settings.dashboard_url(auto_dashboard["dashboard_slug"]),
        }
        payload["summary"]["dashboard_saved"] = True
        payload["summary"]["dashboard_slug"] = auto_dashboard["dashboard_slug"]
        payload["summary"]["delivery_attempted"] = bool(auto_dashboard.get("delivery_results"))
    path = settings.local_call_output_dir / f"{call_session_id}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")
    log_step("local call output result", status="saved", call_session_id=call_session_id, path=str(path))
    return path


def _short_summary(transcript: str) -> str | None:
    if not transcript:
        return None
    return transcript[:700]


def _official_page_analyses(tool_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        item.get("result") or {}
        for item in tool_results
        if item.get("tool_name") == "analyze_official_page" and isinstance(item.get("result"), dict)
    ]


def _official_page_urls(tool_results: list[dict[str, Any]]) -> list[str]:
    urls: list[str] = []
    for analysis in _official_page_analyses(tool_results):
        url = analysis.get("official_url")
        if isinstance(url, str) and url not in urls:
            urls.append(url)
    return urls


def _latest_dashboard_result(tool_results: list[dict[str, Any]]) -> dict[str, Any] | None:
    for item in reversed(tool_results):
        if item.get("tool_name") == "save_dashboard_data" and isinstance(item.get("result"), dict):
            return item["result"]
    return None


def _dashboard_saved(tool_results: list[dict[str, Any]]) -> bool:
    dashboard = _latest_dashboard_result(tool_results)
    return bool(dashboard and dashboard.get("dashboard_slug"))
