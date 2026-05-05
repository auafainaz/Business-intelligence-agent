from app.schemas.tools import ExtractSocialPresenceRequest, LookupBusinessProfileRequest


def lookup_business_profile(payload: LookupBusinessProfileRequest) -> dict:
    # Scaffold only. Live voice research currently uses xAI native web_search.
    return {
        "business_name": payload.business_name,
        "website": str(payload.website) if payload.website else None,
        "city": payload.city,
        "status": "scaffold_only",
        "public_sources": [],
        "profile": {
            "services": [],
            "positioning": None,
            "locations": [],
            "notes": ["Backend scripted public research is disabled while native web_search is being validated."],
        },
    }


def extract_social_presence(payload: ExtractSocialPresenceRequest) -> dict:
    # Scaffold only. Live voice research currently uses xAI native web_search.
    known_links = [str(link) for link in payload.known_links]
    return {
        "business_name": payload.business_name,
        "website": str(payload.website) if payload.website else None,
        "status": "scaffold_only",
        "social_links": known_links,
        "signals": {
            "linkedin": None,
            "facebook": None,
            "instagram": None,
            "other": [],
        },
    }
