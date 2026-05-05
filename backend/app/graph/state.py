from typing import Any, TypedDict


class IntelligenceState(TypedDict, total=False):
    call_session_id: str | None
    transcript: str | None
    transcript_summary: str | None
    extracted_fields: dict[str, Any]
    business_profile: dict[str, Any]
    social_presence: dict[str, Any]
    public_dashboard_payload: dict[str, Any]
    internal_notes: dict[str, Any]
    errors: list[str]


class ArchitectureState(TypedDict, total=False):
    stage_log: list[str]
    current_stage: str
    public_dashboard_ready: bool
    internal_record_ready: bool
    delivery_ready: bool
    errors: list[str]
