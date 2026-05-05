from __future__ import annotations

from langgraph.graph import END, StateGraph

from app.graph.state import ArchitectureState


def _advance(state: ArchitectureState, stage: str) -> ArchitectureState:
    return {
        **state,
        "current_stage": stage,
        "stage_log": [*state.get("stage_log", []), stage],
    }


def public_website_node(state: ArchitectureState) -> ArchitectureState:
    return _advance(state, "public_website_phone_cta")


def twilio_inbound_node(state: ArchitectureState) -> ArchitectureState:
    return _advance(state, "twilio_inbound_voice_call")


def realtime_voice_node(state: ArchitectureState) -> ArchitectureState:
    return _advance(state, "xai_grok_realtime_supervisor_agent")


def live_research_node(state: ArchitectureState) -> ArchitectureState:
    return _advance(state, "official_website_live_research")


def backend_tools_node(state: ArchitectureState) -> ArchitectureState:
    return _advance(state, "fastapi_tool_processing")


def intelligence_workflow_node(state: ArchitectureState) -> ArchitectureState:
    return _advance(state, "langgraph_post_call_intelligence")


def sqlite_persistence_node(state: ArchitectureState) -> ArchitectureState:
    next_state = _advance(state, "sqlite_public_internal_persistence")
    return {
        **next_state,
        "public_dashboard_ready": True,
        "internal_record_ready": True,
    }


def dashboard_route_node(state: ArchitectureState) -> ArchitectureState:
    return _advance(state, "dashboard_slug_route_rendering")


def direct_delivery_node(state: ArchitectureState) -> ArchitectureState:
    next_state = _advance(state, "direct_gmail_twilio_sms_delivery")
    return {**next_state, "delivery_ready": True}


def local_output_node(state: ArchitectureState) -> ArchitectureState:
    return _advance(state, "local_json_call_output")


def build_project_architecture_graph():
    graph = StateGraph(ArchitectureState)
    graph.add_node("public_website", public_website_node)
    graph.add_node("twilio_inbound", twilio_inbound_node)
    graph.add_node("realtime_voice", realtime_voice_node)
    graph.add_node("live_research", live_research_node)
    graph.add_node("backend_tools", backend_tools_node)
    graph.add_node("intelligence_workflow", intelligence_workflow_node)
    graph.add_node("sqlite_persistence", sqlite_persistence_node)
    graph.add_node("dashboard_route", dashboard_route_node)
    graph.add_node("direct_delivery", direct_delivery_node)
    graph.add_node("local_output", local_output_node)

    graph.set_entry_point("public_website")
    graph.add_edge("public_website", "twilio_inbound")
    graph.add_edge("twilio_inbound", "realtime_voice")
    graph.add_edge("realtime_voice", "live_research")
    graph.add_edge("live_research", "backend_tools")
    graph.add_edge("backend_tools", "intelligence_workflow")
    graph.add_edge("intelligence_workflow", "sqlite_persistence")
    graph.add_edge("sqlite_persistence", "dashboard_route")
    graph.add_edge("dashboard_route", "direct_delivery")
    graph.add_edge("direct_delivery", "local_output")
    graph.add_edge("local_output", END)
    return graph.compile()


def run_project_architecture_graph(initial_state: ArchitectureState | None = None) -> ArchitectureState:
    workflow = build_project_architecture_graph()
    return workflow.invoke(initial_state or {"stage_log": []})
