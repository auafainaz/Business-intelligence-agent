from app.config import get_settings


def load_grok_system_prompt() -> str:
    settings = get_settings()
    if not settings.grok_prompt_path.exists():
        raise FileNotFoundError(f"Grok runtime prompt not found: {settings.grok_prompt_path}")
    return settings.grok_prompt_path.read_text(encoding="utf-8").strip()
