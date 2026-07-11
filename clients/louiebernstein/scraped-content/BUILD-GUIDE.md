# Louie Bernstein Website Rebuild Guide

## Overview
Rebuild Louie Bernstein's website from http://louiebernstein.com to a modern, AEO-optimized site on Vercel.

## Current Site Analysis
- **Total Pages Scraped:** 1
- **Scraped Content Location:** `clients/louiebernstein/scraped-content/`
- **Homepage:** `homepage.json` and `homepage.md`
- **All Pages:** `organized-content.json`

## Content Structure

### Homepage Content
Located in: `scraped-content/homepage.json`

### Additional Pages
Located in: `scraped-content/organized-content.json`

## Build Requirements

### 1. Technology Stack
- **Framework:** Next.js 14+ (App Router)
- **Styling:** Tailwind CSS
- **Deployment:** Vercel
- **Type:** Static site generation (SSG) or Server Components

### 2. AEO Optimization Requirements
- ✅ Schema markup (Organization, Service, FAQPage)
- ✅ robots.txt optimized for AI crawlers
- ✅ llms.txt file
- ✅ Semantic HTML structure
- ✅ Clear heading hierarchy (H1, H2, H3)
- ✅ FAQ sections with FAQPage schema
- ✅ Fast loading (<3 seconds)
- ✅ Mobile-responsive design

### 3. Design Requirements
- Modern, professional design
- Clean, easy to navigate
- Mobile-first responsive
- Fast loading
- Accessible (WCAG 2.1 AA)

### 4. Content Pages Needed
Based on scraped content, create:
- Homepage (main landing page)
- About/Services page
- Contact page
- Any other pages found in scraped content

### 5. Key Sections (from scraped content)
Extract and organize:
- Hero section
- About section
- Services section
- Testimonials (if any)
- Contact information
- Call-to-action sections

## File Structure

```
clients/louiebernstein/
├── scraped-content/          # Original scraped content
│   ├── homepage.json
│   ├── homepage.md
│   └── organized-content.json
├── website/                  # New Next.js site (to be created)
│   ├── app/
│   │   ├── page.tsx         # Homepage
│   │   ├── about/page.tsx    # About page
│   │   ├── contact/page.tsx  # Contact page
│   │   └── layout.tsx
│   ├── components/
│   ├── public/
│   └── package.json
└── vercel.json               # Vercel config
```

## Next Steps for Claude Code

1. **Read Scraped Content:**
   - Read `scraped-content/homepage.json`
   - Read `scraped-content/organized-content.json`

2. **Create Next.js Project:**
   - Initialize Next.js 14+ with TypeScript
   - Set up Tailwind CSS
   - Create basic file structure

3. **Build Pages:**
   - Homepage with hero, about, services, contact sections
   - About page (if separate)
   - Contact page

4. **Add AEO Optimization:**
   - Add schema markup to layout.tsx
   - Create robots.txt
   - Create llms.txt
   - Optimize meta tags

5. **Style & Polish:**
   - Modern, professional design
   - Mobile-responsive
   - Fast loading

6. **Deploy:**
   - Set up Vercel project
   - Deploy and test

## Content Sources
All content is in: `clients/louiebernstein/scraped-content/`

## AEO Deliverables Already Created
- Schema markup files (Organization, Service, FAQ)
- robots.txt
- llms.txt
- Content strategy
- Competitor analysis

These are in: `clients/louiebernstein/`

## Questions for Claude Code
1. What sections should be on the homepage?
2. How should we organize the content?
3. What design style should we use?
4. Should we create separate pages or single-page site?

---
**Created:** 2025-11-22T16:28:26.048628
**Total Pages Scraped:** 1
