from __future__ import annotations

from langgraph.graph import END, StateGraph

from app.graph.state import IntelligenceState


def transcript_intelligence_node(state: IntelligenceState) -> IntelligenceState:
    transcript = state.get("transcript") or ""
    summary = state.get("transcript_summary")
    if not summary and transcript:
        summary = transcript[:500]
    return {
        **state,
        "transcript_summary": summary,
        "extracted_fields": {
            **state.get("extracted_fields", {}),
            "phase": "phase_2_scaffold",
            "notes": "Replace deterministic extraction with provider-backed reasoning in Phase 3 if needed.",
        },
    }


def business_enrichment_node(state: IntelligenceState) -> IntelligenceState:
    # TODO: Wire xAI search/browse or backend research providers after credentials and network flow are approved.
    return {
        **state,
        "business_profile": state.get("business_profile", {"status": "not_enriched"}),
        "social_presence": state.get("social_presence", {"status": "not_enriched"}),
    }


def dashboard_payload_node(state: IntelligenceState) -> IntelligenceState:
    public_payload = state.get("public_dashboard_payload") or {
        "company_summary": state.get("transcript_summary"),
        "digital_presence_notes": [],
        "website_notes": [],
        "google_presence_notes": [],
        "social_presence_notes": [],
        "main_opportunities": [],
        "quick_wins": [],
        "next_steps": [],
    }
    return {**state, "public_dashboard_payload": public_payload}


def build_intelligence_graph():
    graph = StateGraph(IntelligenceState)
    graph.add_node("transcript_intelligence", transcript_intelligence_node)
    graph.add_node("business_enrichment", business_enrichment_node)
    graph.add_node("dashboard_payload", dashboard_payload_node)
    graph.set_entry_point("transcript_intelligence")
    graph.add_edge("transcript_intelligence", "business_enrichment")
    graph.add_edge("business_enrichment", "dashboard_payload")
    graph.add_edge("dashboard_payload", END)
    return graph.compile()


def run_intelligence_workflow(initial_state: IntelligenceState) -> IntelligenceState:
    workflow = build_intelligence_graph()
    return workflow.invoke(initial_state)
