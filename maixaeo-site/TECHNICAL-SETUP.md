# Technical Setup Guide for maixAEO.com

## ✅ What's Been Built (Technical Foundation)

### Layer 1: Technical AEO Foundation - COMPLETE

#### 1. Schema Markup ✅
- **Organization Schema** (`src/schema/organization.json`)
  - Company info, founder, services
  - Ready for AI crawlers
  
- **Person Schema** (`src/schema/person.json`)
  - Max's profile, expertise
  - Linked to organization
  
- **Service Schema** (`src/schema/service.json`)
  - Three service packages
  - Offer catalog structure
  
- **FAQ Schema** (dynamically generated)
  - Generated from FAQ section HTML
  - Schema-friendly markup

#### 2. AI Crawler Optimization ✅
- **robots.txt** (`public/robots.txt`)
  - Allows: GPTBot, ChatGPT-User, CCBot, PerplexityBot, anthropic-ai, Claude-Web, Google-Extended
  - Sitemap reference
  
- **llms.txt** (`public/llms.txt`)
  - Structured information for AI crawlers
  - Framework explanation
  - Key statistics
  - Services overview

#### 3. Content Structure ✅
- Clear heading hierarchy (H1 → H2 → H3)
- FAQ section with semantic HTML
- Internal linking structure ready
- Schema-friendly markup throughout

---

## 🎨 What Claude Code Needs to Do (Design & Styling)

### Priority 1: Complete CSS Styling
**File:** `src/styles/main.css`

**Current Status:** Basic structure in place, needs enhancement

**What to Improve:**
1. **Color Palette**
   - Professional blue/teal for primary
   - Accent color for CTAs
   - Neutral backgrounds
   - Text colors for readability

2. **Typography**
   - Modern sans-serif fonts
   - Clear hierarchy
   - Good line-height and spacing

3. **Visual Design**
   - Framework visualization (3 layers)
   - Statistics display (large, bold numbers)
   - Professional, clean aesthetic
   - B2B-friendly design

4. **Responsive Design**
   - Mobile-first approach
   - Tablet optimization
   - Desktop enhancements

5. **Interactivity**
   - Hover states
   - Smooth transitions
   - Clear CTAs

**See:** `docs/DESIGN-BRIEF.md` for complete requirements

---

## 📁 File Structure

```
maixaeo-site/
├── public/                    # Public assets (served at root)
│   ├── robots.txt           # ✅ DONE
│   └── llms.txt             # ✅ DONE
├── src/
│   ├── pages/
│   │   └── index.html       # ✅ DONE (needs styling)
│   ├── components/          # (future)
│   ├── styles/
│   │   └── main.css         # ⏳ NEEDS ENHANCEMENT
│   ├── scripts/
│   │   └── schema-loader.js # ✅ DONE
│   └── schema/              # ✅ DONE
│       ├── organization.json
│       ├── person.json
│       └── service.json
└── docs/
    └── DESIGN-BRIEF.md      # ✅ DONE (for Claude Code)
```

---

## 🚀 Deployment Options

### Option 1: Static Site (Simplest)
- Deploy `public/` and `src/pages/` to any static host
- Netlify, Vercel, GitHub Pages, etc.
- Schema files need to be accessible at `/schema/*.json`

### Option 2: Framework Conversion
- Convert to Next.js, Gatsby, or similar
- Keep schema structure
- Add dynamic routing

### Option 3: Current Structure
- Serve as-is with a simple server
- All files are static HTML/JSON
- Schema loader handles dynamic injection

---

## 📋 Next Steps Checklist

### For Claude Code:
- [ ] Enhance `src/styles/main.css` (see DESIGN-BRIEF.md)
- [ ] Create additional page styles (Framework, Services, About)
- [ ] Add responsive breakpoints
- [ ] Polish visual design
- [ ] Add hover states and transitions

### For Content:
- [ ] Create Framework page (`src/pages/framework.html`)
- [ ] Create Services page (`src/pages/services.html`)
- [ ] Create About page (`src/pages/about.html`)
- [ ] Create Contact page (`src/pages/contact.html`)

### For AEO Optimization:
- [ ] Add more content pieces
- [ ] Create comparison pages
- [ ] Build blog/content section
- [ ] Track visibility metrics

---

## 🔧 Technical Notes

### Schema Loading
- Schemas are loaded via `schema-loader.js`
- JSON files in `src/schema/` are fetched and injected
- FAQ schema is generated from HTML

### File Serving
- Schema files need to be accessible at `/schema/*.json`
- If using static hosting, ensure JSON files are served correctly
- robots.txt and llms.txt should be at root (`/`)

### Browser Compatibility
- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES6+ JavaScript (schema-loader.js)
- CSS Grid and Flexbox

---

## ✅ AEO Optimization Status

### Layer 1: Technical Foundation ✅ COMPLETE
- [x] Schema markup (Organization, Person, Service, FAQ)
- [x] robots.txt optimized for AI crawlers
- [x] llms.txt with structured information
- [x] Clear heading hierarchy
- [x] FAQ section with schema
- [x] Semantic HTML structure

### Layer 2: Visibility Strategy ⏳ IN PROGRESS
- [ ] Content creation
- [ ] Comparison pages
- [ ] Citations strategy

### Layer 3: Brand Authority ⏳ IN PROGRESS
- [ ] Brand positioning content
- [ ] Case studies
- [ ] Thought leadership

---

*Technical foundation complete. Ready for Claude Code to handle design & styling.*
