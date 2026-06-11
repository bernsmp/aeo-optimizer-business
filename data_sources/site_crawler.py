"""Crawl a URL and extract AEO-relevant signals."""

import json
import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

try:
    import extruct
    from w3lib.html import get_base_url
    HAS_EXTRUCT = True
except ImportError:
    HAS_EXTRUCT = False

USER_AGENT = "AEO-Scorer/1.0 (+https://maixaeo.com)"
TIMEOUT = 15


def crawl_url(url: str) -> dict:
    """Crawl a URL and return structured AEO-relevant data.

    Returns a dict with keys:
        url, domain, title, meta_description, headings, faq_items,
        json_ld_schemas, robots_txt, llms_txt, sitemap_referenced,
        raw_html, errors
    """
    result = {
        "url": url,
        "domain": urlparse(url).netloc,
        "title": "",
        "meta_description": "",
        "headings": {"h1": [], "h2": [], "h3": []},
        "faq_items": [],
        "json_ld_schemas": [],
        "microdata_schemas": [],
        "opengraph": [],
        "robots_txt": None,
        "llms_txt": None,
        "sitemap_referenced": False,
        "http_last_modified": None,
        "freshness_signals": {},
        "ai_access_check": {},
        "raw_html": "",
        "errors": [],
    }

    # --- Fetch main page ---
    soup = _fetch_page(url, result)
    if soup:
        _extract_meta(soup, result)
        _extract_headings(soup, result)
        _extract_faq_items(soup, result)
        _extract_json_ld(soup, result)
        _extract_with_extruct(url, result)
        _extract_freshness(soup, result)

    # --- Check domain-level files ---
    base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    _check_robots_txt(base_url, result)
    _check_llms_txt(base_url, result)
    _check_ai_access(base_url, result)

    return result


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _fetch_page(url: str, result: dict) -> BeautifulSoup | None:
    """Fetch page HTML and return a BeautifulSoup object."""
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
        resp.raise_for_status()
        result["raw_html"] = resp.text
        result["http_last_modified"] = resp.headers.get("Last-Modified")
        return BeautifulSoup(resp.text, "html.parser")
    except requests.RequestException as exc:
        result["errors"].append(f"Failed to fetch {url}: {exc}")
        return None


def _extract_meta(soup: BeautifulSoup, result: dict):
    """Pull title and meta description."""
    title_tag = soup.find("title")
    if title_tag:
        result["title"] = title_tag.get_text(strip=True)

    meta_desc = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    if meta_desc:
        result["meta_description"] = meta_desc.get("content", "")


def _extract_headings(soup: BeautifulSoup, result: dict):
    """Extract h1, h2, h3 text."""
    for level in ("h1", "h2", "h3"):
        result["headings"][level] = [
            tag.get_text(strip=True) for tag in soup.find_all(level)
        ]


def _extract_faq_items(soup: BeautifulSoup, result: dict):
    """Detect FAQ-style content from multiple common patterns."""
    faq_items = []

    # Pattern 1: JSON-LD FAQPage (handled separately, but also grab here for content)
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
            items = _faq_from_jsonld(data)
            faq_items.extend(items)
        except (json.JSONDecodeError, TypeError):
            continue

    # Pattern 2: HTML elements with FAQ-like structure
    # Look for <details>/<summary>, accordion patterns, or Q&A sections
    for details in soup.find_all("details"):
        summary = details.find("summary")
        if summary:
            answer_parts = []
            for child in details.children:
                if child != summary and hasattr(child, "get_text"):
                    text = child.get_text(strip=True)
                    if text:
                        answer_parts.append(text)
            answer = " ".join(answer_parts)
            if answer:
                faq_items.append({
                    "question": summary.get_text(strip=True),
                    "answer": answer,
                    "source": "html-details",
                })

    # Pattern 3: Headings that look like questions followed by paragraph answers
    faq_section_found = False
    for heading in soup.find_all(re.compile(r"^h[1-4]$")):
        heading_text = heading.get_text(strip=True)
        # Check if we're in an FAQ section
        if re.search(r"\bfaq|frequently\s+asked|questions\b", heading_text, re.I):
            faq_section_found = True
            continue
        # If heading looks like a question (ends with ? or starts with common Q words)
        if heading_text.endswith("?") or re.match(
            r"^(what|how|why|when|where|who|can|do|does|is|are|should|will)\b",
            heading_text, re.I
        ):
            # Grab sibling paragraphs as the answer
            answer_parts = []
            for sib in heading.find_next_siblings():
                if sib.name and re.match(r"^h[1-4]$", sib.name):
                    break
                text = sib.get_text(strip=True)
                if text:
                    answer_parts.append(text)
            answer = " ".join(answer_parts)
            if answer:
                faq_items.append({
                    "question": heading_text,
                    "answer": answer,
                    "source": "html-heading",
                })

    # Deduplicate by question text
    seen = set()
    unique = []
    for item in faq_items:
        q_lower = item["question"].lower().strip()
        if q_lower not in seen:
            seen.add(q_lower)
            unique.append(item)
    result["faq_items"] = unique


def _faq_from_jsonld(data) -> list[dict]:
    """Extract FAQ items from a JSON-LD object (handles nested @graph)."""
    items = []
    objects = [data] if isinstance(data, dict) else data if isinstance(data, list) else []

    for obj in objects:
        if not isinstance(obj, dict):
            continue
        schema_type = obj.get("@type", "")
        if isinstance(schema_type, list):
            schema_type = " ".join(schema_type)

        if "FAQPage" in schema_type:
            for entry in obj.get("mainEntity", []):
                q = entry.get("name", "")
                a_obj = entry.get("acceptedAnswer", {})
                a = a_obj.get("text", "") if isinstance(a_obj, dict) else ""
                if q:
                    items.append({"question": q, "answer": a, "source": "json-ld"})

        # Recurse into @graph
        if "@graph" in obj:
            items.extend(_faq_from_jsonld(obj["@graph"]))

    return items


def _extract_json_ld(soup: BeautifulSoup, result: dict):
    """Parse all JSON-LD blocks and store them."""
    schemas = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
            schemas.append(data)
        except (json.JSONDecodeError, TypeError) as exc:
            result["errors"].append(f"Invalid JSON-LD block: {exc}")
    result["json_ld_schemas"] = schemas


def _check_robots_txt(base_url: str, result: dict):
    """Fetch robots.txt and store its content."""
    robots_url = f"{base_url}/robots.txt"
    try:
        resp = requests.get(
            robots_url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT
        )
        if resp.status_code == 200 and "text" in resp.headers.get("content-type", ""):
            result["robots_txt"] = resp.text
            # Check if sitemap is referenced
            if re.search(r"^sitemap:", resp.text, re.I | re.M):
                result["sitemap_referenced"] = True
        else:
            result["robots_txt"] = None
    except requests.RequestException as exc:
        result["errors"].append(f"Failed to fetch robots.txt: {exc}")


def _check_llms_txt(base_url: str, result: dict):
    """Fetch llms.txt and store its content."""
    llms_url = f"{base_url}/llms.txt"
    try:
        resp = requests.get(
            llms_url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT
        )
        if resp.status_code == 200 and len(resp.text.strip()) > 0:
            result["llms_txt"] = resp.text
        else:
            result["llms_txt"] = None
    except requests.RequestException as exc:
        result["errors"].append(f"Failed to fetch llms.txt: {exc}")


def _extract_with_extruct(url: str, result: dict):
    """Use extruct to pull microdata, RDFa, and OpenGraph (if available)."""
    if not HAS_EXTRUCT or not result["raw_html"]:
        return

    try:
        base_url = get_base_url(result["raw_html"], url)
        data = extruct.extract(
            result["raw_html"],
            base_url=base_url,
            syntaxes=["microdata", "opengraph", "rdfa"],
            uniform=True,
        )
        result["microdata_schemas"] = data.get("microdata", [])
        result["opengraph"] = data.get("opengraph", [])

        # Merge any microdata schema types into json_ld_schemas for unified analysis
        # (schema_detector already handles JSON-LD; microdata is the gap we're filling)
    except Exception as exc:
        result["errors"].append(f"extruct extraction failed: {exc}")


def _extract_freshness(soup: BeautifulSoup, result: dict):
    """Collect machine-readable date signals (JSON-LD, meta tags, <time>).

    Freshness matters: ~65% of AI bot hits target content under 12 months
    old (Seer Interactive, 2026). A site with no machine-readable dates
    can't prove freshness to an answer engine at all.
    """
    dates: list[tuple[str, str]] = []  # (iso_date, source)
    date_re = re.compile(r"(\d{4}-\d{2}-\d{2})")

    def _add(value, source):
        if not value or not isinstance(value, str):
            return
        m = date_re.search(value)
        if m:
            dates.append((m.group(1), source))

    # JSON-LD datePublished / dateModified (recursive)
    def _walk(obj):
        if isinstance(obj, dict):
            for key in ("dateModified", "datePublished", "dateCreated"):
                _add(obj.get(key), f"json-ld:{key}")
            for v in obj.values():
                _walk(v)
        elif isinstance(obj, list):
            for v in obj:
                _walk(v)

    for schema in result.get("json_ld_schemas", []):
        _walk(schema)

    # Meta tags (OpenGraph / article)
    for prop in ("article:modified_time", "article:published_time", "og:updated_time"):
        tag = soup.find("meta", attrs={"property": prop}) or soup.find("meta", attrs={"name": prop})
        if tag:
            _add(tag.get("content", ""), f"meta:{prop}")

    # <time datetime="..."> elements
    for time_tag in soup.find_all("time")[:20]:
        _add(time_tag.get("datetime", ""), "html:time")

    # HTTP Last-Modified header (weakest signal -- often server time, not content time)
    _add(result.get("http_last_modified") or "", "http:last-modified")

    if dates:
        dates.sort(reverse=True)
        result["freshness_signals"] = {
            "most_recent": dates[0][0],
            "most_recent_source": dates[0][1],
            "dates_found": len(dates),
            "sources": sorted({s for _, s in dates}),
        }
    else:
        result["freshness_signals"] = {
            "most_recent": None,
            "dates_found": 0,
            "sources": [],
        }


# User-agent strings mimicking real AI crawlers, used only to detect
# edge-level (CDN/WAF) filtering of AI traffic.
AI_TEST_AGENTS = {
    "GPTBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.3; +https://openai.com/gptbot",
    "PerplexityBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)",
}

BLOCK_STATUSES = {401, 403, 405, 406, 429, 503}


def _check_ai_access(base_url: str, result: dict):
    """Detect CDN/edge-level blocking of AI crawler user-agents.

    Cloudflare default-blocks unverified AI crawlers for new domains (2025+),
    so a robots.txt that says "Allow" can be silently overridden at the edge.
    This is a differential test: if the normal UA gets a 2xx/3xx but an AI UA
    gets 401/403/429/503, some edge rule is filtering on AI user-agents.

    Caveat (recorded in the result): real crawlers verify via Web Bot Auth /
    published IP ranges, so a spoofed UA being blocked doesn't always mean
    the verified bot is blocked. Differential blocking is a warning to
    confirm in the CDN dashboard or server logs, not a definitive verdict.
    """
    check = {
        "baseline_status": None,
        "results": {},
        "edge_filtering_detected": False,
        "note": (
            "UA-differential test. A blocked spoofed UA may pass as a verified bot; "
            "confirm in CDN dashboard (e.g. Cloudflare AI Crawl Control) or server logs."
        ),
    }

    try:
        baseline = requests.get(
            base_url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT, allow_redirects=True
        )
        check["baseline_status"] = baseline.status_code
    except requests.RequestException as exc:
        result["errors"].append(f"AI access baseline fetch failed: {exc}")
        result["ai_access_check"] = check
        return

    for bot, ua in AI_TEST_AGENTS.items():
        try:
            resp = requests.get(
                base_url, headers={"User-Agent": ua}, timeout=TIMEOUT, allow_redirects=True
            )
            check["results"][bot] = resp.status_code
        except requests.RequestException:
            check["results"][bot] = None

    if check["baseline_status"] and check["baseline_status"] < 400:
        blocked = [
            bot for bot, status in check["results"].items()
            if status in BLOCK_STATUSES
        ]
        if blocked:
            check["edge_filtering_detected"] = True
            check["blocked_agents"] = blocked

    result["ai_access_check"] = check


if __name__ == "__main__":
    import sys

    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    data = crawl_url(url)
    # Print summary (skip raw_html for readability)
    summary = {k: v for k, v in data.items() if k != "raw_html"}
    print(json.dumps(summary, indent=2, default=str))
