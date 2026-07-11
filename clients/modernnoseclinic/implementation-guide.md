# AEO Implementation Guide: Modern Nose Clinic

This guide provides step-by-step instructions for implementing all AEO optimizations on modernnoseclinic.com (Webflow).

---

## Phase 1: Quick Wins (Week 1)

### 1.1 Create & Upload llms.txt

**File Location:** Root directory (`/llms.txt`)

**Webflow Steps:**
1. Webflow doesn't natively support root-level text files
2. **Option A (Recommended):** Use Webflow's custom code hosting or a worker/proxy to serve the file at `modernnoseclinic.com/llms.txt`
3. **Option B:** Host via DNS-level redirect or edge function (Cloudflare, etc.)
4. **Option C:** Add as a static page in Webflow with plain text content type

**llms.txt Content:**

```
# Modern Nose Clinic
## About
Modern Nose Clinic is a multi-location Ear, Nose & Throat (ENT) medical practice specializing in advanced sinus care, allergy treatment, sleep and snoring solutions, and ear pressure relief. The practice serves patients across Oregon and Washington with three clinic locations.

## Specialties
- Otolaryngology (Ear, Nose & Throat)
- Allergy and Immunology
- Sleep Medicine
- Sinus Surgery and Procedures
- Eustachian Tube Treatment

## Proprietary Procedures
- Sinusoft: Minimally-invasive, in-office sinus procedure using balloon technology. No cutting, no bone removal, no narcotics. 96% patient satisfaction. Recovery under 48 hours.
- Otosoft: In-office Eustachian tube treatment for chronic ear pressure, pain, and fullness. Reopens the Eustachian tube to restore natural pressure equalization.
- Dream Bite System: Oral appliance treatment for snoring and sleep apnea. Non-CPAP alternative.
- SMART CARE for Allergy: Sublingual immunotherapy (allergy drops) providing long-term allergy relief without shots.

## Medical Team
- Douglas J. Skarada, MD — Board-certified Otolaryngologist, Practice Founder
- Eric T. Waterman, MD — Otolaryngologist
- Nahmjee Lee-Skarada, DMD — Dental Sleep Medicine
- Breanne Cannon, PA-C
- Jenny Hume, PA-C
- Johnnie Machado, PA-C
- Stephanie Warye, PA-C

## Locations
- Tualatin/Portland, OR: 19150 SW 90th Ave, Tualatin, OR 97062
- Salem, OR: 340 Vista Ave SE, Suite 100, Salem, OR 97302
- Bellevue, WA: 12402 SE 38th Street, Suite 201, Bellevue, WA 98006

## Contact
- Phone: (800) 587-1373
- Text: 503-683-8391
- Fax: (503) 584-1330
- Hours: Monday-Friday, 8:00 AM - 5:00 PM
- Telehealth: Available via Doxy.me
- Appointments: https://www.modernnoseclinic.com/request-an-appointment

## Certifications
- Center of Excellence designation by Entellus Medical

## Conditions Treated
- Chronic sinusitis and sinus infections
- Nasal congestion and breathing difficulties
- Environmental and food allergies
- Snoring and obstructive sleep apnea
- Chronic ear pressure, pain, and fullness
- Deviated septum
- Nasal polyps
- Asthma (allergy-related)

## Key Pages
- Homepage: https://www.modernnoseclinic.com/
- Sinusoft Procedure: https://www.modernnoseclinic.com/sinus/sinusoft
- Balloon Sinuplasty: https://www.modernnoseclinic.com/sinus/balloon-sinuplasty
- Allergy Care: https://www.modernnoseclinic.com/allergy-overview
- Allergy Drops (SMART CARE): https://www.modernnoseclinic.com/smart-care-allergy-treatment
- Sleep & Snoring: https://www.modernnoseclinic.com/sleep-snoring/sleep-and-snoring
- Otosoft: https://www.modernnoseclinic.com/otosoft-the-in-office-solution-for-chronic-ear-pressure
- Our Practice: https://www.modernnoseclinic.com/our-practice/our-practice
- Testimonials: https://www.modernnoseclinic.com/testimonials
- Blog: https://www.modernnoseclinic.com/practice-blog
```

### 1.2 Optimize robots.txt

**Webflow Steps:**
1. Go to **Project Settings > SEO > Custom Code** or use Webflow's robots.txt editor
2. Replace current minimal robots.txt with:

```
User-agent: *
Allow: /
Disallow: /cart
Disallow: /checkout
Disallow: /account
Disallow: /search
Disallow: /*?*

# AI Crawlers - Explicitly Allowed
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: Applebot
Allow: /

User-agent: Bytespider
Allow: /

Sitemap: https://www.modernnoseclinic.com/sitemap.xml
```

### 1.3 Fix Opening Hours in Existing Schema

**Location:** Webflow custom code (site-wide or page-level)

The current LocalBusiness schema has incomplete/placeholder opening hours. Replace with:

```json
"openingHoursSpecification": [
  {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "08:00",
    "closes": "17:00"
  }
]
```

Apply this fix to both Tualatin and Salem LocalBusiness schema blocks.

### 1.4 Add Bellevue Location to Schema

Add a third LocalBusiness schema entry:

```json
{
  "@context": "https://schema.org",
  "@type": "MedicalClinic",
  "name": "Modern Nose Clinic - Bellevue",
  "image": "https://cdn.prod.website-files.com/61e04229ccd2b12ca3cd12dd/61e04229ccd2b1d1a7cd137f_MN_logo_new-min.png",
  "telephone": "(800) 587-1373",
  "url": "https://www.modernnoseclinic.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "12402 SE 38th Street, Suite 201",
    "addressLocality": "Bellevue",
    "addressRegion": "WA",
    "postalCode": "98006",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 47.5659,
    "longitude": -122.1637
  },
  "medicalSpecialty": ["Otolaryngology", "Allergy and Immunology", "Sleep Medicine"],
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "08:00",
      "closes": "17:00"
    }
  ]
}
```

---

## Phase 2: Schema Expansion (Week 1-2)

### 2.1 Add MedicalProcedure Schema — Sinusoft Page

**Location:** Custom code on `/sinus/sinusoft` page

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MedicalProcedure",
  "name": "Sinusoft Procedure",
  "alternateName": "Sinusoft Balloon Sinuplasty",
  "description": "Sinusoft is a minimally-invasive, in-office sinus procedure that uses a small balloon to carefully open blocked sinus pathways, restoring normal drainage and airflow. No cutting, no bone removal, no general anesthesia required. Recovery time under 48 hours.",
  "procedureType": "https://schema.org/NoninvasiveProcedure",
  "bodyLocation": "Sinuses",
  "preparation": "In-office consultation and evaluation. No special preparation required for most patients.",
  "howPerformed": "A small balloon is inserted into the blocked sinus passage and gently inflated to open the pathway. Performed under local anesthesia in the office in under one hour.",
  "followup": "Most patients return to normal activities within 1-2 days.",
  "status": "https://schema.org/ActiveActionStatus",
  "outcome": "96% of patients report drastic improvement in sinusitis symptoms",
  "medicalSpecialty": "Otolaryngology",
  "recognizingAuthority": {
    "@type": "Organization",
    "name": "Entellus Medical"
  }
}
</script>
```

### 2.2 Add FAQPage Schema — Sinusoft Page

The Sinusoft page already has FAQ content. Add schema to match:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is Sinusoft successful?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Absolutely. 96% of patients undergoing a Sinusoft procedure have reported a drastic improvement in sinusitis symptoms."
      }
    },
    {
      "@type": "Question",
      "name": "What is the average recovery time for Sinusoft?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "While recovery time varies with each patient, most patients who undergo the in-office procedure can return to normal activities within two days or sooner."
      }
    },
    {
      "@type": "Question",
      "name": "What is the Sinusoft procedure?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sinusoft is a minimally-invasive, in-office sinus procedure that uses a small balloon to carefully open blocked sinus pathways, restoring normal drainage and airflow. It requires no cutting, no bone removal, and no general anesthesia."
      }
    },
    {
      "@type": "Question",
      "name": "Is Sinusoft covered by insurance?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Many insurance plans cover balloon sinuplasty procedures like Sinusoft. Contact Modern Nose Clinic at (800) 587-1373 to verify your coverage."
      }
    },
    {
      "@type": "Question",
      "name": "How is Sinusoft different from traditional sinus surgery?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Unlike traditional sinus surgery, Sinusoft requires no cutting or bone removal, is performed in-office under local anesthesia (no hospital visit), uses no narcotics for recovery, and has a recovery time of 1-2 days instead of weeks."
      }
    }
  ]
}
</script>
```

### 2.3 Add Physician Schema

**Location:** Global site code or "Our Practice" page

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Physician",
  "name": "Dr. Douglas J. Skarada",
  "honorificPrefix": "Dr.",
  "givenName": "Douglas",
  "familyName": "Skarada",
  "honorificSuffix": "MD",
  "medicalSpecialty": "Otolaryngology",
  "description": "Board-certified Otolaryngologist and founder of Modern Nose Clinic. Specializes in minimally-invasive sinus procedures, allergy treatment, and sleep medicine across Oregon and Washington.",
  "worksFor": {
    "@type": "MedicalClinic",
    "name": "Modern Nose Clinic",
    "url": "https://www.modernnoseclinic.com"
  },
  "url": "https://www.modernnoseclinic.com/our-practice/dr-douglas-j-skarada-md",
  "telephone": "(800) 587-1373",
  "areaServed": [
    {"@type": "City", "name": "Tualatin", "containedInPlace": {"@type": "State", "name": "Oregon"}},
    {"@type": "City", "name": "Salem", "containedInPlace": {"@type": "State", "name": "Oregon"}},
    {"@type": "City", "name": "Bellevue", "containedInPlace": {"@type": "State", "name": "Washington"}}
  ]
}
</script>
```

**Note:** Expand this schema with `alumniOf`, `hasCredential`, `memberOf` once credentials are gathered from the practice.

### 2.4 Add MedicalProcedure Schema — Other Procedures

Repeat the MedicalProcedure pattern for:

| Procedure | Page | Key Details |
|-----------|------|-------------|
| Otosoft | `/otosoft-the-in-office-solution-for-chronic-ear-pressure` | Eustachian tube dilation, in-office, ear pressure relief |
| Balloon Sinuplasty | `/sinus/balloon-sinuplasty` | In-office, balloon dilation, chronic sinusitis |
| Dream Bite System | `/dream-bite` | Oral appliance, snoring/sleep apnea, non-CPAP |
| SMART CARE for Allergy | `/smart-care-allergy-treatment` | Sublingual immunotherapy, no shots, daily drops |

---

## Phase 3: Content E-E-A-T Fixes (Week 2-3)

### 3.1 Add Author Bylines to All Blog Posts

Every blog post must include:

```html
<div class="article-author">
  <img src="[dr-skarada-headshot.jpg]" alt="Dr. Douglas J. Skarada, MD" />
  <div>
    <p class="author-name">Written by Dr. Douglas J. Skarada, MD</p>
    <p class="author-credentials">Board-Certified Otolaryngologist | Founder, Modern Nose Clinic</p>
    <p class="review-date">Medically reviewed: [Date]</p>
  </div>
</div>
```

Add corresponding Article schema:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MedicalWebPage",
  "headline": "[Article Title]",
  "author": {
    "@type": "Physician",
    "name": "Dr. Douglas J. Skarada, MD",
    "medicalSpecialty": "Otolaryngology"
  },
  "reviewedBy": {
    "@type": "Physician",
    "name": "Dr. Douglas J. Skarada, MD"
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "publisher": {
    "@type": "MedicalClinic",
    "name": "Modern Nose Clinic",
    "url": "https://www.modernnoseclinic.com"
  },
  "about": {
    "@type": "MedicalCondition",
    "name": "[Condition Name]"
  }
}
</script>
```

### 3.2 Expand Provider Bio Pages

For each provider, the bio page should include:
- [ ] Full name with credentials
- [ ] Medical school / dental school
- [ ] Residency and fellowship training
- [ ] Board certifications (with certifying body)
- [ ] Professional memberships (AAO-HNS, etc.)
- [ ] Years of experience
- [ ] Areas of clinical focus
- [ ] Publications or research (if any)
- [ ] Professional headshot
- [ ] Personal bio element (builds trust)

### 3.3 Add Publication Dates to Blog Posts

- [ ] Add visible publish date to every blog post
- [ ] Add "Last medically reviewed" date
- [ ] Include dates in Article schema `datePublished` / `dateModified`

---

## Phase 4: Local SEO Enhancement (Week 3-4)

### 4.1 Google Business Profile Optimization

For each of the 3 locations:
- [ ] Claim/verify Google Business Profile
- [ ] Complete ALL profile fields (services, attributes, hours, photos)
- [ ] Add procedure-specific services (Sinusoft, Otosoft, etc.)
- [ ] Upload 20+ photos per location (exterior, interior, staff, equipment)
- [ ] Enable messaging and appointment booking
- [ ] Post weekly updates (Google Posts)
- [ ] Respond to all reviews within 24 hours

### 4.2 Healthcare Directory Profiles

Claim and optimize profiles on:
- [ ] Healthgrades (critical for healthcare)
- [ ] Zocdoc (patient booking + reviews)
- [ ] Vitals
- [ ] WebMD Physician Directory
- [ ] RealSelf (for procedure profiles)
- [ ] Castle Connolly / U.S. News (if eligible)
- [ ] Oregon Medical Board public listing
- [ ] Washington Medical Commission listing

### 4.3 Local Citation Building

Ensure NAP (Name, Address, Phone) consistency across:
- [ ] Yelp
- [ ] Yellow Pages
- [ ] Better Business Bureau
- [ ] Local chamber of commerce (Tualatin, Salem, Bellevue)
- [ ] Portland Business Journal / Salem Statesman Journal directories

---

## Phase 5: Core Web Vitals Fixes (Week 2-3)

**Current Status (Feb 16, 2026 — CrUX field data, last 28 days):**

| Metric | Mobile Homepage | Mobile Sitewide | Desktop Homepage | Desktop Sitewide |
|--------|-----------------|-----------------|------------------|------------------|
| **Assessment** | **FAILING** | PASSING | PASSING | PASSING |
| LCP | 2.2s (borderline) | 1.6s | 1.1s | 0.9s |
| INP | 98ms (good) | 87ms | 44ms | 42ms |
| **CLS** | **0.14 (FAILING)** | 0.1 (borderline) | 0.07 | 0.05 |
| FCP | 1.3s | 1.2s | 0.8s | 0.6s |
| TTFB | 0.8s (borderline) | 0.9s | 0.5s | 0.3s |

**The single failing metric is CLS (Cumulative Layout Shift) on the mobile homepage at 0.14** (threshold: 0.1). Only 63% of mobile users get a "good" CLS experience, and 14% get "poor." Elements are visibly jumping around as the page loads on phones.

### 5.1 Fix Image Dimensions (Impact: HIGH — Primary CLS Fix)

**Problem:** Homepage images (service icons, procedural photos, Entellus badge, star ratings, CareCredit button) likely lack explicit `width` and `height` attributes, causing the browser to reflow content when images load.

**Webflow Fix:**
1. Go to **Designer > Homepage**
2. Select each `<img>` element on the page
3. In **Element Settings**, ensure both width and height are set (not just CSS max-width)
4. For responsive images, use CSS `aspect-ratio` on the image container:

```css
/* Add to homepage image containers */
.service-icon-wrapper {
  aspect-ratio: 1 / 1;  /* adjust to actual ratio */
  overflow: hidden;
}

.hero-image-wrapper {
  aspect-ratio: 16 / 9;  /* adjust to actual ratio */
  overflow: hidden;
}

.carecredit-button img {
  width: 280px;
  height: 100px;
}
```

5. For the CareCredit external embed (280x100), add explicit dimensions:
```html
<img src="carecredit-button.png" width="280" height="100" alt="Apply for CareCredit" loading="lazy">
```

### 5.2 Stabilize Swiper Carousel (Impact: HIGH)

**Problem:** The testimonial/hero Swiper carousel initializes via JavaScript, causing the container to jump from 0px to its rendered height.

**Webflow Fix:**
1. Select the Swiper/carousel container element
2. Set a `min-height` that matches the rendered content height on mobile:

```css
/* Mobile testimonial carousel — adjust value to match actual rendered height */
@media (max-width: 767px) {
  .testimonial-slider,
  .swiper-container {
    min-height: 320px;  /* measure actual height and adjust */
  }
}

/* Tablet */
@media (max-width: 991px) {
  .testimonial-slider,
  .swiper-container {
    min-height: 280px;
  }
}
```

3. Alternatively, use `contain: layout` on the carousel wrapper to prevent it from affecting surrounding layout during initialization.

### 5.3 Defer Third-Party Widget Injection (Impact: MEDIUM)

**Problem:** Klara chat widget and Tolstoy engagement widget load asynchronously and inject floating elements that shift page content.

**Fix Options:**

**Option A (Recommended): Lazy-load widgets on user interaction**
```html
<script>
  // Only load Klara after user scrolls or interacts
  let widgetLoaded = false;
  function loadKlara() {
    if (widgetLoaded) return;
    widgetLoaded = true;
    // Insert original Klara script here
  }
  window.addEventListener('scroll', loadKlara, { once: true });
  window.addEventListener('click', loadKlara, { once: true });
</script>
```

**Option B: Reserve space for widget elements**
```css
/* Reserve space for Klara chat bubble — prevents shift when it appears */
.klara-chat-widget,
[class*="klara"] {
  position: fixed !important;  /* fixed elements don't cause CLS */
  bottom: 20px;
  right: 20px;
}
```

### 5.4 Reduce Font Families (Impact: MEDIUM)

**Problem:** 5 Google Font families loading (Open Sans, Ubuntu, Montserrat, PT Sans, Lato). Font swaps cause text reflow when custom fonts replace system fallbacks.

**Fix:**
1. Audit which fonts are actually used across the site — consolidate to **2 maximum** (one heading, one body)
2. Preload the critical fonts:
```html
<!-- Add to site-wide <head> code -->
<link rel="preload" href="https://fonts.gstatic.com/s/[primary-font]/[hash].woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="https://fonts.gstatic.com/s/[secondary-font]/[hash].woff2" as="font" type="font/woff2" crossorigin>
```
3. Add `font-display: swap` with size-adjusted fallbacks to minimize reflow:
```css
@font-face {
  font-family: 'Primary Font';
  font-display: swap;
  size-adjust: 105%;  /* tune to match system font metrics */
}
```

### 5.5 Preload LCP Image (Impact: MEDIUM — Improves LCP)

**Problem:** Mobile LCP is 2.2s (borderline, threshold is 2.5s). Preloading the hero/above-fold image can shave 200-500ms.

**Fix:**
```html
<!-- Add to homepage <head> code — use the actual hero image URL -->
<link rel="preload" as="image" href="https://cdn.prod.website-files.com/[hero-image-path].avif"
      fetchpriority="high">
```

In Webflow: Add to **Page Settings > Custom Code > Head Code** for the homepage.

### 5.6 Defer Non-Critical Third-Party Scripts (Impact: LOW — Improves TTFB/TBT)

**Problem:** TikTok Universal Pixel and analytics scripts load synchronously, competing with content for bandwidth.

**Fix:**
1. Move TikTok pixel to load after `DOMContentLoaded`:
```html
<script>
  window.addEventListener('DOMContentLoaded', function() {
    // TikTok pixel code here
  });
</script>
```
2. Ensure Matomo script has `defer` attribute
3. Keep Google Tag Manager as-is (it manages its own loading)

### CWV Success Criteria

After fixes, target these field data numbers (next 28-day CrUX cycle):

| Metric | Current (Mobile HP) | Target | Threshold |
|--------|---------------------|--------|-----------|
| CLS | 0.14 (FAIL) | < 0.08 | 0.10 |
| LCP | 2.2s (borderline) | < 2.0s | 2.5s |
| INP | 98ms (good) | Maintain | 200ms |
| FCP | 1.3s (good) | Maintain | 1.8s |
| TTFB | 0.8s (borderline) | < 0.7s | 0.8s |

**Note:** CrUX field data updates on a 28-day rolling window. After deploying fixes, allow 4-6 weeks for the data to fully reflect improvements. Use Chrome DevTools Lighthouse for immediate lab verification.

---

## Phase 6: Technical Verification

### 6.1 Test All Schema

Use these tools to verify implementation:

1. **Google Rich Results Test:** https://search.google.com/test/rich-results
2. **Schema Markup Validator:** https://validator.schema.org/
3. **Google Search Console:** Check for schema errors/warnings

### 6.2 Test AI Crawler Access

Verify robots.txt:
1. Visit: `https://www.modernnoseclinic.com/robots.txt`
2. Confirm AI crawlers have explicit Allow directives

Verify llms.txt:
1. Visit: `https://www.modernnoseclinic.com/llms.txt`
2. Confirm file is accessible and returns 200

### 6.3 Test Core Web Vitals Post-Fix

1. **Lab test (immediate):** Run Lighthouse in Chrome DevTools on mobile for homepage
   - CLS should be < 0.1
   - LCP should be < 2.5s
2. **Field test (4-6 weeks):** Re-check PageSpeed Insights for updated CrUX data
   - Verify mobile homepage assessment changes from FAIL to PASS
3. **Google Search Console:** Check Core Web Vitals report for any remaining "Poor" URLs

### 6.4 Test AI Visibility (Baseline)

Run these queries across ChatGPT, Claude, Perplexity, and Google AI Overview:
- "Best ENT clinic in Portland Oregon"
- "What is Sinusoft sinus procedure"
- "Balloon sinuplasty Portland Oregon"
- "Best allergy doctor near Tualatin OR"
- "Snoring treatment Salem Oregon"
- "Otosoft ear procedure"

Document which queries mention Modern Nose Clinic (baseline for tracking improvement).

---

## Implementation Checklist

### Week 1
- [ ] Create and upload llms.txt
- [ ] Optimize robots.txt with AI crawler directives
- [ ] Fix opening hours in existing LocalBusiness schema
- [ ] Add Bellevue location to schema
- [ ] Add MedicalProcedure schema to Sinusoft page
- [ ] Add FAQPage schema to Sinusoft page

### Week 2
- [ ] Add Physician schema for Dr. Skarada
- [ ] Add MedicalProcedure schema to remaining procedure pages
- [ ] Add author bylines to all existing blog posts
- [ ] Add Article/MedicalWebPage schema to blog posts
- [ ] Add publication dates to all blog content
- [ ] **CWV: Add explicit dimensions to all homepage images**
- [ ] **CWV: Set min-height on Swiper/testimonial carousel for mobile**
- [ ] **CWV: Preload hero/LCP image on homepage**

### Week 3
- [ ] Expand all provider bio pages with credentials
- [ ] Claim/optimize Google Business Profiles (all 3 locations)
- [ ] Begin healthcare directory profile claims
- [ ] Test all schema with Google Rich Results Test
- [ ] **CWV: Defer Klara/Tolstoy widget loading (lazy-load on interaction)**
- [ ] **CWV: Consolidate Google Fonts to 2 families max + preload**
- [ ] **CWV: Defer TikTok pixel to DOMContentLoaded**
- [ ] **CWV: Run Lighthouse mobile audit to verify CLS < 0.1**

### Week 4
- [ ] Complete healthcare directory profiles
- [ ] Local citation audit and NAP consistency check
- [ ] Run baseline AI visibility tests
- [ ] Begin content strategy implementation (separate document)

### Week 6-8 (CWV Verification)
- [ ] **CWV: Check PageSpeed Insights for updated CrUX field data**
- [ ] **CWV: Verify mobile homepage assessment changed from FAIL to PASS**
- [ ] **CWV: Check Google Search Console Core Web Vitals report**

---

## Webflow-Specific Notes

### Adding Schema in Webflow
1. **Site-wide schema:** Project Settings > Custom Code > Head Code
2. **Page-specific schema:** Page Settings > Custom Code > Head Code
3. **Collection-based schema:** Use Webflow CMS dynamic fields in custom code blocks

### Webflow Limitations
- No native robots.txt editor (use custom hosting rules or Webflow Enterprise)
- Static files (llms.txt) require workaround (page with plain text or external hosting)
- CMS blog posts can use dynamic fields for schema automation
- Custom code blocks in Webflow have a character limit per block

### Recommended Webflow Apps/Integrations
1. **Finsweet Attributes** — Enhanced CMS functionality
2. **Schema App** — Automated schema generation
3. **Webflow Logic** — Form automation for appointment requests

---

*Implementation guide prepared for Modern Nose Clinic. Contact for support with Webflow-specific schema deployment.*
