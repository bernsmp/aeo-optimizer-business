# AEO Optimizer Resource Hub

A clean, premium resource hub for AEO (Answer Engine Optimization) resources, inspired by Get Thin USA's design principles.

## Features

- ✅ Clean, premium design with white background and blue accent
- ✅ Email capture component (backend TBD - ready for Beehiiv, ConvertKit, etc.)
- ✅ Markdown-based CMS for resources
- ✅ Responsive design (mobile-first)
- ✅ Resource cards and categories
- ✅ FAQ section
- ✅ All sections with copy ready

## Getting Started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the site.

## Email Integration (TBD)

The email capture component is ready but needs backend integration. Options:

1. **Beehiiv API** - Newsletter platform
2. **ConvertKit** - Email marketing
3. **Mailchimp** - Email marketing
4. **Custom API** - Build your own endpoint

See `components/ui/EmailCapture.tsx` for integration instructions.

## Adding Resources

Add markdown files to `content/resources/` with frontmatter:

```markdown
---
title: Your Resource Title
description: Brief description
type: guide | tool | template | article
date: 2024-01-15
downloadCount: 100
badge: Free
---

Your content here...
```

## Project Structure

```
website/
├── app/                    # Next.js app directory
│   ├── page.tsx           # Homepage
│   └── layout.tsx         # Root layout
├── components/
│   ├── ui/                # Reusable UI components
│   │   ├── EmailCapture.tsx
│   │   ├── ResourceCard.tsx
│   │   └── FAQ.tsx
│   ├── sections/          # Page sections
│   │   ├── Hero.tsx
│   │   ├── FeaturedResources.tsx
│   │   └── ...
│   ├── Header.tsx
│   └── Footer.tsx
├── content/
│   └── resources/         # Markdown resources
└── lib/
    └── resources.ts       # Resource utilities
```

## Design Principles

- **Clean white background** with minimal color
- **Generous white space** between sections
- **Clear visual hierarchy** with large headings
- **One accent color** (blue #0066FF) for CTAs
- **Professional typography** (Inter font)
- **Mobile-first** responsive design

## Next Steps

1. Set up email service integration (Beehiiv/ConvertKit/etc.)
2. Add more resources to `content/resources/`
3. Create resource detail pages
4. Add tools pages (AEO checker, schema generator)
5. Set up analytics

## Deployment

Deploy to Vercel:

```bash
vercel
```

Or any other hosting platform that supports Next.js.
