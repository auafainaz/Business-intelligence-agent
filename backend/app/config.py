from functools import lru_cache
from pathlib import Path
import os

from pydantic import BaseModel


def _resolve_path(value: str | Path, *, project_root: Path, backend_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    project_path = project_root / path
    if project_path.exists() or str(path).startswith(("docs", "frontend")):
        return project_path
    return backend_root / path


def _load_backend_env_file(backend_root: Path) -> None:
    env_path = backend_root / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ[key] = value


class Settings(BaseModel):
    app_name: str = "ClientIQ Backend"
    environment: str = "local"
    api_prefix: str = "/api"
    project_root: Path
    backend_root: Path
    database_path: Path
    local_call_output_dir: Path
    grok_prompt_path: Path
    save_dashboard_schema_path: Path
    xai_realtime_model: str = "grok-realtime"
    xai_voice: str = "alloy"
    xai_api_key: str | None = None
    xai_realtime_url: str = "wss://api.x.ai/v1/realtime"
    public_base_url: str = "http://localhost:8000"
    frontend_base_url: str = "http://localhost:3000"
    twilio_account_sid: str | None = None
    twilio_auth_token: str | None = None
    twilio_phone_number: str | None = None
    gmail_smtp_host: str = "smtp.gmail.com"
    gmail_smtp_port: int = 587
    gmail_username: str | None = None
    gmail_app_password: str | None = None
    gmail_from_email: str | None = None
    delivery_enabled: bool = True

    @property
    def twilio_media_stream_url(self) -> str:
        base_url = self.public_base_url.rstrip("/")
        if base_url.startswith("https://"):
            media_base_url = "wss://" + base_url.removeprefix("https://")
        elif base_url.startswith("http://"):
            media_base_url = "ws://" + base_url.removeprefix("http://")
        else:
            media_base_url = base_url
        return f"{media_base_url}{self.api_prefix}/twilio/media"

    def dashboard_url(self, slug: str) -> str:
        return f"{self.frontend_base_url.rstrip('/')}/dashboard/{slug}"


@lru_cache
def get_settings() -> Settings:
    backend_root = Path(__file__).resolve().parents[1]
    project_root = backend_root.parent
    _load_backend_env_file(backend_root)
    database_path = _resolve_path(
        os.getenv("DATABASE_PATH", backend_root / "data" / "clientiq.sqlite3"),
        project_root=project_root,
        backend_root=backend_root,
    )
    local_call_output_dir = _resolve_path(
        os.getenv("LOCAL_CALL_OUTPUT_DIR", backend_root / "outputs" / "calls"),
        project_root=project_root,
        backend_root=backend_root,
    )
    grok_prompt_path = _resolve_path(
        os.getenv("GROK_VOICE_PROMPT_PATH", backend_root / "prompts" / "grok-voice-system-prompt.md"),
        project_root=project_root,
        backend_root=backend_root,
    )
    save_dashboard_schema_path = _resolve_path(
        os.getenv("SAVE_DASHBOARD_SCHEMA_PATH", project_root / "docs" / "tool-schemas" / "save_dashboard_data.json"),
        project_root=project_root,
        backend_root=backend_root,
    )
    return Settings(
        environment=os.getenv("APP_ENV", "local"),
        project_root=project_root,
        backend_root=backend_root,
        database_path=database_path,
        local_call_output_dir=local_call_output_dir,
        grok_prompt_path=grok_prompt_path,
        save_dashboard_schema_path=save_dashboard_schema_path,
        xai_realtime_model=os.getenv("XAI_REALTIME_MODEL", "grok-realtime"),
        xai_voice=os.getenv("XAI_REALTIME_VOICE", "ara").strip().lower(),
        xai_api_key=os.getenv("XAI_API_KEY"),
        xai_realtime_url=os.getenv("XAI_REALTIME_URL", "wss://api.x.ai/v1/realtime"),
        public_base_url=os.getenv("PUBLIC_BASE_URL", "http://localhost:8000"),
        frontend_base_url=os.getenv("FRONTEND_BASE_URL", os.getenv("PUBLIC_FRONTEND_BASE_URL", "http://localhost:3000")),
        twilio_account_sid=os.getenv("TWILIO_ACCOUNT_SID"),
        twilio_auth_token=os.getenv("TWILIO_AUTH_TOKEN"),
        twilio_phone_number=os.getenv("TWILIO_PHONE_NUMBER"),
        gmail_smtp_host=os.getenv("GMAIL_SMTP_HOST", "smtp.gmail.com"),
        gmail_smtp_port=int(os.getenv("GMAIL_SMTP_PORT", "587")),
        gmail_username=os.getenv("GMAIL_USERNAME"),
        gmail_app_password=os.getenv("GMAIL_APP_PASSWORD"),
        gmail_from_email=os.getenv("GMAIL_FROM_EMAIL") or os.getenv("GMAIL_USERNAME"),
        delivery_enabled=os.getenv("DELIVERY_ENABLED", "true").strip().lower() in {"1", "true", "yes", "on"},
    )
