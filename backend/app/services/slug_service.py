import re

from app.db import repository


def _slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "client"


def generate_unique_dashboard_slug(business_name: str, city: str | None = None) -> str:
    base = _slugify(f"{business_name} {city or ''}")
    slug = base
    suffix = 2
    while repository.dashboard_slug_exists(slug):
        slug = f"{base}-{suffix}"
        suffix += 1
    return slug
