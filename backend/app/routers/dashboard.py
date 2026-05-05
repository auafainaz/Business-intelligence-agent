from fastapi import APIRouter, HTTPException

from app.db.repository import get_public_dashboard_payload
from app.schemas.dashboard import PublicDashboardResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/{dashboard_slug}", response_model=PublicDashboardResponse)
def get_dashboard_payload(dashboard_slug: str) -> dict:
    payload = get_public_dashboard_payload(dashboard_slug)
    if not payload:
        raise HTTPException(status_code=404, detail="Dashboard payload not found")
    return payload
