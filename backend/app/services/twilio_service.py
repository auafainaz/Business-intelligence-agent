from html import escape

from app.config import get_settings
from app.db import repository


def create_inbound_call_session(form_data: dict[str, str]) -> dict:
    settings = get_settings()
    call_sid = form_data.get("CallSid")
    if call_sid:
        existing = repository.find_call_session_by_twilio_sid(call_sid)
        if existing:
            return existing
    return repository.create_call_session(
        twilio_call_sid=call_sid,
        caller_number=form_data.get("From"),
        called_number=form_data.get("To"),
        voice_model=settings.xai_realtime_model,
        metadata={"twilio": form_data},
    )


def build_inbound_twiml(call_session_id: str) -> str:
    settings = get_settings()
    media_url = escape(settings.twilio_media_stream_url, quote=True)
    escaped_session = escape(call_session_id, quote=True)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <Stream url="{media_url}">
      <Parameter name="call_session_id" value="{escaped_session}" />
    </Stream>
  </Connect>
</Response>"""


def build_status_twiml() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?><Response></Response>"""
