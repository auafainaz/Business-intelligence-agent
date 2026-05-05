from fastapi import APIRouter

from app.schemas.delivery import DeliveryResponse, PostCallEventRequest
from app.services.post_call_service import trigger_post_call_flow

router = APIRouter(prefix="/automation", tags=["automation"])


@router.post("/post-call", response_model=DeliveryResponse)
def post_call_event(payload: PostCallEventRequest) -> DeliveryResponse:
    result = trigger_post_call_flow(
        dashboard_payload_id=payload.dashboard_payload_id,
        dashboard_slug=payload.dashboard_slug,
        public_payload=payload.public_payload,
        conversation_summary=payload.conversation_summary,
        recipient=payload.recipient,
    )
    return DeliveryResponse(ok=True, result=result)
