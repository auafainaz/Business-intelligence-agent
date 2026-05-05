from fastapi import APIRouter

from app.schemas.realtime import RealtimeSessionConfig
from app.services.xai_realtime import build_xai_realtime_session_config, get_tool_registry

router = APIRouter(prefix="/realtime", tags=["realtime"])


@router.get("/session-config", response_model=RealtimeSessionConfig)
def get_session_config(call_session_id: str | None = None) -> dict:
    return build_xai_realtime_session_config(call_session_id=call_session_id)


@router.get("/tools")
def list_realtime_tools() -> dict:
    tools = get_tool_registry()
    return {
        "tools": [
            {"name": tool.get("name") or tool.get("type"), "type": tool.get("type", "function")}
            for tool in tools
        ]
    }
