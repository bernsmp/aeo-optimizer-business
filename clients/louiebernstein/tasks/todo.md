# CMS Sync Fix and Slack Integration — Execution Plan (for Louie Bernstein)

Overview
Fix CMS ↔ site content parity, then complete the Slack bot for natural-language website editing. Keep changes minimal and isolated. No creds in code; use env files. After each phase, run, verify, and only then request a Git commit.

Phases (you review before I start execution)
1) Fix CMS Sync (Phase 1)
- Seed defaults via authenticated script (no manual admin flow)
- Correct mergeSettings() so CMS data prevails when present; use defaults only when truly empty
- Verify CMS state and that site reflects CMS within ISR window

2) Complete Slack Bot Integration (Phase 2)
- Parsing: expand patterns, add LLM-based parser, better errors
- Slack server: post responses back to Slack, confirmation flow with buttons, thread handling
- CMS client: robust auth, token cache/refresh, error handling/retries
- Webhooks: trigger Vercel deploy after CMS writes; notify Slack

3) Create Slack App & Deploy Bot (Phase 3)
- Set up Slack app, scopes, env; deploy on Railway; wire endpoints

4) Test & Refine (Phase 4)
- Exercise simple/complex edit scenarios, ambiguous parsing, error paths; update docs

Scope and Key Files
- clients/louiebernstein/website/lib/payload.ts (merge logic)
- clients/louiebernstein/website/scripts/seed-defaults.ts (auth seeding)
- VoiceCraft/integrations/cms_integration.py (parser + CMS client auth)
- VoiceCraft/integrations/slack_bot_server.py (Slack posting, confirm flow, interactive handling)
- VoiceCraft/integrations/slack_bot.py (message formatting/utilities if present)
- VoiceCraft/integrations/SLACK-CMS-SETUP.md (docs)

Assumptions to Validate
- Lines referenced in your brief exist or are nearby; if not, I’ll adapt with minimal diff
- ISR cache invalidation or revalidate path exists for ~60s propagation

Tasks (todo)
- [x] Phase 1: Seed script
  - [x] Add API key/JWT auth to scripts/seed-defaults.ts (non-interactive)
  - [x] Seed all default content; idempotent and safe for re-run
- [x] Phase 1: Merge logic
  - [x] Update mergeSettings() to prefer CMS when present; treat undefined/missing as empty, not falsy zero/false
  - [ ] Unit or inline tests for representative fields (deferred; manual tested OK)
  - [ ] Manual verify in /admin and on-site after ISR (you to verify once deployed)
- [x] Phase 2: Parsing
  - [x] Enhance _extract_value() patterns (add : and = variants)
  - [x] Implement _parse_with_llm() using Claude Opus 4.5; fallback to patterns
  - [x] Improve user-facing errors with field suggestions
- [x] Phase 2: Slack bot server
  - [x] Use Slack WebClient to post in channel/DM (no prints)
  - [x] Thread replies correctly
  - [x] Add preview + Confirm/Cancel buttons; handle in handle_interactive()
  - [x] Add retries/backoff for transient failures (3 retries, exponential)
- [x] Phase 2: CMS client
  - [x] Harden login(): error surfacing, token cache/refresh (6-day expiry)
  - [x] Add _request_with_retry() with exponential backoff
- [x] Phase 2: Deploy webhook
  - [x] Add deploy_webhook.py module (trigger Vercel, notify Slack)
  - [x] Add /webhooks/cms-update endpoint to slack_bot_server
- [ ] Phase 3: Slack app + Railway
  - [ ] Create app, scopes, install; set SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET
  - [ ] Deploy on Railway; set start cmd and health endpoint
  - [ ] Set Event Subscriptions + optional /site slash command
- [ ] Phase 4: Tests & docs
  - [ ] Run scenario tests (simple/complex/errors)
  - [ ] Update SLACK-CMS-SETUP.md with Railway + env vars

Success Criteria
- [ ] All CMS content editable in /admin
- [ ] Site reflects CMS within ~60s; no defaults overriding real data
- [ ] Bot replies in Slack, previews changes, applies only on confirm
- [ ] Railway deployment healthy; Slack events verified

Risk Mitigations
- Keep diffs localized; feature-flag risky behavior where feasible
- Add dry-run/preview for CMS mutations; log all operations (no secrets)
- Retries with jitter for Slack/Payload network flakiness

Environment Variables (no secrets in code)
- SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET
- LOUIE_SITE_URL, LOUIE_ADMIN_EMAIL, LOUIE_ADMIN_PASSWORD
- ANTHROPIC_API_KEY
- (Optional) PAYLOAD_API_URL, PAYLOAD_API_KEY, VERCEL_DEPLOY_HOOK_URL

Review

## Phase 1 Summary
- **Seed script**: website/scripts/seed-defaults.ts now authenticates (JWT or API key) and POSTs defaults to /api/globals/site-settings. Idempotent.
- **Merge logic**: website/lib/payload.ts uses presence-based merge; CMS wins even for empty strings/arrays/false.
- **Dependencies**: Added dotenv, @types/node to website/package.json.
- **Env vars**: PAYLOAD_URL, LOUIE_ADMIN_EMAIL, LOUIE_ADMIN_PASSWORD in .env.local; optional PAYLOAD_API_KEY.

## Phase 2 Summary
- **LLM parsing** (VoiceCraft/integrations/cms_integration.py): _parse_with_llm() uses Claude Opus 4.5 for ambiguous commands; pattern matching for simple edits; better error messages with field suggestions.
- **Slack posting** (VoiceCraft/integrations/slack_bot_server.py): Uses Slack WebClient to post responses; threads replies; preview mode with Confirm/Cancel buttons via handle_interactive().
- **Auth hardening** (VoiceCraft/integrations/cms_integration.py): Token cache/refresh (6-day expiry), _request_with_retry() with exponential backoff (3 retries, 0.5s base).
- **Deploy webhooks** (VoiceCraft/integrations/deploy_webhook.py + slack_bot_server.py): trigger_deploy_and_notify() for Vercel; /webhooks/cms-update endpoint; notify Slack (🚀 started → ✅ success).
- **AITable adapter** (VoiceCraft/integrations/cms_aitable_adapter.py): Scaffolded; feature-flag via USE_AITABLE_CMS=true.
- **Dependencies**: Already present (anthropic, slack-sdk in requirements.txt).
- **Env vars**: ANTHROPIC_API_KEY (LLM parsing), VERCEL_DEPLOY_HOOK_URL, SLACK_DEPLOY_CHANNEL (optional).

## Known Limitations / Future Improvements
- **Array operations**: LLM parsing supports add/remove testimonials or FAQs but needs field mapping extension for nested arrays.
- **Confirmation state**: In-memory dict for pending_confirmations; production should use Redis or DB.
- **Token expiry**: Hardcoded 6-day expiry; Payload JWT spec varies; could parse JWT exp claim.
- **AITable adapter**: _find_record_id() stub returns None (always creates); implement query by filter or local cache.
- **Payload webhook**: Code provided in deploy_webhook.py docstring; requires manual Payload config edit (afterChange hook).
