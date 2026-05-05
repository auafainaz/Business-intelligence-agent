import json
from typing import Any

from pydantic import ValidationError

from app.schemas.tools import (
    AnalyzeOfficialPageRequest,
    CreateDashboardPayloadRequest,
    GenerateDashboardSlugRequest,
    SaveCallTranscriptRequest,
    SaveDashboardDataRequest,
    SendDashboardDeliveryRequest,
)
from app.services import delivery_service, official_page_research, tool_service, transcript_service


def execute_realtime_tool(name: str, raw_arguments: str | dict[str, Any]) -> dict[str, Any]:
    arguments = json.loads(raw_arguments) if isinstance(raw_arguments, str) and raw_arguments else raw_arguments
    arguments = arguments or {}
    try:
        if name == "save_dashboard_data":
            return tool_service.save_dashboard_data(SaveDashboardDataRequest(**arguments))
        if name == "save_call_transcript":
            result = transcript_service.save_call_transcript(SaveCallTranscriptRequest(**arguments))
            return {"transcript_id": result["id"]}
        if name == "create_dashboard_payload":
            return tool_service.create_dashboard_payload(CreateDashboardPayloadRequest(**arguments))
        if name == "generate_dashboard_slug":
            return tool_service.generate_dashboard_slug(GenerateDashboardSlugRequest(**arguments))
        if name == "analyze_official_page":
            return official_page_research.analyze_official_page(AnalyzeOfficialPageRequest(**arguments))
        if name == "send_dashboard_delivery":
            payload = SendDashboardDeliveryRequest(**arguments)
            return delivery_service.send_dashboard_delivery(
                dashboard_slug=payload.dashboard_slug,
                dashboard_payload_id=payload.dashboard_payload_id,
                public_payload=payload.public_payload,
                conversation_summary=payload.conversation_summary,
                recipient={
                    "email": payload.recipient_email,
                    "phone": payload.recipient_phone,
                    "name": payload.recipient_name,
                },
            )
        return {"error": f"Unknown tool: {name}"}
    except (json.JSONDecodeError, ValidationError, ValueError) as exc:
        return {"error": str(exc)}
