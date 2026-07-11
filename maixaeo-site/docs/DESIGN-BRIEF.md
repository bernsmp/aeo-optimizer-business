# Design Brief for maixAEO.com
## For Claude Code - Design & Styling

**Design Inspiration:** https://www.getthinusa.com/  
**Goal:** Create a clean, premium, easy-to-read design similar to getthinusa.com

**See:** `DESIGN-INSPIRATION-ANALYSIS.md` for detailed analysis of what to borrow from getthinusa.com

---

## 🎨 Brand Identity

### Positioning
**"Anti-AEO-hack technical expert"** - Professional, trustworthy, evidence-based

### Key Messaging
- Hero: "No Magic AEO Hacks. Just Technical Excellence That Works."
- Subheadline: "95% of AEO Initiatives Fail. We Focus on the 5% That Works."
- Tagline: "Max + AI + AEO = maixAEO" (clever wordplay)

### Brand Personality
- **Technical** - Shows expertise, not fluff
- **Honest** - No hype, just facts
- **Evidence-based** - Cites research (Princeton, competitive intelligence)
- **Professional** - B2B-friendly, trustworthy
- **Modern** - Tech-forward, but not flashy

---

## 🎨 Design Direction

### Color Palette
- **Primary:** Professional blue or dark teal (trust, expertise)
  - *Note: Analyze getthinusa.com color choices and adapt*
- **Secondary:** Accent color for CTAs (orange/red for urgency, or green for success)
  - *Note: Borrow CTA color strategy from getthinusa.com*
- **Neutral:** Clean whites, light grays for backgrounds
  - *Note: Match getthinusa.com's background color approach*
- **Text:** Dark gray/black for readability
  - *Note: Use similar text color contrast as getthinusa.com*

### Typography
- **Headings:** Modern sans-serif (Inter, Poppins, or similar)
  - *Note: Analyze getthinusa.com font choices and use similar approach*
- **Body:** Clean, readable sans-serif
  - *Note: Match getthinusa.com's readability standards*
- **Code/Technical:** Monospace for technical content
- **Hierarchy:** Clear H1 → H6 structure
  - *Note: Borrow typography hierarchy from getthinusa.com*

### Visual Style
- **Clean & Minimal** - No clutter, focus on content
  - *Match getthinusa.com's minimalism level*
- **Data-Driven** - Statistics prominently displayed
  - *Use similar emphasis approach as getthinusa.com*
- **Technical** - Subtle tech elements (grids, lines, code snippets)
- **Professional** - B2B aesthetic, not consumer flashy
  - *Achieve same "premium" feel as getthinusa.com*

---

## 📐 Layout Requirements

### Homepage Structure
1. **Header/Navigation**
   - Logo: maixAEO (stylized)
   - Nav: Framework | Services | About | Contact
   - Clean, sticky header

2. **Hero Section**
   - Large, bold headline
   - Subheadline
   - Value prop ("Early-stage companies can win visibility in 2 days")
   - Two CTAs: "Get Started" (primary) | "See Our Framework" (secondary)

3. **Framework Overview**
   - Three columns (Layer 1, 2, 3)
   - Visual connection between layers (arrows/flow)
   - Benefits highlighted

4. **Statistics Section**
   - Grid of 4 key stats
   - Large numbers, clear labels
   - Visual emphasis on "95% fail" and "0.664 correlation"

5. **What Works Section**
   - List format with +30-40%, +37%, -10%, -40%
   - Source citation (Princeton)
   - Visual distinction between positive/negative

6. **FAQ Section**
   - Accordion or expandable format
   - Clear Q&A structure
   - Schema-friendly markup

7. **CTA Section**
   - Final call-to-action
   - "Ready to Win at AEO?"

8. **Footer**
   - Links, copyright
   - Clean, minimal

---

## 🎯 Key Design Elements

### Framework Visualization
- **Three layers** visually connected
- Could use:
  - Stacked layers (1 → 2 → 3)
  - Flow diagram (arrows)
  - Three columns with connecting lines
- Each layer should show:
  - Layer name
  - What it includes
  - Benefit (✅ Also helps SEO, etc.)

### Statistics Display
- **Large, bold numbers** (95%, 30%, 0.664, 10x)
- **Clear labels** below numbers
- **Visual hierarchy** - most important stats larger
- **Color coding** - negative stats (95% fail) vs. positive (0.664 correlation)

### Evidence-Based Design
- **Citations visible** - Princeton study, sources
- **Research-backed** - Show credibility
- **No hype** - Professional, factual

---

## 📱 Responsive Design

### Mobile-First
- Mobile-friendly navigation (hamburger menu)
- Stacked layout on mobile
- Touch-friendly CTAs
- Readable text sizes

### Tablet & Desktop
- Multi-column layouts
- Side-by-side comparisons
- Hover states for interactivity

---

## 🎨 Component Styles Needed

### Buttons
- **Primary CTA:** Bold, prominent, action color
- **Secondary CTA:** Outlined, less prominent
- **Hover states:** Clear feedback

### Cards/Sections
- **Framework layers:** Card-style with borders/shadows
- **Statistics:** Card-style with emphasis
- **FAQ items:** Expandable cards

### Typography Hierarchy
- **H1:** Hero headline (largest)
- **H2:** Section headers
- **H3:** Subsection headers
- **Body:** Readable, good line-height

---

## 🚫 What NOT to Do

- ❌ Flashy animations (professional, not consumer)
- ❌ Overly colorful (keep it professional)
- ❌ Hype language visuals (no "magic" imagery)
- ❌ Cluttered layouts (clean, focused)
- ❌ Generic stock photos (use illustrations or real content)

---

## ✅ What TO Do

- ✅ Clean, professional design
- ✅ Clear visual hierarchy
- ✅ Data-driven (statistics prominent)
- ✅ Technical aesthetic (subtle)
- ✅ Evidence-based (citations visible)
- ✅ Trust-building (professional, honest)

---

## 📋 Files to Style

### Main Files:
- `src/pages/index.html` - Homepage
- `src/styles/main.css` - Main stylesheet

### Additional Pages (to be created):
- `src/pages/framework.html` - Framework explanation
- `src/pages/services.html` - Services page
- `src/pages/about.html` - About page
- `src/pages/contact.html` - Contact page

---

## 🎯 Design Goals

1. **Build Trust** - Professional, evidence-based design
2. **Show Expertise** - Technical, knowledgeable aesthetic
3. **Differentiate** - "Anti-hack" positioning visually clear
4. **Convert** - Clear CTAs, easy navigation
5. **AEO-Optimized** - Schema-friendly, semantic HTML

---

## 📝 Notes for Claude Code

- All HTML structure is in place
- Schema markup is loaded dynamically
- Focus on CSS styling and visual design
- Maintain semantic HTML structure
- Ensure accessibility (WCAG guidelines)
- Optimize for performance (fast loading)
- Mobile-first responsive design

**Start with:** `src/styles/main.css` - Create comprehensive stylesheet for the homepage, then extend to other pages.

---

*Design should reflect: Technical excellence, evidence-based approach, anti-hack positioning, professional B2B aesthetic.*
