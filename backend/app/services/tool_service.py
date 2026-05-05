import re

from app.db import repository
from app.graph.workflow import run_intelligence_workflow
from app.schemas.tools import (
    CreateDashboardPayloadRequest,
    GenerateDashboardSlugRequest,
    SaveDashboardDataRequest,
)
from app.services.dashboard_service import build_internal_payload, build_public_dashboard_payload
from app.services.integration_logger import log_step
from app.services.post_call_service import trigger_post_call_flow
from app.services.slug_service import generate_unique_dashboard_slug


def generate_dashboard_slug(payload: GenerateDashboardSlugRequest) -> dict:
    slug = generate_unique_dashboard_slug(payload.business_name, payload.city)
    return {"dashboard_slug": slug}


def create_dashboard_payload(payload: CreateDashboardPayloadRequest) -> dict:
    public_payload = build_public_dashboard_payload(payload)
    return {"public_payload": public_payload}


def save_dashboard_data(payload: SaveDashboardDataRequest) -> dict:
    client = payload.client
    call_session_id = payload.call_session_id
    call_session = repository.get_call_session(call_session_id) if call_session_id else None
    resolved_email = _resolve_email(str(client.email) if client.email else None, payload.full_transcript)
    resolved_phone = client.phone or ((call_session or {}).get("caller_number"))

    if payload.full_transcript:
        workflow_state = run_intelligence_workflow(
            {
                "call_session_id": call_session_id,
                "transcript": payload.full_transcript,
                "transcript_summary": payload.conversation_summary,
                "extracted_fields": {
                    "client": client.model_dump(mode="json"),
                    "key_pain_points": payload.key_pain_points,
                    "key_goals": payload.key_goals,
                },
            }
        )
        transcript = repository.create_transcript(
            call_session_id=call_session_id,
            raw_transcript=payload.full_transcript,
            summary=workflow_state.get("transcript_summary") or payload.conversation_summary,
            extracted_fields=workflow_state.get("extracted_fields", {}),
        )
        log_step("transcript save result", call_session_id=call_session_id, transcript_id=transcript["id"])
    else:
        transcript = None
        workflow_state = run_intelligence_workflow(
            {
                "call_session_id": call_session_id,
                "transcript_summary": payload.conversation_summary,
                "extracted_fields": {"client": client.model_dump(mode="json")},
            }
        )

    profile = repository.create_client_profile(
        {
            "call_session_id": call_session_id,
            "full_name": client.full_name,
            "role": client.role,
            "email": resolved_email,
            "phone": resolved_phone,
            "company_name": client.business_name,
            "website": str(client.website) if client.website else None,
            "city_or_location": client.city,
            "years_in_business": client.years_in_business,
            "number_of_locations": client.number_of_locations,
            "key_frustrations": payload.key_pain_points,
            "key_goals": payload.key_goals,
            "ai_familiarity": payload.ai_familiarity,
            "current_systems": payload.current_systems,
            "lead_source": payload.lead_source,
        }
    )
    log_step("profile save result", call_session_id=call_session_id, client_profile_id=profile["id"])
    slug = generate_unique_dashboard_slug(client.business_name, client.city)
    log_step("dashboard slug result", dashboard_slug=slug)
    public_payload = build_public_dashboard_payload(payload)
    graph_payload = workflow_state.get("public_dashboard_payload") or {}
    if graph_payload:
        public_payload = {**graph_payload, **public_payload}
    internal_payload = build_internal_payload(payload)
    dashboard = repository.create_dashboard_payload(
        client_profile_id=profile["id"],
        call_session_id=call_session_id,
        dashboard_slug=slug,
        public_payload=public_payload,
        internal_payload=internal_payload,
        conversation_summary=payload.conversation_summary,
    )
    delivery_results = trigger_post_call_flow(
        dashboard_payload_id=dashboard["id"],
        dashboard_slug=slug,
        public_payload=public_payload,
        conversation_summary=payload.conversation_summary,
        recipient={
            "email": resolved_email,
            "phone": resolved_phone,
            "name": client.full_name,
        },
    )
    return {
        "dashboard_slug": slug,
        "client_profile_id": profile["id"],
        "dashboard_payload_id": dashboard["id"],
        "transcript_id": transcript["id"] if transcript else None,
        "public_payload": public_payload,
        "delivery_results": delivery_results,
    }


def _resolve_email(client_email: str | None, transcript: str | None) -> str | None:
    transcript_email = _extract_email_from_transcript(transcript or "")
    if transcript_email:
        return transcript_email
    return client_email


def _extract_email_from_transcript(transcript: str) -> str | None:
    direct = re.search(r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}", transcript)
    if direct:
        return direct.group(0).lower()
    spoken = transcript.lower()
    match = re.search(r"([a-z0-9\s]+?)\s+at\s+([a-z0-9\s]+?)\s+dot\s+([a-z]{2,})", spoken)
    if not match:
        return None
    local = "".join(match.group(1).split())
    domain = "".join(match.group(2).split())
    tld = "".join(match.group(3).split())
    local = local.replace("double", "")
    if not local or not domain or not tld:
        return None
    return f"{local}@{domain}.{tld}"
