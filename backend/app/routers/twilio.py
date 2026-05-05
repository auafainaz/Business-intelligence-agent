from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import Response

from app.db import repository
from app.services.twilio_service import build_inbound_twiml, build_status_twiml, create_inbound_call_session
from app.services.xai_twilio_bridge import TwilioXaiBridge

router = APIRouter(prefix="/twilio", tags=["twilio"])


@router.post("/inbound")
async def inbound_call(request: Request) -> Response:
    form = await request.form()
    call_session = create_inbound_call_session({key: str(value) for key, value in form.items()})
    twiml = build_inbound_twiml(call_session["id"])
    return Response(content=twiml, media_type="application/xml")


@router.post("/status")
async def call_status(request: Request) -> Response:
    form = await request.form()
    call_sid = str(form.get("CallSid") or "")
    call_status_value = str(form.get("CallStatus") or "unknown")
    session = repository.find_call_session_by_twilio_sid(call_sid) if call_sid else None
    if session:
        ended_at = repository.utc_now_iso() if call_status_value in {"completed", "failed", "busy", "no-answer"} else None
        repository.update_call_session_status(
            call_session_id=session["id"],
            session_status=call_status_value,
            ended_at=ended_at,
        )
    return Response(content=build_status_twiml(), media_type="application/xml")


@router.websocket("/media")
async def twilio_media_stream(websocket: WebSocket) -> None:
    bridge = TwilioXaiBridge(websocket)
    await bridge.run()
