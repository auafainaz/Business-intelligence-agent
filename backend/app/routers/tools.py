from fastapi import APIRouter, HTTPException

from app.graph.workflow import run_intelligence_workflow
from app.schemas.tools import (
    AnalyzeOfficialPageRequest,
    CreateDashboardPayloadRequest,
    ExtractSocialPresenceRequest,
    GenerateDashboardSlugRequest,
    LookupBusinessProfileRequest,
    SaveCallTranscriptRequest,
    SaveDashboardDataRequest,
    ToolResponse,
)
from app.services import business_enrichment, official_page_research, tool_service, transcript_service

router = APIRouter(prefix="/tools", tags=["tools"])


def _ok(tool: str, result: dict) -> ToolResponse:
    return ToolResponse(ok=True, tool=tool, result=result)


@router.post("/save-dashboard-data", response_model=ToolResponse)
def save_dashboard_data(payload: SaveDashboardDataRequest) -> ToolResponse:
    result = tool_service.save_dashboard_data(payload)
    return _ok("save_dashboard_data", result)


@router.post("/save-call-transcript", response_model=ToolResponse)
def save_call_transcript(payload: SaveCallTranscriptRequest) -> ToolResponse:
    result = transcript_service.save_call_transcript(payload)
    return _ok("save_call_transcript", {"transcript_id": result["id"]})


@router.post("/create-dashboard-payload", response_model=ToolResponse)
def create_dashboard_payload(payload: CreateDashboardPayloadRequest) -> ToolResponse:
    result = tool_service.create_dashboard_payload(payload)
    return _ok("create_dashboard_payload", result)


@router.post("/generate-dashboard-slug", response_model=ToolResponse)
def generate_dashboard_slug(payload: GenerateDashboardSlugRequest) -> ToolResponse:
    return _ok("generate_dashboard_slug", tool_service.generate_dashboard_slug(payload))


@router.post("/lookup-business-profile", response_model=ToolResponse)
def lookup_business_profile(payload: LookupBusinessProfileRequest) -> ToolResponse:
    return _ok("lookup_business_profile", business_enrichment.lookup_business_profile(payload))


@router.post("/extract-social-presence", response_model=ToolResponse)
def extract_social_presence(payload: ExtractSocialPresenceRequest) -> ToolResponse:
    return _ok("extract_social_presence", business_enrichment.extract_social_presence(payload))


@router.post("/analyze-official-page", response_model=ToolResponse)
def analyze_official_page(payload: AnalyzeOfficialPageRequest) -> ToolResponse:
    return _ok("analyze_official_page", official_page_research.analyze_official_page(payload))


@router.post("/run-intelligence-workflow", response_model=ToolResponse)
def run_workflow(payload: SaveCallTranscriptRequest) -> ToolResponse:
    try:
        result = run_intelligence_workflow(
            {
                "call_session_id": payload.call_session_id,
                "transcript": payload.raw_transcript,
                "transcript_summary": payload.summary,
                "extracted_fields": payload.extracted_fields,
            }
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"LangGraph workflow failed: {exc}") from exc
    return _ok("run_intelligence_workflow", dict(result))
