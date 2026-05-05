from fastapi import APIRouter

from app.db.repository import list_delivery_records_for_slug
from app.schemas.delivery import DeliveryResponse, PostCallEventRequest
from app.services.delivery_service import (
    build_post_call_payload,
    send_gmail_post_call_email,
    send_dashboard_delivery,
    send_twilio_dashboard_sms,
)

router = APIRouter(prefix="/delivery", tags=["delivery"])


def _payload(payload: PostCallEventRequest) -> dict:
    return build_post_call_payload(
        dashboard_payload_id=payload.dashboard_payload_id,
        dashboard_slug=payload.dashboard_slug,
        public_payload=payload.public_payload,
        conversation_summary=payload.conversation_summary,
        recipient=payload.recipient,
    )


@router.post("/send-email", response_model=DeliveryResponse)
def send_email(payload: PostCallEventRequest) -> DeliveryResponse:
    return DeliveryResponse(ok=True, result=send_gmail_post_call_email(_payload(payload)))


@router.post("/send-sms", response_model=DeliveryResponse)
def send_sms(payload: PostCallEventRequest) -> DeliveryResponse:
    return DeliveryResponse(ok=True, result=send_twilio_dashboard_sms(_payload(payload)))


@router.post("/send-dashboard", response_model=DeliveryResponse)
def send_dashboard(payload: PostCallEventRequest) -> DeliveryResponse:
    return DeliveryResponse(
        ok=True,
        result=send_dashboard_delivery(
            dashboard_slug=payload.dashboard_slug,
            dashboard_payload_id=payload.dashboard_payload_id,
            public_payload=payload.public_payload,
            conversation_summary=payload.conversation_summary,
            recipient=payload.recipient,
        ),
    )


@router.get("/{dashboard_slug}", response_model=DeliveryResponse)
def list_deliveries(dashboard_slug: str) -> DeliveryResponse:
    return DeliveryResponse(ok=True, result={"deliveries": list_delivery_records_for_slug(dashboard_slug)})
