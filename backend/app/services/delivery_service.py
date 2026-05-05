from __future__ import annotations

from email.message import EmailMessage
import smtplib
from typing import Any

import httpx

from app.config import get_settings
from app.db import repository
from app.services.integration_logger import log_step


def _quick_items(public_payload: dict[str, Any], key: str) -> list[str]:
    value = public_payload.get(key)
    return value if isinstance(value, list) else []


def build_post_call_payload(
    *,
    dashboard_payload_id: str,
    dashboard_slug: str,
    public_payload: dict[str, Any],
    conversation_summary: str | None,
    recipient: dict[str, Any],
) -> dict[str, Any]:
    settings = get_settings()
    client = public_payload.get("client") or {}
    return {
        "event": "post_call_dashboard_ready",
        "dashboard_payload_id": dashboard_payload_id,
        "dashboard_slug": dashboard_slug,
        "dashboard_url": settings.dashboard_url(dashboard_slug),
        "client": client,
        "recipient": recipient,
        "summary": conversation_summary or public_payload.get("company_summary"),
        "quick_wins": _quick_items(public_payload, "quick_wins"),
        "key_pain_points": _quick_items(public_payload, "key_pain_points"),
        "next_steps": _quick_items(public_payload, "next_steps"),
    }


def send_gmail_post_call_email(payload: dict[str, Any]) -> dict[str, Any]:
    settings = get_settings()
    recipient = (payload.get("recipient") or {}).get("email")
    slug = payload["dashboard_slug"]
    idempotency_key = f"{slug}:gmail:{recipient or 'missing'}"
    existing = repository.get_delivery_by_idempotency_key(idempotency_key)
    if existing and existing.get("status") == "sent":
        return {"status": "duplicate_skipped", "delivery_record_id": existing["id"]}
    if not recipient:
        record = repository.create_delivery_record(
            dashboard_payload_id=payload.get("dashboard_payload_id"),
            dashboard_slug=slug,
            channel="gmail",
            recipient=None,
            status="skipped",
            idempotency_key=idempotency_key,
            error="No recipient email in public payload.",
        )
        log_step("Gmail send result", dashboard_slug=slug, status="skipped", reason="missing_email")
        return {"status": "skipped", "delivery_record_id": record["id"], "reason": "missing_email"}
    if not (settings.gmail_username and settings.gmail_app_password and settings.gmail_from_email):
        record = repository.create_delivery_record(
            dashboard_payload_id=payload.get("dashboard_payload_id"),
            dashboard_slug=slug,
            channel="gmail",
            recipient=recipient,
            status="skipped",
            idempotency_key=idempotency_key,
            error="Gmail credentials not configured.",
        )
        log_step("Gmail send result", dashboard_slug=slug, status="skipped")
        return {"status": "skipped", "delivery_record_id": record["id"], "reason": "gmail_not_configured"}

    body = _build_email_body(payload)
    message = EmailMessage()
    message["Subject"] = "Your ClientIQ dashboard is ready"
    message["From"] = settings.gmail_from_email
    message["To"] = recipient
    message.set_content(body)
    try:
        with smtplib.SMTP(settings.gmail_smtp_host, settings.gmail_smtp_port, timeout=20) as smtp:
            smtp.starttls()
            smtp.login(settings.gmail_username, settings.gmail_app_password)
            smtp.send_message(message)
        record = repository.create_delivery_record(
            dashboard_payload_id=payload.get("dashboard_payload_id"),
            dashboard_slug=slug,
            channel="gmail",
            recipient=recipient,
            status="sent",
            idempotency_key=idempotency_key,
            sent_at=repository.utc_now_iso(),
        )
        log_step("Gmail send result", dashboard_slug=slug, status="sent")
        return {"status": "sent", "delivery_record_id": record["id"]}
    except Exception as exc:
        record = repository.create_delivery_record(
            dashboard_payload_id=payload.get("dashboard_payload_id"),
            dashboard_slug=slug,
            channel="gmail",
            recipient=recipient,
            status="failed",
            idempotency_key=idempotency_key,
            error=str(exc),
        )
        log_step("Gmail send result", dashboard_slug=slug, status="failed", error=str(exc))
        return {"status": "failed", "delivery_record_id": record["id"], "error": str(exc)}


def send_twilio_dashboard_sms(payload: dict[str, Any]) -> dict[str, Any]:
    settings = get_settings()
    recipient = (payload.get("recipient") or {}).get("phone")
    slug = payload["dashboard_slug"]
    idempotency_key = f"{slug}:sms:{recipient or 'missing'}"
    existing = repository.get_delivery_by_idempotency_key(idempotency_key)
    if existing and existing.get("status") == "sent":
        return {"status": "duplicate_skipped", "delivery_record_id": existing["id"]}
    if not recipient:
        record = repository.create_delivery_record(
            dashboard_payload_id=payload.get("dashboard_payload_id"),
            dashboard_slug=slug,
            channel="twilio_sms",
            recipient=None,
            status="skipped",
            idempotency_key=idempotency_key,
            error="No recipient phone in public payload.",
        )
        log_step("Twilio SMS send result", dashboard_slug=slug, status="skipped", reason="missing_phone")
        return {"status": "skipped", "delivery_record_id": record["id"], "reason": "missing_phone"}
    if not (settings.twilio_account_sid and settings.twilio_auth_token and settings.twilio_phone_number):
        record = repository.create_delivery_record(
            dashboard_payload_id=payload.get("dashboard_payload_id"),
            dashboard_slug=slug,
            channel="twilio_sms",
            recipient=recipient,
            status="skipped",
            idempotency_key=idempotency_key,
            error="Twilio SMS credentials not configured.",
        )
        log_step("Twilio SMS send result", dashboard_slug=slug, status="skipped")
        return {"status": "skipped", "delivery_record_id": record["id"], "reason": "twilio_not_configured"}

    body = f"Thanks for speaking with ClientIQ. Your dashboard is ready: {payload['dashboard_url']}"
    try:
        response = httpx.post(
            f"https://api.twilio.com/2010-04-01/Accounts/{settings.twilio_account_sid}/Messages.json",
            data={"To": recipient, "From": settings.twilio_phone_number, "Body": body},
            auth=(settings.twilio_account_sid, settings.twilio_auth_token),
            timeout=20,
        )
        response.raise_for_status()
        response_json = response.json()
        record = repository.create_delivery_record(
            dashboard_payload_id=payload.get("dashboard_payload_id"),
            dashboard_slug=slug,
            channel="twilio_sms",
            recipient=recipient,
            status="sent",
            provider_message_id=response_json.get("sid"),
            idempotency_key=idempotency_key,
            sent_at=repository.utc_now_iso(),
        )
        log_step("Twilio SMS send result", dashboard_slug=slug, status="sent", message_sid=response_json.get("sid"))
        return {"status": "sent", "delivery_record_id": record["id"], "provider_message_id": response_json.get("sid")}
    except Exception as exc:
        record = repository.create_delivery_record(
            dashboard_payload_id=payload.get("dashboard_payload_id"),
            dashboard_slug=slug,
            channel="twilio_sms",
            recipient=recipient,
            status="failed",
            idempotency_key=idempotency_key,
            error=str(exc),
        )
        log_step("Twilio SMS send result", dashboard_slug=slug, status="failed", error=str(exc))
        return {"status": "failed", "delivery_record_id": record["id"], "error": str(exc)}


def run_post_call_delivery(payload: dict[str, Any]) -> dict[str, Any]:
    settings = get_settings()
    if not settings.delivery_enabled:
        slug = payload["dashboard_slug"]
        log_step("Gmail send result", dashboard_slug=slug, status="skipped", reason="delivery_disabled")
        log_step("Twilio SMS send result", dashboard_slug=slug, status="skipped", reason="delivery_disabled")
        return {"status": "disabled"}
    results = {
        "gmail": send_gmail_post_call_email(payload),
        "twilio_sms": send_twilio_dashboard_sms(payload),
    }
    return results


def send_dashboard_delivery(
    *,
    dashboard_slug: str,
    dashboard_payload_id: str | None = None,
    public_payload: dict[str, Any] | None = None,
    conversation_summary: str | None = None,
    recipient: dict[str, Any] | None = None,
) -> dict[str, Any]:
    record = repository.get_dashboard_payload_record_by_slug(dashboard_slug)
    resolved_public_payload = public_payload or {}
    resolved_summary = conversation_summary
    resolved_payload_id = dashboard_payload_id
    if record:
        resolved_payload_id = resolved_payload_id or record["id"]
        if not resolved_public_payload:
            resolved_public_payload = _loads_json(record.get("public_payload_json"))
        resolved_summary = resolved_summary or record.get("conversation_summary")
    if not resolved_payload_id:
        return {"status": "failed", "reason": "dashboard_payload_not_found", "dashboard_slug": dashboard_slug}
    payload = build_post_call_payload(
        dashboard_payload_id=resolved_payload_id,
        dashboard_slug=dashboard_slug,
        public_payload=resolved_public_payload,
        conversation_summary=resolved_summary,
        recipient=recipient or {},
    )
    return run_post_call_delivery(payload)


def _build_email_body(payload: dict[str, Any]) -> str:
    name = (payload.get("recipient") or {}).get("name") or "there"
    quick_wins = payload.get("quick_wins") or []
    pain_points = payload.get("key_pain_points") or []
    lines = [
        f"Hi {name},",
        "",
        "Thank you for speaking with ClientIQ.",
        "",
        f"Your dashboard is ready: {payload['dashboard_url']}",
        "",
        "Short summary:",
        payload.get("summary") or "Your business intelligence summary is ready in the dashboard.",
        "",
    ]
    if pain_points:
        lines.extend(["Key areas we heard:", *[f"- {item}" for item in pain_points[:3]], ""])
    if quick_wins:
        lines.extend(["Quick wins:", *[f"- {item}" for item in quick_wins[:3]], ""])
    lines.extend([
        "Next step:",
        "Review the dashboard and use it as a starting point for a sharper follow-up strategy.",
        "",
        "ClientIQ",
    ])
    return "\n".join(lines)


def _loads_json(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    try:
        loaded = __import__("json").loads(value)
        return loaded if isinstance(loaded, dict) else {}
    except Exception:
        return {}
