# Louie Bernstein Site: CMS Integration Plan

## Overview

This site will be upgraded with **Payload CMS** + **VoiceCraft** integration as the first implementation of the AI-Managed Website Platform.

**Full Product Vision:** See `/Users/maxb/Desktop/Vibe Projects/VoiceCraft/PRODUCT-VISION-VOICECRAFT-CMS.md`

---

## What Louie Gets

### 1. Visual Admin Panel (`/admin`)
- See all articles, videos, testimonials
- Edit content with rich text editor
- Upload images
- Manage site settings
- Preview before publishing

### 2. Slack Integration
```
"Write an article about sales compensation plans"
→ AI writes in Louie's voice, publishes to site

"Update hero video to [youtube-url]"
→ Done in seconds

"Add testimonial from John at Acme"
→ Added and deployed
```

### 3. AI Content Generation
- Articles written in Louie's authentic voice
- Style fusion with sales writing masters
- SEO/AEO optimized automatically

---

## Content to Migrate

| Content Type | Current Location | Payload Collection |
|--------------|------------------|-------------------|
| Articles | `/content/articles/*.md` | `articles` |
| Hero Video | Hardcoded in Hero.tsx | `settings.heroVideo` |
| Video Playlists | Hardcoded in pages | `videos` |
| Testimonials | Hardcoded in components | `testimonials` |
| Site Settings | Hardcoded throughout | `settings` |

---

## Implementation Steps

### Phase 1: Payload Setup
- [ ] Install Payload CMS
- [ ] Configure database (MongoDB Atlas free tier)
- [ ] Define collections (Articles, Videos, Testimonials, Settings)
- [ ] Apply Louie's branding to admin panel
- [ ] Deploy and test admin access

### Phase 2: Content Migration
- [ ] Migrate article from markdown to Payload
- [ ] Move video links to Payload
- [ ] Add testimonials to Payload
- [ ] Create site settings

### Phase 3: Frontend Integration
- [ ] Update pages to fetch from Payload
- [ ] Add ISR (Incremental Static Regeneration)
- [ ] Test all pages

### Phase 4: VoiceCraft Connection
- [ ] Connect VoiceCraft to Payload API
- [ ] Add Slack commands for website management
- [ ] Set up deploy webhooks
- [ ] Test full workflow

---

## Tech Stack After Integration

```
louiebernstein.com
├── Next.js 16 (Frontend)
├── Payload CMS 3.x (Admin + API)
├── MongoDB Atlas (Database - free tier)
├── Vercel (Hosting)
└── VoiceCraft (AI Content via Slack)
```

---

## Timeline

| Task | Estimated Time |
|------|---------------|
| Payload setup + schemas | 3-4 hours |
| Admin branding | 1 hour |
| Content migration | 2 hours |
| Frontend integration | 2-3 hours |
| VoiceCraft connection | 2-3 hours |
| Testing | 2 hours |
| **Total** | **~12-14 hours** |

---

## Links

- **VoiceCraft Project:** `/Users/maxb/Desktop/Vibe Projects/VoiceCraft`
- **Voice Profile:** `/VoiceCraft/data/voices/louie_bernstein.json`
- **Product Vision:** `/VoiceCraft/PRODUCT-VISION-VOICECRAFT-CMS.md`
- **Live Site:** https://louiebernstein.com
- **Vercel Project:** website (maxs-projects-c414fff2)

---

*This is the first implementation of the VoiceCraft + CMS platform.*

