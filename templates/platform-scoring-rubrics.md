# Platform-Specific AEO Scoring Rubrics

Each AI platform selects and cites sources differently. Score each one separately (0-100) to identify platform-specific gaps.

Source: Adapted from zubair-trabzada/geo-seo-claude platform optimizer + AEO Machine research.

---

## Google AI Overviews (AIO)

**How it selects sources:** 92% of citations come from pages already in top 10 organic. Heavily weights traditional SEO signals + structured data.

### Scoring Rubric (0-100)

| Factor | Points | Criteria |
|--------|--------|----------|
| Top 10 organic ranking | 20 | Already ranking for target queries |
| Schema markup | 15 | Organization, FAQ, HowTo JSON-LD present |
| Content structure | 15 | Direct answer in first paragraph, question-based H2s |
| Page experience | 10 | Core Web Vitals passing (LCP < 2.5s) |
| HTTPS + mobile | 5 | Secure, responsive |
| Featured snippet format | 10 | Content formatted for snippet extraction (lists, tables, definitions) |
| Freshness signals | 10 | Updated within 6 months, dateModified in schema |
| E-E-A-T signals | 10 | Author bios, credentials, cited sources |
| Internal linking | 5 | Topic cluster structure, hub pages |

### Priority Actions
1. If not in top 10 organic, fix traditional SEO first (AIO pulls from organic)
2. Add FAQ schema to every key page
3. Structure content with direct-answer first paragraphs
4. Ensure dateModified is current in schema

---

## ChatGPT (Web Search)

**How it selects sources:** Entity recognition-heavy. Wikipedia = 47.9% of citations. Reddit = 11.3%. Prefers authoritative, well-structured pages. Only 11% overlap with Google AIO citations.

### Scoring Rubric (0-100)

| Factor | Points | Criteria |
|--------|--------|----------|
| Wikipedia/Wikidata presence | 20 | Has a Wikipedia page or Wikidata entry |
| Entity clarity | 15 | Brand name is unambiguous, Organization schema has sameAs links |
| Content self-containment | 15 | Passages extractable without context (134-167 words optimal) |
| GPTBot access | 10 | Not blocked in robots.txt |
| OAI-SearchBot access | 5 | Specifically allowed (search-only, no training) |
| llms.txt present | 5 | Structured summary for AI consumption |
| Authoritative backlinks | 10 | Links from .edu, .gov, Wikipedia, major publications |
| Reddit mentions | 10 | Positive mentions in relevant subreddits |
| Content freshness | 5 | Recently published or updated content |
| Structured data | 5 | JSON-LD schemas with sameAs, url, description |

### Priority Actions
1. If no Wikipedia page, start with Wikidata entry
2. Ensure GPTBot + OAI-SearchBot are allowed in robots.txt
3. Add sameAs links in Organization schema (Wikipedia, LinkedIn, Crunchbase URLs)
4. Build Reddit presence in 2-3 relevant subreddits

---

## Perplexity AI

**How it selects sources:** Reddit = 46.7% of citations. Prioritizes recent, discussion-based content. Aggressive crawler (PerplexityBot).

### Scoring Rubric (0-100)

| Factor | Points | Criteria |
|--------|--------|----------|
| Reddit presence | 25 | Brand mentioned positively in relevant subreddits |
| PerplexityBot access | 10 | Not blocked in robots.txt |
| Content recency | 15 | Published/updated within 90 days |
| Discussion-style content | 10 | Comparisons, "X vs Y", community-oriented |
| Direct answer format | 10 | Question headings with concise answers |
| Statistical density | 10 | Specific numbers, percentages, data points |
| Forum/community presence | 10 | Active in industry forums, Q&A sites |
| Source attribution | 5 | Content cites its own sources (builds trust chain) |
| Technical accessibility | 5 | Fast load, clean HTML, no heavy JS rendering |

### Priority Actions
1. Reddit is 46.7% of Perplexity citations. This is your #1 lever.
2. Allow PerplexityBot in robots.txt
3. Create comparison content ("X vs Y", "best X for Y")
4. Keep content fresh (update dates, add new data quarterly)

---

## Google Gemini

**How it selects sources:** Pulls from Google's index + Knowledge Graph. Similar to AIO but with more weight on entity relationships and Knowledge Panel data.

### Scoring Rubric (0-100)

| Factor | Points | Criteria |
|--------|--------|----------|
| Google Knowledge Panel | 20 | Brand has a Knowledge Panel |
| Google Business Profile | 10 | Complete, verified GBP (if applicable) |
| Schema markup | 15 | Organization with sameAs, FAQ, Service schemas |
| Google-Extended access | 10 | Not blocked in robots.txt |
| YouTube presence | 15 | Active channel (Gemini heavily references YouTube) |
| Organic authority | 10 | Strong organic rankings for target terms |
| Structured content | 10 | Tables, lists, clear headings |
| Review signals | 5 | Google Reviews, third-party review sites |
| Site speed | 5 | Core Web Vitals passing |

### Priority Actions
1. Claim/optimize Google Business Profile
2. Allow Google-Extended in robots.txt
3. YouTube is tightly integrated with Gemini. Videos rank here.
4. Add comprehensive Organization schema with sameAs links

---

## Bing Copilot

**How it selects sources:** Bing index + Microsoft ecosystem. Bing Webmaster Tools verification matters. Less studied but growing.

### Scoring Rubric (0-100)

| Factor | Points | Criteria |
|--------|--------|----------|
| Bing Webmaster Tools | 15 | Site verified and submitted |
| Bing organic rankings | 15 | Ranking for target queries in Bing |
| Schema markup | 15 | Standard JSON-LD schemas present |
| LinkedIn presence | 15 | Active company page (Microsoft owns LinkedIn) |
| Content structure | 10 | Clear headings, direct answers, lists |
| HTTPS + accessibility | 5 | Secure, fast, accessible |
| Bing Places | 10 | Listed (if local business) |
| Content freshness | 10 | Updated within 6 months |
| GitHub presence | 5 | For tech companies (Microsoft owns GitHub) |

### Priority Actions
1. Verify site in Bing Webmaster Tools (most people skip this)
2. LinkedIn matters more here than on other platforms (Microsoft ecosystem)
3. Claim Bing Places listing if you're a local business
4. Submit sitemap to Bing specifically

---

## Cross-Platform Summary

### Universal Actions (help everywhere)
- Schema markup (Organization, FAQ, Service)
- Clean heading hierarchy with question-format H2s
- Content in 134-167 word extractable blocks
- Fast, accessible, HTTPS site
- Allow all AI crawlers in robots.txt

### Platform-Specific Priority Matrix

| If you want to rank on... | Focus on... |
|---------------------------|-------------|
| Google AIO | Traditional SEO + structured data |
| ChatGPT | Wikipedia + entity clarity + Reddit |
| Perplexity | Reddit (46.7%!) + recency + discussion content |
| Gemini | Google ecosystem (GBP, YouTube, Knowledge Panel) |
| Bing Copilot | Bing Webmaster Tools + LinkedIn + Bing Places |

### Key Stat: Only 11% of domains are cited by both ChatGPT and Google AIO for the same query. Optimizing for one doesn't automatically cover the other.
