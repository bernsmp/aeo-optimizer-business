#!/usr/bin/env python3
"""
Brand Authority Scorer.

Scores brand authority across the platforms that correlate most strongly
with AI citation rates, using weighted formula from Ahrefs Dec 2025 study
(75K brands).

Key finding: brand mentions correlate 3x more strongly with AI visibility
than backlinks.

Platform weights (correlation-based):
    YouTube:    25% (0.737 correlation with AI citation)
    Reddit:     25% (highest-cited domain across ChatGPT + Perplexity)
    Wikipedia:  20% (top single ChatGPT citation domain, ~13.2% per 5W May 2026)
    LinkedIn:   15% (professional authority signal)
    Other:      15% (Crunchbase, G2, industry directories, podcasts)

Stats refreshed 2026-06-11. Citation-share numbers are volatile; re-verify
quarterly before quoting in client deliverables.

Adapted from zubair-trabzada/geo-seo-claude brand authority formula,
integrated into the AEO Machine visibility layer.
"""

from typing import Optional


# ---------------------------------------------------------------------------
# Platform scoring rubrics (each 0-100)
# ---------------------------------------------------------------------------

def score_youtube(data: dict) -> int:
    """Score YouTube presence 0-100.

    data keys:
        channel_exists (bool)
        subscriber_count (int)
        video_count (int)
        avg_views (int)
        recent_upload_days (int) -- days since last upload
        brand_search_videos (int) -- videos mentioning brand by others
    """
    score = 0

    if not data.get("channel_exists"):
        return 0

    score += 15  # channel exists

    # Subscribers
    subs = data.get("subscriber_count", 0)
    if subs >= 100_000:
        score += 20
    elif subs >= 10_000:
        score += 15
    elif subs >= 1_000:
        score += 10
    elif subs >= 100:
        score += 5

    # Video count
    vids = data.get("video_count", 0)
    if vids >= 50:
        score += 15
    elif vids >= 20:
        score += 10
    elif vids >= 5:
        score += 5

    # Average views
    avg = data.get("avg_views", 0)
    if avg >= 10_000:
        score += 15
    elif avg >= 1_000:
        score += 10
    elif avg >= 100:
        score += 5

    # Recency
    days = data.get("recent_upload_days", 999)
    if days <= 30:
        score += 15
    elif days <= 90:
        score += 10
    elif days <= 180:
        score += 5

    # Third-party mentions (others making videos about you)
    mentions = data.get("brand_search_videos", 0)
    if mentions >= 10:
        score += 20
    elif mentions >= 5:
        score += 12
    elif mentions >= 1:
        score += 5

    return min(score, 100)


def score_reddit(data: dict) -> int:
    """Score Reddit presence 0-100.

    data keys:
        brand_mentions (int) -- total mentions found
        subreddits_mentioned_in (int)
        positive_sentiment_ratio (float) -- 0.0-1.0
        recent_mentions_30d (int)
        has_official_account (bool)
    """
    score = 0

    mentions = data.get("brand_mentions", 0)
    if mentions == 0:
        return 0

    # Total mentions
    if mentions >= 100:
        score += 25
    elif mentions >= 50:
        score += 20
    elif mentions >= 20:
        score += 15
    elif mentions >= 5:
        score += 10
    else:
        score += 5

    # Subreddit spread (breadth)
    subs = data.get("subreddits_mentioned_in", 0)
    if subs >= 10:
        score += 20
    elif subs >= 5:
        score += 15
    elif subs >= 2:
        score += 10
    else:
        score += 5

    # Sentiment
    sentiment = data.get("positive_sentiment_ratio", 0.5)
    if sentiment >= 0.7:
        score += 20
    elif sentiment >= 0.5:
        score += 12
    elif sentiment >= 0.3:
        score += 5

    # Recency
    recent = data.get("recent_mentions_30d", 0)
    if recent >= 10:
        score += 20
    elif recent >= 5:
        score += 15
    elif recent >= 1:
        score += 10

    # Official presence
    if data.get("has_official_account"):
        score += 15

    return min(score, 100)


def score_wikipedia(data: dict) -> int:
    """Score Wikipedia/Wikidata presence 0-100.

    data keys:
        has_wikipedia_page (bool)
        has_wikidata_entry (bool)
        page_length_bytes (int)
        reference_count (int)
        languages (int) -- number of language editions
        last_edit_days (int)
    """
    score = 0

    if data.get("has_wikipedia_page"):
        score += 30

        # Page completeness
        length = data.get("page_length_bytes", 0)
        if length >= 50_000:
            score += 15
        elif length >= 20_000:
            score += 10
        elif length >= 5_000:
            score += 5

        # References
        refs = data.get("reference_count", 0)
        if refs >= 50:
            score += 15
        elif refs >= 20:
            score += 10
        elif refs >= 5:
            score += 5

        # Multi-language (global authority)
        langs = data.get("languages", 1)
        if langs >= 10:
            score += 10
        elif langs >= 3:
            score += 5

        # Freshness
        days = data.get("last_edit_days", 999)
        if days <= 90:
            score += 10
        elif days <= 365:
            score += 5

    elif data.get("has_wikidata_entry"):
        score += 15  # Wikidata only, no full article

    return min(score, 100)


def score_linkedin(data: dict) -> int:
    """Score LinkedIn presence 0-100.

    data keys:
        has_company_page (bool)
        follower_count (int)
        employee_count (int)
        post_frequency_monthly (int)
        engagement_rate (float)
        founder_followers (int) -- personal brand of founder/CEO
    """
    score = 0

    if not data.get("has_company_page"):
        # Personal brand can still score
        founder = data.get("founder_followers", 0)
        if founder >= 10_000:
            return 50
        elif founder >= 1_000:
            return 30
        elif founder >= 500:
            return 15
        return 0

    score += 10  # page exists

    # Followers
    followers = data.get("follower_count", 0)
    if followers >= 50_000:
        score += 20
    elif followers >= 10_000:
        score += 15
    elif followers >= 1_000:
        score += 10
    elif followers >= 100:
        score += 5

    # Employee count (credibility)
    employees = data.get("employee_count", 0)
    if employees >= 50:
        score += 15
    elif employees >= 10:
        score += 10
    elif employees >= 2:
        score += 5

    # Posting frequency
    posts = data.get("post_frequency_monthly", 0)
    if posts >= 12:
        score += 15
    elif posts >= 4:
        score += 10
    elif posts >= 1:
        score += 5

    # Founder personal brand
    founder = data.get("founder_followers", 0)
    if founder >= 10_000:
        score += 20
    elif founder >= 1_000:
        score += 10
    elif founder >= 500:
        score += 5

    # Engagement
    engagement = data.get("engagement_rate", 0)
    if engagement >= 0.05:
        score += 20
    elif engagement >= 0.02:
        score += 10
    elif engagement >= 0.01:
        score += 5

    return min(score, 100)


def score_other_platforms(data: dict) -> int:
    """Score other authority platforms 0-100.

    data keys:
        g2_listed (bool)
        g2_rating (float)
        crunchbase_listed (bool)
        podcast_appearances (int)
        industry_directories (int) -- listed in industry-specific directories
        press_mentions (int)
        github_stars (int) -- for tech companies
    """
    score = 0

    if data.get("g2_listed"):
        score += 15
        rating = data.get("g2_rating", 0)
        if rating >= 4.5:
            score += 10
        elif rating >= 4.0:
            score += 5

    if data.get("crunchbase_listed"):
        score += 10

    podcasts = data.get("podcast_appearances", 0)
    if podcasts >= 10:
        score += 20
    elif podcasts >= 5:
        score += 15
    elif podcasts >= 1:
        score += 10

    directories = data.get("industry_directories", 0)
    if directories >= 5:
        score += 15
    elif directories >= 2:
        score += 10
    elif directories >= 1:
        score += 5

    press = data.get("press_mentions", 0)
    if press >= 10:
        score += 15
    elif press >= 3:
        score += 10
    elif press >= 1:
        score += 5

    stars = data.get("github_stars", 0)
    if stars >= 1_000:
        score += 15
    elif stars >= 100:
        score += 10
    elif stars >= 10:
        score += 5

    return min(score, 100)


# ---------------------------------------------------------------------------
# Composite Brand Authority Score
# ---------------------------------------------------------------------------

BRAND_WEIGHTS = {
    "youtube":   0.25,  # 0.737 correlation with AI citation (Ahrefs Dec 2025)
    "reddit":    0.25,  # top-cited on Perplexity (~47% of top-10, volatile); ~12.0% of ChatGPT citations (5W May 2026)
    "wikipedia": 0.20,  # top single ChatGPT citation domain, ~13.2% (5W May 2026; was widely quoted at 47.9% in 2025)
    "linkedin":  0.15,  # professional authority signal
    "other":     0.15,  # directories, press, podcasts, Crunchbase, G2
}


def score_brand_authority(
    youtube_data: Optional[dict] = None,
    reddit_data: Optional[dict] = None,
    wikipedia_data: Optional[dict] = None,
    linkedin_data: Optional[dict] = None,
    other_data: Optional[dict] = None,
) -> dict:
    """Compute composite Brand Authority Score (0-100).

    Args:
        *_data: Platform-specific data dicts. Pass None or {} for unknown platforms.

    Returns:
        Dict with composite score, per-platform breakdown, grade, and recommendations.
    """
    platforms = {
        "youtube": {
            "score": score_youtube(youtube_data or {}),
            "weight": BRAND_WEIGHTS["youtube"],
            "label": "YouTube (0.737 correlation)",
        },
        "reddit": {
            "score": score_reddit(reddit_data or {}),
            "weight": BRAND_WEIGHTS["reddit"],
            "label": "Reddit",
        },
        "wikipedia": {
            "score": score_wikipedia(wikipedia_data or {}),
            "weight": BRAND_WEIGHTS["wikipedia"],
            "label": "Wikipedia / Wikidata",
        },
        "linkedin": {
            "score": score_linkedin(linkedin_data or {}),
            "weight": BRAND_WEIGHTS["linkedin"],
            "label": "LinkedIn",
        },
        "other": {
            "score": score_other_platforms(other_data or {}),
            "weight": BRAND_WEIGHTS["other"],
            "label": "Other Platforms",
        },
    }

    composite = sum(p["score"] * p["weight"] for p in platforms.values())
    composite_score = round(composite)

    if composite_score >= 80:
        grade, label = "A", "Strong Brand Authority"
    elif composite_score >= 60:
        grade, label = "B", "Good Brand Authority"
    elif composite_score >= 40:
        grade, label = "C", "Moderate Brand Authority"
    elif composite_score >= 20:
        grade, label = "D", "Weak Brand Authority"
    else:
        grade, label = "F", "Minimal Brand Authority"

    # Recommendations based on weakest platforms
    recs = _brand_recommendations(platforms)

    return {
        "composite_score": composite_score,
        "grade": grade,
        "label": label,
        "platforms": platforms,
        "recommendations": recs,
        "key_stat": "Brand mentions correlate 3x more strongly with AI visibility than backlinks (Ahrefs Dec 2025, 75K brands)",
    }


def _brand_recommendations(platforms: dict) -> list[str]:
    """Generate recommendations from weakest platform scores."""
    recs = []
    sorted_platforms = sorted(platforms.items(), key=lambda x: x[1]["score"])

    for key, p in sorted_platforms:
        if p["score"] >= 60:
            continue

        if key == "youtube" and p["score"] < 40:
            recs.append(
                "YouTube is your #1 priority. It has the strongest correlation (0.737) "
                "with AI citation. Start with 5-10 short videos answering your top industry questions."
            )
        elif key == "reddit" and p["score"] < 40:
            recs.append(
                "Reddit is the top-cited domain on Perplexity and top-2 on ChatGPT. "
                "Start authentic engagement in 2-3 subreddits where your customers ask questions."
            )
        elif key == "wikipedia" and p["score"] < 40:
            recs.append(
                "Wikipedia is the single most-cited domain on ChatGPT (~13% of US citations, "
                "5W May 2026). If you qualify for a page, this is high-leverage. Start with "
                "a Wikidata entry."
            )
        elif key == "linkedin" and p["score"] < 40:
            recs.append(
                "Build founder/CEO personal brand on LinkedIn. "
                "AI models use LinkedIn as a professional authority signal."
            )
        elif key == "other" and p["score"] < 40:
            recs.append(
                "Get listed on industry directories, G2, and Crunchbase. "
                "Companies in 5+ authority sources get 2.7x higher AI mention rates."
            )

    return recs[:5]


def format_brand_report(result: dict) -> str:
    """Format a human-readable brand authority report."""
    lines = [
        "# Brand Authority Score Report",
        f"**Composite Score:** {result['composite_score']}/100 (Grade: {result['grade']})",
        f"**Assessment:** {result['label']}",
        "",
        f"> {result['key_stat']}",
        "",
        "## Platform Breakdown",
        "",
        "| Platform | Weight | Score | Weighted |",
        "|----------|--------|-------|----------|",
    ]

    for key, p in result["platforms"].items():
        weighted = round(p["score"] * p["weight"], 1)
        lines.append(f"| {p['label']} | {int(p['weight'] * 100)}% | {p['score']}/100 | {weighted} |")

    lines.append(f"| **TOTAL** | **100%** | | **{result['composite_score']}** |")
    lines.append("")

    if result["recommendations"]:
        lines.append("## Recommendations")
        lines.append("")
        for i, rec in enumerate(result["recommendations"], 1):
            lines.append(f"{i}. {rec}")

    return "\n".join(lines)
