from typing import Any

from pydantic import BaseModel, Field


class PublicDashboardResponse(BaseModel):
    dashboard_slug: str
    conversation_summary: str | None = None
    public_payload: dict[str, Any] = Field(default_factory=dict)
    created_at: str | None = None
