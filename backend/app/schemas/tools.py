from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl


class ClientIdentity(BaseModel):
    full_name: str
    role: Literal["Owner", "Decision Maker", "Manager", "Other"] | str | None = None
    email: str | None = None
    phone: str | None = None
    website: HttpUrl | str | None = None
    business_name: str
    city: str | None = None
    years_in_business: int | None = Field(default=None, ge=0)
    number_of_locations: int | None = Field(default=None, ge=0)


class DashboardData(BaseModel):
    google_rank: str | None = None
    google_rating: str | None = None
    review_count: str | None = None
    ai_search_status: str | None = None
    website_traffic_estimate: str | None = None
    ai_website_agent: str | None = None
    load_speed: str | None = None
    social_footprint: dict[str, Any] = Field(default_factory=dict)
    main_opportunities: list[str] = Field(default_factory=list)
    public_summary: str | None = None
    digital_presence_notes: list[str] = Field(default_factory=list)
    website_notes: list[str] = Field(default_factory=list)
    google_presence_notes: list[str] = Field(default_factory=list)
    social_presence_notes: list[str] = Field(default_factory=list)
    quick_wins: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)


class SaveDashboardDataRequest(BaseModel):
    call_session_id: str | None = None
    client: ClientIdentity
    conversation_summary: str
    key_pain_points: list[str] = Field(default_factory=list)
    key_goals: list[str] = Field(default_factory=list)
    ai_familiarity: str | None = None
    current_systems: list[str] = Field(default_factory=list)
    dashboard_data: DashboardData = Field(default_factory=DashboardData)
    personal_touch: str
    full_transcript: str | None = None
    timestamp: str | None = None
    lead_source: Literal["inbound_call", "outbound", "website_chat"] = "inbound_call"


class SaveCallTranscriptRequest(BaseModel):
    call_session_id: str | None = None
    raw_transcript: str
    summary: str | None = None
    extracted_fields: dict[str, Any] = Field(default_factory=dict)


class GenerateDashboardSlugRequest(BaseModel):
    business_name: str
    city: str | None = None


class CreateDashboardPayloadRequest(BaseModel):
    client: ClientIdentity
    conversation_summary: str | None = None
    dashboard_data: DashboardData = Field(default_factory=DashboardData)
    key_pain_points: list[str] = Field(default_factory=list)
    key_goals: list[str] = Field(default_factory=list)


class LookupBusinessProfileRequest(BaseModel):
    business_name: str
    website: HttpUrl | str | None = None
    city: str | None = None


class ExtractSocialPresenceRequest(BaseModel):
    business_name: str
    website: HttpUrl | str | None = None
    known_links: list[str] = Field(default_factory=list)


class AnalyzeOfficialPageRequest(BaseModel):
    official_url: HttpUrl | str
    organization_name: str | None = None


class SendDashboardDeliveryRequest(BaseModel):
    dashboard_slug: str
    dashboard_payload_id: str | None = None
    recipient_email: str | None = None
    recipient_phone: str | None = None
    recipient_name: str | None = None
    conversation_summary: str | None = None
    public_payload: dict[str, Any] = Field(default_factory=dict)


class ToolResponse(BaseModel):
    ok: bool
    tool: str
    result: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
