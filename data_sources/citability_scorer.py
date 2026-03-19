#!/usr/bin/env python3
"""
Passage-Level Citability Scorer.

Scores individual content blocks on a page for AI citation readiness.
Complements the page-level citability score in aeo_scorer.py with
granular, passage-by-passage analysis.

Based on research showing optimal AI-cited passages are:
- 134-167 words long (Bortolato 2025)
- Self-contained (extractable without surrounding context)
- Fact-rich with specific statistics
- Structured with clear answer patterns

Adapted from zubair-trabzada/geo-seo-claude, integrated into the
AEO Machine scoring pipeline.
"""

import sys
import json
import re
from typing import Optional

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Required packages not installed. Run: pip install -r requirements.txt")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Passage-level scoring
# ---------------------------------------------------------------------------

def score_passage(text: str, heading: Optional[str] = None) -> dict:
    """Score a single passage for AI citability (0-100).

    Five dimensions:
        1. Answer Block Quality (30%) -- does the passage directly answer a question?
        2. Self-Containment (25%) -- can AI extract it without surrounding context?
        3. Structural Readability (20%) -- clean sentences, lists, paragraphs
        4. Statistical Density (15%) -- specific numbers, named sources, dates
        5. Uniqueness Signals (10%) -- original data, case studies, proprietary insights
    """
    words = text.split()
    word_count = len(words)

    scores = {
        "answer_block_quality": 0,
        "self_containment": 0,
        "structural_readability": 0,
        "statistical_density": 0,
        "uniqueness_signals": 0,
    }

    # === 1. Answer Block Quality (30%) ===
    abq = 0

    # Definition patterns ("X is...", "X refers to...")
    definition_patterns = [
        r"\b\w+\s+is\s+(?:a|an|the)\s",
        r"\b\w+\s+refers?\s+to\s",
        r"\b\w+\s+means?\s",
        r"\b\w+\s+(?:can be |are )?defined\s+as\s",
        r"\bin\s+(?:simple|other)\s+(?:terms|words)\s*,",
    ]
    for pattern in definition_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            abq += 15
            break

    # Answer appears early (first 60 words contain facts/definitions)
    first_60 = " ".join(words[:60])
    if any(
        re.search(p, first_60, re.IGNORECASE)
        for p in [
            r"\b(?:is|are|was|were|means?|refers?)\b",
            r"\d+%",
            r"\$[\d,]+",
            r"\d+\s+(?:million|billion|thousand)",
        ]
    ):
        abq += 15

    # Question-based heading bonus
    if heading and heading.strip().endswith("?"):
        abq += 10

    # Clear, direct sentence structure
    sentences = re.split(r"[.!?]+", text)
    sentences = [s for s in sentences if s.strip()]
    short_clear = sum(1 for s in sentences if 5 <= len(s.split()) <= 25)
    if sentences:
        clarity_ratio = short_clear / len(sentences)
        abq += int(clarity_ratio * 10)

    # Research/authority attribution
    if re.search(
        r"(?:according to|research shows|studies? (?:show|indicate|suggest|found)|data (?:shows|indicates|suggests))",
        text,
        re.IGNORECASE,
    ):
        abq += 10

    scores["answer_block_quality"] = min(abq, 30)

    # === 2. Self-Containment (25%) ===
    sc = 0

    # Optimal word count (134-167 words is the sweet spot)
    if 134 <= word_count <= 167:
        sc += 10
    elif 100 <= word_count <= 200:
        sc += 7
    elif 80 <= word_count <= 250:
        sc += 4
    elif word_count < 30 or word_count > 400:
        sc += 0
    else:
        sc += 2

    # Low pronoun density = more self-contained
    pronoun_count = len(
        re.findall(
            r"\b(?:it|they|them|their|this|that|these|those|he|she|his|her)\b",
            text,
            re.IGNORECASE,
        )
    )
    if word_count > 0:
        pronoun_ratio = pronoun_count / word_count
        if pronoun_ratio < 0.02:
            sc += 8
        elif pronoun_ratio < 0.04:
            sc += 5
        elif pronoun_ratio < 0.06:
            sc += 3

    # Named entities (proper nouns, brands, specific terms)
    proper_nouns = len(re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", text))
    if proper_nouns >= 3:
        sc += 7
    elif proper_nouns >= 1:
        sc += 4

    scores["self_containment"] = min(sc, 25)

    # === 3. Structural Readability (20%) ===
    sr = 0

    if sentences:
        avg_len = word_count / len(sentences)
        if 10 <= avg_len <= 20:
            sr += 8
        elif 8 <= avg_len <= 25:
            sr += 5
        else:
            sr += 2

    # List-like structures
    if re.search(r"(?:first|second|third|finally|additionally|moreover)", text, re.IGNORECASE):
        sr += 4

    # Numbered items
    if re.search(r"(?:\d+[\.\)]\s|\b(?:step|tip|point)\s+\d+)", text, re.IGNORECASE):
        sr += 4

    # Paragraph breaks
    if "\n" in text:
        sr += 4

    scores["structural_readability"] = min(sr, 20)

    # === 4. Statistical Density (15%) ===
    sd = 0

    # Percentages
    pct_count = len(re.findall(r"\d+(?:\.\d+)?%", text))
    sd += min(pct_count * 3, 6)

    # Dollar amounts
    dollar_count = len(re.findall(r"\$[\d,]+(?:\.\d+)?(?:\s*(?:million|billion|M|B|K))?", text))
    sd += min(dollar_count * 3, 5)

    # Numbers with context
    number_count = len(re.findall(
        r"\b\d+(?:,\d{3})*(?:\.\d+)?\s+(?:users|customers|pages|sites|companies|businesses|people|percent|times|x\b)",
        text, re.IGNORECASE
    ))
    sd += min(number_count * 2, 4)

    # Year references (timeliness)
    if re.findall(r"\b20(?:2[3-6]|1\d)\b", text):
        sd += 2

    # Named sources
    source_patterns = [
        r"(?:according to|per|from|by)\s+[A-Z]",
        r"(?:Gartner|Forrester|McKinsey|Harvard|Stanford|MIT|Google|Microsoft|OpenAI|Anthropic)",
        r"\([A-Z][a-z]+(?:\s+\d{4})?\)",
    ]
    for pattern in source_patterns:
        if re.search(pattern, text):
            sd += 2

    scores["statistical_density"] = min(sd, 15)

    # === 5. Uniqueness Signals (10%) ===
    us = 0

    # Original data indicators
    if re.search(
        r"(?:our (?:research|study|data|analysis|survey|findings)|we (?:found|discovered|analyzed|surveyed|measured))",
        text, re.IGNORECASE,
    ):
        us += 5

    # Case study / example indicators
    if re.search(
        r"(?:case study|for example|for instance|in practice|real-world|hands-on)",
        text, re.IGNORECASE,
    ):
        us += 3

    # Specific tool/product mentions
    if re.search(r"(?:using|with|via|through)\s+[A-Z][a-z]+", text):
        us += 2

    scores["uniqueness_signals"] = min(us, 10)

    # === Total ===
    total = sum(scores.values())

    if total >= 80:
        grade, label = "A", "Highly Citable"
    elif total >= 65:
        grade, label = "B", "Good Citability"
    elif total >= 50:
        grade, label = "C", "Moderate Citability"
    elif total >= 35:
        grade, label = "D", "Low Citability"
    else:
        grade, label = "F", "Poor Citability"

    return {
        "heading": heading,
        "word_count": word_count,
        "total_score": total,
        "grade": grade,
        "label": label,
        "breakdown": scores,
        "preview": " ".join(words[:30]) + ("..." if word_count > 30 else ""),
    }


# ---------------------------------------------------------------------------
# Page-level analysis
# ---------------------------------------------------------------------------

def analyze_page_citability(url: str) -> dict:
    """Analyze all content blocks on a page for passage-level citability.

    Returns per-block scores, top/bottom 5, grade distribution,
    and the count of passages in the optimal 134-167 word range.
    """
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"},
            timeout=30,
        )
        response.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to fetch page: {str(e)}"}

    soup = BeautifulSoup(response.text, "lxml")

    # Strip non-content elements
    for el in soup.find_all(["script", "style", "nav", "footer", "header", "aside", "form"]):
        el.decompose()

    # Extract content blocks by heading sections
    blocks = []
    current_heading = "Introduction"
    current_paragraphs = []

    for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "ul", "ol", "table"]):
        if el.name.startswith("h"):
            if current_paragraphs:
                combined = " ".join(current_paragraphs)
                if len(combined.split()) >= 20:
                    blocks.append({"heading": current_heading, "content": combined})
            current_heading = el.get_text(strip=True)
            current_paragraphs = []
        else:
            text = el.get_text(strip=True)
            if text and len(text.split()) >= 5:
                current_paragraphs.append(text)

    # Last block
    if current_paragraphs:
        combined = " ".join(current_paragraphs)
        if len(combined.split()) >= 20:
            blocks.append({"heading": current_heading, "content": combined})

    # Score each block
    scored = [score_passage(b["content"], b["heading"]) for b in blocks]

    if scored:
        avg_score = sum(b["total_score"] for b in scored) / len(scored)
        top_5 = sorted(scored, key=lambda x: x["total_score"], reverse=True)[:5]
        bottom_5 = sorted(scored, key=lambda x: x["total_score"])[:5]
        optimal_count = sum(1 for b in scored if 134 <= b["word_count"] <= 167)
    else:
        avg_score = 0
        top_5, bottom_5 = [], []
        optimal_count = 0

    grade_dist = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for block in scored:
        grade_dist[block["grade"]] += 1

    return {
        "url": url,
        "total_blocks_analyzed": len(scored),
        "average_citability_score": round(avg_score, 1),
        "optimal_length_passages": optimal_count,
        "optimal_length_target": "134-167 words (Bortolato 2025)",
        "grade_distribution": grade_dist,
        "top_5_citable": top_5,
        "bottom_5_citable": bottom_5,
        "all_blocks": scored,
    }


def format_citability_report(result: dict) -> str:
    """Format a human-readable citability report."""
    if "error" in result:
        return f"Error: {result['error']}"

    lines = [
        f"# Passage-Level Citability Report",
        f"**URL:** {result['url']}",
        f"**Average Citability Score:** {result['average_citability_score']}/100",
        f"**Blocks Analyzed:** {result['total_blocks_analyzed']}",
        f"**Optimal Length Passages (134-167 words):** {result['optimal_length_passages']}",
        "",
        "## Grade Distribution",
        "",
        "| Grade | Count | Meaning |",
        "|-------|-------|---------|",
        f"| A | {result['grade_distribution']['A']} | Highly Citable |",
        f"| B | {result['grade_distribution']['B']} | Good Citability |",
        f"| C | {result['grade_distribution']['C']} | Moderate |",
        f"| D | {result['grade_distribution']['D']} | Low Citability |",
        f"| F | {result['grade_distribution']['F']} | Poor Citability |",
        "",
        "## Top 5 Most Citable Passages",
        "",
    ]

    for i, block in enumerate(result.get("top_5_citable", []), 1):
        lines.append(f"### {i}. {block['heading']} (Score: {block['total_score']}/100, Grade: {block['grade']})")
        lines.append(f"- Words: {block['word_count']}")
        lines.append(f"- Answer Quality: {block['breakdown']['answer_block_quality']}/30")
        lines.append(f"- Self-Containment: {block['breakdown']['self_containment']}/25")
        lines.append(f"- Readability: {block['breakdown']['structural_readability']}/20")
        lines.append(f"- Statistical Density: {block['breakdown']['statistical_density']}/15")
        lines.append(f"- Uniqueness: {block['breakdown']['uniqueness_signals']}/10")
        lines.append(f"- Preview: *{block['preview']}*")
        lines.append("")

    lines.append("## Bottom 5 (Rewrite Priority)")
    lines.append("")

    for i, block in enumerate(result.get("bottom_5_citable", []), 1):
        lines.append(f"### {i}. {block['heading']} (Score: {block['total_score']}/100, Grade: {block['grade']})")
        lines.append(f"- Words: {block['word_count']} {'(too short)' if block['word_count'] < 80 else '(too long)' if block['word_count'] > 250 else ''}")
        lines.append(f"- Preview: *{block['preview']}*")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python citability_scorer.py <url> [--json]")
        print("Scores every content block on a page for AI citability.")
        sys.exit(1)

    url = sys.argv[1]
    result = analyze_page_citability(url)

    if "--json" in sys.argv:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(format_citability_report(result))
