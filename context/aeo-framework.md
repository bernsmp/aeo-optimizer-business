# AEO Framework Methodology

AI Engine Optimization (AEO) is the practice of structuring a business's online presence so AI systems (ChatGPT, Perplexity, Gemini, Claude, Google AI Mode) can find, understand, and recommend it.

Last major revision: 2026-06-11 (June 2026 research update. See Research Basis at the bottom.)

## Three Layers

### Layer 1: Technical Foundation

The baseline. This is hygiene, not magic: it makes the site parseable and provably fresh, and it keeps the doors open. It no longer carries the engagement by itself (see Research Basis).

- **Schema markup**: Organization (with `sameAs` links to profiles), Service, FAQ, HowTo, Event. JSON-LD format. Frame: entity disambiguation, telling AI systems exactly who you are. Not a citation driver.
- **AI crawler access (three tiers)**: robots.txt must allow the SEARCH-tier bots (OAI-SearchBot, Claude-SearchBot, PerplexityBot, Bingbot) and USER-tier fetchers (ChatGPT-User, Claude-User, Perplexity-User). TRAINING-tier bots (GPTBot, ClaudeBot, Google-Extended) are a client business decision; allowing them builds long-term model memory.
- **CDN/edge check**: Cloudflare default-blocks unverified AI crawlers and runs Pay-Per-Crawl. A robots.txt "Allow" means nothing if the CDN blocks the bot. Every audit must check edge-level access (the crawler now does this automatically).
- **Freshness signals**: machine-readable dates (`dateModified`/`datePublished` in schema, article meta tags). Roughly 65% of AI bot hits target content under 12 months old. Substantive updates only; date-stamp gaming doesn't work.
- **Content structure**: Clear H1/H2/H3 hierarchy. One topic per page. Answer-first: key facts in the first 30% of the page (where 44.2% of LLM citations come from). Definitive statements AI can extract.
- **Q&A content**: Dedicated FAQ pages with real customer questions. Note: Google removed FAQ rich results (May 2026), so the pitch is AI answer extraction, not rich snippets. FAQPage schema stays for entity clarity.
- **llms.txt**: a 10-minute hedge, weighted accordingly. Google explicitly does not use it. OpenAI has never confirmed it. Anthropic and Perplexity reportedly honor it in retrieval. Ship it, but never sell it as a driver.
- **Long-tail question content** and **comparison pages**: pages targeting the specific questions people ask AI, structured so differentiators are extractable.

### Layer 2: Visibility Strategy

THE growth lever as of 2026. Off-site brand mentions correlate 0.664 with AI citation rate, roughly 3x stronger than backlinks (Ahrefs, 75K brands). Wikipedia plus Reddit alone drive 25%+ of ChatGPT citations.

- **Reddit engagement**: Authentic participation where customers ask questions. Top-cited domain on Perplexity, top-2 on ChatGPT. Volatile (source shares can swing 6x in weeks), so monitor rather than set-and-forget.
- **YouTube**: Strongest single-platform correlation with AI citation (0.737). Answer-format videos with transcripts.
- **Review platforms**: G2/Capterra/Trustpilot/industry reviews give roughly a 3x citation multiplier.
- **Digital PR for unlinked mentions**: Press coverage, guest articles, podcasts. The mention is the asset; the link is a bonus.
- **Wikipedia/Wikidata**: highest-leverage single source where legitimately earned. Start with Wikidata.
- **Per-platform strategy**: only about 11% of cited domains overlap between ChatGPT and Perplexity. One strategy can't win every surface, so pick target platforms per client (see templates/platform-scoring-rubrics.md).
- **Continuous monitoring**: citation sources are volatile. This is the structural argument for monthly retainers over one-time audits.

### Layer 3: Brand Strategy

The strategic layer that makes AI recommendations stick.

- **Brand positioning audit**: How the business is currently perceived vs. how it should be positioned for AI discovery.
- **Entity consistency**: same name, description, and facts everywhere AI looks.
- **Story framework**: A clear narrative AI can retell. Origin story, mission, unique methodology.
- **Content strategy**: Editorial calendar aligned with the questions AI users actually ask. Original data, statistics, and named expert quotes earn citations.
- **Differentiation**: What makes this business the obvious answer when AI is asked "Who is the best X?"

---

## AEO Scoring Rubric

Total score: 100 points. Rebalanced 2026-06-11.

| Category | Weight | What It Measures |
|----------|--------|------------------|
| Citability & Structure | 20% | How easily AI extracts answers: question headings, answer-first layout, clean hierarchy |
| AI Mentions | 15% | Current visibility in search-grounded AI responses (citation checker) |
| Off-Site Authority | 15% | Brand presence on YouTube, Reddit, Wikipedia, LinkedIn, reviews/directories (brand authority scorer) |
| Schema & Structured Data | 15% | JSON-LD coverage and breadth. Entity hygiene, merged from the old two schema dimensions |
| Answer Content (FAQ) | 10% | Real customer questions answered in depth; schema is secondary to content |
| AI Crawler Access | 10% | Three-tier robots.txt config plus edge/CDN block detection |
| Freshness Signals | 10% | Machine-readable dates, recency of latest content |
| llms.txt | 5% | Present and well-formed. Scored as a hedge |

**Unmeasured dimensions** (citation check not run, brand authority not assessed) are excluded and the remaining weights renormalized. Never scored as 0.

### Score Ranges

- **80-100**: Strong AEO presence. AI models likely recommend this business.
- **60-79**: Decent foundation. Key gaps to fill for consistent AI visibility.
- **40-59**: Partial coverage. Missing critical elements that AI models need.
- **20-39**: Weak. AI models probably skip this business or give incomplete info.
- **0-19**: No AEO presence. Invisible to AI recommendation engines.

---

## Research Basis (June 2026)

Why the rubric looks like this. The receipts behind the weights:

1. **Schema demoted (40% to 15%)**: Ahrefs (May 2026) tracked 1,885 pages adding JSON-LD vs 4,000 controls. AI citations barely moved on any platform. Google's official AI guide (May 15, 2026): AI Overviews/AI Mode use the same index and signals as organic search, no special AI markup. Schema's remaining value is entity disambiguation.
2. **Off-site raised (10% to 30% combined)**: Ahrefs 75K-brand study found brand mentions correlate 0.664 with AI citation rate (about 3x backlinks). 5W Research (May 2026): Wikipedia (13.15%) plus Reddit (11.97%) account for 25%+ of US ChatGPT citations; no other domain above 3%.
3. **FAQ rich results killed**: Google removed them May 7, 2026 (Search Console support sunsetting June-Aug 2026). Q&A content still matters for AI extraction; the rich-snippet pitch is dead.
4. **llms.txt cut (10% to 5%)**: Google explicitly doesn't read it. A Semrush controlled study found no correlation. Only Anthropic/Perplexity reportedly honor it.
5. **Crawler access raised, edge check added**: three-tier bot fleet (search/user/training). Cloudflare default-blocks unverified AI crawlers and runs Pay-Per-Crawl. Silent CDN-level blocking is a common failure mode robots.txt can't reveal.
6. **Freshness added**: about 65% of AI bot hits target content under 12 months old (Seer Interactive, 5,000+ URLs).
7. **Platform fragmentation**: only about 11% of cited domains overlap between ChatGPT and Perplexity. Citation source shares are volatile (Reddit's ChatGPT share once collapsed from about 60% to about 10% in two weeks). Continuous multi-engine monitoring beats one-time audits.
8. **Organic rank is the doorway to Google surfaces**: AI Overviews/AI Mode citations correlate strongly with top organic positions, so classic SEO is the entry fee for the Google side. (Not in the automated score; covered in engagement strategy.)

Stat shares above are point-in-time and volatile. Re-verify quarterly; update this file and aeo_scorer.py together.
