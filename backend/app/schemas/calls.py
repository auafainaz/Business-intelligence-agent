from typing import Any

from pydantic import BaseModel, Field


class CallSessionCreate(BaseModel):
    twilio_call_sid: str | None = None
    caller_number: str | None = None
    called_number: str | None = None
    voice_model: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class CallSessionComplete(BaseModel):
    call_session_id: str
    session_status: str = "completed"
    ended_at: str | None = None
    transcript_status: str | None = None


class CallSessionResponse(BaseModel):
    call_session_id: str
    twilio_call_sid: str | None = None
    status: str
    media_stream_url: str | None = None
