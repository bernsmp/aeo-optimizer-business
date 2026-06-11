"""
AEO Full Audit Pipeline.

Chains: site_crawler -> schema_detector -> multi_page_crawler -> aeo_scorer
        (optionally) -> citation_checker

Produces a complete audit report and saves all artifacts to the client folder.

Usage:
    python3 aeo_audit.py <url> [--brand "Brand Name"] [--industry "industry"]
                                [--citations] [--pages 30] [--client client-slug]
                                [--json]

Examples:
    # Quick audit (no citation check, saves to stdout)
    python3 aeo_audit.py https://example.com

    # Full audit with citations, saved to client folder
    python3 aeo_audit.py https://vantagepoint-financial.com \\
        --brand "Vantage Point Financial" \\
        --industry "financial advisory" \\
        --citations \\
        --client vantagepointfinancial

    # Batch mode: just the score, no report
    python3 aeo_audit.py https://example.com --json --quiet
"""

import argparse
import json
import os
import sys
from datetime import datetime
from urllib.parse import urlparse

from site_crawler import crawl_url
from schema_detector import detect_schemas, generate_schema
from multi_page_crawler import analyze_site
from aeo_scorer import score_site
from citability_scorer import analyze_page_citability, format_citability_report


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def _grade_emoji(grade: str) -> str:
    return {"A": "A", "B": "B", "C": "C", "D": "D", "F": "F"}.get(grade, "?")


def _summarize_state(crawl_data: dict, schema_analysis: dict, site_analysis: dict) -> str:
    """Generate a narrative summary of the site's current AEO state."""
    domain = crawl_data.get("domain", "the site")
    existing_types = set(schema_analysis.get("existing_types", []))
    missing = schema_analysis.get("missing_schemas", [])
    faq_count = len(crawl_data.get("faq_items", []))
    has_llms = crawl_data.get("llms_txt") is not None
    pages_crawled = site_analysis.get("pages_crawled", 0)
    schema_coverage_pct = site_analysis.get("schema_coverage_pct", 0)

    parts = []

    # Identity schemas
    identity = existing_types & {"Organization", "LocalBusiness", "FinancialService", "ProfessionalService"}
    if identity:
        parts.append(f"Has {', '.join(sorted(identity))} schema")
    else:
        parts.append("No identity schema (Organization/LocalBusiness) found")

    # Schema breadth
    if len(existing_types) >= 5:
        parts.append(f"{len(existing_types)} schema types detected across the site")
    elif existing_types:
        parts.append(f"Only {len(existing_types)} schema types found: {', '.join(sorted(existing_types))}")
    else:
        parts.append("No structured data detected")

    # Site-wide coverage
    if pages_crawled > 1:
        parts.append(f"{schema_coverage_pct}% of {pages_crawled} crawled pages have schema markup")

    # FAQ
    if faq_count > 0:
        has_faq_schema = "FAQPage" in existing_types
        if has_faq_schema:
            parts.append(f"{faq_count} FAQ items with proper FAQPage schema")
        else:
            parts.append(f"{faq_count} FAQ items detected but missing FAQPage schema markup")
    else:
        parts.append("No FAQ content detected on the homepage")

    # llms.txt
    if has_llms:
        parts.append("llms.txt file is present")
    else:
        parts.append("No llms.txt file")

    # AI crawler access (search-tier bots gate AI search visibility)
    robots = crawl_data.get("robots_txt")
    if robots:
        import re
        blocked = []
        for bot in ["GPTBot", "OAI-SearchBot", "ClaudeBot", "Claude-SearchBot", "PerplexityBot"]:
            pattern = rf"User-agent:\s*{re.escape(bot)}.*?Disallow:\s*/"
            if re.search(pattern, robots, re.I | re.S):
                blocked.append(bot)
        if blocked:
            parts.append(f"AI crawlers blocked: {', '.join(blocked)}")
        else:
            parts.append("AI crawlers are not blocked in robots.txt")

    # Edge/CDN-level filtering (overrides robots.txt)
    access_check = crawl_data.get("ai_access_check") or {}
    if access_check.get("edge_filtering_detected"):
        blocked_agents = ", ".join(access_check.get("blocked_agents", []))
        parts.append(
            f"WARNING: edge/CDN-level AI filtering detected ({blocked_agents} get blocked "
            "while normal traffic passes) -- verify in the CDN dashboard"
        )

    return ". ".join(parts) + "."


def _build_gap_analysis(schema_analysis: dict, site_analysis: dict, score_result: dict) -> str:
    """Build the gap analysis section of the report."""
    lines = []

    # Schema gaps
    missing = schema_analysis.get("missing_schemas", [])
    if missing:
        lines.append("### Schema Gaps")
        lines.append("")
        for m in sorted(missing, key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.get("priority", "low"), 3)):
            priority = m.get("priority", "unknown").upper()
            lines.append(f"- **[{priority}] {m['type']}**: {m['reason']}")
        lines.append("")

    # Site-wide gaps
    site_missing = site_analysis.get("important_types_missing", [])
    if site_missing:
        lines.append("### Site-Wide Missing Schema Types")
        lines.append("")
        lines.append(f"Across {site_analysis.get('pages_crawled', 0)} pages crawled, these important schema types were not found anywhere:")
        lines.append("")
        for t in site_missing:
            lines.append(f"- {t}")
        lines.append("")

    # Dimension gaps
    dims = score_result.get("dimensions", {})
    weak_dims = [(k, d) for k, d in dims.items() if d.get("measured", True) and d["score"] < 50]
    if weak_dims:
        lines.append("### Weakest Dimensions")
        lines.append("")
        for key, dim in sorted(weak_dims, key=lambda x: x[1]["score"]):
            lines.append(f"- **{dim['label']}**: {dim['score']}/100")
        lines.append("")

    return "\n".join(lines)


def _build_full_report(
    crawl_data: dict,
    schema_analysis: dict,
    site_analysis: dict,
    score_result: dict,
    citation_data: dict | None,
    brand: str,
    industry: str,
    citability_result: dict | None = None,
) -> str:
    """Build the complete audit report markdown."""
    domain = crawl_data.get("domain", "unknown")
    url = crawl_data.get("url", "unknown")
    date = datetime.now().strftime("%Y-%m-%d")
    composite = score_result["composite_score"]
    grade = score_result["grade"]
    dims = score_result["dimensions"]
    recs = score_result["recommendations"]

    lines = [
        f"# AEO Audit Report: {brand or domain}",
        "",
        f"**URL:** {url}",
        f"**Date:** {date}",
        f"**Prepared by:** MAIX AEO",
    ]

    if industry:
        lines.append(f"**Industry:** {industry}")

    lines.extend([
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        f"**Overall AEO Score: {composite}/100 (Grade: {grade})**",
        "",
    ])

    # Summary paragraph
    state_summary = _summarize_state(crawl_data, schema_analysis, site_analysis)
    lines.append(state_summary)
    lines.extend(["", "---", ""])

    # Score breakdown
    lines.extend([
        "## Score Breakdown",
        "",
        "| Dimension | Weight | Score | Weighted |",
        "|-----------|--------|-------|----------|",
    ])

    for key, dim in dims.items():
        if dim.get("measured", True):
            weighted = round(dim["score"] * dim["weight"], 1)
            lines.append(f"| {dim['label']} | {int(dim['weight'] * 100)}% | {dim['score']}/100 | {weighted} |")
        else:
            lines.append(f"| {dim['label']} | {int(dim['weight'] * 100)}% | not measured | n/a |")

    lines.append(f"| **TOTAL** | **100%** | | **{composite}** |")

    unmeasured_labels = [d["label"] for d in dims.values() if not d.get("measured", True)]
    if unmeasured_labels:
        lines.append("")
        lines.append(
            f"*Composite renormalized over measured dimensions "
            f"(not measured: {', '.join(unmeasured_labels)}).*"
        )
    lines.extend(["", "---", ""])

    # Current state details
    lines.extend([
        "## Current State Analysis",
        "",
    ])

    # Existing schemas
    existing = schema_analysis.get("existing_schemas", [])
    if existing:
        lines.append("### Existing Schema Markup")
        lines.append("")
        for s in existing:
            name = s.get("name", "unnamed")
            lines.append(f"- **{s['type']}**: {name}")
        lines.append("")

    # Site-wide analysis
    if site_analysis.get("pages_crawled", 0) > 1:
        lines.append("### Site-Wide Coverage")
        lines.append("")
        lines.append(f"- Pages crawled: {site_analysis['pages_crawled']}")
        lines.append(f"- Pages with schema: {site_analysis['pages_with_schema']} ({site_analysis['schema_coverage_pct']}%)")
        lines.append(f"- OpenGraph coverage: {site_analysis['opengraph_coverage_pct']}%")
        lines.append(f"- JSON-LD types found: {', '.join(site_analysis.get('json_ld_types_found', [])) or 'None'}")
        lines.append("")

    # FAQ analysis
    faq_items = crawl_data.get("faq_items", [])
    if faq_items:
        lines.append("### FAQ Content Detected")
        lines.append("")
        lines.append(f"Found {len(faq_items)} FAQ items:")
        lines.append("")
        for faq in faq_items[:10]:  # show first 10
            q = faq["question"][:80]
            source = faq.get("source", "unknown")
            lines.append(f"- \"{q}\" (source: {source})")
        if len(faq_items) > 10:
            lines.append(f"- ... and {len(faq_items) - 10} more")
        lines.append("")

    # llms.txt status
    if crawl_data.get("llms_txt"):
        lines.append("### llms.txt")
        lines.append("")
        preview = crawl_data["llms_txt"][:300].strip()
        lines.append(f"```\n{preview}\n```")
        lines.append("")
    else:
        lines.append("### llms.txt: Not Found")
        lines.append("")

    lines.extend(["---", ""])

    # Gap analysis
    lines.extend([
        "## Gap Analysis",
        "",
    ])
    gap_text = _build_gap_analysis(schema_analysis, site_analysis, score_result)
    lines.append(gap_text)
    lines.extend(["---", ""])

    # Recommendations
    lines.extend([
        "## Priority Recommendations",
        "",
    ])
    for i, rec in enumerate(recs, 1):
        lines.append(f"{i}. {rec}")
    lines.extend(["", "---", ""])

    # Passage-level citability (if available)
    if citability_result and "error" not in citability_result:
        lines.extend([
            "## Passage-Level Citability Analysis",
            "",
            f"**Average Citability Score:** {citability_result['average_citability_score']}/100",
            f"**Content Blocks Analyzed:** {citability_result['total_blocks_analyzed']}",
            f"**Optimal Length Passages (134-167 words):** {citability_result['optimal_length_passages']}",
            "",
            "Grade distribution:",
            "",
        ])
        gd = citability_result.get("grade_distribution", {})
        lines.append("| Grade | Count | Meaning |")
        lines.append("|-------|-------|---------|")
        lines.append(f"| A | {gd.get('A', 0)} | Highly Citable |")
        lines.append(f"| B | {gd.get('B', 0)} | Good |")
        lines.append(f"| C | {gd.get('C', 0)} | Moderate |")
        lines.append(f"| D | {gd.get('D', 0)} | Low |")
        lines.append(f"| F | {gd.get('F', 0)} | Poor |")
        lines.append("")

        top = citability_result.get("top_5_citable", [])
        if top:
            lines.append("### Top Citable Passages")
            lines.append("")
            for i, b in enumerate(top[:3], 1):
                lines.append(f"{i}. **{b['heading']}** (Score: {b['total_score']}/100, {b['word_count']} words)")
                lines.append(f"   - {b['preview']}")
            lines.append("")

        bottom = citability_result.get("bottom_5_citable", [])
        if bottom:
            lines.append("### Rewrite Priority (Lowest Scoring)")
            lines.append("")
            for i, b in enumerate(bottom[:3], 1):
                lines.append(f"{i}. **{b['heading']}** (Score: {b['total_score']}/100, {b['word_count']} words)")
            lines.append("")

        lines.extend(["---", ""])

    # Citation results (if available)
    if citation_data:
        lines.extend([
            "## AI Citation Check",
            "",
            f"**Citation Score:** {citation_data.get('overall_score', 0)}/100",
            "",
        ])
        for model_id, info in citation_data.get("model_results", {}).items():
            label = info["label"]
            mentioned = info["mentioned_in"]
            total = info["queries_tested"]
            lines.append(f"- **{label}**: Mentioned in {mentioned}/{total} queries")
        lines.extend(["", "---", ""])

    # Generated schemas (if there are gaps)
    missing_schemas = schema_analysis.get("missing_schemas", [])
    high_priority_missing = [m for m in missing_schemas if m.get("priority") == "high"]

    if high_priority_missing:
        lines.extend([
            "## Generated Schemas (Ready to Implement)",
            "",
        ])
        for m in high_priority_missing:
            schema_type = m["type"]
            generated = generate_schema(schema_type, crawl_data)
            lines.append(f"### {schema_type}")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(generated, indent=2))
            lines.append("```")
            lines.append("")

    # Package recommendation
    lines.extend([
        "---",
        "",
        "## Recommended Next Steps",
        "",
    ])

    if composite < 40:
        lines.append("**Recommended: Full AEO Foundation Package (Layer 1)**")
        lines.append("")
        lines.append("This site needs foundational work across schema markup, FAQ content, and AI crawler optimization. We recommend the full Layer 1 implementation:")
        lines.append("")
        lines.append("- Schema markup: Organization/LocalBusiness, FAQPage, Service")
        lines.append("- llms.txt and robots.txt optimization")
        lines.append("- FAQ page creation with proper schema")
        lines.append("- Content restructuring for AI readability")
    elif composite < 65:
        lines.append("**Recommended: Targeted AEO Fixes**")
        lines.append("")
        lines.append("The foundation exists but has specific gaps. We recommend targeted fixes:")
        lines.append("")
        for rec in recs[:5]:
            lines.append(f"- {rec}")
    else:
        lines.append("**Recommended: Visibility & Monitoring**")
        lines.append("")
        lines.append("Technical foundation is solid. Focus shifts to Layer 2 (Visibility Strategy):")
        lines.append("")
        lines.append("- Third-party mention building")
        lines.append("- Citation monitoring")
        lines.append("- Content distribution for AI training data")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main audit pipeline
# ---------------------------------------------------------------------------

def run_audit(
    url: str,
    brand: str = "",
    industry: str = "",
    run_citations: bool = False,
    max_pages: int = 30,
    client_slug: str = "",
    quiet: bool = False,
    brand_data_path: str = "",
) -> dict:
    """Run the full AEO audit pipeline.

    Returns a dict with all results and the formatted report.
    """
    domain = urlparse(url).netloc

    if not brand:
        brand = domain

    def log(msg):
        if not quiet:
            print(msg)

    # Step 1: Crawl homepage
    log(f"[1/5] Crawling {url}...")
    crawl_data = crawl_url(url)

    if crawl_data.get("errors"):
        for err in crawl_data["errors"]:
            log(f"  Warning: {err}")

    # Step 2: Schema analysis
    log("[2/5] Analyzing schemas...")
    schema_analysis = detect_schemas(crawl_data)
    log(f"  Found {len(schema_analysis.get('existing_types', []))} schema types, "
        f"{len(schema_analysis.get('missing_schemas', []))} gaps")

    # Step 3: Multi-page crawl
    log(f"[3/5] Crawling site (up to {max_pages} pages)...")
    site_analysis = analyze_site(url, max_pages=max_pages)
    log(f"  Crawled {site_analysis['pages_crawled']} pages, "
        f"{site_analysis['schema_coverage_pct']}% have schema markup")

    # Step 4: Citation check (optional)
    citation_data = None
    if run_citations:
        log("[4/5] Running citation checks (this takes 30-60 seconds)...")
        try:
            from citation_checker import check_citations
            citation_data = check_citations(brand, industry, url)
            log(f"  Citation score: {citation_data.get('overall_score', 0)}/100")
        except Exception as exc:
            log(f"  Citation check failed: {exc}")
    else:
        log("[4/5] Skipping citation check (use --citations to enable)")

    # Step 5: Passage-level citability analysis
    log("[5/5] Analyzing passage-level citability...")
    citability_result = analyze_page_citability(url)
    if "error" not in citability_result:
        log(f"  Analyzed {citability_result['total_blocks_analyzed']} content blocks, "
            f"avg citability: {citability_result['average_citability_score']}/100, "
            f"{citability_result['optimal_length_passages']} passages in optimal range (134-167 words)")
    else:
        log(f"  Citability analysis skipped: {citability_result.get('error')}")

    # Optional: brand authority from manually-collected platform data
    # (off-site mentions are the strongest measured AI-citation correlate)
    brand_authority = None
    if brand_data_path:
        try:
            from brand_authority_scorer import score_brand_authority
            with open(brand_data_path) as f:
                platform_data = json.load(f)
            brand_authority = score_brand_authority(
                youtube_data=platform_data.get("youtube"),
                reddit_data=platform_data.get("reddit"),
                wikipedia_data=platform_data.get("wikipedia"),
                linkedin_data=platform_data.get("linkedin"),
                other_data=platform_data.get("other"),
            )
            log(f"  Brand authority score: {brand_authority['composite_score']}/100")
        except Exception as exc:
            log(f"  Brand authority scoring failed: {exc}")

    # Score
    log("\nScoring...")
    score_result = score_site(crawl_data, schema_analysis, citation_data, brand_authority)
    log(f"  Composite score: {score_result['composite_score']}/100 (Grade: {score_result['grade']})")

    # Build report
    report = _build_full_report(
        crawl_data, schema_analysis, site_analysis,
        score_result, citation_data, brand, industry,
        citability_result if "error" not in citability_result else None,
    )

    result = {
        "url": url,
        "domain": domain,
        "brand": brand,
        "industry": industry,
        "date": datetime.now().isoformat(),
        "composite_score": score_result["composite_score"],
        "grade": score_result["grade"],
        "dimensions": score_result["dimensions"],
        "recommendations": score_result["recommendations"],
        "citability_analysis": {
            "average_score": citability_result.get("average_citability_score", 0),
            "blocks_analyzed": citability_result.get("total_blocks_analyzed", 0),
            "optimal_length_passages": citability_result.get("optimal_length_passages", 0),
            "grade_distribution": citability_result.get("grade_distribution", {}),
        } if "error" not in citability_result else None,
        "schema_analysis": {
            "existing_types": schema_analysis.get("existing_types", []),
            "missing_schemas": schema_analysis.get("missing_schemas", []),
            "gap_score": schema_analysis.get("gap_score", 0),
        },
        "site_analysis": {
            "pages_crawled": site_analysis.get("pages_crawled", 0),
            "pages_with_schema": site_analysis.get("pages_with_schema", 0),
            "schema_coverage_pct": site_analysis.get("schema_coverage_pct", 0),
            "types_found": site_analysis.get("json_ld_types_found", []),
            "types_missing": site_analysis.get("important_types_missing", []),
        },
        "citation_score": citation_data.get("overall_score") if citation_data else None,
        "brand_authority_score": brand_authority.get("composite_score") if brand_authority else None,
        "report": report,
    }

    # Save to client folder if specified
    if client_slug:
        _save_to_client_folder(client_slug, result, report, schema_analysis, crawl_data, citability_result)
        log(f"\nSaved to clients/{client_slug}/")

    return result


def _save_to_client_folder(
    client_slug: str,
    result: dict,
    report: str,
    schema_analysis: dict,
    crawl_data: dict,
    citability_result: dict | None = None,
):
    """Save all audit artifacts to the client folder."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    client_dir = os.path.join(base, "clients", client_slug)

    # Create subdirectories
    for subdir in ["audit", "schemas", "content", "reports"]:
        os.makedirs(os.path.join(client_dir, subdir), exist_ok=True)

    date_str = datetime.now().strftime("%Y%m%d")

    # Save the full report
    report_path = os.path.join(client_dir, "audit", f"aeo-audit-report.md")
    with open(report_path, "w") as f:
        f.write(report)

    # Save score data as JSON
    score_path = os.path.join(client_dir, "audit", f"score-data.json")
    score_data = {k: v for k, v in result.items() if k != "report"}
    with open(score_path, "w") as f:
        json.dump(score_data, f, indent=2, default=str)

    # Save citability report
    if citability_result and "error" not in citability_result:
        cit_report = format_citability_report(citability_result)
        cit_path = os.path.join(client_dir, "audit", "citability-report.md")
        with open(cit_path, "w") as f:
            f.write(cit_report)

    # Generate and save missing schemas
    missing = schema_analysis.get("missing_schemas", [])
    for m in missing:
        if m.get("priority") in ("high", "medium"):
            schema_type = m["type"]
            schema = generate_schema(schema_type, crawl_data)
            filename = f"{schema_type.lower().replace(' ', '-')}.json"
            schema_path = os.path.join(client_dir, "schemas", filename)
            with open(schema_path, "w") as f:
                json.dump(schema, f, indent=2)

    # Generate llms.txt if missing
    if crawl_data.get("llms_txt") is None:
        llms_path = os.path.join(client_dir, "content", "llms.txt")
        if not os.path.exists(llms_path):
            domain = crawl_data.get("domain", "example.com")
            title = crawl_data.get("title", "").split("|")[0].split("-")[0].strip()
            meta = crawl_data.get("meta_description", "")
            llms_content = f"""# {title or domain}

> {meta}

## About
{title or domain} is a business located at https://{domain}/

## Key Pages
- Homepage: https://{domain}/
- About: https://{domain}/about/
- Services: https://{domain}/services/
- Contact: https://{domain}/contact/

## Services
[List your services here]

## Locations
[List your locations here]
"""
            with open(llms_path, "w") as f:
                f.write(llms_content)

    # Generate recommended robots.txt additions
    robots_path = os.path.join(client_dir, "content", "robots-recommended.txt")
    if not os.path.exists(robots_path):
        robots_content = """# Recommended robots.txt additions for AI crawler access
# Add these to your existing robots.txt
#
# The AI bot fleet has three tiers (June 2026). SEARCH and USER tiers
# gate your visibility in AI answers -- allow them. TRAINING tier is a
# business/licensing decision; allowing it builds long-term model memory.
#
# NOTE: if you're behind Cloudflare, also check AI Crawl Control --
# Cloudflare default-blocks unverified AI crawlers regardless of
# robots.txt.

# --- SEARCH-INDEX crawlers (gate AI search visibility -- allow) ---
User-agent: OAI-SearchBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

# --- USER-INITIATED fetchers (a human asked the AI to read your page) ---
User-agent: ChatGPT-User
Allow: /

User-agent: Claude-User
Allow: /

User-agent: Perplexity-User
Allow: /

# --- TRAINING crawlers (long-term model memory -- recommended: allow) ---
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

# Reference your sitemap
Sitemap: https://YOURDOMAIN.com/sitemap.xml
"""
        with open(robots_path, "w") as f:
            f.write(robots_content)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Run a full AEO audit on a website.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 aeo_audit.py https://example.com
  python3 aeo_audit.py https://example.com --brand "Acme Corp" --industry "consulting"
  python3 aeo_audit.py https://example.com --citations --client acme --pages 50
        """,
    )
    parser.add_argument("url", help="URL to audit")
    parser.add_argument("--brand", default="", help="Brand name for citation checks")
    parser.add_argument("--industry", default="", help="Industry for context")
    parser.add_argument("--citations", action="store_true", help="Run AI citation checks (slower)")
    parser.add_argument("--pages", type=int, default=30, help="Max pages to crawl (default: 30)")
    parser.add_argument("--client", default="", help="Client slug for saving to client folder")
    parser.add_argument("--brand-data", default="", help="Path to JSON with platform data for brand authority scoring (keys: youtube, reddit, wikipedia, linkedin, other)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON data")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress messages")

    args = parser.parse_args()

    result = run_audit(
        url=args.url,
        brand=args.brand,
        industry=args.industry,
        run_citations=args.citations,
        max_pages=args.pages,
        client_slug=args.client,
        quiet=args.quiet,
        brand_data_path=args.brand_data,
    )

    if args.json:
        output = {k: v for k, v in result.items() if k != "report"}
        print(json.dumps(output, indent=2, default=str))
    else:
        print()
        print(result["report"])


if __name__ == "__main__":
    main()
