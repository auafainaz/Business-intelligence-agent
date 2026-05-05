from __future__ import annotations

from datetime import UTC, datetime
import json
import sqlite3
from typing import Any
from uuid import uuid4

from app.db.connection import get_connection


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


def new_id() -> str:
    return str(uuid4())


def _json(data: Any) -> str:
    return json.dumps(data if data is not None else {}, ensure_ascii=True)


def _row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row else None


def create_call_session(
    *,
    twilio_call_sid: str | None = None,
    caller_number: str | None = None,
    called_number: str | None = None,
    voice_model: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    session_id = new_id()
    now = utc_now_iso()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO call_sessions (
                id, twilio_call_sid, caller_number, called_number, session_status,
                voice_model, transcript_status, started_at, metadata_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                twilio_call_sid,
                caller_number,
                called_number,
                "started",
                voice_model,
                "pending",
                now,
                _json(metadata or {}),
            ),
        )
        row = connection.execute("SELECT * FROM call_sessions WHERE id = ?", (session_id,)).fetchone()
    return _row_to_dict(row) or {}


def update_call_session_status(
    *, call_session_id: str, session_status: str, ended_at: str | None = None, transcript_status: str | None = None
) -> dict[str, Any] | None:
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE call_sessions
            SET session_status = ?,
                ended_at = COALESCE(?, ended_at),
                transcript_status = COALESCE(?, transcript_status),
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (session_status, ended_at, transcript_status, call_session_id),
        )
        row = connection.execute("SELECT * FROM call_sessions WHERE id = ?", (call_session_id,)).fetchone()
    return _row_to_dict(row)


def get_call_session(call_session_id: str) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM call_sessions WHERE id = ?", (call_session_id,)).fetchone()
    return _row_to_dict(row)


def find_call_session_by_twilio_sid(twilio_call_sid: str) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM call_sessions WHERE twilio_call_sid = ?", (twilio_call_sid,)).fetchone()
    return _row_to_dict(row)


def create_transcript(
    *,
    call_session_id: str | None,
    raw_transcript: str,
    summary: str | None = None,
    extracted_fields: dict[str, Any] | None = None,
) -> dict[str, Any]:
    transcript_id = new_id()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO transcripts (id, call_session_id, raw_transcript, summary, extracted_fields_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (transcript_id, call_session_id, raw_transcript, summary, _json(extracted_fields or {})),
        )
        if call_session_id:
            connection.execute(
                "UPDATE call_sessions SET transcript_status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                ("saved", call_session_id),
            )
        row = connection.execute("SELECT * FROM transcripts WHERE id = ?", (transcript_id,)).fetchone()
    return _row_to_dict(row) or {}


def create_client_profile(profile: dict[str, Any]) -> dict[str, Any]:
    profile_id = new_id()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO client_profiles (
                id, call_session_id, full_name, role, email, phone, company_name, website,
                city_or_location, years_in_business, number_of_locations, business_type,
                industry, service_summary, company_summary, key_frustrations_json,
                key_goals_json, ai_familiarity, current_systems_json, lead_source
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                profile_id,
                profile.get("call_session_id"),
                profile.get("full_name"),
                profile.get("role"),
                profile.get("email"),
                profile.get("phone"),
                profile["company_name"],
                profile.get("website"),
                profile.get("city_or_location"),
                profile.get("years_in_business"),
                profile.get("number_of_locations"),
                profile.get("business_type"),
                profile.get("industry"),
                profile.get("service_summary"),
                profile.get("company_summary"),
                _json(profile.get("key_frustrations") or []),
                _json(profile.get("key_goals") or []),
                profile.get("ai_familiarity"),
                _json(profile.get("current_systems") or []),
                profile.get("lead_source") or "inbound_call",
            ),
        )
        row = connection.execute("SELECT * FROM client_profiles WHERE id = ?", (profile_id,)).fetchone()
    return _row_to_dict(row) or {}


def create_dashboard_payload(
    *,
    client_profile_id: str | None,
    call_session_id: str | None,
    dashboard_slug: str,
    public_payload: dict[str, Any],
    internal_payload: dict[str, Any],
    conversation_summary: str | None,
) -> dict[str, Any]:
    payload_id = new_id()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO dashboard_payloads (
                id, client_profile_id, call_session_id, dashboard_slug,
                public_payload_json, internal_payload_json, conversation_summary
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload_id,
                client_profile_id,
                call_session_id,
                dashboard_slug,
                _json(public_payload),
                _json(internal_payload),
                conversation_summary,
            ),
        )
        row = connection.execute("SELECT * FROM dashboard_payloads WHERE id = ?", (payload_id,)).fetchone()
    return _row_to_dict(row) or {}


def get_dashboard_payload_record_by_id(payload_id: str) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM dashboard_payloads WHERE id = ?", (payload_id,)).fetchone()
    return _row_to_dict(row)


def get_dashboard_payload_record_by_call_session_id(call_session_id: str) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM dashboard_payloads WHERE call_session_id = ? ORDER BY created_at DESC LIMIT 1",
            (call_session_id,),
        ).fetchone()
    return _row_to_dict(row)


def get_dashboard_payload_record_by_slug(dashboard_slug: str) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM dashboard_payloads WHERE dashboard_slug = ?",
            (dashboard_slug,),
        ).fetchone()
    return _row_to_dict(row)


def dashboard_slug_exists(slug: str) -> bool:
    with get_connection() as connection:
        row = connection.execute("SELECT 1 FROM dashboard_payloads WHERE dashboard_slug = ?", (slug,)).fetchone()
    return row is not None


def get_public_dashboard_payload(slug: str) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT dashboard_slug, public_payload_json, conversation_summary, created_at FROM dashboard_payloads WHERE dashboard_slug = ?",
            (slug,),
        ).fetchone()
    if not row:
        return None
    return {
        "dashboard_slug": row["dashboard_slug"],
        "conversation_summary": row["conversation_summary"],
        "created_at": row["created_at"],
        "public_payload": json.loads(row["public_payload_json"]),
    }


def create_automation_event(
    *,
    dashboard_payload_id: str | None,
    dashboard_slug: str,
    event_type: str,
    request_payload: dict[str, Any],
    status: str = "pending",
    response_payload: dict[str, Any] | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    event_id = new_id()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO automation_events (
                id, dashboard_payload_id, dashboard_slug, event_type, status,
                request_json, response_json, error
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_id,
                dashboard_payload_id,
                dashboard_slug,
                event_type,
                status,
                _json(request_payload),
                _json(response_payload or {}),
                error,
            ),
        )
        row = connection.execute("SELECT * FROM automation_events WHERE id = ?", (event_id,)).fetchone()
    return _row_to_dict(row) or {}


def get_delivery_by_idempotency_key(idempotency_key: str) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM delivery_records WHERE idempotency_key = ?",
            (idempotency_key,),
        ).fetchone()
    return _row_to_dict(row)


def create_delivery_record(
    *,
    dashboard_payload_id: str | None,
    dashboard_slug: str,
    channel: str,
    recipient: str | None,
    status: str,
    idempotency_key: str,
    provider_message_id: str | None = None,
    error: str | None = None,
    sent_at: str | None = None,
) -> dict[str, Any]:
    existing = get_delivery_by_idempotency_key(idempotency_key)
    if existing:
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE delivery_records
                SET dashboard_payload_id = ?, dashboard_slug = ?, channel = ?,
                    recipient = ?, status = ?, provider_message_id = ?,
                    error = ?, sent_at = ?, updated_at = CURRENT_TIMESTAMP
                WHERE idempotency_key = ?
                """,
                (
                    dashboard_payload_id,
                    dashboard_slug,
                    channel,
                    recipient,
                    status,
                    provider_message_id,
                    error,
                    sent_at,
                    idempotency_key,
                ),
            )
            row = connection.execute(
                "SELECT * FROM delivery_records WHERE idempotency_key = ?",
                (idempotency_key,),
            ).fetchone()
        return _row_to_dict(row) or existing
    delivery_id = new_id()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO delivery_records (
                id, dashboard_payload_id, dashboard_slug, channel, recipient,
                status, provider_message_id, error, idempotency_key, sent_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                delivery_id,
                dashboard_payload_id,
                dashboard_slug,
                channel,
                recipient,
                status,
                provider_message_id,
                error,
                idempotency_key,
                sent_at,
            ),
        )
        row = connection.execute("SELECT * FROM delivery_records WHERE id = ?", (delivery_id,)).fetchone()
    return _row_to_dict(row) or {}


def list_delivery_records_for_slug(dashboard_slug: str) -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM delivery_records WHERE dashboard_slug = ? ORDER BY created_at DESC",
            (dashboard_slug,),
        ).fetchall()
    return [dict(row) for row in rows]
