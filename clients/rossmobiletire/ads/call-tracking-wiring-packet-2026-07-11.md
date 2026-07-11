# Ross Ads Call-Tracking Wiring Packet (2026-07-11, draft, nothing purchased)

The June 11 marketing roadmap blocks Campaign 1 launch on "landing pages and call tracking are live." The call-tracking half is now one command away, because Max stood up a Twilio account on 2026-07-11 for the Atlanta Emergency Services directory pilot (account upgraded to Full, card on file, credentials in the Directory Sites repo `.env`).

## What exists already (shared infrastructure)

- Twilio account: Full, active. First tracked number (678) 325-5530 forwards to Ross's dispatch line (404) 649-0976 with a whisper, live on atlantaemergencyservices.com since 2026-07-11.
- Log-pull tooling: `Directory Sites/scripts/maintenance/pull_call_logs.py` writes dated receipts (call count, duration, caller area code only). Reusable for any number on the account.

## What Ross's ads need (when the ads project resumes)

1. Buy ONE more local number (~$1.15/mo) on the same account for the ad landing pages (`redesign/landing-mobile-tire-repair.html`, `redesign/landing-flat-tire.html`). Keep (404) 649-0976 as the canonical number on the organic site and GBP (NAP consistency); the tracked number appears ONLY on paid landing pages, which are noindexed, so citation consistency is not polluted.
2. Point the new number's voice URL at the same forward+whisper pattern, whisper text "Call from your Google ad" or simply no whisper (Ross's own leads; attribution matters less than answer speed).
3. Wire Google Ads call reporting: use the tracked number as the call extension / on-page number so cost-per-call is measurable against the roadmap's $150 threshold.
4. Add the number to the log-pull cadence so Max's receipts show organic-directory calls and paid calls side by side.

## Decision needed from Max (not Ross)

- Whether directory-pilot receipts and ads receipts should stay in one Twilio account (simpler, one bill) or split when/if Ross starts paying for the line (cleaner books). Recommendation: one account until money changes hands, then revisit.

## Blocked exactly where the roadmap was blocked

Ross inputs still gate the ads launch: GBP access, dispatch radius, budget, Google Ads account access, job photos, hosting decision. Nothing in this packet changes that; it just removes "call tracking" from the blocker list the day those land.
