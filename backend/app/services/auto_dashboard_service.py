from __future__ import annotations

import json
import re
from typing import Any

from app.db import repository
from app.services.delivery_service import send_dashboard_delivery
from app.services.integration_logger import log_step
from app.services.slug_service import generate_unique_dashboard_slug


def create_dashboard_from_call_output(call_output: dict[str, Any]) -> dict[str, Any]:
    call = call_output.get("call") or {}
    call_session_id = call.get("call_session_id")
    if not call_session_id:
        return {"status": "skipped", "reason": "missing_call_session_id"}

    existing = repository.get_dashboard_payload_record_by_call_session_id(call_session_id)
    if existing:
        return {
            "status": "existing",
            "dashboard_slug": existing["dashboard_slug"],
            "dashboard_payload_id": existing["id"],
        }

    transcript = ((call_output.get("transcript") or {}).get("raw") or "").strip()
    research = call_output.get("research") or {}
    official_analyses = _valid_official_analyses(research.get("official_page_analyses") or [])
    saved_dashboard = _saved_dashboard_result(research.get("all_tool_results") or [])
    if saved_dashboard:
        return {
            "status": "existing",
            "dashboard_slug": saved_dashboard["dashboard_slug"],
            "dashboard_payload_id": saved_dashboard.get("dashboard_payload_id"),
        }
    client = _extract_client(transcript, official_analyses)
    pain_points = _extract_pain_points(transcript)
    goals = _extract_goals(transcript)
    company_analysis = _company_analysis(official_analyses)
    improvement_tips = _improvement_tips(pain_points, transcript, company_analysis)
    summary = _summary(client, transcript, company_analysis, pain_points)

    profile = repository.create_client_profile(
        {
            "call_session_id": call_session_id,
            "full_name": client.get("full_name"),
            "role": client.get("role"),
            "email": client.get("email"),
            "phone": call.get("caller_number"),
            "company_name": client["business_name"],
            "website": client.get("website"),
            "city_or_location": None,
            "years_in_business": client.get("years_in_business"),
            "number_of_locations": None,
            "business_type": "IT services" if _contains(transcript, "it services") else None,
            "industry": "Technology",
            "service_summary": summary,
            "company_summary": summary,
            "key_frustrations": pain_points,
            "key_goals": goals,
            "ai_familiarity": _ai_familiarity(transcript),
            "current_systems": [],
            "lead_source": "inbound_call",
        }
    )
    slug = generate_unique_dashboard_slug(client["business_name"])
    public_payload = {
        "client": client,
        "company_summary": summary,
        "company_analysis": company_analysis,
        "digital_presence_notes": _digital_presence_notes(official_analyses),
        "website_notes": _website_notes(official_analyses),
        "google_presence_notes": _google_notes(research),
        "social_presence_notes": _social_notes(transcript),
        "main_opportunities": _opportunities(pain_points, transcript),
        "key_pain_points": pain_points,
        "improvement_tips": improvement_tips,
        "quick_wins": improvement_tips[:4],
        "next_steps": _next_steps(client, pain_points),
        "safe_metrics": {
            "ai_search_status": "Public website reviewed" if official_analyses else "Call transcript reviewed",
            "load_speed": "Not measured",
            "google_rating": "Not measured",
            "review_count": "Not measured",
        },
    }
    internal_payload = {
        "source": "auto_post_call_dashboard",
        "call": call,
        "transcript": transcript,
        "tool_results": research.get("all_tool_results") or [],
        "official_page_analyses": official_analyses,
    }
    dashboard = repository.create_dashboard_payload(
        client_profile_id=profile["id"],
        call_session_id=call_session_id,
        dashboard_slug=slug,
        public_payload=public_payload,
        internal_payload=internal_payload,
        conversation_summary=summary,
    )
    delivery_results = send_dashboard_delivery(
        dashboard_slug=slug,
        dashboard_payload_id=dashboard["id"],
        public_payload=public_payload,
        conversation_summary=summary,
        recipient={
            "email": client.get("email"),
            "phone": call.get("caller_number"),
            "name": client.get("full_name"),
        },
    )
    log_step(
        "auto dashboard result",
        status="created",
        call_session_id=call_session_id,
        dashboard_slug=slug,
        dashboard_payload_id=dashboard["id"],
    )
    return {
        "status": "created",
        "dashboard_slug": slug,
        "dashboard_payload_id": dashboard["id"],
        "client_profile_id": profile["id"],
        "delivery_results": delivery_results,
    }


def _extract_client(transcript: str, official_analyses: list[dict[str, Any]]) -> dict[str, Any]:
    name = _first_match(transcript, [r"my name is ([A-Za-z ]+?)(?:\.|\n|$)", r"this is ([A-Za-z ]+?)(?:\.|\n|$)"])
    business_name = _first_match(
        transcript,
        [
            r"(?:company|business|organization) name is ([A-Za-z0-9 &.-]+?)(?:\.|\n|,|$)",
            r"(?:company|business|organization) named ([A-Za-z0-9 &.-]+?)(?:\.|\n|,|$)",
            r"my company is ([A-Za-z0-9 &.-]+?)(?:\.|\n|,|$)",
            r"your company is ([A-Za-z0-9 &.-]+?)(?:\.|\n|,|$)",
            r"named ([A-Za-z0-9 &.-]+?)(?:\.|\n|,|$)",
        ],
    )
    if business_name and _looks_like_spoken_url(business_name):
        business_name = None
    website = _official_url(official_analyses)
    if not business_name and website:
        business_name = _domain_name(website)
    business_name = business_name or "Client Business"
    return {
        "full_name": _clean_person_name(name) if name else None,
        "role": "Owner / Founder" if _contains(transcript, "owner") or _contains(transcript, "founder") else None,
        "email": _extract_email(transcript),
        "business_name": _clean_business_name(business_name),
        "website": website,
        "city": None,
        "years_in_business": _years_in_business(transcript),
        "number_of_locations": None,
    }


def _extract_pain_points(transcript: str) -> list[str]:
    points: list[str] = []
    if _contains(transcript, "manual"):
        points.append("Manual work is slowing the team down.")
    if _contains(transcript, "time consuming") or _contains(transcript, "took time"):
        points.append("Important workflows are taking too much time to complete.")
    if _contains(transcript, "hr") and _contains(transcript, "onboarding"):
        points.append("HR onboarding is a time-consuming manual process.")
    if _contains(transcript, "not using ai"):
        points.append("The business has not yet adopted AI tools in daily operations.")
    return points or ["The call surfaced opportunities to reduce manual follow-up and improve operating efficiency."]


def _extract_goals(transcript: str) -> list[str]:
    goals: list[str] = []
    if _contains(transcript, "manual") or _contains(transcript, "time consuming"):
        goals.append("Reduce manual work and speed up internal workflows.")
    if _contains(transcript, "client"):
        goals.append("Improve service delivery for clients.")
    if _contains(transcript, "ai"):
        goals.append("Identify practical AI use cases that fit the business.")
    return goals or ["Create a clearer follow-up and improvement plan from the discovery call."]


def _company_analysis(official_analyses: list[dict[str, Any]]) -> list[str]:
    if not official_analyses:
        return ["No official website analysis was captured. This dashboard is based on the call transcript only."]
    analysis = official_analyses[-1]
    items: list[str] = []
    if analysis.get("summary"):
        items.append(str(analysis["summary"]))
    for observation in analysis.get("public_observations") or []:
        items.append(str(observation))
    return items[:5]


def _improvement_tips(pain_points: list[str], transcript: str, company_analysis: list[str]) -> list[str]:
    tips: list[str] = []
    if _contains(transcript, "hr") and _contains(transcript, "onboarding"):
        tips.extend(
            [
                "Create an AI-assisted HR onboarding intake that collects candidate and employee details once.",
                "Use workflow automation to route onboarding tasks, documents, and approvals to the right team members.",
            ]
        )
    if _contains(transcript, "manual"):
        tips.append("Map the most repeated manual steps and automate the first high-volume workflow before expanding.")
    if _contains(transcript, "not using ai"):
        tips.append("Start with a low-risk AI assistant for summarizing calls, documents, or onboarding checklists.")
    if company_analysis:
        tips.append("Align website messaging with the highest-value service areas mentioned during the call.")
    return tips[:5] or ["Turn the call transcript into a short action plan, then choose one workflow to automate first."]


def _summary(client: dict[str, Any], transcript: str, company_analysis: list[str], pain_points: list[str]) -> str:
    years = client.get("years_in_business")
    years_text = f" with about {years} years in business" if years else ""
    if company_analysis and "No official website analysis" not in company_analysis[0]:
        return f"{client['business_name']} appears to be an established business{years_text}. The call highlighted {pain_points[0].lower()} Public website analysis adds useful context for sharper improvement planning."
    return f"{client['business_name']} completed an AI discovery call{years_text}. The main opportunity is to reduce manual work and convert the call findings into practical next steps."


def _digital_presence_notes(official_analyses: list[dict[str, Any]]) -> list[str]:
    if not official_analyses:
        return ["Digital presence analysis was not completed during the call."]
    analysis = official_analyses[-1]
    notes = []
    if analysis.get("title"):
        notes.append(f"Official page title: {analysis['title']}")
    if analysis.get("description"):
        notes.append(f"Official page description: {analysis['description']}")
    return notes[:3]


def _website_notes(official_analyses: list[dict[str, Any]]) -> list[str]:
    if not official_analyses:
        return ["No official page was analyzed for this call."]
    analysis = official_analyses[-1]
    headings = analysis.get("headings") or []
    notes = [f"Prominent page heading: {heading}" for heading in headings[:4]]
    if analysis.get("same_domain_links"):
        notes.append(f"Found {len(analysis['same_domain_links'])} same-domain links for deeper follow-up review.")
    return notes[:5]


def _google_notes(research: dict[str, Any]) -> list[str]:
    tool_names = [item.get("tool_name") for item in research.get("all_tool_results") or []]
    if "web_search" in tool_names:
        return ["Native web search was requested during the call."]
    return ["No native web search result was captured in the local output."]


def _social_notes(transcript: str) -> list[str]:
    if _contains(transcript, "linkedin"):
        return ["Caller mentioned LinkedIn as an important presence or audience channel."]
    return []


def _opportunities(pain_points: list[str], transcript: str) -> list[str]:
    opportunities = ["Create a structured post-call follow-up workflow."]
    if _contains(transcript, "hr") and _contains(transcript, "onboarding"):
        opportunities.insert(0, "Automate HR onboarding intake, routing, and status tracking.")
    if _contains(transcript, "manual"):
        opportunities.append("Reduce manual task handoffs with simple workflow automation.")
    if _contains(transcript, "not using ai"):
        opportunities.append("Introduce AI gradually through one measurable internal use case.")
    return opportunities[:5]


def _next_steps(client: dict[str, Any], pain_points: list[str]) -> list[str]:
    return [
        f"Review the dashboard findings for {client['business_name']}.",
        "Choose the single most repetitive workflow to automate first.",
        "Prepare a simple before/after process map for the top pain point.",
    ]


def _ai_familiarity(transcript: str) -> str | None:
    if _contains(transcript, "not using ai") or _contains(transcript, "not use ai"):
        return "Not currently using AI."
    return None


def _official_url(official_analyses: list[dict[str, Any]]) -> str | None:
    for analysis in reversed(official_analyses):
        url = analysis.get("official_url")
        if isinstance(url, str) and url:
            return url
    return None


def _valid_official_analyses(analyses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        analysis
        for analysis in analyses
        if analysis.get("status") == "analyzed" and _is_valid_business_url(str(analysis.get("official_url") or ""))
    ]


def _saved_dashboard_result(tool_results: list[dict[str, Any]]) -> dict[str, Any] | None:
    for item in reversed(tool_results):
        if item.get("tool_name") == "save_dashboard_data" and isinstance(item.get("result"), dict):
            result = item["result"]
            if result.get("dashboard_slug"):
                return result
    return None


def _looks_like_spoken_url(value: str) -> bool:
    lowered = value.lower()
    return " dot " in lowered or lowered.startswith("www") or "." in lowered


def _is_valid_business_url(url: str) -> bool:
    host = re.sub(r"^https?://", "", url).split("/", 1)[0].removeprefix("www.").lower()
    blocked_hosts = {"gmail.com", "google.com", "accounts.google.com", "mail.google.com", "yahoo.com", "outlook.com"}
    return bool(host) and host not in blocked_hosts and not host.endswith("google.com")


def _domain_name(url: str) -> str:
    host = re.sub(r"^https?://", "", url).split("/", 1)[0].removeprefix("www.")
    return host.split(".", 1)[0].title()


def _years_in_business(transcript: str) -> int | None:
    match = re.search(r"(\d{1,3})\s+years?", transcript, re.IGNORECASE)
    return int(match.group(1)) if match else None


def _first_match(text: str, patterns: list[str]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def _contains(text: str, needle: str) -> bool:
    return needle.lower() in text.lower()


def _clean_person_name(name: str) -> str:
    return re.sub(r"[^A-Za-z ]+", "", name).strip().title()


def _clean_business_name(name: str) -> str:
    cleaned = re.sub(r"\s+", " ", name).strip(" .,")
    return cleaned[:80] or "Client Business"


def _extract_email(transcript: str) -> str | None:
    direct = re.search(r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}", transcript)
    if direct:
        return direct.group(0).lower()
    spoken = transcript.lower()
    match = re.search(r"([a-z0-9\s]+?)\s+at\s+([a-z0-9\s]+?)\s+dot\s+([a-z]{2,})", spoken)
    if not match:
        return None
    local = "".join(match.group(1).split())
    domain = "".join(match.group(2).split())
    tld = "".join(match.group(3).split())
    local = local.replace("double", "")
    return f"{local}@{domain}.{tld}"
