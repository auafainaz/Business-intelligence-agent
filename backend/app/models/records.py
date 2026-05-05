from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CallSessionRecord:
    id: str
    twilio_call_sid: str | None
    caller_number: str | None
    called_number: str | None
    session_status: str
    voice_model: str | None
    transcript_status: str
    started_at: str
    ended_at: str | None
    metadata: dict[str, Any]


@dataclass(frozen=True)
class TranscriptRecord:
    id: str
    call_session_id: str | None
    raw_transcript: str
    summary: str | None
    extracted_fields: dict[str, Any]


@dataclass(frozen=True)
class ClientProfileRecord:
    id: str
    call_session_id: str | None
    full_name: str | None
    role: str | None
    email: str | None
    phone: str | None
    company_name: str
    website: str | None
    lead_source: str


@dataclass(frozen=True)
class DashboardPayloadRecord:
    id: str
    client_profile_id: str | None
    call_session_id: str | None
    dashboard_slug: str
    public_payload: dict[str, Any]
    internal_payload: dict[str, Any]
    conversation_summary: str | None
