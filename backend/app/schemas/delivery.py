from typing import Any

from pydantic import BaseModel, Field


class PostCallEventRequest(BaseModel):
    dashboard_payload_id: str
    dashboard_slug: str
    public_payload: dict[str, Any] = Field(default_factory=dict)
    conversation_summary: str | None = None
    recipient: dict[str, Any] = Field(default_factory=dict)


class DeliveryResponse(BaseModel):
    ok: bool
    result: dict[str, Any] = Field(default_factory=dict)
