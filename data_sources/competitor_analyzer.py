"""
Competitor Analyzer for AEO Machine.

Runs the same crawl -> schema -> score pipeline on your site and one or
more competitors, then produces a side-by-side comparison highlighting
gaps, advantages, and quick wins.

Note: this compares ON-SITE AEO posture. Only ~11% of cited domains
overlap between ChatGPT and Perplexity, and off-site authority is the
strongest citation driver -- so pair this with citation checks and brand
authority assessment for the full picture.

Usage:
    python3 competitor_analyzer.py <your_url> <competitor_url> [competitor_url2 ...]
                                   [--pages 10] [--client client-slug] [--json]

Example:
    python3 competitor_analyzer.py https://yourclient.com https://rival.com \\
        --pages 10 --client yourclient
"""

import argparse
import json
import os
from datetime import datetime
from urllib.parse import urlparse

from site_crawler import crawl_url
from schema_detector import detect_schemas
from aeo_scorer import score_site


# ---------------------------------------------------------------------------
# Per-site analysis
# ---------------------------------------------------------------------------

def analyze_one(url: str, quiet: bool = False) -> dict:
    """Crawl and score a single site. Returns dict with crawl, schema, score."""
    if not quiet:
        print(f"  Crawling {url}...")
    crawl_data = crawl_url(url)

    schema_analysis = detect_schemas(crawl_data)
    score_result = score_site(crawl_data, schema_analysis)

    return {
        "url": url,
        "domain": crawl_data.get("domain", urlparse(url).netloc),
        "crawl_data": crawl_data,
        "schema_analysis": schema_analysis,
        "score_result": score_result,
    }


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------

def compare_sites(your_url: str, competitor_urls: list[str], quiet: bool = False) -> dict:
    """Run the full comparison. First URL is "you", the rest are competitors."""
    if not quiet:
        print(f"[1/{1 + len(competitor_urls)}] Analyzing your site...")
    you = analyze_one(your_url, quiet)

    competitors = []
    for i, comp_url in enumerate(competitor_urls, start=2):
        if not quiet:
            print(f"[{i}/{1 + len(competitor_urls)}] Analyzing competitor...")
        competitors.append(analyze_one(comp_url, quiet))

    comparison = _build_comparison(you, competitors)
    report = _format_comparison_report(you, competitors, comparison)

    return {
        "you": _strip_heavy(you),
        "competitors": [_strip_heavy(c) for c in competitors],
        "comparison": comparison,
        "report": report,
        "date": datetime.now().isoformat(),
    }


def _strip_heavy(site: dict) -> dict:
    """Drop raw HTML and verbose crawl data for JSON output."""
    return {
        "url": site["url"],
        "domain": site["domain"],
        "composite_score": site["score_result"]["composite_score"],
        "grade": site["score_result"]["grade"],
        "dimensions": {
            k: {"score": d["score"], "measured": d["measured"]}
            for k, d in site["score_result"]["dimensions"].items()
        },
        "existing_schema_types": site["schema_analysis"].get("existing_types", []),
        "faq_count": len(site["crawl_data"].get("faq_items", [])),
        "has_llms_txt": site["crawl_data"].get("llms_txt") is not None,
    }


def _build_comparison(you: dict, competitors: list[dict]) -> dict:
    """Compute per-dimension gaps against the best competitor."""
    your_dims = you["score_result"]["dimensions"]

    gaps = []       # dimensions where a competitor beats you
    advantages = [] # dimensions where you beat every competitor

    for key, your_dim in your_dims.items():
        if not your_dim["measured"]:
            continue

        comp_scores = []
        for comp in competitors:
            comp_dim = comp["score_result"]["dimensions"].get(key)
            if comp_dim and comp_dim["measured"]:
                comp_scores.append((comp["domain"], comp_dim["score"]))

        if not comp_scores:
            continue

        best_comp_domain, best_comp_score = max(comp_scores, key=lambda x: x[1])
        delta = your_dim["score"] - best_comp_score

        entry = {
            "dimension": key,
            "label": your_dim["label"],
            "weight": your_dim["weight"],
            "your_score": your_dim["score"],
            "best_competitor": best_comp_domain,
            "best_competitor_score": best_comp_score,
            "delta": delta,
        }
        if delta < 0:
            gaps.append(entry)
        else:
            advantages.append(entry)

    # Sort gaps by weighted impact (how much composite you give up)
    gaps.sort(key=lambda g: g["delta"] * g["weight"])
    advantages.sort(key=lambda a: -(a["delta"] * a["weight"]))

    # Quick wins: big gaps in dimensions that are cheap to fix on-site
    quick_win_dims = {"llms_txt", "crawler_access", "schema_structured", "faq_quality", "freshness"}
    quick_wins = [g for g in gaps if g["dimension"] in quick_win_dims and g["delta"] <= -15]

    # Schema types competitors have that you don't
    your_types = set(you["schema_analysis"].get("existing_types", []))
    schema_gaps = {}
    for comp in competitors:
        comp_types = set(comp["schema_analysis"].get("existing_types", []))
        missing = comp_types - your_types
        if missing:
            schema_gaps[comp["domain"]] = sorted(missing)

    return {
        "gaps": gaps,
        "advantages": advantages,
        "quick_wins": quick_wins,
        "schema_types_competitors_have": schema_gaps,
    }


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def _format_comparison_report(you: dict, competitors: list[dict], comparison: dict) -> str:
    date = datetime.now().strftime("%Y-%m-%d")
    your_score = you["score_result"]["composite_score"]
    your_grade = you["score_result"]["grade"]

    lines = [
        f"# Competitor AEO Comparison: {you['domain']}",
        "",
        f"**Date:** {date}",
        f"**Scope:** On-site AEO posture (pair with citation checks + brand authority for off-site)",
        "",
        "## Composite Scores",
        "",
        "| Site | Score | Grade |",
        "|------|-------|-------|",
        f"| **{you['domain']} (you)** | **{your_score}/100** | **{your_grade}** |",
    ]

    for comp in competitors:
        cs = comp["score_result"]["composite_score"]
        cg = comp["score_result"]["grade"]
        lines.append(f"| {comp['domain']} | {cs}/100 | {cg} |")

    # Dimension-by-dimension table
    lines.extend(["", "## Dimension Breakdown", ""])
    header = "| Dimension | " + you["domain"] + " | " + " | ".join(c["domain"] for c in competitors) + " |"
    sep = "|" + "---|" * (2 + len(competitors))
    lines.extend([header, sep])

    for key, your_dim in you["score_result"]["dimensions"].items():
        row = [your_dim["label"]]
        row.append(str(your_dim["score"]) if your_dim["measured"] else "n/m")
        for comp in competitors:
            comp_dim = comp["score_result"]["dimensions"].get(key, {})
            if comp_dim.get("measured"):
                row.append(str(comp_dim["score"]))
            else:
                row.append("n/m")
        lines.append("| " + " | ".join(row) + " |")

    # Gaps
    gaps = comparison["gaps"]
    if gaps:
        lines.extend(["", "## Where Competitors Beat You", ""])
        for g in gaps:
            lines.append(
                f"- **{g['label']}** ({int(g['weight'] * 100)}% weight): "
                f"you {g['your_score']}/100 vs {g['best_competitor']} "
                f"{g['best_competitor_score']}/100 ({g['delta']:+d})"
            )

    # Advantages
    advantages = comparison["advantages"]
    if advantages:
        lines.extend(["", "## Where You Lead", ""])
        for a in advantages[:5]:
            lines.append(
                f"- **{a['label']}**: you {a['your_score']}/100 vs best competitor "
                f"{a['best_competitor_score']}/100 ({a['delta']:+d})"
            )

    # Quick wins
    quick_wins = comparison["quick_wins"]
    if quick_wins:
        lines.extend(["", "## Quick Wins (cheap on-site fixes with big deltas)", ""])
        for i, q in enumerate(quick_wins, 1):
            lines.append(f"{i}. Close the **{q['label']}** gap ({q['delta']:+d} vs {q['best_competitor']})")

    # Schema type gaps
    schema_gaps = comparison["schema_types_competitors_have"]
    if schema_gaps:
        lines.extend(["", "## Schema Types Competitors Have That You Don't", ""])
        for domain, types in schema_gaps.items():
            lines.append(f"- **{domain}**: {', '.join(types)}")

    lines.extend([
        "",
        "---",
        "",
        "*On-site scores only. Off-site authority (mentions, Reddit, reviews, press) is the "
        "strongest AI citation driver and isn't visible in this comparison -- run the brand "
        "authority assessment and citation checks on both brands for the full picture.*",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Save to client folder
# ---------------------------------------------------------------------------

def _save_to_client_folder(client_slug: str, result: dict):
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    client_dir = os.path.join(base, "clients", client_slug, "audit")
    os.makedirs(client_dir, exist_ok=True)

    report_path = os.path.join(client_dir, "competitor-comparison.md")
    with open(report_path, "w") as f:
        f.write(result["report"])

    data_path = os.path.join(client_dir, "competitor-data.json")
    data = {k: v for k, v in result.items() if k != "report"}
    with open(data_path, "w") as f:
        json.dump(data, f, indent=2, default=str)

    return report_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Head-to-head AEO comparison: your site vs competitors.",
    )
    parser.add_argument("your_url", help="Your (or your client's) URL")
    parser.add_argument("competitor_urls", nargs="+", help="One or more competitor URLs")
    parser.add_argument("--client", default="", help="Client slug for saving to client folder")
    parser.add_argument("--json", action="store_true", help="Output raw JSON data")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress messages")

    args = parser.parse_args()

    result = compare_sites(args.your_url, args.competitor_urls, quiet=args.quiet)

    if args.client:
        path = _save_to_client_folder(args.client, result)
        if not args.quiet:
            print(f"\nSaved to {path}")

    if args.json:
        output = {k: v for k, v in result.items() if k != "report"}
        print(json.dumps(output, indent=2, default=str))
    else:
        print()
        print(result["report"])


if __name__ == "__main__":
    main()
