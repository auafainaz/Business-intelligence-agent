from fastapi import FastAPI
import logging

from app.config import get_settings
from app.db.connection import init_db
from app.routers import automation, calls, dashboard, delivery, health, realtime, tools, twilio


def create_app() -> FastAPI:
    settings = get_settings()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    app = FastAPI(
        title=settings.app_name,
        version="0.3.0",
        description="Phase 3 integrated backend for the ClientIQ realtime voice and dashboard flow.",
    )

    @app.on_event("startup")
    def startup() -> None:
        init_db()

    app.include_router(health.router, prefix=settings.api_prefix)
    app.include_router(calls.router, prefix=settings.api_prefix)
    app.include_router(tools.router, prefix=settings.api_prefix)
    app.include_router(twilio.router, prefix=settings.api_prefix)
    app.include_router(realtime.router, prefix=settings.api_prefix)
    app.include_router(dashboard.router, prefix=settings.api_prefix)
    app.include_router(automation.router, prefix=settings.api_prefix)
    app.include_router(delivery.router, prefix=settings.api_prefix)
    return app


app = create_app()
