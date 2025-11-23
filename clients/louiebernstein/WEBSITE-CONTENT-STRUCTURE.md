# Website Content Structure - Louie Bernstein

## Content Organization for Website Build

This document breaks down all content from the scraped site into organized sections for easy implementation.

---

## 🏠 Homepage Structure (Single Page Site)

### Section 1: Hero Section
```markdown
Headline: Fractional Sales Leader
Tagline: Less Spend. More Sales.
Value Proposition: I'll organize, optimize, and train your sales team, so you don't have to.
```

**Design Notes:**
- Large, bold headline
- Prominent tagline
- Clear value proposition
- CTA buttons below

---

### Section 2: Primary CTAs
```markdown
CTA 1:
  Text: "Learn How my Fractional Sales Leadership will drive results for you and your team"
  Link: https://www.linkedin.com/in/sales-processes/
  Style: Primary button

CTA 2:
  Text: "Schedule a Discussion"
  Link: https://calendly.com/louiebernstein/30minutes?month=2023-12
  Style: Secondary button
```

**Design Notes:**
- Two prominent buttons
- Clear, action-oriented text
- External links (LinkedIn, Calendly)

---

### Section 3: Testimonials
```markdown
Testimonial 1:
  Quote: "When Louie came on board he wrote and organized our outbound scripts and emails. We now had everyone working off the same playbook, and it gave us consistency."
  Author: Neal Reynolds
  Title: CEO
  Company: BankMarketingCenter.com

Testimonial 2:
  Quote: "Thank you Louie for what you have done in the past year. I believe our sales are far better than where they were a year ago, great job."
  Author: Kevin Zhao
  Title: CEO
  Company: ZBS POS
```

**Design Notes:**
- Card-based layout
- Quote styling
- Author attribution
- Company logos (if available)

---

### Section 4: Value Proposition
```markdown
Headline: It's not how much you sell.
Subheadline: It's how much you take home.
CTA: Let's get going!
```

**Design Notes:**
- Bold, impactful statement
- Visual emphasis
- CTA button

---

### Section 5: Awards & Credentials
```markdown
Image: https://d1yei2z3i6k35z.cloudfront.net/1671832/64e3c2e5505e3_fourawards.png
Alt Text: Four Awards for Sales Consulting Services
```

**Design Notes:**
- Display awards image
- Alt text for accessibility
- Optional: Add text about awards

---

### Section 6: Contact Information
```markdown
Email: Louie@LouieBernstein.com
Phone: (404)808-5326
```

**Design Notes:**
- Clear, easy to find
- Clickable email link
- Clickable phone number (tel: link)
- Icon support (email, phone)

---

### Section 7: Social Links
```markdown
LinkedIn:
  URL: https://www.linkedin.com/in/sales-processes/
  Icon: https://d1yei2z3i6k35z.cloudfront.net/1671832/6314e5dbd04ec_LinkedIn.png
  Text: Connect on LinkedIn

YouTube:
  URL: https://www.youtube.com/playlist?list=PL7HfhnqHyzRmGDUMDhcSgZW8pR7DhW_Hl
  Icon: https://d1yei2z3i6k35z.cloudfront.net/1671832/63d58395c8873_youtube.png
  Text: Watch on YouTube
```

**Design Notes:**
- Social media icons
- Hover effects
- External link indicators

---

## ➕ Additional Sections to Add (Not in Current Site)

### Section 8: About Louie (NEW)
```markdown
Headline: About Louie Bernstein
Content: 
  - Experienced fractional sales leader
  - Helps $1M-$10M ARR companies
  - Focus on organizing, optimizing, training sales teams
  - LinkedIn Top Voice
  - Scaled from zero to INC 500
  - Four awards for sales consulting
```

**Source:** Use content from `CLIENT-INFO.md` and `llms.txt`

---

### Section 9: Services (NEW)
```markdown
Headline: Services
Services:
  1. Sales Team Organization & Optimization
  2. Sales Team Training
  3. Sales Process Documentation
  4. Sales Rep Onboarding
  5. Pipeline Management
  6. Sales Playbook Development
```

**Source:** Use content from `CLIENT-INFO.md`

---

### Section 10: How It Works / Process (NEW)
```markdown
Headline: How Fractional Sales Leadership Works
Steps:
  1. Initial Consultation
  2. Assessment & Strategy Development
  3. Implementation
  4. Training & Enablement
  5. Ongoing Support
```

**Source:** Create based on typical fractional sales leadership process

---

### Section 11: FAQ Section (NEW - CRITICAL FOR AEO!)
```markdown
Headline: Frequently Asked Questions

Questions (from SCHEMA-FAQ.md):
  1. What is fractional sales leadership?
  2. How does fractional sales leadership work?
  3. Who is fractional sales leadership for?
  4. How much does fractional sales leadership cost?
  5. What is the time commitment?
  6. What results can I expect?
  7. What is the process for working with a fractional sales leader?

Additional Questions (from content strategy):
  8. What is a fractional sales manager?
  9. What is sales enablement consulting?
  10. What is the difference between a fractional sales consultant and fractional sales leader?
```

**Source:** Use `SCHEMA-FAQ.md` and `content-strategy.md`

**AEO Note:** This section MUST include FAQPage schema markup!

---

## 📐 Recommended Page Layout Order

1. **Hero** - First impression
2. **About** - Who Louie is
3. **Services** - What Louie offers
4. **Value Proposition** - Why it matters
5. **How It Works** - Process explanation
6. **Testimonials** - Social proof
7. **FAQ** - Answer common questions (AEO gold!)
8. **Awards** - Credibility
9. **Contact** - Easy to find
10. **Social Links** - Footer

---

## 🎨 Content Enhancements

### Expand Testimonials
- Add more detail about results
- Include metrics if available
- Add company logos if possible

### Add Case Studies (Future)
- BankMarketingCenter.com case study
- ZBS POS case study
- Detail the process and results

### Add Blog Section (Future)
- Link to content strategy articles
- SEO benefits
- Authority building

---

## 📝 Content Sources

### From Scraped Site:
- `scraped-content/homepage.json` - All current content

### From AEO Deliverables:
- `CLIENT-INFO.md` - Business information
- `llms.txt` - Key facts about Louie
- `SCHEMA-FAQ.md` - FAQ content
- `content-strategy.md` - Content ideas

### To Create:
- About section content
- Services detailed descriptions
- Process explanation
- Additional FAQs

---

## ✅ Content Checklist

- [x] Hero section content
- [x] CTAs
- [x] Testimonials (2)
- [x] Value proposition
- [x] Awards image
- [x] Contact information
- [x] Social links
- [ ] About section (to create)
- [ ] Services section (to create)
- [ ] Process section (to create)
- [ ] FAQ section (to create from schema)

---

**All content is ready for Claude Code to build!** 🚀


