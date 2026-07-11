"""
AEO Composite Scorer.

Takes crawl data + schema analysis + citation results (+ optional brand
authority data) and produces a 0-100 composite AEO score with dimension
breakdown and letter grade.

Scoring weights match the framework in context/aeo-framework.md.

Rebalanced 2026-06-11 against June 2026 research:
- Schema demoted from 40% combined to 15% (Ahrefs May 2026 causal study:
  1,885 pages adding schema, AI citations barely moved; Google's May 2026
  AI guide: same index, same signals, no special AI markup).
- Off-site authority + AI mentions raised to 30% combined (Ahrefs 75K-brand
  study: brand mentions correlate 0.664 with AI citation rate, ~3x backlinks).
- Freshness added (65% of AI bot hits target content <12 months old).
- Crawler access raised and extended with edge/CDN block detection
  (Cloudflare default-blocks unverified AI crawlers since 2025).
- llms.txt cut to 5% (Google: explicitly unused; Semrush controlled study:
  no correlation; only Anthropic/Perplexity reportedly honor it).
- Dimensions that weren't measured (citations not run, brand authority not
  assessed) are now EXCLUDED and weights renormalized, instead of silently
  scoring 0 and dragging the composite down.
"""

import re
from datetime import datetime
from typing import Optional


# ---------------------------------------------------------------------------
# Weights (must sum to 1.0)
# ---------------------------------------------------------------------------

WEIGHTS = {
    "citability": 0.20,
    "ai_mentions": 0.15,
    "off_site_authority": 0.15,
    "schema_structured": 0.15,
    "faq_quality": 0.10,
    "crawler_access": 0.10,
    "freshness": 0.10,
    "llms_txt": 0.05,
}


# ---------------------------------------------------------------------------
# AI crawler tiers (June 2026 landscape)
#
# The bot fleet split into three tiers with independent robots.txt entries.
# Blocking a SEARCH-tier bot makes you invisible on that AI search surface.
# Blocking a TRAINING-tier bot is a legitimate business decision and is
# only lightly weighted.
# ---------------------------------------------------------------------------

AI_BOT_TIERS = {
    "search": {
        "OAI-SearchBot": "OpenAI (ChatGPT Search index)",
        "Claude-SearchBot": "Anthropic (Claude search index)",
        "PerplexityBot": "Perplexity (search index)",
        "Bingbot": "Microsoft (feeds ChatGPT Search + Copilot)",
    },
    "user": {
        "ChatGPT-User": "OpenAI (user-initiated fetch)",
        "Claude-User": "Anthropic (user-initiated fetch)",
        "Perplexity-User": "Perplexity (user-initiated fetch)",
    },
    "training": {
        "GPTBot": "OpenAI (training)",
        "ClaudeBot": "Anthropic (training)",
        "Google-Extended": "Google (Gemini training only)",
        "CCBot": "Common Crawl",
        "Applebot-Extended": "Apple (training)",
        "Meta-ExternalAgent": "Meta (training)",
        "Amazonbot": "Amazon",
    },
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


def _score_schema_structured(crawl_data: dict, schema_analysis: dict) -> int:
    """Merged schema dimension: coverage of key types + breadth/validity.

    Schema is a hygiene factor for entity disambiguation, not a citation
    driver (Ahrefs May 2026). One dimension at 15% replaces the old two
    at 40% combined.
    """
    coverage = _score_schema_coverage(crawl_data, schema_analysis)
    breadth = _score_structured_data(crawl_data, schema_analysis)
    return round(0.6 * coverage + 0.4 * breadth)


def _score_faq_quality(crawl_data: dict, schema_analysis: dict) -> int:
    """Score 0-100 based on FAQ/answer content quality.

    Internal rebalance 2026-06: content depth now outweighs markup.
    Google removed FAQ rich results (May 2026), but answer engines still
    extract Q&A-structured content, so the schema bonus shrank rather
    than disappeared.
    """
    faq_items = crawl_data.get("faq_items", [])
    existing_types = set(schema_analysis.get("existing_types", []))

    if not faq_items:
        return 0

    score = 0

    # Number of FAQs (up to 35 points)
    count = len(faq_items)
    if count >= 20:
        score += 35
    elif count >= 10:
        score += 25
    elif count >= 5:
        score += 18
    else:
        score += count * 3

    # Answer depth (up to 35 points)
    avg_answer_len = sum(len(f.get("answer", "")) for f in faq_items) / max(count, 1)
    if avg_answer_len >= 200:
        score += 35
    elif avg_answer_len >= 100:
        score += 22
    elif avg_answer_len >= 50:
        score += 12
    else:
        score += 5

    # Schema markup present (20 points)
    if "FAQPage" in existing_types:
        score += 20

    # JSON-LD sourced FAQs (10 points)
    jsonld_faqs = [f for f in faq_items if f.get("source") == "json-ld"]
    if jsonld_faqs:
        score += 10

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


def _score_citability_combined(crawl_data: dict) -> int:
    """Citability dimension: extraction signals + structural clarity.

    Structure is a proven extraction driver: 44.2% of LLM citations come
    from the first 30% of page content, and structured pages are ~2.8x
    more likely to be cited. Clarity folded in here (was its own 5%
    dimension) since the checks overlap.
    """
    return round(0.7 * _score_citability(crawl_data) + 0.3 * _score_content_clarity(crawl_data))


def _bot_block_status(robots: str, bots: dict) -> tuple[list[str], float]:
    """Return (blocked bot names, allowed ratio) for a tier of bots."""
    blocked = []
    for bot in bots:
        pattern = rf"User-agent:\s*{re.escape(bot)}.*?Disallow:\s*/\s*$"
        if re.search(pattern, robots, re.I | re.S | re.M):
            blocked.append(bot)
    allowed_ratio = 1 - (len(blocked) / len(bots)) if bots else 1.0
    return blocked, allowed_ratio


def _score_crawler_access(crawl_data: dict) -> int:
    """Score 0-100 for AI crawler access: robots.txt tiers + edge blocking.

    Search-tier access is a binary gate (block OAI-SearchBot and you're
    invisible in ChatGPT Search), so it carries most of the points.
    Training-tier blocking is a legitimate licensing/business decision and
    is only lightly weighted. An edge/CDN filter caps the whole dimension
    because it silently overrides whatever robots.txt says.
    """
    robots = crawl_data.get("robots_txt")
    score = 0

    if robots is None:
        # No robots.txt: nothing is blocked by default, but there's no
        # explicit config and no sitemap reference either.
        score = 70
    else:
        score += 10  # file exists

        blocked_search, ratio_search = _bot_block_status(robots, AI_BOT_TIERS["search"])
        score += round(45 * ratio_search)

        blocked_user, ratio_user = _bot_block_status(robots, AI_BOT_TIERS["user"])
        score += round(15 * ratio_user)

        blocked_training, ratio_training = _bot_block_status(robots, AI_BOT_TIERS["training"])
        score += round(10 * ratio_training)

        if crawl_data.get("sitemap_referenced"):
            score += 15

    # Edge/CDN-level AI filtering overrides robots.txt entirely
    access_check = crawl_data.get("ai_access_check") or {}
    if access_check.get("edge_filtering_detected"):
        score = min(score, 35)

    return min(score, 100)


def _score_freshness(crawl_data: dict) -> int:
    """Score 0-100 from machine-readable date signals.

    ~65% of AI bot hits target content under 12 months old. A site with
    no machine-readable dates can't prove freshness at all, which is
    itself a defect -- but a markup defect, so it floors at 30 rather
    than 0.
    """
    signals = crawl_data.get("freshness_signals") or {}
    most_recent = signals.get("most_recent")

    if not most_recent:
        return 30

    try:
        last_date = datetime.strptime(most_recent[:10], "%Y-%m-%d")
    except ValueError:
        return 30

    age_days = (datetime.now() - last_date).days

    if age_days <= 90:
        return 100
    if age_days <= 180:
        return 85
    if age_days <= 365:
        return 65
    if age_days <= 730:
        return 40
    return 20


def _score_llms_txt(crawl_data: dict) -> int:
    """Score 0-100 based on llms.txt presence and quality.

    June 2026 framing: a low-cost hedge, not a driver. Google explicitly
    doesn't use it; only Anthropic and Perplexity reportedly honor it.
    Weighted at 5% accordingly.
    """
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


def _score_ai_mentions(citation_data: Optional[dict]) -> Optional[int]:
    """Score 0-100 from citation checker results. None = not measured."""
    if not citation_data:
        return None
    return citation_data.get("overall_score", 0)


def _score_off_site_authority(brand_authority_data) -> Optional[int]:
    """Score 0-100 from brand authority assessment. None = not measured.

    Accepts either the result dict from brand_authority_scorer
    .score_brand_authority() or a plain int score.
    """
    if brand_authority_data is None:
        return None
    if isinstance(brand_authority_data, dict):
        return int(brand_authority_data.get("composite_score", 0))
    return int(brand_authority_data)


# ---------------------------------------------------------------------------
# Composite scorer
# ---------------------------------------------------------------------------

def score_site(
    crawl_data: dict,
    schema_analysis: dict,
    citation_data: Optional[dict] = None,
    brand_authority_data=None,
) -> dict:
    """Produce the full AEO composite score.

    Args:
        crawl_data: Output from site_crawler.crawl_url()
        schema_analysis: Output from schema_detector.detect_schemas()
        citation_data: Optional output from citation_checker.check_citations()
        brand_authority_data: Optional output from
            brand_authority_scorer.score_brand_authority() (or an int score)

    Returns:
        Dict with composite_score, grade, dimensions, and recommendations.
        Dimensions that weren't measured (no citation run, no brand
        authority assessment) carry score=None / measured=False and are
        excluded from the composite; remaining weights are renormalized.
    """
    ai_mentions_score = _score_ai_mentions(citation_data)
    off_site_score = _score_off_site_authority(brand_authority_data)

    dimensions = {
        "citability": {
            "score": _score_citability_combined(crawl_data),
            "weight": WEIGHTS["citability"],
            "label": "Citability & Structure",
            "measured": True,
        },
        "ai_mentions": {
            "score": ai_mentions_score,
            "weight": WEIGHTS["ai_mentions"],
            "label": "AI Mentions",
            "measured": ai_mentions_score is not None,
        },
        "off_site_authority": {
            "score": off_site_score,
            "weight": WEIGHTS["off_site_authority"],
            "label": "Off-Site Authority",
            "measured": off_site_score is not None,
        },
        "schema_structured": {
            "score": _score_schema_structured(crawl_data, schema_analysis),
            "weight": WEIGHTS["schema_structured"],
            "label": "Schema & Structured Data",
            "measured": True,
        },
        "faq_quality": {
            "score": _score_faq_quality(crawl_data, schema_analysis),
            "weight": WEIGHTS["faq_quality"],
            "label": "Answer Content (FAQ)",
            "measured": True,
        },
        "crawler_access": {
            "score": _score_crawler_access(crawl_data),
            "weight": WEIGHTS["crawler_access"],
            "label": "AI Crawler Access",
            "measured": True,
        },
        "freshness": {
            "score": _score_freshness(crawl_data),
            "weight": WEIGHTS["freshness"],
            "label": "Freshness Signals",
            "measured": True,
        },
        "llms_txt": {
            "score": _score_llms_txt(crawl_data),
            "weight": WEIGHTS["llms_txt"],
            "label": "llms.txt (Hedge)",
            "measured": True,
        },
    }

    # Weighted composite over MEASURED dimensions only, renormalized
    measured = {k: d for k, d in dimensions.items() if d["measured"]}
    total_weight = sum(d["weight"] for d in measured.values())
    if total_weight > 0:
        composite = sum(d["score"] * d["weight"] for d in measured.values()) / total_weight
    else:
        composite = 0

    composite_score = round(composite)
    grade = _letter_grade(composite_score)
    unmeasured = [k for k, d in dimensions.items() if not d["measured"]]

    # Build recommendations from lowest-scoring dimensions
    recs = _build_recommendations(dimensions, crawl_data, schema_analysis)

    return {
        "composite_score": composite_score,
        "grade": grade,
        "dimensions": dimensions,
        "unmeasured_dimensions": unmeasured,
        "recommendations": recs,
        "report": _format_report(crawl_data, composite_score, grade, dimensions, recs),
    }


def _build_recommendations(dimensions: dict, crawl_data: dict, schema_analysis: dict) -> list[str]:
    """Generate prioritized recommendations from dimension scores."""
    recs = []

    # Unmeasured dimensions first: they're the highest-weight blind spots
    if not dimensions["off_site_authority"]["measured"]:
        recs.append(
            "Off-site authority not yet assessed (15% of score). Run the brand authority "
            "assessment -- off-site brand mentions are the strongest measured correlate of "
            "AI citations (0.664, ~3x stronger than backlinks)."
        )
    if not dimensions["ai_mentions"]["measured"]:
        recs.append(
            "AI mention check not run (15% of score). Run with --citations to see whether "
            "ChatGPT, Gemini, Claude, and Perplexity currently surface the brand."
        )

    # Sort measured dimensions by score (lowest first)
    sorted_dims = sorted(
        (item for item in dimensions.items() if item[1]["measured"]),
        key=lambda x: x[1]["score"],
    )

    for key, dim in sorted_dims:
        score = dim["score"]

        if score >= 75:
            continue  # good enough, skip

        if key == "schema_structured" and score < 50:
            missing = schema_analysis.get("missing_schemas", [])
            high_priority = [m for m in missing if m.get("priority") == "high"]
            if high_priority:
                types = ", ".join(m["type"] for m in high_priority[:3])
                recs.append(
                    f"Add missing high-priority schemas: {types}. Schema is table stakes for "
                    "entity disambiguation, not a citation driver -- implement it once, cleanly."
                )
            else:
                recs.append(
                    "Add Organization and Service schema with sameAs links to your profiles. "
                    "This is entity hygiene: it tells AI systems exactly who you are."
                )

        elif key == "faq_quality" and score < 50:
            faq_count = len(crawl_data.get("faq_items", []))
            if faq_count == 0:
                recs.append(
                    "Create a Q&A page answering real customer questions. Google dropped FAQ "
                    "rich results (May 2026), but answer engines still extract Q&A-structured "
                    "content -- write for extraction, not for rich snippets."
                )
            else:
                recs.append(
                    f"Found {faq_count} FAQ items -- deepen the answers (aim for 100-200 words "
                    "each, answer-first) and add FAQPage JSON-LD for entity clarity."
                )

        elif key == "citability" and score < 50:
            recs.append(
                "Restructure content for extraction: question-format headings, direct answers "
                "in the first sentence, key facts in the first 30% of the page (where 44% of "
                "AI citations come from)."
            )

        elif key == "crawler_access" and score < 50:
            access_check = crawl_data.get("ai_access_check") or {}
            if access_check.get("edge_filtering_detected"):
                blocked = ", ".join(access_check.get("blocked_agents", []))
                recs.append(
                    f"CRITICAL: edge/CDN-level AI filtering detected ({blocked} blocked while "
                    "normal traffic passes). Check Cloudflare AI Crawl Control or equivalent -- "
                    "robots.txt allows mean nothing if the CDN blocks the bots."
                )
            else:
                recs.append(
                    "Update robots.txt to allow AI search crawlers (OAI-SearchBot, "
                    "Claude-SearchBot, PerplexityBot) and user agents (ChatGPT-User, "
                    "Perplexity-User). Training bots (GPTBot, ClaudeBot) are a separate "
                    "business decision."
                )

        elif key == "freshness" and score < 50:
            signals = crawl_data.get("freshness_signals") or {}
            if not signals.get("most_recent"):
                recs.append(
                    "No machine-readable dates found. Add dateModified/datePublished to schema "
                    "markup -- AI engines strongly prefer content they can verify as fresh "
                    "(65% of AI bot hits target content under 12 months old)."
                )
            else:
                recs.append(
                    f"Content freshness signals are stale (latest: {signals['most_recent']}). "
                    "Substantively update key pages and refresh dateModified -- date-stamp "
                    "gaming without real updates doesn't work."
                )

        elif key == "llms_txt" and score < 50:
            recs.append(
                "Add an llms.txt file (10-minute task). Set expectations correctly: it's a "
                "hedge that Claude and Perplexity reportedly honor -- Google explicitly "
                "ignores it."
            )

        elif key == "ai_mentions" and score < 50:
            recs.append(
                "Brand has low AI visibility. Prioritize off-site mentions: Reddit threads, "
                "review platforms, industry roundups, digital PR. Wikipedia + Reddit alone "
                "drive 25%+ of ChatGPT citations."
            )

        elif key == "off_site_authority" and score < 50:
            recs.append(
                "Off-site authority is weak. Focus Layer 2 work: YouTube answer content, "
                "authentic Reddit presence, review platforms, podcast appearances, and "
                "unlinked brand mentions via digital PR."
            )

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
        if dim["measured"]:
            weighted = round(dim["score"] * dim["weight"], 1)
            lines.append(
                f"| {dim['label']} | {int(dim['weight'] * 100)}% | {dim['score']}/100 | {weighted} |"
            )
        else:
            lines.append(
                f"| {dim['label']} | {int(dim['weight'] * 100)}% | not measured | n/a |"
            )

    lines.append(f"| **TOTAL** | **100%** | | **{composite_score}** |")

    unmeasured = [d["label"] for d in dimensions.values() if not d["measured"]]
    if unmeasured:
        lines.append("")
        lines.append(
            f"*Composite renormalized over measured dimensions only "
            f"(not measured: {', '.join(unmeasured)}).*"
        )
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
