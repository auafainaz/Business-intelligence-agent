from typing import Any

from app.schemas.tools import CreateDashboardPayloadRequest, SaveDashboardDataRequest


def build_public_dashboard_payload(payload: SaveDashboardDataRequest | CreateDashboardPayloadRequest) -> dict[str, Any]:
    client = payload.client
    dashboard_data = payload.dashboard_data.model_dump(mode="json")
    return {
        "client": {
            "full_name": client.full_name,
            "role": client.role,
            "business_name": client.business_name,
            "website": str(client.website) if client.website else None,
            "city": client.city,
            "years_in_business": client.years_in_business,
            "number_of_locations": client.number_of_locations,
        },
        "company_summary": dashboard_data.get("public_summary") or payload.conversation_summary,
        "digital_presence_notes": dashboard_data.get("digital_presence_notes", []),
        "website_notes": dashboard_data.get("website_notes", []),
        "google_presence_notes": dashboard_data.get("google_presence_notes", []),
        "social_presence_notes": dashboard_data.get("social_presence_notes", []),
        "main_opportunities": dashboard_data.get("main_opportunities", []),
        "quick_wins": dashboard_data.get("quick_wins", []),
        "next_steps": dashboard_data.get("next_steps", []),
        "safe_metrics": {
            "google_rank": dashboard_data.get("google_rank"),
            "google_rating": dashboard_data.get("google_rating"),
            "review_count": dashboard_data.get("review_count"),
            "ai_search_status": dashboard_data.get("ai_search_status"),
            "website_traffic_estimate": dashboard_data.get("website_traffic_estimate"),
            "ai_website_agent": dashboard_data.get("ai_website_agent"),
            "load_speed": dashboard_data.get("load_speed"),
            "social_footprint": dashboard_data.get("social_footprint", {}),
        },
        "key_goals": payload.key_goals,
        "key_pain_points": payload.key_pain_points,
    }


def build_internal_payload(payload: SaveDashboardDataRequest) -> dict[str, Any]:
    return {
        "client": payload.client.model_dump(mode="json"),
        "conversation_summary": payload.conversation_summary,
        "key_pain_points": payload.key_pain_points,
        "key_goals": payload.key_goals,
        "ai_familiarity": payload.ai_familiarity,
        "current_systems": payload.current_systems,
        "dashboard_data": payload.dashboard_data.model_dump(mode="json"),
        "personal_touch": payload.personal_touch,
        "full_transcript": payload.full_transcript,
        "timestamp": payload.timestamp,
        "lead_source": payload.lead_source,
    }
