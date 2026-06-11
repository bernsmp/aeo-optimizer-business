"""Detect existing schemas and identify gaps."""

import json
import re
from datetime import datetime


# Schema types we care about for AEO, grouped by category
SCHEMA_TYPES = {
    "identity": ["Organization", "LocalBusiness", "Person"],
    "content": ["FAQPage", "HowTo", "Article", "BlogPosting"],
    "service": ["Service", "Product", "Offer"],
    "navigation": ["BreadcrumbList", "SiteNavigationElement", "WebSite", "WebPage"],
    "events": ["Event"],
    "reviews": ["Review", "AggregateRating"],
}

ALL_KNOWN_TYPES = []
for group in SCHEMA_TYPES.values():
    ALL_KNOWN_TYPES.extend(group)


def detect_schemas(crawl_data: dict) -> dict:
    """Analyze crawled data and return schema gap analysis.

    Args:
        crawl_data: Output from site_crawler.crawl_url()

    Returns dict with keys:
        existing_schemas: list of dicts with type and summary
        missing_schemas: list of schema types that should be present
        recommendations: list of actionable suggestions
        gap_score: 0-100 (higher = more gaps)
    """
    existing = _catalog_existing(crawl_data.get("json_ld_schemas", []))
    existing_types = {s["type"] for s in existing}

    missing = _identify_missing(existing_types, crawl_data)
    recommendations = _build_recommendations(existing_types, missing, crawl_data)

    total_relevant = len(existing_types) + len(missing)
    gap_score = round((len(missing) / max(total_relevant, 1)) * 100)

    return {
        "existing_schemas": existing,
        "existing_types": sorted(existing_types),
        "missing_schemas": missing,
        "recommendations": recommendations,
        "gap_score": gap_score,
    }


def generate_schema(schema_type: str, crawl_data: dict) -> dict:
    """Generate a JSON-LD schema block for a given type using crawl data.

    Returns a ready-to-use JSON-LD dict.
    """
    generators = {
        "Organization": _gen_organization,
        "LocalBusiness": _gen_local_business,
        "FAQPage": _gen_faq_page,
        "WebSite": _gen_website,
        "BreadcrumbList": _gen_breadcrumb,
        "HowTo": _gen_howto,
        "Service": _gen_service,
        "Article": _gen_article,
    }

    generator = generators.get(schema_type)
    if not generator:
        return {
            "@context": "https://schema.org",
            "@type": schema_type,
            "name": crawl_data.get("title", ""),
            "url": crawl_data.get("url", ""),
        }

    return generator(crawl_data)


# ---------------------------------------------------------------------------
# Cataloging existing schemas
# ---------------------------------------------------------------------------

def _catalog_existing(json_ld_blocks: list) -> list[dict]:
    """Walk all JSON-LD blocks and extract type + summary info."""
    found = []

    for block in json_ld_blocks:
        _walk_schema(block, found)

    return found


def _walk_schema(obj, found: list):
    """Recursively walk a JSON-LD object (handles @graph, lists)."""
    if isinstance(obj, list):
        for item in obj:
            _walk_schema(item, found)
        return

    if not isinstance(obj, dict):
        return

    schema_type = obj.get("@type", "")
    if isinstance(schema_type, list):
        for t in schema_type:
            found.append({
                "type": t,
                "name": obj.get("name", obj.get("headline", "")),
                "url": obj.get("url", ""),
            })
    elif schema_type:
        found.append({
            "type": schema_type,
            "name": obj.get("name", obj.get("headline", "")),
            "url": obj.get("url", ""),
        })

    # Recurse into @graph
    if "@graph" in obj:
        _walk_schema(obj["@graph"], found)


# ---------------------------------------------------------------------------
# Gap identification
# ---------------------------------------------------------------------------

def _identify_missing(existing_types: set, crawl_data: dict) -> list[dict]:
    """Figure out what's missing based on existing content signals."""
    missing = []

    # Every site should have Organization or LocalBusiness
    if not existing_types & {"Organization", "LocalBusiness", "Person"}:
        missing.append({
            "type": "Organization",
            "reason": "No identity schema found. Every site needs Organization or LocalBusiness.",
            "priority": "high",
        })

    # Every site should have WebSite
    if "WebSite" not in existing_types:
        missing.append({
            "type": "WebSite",
            "reason": "WebSite schema helps search engines understand site structure.",
            "priority": "medium",
        })

    # If FAQ content exists but no FAQPage schema
    faq_items = crawl_data.get("faq_items", [])
    non_jsonld_faqs = [f for f in faq_items if f.get("source") != "json-ld"]
    if non_jsonld_faqs and "FAQPage" not in existing_types:
        missing.append({
            "type": "FAQPage",
            "reason": f"Found {len(non_jsonld_faqs)} FAQ items in HTML without schema markup.",
            "priority": "high",
        })

    # If no FAQ content at all, suggest adding it
    if not faq_items:
        missing.append({
            "type": "FAQPage",
            "reason": "No FAQ content detected. FAQ schema is a top AEO signal.",
            "priority": "high",
        })

    # BreadcrumbList for navigation
    if "BreadcrumbList" not in existing_types:
        missing.append({
            "type": "BreadcrumbList",
            "reason": "Breadcrumb schema improves navigation visibility in search.",
            "priority": "low",
        })

    # Check headings for how-to signals
    all_headings = []
    for level in ("h1", "h2", "h3"):
        all_headings.extend(crawl_data.get("headings", {}).get(level, []))
    howto_signal = any(
        re.search(r"\bhow\s+to\b", h, re.I) for h in all_headings
    )
    if howto_signal and "HowTo" not in existing_types:
        missing.append({
            "type": "HowTo",
            "reason": "How-to content detected in headings but no HowTo schema present.",
            "priority": "medium",
        })

    # Service schema for service-oriented sites
    service_signal = any(
        re.search(r"\bservices?\b", h, re.I) for h in all_headings
    )
    if service_signal and "Service" not in existing_types:
        missing.append({
            "type": "Service",
            "reason": "Service-related headings found but no Service schema.",
            "priority": "medium",
        })

    return missing


def _build_recommendations(existing_types: set, missing: list, crawl_data: dict) -> list[str]:
    """Build ordered list of actionable recommendations."""
    recs = []

    # High priority first
    for gap in sorted(missing, key=lambda g: {"high": 0, "medium": 1, "low": 2}.get(g["priority"], 3)):
        recs.append(f"Add {gap['type']} schema: {gap['reason']}")

    # Check for llms.txt
    if crawl_data.get("llms_txt") is None:
        recs.append("Create an llms.txt file to help AI systems understand your site.")

    # Check robots.txt for AI crawler access
    robots = crawl_data.get("robots_txt")
    if robots:
        ai_bots = ["GPTBot", "anthropic-ai", "Google-Extended", "CCBot", "ClaudeBot"]
        blocked = [bot for bot in ai_bots if re.search(
            rf"User-agent:\s*{re.escape(bot)}.*?Disallow:\s*/",
            robots, re.I | re.S
        )]
        if blocked:
            recs.append(f"robots.txt blocks these AI crawlers: {', '.join(blocked)}. Consider allowing them.")

    return recs


# ---------------------------------------------------------------------------
# Schema generators
# ---------------------------------------------------------------------------

def _gen_organization(data: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": data.get("title", "").split("|")[0].split("-")[0].strip() or "Your Organization",
        "url": data.get("url", ""),
        "description": data.get("meta_description", ""),
    }


def _gen_local_business(data: dict) -> dict:
    schema = _gen_organization(data)
    schema["@type"] = "LocalBusiness"
    return schema


def _gen_faq_page(data: dict) -> dict:
    faq_items = data.get("faq_items", [])
    main_entity = []
    for item in faq_items:
        main_entity.append({
            "@type": "Question",
            "name": item["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": item["answer"],
            },
        })

    # If no FAQ items found, provide a template
    if not main_entity:
        main_entity.append({
            "@type": "Question",
            "name": "What does your company do?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": data.get("meta_description", "Replace with your answer."),
            },
        })

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main_entity,
    }


def _gen_website(data: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": data.get("title", "").split("|")[0].split("-")[0].strip() or "Website",
        "url": data.get("url", ""),
        "potentialAction": {
            "@type": "SearchAction",
            "target": data.get("url", "") + "?s={search_term_string}",
            "query-input": "required name=search_term_string",
        },
    }


def _gen_breadcrumb(data: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": data.get("url", ""),
            },
        ],
    }


def _gen_howto(data: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": "Replace with your how-to title",
        "description": data.get("meta_description", ""),
        "step": [
            {
                "@type": "HowToStep",
                "name": "Step 1",
                "text": "Describe step 1 here.",
            },
        ],
    }


def _gen_service(data: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": "Replace with service name",
        "description": data.get("meta_description", ""),
        "provider": {
            "@type": "Organization",
            "name": data.get("title", "").split("|")[0].split("-")[0].strip(),
            "url": data.get("url", ""),
        },
    }


def _gen_article(data: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": data.get("title", ""),
        "description": data.get("meta_description", ""),
        "url": data.get("url", ""),
        "datePublished": datetime.now().strftime("%Y-%m-%d"),
    }


if __name__ == "__main__":
    import sys
    from site_crawler import crawl_url

    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    crawl_data = crawl_url(url)
    analysis = detect_schemas(crawl_data)

    print("Existing schemas:")
    for s in analysis["existing_schemas"]:
        print(f"  - {s['type']}: {s.get('name', 'unnamed')}")

    print(f"\nMissing schemas ({len(analysis['missing_schemas'])}):")
    for m in analysis["missing_schemas"]:
        print(f"  [{m['priority'].upper()}] {m['type']}: {m['reason']}")

    print(f"\nGap score: {analysis['gap_score']}/100")

    if analysis["missing_schemas"]:
        first_missing = analysis["missing_schemas"][0]["type"]
        print(f"\nGenerated {first_missing} schema:")
        print(json.dumps(generate_schema(first_missing, crawl_data), indent=2))
