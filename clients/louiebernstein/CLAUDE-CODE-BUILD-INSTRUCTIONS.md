# Claude Code Build Instructions: Louie Bernstein Website

## 🎯 Project Overview

**Goal:** Rebuild Louie Bernstein's website from Systeme.io to a modern, AEO-optimized Next.js site on Vercel.

**Current Site:** Single-page site at http://louiebernstein.com (hosted on Systeme.io)
**New Site:** Next.js 14+ with TypeScript, Tailwind CSS, deployed to Vercel

---

## 📋 Content Breakdown (From Scraped Site)

### Homepage Sections (Single Page Site)

#### 1. **Hero Section**
- **Headline:** "Fractional Sales Leader"
- **Tagline:** "Less Spend. More Sales."
- **Value Proposition:** "I'll organize, optimize, and train your sales team, so you don't have to."

#### 2. **Call-to-Action Section**
- **CTA 1:** "Click to Learn How my Fractional Sales Leadership will drive results for you and your team."
  - Link: https://www.linkedin.com/in/sales-processes/
- **CTA 2:** "Click to schedule a discussion"
  - Link: https://calendly.com/louiebernstein/30minutes?month=2023-12

#### 3. **Testimonials Section**
- **Testimonial 1:**
  - Quote: "When Louie came on board he wrote and organized our outbound scripts and emails. We now had everyone working off the same playbook, and it gave us consistency."
  - Author: Neal Reynolds, CEO - BankMarketingCenter.com

- **Testimonial 2:**
  - Quote: "Thank you Louie for what you have done in the past year. I believe our sales are far better than where they were a year ago, great job."
  - Author: Kevin Zhao, CEO ZBS POS

#### 4. **Value Proposition Section**
- **Headline:** "It's not how much you sell."
- **Subheadline:** "It's how much you take home."
- **CTA:** "Let's get going!"

#### 5. **Awards Section**
- **Image:** https://d1yei2z3i6k35z.cloudfront.net/1671832/64e3c2e5505e5505e3_fourawards.png
- **Note:** Louie has received four awards for sales consulting

#### 6. **Contact Section**
- **Email:** Louie@LouieBernstein.com
- **Phone:** (404)808-5326

#### 7. **Social Links Section**
- **LinkedIn:** https://www.linkedin.com/in/sales-processes/
  - Icon: https://d1yei2z3i6k35z.cloudfront.net/1671832/6314e5dbd04ec_LinkedIn.png
- **YouTube:** https://www.youtube.com/playlist?list=PL7HfhnqHyzRmGDUMDhcSgZW8pR7DhW_Hl
  - Icon: https://d1yei2z3i6k35z.cloudfront.net/1671832/63d58395c8873_youtube.png

---

## 🏗️ Technical Requirements

### Stack
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Deployment:** Vercel
- **Type:** Static Site Generation (SSG) or Server Components

### File Structure
```
clients/louiebernstein/website/
├── app/
│   ├── layout.tsx          # Root layout with schema markup + header/footer
│   ├── page.tsx            # Homepage
│   ├── articles/
│   │   └── page.tsx        # Articles/Blog page
│   ├── videos/
│   │   └── page.tsx        # All YouTube Videos page
│   ├── featured-videos/
│   │   └── page.tsx        # Featured Videos page
│   ├── newsletter/
│   │   └── page.tsx        # Sunday Starter Newsletter page
│   ├── about/
│   │   └── page.tsx        # About page (optional, separate from homepage)
│   ├── services/
│   │   └── page.tsx        # Services page (optional, separate from homepage)
│   ├── contact/
│   │   └── page.tsx        # Contact page (optional, separate from homepage)
│   ├── faq/
│   │   └── page.tsx        # FAQ page (optional, separate from homepage)
│   └── globals.css         # Global styles
├── components/
│   ├── ui/                 # shadcn components (if using shadcn)
│   │   └── background-ripple-effect.tsx  # Animated hero background
│   ├── Header.tsx          # Navigation header with menu
│   ├── Footer.tsx          # Footer component
│   ├── Hero.tsx            # Hero section (uses BackgroundCells)
│   ├── CTASection.tsx
│   ├── Testimonials.tsx
│   ├── ValueProp.tsx
│   ├── Awards.tsx
│   ├── Contact.tsx
│   ├── SocialLinks.tsx
│   ├── VideoEmbed.tsx      # YouTube video embed component
│   └── NewsletterSignup.tsx # Newsletter signup component
├── lib/
│   └── utils.ts            # cn utility function (required for components)
├── public/
│   ├── robots.txt
│   ├── llms.txt
│   └── images/            # Any images/assets
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.js
```

---

## 🎨 Design Requirements

### Style Guidelines
- **Modern & Professional:** Clean, business-focused design
- **Mobile-First:** Responsive design (mobile, tablet, desktop)
- **Fast Loading:** <3 seconds page load
- **Accessible:** WCAG 2.1 AA compliance
- **Color Scheme:** Professional (suggest navy blue, white, accent color)
- **Typography:** Clean, readable fonts (suggest Inter, Poppins, or similar)

### Layout Suggestions
- **Header:** Fixed or sticky navigation with logo and menu
- **Hero:** Full-width, centered content, prominent CTA
- **Sections:** Clear visual separation between sections
- **Testimonials:** Card-based layout, alternating or side-by-side
- **Contact:** Easy to find, clear contact information
- **Footer:** Social links, contact info, copyright

### Navigation Menu Structure
**Header Menu Items:**
- Home
- Articles
- Videos (dropdown or separate)
  - All Videos
  - Featured Videos
- Newsletter (Sunday Starter)
- About (optional)
- Services (optional)
- Contact (optional)
- FAQ (optional)

---

## 🔍 AEO Optimization Requirements

### 1. Schema Markup (Already Created)
**Location:** `clients/louiebernstein/`

Add these schemas to `app/layout.tsx`:
- ✅ **Organization Schema** (`schema-organization.html`)
- ✅ **Service Schema** (`schema-service.html`)
- ✅ **FAQPage Schema** (`schema-faq.html`)

### 2. Technical Files (Already Created)
- ✅ **robots.txt** - Copy to `public/robots.txt`
- ✅ **llms.txt** - Copy to `public/llms.txt`

### 3. SEO Optimization
- **Meta Tags:** Title, description, OpenGraph
- **Semantic HTML:** Proper heading hierarchy (H1, H2, H3)
- **Alt Text:** All images need descriptive alt text
- **Internal Linking:** (if multiple pages added later)
- **Structured Data:** All schema markup implemented

### 4. Content Optimization
- **Clear Headings:** H1 for main title, H2 for sections
- **FAQ Section:** Add FAQ section with FAQPage schema
- **Keywords:** Include target keywords naturally:
  - "fractional sales leader"
  - "fractional sales leadership"
  - "sales team optimization"
  - "sales process consulting"

---

## 📝 Content Enhancements Needed

### Add These Sections (Not in Current Site):

1. **About Section** (Expand on value proposition)
   - Who Louie is
   - Experience/credentials
   - Why fractional sales leadership

2. **Services Section** (Detail what Louie offers)
   - Sales team organization
   - Sales process optimization
   - Sales team training
   - Sales playbook development
   - Pipeline management

3. **FAQ Section** (Critical for AEO!)
   - Use FAQs from `SCHEMA-FAQ.md`
   - Add question-based keywords from content strategy
   - Implement FAQPage schema

4. **Process Section** (How it works)
   - Step-by-step process
   - What to expect
   - Timeline

---

## 📄 Page Structure & Navigation

### Required Pages

#### 1. **Homepage** (`app/page.tsx`)
- All sections from scraped content
- Hero, About, Services, Testimonials, FAQ, Contact, etc.

#### 2. **Articles Page** (`app/articles/page.tsx`)
- **Purpose:** Display blog articles/content
- **Content:** Articles from content strategy (to be created)
- **Layout:** Grid or list of article cards
- **Features:** 
  - Article titles
  - Excerpts
  - Read more links
  - Categories/tags (optional)
- **Future:** Link to articles from content strategy

#### 3. **Videos Page** (`app/videos/page.tsx`)
- **Purpose:** Display all YouTube videos
- **Content:** Embed YouTube videos from Louie's channel
- **YouTube Playlist:** https://www.youtube.com/playlist?list=PL7HfhnqHyzRmGDUMDhcSgZW8pR7DhW_Hl
- **Layout:** Grid of video embeds
- **Features:**
  - Video thumbnails
  - Video titles
  - Descriptions
  - YouTube embed component
- **Implementation:** Use YouTube iframe API or embed URLs

#### 4. **Featured Videos Page** (`app/featured-videos/page.tsx`)
- **Purpose:** Showcase selected/best videos
- **Content:** Curated selection of top videos
- **Layout:** Larger, more prominent video cards
- **Features:**
  - Featured video highlight
  - Selected videos grid
  - "Why featured" descriptions (optional)
- **Implementation:** Manually select videos to feature

#### 5. **Newsletter Page** (`app/newsletter/page.tsx`)
- **Purpose:** Promote Sunday Starter newsletter
- **Content:** 
  - Newsletter description
  - Embedded YouTube videos (from newsletter)
  - Signup link to LinkedIn newsletter
- **LinkedIn Newsletter:** https://www.linkedin.com/newsletters/the-sunday-starter-6914239256987131904/
- **Layout:**
  - Hero section about newsletter
  - Embedded videos section
  - Prominent signup CTA
- **Features:**
  - Newsletter benefits/description
  - Video embeds
  - "Subscribe on LinkedIn" button/link
  - Newsletter archive (if available)

### Optional Pages (Recommended)

#### 6. **About Page** (`app/about/page.tsx`)
- **Purpose:** Detailed about Louie
- **Content:** Expanded about section
- **Benefits:** Better SEO, dedicated page for "About" queries

#### 7. **Services Page** (`app/services/page.tsx`)
- **Purpose:** Detailed services information
- **Content:** Expanded services section
- **Benefits:** Better SEO, dedicated page for service queries

#### 8. **Contact Page** (`app/contact/page.tsx`)
- **Purpose:** Contact form and information
- **Content:** Contact form, email, phone, Calendly link
- **Benefits:** Better UX, dedicated contact page

#### 9. **FAQ Page** (`app/faq/page.tsx`)
- **Purpose:** Comprehensive FAQ section
- **Content:** All FAQs from schema
- **Benefits:** Critical for AEO, dedicated FAQ page ranks well

---

## 🎬 YouTube Integration

### YouTube Channel
- **Channel:** Louie Bernstein YouTube Channel
- **Playlist:** https://www.youtube.com/playlist?list=PL7HfhnqHyzRmGDUMDhcSgZW8pR7DhW_Hl

### Implementation Options

#### Option 1: YouTube Playlist Embed
- Embed entire playlist
- Simple, but less control

#### Option 2: Individual Video Embeds
- Embed specific videos
- More control over layout
- Better for featured videos

#### Option 3: YouTube API (Advanced)
- Fetch videos dynamically
- More features, but requires API setup

**Recommendation:** Start with Option 2 (individual embeds) for featured videos, Option 1 for all videos page.

### Video Embed Component
Create `components/VideoEmbed.tsx`:
```tsx
// Example structure
<iframe
  src="https://www.youtube.com/embed/VIDEO_ID"
  title="Video title"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowFullScreen
/>
```

---

## 📧 Newsletter Integration

### Sunday Starter Newsletter
- **LinkedIn Newsletter:** https://www.linkedin.com/newsletters/the-sunday-starter-6914239256987131904/
- **Description:** "Delivered to accelerate your success" - Weekly newsletter
- **Content:** YouTube videos embedded in newsletter

### Newsletter Page Features
1. **Hero Section:**
   - Newsletter name: "The Sunday Starter"
   - Tagline: "Delivered to accelerate your success"
   - Description: What the newsletter is about

2. **Videos Section:**
   - Embedded YouTube videos from newsletter
   - Video titles and descriptions
   - Grid layout

3. **Signup Section:**
   - Prominent CTA: "Subscribe on LinkedIn"
   - Link to: https://www.linkedin.com/newsletters/the-sunday-starter-6914239256987131904/
   - Benefits of subscribing

4. **Archive Section (Optional):**
   - Past newsletter issues
   - Links to LinkedIn newsletter

---

## 🎯 Additional Page Suggestions

### Recommended Additions:

1. **Case Studies Page** (`app/case-studies/page.tsx`)
   - **Why:** Expand on testimonials with detailed case studies
   - **Content:** BankMarketingCenter.com, ZBS POS case studies
   - **Benefits:** Social proof, SEO value

2. **Resources Page** (`app/resources/page.tsx`)
   - **Why:** Central hub for all content
   - **Content:** Links to articles, videos, newsletter, tools
   - **Benefits:** Better UX, internal linking for SEO

3. **Process Page** (`app/process/page.tsx`)
   - **Why:** Detailed "How It Works" explanation
   - **Content:** Step-by-step process, timeline, expectations
   - **Benefits:** Conversion optimization, SEO

### Navigation Menu Options:

**Option 1: Simple Menu**
- Home
- Articles
- Videos
- Newsletter
- Contact

**Option 2: Expanded Menu**
- Home
- About
- Services
- Articles
- Videos
  - All Videos
  - Featured Videos
- Newsletter
- FAQ
- Contact

**Recommendation:** Start with Option 1, expand to Option 2 as content grows.

---

## 🚀 Build Steps for Claude Code

### Step 1: Initialize Next.js Project
```bash
cd clients/louiebernstein
npx create-next-app@latest website --typescript --tailwind --app --no-src-dir
cd website
```

### Step 2: Install Dependencies
```bash
npm install
npm install framer-motion
npm install clsx tailwind-merge  # For cn utility function
```

**Note:** If using shadcn/ui, run `npx shadcn@latest init` first, then install dependencies.

### Step 3: Setup shadcn/ui (Optional but Recommended)
```bash
npx shadcn@latest init
```
- Choose default settings
- **Important:** Set components directory to `components/ui`
- This creates the `lib/utils.ts` file needed for components

### Step 4: Create Component Structure
- Create `components/` directory (and `components/ui/` if using shadcn)
- Create `lib/utils.ts` with `cn` function (if not created by shadcn)
- Copy `background-ripple-effect.tsx` to `components/ui/` (see FRAMER-MOTION-HERO-SETUP.md)
- Build reusable components for each section
- Use TypeScript for type safety
- **Important:** Create `Header.tsx` and `Footer.tsx` components first

### Step 5: Build Hero Component (`components/Hero.tsx`)
- Use `BackgroundCells` component from `components/ui/background-ripple-effect.tsx`
- Add hero content (headline, tagline, value proposition)
- Add CTA buttons
- See `FRAMER-MOTION-HERO-SETUP.md` for detailed usage

### Step 6: Build Header & Navigation (`components/Header.tsx`)
- Create header component with logo
- Add navigation menu:
  - Home
  - Articles
  - Videos (with dropdown: All Videos, Featured Videos)
  - Newsletter
  - Contact (optional)
- Make it responsive (mobile hamburger menu)
- Add to `app/layout.tsx`

### Step 7: Build Footer (`components/Footer.tsx`)
- Contact information
- Social links
- Copyright
- Add to `app/layout.tsx`

### Step 8: Build Homepage (`app/page.tsx`)
- Import all section components
- Arrange sections in logical order:
  1. Hero
  2. About (new)
  3. Services (new)
  4. Value Proposition
  5. Testimonials
  6. Process (new)
  7. FAQ (new)
  8. Contact
  9. Awards
  10. Social Links

### Step 9: Add Schema Markup (`app/layout.tsx`)
- Read schema files from parent directory
- Add JSON-LD scripts to `<head>`
- Include Organization, Service, FAQPage schemas

### Step 10: Add Technical Files
- Copy `robots.txt` to `public/robots.txt`
- Copy `llms.txt` to `public/llms.txt`
- Ensure they're accessible at root URLs

### Step 11: Build Additional Pages
- **Articles Page** (`app/articles/page.tsx`)
  - Grid/list of articles
  - Article cards with titles, excerpts
  - Placeholder for future articles
  
- **Videos Page** (`app/videos/page.tsx`)
  - Embed YouTube playlist or individual videos
  - Grid layout
  - Video titles and descriptions
  
- **Featured Videos Page** (`app/featured-videos/page.tsx`)
  - Selected videos
  - Larger, more prominent layout
  - Featured video highlight
  
- **Newsletter Page** (`app/newsletter/page.tsx`)
  - Newsletter description
  - Embedded videos
  - LinkedIn signup link/button
  - Benefits of subscribing

### Step 12: Style & Polish
- Use Tailwind CSS for styling
- Ensure mobile responsiveness
- Optimize images (use Next.js Image component)
- Test loading speed
- Test navigation on all pages

### Step 13: Deploy to Vercel
```bash
vercel login
vercel --prod
```

---

## 📄 Files to Reference

### Scraped Content
- `scraped-content/homepage.json` - Original content
- `scraped-content/homepage.md` - Markdown version

### Component Setup
- `FRAMER-MOTION-HERO-SETUP.md` - Detailed setup for animated hero component
- `components/background-ripple-effect.tsx` - Framer Motion hero component

### AEO Deliverables (Already Created)
- `schema-organization.html` - Organization schema
- `schema-service.html` - Service schema
- `schema-faq.html` - FAQPage schema
- `robots.txt` - Robots file
- `llms.txt` - LLMs file
- `content-strategy.md` - Content strategy
- `COMPETITOR-ANALYSIS.md` - Competitor analysis

### Client Info
- `CLIENT-INFO.md` - Business information
- `aeo-score-analysis.md` - AEO analysis

---

## 🎯 Key Priorities

1. **AEO Optimization:** Implement all schema markup, robots.txt, llms.txt
2. **Modern Design:** Clean, professional, mobile-responsive
3. **Fast Loading:** Optimize images, minimize bundle size
4. **Content Enhancement:** Add About, Services, FAQ sections
5. **SEO:** Proper meta tags, semantic HTML, keyword optimization

---

## ✅ Checklist for Claude Code

### Setup
- [ ] Initialize Next.js project
- [ ] Set up shadcn/ui (optional but recommended)
- [ ] Install dependencies (framer-motion, clsx, tailwind-merge)
- [ ] Create component structure
- [ ] Set up Tailwind CSS
- [ ] Create `lib/utils.ts` with `cn` function
- [ ] Copy `background-ripple-effect.tsx` to `components/ui/`

### Core Components
- [ ] Build Hero component with BackgroundCells animation
- [ ] Build Header component with navigation
- [ ] Build Footer component
- [ ] Create reusable section components (CTAs, Testimonials, etc.)

### Pages
- [ ] Build homepage with all sections
- [ ] Build Articles page
- [ ] Build Videos page (all videos)
- [ ] Build Featured Videos page
- [ ] Build Newsletter page
- [ ] (Optional) Build About page
- [ ] (Optional) Build Services page
- [ ] (Optional) Build Contact page
- [ ] (Optional) Build FAQ page

### AEO & SEO
- [ ] Add schema markup (Organization, Service, FAQPage) to layout.tsx
- [ ] Copy robots.txt to public/
- [ ] Copy llms.txt to public/
- [ ] Add meta tags to each page (title, description, OpenGraph)
- [ ] Ensure semantic HTML structure
- [ ] Add proper heading hierarchy (H1, H2, H3)

### YouTube Integration
- [ ] Create VideoEmbed component
- [ ] Embed videos on Videos page
- [ ] Embed featured videos on Featured Videos page
- [ ] Embed videos on Newsletter page

### Newsletter Integration
- [ ] Add newsletter description
- [ ] Add LinkedIn signup link/button
- [ ] Embed newsletter videos

### Styling & Polish
- [ ] Style with Tailwind CSS (mobile-responsive)
- [ ] Optimize images (use Next.js Image component)
- [ ] Test navigation on all pages
- [ ] Test mobile hamburger menu
- [ ] Ensure fast loading (<3 seconds)

### Testing
- [ ] Test on mobile, tablet, desktop
- [ ] Test all navigation links
- [ ] Test YouTube embeds
- [ ] Test newsletter signup link
- [ ] Verify schema markup (use Google Rich Results Test)
- [ ] Test robots.txt and llms.txt accessibility

### Deployment
- [ ] Deploy to Vercel
- [ ] Test live site
- [ ] Verify all pages load correctly

---

## 💡 Design Inspiration

**Style:** Modern B2B consultant website
**Examples:** 
- Clean, professional layouts
- Clear CTAs
- Testimonial sections
- Service/process explanations
- Contact forms or clear contact info

**Color Suggestions:**
- Primary: Navy blue (#1e3a8a) or dark blue
- Secondary: White (#ffffff)
- Accent: Orange (#f97316) or teal (#14b8a6)
- Text: Dark gray (#1f2937)

---

## 🎬 Ready to Build!

All content is scraped and organized. All AEO deliverables are ready. Now it's time to build a beautiful, modern, AEO-optimized website!

**Start with:** Reading the scraped content, then building the Next.js project structure.

