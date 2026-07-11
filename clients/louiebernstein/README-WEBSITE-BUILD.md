# Louie Bernstein Website Rebuild - Ready for Claude Code! 🚀

## ✅ What's Done

### 1. Site Scraping ✅
- ✅ Scraped current site at http://louiebernstein.com
- ✅ Extracted all content (homepage)
- ✅ Organized content into structured format
- **Location:** `scraped-content/`

### 2. AEO Deliverables ✅
- ✅ Organization Schema (`schema-organization.html`)
- ✅ Service Schema (`schema-service.html`)
- ✅ FAQPage Schema (`schema-faq.html`)
- ✅ robots.txt (optimized for AI crawlers)
- ✅ llms.txt (AI instructions)
- ✅ Content Strategy (`content-strategy.md`)
- ✅ Competitor Analysis (`COMPETITOR-ANALYSIS.md`)

### 3. Build Documentation ✅
- ✅ Build Instructions (`CLAUDE-CODE-BUILD-INSTRUCTIONS.md`)
- ✅ Content Structure (`WEBSITE-CONTENT-STRUCTURE.md`)
- ✅ Build Guide (`scraped-content/BUILD-GUIDE.md`)

---

## 📁 File Structure

```
clients/louiebernstein/
├── scraped-content/              # ✅ Scraped original site
│   ├── homepage.json
│   ├── homepage.md
│   ├── all-pages.json
│   ├── organized-content.json
│   └── BUILD-GUIDE.md
│
├── website/                      # 🚧 TO BE CREATED BY CLAUDE CODE
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   ├── public/
│   │   ├── robots.txt
│   │   └── llms.txt
│   └── package.json
│
├── AEO Deliverables (Ready):
│   ├── schema-organization.html
│   ├── schema-service.html
│   ├── schema-faq.html
│   ├── robots.txt
│   ├── llms.txt
│   ├── content-strategy.md
│   └── COMPETITOR-ANALYSIS.md
│
└── Documentation:
    ├── CLAUDE-CODE-BUILD-INSTRUCTIONS.md  # ⭐ START HERE
    ├── WEBSITE-CONTENT-STRUCTURE.md
    └── README-WEBSITE-BUILD.md (this file)
```

---

## 🎯 Next Steps for Claude Code

### Step 1: Read Documentation
1. Read `CLAUDE-CODE-BUILD-INSTRUCTIONS.md` - Complete build guide
2. Read `WEBSITE-CONTENT-STRUCTURE.md` - Content breakdown
3. Read `scraped-content/homepage.json` - Original content

### Step 2: Initialize Next.js Project
```bash
cd clients/louiebernstein
npx create-next-app@latest website --typescript --tailwind --app --no-src-dir
cd website
```

### Step 3: Build Website
- Create components for each section
- Build homepage with all sections
- Add schema markup
- Copy robots.txt and llms.txt
- Style with Tailwind CSS
- Deploy to Vercel

---

## 📋 Key Files to Reference

### For Content:
- `scraped-content/homepage.json` - Original site content
- `WEBSITE-CONTENT-STRUCTURE.md` - Content breakdown
- `CLIENT-INFO.md` - Business information

### For AEO:
- `schema-organization.html` - Organization schema
- `schema-service.html` - Service schema
- `schema-faq.html` - FAQPage schema
- `robots.txt` - Robots file
- `llms.txt` - LLMs file

### For Build:
- `CLAUDE-CODE-BUILD-INSTRUCTIONS.md` - Complete instructions
- `scraped-content/BUILD-GUIDE.md` - Technical guide

---

## 🎨 Design Requirements

- **Style:** Modern, professional B2B consultant website
- **Framework:** Next.js 14+ (App Router)
- **Styling:** Tailwind CSS
- **Deployment:** Vercel
- **Mobile-First:** Responsive design
- **Fast Loading:** <3 seconds

---

## 🔍 AEO Requirements

### Must Include:
- ✅ All schema markup (Organization, Service, FAQPage)
- ✅ robots.txt in public/
- ✅ llms.txt in public/
- ✅ FAQ section with FAQPage schema
- ✅ Semantic HTML structure
- ✅ Proper heading hierarchy
- ✅ Meta tags (title, description, OpenGraph)

---

## 📝 Content Sections

### From Current Site:
1. Hero section
2. CTAs (LinkedIn, Calendly)
3. Testimonials (2)
4. Value proposition
5. Awards image
6. Contact info
7. Social links

### To Add (NEW):
8. About section
9. Services section
10. Process/How It Works section
11. FAQ section (CRITICAL for AEO!)

---

## ✅ Checklist

### Preparation (Done):
- [x] Scrape current site
- [x] Organize content
- [x] Create AEO deliverables
- [x] Write build documentation

### Build (Claude Code):
- [ ] Initialize Next.js project
- [ ] Create component structure
- [ ] Build homepage sections
- [ ] Add schema markup
- [ ] Copy robots.txt and llms.txt
- [ ] Style with Tailwind CSS
- [ ] Test responsiveness
- [ ] Deploy to Vercel
- [ ] Verify schema markup
- [ ] Test robots.txt and llms.txt

---

## 🚀 Ready to Build!

**Everything is organized and ready!** 

Claude Code should:
1. Read `CLAUDE-CODE-BUILD-INSTRUCTIONS.md` first
2. Review scraped content
3. Build the Next.js site
4. Implement all AEO optimizations
5. Deploy to Vercel

**Let's build a beautiful, modern, AEO-optimized website!** 🎉


