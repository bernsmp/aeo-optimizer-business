# AEO Analysis Report: Modern Nose Clinic

**Site:** https://www.modernnoseclinic.com
**Analysis Date:** February 16, 2026
**Industry:** Healthcare / ENT / Otolaryngology (Multi-Location Medical Practice)
**Platform:** Webflow

---

## Overall AEO Score: 38/100

---

## Breakdown by Category

### 1. Technical Foundation: 50/100
**What's Working:**
- SSL/HTTPS enabled
- Webflow hosting (solid infrastructure, fast CDN)
- Google Tag Manager implemented (GTM-MTVLHJ4)
- Matomo analytics for privacy-compliant tracking
- Mobile-responsive design
- XML sitemap declared in robots.txt
- LocalBusiness schema present for 2 locations (Tualatin, Salem)
- MedicalClinic schema with specialties, contact info, and provider data
- AggregateRating schema present (5/5, 3 reviews)

**Gaps:**
- No llms.txt file (404)
- robots.txt is bare minimum (`User-agent: * / Disallow:`) — no AI crawler directives
- Schema markup has **incomplete opening hours** (placeholder text, not actual times)
- Bellevue location **missing from schema** entirely
- No BreadcrumbList schema for navigation
- AggregateRating shows only 3 reviews — too thin for credibility
- Multiple Google Fonts loaded (5 font families) — potential performance drag
- TikTok Universal Pixel adds tracking overhead

### 2. Content Structure: 35/100
**What's Working:**
- Clear service segmentation (Sinus, Allergy, Sleep/Snoring, Ears)
- Symptom-focused messaging that matches patient search intent
- Quiz funnels for Sinus, Allergy, and Snoring (interactive engagement)
- Patient testimonials page with 25+ stories
- Blog exists with relevant health content
- Video library with categorized content
- CareCredit financing option displayed

**Gaps:**
- Only 5 blog posts visible — extremely thin content library
- Blog posts have **no dates or author attribution** (E-E-A-T failure)
- No FAQ schema on any page despite having FAQ-style content on Sinusoft page
- Service pages lack comprehensive educational depth
- No "condition vs. treatment" comparison content
- No procedure preparation/recovery guides as standalone content
- Provider bios lack depth — no education, residency, board certifications, publications
- No patient outcome data or statistics pages
- Missing "what to expect" content for each procedure

### 3. AI Crawler Access: 20/100
**What's Working:**
- Site is fully crawlable (no blocks in robots.txt)
- Sitemap declared

**Gaps:**
- **No llms.txt file** — AI systems have zero guidance on what this practice does
- **No explicit AI crawler directives** in robots.txt (GPTBot, Claude-Web, PerplexityBot, etc.)
- No structured content specifically formatted for AI consumption
- No sitemap optimization distinguishing service pages from navigation pages
- No `.well-known` directory for AI discovery protocols

### 4. Schema Markup: 45/100
**What's Working:**
- MedicalClinic schema with provider names and specialties
- LocalBusiness schema for 2 of 3 locations
- Organization-level social media links (Facebook, YouTube, Instagram)
- AggregateRating schema present
- Contact information in schema (phone, fax)

**Gaps:**
- **No MedicalProcedure schema** for Sinusoft, Balloon Sinuplasty, Otosoft, Dream Bite
- **No FAQPage schema** despite FAQ content on Sinusoft page
- **No Physician schema** with proper credentials (medicalSpecialty, education, board certs)
- **No MedicalCondition schema** linking conditions to treatments
- **Bellevue WA location entirely missing** from schema
- Opening hours schema contains **placeholder/incomplete text** (not actual hours)
- AggregateRating has only 3 reviews — needs 25+ from testimonials page
- No VideoObject schema for video library content
- No Article schema on blog posts
- No HowTo schema for procedure preparation content
- No Review schema for individual testimonials

### 5. Content Quality for AI Citation: 30/100
**What's Working:**
- Branded proprietary procedures (Sinusoft, Otosoft, Dream Bite System)
- Specific success statistics ("96% of patients report drastic improvement")
- Recovery time claims ("less than 48 hours")
- Center of Excellence designation by Entellus Medical
- Real patient testimonials with specific procedure outcomes
- Multi-location presence (Oregon + Washington)

**Gaps:**
- **No original research or outcome data** published
- **No clinical citations or study references** supporting procedure claims
- Provider bios lack educational credentials, fellowship training, publications
- No comparison content (e.g., "Sinusoft vs Traditional Sinus Surgery")
- No "best ENT in [city]" positioning content
- No condition-specific educational deep-dives
- Blog posts lack author bylines from physicians (E-E-A-T critical for YMYL)
- No press mentions, media appearances, or external authority signals
- No community/civic involvement content for local authority

---

## AI Recommendation Likelihood

### Current State
When someone asks ChatGPT/Perplexity/Claude:
> "What's the best ENT clinic in Portland Oregon?"
> "What is balloon sinuplasty and where can I get it in Oregon?"
> "Best sinus doctor near Tualatin OR"

**Modern Nose Clinic's chance of being mentioned: LOW-MODERATE**

**Why:**
- Schema exists but is incomplete — AI can parse some structured data
- No third-party citations or authoritative external mentions found
- Blog content is too thin to establish topical authority
- Provider credentials not structured for AI extraction
- Local competitor content likely more robust

### YMYL Factor (Your Money Your Life)

**Critical:** Healthcare is the highest-stakes YMYL category. Google and AI systems apply **maximum scrutiny** to medical content:
- Author credentials MUST be visible and structured
- Claims MUST cite medical evidence
- E-E-A-T signals are non-negotiable for ranking
- AI systems heavily weight institutional authority for health recommendations

### Competitor Advantage Check
Local ENT competitors in Portland/Salem/Bellevue likely have:
- More robust Google Business Profiles with hundreds of reviews
- Healthgrades, Zocdoc, Vitals, and WebMD profiles with external authority
- Hospital/health system affiliations with domain authority
- More extensive blog/educational content
- RealSelf or similar platform presence for procedures

---

## Top 5 Priority Fixes

### 1. Fix & Expand Schema Markup (Impact: HIGH)
```
Priority: CRITICAL
Effort: Low-Medium
Impact: Immediate improvement in rich results + AI parsing
```
- Fix opening hours placeholder data in LocalBusiness schema
- Add Bellevue location to schema
- Add MedicalProcedure schema for Sinusoft, Balloon Sinuplasty, Otosoft, Dream Bite
- Add Physician schema with credentials for Dr. Skarada and all providers
- Add FAQPage schema to Sinusoft page (FAQ already exists in content)
- Update AggregateRating to reflect actual review volume (25+ testimonials)

### 2. Create llms.txt + Optimize robots.txt (Impact: HIGH)
```
Priority: CRITICAL
Effort: Low
Impact: Direct AI system guidance + crawler access
```
- Create llms.txt defining practice, specialties, locations, providers, procedures
- Add explicit AI crawler directives to robots.txt
- Ensure GPTBot, Claude-Web, PerplexityBot, Google-Extended, Applebot are allowed

### 3. Build Physician Authority Content (Impact: HIGH)
```
Priority: HIGH
Effort: Medium
Impact: E-E-A-T compliance for YMYL healthcare content
```
- Expand Dr. Skarada's bio: education, residency, board certifications, publications, affiliations
- Add author bylines to ALL blog posts and service pages
- Create "Our Approach" thought leadership content from Dr. Skarada
- Add clinical outcome data where available

### 4. Expand Blog + Educational Content Library (Impact: HIGH)
```
Priority: HIGH
Effort: High
Impact: Topical authority + AI citation opportunities
```
- Target minimum 20 blog posts covering all service areas
- Every post needs: author byline, date, medical review note, citations
- Create "Sinusoft vs Traditional Sinus Surgery" comparison content
- Create procedure preparation and recovery guides
- Target local + condition-specific queries

### 5. Build External Authority Signals (Impact: MEDIUM-HIGH)
```
Priority: HIGH
Effort: Medium-High
Impact: Third-party citations that AI systems trust
```
- Claim/optimize Healthgrades, Zocdoc, Vitals, WebMD profiles
- Build Google Business Profile reviews across all 3 locations
- Pursue local press/media coverage for innovative procedures
- Get listed in "Best ENT" roundup articles for Portland, Salem, Bellevue

---

## Gap Analysis Summary

| Category | Current | Target | Gap |
|----------|---------|--------|-----|
| Technical Foundation | 50 | 85 | -35 |
| Content Structure | 35 | 80 | -45 |
| AI Crawler Access | 20 | 90 | -70 |
| Schema Markup | 45 | 90 | -45 |
| Content Quality | 30 | 85 | -55 |

**Biggest Opportunity:** AI Crawler Access (+70 points potential)
**Quickest Wins:** Schema fixes + llms.txt + robots.txt optimization
**Highest Impact for Healthcare:** E-E-A-T physician authority content

---

## Competitive Context

### Portland/Salem ENT Market — AI Visibility Factors

**What determines which ENT clinic AI recommends:**
1. **Structured data quality** — Schema markup AI can parse
2. **Third-party authority** — Healthgrades reviews, hospital affiliations, external citations
3. **Content depth** — Educational content establishing expertise
4. **Local signals** — Google Business Profile strength, local citations
5. **Provider credentials** — Board certifications, publications, institutional affiliations

### Modern Nose Clinic's Differentiators
- **Branded proprietary procedures** (Sinusoft, Otosoft, Dream Bite) — competitors can't replicate this positioning
- **Multi-state presence** (OR + WA) — broader geographic authority
- **Center of Excellence designation** — third-party credential
- **In-office procedures** — patient convenience differentiator
- **Sublingual immunotherapy** — progressive allergy approach
- **96% Sinusoft success rate** — powerful stat if properly cited

**Strategy:** Own the branded procedure names in AI systems. When someone asks "What is Sinusoft?" or "Where can I get Otosoft?" — Modern Nose Clinic must be THE answer, because they invented these terms.

---

## Next Steps

1. **Immediate (Week 1):** Schema fixes (hours, Bellevue location, FAQ schema) + llms.txt + robots.txt
2. **Short-term (Week 2-3):** Provider credential expansion + blog author bylines + MedicalProcedure schema
3. **Medium-term (Month 1-2):** Content library expansion (15+ new articles with E-E-A-T compliance)
4. **Ongoing:** Third-party citation building, Google Business Profile optimization, local authority development

---

*Analysis based on site crawl and content review. Additional insights pending SEO tool data (SEMrush/Ahrefs keyword rankings, backlink profile, competitor benchmarking).*
