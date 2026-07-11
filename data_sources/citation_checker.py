"""
Citation Checker Module for AEO Machine.

Queries multiple AI models through OpenRouter to check whether a brand
is being cited/mentioned in AI-generated responses. Returns a citability
score (0-100) with per-model breakdown and actionable recommendations.
"""

import json
import os
import re
import subprocess
import time
from typing import Optional

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Search-grounded models approximating consumer AI surfaces (which all do
# live web search now). The ":online" suffix adds web grounding through
# OpenRouter; Perplexity Sonar is natively search-grounded.
# IDs verified against the live OpenRouter catalog on 2026-06-11.
SURFACE_MODELS = {
    "openai/gpt-5.5:online": "ChatGPT (GPT-5.5 + web)",
    "google/gemini-3.5-flash:online": "Gemini (3.5 Flash + web)",
    "anthropic/claude-sonnet-4.6:online": "Claude (Sonnet 4.6 + web)",
    "perplexity/sonar-pro": "Perplexity (Sonar Pro)",
}

# Ungrounded versions of the same models probe training-data brand memory:
# does the model know the brand WITHOUT live retrieval? The surface/memory
# gap tells you whether the problem is retrieval (fixable with content and
# citability work, months) or durable brand presence (needs off-site
# authority building, longer).
MEMORY_MODELS = {
    "openai/gpt-5.5": "GPT-5.5 (no web)",
    "google/gemini-3.5-flash": "Gemini 3.5 Flash (no web)",
    "anthropic/claude-sonnet-4.6": "Claude Sonnet 4.6 (no web)",
}

MODELS = SURFACE_MODELS  # backward-compat alias

REQUEST_TIMEOUT = 45  # seconds per API call
RETRY_DELAY = 2       # seconds between retries on rate-limit
MAX_RETRIES = 2


# ---------------------------------------------------------------------------
# API key resolution
# ---------------------------------------------------------------------------

def _get_api_key() -> str:
    """Return the OpenRouter API key from env or 1Password CLI."""
    load_dotenv()
    key = os.getenv("OPENROUTER_API_KEY")
    if key:
        return key

    # Fallback: pull from 1Password CLI
    try:
        result = subprocess.run(
            ["op", "read", "op://Private/OpenRouter API Key/credential"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    raise EnvironmentError(
        "OPENROUTER_API_KEY not found in environment and 1Password CLI "
        "fallback failed. Set the env var or install the `op` CLI."
    )


# ---------------------------------------------------------------------------
# Query generation
# ---------------------------------------------------------------------------

def _build_queries(brand: str, industry: str, url: Optional[str] = None) -> list[str]:
    """Generate test queries a potential customer might type into an AI chat."""
    queries = [
        f"Who are the best {industry} providers?",
        f"What companies offer {industry} services?",
        f"Tell me about {brand}",
        f"Who should I hire for {industry}?",
        f"What is {industry} and who does it well?",
    ]
    return queries


# ---------------------------------------------------------------------------
# Citation quality scoring
# ---------------------------------------------------------------------------

def _score_response(brand: str, response_text: str) -> dict:
    """Score how well the brand is cited in a single model response.

    Returns:
        dict with keys: mentioned (bool), quality (int 0-100), context (str)
    """
    text_lower = response_text.lower()
    brand_lower = brand.lower()

    if brand_lower not in text_lower:
        return {"mentioned": False, "quality": 0, "context": "Not mentioned"}

    # Brand appears -- figure out sentiment / strength
    # Build a small window around the first mention for context
    idx = text_lower.index(brand_lower)
    start = max(0, idx - 120)
    end = min(len(response_text), idx + len(brand) + 120)
    snippet = response_text[start:end].replace("\n", " ").strip()

    # Simple heuristic: look for recommendation-strength language
    rec_patterns = [
        r"recommend",
        r"top\s+(choice|pick|option|provider)",
        r"leading",
        r"go-to",
        r"standout",
        r"excellent",
        r"highly\s+regarded",
        r"well[- ]known",
        r"trusted",
        r"specialist",
        r"expert",
    ]
    negative_patterns = [
        r"controversy",
        r"negative",
        r"avoid",
        r"poor",
        r"complaint",
        r"lawsuit",
    ]

    text_around = response_text[max(0, idx - 300):min(len(response_text), idx + 300)].lower()

    if any(re.search(p, text_around) for p in negative_patterns):
        return {"mentioned": True, "quality": 25, "context": snippet}

    if any(re.search(p, text_around) for p in rec_patterns):
        return {"mentioned": True, "quality": 100, "context": snippet}

    # Mentioned positively (general positive framing without strong rec)
    positive_lite = [r"known for", r"offers", r"provides", r"focuses on", r"specializ"]
    if any(re.search(p, text_around) for p in positive_lite):
        return {"mentioned": True, "quality": 75, "context": snippet}

    # Neutral mention
    return {"mentioned": True, "quality": 50, "context": snippet}


# ---------------------------------------------------------------------------
# OpenRouter API call
# ---------------------------------------------------------------------------

def _query_model(api_key: str, model: str, prompt: str) -> Optional[str]:
    """Send a single prompt to a model via OpenRouter. Returns response text or None."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://aeo-machine.com",
        "X-Title": "AEO Citation Checker",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 1024,
    }

    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = requests.post(
                OPENROUTER_BASE_URL,
                headers=headers,
                json=payload,
                timeout=REQUEST_TIMEOUT,
            )
            if resp.status_code == 429:
                # Rate limited -- back off
                wait = RETRY_DELAY * (attempt + 1)
                print(f"  Rate limited on {model}, waiting {wait}s...")
                time.sleep(wait)
                continue

            if resp.status_code != 200:
                print(f"  [{model}] HTTP {resp.status_code}: {resp.text[:200]}")
                return None

            data = resp.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.Timeout:
            print(f"  [{model}] Timeout on attempt {attempt + 1}")
        except (requests.exceptions.RequestException, KeyError, IndexError) as exc:
            print(f"  [{model}] Error: {exc}")
            return None

    return None


# ---------------------------------------------------------------------------
# Main checker
# ---------------------------------------------------------------------------

def _run_model_set(
    api_key: str,
    models: dict,
    queries: list[str],
    brand: str,
) -> tuple[dict, dict]:
    """Run all queries against a set of models. Returns (model_results, query_mention_counts)."""
    model_results: dict = {}
    query_mention_counts: dict[str, int] = {q: 0 for q in queries}

    for model_id, model_label in models.items():
        print(f"Querying {model_label}...")
        details = []
        mention_count = 0
        quality_sum = 0

        for query in queries:
            response_text = _query_model(api_key, model_id, query)
            if response_text is None:
                details.append({
                    "query": query,
                    "mentioned": False,
                    "quality": 0,
                    "context": "Model unavailable or error",
                    "error": True,
                })
                continue

            score_info = _score_response(brand, response_text)
            details.append({
                "query": query,
                "mentioned": score_info["mentioned"],
                "quality": score_info["quality"],
                "context": score_info["context"],
                "error": False,
            })
            if score_info["mentioned"]:
                mention_count += 1
                query_mention_counts[query] += 1
            quality_sum += score_info["quality"]

        avg_quality = quality_sum / len(queries) if queries else 0
        model_results[model_id] = {
            "label": model_label,
            "queries_tested": len(queries),
            "mentioned_in": mention_count,
            "average_quality": round(avg_quality, 1),
            "details": details,
        }

    return model_results, query_mention_counts


def check_citations(
    brand: str,
    industry: str = "consulting",
    url: Optional[str] = None,
    include_memory: bool = False,
) -> dict:
    """Run the full citation check across all models and queries.

    Args:
        brand: The brand or person name to check for.
        industry: Industry / service description for query generation.
        url: Optional website URL (reserved for future use).
        include_memory: Also probe ungrounded models to separate
            "live retrieval surfaces the brand" from "the model knows the
            brand from training data" -- different problems with different
            fixes.

    Returns:
        Dict with overall_score, model_results, memory_results, and report.
        overall_score reflects the search-grounded (surface) models only.
    """
    api_key = _get_api_key()
    queries = _build_queries(brand, industry, url)

    model_results, query_mention_counts = _run_model_set(
        api_key, SURFACE_MODELS, queries, brand
    )

    memory_results = None
    if include_memory:
        print("Running memory probe (ungrounded models)...")
        memory_results, _ = _run_model_set(api_key, MEMORY_MODELS, queries, brand)

    # Overall score: average of per-model average quality (surface only)
    if model_results:
        overall_score = round(
            sum(m["average_quality"] for m in model_results.values()) / len(model_results)
        )
    else:
        overall_score = 0

    # Best / worst queries
    best_query = max(query_mention_counts, key=query_mention_counts.get) if query_mention_counts else ""
    worst_query = min(query_mention_counts, key=query_mention_counts.get) if query_mention_counts else ""

    report = _build_report(
        brand, industry, overall_score, model_results, best_query, worst_query, memory_results
    )

    return {
        "brand": brand,
        "overall_score": overall_score,
        "model_results": model_results,
        "memory_results": memory_results,
        "report": report,
    }


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def _progress_bar(fraction: float, width: int = 20) -> str:
    filled = round(fraction * width)
    return "=" * filled + "-" * (width - filled)


def _build_report(
    brand: str,
    industry: str,
    overall_score: int,
    model_results: dict,
    best_query: str,
    worst_query: str,
    memory_results: Optional[dict] = None,
) -> str:
    lines = [
        f"Citation Check: {brand}",
        f"Industry: {industry}",
        "",
        f"Overall Citability Score: {overall_score}/100",
        "",
        "Methodology: search-grounded API models approximate the consumer AI",
        "surfaces (ChatGPT, Gemini, Claude, Perplexity all search the web).",
        "Results can differ from the consumer apps, which layer their own",
        "retrieval and personalization on top.",
        "",
        "Model Breakdown:",
    ]

    # Find longest label for alignment
    max_label_len = max(len(m["label"]) for m in model_results.values()) if model_results else 10

    for model_id, info in model_results.items():
        label = info["label"]
        n = info["queries_tested"]
        m = info["mentioned_in"]
        bar = _progress_bar(m / n if n else 0)
        padding = " " * (max_label_len - len(label))
        lines.append(f"  {label}:{padding}  mentioned in {m}/{n} queries  [{bar}]")

    # Memory probe section (surface vs training-data presence)
    if memory_results:
        lines.append("")
        lines.append("Memory Probe (no web access -- training-data presence):")
        mem_label_len = max(len(m["label"]) for m in memory_results.values())
        for model_id, info in memory_results.items():
            label = info["label"]
            n = info["queries_tested"]
            m = info["mentioned_in"]
            bar = _progress_bar(m / n if n else 0)
            padding = " " * (mem_label_len - len(label))
            lines.append(f"  {label}:{padding}  mentioned in {m}/{n} queries  [{bar}]")

    lines.append("")
    if best_query:
        lines.append(f'Best performing query: "{best_query}"')
    if worst_query:
        lines.append(f'Worst performing query: "{worst_query}"')

    # Recommendations
    lines.append("")
    lines.append("Recommendations:")
    recs = _generate_recommendations(overall_score, model_results, best_query, worst_query, memory_results)
    for i, rec in enumerate(recs, 1):
        lines.append(f"  {i}. {rec}")

    return "\n".join(lines)


def _generate_recommendations(
    overall_score: int,
    model_results: dict,
    best_query: str,
    worst_query: str,
    memory_results: Optional[dict] = None,
) -> list[str]:
    recs = []

    # Check if direct brand queries work vs. generic industry queries
    direct_mention = False
    generic_mention = False
    for info in model_results.values():
        for detail in info["details"]:
            if detail.get("error"):
                continue
            q_lower = detail["query"].lower()
            if "tell me about" in q_lower and detail["mentioned"]:
                direct_mention = True
            elif detail["mentioned"]:
                generic_mention = True

    if direct_mention and not generic_mention:
        recs.append("Brand not appearing in general industry queries. Need more web presence and topical authority.")
        recs.append("Direct brand queries working. The foundation exists.")
        recs.append("Focus on getting cited in industry comparison and roundup content.")
    elif not direct_mention and not generic_mention:
        recs.append("Brand not appearing in any AI responses. Significant content and authority gap.")
        recs.append("Publish expert content targeting the queries AI models pull from.")
        recs.append("Build structured data (schema markup) on the website so models can parse it.")
    elif generic_mention and direct_mention:
        recs.append("Brand appearing in both direct and industry queries. Solid baseline.")
        recs.append("Push for recommendation-level language in third-party content and reviews.")
        recs.append("Monitor citation quality monthly to track improvements.")
    else:
        recs.append("Brand showing up in some industry queries but not direct lookups. Add a strong About/bio page.")
        recs.append("Ensure consistent NAP (name, address, phone) and structured data across the web.")

    if overall_score < 30:
        recs.append("Score is low. Prioritize AEO content strategy before competitors claim these queries.")
    elif overall_score < 60:
        recs.append("Score is moderate. Consistent publishing and backlink building will move the needle.")

    # Surface vs memory gap diagnosis (when the memory probe was run)
    if memory_results:
        surface_mentions = sum(m["mentioned_in"] for m in model_results.values())
        memory_mentions = sum(m["mentioned_in"] for m in memory_results.values())
        if surface_mentions > 0 and memory_mentions == 0:
            recs.append(
                "Live web retrieval surfaces the brand, but it's absent from model memory. "
                "Retrieval visibility is rented; durable presence needs sustained off-site "
                "mentions (Reddit, reviews, press) that future training runs absorb."
            )
        elif memory_mentions > 0 and surface_mentions == 0:
            recs.append(
                "Models know the brand from training data, but live search doesn't retrieve "
                "it. That's a content/citability problem on the site -- fixable in months, "
                "not years. Prioritize extractable answer content for the losing queries."
            )

    # Retrieval recon callout — surface when citability is weak
    if overall_score < 60:
        recs.append(
            "NEXT STEP: Run /retrieval-recon for your industry to see what URLs are actually "
            "winning AI retrieval. These citation checks show the model's opinion — retrieval "
            "recon shows what Perplexity's search system actually fetches at query time. "
            "Use that data to build a content plan targeting the gaps."
        )
    elif not generic_mention:
        recs.append(
            "Consider running /retrieval-recon to see which competitors are winning retrieval "
            "for your industry queries. Your brand isn't appearing in generic searches — "
            "retrieval data will show exactly what content is beating you."
        )

    return recs


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    brand = args[0] if len(args) > 0 else "Example Brand"
    industry = args[1] if len(args) > 1 else "consulting"
    url = args[2] if len(args) > 2 else None

    result = check_citations(brand, industry, url, include_memory="--memory" in sys.argv)
    print()
    print(result["report"])
    print()
    print(f"Raw data saved to stdout. Pass to other modules or pipe to JSON.")
    # Optionally dump JSON for piping
    if "--json" in sys.argv:
        # Strip non-serializable bits and dump
        print(json.dumps(result, indent=2))
