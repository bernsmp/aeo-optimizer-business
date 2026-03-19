"""
AEO Composite Scorer.

Takes crawl data + schema analysis + citation results and produces
a 0-100 composite AEO score with dimension breakdown and letter grade.

Scoring weights match the framework in context/aeo-framework.md.
"""

import re
from typing import Optional


# ---------------------------------------------------------------------------
# Weights (must sum to 1.0)
# ---------------------------------------------------------------------------

WEIGHTS = {
    "schema_coverage": 0.25,
    "faq_quality": 0.20,
    "citability": 0.15,
    "structured_data": 0.15,
    "llms_txt": 0.10,
    "robots_txt": 0.05,
    "content_clarity": 0.05,
    "ai_mentions": 0.05,
}


# ---------------------------------------------------------------------------
# Grade thresholds
# ---------------------------------------------------------------------------

def _letter_grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    if score >= 40:
        return "D"
    return "F"


# ---------------------------------------------------------------------------
# Dimension scorers
# ---------------------------------------------------------------------------

def _score_schema_coverage(crawl_data: dict, schema_analysis: dict) -> int:
    """Score 0-100 based on presence of key schema types."""
    existing = set(schema_analysis.get("existing_types", []))

    # Points per schema type (total available = 100)
    type_points = {
        "Organization": 15,
        "LocalBusiness": 15,  # alt for Organization
        "FinancialService": 15,  # alt for Organization
        "ProfessionalService": 15,  # alt for Organization
        "FAQPage": 25,
        "Service": 15,
        "WebSite": 5,
        "BreadcrumbList": 5,
        "Person": 10,
        "Event": 5,
        "HowTo": 5,
        "Article": 5,
        "BlogPosting": 5,
        "Review": 5,
        "AggregateRating": 5,
    }

    score = 0
    # Identity group: only count the best one
    identity_types = {"Organization", "LocalBusiness", "FinancialService", "ProfessionalService"}
    if existing & identity_types:
        score += 15
        # Bonus for specific type (not generic Organization)
        if existing & {"LocalBusiness", "FinancialService", "ProfessionalService"}:
            score += 5

    # Other types
    for schema_type, points in type_points.items():
        if schema_type in identity_types:
            continue
        if schema_type in existing:
            score += points

    return min(score, 100)


def _score_faq_quality(crawl_data: dict, schema_analysis: dict) -> int:
    """Score 0-100 based on FAQ content and schema markup."""
    faq_items = crawl_data.get("faq_items", [])
    existing_types = set(schema_analysis.get("existing_types", []))

    if not faq_items:
        return 0

    score = 0

    # Number of FAQs (up to 30 points)
    count = len(faq_items)
    if count >= 20:
        score += 30
    elif count >= 10:
        score += 20
    elif count >= 5:
        score += 15
    else:
        score += count * 3

    # Answer depth (up to 25 points)
    avg_answer_len = sum(len(f.get("answer", "")) for f in faq_items) / max(count, 1)
    if avg_answer_len >= 200:
        score += 25
    elif avg_answer_len >= 100:
        score += 15
    elif avg_answer_len >= 50:
        score += 10
    else:
        score += 5

    # Schema markup present (25 points)
    if "FAQPage" in existing_types:
        score += 25

    # JSON-LD sourced FAQs (20 points)
    jsonld_faqs = [f for f in faq_items if f.get("source") == "json-ld"]
    if jsonld_faqs:
        score += 20

    return min(score, 100)


def _score_citability(crawl_data: dict) -> int:
    """Score 0-100 based on how extractable the content is for AI models."""
    score = 0
    headings = crawl_data.get("headings", {})

    # Has clear H1 (10 points)
    h1s = headings.get("h1", [])
    if len(h1s) == 1:
        score += 10
    elif h1s:
        score += 5  # multiple H1s is worse

    # Has H2 structure (15 points)
    h2s = headings.get("h2", [])
    if len(h2s) >= 3:
        score += 15
    elif h2s:
        score += 8

    # Question-format headings (20 points) - great for AI extraction
    all_headings = h1s + h2s + headings.get("h3", [])
    question_headings = [h for h in all_headings if h.strip().endswith("?")]
    if len(question_headings) >= 5:
        score += 20
    elif len(question_headings) >= 2:
        score += 12
    elif question_headings:
        score += 5

    # Meta description present and decent length (15 points)
    meta = crawl_data.get("meta_description", "")
    if len(meta) >= 120:
        score += 15
    elif len(meta) >= 50:
        score += 10
    elif meta:
        score += 5

    # Title exists and is reasonable (10 points)
    title = crawl_data.get("title", "")
    if 10 < len(title) < 80:
        score += 10
    elif title:
        score += 5

    # Direct answer patterns in content (30 points)
    # Check if headings contain "what is", "how to", definitive patterns
    definitive_patterns = [
        r"^what\s+is\b",
        r"^how\s+to\b",
        r"^why\b",
        r"^who\s+(is|are)\b",
        r"^best\b",
        r"^top\b",
        r"^guide\s+to\b",
    ]
    definitive_count = sum(
        1 for h in all_headings
        if any(re.search(p, h, re.I) for p in definitive_patterns)
    )
    if definitive_count >= 5:
        score += 30
    elif definitive_count >= 3:
        score += 20
    elif definitive_count >= 1:
        score += 10

    return min(score, 100)


def _score_structured_data(crawl_data: dict, schema_analysis: dict) -> int:
    """Score 0-100 based on breadth and validity of structured data."""
    existing = schema_analysis.get("existing_schemas", [])
    existing_types = set(schema_analysis.get("existing_types", []))

    if not existing:
        return 0

    score = 0

    # Number of distinct schema types (up to 40 points)
    type_count = len(existing_types)
    if type_count >= 6:
        score += 40
    elif type_count >= 4:
        score += 30
    elif type_count >= 2:
        score += 20
    else:
        score += 10

    # Has BreadcrumbList (15 points)
    if "BreadcrumbList" in existing_types:
        score += 15

    # Has WebSite with SearchAction (15 points)
    if "WebSite" in existing_types:
        score += 15

    # Schemas have URLs (completeness indicator, 15 points)
    schemas_with_urls = sum(1 for s in existing if s.get("url"))
    if schemas_with_urls >= 3:
        score += 15
    elif schemas_with_urls >= 1:
        score += 8

    # Gap score inverse (15 points) - lower gaps = better
    gap_score = schema_analysis.get("gap_score", 100)
    score += max(0, round(15 * (1 - gap_score / 100)))

    return min(score, 100)


def _score_llms_txt(crawl_data: dict) -> int:
    """Score 0-100 based on llms.txt presence and quality."""
    llms_txt = crawl_data.get("llms_txt")

    if not llms_txt:
        return 0

    score = 30  # exists at all

    content = llms_txt.strip()
    lines = content.split("\n")

    # Length / thoroughness (up to 30 points)
    if len(content) >= 1000:
        score += 30
    elif len(content) >= 500:
        score += 20
    elif len(content) >= 100:
        score += 10

    # Has sections/structure (up to 20 points)
    heading_lines = [l for l in lines if l.startswith("#") or l.startswith(">")]
    if len(heading_lines) >= 3:
        score += 20
    elif heading_lines:
        score += 10

    # Contains URLs (linking to key pages, 20 points)
    url_count = len(re.findall(r"https?://", content))
    if url_count >= 5:
        score += 20
    elif url_count >= 1:
        score += 10

    return min(score, 100)


def _score_robots_txt(crawl_data: dict) -> int:
    """Score 0-100 based on robots.txt AI crawler configuration."""
    robots = crawl_data.get("robots_txt")

    if robots is None:
        return 20  # no robots.txt means nothing is blocked (kinda okay)

    score = 30  # file exists

    # Check AI bot access
    ai_bots = {
        "GPTBot": "OpenAI",
        "ClaudeBot": "Anthropic",
        "anthropic-ai": "Anthropic",
        "Google-Extended": "Google AI",
        "CCBot": "Common Crawl",
        "PerplexityBot": "Perplexity",
    }

    blocked_bots = []
    allowed_bots = []

    for bot, label in ai_bots.items():
        # Check if explicitly blocked
        pattern = rf"User-agent:\s*{re.escape(bot)}.*?Disallow:\s*/"
        if re.search(pattern, robots, re.I | re.S):
            blocked_bots.append(label)
        else:
            allowed_bots.append(label)

    # Points for allowing AI bots (up to 50 points)
    if not blocked_bots:
        score += 50
    else:
        allowed_ratio = len(allowed_bots) / len(ai_bots)
        score += round(50 * allowed_ratio)

    # Sitemap reference (20 points)
    if crawl_data.get("sitemap_referenced"):
        score += 20

    return min(score, 100)


def _score_content_clarity(crawl_data: dict) -> int:
    """Score 0-100 based on heading hierarchy and content structure."""
    headings = crawl_data.get("headings", {})
    score = 0

    h1s = headings.get("h1", [])
    h2s = headings.get("h2", [])
    h3s = headings.get("h3", [])

    # Single H1 (25 points)
    if len(h1s) == 1:
        score += 25
    elif h1s:
        score += 10

    # H2 hierarchy (25 points)
    if len(h2s) >= 3:
        score += 25
    elif h2s:
        score += 15

    # H3 sub-hierarchy (15 points)
    if h3s:
        score += 15

    # Proper nesting: H2s should exist if H3s do (10 points)
    if h3s and h2s:
        score += 10
    elif h3s and not h2s:
        score += 0  # bad nesting

    # Title present and descriptive (15 points)
    title = crawl_data.get("title", "")
    if len(title) >= 20:
        score += 15
    elif title:
        score += 8

    # Meta description (10 points)
    if crawl_data.get("meta_description"):
        score += 10

    return min(score, 100)


def _score_ai_mentions(citation_data: Optional[dict]) -> int:
    """Score 0-100 based on citation checker results."""
    if not citation_data:
        return 0

    return citation_data.get("overall_score", 0)


# ---------------------------------------------------------------------------
# Composite scorer
# ---------------------------------------------------------------------------

def score_site(
    crawl_data: dict,
    schema_analysis: dict,
    citation_data: Optional[dict] = None,
) -> dict:
    """Produce the full AEO composite score.

    Args:
        crawl_data: Output from site_crawler.crawl_url()
        schema_analysis: Output from schema_detector.detect_schemas()
        citation_data: Optional output from citation_checker.check_citations()

    Returns:
        Dict with composite_score, grade, dimensions, and recommendations.
    """
    dimensions = {
        "schema_coverage": {
            "score": _score_schema_coverage(crawl_data, schema_analysis),
            "weight": WEIGHTS["schema_coverage"],
            "label": "Schema Coverage",
        },
        "faq_quality": {
            "score": _score_faq_quality(crawl_data, schema_analysis),
            "weight": WEIGHTS["faq_quality"],
            "label": "FAQ Quality",
        },
        "citability": {
            "score": _score_citability(crawl_data),
            "weight": WEIGHTS["citability"],
            "label": "Citability",
        },
        "structured_data": {
            "score": _score_structured_data(crawl_data, schema_analysis),
            "weight": WEIGHTS["structured_data"],
            "label": "Structured Data",
        },
        "llms_txt": {
            "score": _score_llms_txt(crawl_data),
            "weight": WEIGHTS["llms_txt"],
            "label": "llms.txt Present",
        },
        "robots_txt": {
            "score": _score_robots_txt(crawl_data),
            "weight": WEIGHTS["robots_txt"],
            "label": "robots.txt Config",
        },
        "content_clarity": {
            "score": _score_content_clarity(crawl_data),
            "weight": WEIGHTS["content_clarity"],
            "label": "Content Clarity",
        },
        "ai_mentions": {
            "score": _score_ai_mentions(citation_data),
            "weight": WEIGHTS["ai_mentions"],
            "label": "AI Mentions",
        },
    }

    # Compute weighted composite
    composite = sum(
        d["score"] * d["weight"] for d in dimensions.values()
    )
    composite_score = round(composite)
    grade = _letter_grade(composite_score)

    # Build recommendations from lowest-scoring dimensions
    recs = _build_recommendations(dimensions, crawl_data, schema_analysis)

    return {
        "composite_score": composite_score,
        "grade": grade,
        "dimensions": dimensions,
        "recommendations": recs,
        "report": _format_report(crawl_data, composite_score, grade, dimensions, recs),
    }


def _build_recommendations(dimensions: dict, crawl_data: dict, schema_analysis: dict) -> list[str]:
    """Generate prioritized recommendations from dimension scores."""
    recs = []

    # Sort dimensions by score (lowest first)
    sorted_dims = sorted(dimensions.items(), key=lambda x: x[1]["score"])

    for key, dim in sorted_dims:
        score = dim["score"]
        label = dim["label"]

        if score >= 75:
            continue  # good enough, skip

        if key == "schema_coverage" and score < 50:
            missing = schema_analysis.get("missing_schemas", [])
            high_priority = [m for m in missing if m.get("priority") == "high"]
            if high_priority:
                types = ", ".join(m["type"] for m in high_priority[:3])
                recs.append(f"Add missing high-priority schemas: {types}")
            else:
                recs.append("Improve schema coverage with Organization, FAQ, and Service schemas")

        elif key == "faq_quality" and score < 50:
            faq_count = len(crawl_data.get("faq_items", []))
            if faq_count == 0:
                recs.append("Create FAQ content. This is the #1 signal AI models use to extract answers")
            else:
                recs.append(f"Found {faq_count} FAQ items but they lack schema markup. Add FAQPage JSON-LD")

        elif key == "citability" and score < 50:
            recs.append("Restructure content with question-format headings and direct answer paragraphs")

        elif key == "structured_data" and score < 50:
            recs.append("Expand structured data beyond basics. Add Service, Person, Event schemas where relevant")

        elif key == "llms_txt" and score < 50:
            if score == 0:
                recs.append("Create an llms.txt file at the domain root describing your business for AI systems")
            else:
                recs.append("Expand llms.txt with more detail, sections, and links to key pages")

        elif key == "robots_txt" and score < 50:
            recs.append("Update robots.txt to allow AI crawlers (GPTBot, ClaudeBot, PerplexityBot)")

        elif key == "content_clarity" and score < 50:
            recs.append("Fix heading hierarchy: use a single H1, clear H2 sections, and H3 subsections")

        elif key == "ai_mentions" and score < 50:
            recs.append("Brand has low AI visibility. Focus on third-party mentions, reviews, and directory listings")

    return recs[:8]  # cap at 8 recommendations


def _format_report(
    crawl_data: dict,
    composite_score: int,
    grade: str,
    dimensions: dict,
    recs: list[str],
) -> str:
    """Format a human-readable score report."""
    url = crawl_data.get("url", "unknown")
    domain = crawl_data.get("domain", "unknown")

    lines = [
        f"# AEO Score Report: {domain}",
        f"**URL:** {url}",
        f"**Composite Score:** {composite_score}/100 (Grade: {grade})",
        "",
        "## Dimension Breakdown",
        "",
        "| Dimension | Weight | Score | Weighted |",
        "|-----------|--------|-------|----------|",
    ]

    for key, dim in dimensions.items():
        weighted = round(dim["score"] * dim["weight"], 1)
        lines.append(
            f"| {dim['label']} | {int(dim['weight'] * 100)}% | {dim['score']}/100 | {weighted} |"
        )

    lines.append(f"| **TOTAL** | **100%** | | **{composite_score}** |")
    lines.append("")

    if recs:
        lines.append("## Priority Recommendations")
        lines.append("")
        for i, rec in enumerate(recs, 1):
            lines.append(f"{i}. {rec}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import json
    import sys

    from site_crawler import crawl_url
    from schema_detector import detect_schemas

    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"

    print(f"Crawling {url}...")
    crawl_data = crawl_url(url)

    print("Analyzing schemas...")
    schema_analysis = detect_schemas(crawl_data)

    print("Scoring...")
    result = score_site(crawl_data, schema_analysis)

    print()
    print(result["report"])

    if "--json" in sys.argv:
        # Strip report text from JSON output (it's redundant)
        output = {k: v for k, v in result.items() if k != "report"}
        print()
        print(json.dumps(output, indent=2))
