# Ross Mobile Tire & Roadside: Marketing Roadmap

**Date:** 2026-06-11
**Site:** rossmobiletireandroadside.com (Wix)
**Market:** 24/7 mobile tire repair + roadside assistance, metro Atlanta

---

## Where Ross stands today

**AEO/SEO composite: 40/100 (Grade D)** across 8 dimensions, with off-site authority measured.

The shape of the score matters more than the number:

| Strong | Weak |
|---|---|
| AI crawler access 95/100 | Answer content (FAQ) 0/100 |
| llms.txt 90/100 | Off-site authority 2/100 |
| Citability structure 79/100 | AI mentions 11/100 (1 of 5 queries per engine) |
| | Freshness signals 30/100, schema 38/100 |

**The surprise from the competitor pass:** Ross already leads on-site. Head-to-head scores: Ross 55, 3030 Roadside 44, Atlanta Roadside Assistance 44, I&I Tires 43. Nobody in this market has built real answer content. The on-site bar is low.

**The real gap is off-site.** 3030 Roadside: ~483 Google reviews at 4.6. I&I: 138 at 3.5. Ross: ~42 at 4.9. Ross has the best rating and a tenth of the leader's volume. No YouTube, no Facebook, no Nextdoor, no LinkedIn, no Reddit presence. Directory listings exist but are unclaimed, with wrong categories and an inconsistent phone number.

**The structural defect:** the site shows two different phone numbers. Directories use (404) 649-0976; the site header pushes (404) 540-8429. Every signal Ross sends is split in half.

## The three levers, in order

### 1. Reviews + Google Business Profile (cost: time only)
For "near me" emergency queries, GBP and review volume outweigh everything on the website. The full fix list and SMS review-ask system: `gbp-review-playbook.md`. Target 15+ reviews/month; every completed job gets the same text within the hour.

### 2. A call-first site (built, ready to review)
Redesigned homepage plus two ad landing pages: dark, fast (under 30KB vs 572KB today), one orange call beacon, answer-first copy, FAQ + schema + freshness baked in, one canonical phone number. Files in `redesign/`, decisions in `redesign/design-notes.md`.

### 3. Emergency-intent Google Ads (needs budget + account)
Calls are the conversion. Two campaigns (Emergency Now 24/7, Scheduled + Fleet), per-service ad groups, insurance-program negatives to stop the biggest budget leak. Market CPCs run $12-22 for emergency roadside in metro markets; realistic floor budget $1,500-2,500/month. Full plan: `ads/google-search-campaign-2026-06-11.md`, importable build: `ads/google-ads-import-2026-06-11.csv`.

## 30 / 60 / 90

**Days 1-30 (foundation, mostly free):**
- GBP: access, categories, services, photos, Q&A seeding, one canonical phone everywhere
- Review SMS system live on every completed job
- Publish redesigned site (or port its content/schema into Wix if staying)
- Claim and correct the 8 directory listings

**Days 31-60 (visibility):**
- Launch Campaign 1 (Emergency Now) once landing pages and call tracking are live
- Facebook + Nextdoor pages up; first 5 YouTube job clips
- Weekly GBP posts from real jobs
- Watch search terms weekly; prune and add negatives

**Days 61-90 (compound):**
- Review count should pass ~75-90; respond to all, recover any sour ones
- Launch Campaign 2 (Scheduled + Fleet) if Campaign 1 cost-per-call holds under ~$150
- Service-area pages for confirmed dispatch suburbs (template ready to clone)
- Re-run the AEO audit; expect FAQ/freshness/schema dimensions to jump, AI mentions to follow reviews

## Blocked on Ross / Max

1. GBP manager access (gates lever 1)
2. Which number rings dispatch 24/7, and what (404) 540-8429 actually is
3. Real dispatch radius (gates geo targeting + service-area pages)
4. Ads budget + Google Ads account access (gates lever 3)
5. Real job photos for the site and GBP (phone shots are fine)
6. Hosting decision: static hosting for the new site vs staying on Wix

## Deliverables index

| File | What it is |
|---|---|
| `MARKETING-ROADMAP.md` | This document |
| `audit/aeo-audit-report.md` | Full 8-dimension audit, 40/100, with off-site addendum |
| `audit/competitor-comparison.md` | Head-to-head vs 3 Atlanta rivals |
| `audit/citability-report.md` | Passage-level extraction analysis |
| `local-seo-notes.md` | NAP/GBP/citations findings the scorer does not cover |
| `gbp-review-playbook.md` | GBP fix list, review SMS engine, citation cleanup, off-site ladder |
| `redesign/index.html` | New homepage, verified desktop + mobile |
| `redesign/landing-mobile-tire-repair.html` | Ad landing page, tire repair intent |
| `redesign/landing-flat-tire.html` | Ad landing page, flat tire intent |
| `redesign/design-notes.md` | Design system, AEO fixes, open items before publish |
| `ads/google-search-campaign-2026-06-11.md` | Keyword research, campaign structure, RSA copy, negatives, bidding |
| `ads/google-ads-import-2026-06-11.csv` | Ads Editor import: 34 keywords + 6 RSAs, validated lengths |
| `content/robots-recommended.txt` | Three-tier AI crawler robots.txt |
| `schemas/` | Generated JSON-LD starters from the audit |
| `ads/call-tracking-wiring-packet-2026-07-11.md` | Call tracking unblocked: shared Twilio account live (AES directory pilot), one number-buy away from ads launch readiness |
