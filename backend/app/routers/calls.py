from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.db import repository
from app.schemas.calls import CallSessionComplete, CallSessionCreate, CallSessionResponse

router = APIRouter(prefix="/calls", tags=["calls"])


@router.post("/start", response_model=CallSessionResponse)
def start_call(payload: CallSessionCreate) -> CallSessionResponse:
    settings = get_settings()
    session = repository.create_call_session(
        twilio_call_sid=payload.twilio_call_sid,
        caller_number=payload.caller_number,
        called_number=payload.called_number,
        voice_model=payload.voice_model or settings.xai_realtime_model,
        metadata=payload.metadata,
    )
    return CallSessionResponse(
        call_session_id=session["id"],
        twilio_call_sid=session["twilio_call_sid"],
        status=session["session_status"],
        media_stream_url=settings.twilio_media_stream_url,
    )


@router.post("/complete", response_model=CallSessionResponse)
def complete_call(payload: CallSessionComplete) -> CallSessionResponse:
    session = repository.update_call_session_status(
        call_session_id=payload.call_session_id,
        session_status=payload.session_status,
        ended_at=payload.ended_at or repository.utc_now_iso(),
        transcript_status=payload.transcript_status,
    )
    if not session:
        raise HTTPException(status_code=404, detail="Call session not found")
    return CallSessionResponse(
        call_session_id=session["id"],
        twilio_call_sid=session["twilio_call_sid"],
        status=session["session_status"],
    )
