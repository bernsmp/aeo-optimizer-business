# June 2026 Best-Practices Update — Build Plan

Approved by Max 2026-06-11 ("make the updates and get building").
Note: `tasks/todo.md` is an existing Little Tree Gas work file — left untouched.

## Todos

- [x] 1. Verify current OpenRouter model IDs live (public /models endpoint) — 3 of 4 confirmed dead, replacements confirmed valid
- [ ] 2. `site_crawler.py` — add freshness-signal extraction + edge/CDN AI-UA block detection
- [ ] 3. `aeo_scorer.py` — rebalanced rubric (schema 40%→15% merged; off-site 5%→30% combined; freshness new; crawler access raised), unmeasured-dimension renormalization (fixes the silent ai_mentions=0 penalty), 3-tier crawler list
- [ ] 4. `citation_checker.py` — replace dead model IDs with web-grounded (`:online`) equivalents, optional memory-probe mode, surface-vs-API disclaimer
- [ ] 5. Build `competitor_analyzer.py` (claimed in CLAUDE.md, never existed)
- [ ] 6. `aeo_audit.py` — handle unmeasured dimensions, expanded bot list, updated robots-recommended template, optional --brand-data input
- [ ] 7. `context/aeo-framework.md` — new rubric, llms.txt reframe, FAQ rich-results sunset, off-site authority elevation
- [ ] 8. `CLAUDE.md` — rubric table, model IDs, competitor agent status, last-updated
- [ ] 9. `templates/robots.txt` — 3-tier crawler list + remove leftover client domain; `templates/platform-scoring-rubrics.md` — refresh stale stats (Wikipedia 47.9%→13.15% per 5W May 2026)
- [ ] 10. `brand_authority_scorer.py` — refresh stat citations + volatility note (weights unchanged)
- [ ] 11. Test: compile all modules, run scorer end-to-end on a live site, validate competitor analyzer
- [ ] 12. Review section

## Out of scope (this session)

- Key rotation in automation/.env + data_sources/.env (Max — provider dashboards; SEMrush/SiteGuru shared password too)
- Slash-command wiring as Claude Code skills
- Google Docs delivery agent

## Review (completed 2026-06-11)

All 11 todos done. Summary of changes:

**Code (data_sources/):**
- `aeo_scorer.py` rewritten: 8 rebalanced dimensions (schema 40%>15% merged, off-site 10%>30% combined, freshness + 3-tier crawler access new, llms.txt 10%>5%). Unmeasured dimensions now excluded + weights renormalized instead of scoring 0 (old behavior silently penalized every non-citation audit by 5%).
- `citation_checker.py`: 3 dead model IDs replaced with live-verified ones (`openai/gpt-5.5:online`, `google/gemini-3.5-flash:online`, `anthropic/claude-sonnet-4.6:online`, `perplexity/sonar-pro`). New `--memory` probe separates retrieval visibility from training-data presence. Methodology disclaimer added to reports.
- `site_crawler.py`: freshness-signal extraction (JSON-LD dates, meta tags, time elements, Last-Modified) + edge/CDN AI-block differential test (Cloudflare default-blocking detection, with spoofed-UA caveat).
- `competitor_analyzer.py`: BUILT (was claimed in CLAUDE.md, never existed). Side-by-side scores, gaps, quick wins, schema-type gaps. On-site-only scope disclaimer.
- `aeo_audit.py`: unmeasured-dim rendering, expanded bot summary, edge-filter warning, 3-tier robots-recommended template, `--brand-data` flag wiring brand_authority_scorer into the composite.
- `multi_page_crawler.py`: hard extruct import made graceful (JSON-LD fallback). Pre-existing crash, env never had extruct installed (PEP 668 blocks pip; venv optional later).
- `brand_authority_scorer.py`: stale stats refreshed (Wikipedia 47.9%>13.2% per 5W May 2026), volatility notes.

**Docs:** `CLAUDE.md` (rubric, status, model IDs, quarterly re-verify note), `context/aeo-framework.md` (full rewrite with Research Basis section), `templates/robots.txt` (3-tier + removed leftover client domain), `templates/platform-scoring-rubrics.md` (stats refreshed, Grok added), `templates/audit-report.md` + `templates/monthly-delta-report.md` (new dimension tables).

**Tested:** all modules compile; 6 synthetic scorer cases pass (renormalization math, edge-block cap, freshness tiers); live scorer run on louiebernstein.com (74/100); live competitor comparison; full 5-stage audit pipeline end-to-end. Citation checker model IDs verified against live OpenRouter catalog; actual completion call NOT yet executed (no OPENROUTER_API_KEY in this shell). One live `--citations` run still needed to confirm.

**New deps:** none added. **Env vars:** unchanged.
**Limitations:** off-site authority dimension needs manually collected platform data (JSON via --brand-data); extruct still not installed (fallback active); slash commands still not wired.
**NOT done (Max):** rotate keys in `automation/.env` + `data_sources/.env`, change shared SEMrush/SiteGuru password.
