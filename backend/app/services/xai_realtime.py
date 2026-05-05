import json
from typing import Any

from app.config import get_settings
from app.services.prompt_loader import load_grok_system_prompt


def _tool_definition(
    name: str,
    description: str,
    parameters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "type": "function",
        "name": name,
        "description": description,
        "parameters": parameters or {"type": "object", "properties": {}},
    }


def load_save_dashboard_tool_schema() -> dict[str, Any]:
    settings = get_settings()
    return json.loads(settings.save_dashboard_schema_path.read_text(encoding="utf-8"))


def get_tool_registry() -> list[dict[str, Any]]:
    save_dashboard_schema = load_save_dashboard_tool_schema()
    return [
        {"type": "web_search"},
        # xAI web_search already exposes browsing behavior internally. Registering a
        # separate browse_page function creates a duplicate tool-name error.
        save_dashboard_schema,
        _tool_definition(
            "save_call_transcript",
            "Persist a call transcript and extracted fields for internal use.",
            {
                "type": "object",
                "properties": {
                    "call_session_id": {"type": "string"},
                    "raw_transcript": {"type": "string"},
                    "summary": {"type": "string"},
                    "extracted_fields": {"type": "object"},
                },
                "required": ["raw_transcript"],
            },
        ),
        _tool_definition(
            "create_dashboard_payload",
            "Map gathered call insights into public dashboard-safe data.",
            {"type": "object", "properties": {"client": {"type": "object"}, "dashboard_data": {"type": "object"}}},
        ),
        _tool_definition(
            "generate_dashboard_slug",
            "Generate a route-safe client dashboard slug.",
            {
                "type": "object",
                "properties": {"business_name": {"type": "string"}, "city": {"type": "string"}},
                "required": ["business_name"],
            },
        ),
        _tool_definition(
            "analyze_official_page",
            "Fetch and analyze the official public website page after web_search has identified the official URL.",
            {
                "type": "object",
                "properties": {
                    "official_url": {
                        "type": "string",
                        "description": "Official website URL found from native web_search.",
                    },
                    "organization_name": {"type": "string"},
                },
                "required": ["official_url"],
            },
        ),
        _tool_definition(
            "send_dashboard_delivery",
            "Send the saved dashboard link by Gmail and Twilio SMS after the dashboard slug has been created.",
            {
                "type": "object",
                "properties": {
                    "dashboard_slug": {"type": "string"},
                    "dashboard_payload_id": {"type": "string"},
                    "recipient_email": {"type": "string"},
                    "recipient_phone": {"type": "string"},
                    "recipient_name": {"type": "string"},
                    "conversation_summary": {"type": "string"},
                    "public_payload": {"type": "object"},
                },
                "required": ["dashboard_slug"],
            },
        ),
    ]


def build_xai_realtime_session_config(call_session_id: str | None = None) -> dict[str, Any]:
    settings = get_settings()
    return {
        "provider": "xai",
        "model": settings.xai_realtime_model,
        "voice": settings.xai_voice,
        "instructions": load_grok_system_prompt(),
        "audio": {
            "input": {"format": {"type": "audio/pcmu"}},
            "output": {"format": {"type": "audio/pcmu"}},
        },
        "tools": get_tool_registry(),
        "metadata": {
            "call_session_id": call_session_id,
            "agent_role": "single_supervisor_voice_agent",
            "phase": 3,
            "credential_status": "XAI_API_KEY is loaded server-side when configured in backend/.env",
        },
    }
