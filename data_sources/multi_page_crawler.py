"""
Multi-page crawler using advertools + extruct.

Crawls an entire site (via sitemap or link-following) and extracts
structured data from every page. Feeds into the single-page scorer
for aggregate site-wide AEO analysis.
"""

import json
import re
from urllib.parse import urlparse

import requests

try:
    import extruct
    from w3lib.html import get_base_url
    HAS_EXTRUCT = True
except ImportError:
    HAS_EXTRUCT = False

from site_crawler import USER_AGENT, TIMEOUT


# ---------------------------------------------------------------------------
# Structured data extraction (extruct)
# ---------------------------------------------------------------------------

def extract_all_structured_data(url: str, html: str = None) -> dict:
    """Extract all structured data types from a URL using extruct.

    Returns dict with keys: json-ld, microdata, rdfa, opengraph, microformat, dublincore
    """
    if html is None:
        try:
            resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
            resp.raise_for_status()
            html = resp.text
        except requests.RequestException as exc:
            return {"error": str(exc), "url": url}

    if not HAS_EXTRUCT:
        # Fallback: JSON-LD only via BeautifulSoup (extruct not installed).
        # Loses microdata/RDFa/opengraph breadth but keeps the primary signal.
        return _extract_jsonld_fallback(url, html)

    base_url = get_base_url(html, url)

    try:
        data = extruct.extract(
            html,
            base_url=base_url,
            syntaxes=["json-ld", "microdata", "rdfa", "opengraph", "microformat", "dublincore"],
            uniform=True,
        )
    except Exception as exc:
        return {"error": str(exc), "url": url}

    data["url"] = url
    return data


def _extract_jsonld_fallback(url: str, html: str) -> dict:
    """JSON-LD-only extraction used when extruct isn't installed."""
    from bs4 import BeautifulSoup

    schemas = []
    soup = BeautifulSoup(html, "html.parser")
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            schemas.append(json.loads(script.string or ""))
        except (json.JSONDecodeError, TypeError):
            continue

    og = []
    og_type = soup.find("meta", attrs={"property": "og:type"})
    if og_type:
        og.append({"og:type": og_type.get("content", "")})

    return {
        "url": url,
        "json-ld": schemas,
        "microdata": [],
        "rdfa": [],
        "opengraph": og,
        "microformat": [],
        "dublincore": [],
    }


def _collect_types_from_jsonld(obj, types_list: list):
    """Recursively collect @type values from JSON-LD, including @graph."""
    if isinstance(obj, list):
        for item in obj:
            _collect_types_from_jsonld(item, types_list)
        return
    if not isinstance(obj, dict):
        return

    schema_type = obj.get("@type")
    if schema_type:
        if isinstance(schema_type, list):
            types_list.extend(schema_type)
        else:
            types_list.append(schema_type)

    # Recurse into @graph
    if "@graph" in obj:
        _collect_types_from_jsonld(obj["@graph"], types_list)


def summarize_structured_data(extracted: dict) -> dict:
    """Summarize extracted structured data into AEO-relevant signals."""
    summary = {
        "url": extracted.get("url", ""),
        "json_ld_types": [],
        "microdata_types": [],
        "has_opengraph": False,
        "opengraph_type": None,
        "total_schemas": 0,
    }

    # JSON-LD (walk @graph if present)
    for item in extracted.get("json-ld", []):
        _collect_types_from_jsonld(item, summary["json_ld_types"])

    # Microdata
    for item in extracted.get("microdata", []):
        schema_type = item.get("@type", "Unknown")
        if isinstance(schema_type, list):
            summary["microdata_types"].extend(schema_type)
        else:
            summary["microdata_types"].append(schema_type)

    # OpenGraph
    og = extracted.get("opengraph", [])
    if og:
        summary["has_opengraph"] = True
        if og and isinstance(og[0], dict):
            summary["opengraph_type"] = og[0].get("og:type")

    summary["total_schemas"] = (
        len(summary["json_ld_types"])
        + len(summary["microdata_types"])
    )

    return summary


# ---------------------------------------------------------------------------
# Sitemap-based crawl
# ---------------------------------------------------------------------------

def _parse_sitemap_xml(xml_text: str) -> list[str]:
    """Extract URLs from sitemap XML (handles both sitemap and sitemap index)."""
    from bs4 import BeautifulSoup as BS

    soup = BS(xml_text, "xml")
    if not soup:
        soup = BS(xml_text, "html.parser")

    urls = []

    # Sitemap index: contains <sitemap><loc> entries
    for sitemap_tag in soup.find_all("sitemap"):
        loc = sitemap_tag.find("loc")
        if loc:
            urls.append(loc.get_text(strip=True))

    # Regular sitemap: contains <url><loc> entries
    for url_tag in soup.find_all("url"):
        loc = url_tag.find("loc")
        if loc:
            urls.append(loc.get_text(strip=True))

    return urls


def crawl_sitemap(url: str) -> list[str]:
    """Fetch sitemap and return a list of URLs.

    Uses requests (handles SSL properly) instead of urllib.
    Follows redirects. Recurses into sitemap index files.
    """
    base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

    sitemap_urls = [
        url if url.endswith(".xml") else f"{base}/sitemap.xml",
        f"{base}/sitemap_index.xml",
        f"{base}/wp-sitemap.xml",
    ]

    for sitemap_url in sitemap_urls:
        try:
            resp = requests.get(
                sitemap_url,
                headers={"User-Agent": USER_AGENT},
                timeout=15,
                allow_redirects=True,
            )
            if resp.status_code != 200:
                continue

            urls = _parse_sitemap_xml(resp.text)
            if not urls:
                continue

            # Check if these are sub-sitemaps (sitemap index)
            page_urls = []
            for u in urls:
                if u.endswith(".xml") or "sitemap" in u.lower():
                    # It's a sub-sitemap, fetch it too
                    try:
                        sub_resp = requests.get(
                            u, headers={"User-Agent": USER_AGENT},
                            timeout=15, allow_redirects=True,
                        )
                        if sub_resp.status_code == 200:
                            page_urls.extend(_parse_sitemap_xml(sub_resp.text))
                    except requests.RequestException:
                        continue
                else:
                    page_urls.append(u)

            if page_urls:
                return page_urls

        except requests.RequestException:
            continue

    return []


def crawl_site_pages(
    url: str,
    max_pages: int = 50,
    use_sitemap: bool = True,
) -> list[dict]:
    """Crawl multiple pages and extract structured data from each.

    Args:
        url: Starting URL or domain
        max_pages: Maximum pages to crawl
        use_sitemap: Try sitemap first, fall back to link discovery

    Returns:
        List of dicts, each with url + structured data summary
    """
    base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    pages_to_crawl = []

    # Try sitemap first
    if use_sitemap:
        sitemap_urls = crawl_sitemap(url)
        if sitemap_urls:
            pages_to_crawl = sitemap_urls[:max_pages]

    # Fall back to just the provided URL + homepage
    if not pages_to_crawl:
        pages_to_crawl = [url]
        if url != base and url != base + "/":
            pages_to_crawl.append(base)

    results = []
    seen = set()

    for page_url in pages_to_crawl:
        if page_url in seen:
            continue
        seen.add(page_url)

        extracted = extract_all_structured_data(page_url)
        if "error" in extracted:
            results.append({
                "url": page_url,
                "error": extracted["error"],
                "json_ld_types": [],
                "microdata_types": [],
                "has_opengraph": False,
                "total_schemas": 0,
            })
            continue

        summary = summarize_structured_data(extracted)
        results.append(summary)

    return results


# ---------------------------------------------------------------------------
# Site-wide analysis
# ---------------------------------------------------------------------------

def analyze_site(url: str, max_pages: int = 30) -> dict:
    """Run a site-wide structured data analysis.

    Returns a dict with:
        pages_crawled, pages_with_schema, schema_type_coverage,
        missing_on_pages, site_score_signals
    """
    pages = crawl_site_pages(url, max_pages=max_pages)

    total = len(pages)
    pages_with_schema = sum(1 for p in pages if p.get("total_schemas", 0) > 0)
    pages_with_errors = sum(1 for p in pages if "error" in p)

    # Aggregate schema types across all pages
    all_jsonld_types = set()
    all_microdata_types = set()
    pages_with_opengraph = 0

    for page in pages:
        all_jsonld_types.update(page.get("json_ld_types", []))
        all_microdata_types.update(page.get("microdata_types", []))
        if page.get("has_opengraph"):
            pages_with_opengraph += 1

    # Key schema types to check for
    important_types = {
        "Organization", "LocalBusiness", "FAQPage", "Service",
        "WebSite", "BreadcrumbList", "Person", "Article",
        "BlogPosting", "HowTo", "Event", "Review", "AggregateRating",
    }
    all_types = all_jsonld_types | all_microdata_types
    present = all_types & important_types
    missing = important_types - all_types

    return {
        "url": url,
        "pages_crawled": total,
        "pages_with_schema": pages_with_schema,
        "pages_with_errors": pages_with_errors,
        "schema_coverage_pct": round(pages_with_schema / max(total, 1) * 100),
        "opengraph_coverage_pct": round(pages_with_opengraph / max(total, 1) * 100),
        "json_ld_types_found": sorted(all_jsonld_types),
        "microdata_types_found": sorted(all_microdata_types),
        "important_types_present": sorted(present),
        "important_types_missing": sorted(missing),
        "pages": pages,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 20

    print(f"Analyzing {url} (up to {max_pages} pages)...")
    result = analyze_site(url, max_pages=max_pages)

    print(f"\nPages crawled: {result['pages_crawled']}")
    print(f"Pages with schema: {result['pages_with_schema']} ({result['schema_coverage_pct']}%)")
    print(f"OpenGraph coverage: {result['opengraph_coverage_pct']}%")
    print(f"\nJSON-LD types found: {', '.join(result['json_ld_types_found']) or 'None'}")
    print(f"Microdata types found: {', '.join(result['microdata_types_found']) or 'None'}")
    print(f"\nImportant types present: {', '.join(result['important_types_present']) or 'None'}")
    print(f"Important types missing: {', '.join(result['important_types_missing']) or 'None'}")

    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
