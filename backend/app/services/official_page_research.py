from __future__ import annotations

from html.parser import HTMLParser
from typing import Any
from urllib.parse import urljoin, urlparse

import httpx

from app.schemas.tools import AnalyzeOfficialPageRequest
from app.services.integration_logger import log_step


class OfficialPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.description = ""
        self.headings: list[str] = []
        self.links: list[str] = []
        self._tag_stack: list[str] = []
        self._capture_title = False
        self._capture_heading = False
        self._text_parts: list[str] = []
        self._current_heading: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._tag_stack.append(tag)
        attrs_dict = {key.lower(): value or "" for key, value in attrs}
        if tag == "title":
            self._capture_title = True
        elif tag in {"h1", "h2", "h3"}:
            self._capture_heading = True
            self._current_heading = []
        elif tag == "meta" and attrs_dict.get("name", "").lower() == "description":
            self.description = attrs_dict.get("content", "").strip()
        elif tag == "a" and attrs_dict.get("href"):
            self.links.append(attrs_dict["href"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._capture_title = False
        elif tag in {"h1", "h2", "h3"} and self._capture_heading:
            heading = _clean_text(" ".join(self._current_heading))
            if heading:
                self.headings.append(heading)
            self._capture_heading = False
            self._current_heading = []
        if self._tag_stack:
            self._tag_stack.pop()

    def handle_data(self, data: str) -> None:
        active = self._tag_stack[-1] if self._tag_stack else ""
        if active in {"script", "style", "noscript", "svg"}:
            return
        clean = _clean_text(data)
        if not clean:
            return
        if self._capture_title:
            self.title = _clean_text(f"{self.title} {clean}")
        elif self._capture_heading:
            self._current_heading.append(clean)
        else:
            self._text_parts.append(clean)

    @property
    def visible_text(self) -> str:
        return _clean_text(" ".join(self._text_parts))


def analyze_official_page(payload: AnalyzeOfficialPageRequest) -> dict[str, Any]:
    url = str(payload.official_url)
    normalized_url = _normalize_url(url)
    try:
        response = httpx.get(
            normalized_url,
            follow_redirects=True,
            timeout=15,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (compatible; FainazClientIQ/0.1; "
                    "+https://owneriqai.com)"
                )
            },
        )
        response.raise_for_status()
    except Exception as exc:
        log_step("official page research result", status="failed", url=normalized_url, error=str(exc))
        return {"status": "failed", "official_url": normalized_url, "error": str(exc)}

    parser = OfficialPageParser()
    parser.feed(response.text[:500_000])
    final_url = str(response.url)
    same_domain_links = _same_domain_links(final_url, parser.links)
    social_links = _social_links(final_url, parser.links)
    summary = _build_summary(
        organization_name=payload.organization_name,
        title=parser.title,
        description=parser.description,
        headings=parser.headings,
        visible_text=parser.visible_text,
    )
    result = {
        "status": "analyzed",
        "official_url": final_url,
        "http_status": response.status_code,
        "title": parser.title,
        "description": parser.description,
        "headings": parser.headings[:12],
        "summary": summary,
        "public_observations": _public_observations(parser.description, parser.headings, parser.visible_text),
        "live_conversation_hooks": _live_conversation_hooks(
            title=parser.title,
            description=parser.description,
            headings=parser.headings,
            visible_text=parser.visible_text,
        ),
        "same_domain_links": same_domain_links[:10],
        "social_links": social_links[:10],
    }
    log_step(
        "official page research result",
        status="analyzed",
        url=final_url,
        heading_count=len(parser.headings),
        same_domain_link_count=len(same_domain_links),
    )
    return result


def _normalize_url(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme:
        return f"https://{url}"
    return url


def _clean_text(value: str) -> str:
    return " ".join(value.split())


def _same_domain_links(base_url: str, links: list[str]) -> list[str]:
    base_host = urlparse(base_url).netloc.lower().removeprefix("www.")
    results: list[str] = []
    for link in links:
        absolute = urljoin(base_url, link)
        parsed = urlparse(absolute)
        host = parsed.netloc.lower().removeprefix("www.")
        if host == base_host and absolute not in results:
            results.append(absolute)
    return results


def _social_links(base_url: str, links: list[str]) -> list[str]:
    social_hosts = ("linkedin.com", "facebook.com", "instagram.com", "x.com", "twitter.com", "youtube.com")
    results: list[str] = []
    for link in links:
        absolute = urljoin(base_url, link)
        host = urlparse(absolute).netloc.lower()
        if any(social_host in host for social_host in social_hosts) and absolute not in results:
            results.append(absolute)
    return results


def _public_observations(description: str, headings: list[str], visible_text: str) -> list[str]:
    observations: list[str] = []
    if description:
        observations.append(f"Meta description says: {description[:220]}")
    for heading in headings[:4]:
        observations.append(f"Page heading: {heading[:180]}")
    if not observations and visible_text:
        observations.append(f"Visible page copy starts with: {visible_text[:220]}")
    return observations[:5]


def _live_conversation_hooks(
    *,
    title: str,
    description: str,
    headings: list[str],
    visible_text: str,
) -> list[str]:
    hooks: list[str] = []
    if title:
        hooks.append(f"The website headline/title is focused on: {title[:140]}")
    if description:
        hooks.append(f"The public website positioning says: {description[:180]}")
    for heading in headings[:3]:
        hooks.append(f"A prominent website section says: {heading[:140]}")
    if not hooks and visible_text:
        hooks.append(f"The public website copy starts with: {visible_text[:180]}")
    return hooks[:4]


def _build_summary(
    *,
    organization_name: str | None,
    title: str,
    description: str,
    headings: list[str],
    visible_text: str,
) -> str:
    subject = organization_name or "The organization"
    evidence = description or ". ".join(headings[:3]) or visible_text[:240]
    if not evidence:
        return f"{subject} has an official page, but the page did not expose enough readable text to summarize."
    return f"{subject} official page presents: {evidence[:450]}"
