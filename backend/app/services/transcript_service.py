from app.db import repository
from app.schemas.tools import SaveCallTranscriptRequest


def save_call_transcript(payload: SaveCallTranscriptRequest) -> dict:
    return repository.create_transcript(
        call_session_id=payload.call_session_id,
        raw_transcript=payload.raw_transcript,
        summary=payload.summary,
        extracted_fields=payload.extracted_fields,
    )
