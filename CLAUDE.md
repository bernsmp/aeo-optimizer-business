# AEO Machine -- Claude Code Workspace

Answer Engine Optimization workspace: tooling to analyze and optimize sites for visibility in ChatGPT, Perplexity, Google AI Overviews, and Gemini. This is a working toolkit, not a productized offering.

Built on a three-layer framework: Technical Foundation -> Visibility Strategy -> Brand Strategy.

Modeled after the SEO Machine (github.com/TheCraigHewitt/seomachine) but focused entirely on AI search optimization.

---

## Quick Status

- **Current state:** Phase 1 engines live; slash commands not yet wired
- **Clients delivered:** 7 (louiebernstein, littletreegas, modernnoseclinic, fourgenerationsoneroof, testolite, chartstudioai, cognitivefingerprint)
- **Scoring engine:** LIVE -- rubric rebalanced 2026-06-11 against June 2026 research (see context/aeo-framework.md Research Basis)
- **Citation checker:** LIVE -- model IDs refreshed 2026-06-11 (old 3 of 4 were dead on OpenRouter); now uses search-grounded models + optional --memory probe
- **Competitor analyzer:** BUILT 2026-06-11 (data_sources/competitor_analyzer.py)
- **Crawler:** detects freshness signals + edge/CDN-level AI blocking (Cloudflare default-blocks unverified AI crawlers)
- **Last updated:** 2026-06-11

---

## Available Commands

None of these are wired up yet. This is the spec we're building toward.

### /aeo-audit {url}
Full site audit. Crawls the site, scores across 8 dimensions, runs gap analysis, generates report. Calls Schema Agent, Scoring Agent, and Content Agent.

### /gen-schemas {url}
Detects schema gaps, generates JSON-LD for Organization, FAQ, Service, HowTo, and Event types. Validates against schema.org. Calls Schema Agent.

### /write-faqs {url} {industry}
Generates 15-20 industry-specific FAQs with full answers. Optimized for AI readability and FAQ schema markup. Calls Content Agent.

### /score-site {url}
Quick 0-100 AEO score with dimension breakdown. No full crawl, just the scorecard. Calls Scoring Agent.

### /cite-check {brand}
Queries ChatGPT, Perplexity, Gemini, and Claude via OpenRouter. Checks if the brand gets mentioned in AI responses to relevant queries. Calls Citation Agent.

### /competitor {url url}
Head-to-head AEO score comparison. Shows gaps and opportunities. Calls Competitor Agent.

### /write-llms {url}
Generates llms.txt and robots.txt files optimized for AI crawler access. Calls Content Agent.

### /publish {client}
Packages all deliverables into a client-ready Google Docs report with score cards and implementation guide. Calls Delivery Agent.

---

## Directory Structure

```
aeo-machine/
  CLAUDE.md                    -- This file
  context/                     -- Shared knowledge
    aeo-framework.md           -- Methodology + scoring rubric
    industry-templates/        -- Healthcare, legal, ecommerce, local service
    schema-library/            -- Validated JSON-LD templates
    competitor-baselines/      -- Known AEO scores by vertical
  clients/                     -- One folder per client
    {client-name}/
      audit/                   -- Initial site crawl + analysis
      schemas/                 -- Generated JSON-LD files
      content/                 -- FAQs, llms.txt, robots.txt
      reports/                 -- Score cards + implementation guides
      published/               -- Final delivered packages
  data_sources/                -- Python analysis modules
    site_crawler.py
    schema_detector.py
    aeo_scorer.py
    citation_checker.py
    competitor_analyzer.py
    requirements.txt
  templates/                   -- Reusable output templates
    audit-report.md
    implementation-guide.md
    score-card.md
    schemas/                   -- JSON-LD starter templates
  examples/                    -- Reference implementations
    louiebernstein/
```

---

## Agent Definitions

Six specialized agents. Each handles a specific slice of AEO work.

### Schema Agent
Detects missing structured data on a site. Generates valid JSON-LD for Organization, FAQ, Service, HowTo, and Event schemas. Validates against schema.org specs. Knows industry-specific best practices (healthcare needs MedicalOrganization, legal needs Attorney, etc.).

Called by: `/gen-schemas`, `/aeo-audit`

### Citation Agent
Queries ChatGPT, Perplexity, Gemini, and Claude through the OpenRouter API. Asks industry-relevant questions and checks whether the brand appears in responses. Tracks mention frequency, context quality, and sentiment. Produces a citability score.

Called by: `/cite-check`

### Content Agent
Generates FAQ sets, blog outlines, and answer-formatted content. Matches the client's existing voice and tone. Structures content for maximum AI readability: clear headings, direct answers, short paragraphs. Also generates llms.txt and robots.txt files.

Called by: `/write-faqs`, `/write-llms`

### Scoring Agent
Runs the 0-100 AEO composite scorer across 8 dimensions (see Scoring Rubric below). Produces a score card with dimension breakdown, letter grade, and specific recommendations per dimension.

Called by: `/score-site`, `/aeo-audit`

### Competitor Agent
Scrapes competitor sites and runs the same scoring pipeline. Produces side-by-side comparisons highlighting gaps, advantages, and quick-win opportunities.

Called by: `/competitor`

### Delivery Agent
Packages everything into client-ready deliverables. Creates Google Docs reports, PDF score cards, and step-by-step implementation guides. Handles formatting, branding, and file organization.

Called by: `/publish`

---

## Scoring Rubric

0-100 composite score across 8 weighted dimensions. Rebalanced 2026-06-11 (full research basis in context/aeo-framework.md).

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Citability & Structure | 20% | Answer extraction: question headings, answer-first layout, clean hierarchy |
| AI Mentions | 15% | Brand appears in search-grounded ChatGPT, Gemini, Claude, Perplexity responses |
| Off-Site Authority | 15% | YouTube, Reddit, Wikipedia, LinkedIn, reviews/directories (brand_authority_scorer) |
| Schema & Structured Data | 15% | JSON-LD coverage + breadth. Entity hygiene, not a citation driver (Ahrefs May 2026) |
| Answer Content (FAQ) | 10% | Question depth and answer quality; schema markup secondary (FAQ rich results died May 2026) |
| AI Crawler Access | 10% | Three-tier robots.txt (search/user/training bots) + edge/CDN block detection |
| Freshness Signals | 10% | Machine-readable dates; ~65% of AI bot hits target content under 12 months old |
| llms.txt | 5% | Present and well-formed. A hedge: Anthropic/Perplexity honor it, Google ignores it |

Dimensions that aren't measured in a given run (no --citations, no brand data) are excluded and weights renormalized, never scored as 0.

**Grading scale:**
- 90-100: A (Excellent, AI-optimized)
- 75-89: B (Strong foundation, minor gaps)
- 60-74: C (Decent, significant improvement possible)
- 40-59: D (Weak, major gaps across multiple dimensions)
- 0-39: F (Not optimized for AI search at all)

---

## Client Workflow

Step-by-step for running a new client engagement.

1. Create client folder: `clients/{name}/`
2. Run `/aeo-audit {url}` -- generates full analysis across all 8 dimensions
3. Review score card and gap analysis
4. Run `/gen-schemas {url}` -- creates all missing schema markup
5. Run `/write-faqs {url} {industry}` -- generates 15-20 FAQs with answers
6. Run `/write-llms {url}` -- generates llms.txt and robots.txt
7. Run `/publish {client}` -- packages everything into deliverable format
8. Deliver to client via Google Docs link

---

## API Setup

**OpenRouter** provides access to ChatGPT, Gemini, Perplexity, and Claude through a single API endpoint. Used by the Citation Agent for brand mention checks.

- Pull API key from 1Password: `op read "op://Private/OpenRouter API Key/credential"`
- Store in `data_sources/.env` as `OPENROUTER_API_KEY`
- Endpoint: `https://openrouter.ai/api/v1/chat/completions`
- Surface models (search-grounded, verified live 2026-06-11): `openai/gpt-5.5:online`, `google/gemini-3.5-flash:online`, `anthropic/claude-sonnet-4.6:online`, `perplexity/sonar-pro`
- Memory-probe models (ungrounded, via `--memory`): same models without the `:online` suffix
- Model IDs rot. Re-verify against `https://openrouter.ai/api/v1/models` quarterly; 3 of 4 had silently died between late 2025 and June 2026.

---

## Three-Layer Framework

### Layer 1: Technical Foundation
Schema markup (Organization, FAQ, Service, HowTo, Event). robots.txt configured for AI crawlers (three tiers) plus CDN-level access check. llms.txt file. Content restructured for AI readability. Q&A content. Freshness signals.

This is what the tooling automates. Most sites need this first.

### Layer 2: Visibility Strategy
YouTube presence and optimization. Reddit strategy. PR mentions and unlinked brand citations. Review platforms. Content distribution across platforms that AI models train on and reference. The biggest lever as of 2026.

### Layer 3: Brand Strategy
Brand positioning and differentiation. Entity consistency. Story framework development. Thought leadership content strategy. Building the kind of brand authority that makes AI models cite a site by default.

---

## Existing Clients

| Client | Status | Notes |
|--------|--------|-------|
| louiebernstein | Most complete | Full website redesign + AEO implementation |
| littletreegas | Delivered | AEO audit + schemas + implementation guide |
| modernnoseclinic | Delivered | AEO score analysis (38/100) + content strategy |
| fourgenerationsoneroof | Delivered | Full AEO package + implementation guide |
| testolite | Delivered | AEO audit + full report |
| chartstudioai | In progress | Content roadmap |
| cognitivefingerprint | In progress | Content strategy development |

Client folders live in `clients/{name}/`. Each contains audit data, generated schemas, content, reports, and published deliverables.

---

## Build Notes

- Python modules go in `data_sources/`. Keep them modular: one file per concern.
- Templates go in `templates/`. Reusable across all clients.
- Industry-specific knowledge goes in `context/industry-templates/`.
- Schema examples go in `context/schema-library/`.
- When adding a new scoring dimension or changing weights, update both this file and `context/aeo-framework.md`.
- Existing schema templates already live in `templates/` (faq-schema.html, comprehensive-schema.html, etc.). Use those as starting points.
- AEO research has a shelf life of months, not years. Quarterly: re-verify model IDs (OpenRouter catalog), AI crawler user-agents, and the citation-share stats in `templates/platform-scoring-rubrics.md` and `brand_authority_scorer.py`. The June 2026 sweep found 3 dead model IDs, a dead rich-results feature, and a 3.6x-stale Wikipedia citation share.
