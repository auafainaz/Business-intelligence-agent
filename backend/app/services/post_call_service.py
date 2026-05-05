from app.services.delivery_service import build_post_call_payload, run_post_call_delivery
from app.services.integration_logger import log_step


def trigger_post_call_flow(
    *,
    dashboard_payload_id: str,
    dashboard_slug: str,
    public_payload: dict,
    conversation_summary: str | None,
    recipient: dict,
) -> dict:
    payload = build_post_call_payload(
        dashboard_payload_id=dashboard_payload_id,
        dashboard_slug=dashboard_slug,
        public_payload=public_payload,
        conversation_summary=conversation_summary,
        recipient=recipient,
    )
    log_step("dashboard payload save result", dashboard_slug=dashboard_slug, dashboard_payload_id=dashboard_payload_id)
    return run_post_call_delivery(payload)
