# SOP: AI-Managed Website Setup

Standard Operating Procedure for setting up a fully editable website with Payload CMS + VoiceCraft integration.

---

## Overview

This SOP creates a website where clients can:
1. **Edit via Admin Panel** (louiebernstein.com/admin)
2. **Edit via Slack** (natural language commands)
3. **Generate content via VoiceCraft** (AI writes in their voice)

---

## Prerequisites

- [ ] Next.js website template
- [ ] MongoDB Atlas account (free tier works)
- [ ] Vercel account for hosting
- [ ] Client's branding (logo, colors, fonts)
- [ ] Client's content (copy, images, videos)

---

## Phase 1: Database Setup (5 min)

### 1.1 Create MongoDB Atlas Cluster

1. Go to https://cloud.mongodb.com
2. Create free cluster (M0 Sandbox)
3. Create database user with password
4. **IMPORTANT:** Go to Network Access → Add IP Address → "Allow Access from Anywhere" (0.0.0.0/0)
5. Get connection string: `mongodb+srv://USER:PASS@cluster.mongodb.net/DATABASE`

### 1.2 Generate Payload Secret

```bash
openssl rand -base64 32
```

Save both values for environment variables.

---

## Phase 2: Payload CMS Integration (30 min)

### 2.1 Install Dependencies

```bash
npm install payload @payloadcms/db-mongodb @payloadcms/next @payloadcms/richtext-lexical graphql sharp
```

### 2.2 Create Payload Config

Create `payload.config.ts` in project root:

```typescript
import { buildConfig } from 'payload'
import { mongooseAdapter } from '@payloadcms/db-mongodb'
import { lexicalEditor } from '@payloadcms/richtext-lexical'
import path from 'path'
import { fileURLToPath } from 'url'

// Import collections and globals
import { Users } from './payload/collections/Users'
import { Articles } from './payload/collections/Articles'
import { SiteSettings } from './payload/globals/SiteSettings'

const filename = fileURLToPath(import.meta.url)
const dirname = path.dirname(filename)

export default buildConfig({
  admin: {
    user: Users.slug,
    meta: {
      titleSuffix: ' - Client Admin',
    },
    components: {
      graphics: {
        Logo: '@/payload/components/Logo#Logo',
        Icon: '@/payload/components/Icon#Icon',
      },
    },
  },
  collections: [Users, Articles],
  globals: [SiteSettings],
  editor: lexicalEditor(),
  db: mongooseAdapter({
    url: process.env.MONGODB_URI || '',
  }),
  typescript: {
    outputFile: path.resolve(dirname, 'payload-types.ts'),
  },
  secret: process.env.PAYLOAD_SECRET || '',
})
```

### 2.3 Create Collections

**`payload/collections/Users.ts`**
```typescript
import type { CollectionConfig } from 'payload'

export const Users: CollectionConfig = {
  slug: 'users',
  admin: { useAsTitle: 'email' },
  auth: true,
  fields: [
    { name: 'name', type: 'text' },
    { name: 'role', type: 'select', options: ['admin', 'editor'], defaultValue: 'editor' },
  ],
}
```

### 2.4 Create Site Settings Global

This is the heart of the editable content. Include ALL text that the client might want to change.

**Categories to include:**
- Hero section (headline, tagline, description, video, CTAs)
- About section (paragraphs, stats, callout)
- Services section (headline + array of items)
- Process section (headline + array of steps)
- FAQ section (headline + array of Q&As)
- Testimonials header (items managed separately)
- Awards section
- Contact info (email, phone)
- Social links (LinkedIn, YouTube, Calendly)
- Footer content
- SEO settings
- Page-specific content (Course, Newsletter, Videos pages)

**Key pattern for repeatable content:**
```typescript
{
  name: 'services',
  type: 'group',
  fields: [
    { name: 'headline', type: 'text' },
    { name: 'subheadline', type: 'text' },
    {
      name: 'items',
      type: 'array',
      fields: [
        { name: 'title', type: 'text', required: true },
        { name: 'description', type: 'textarea', required: true },
        { name: 'icon', type: 'text' },
      ],
    },
  ],
}
```

### 2.5 Create Admin Routes

**`app/(payload)/layout.tsx`**
```typescript
import config from '@payload-config'
import { RootLayout, handleServerFunctions } from '@payloadcms/next/layouts'
import { importMap } from './admin/importMap'
import '@payloadcms/next/css'

export default function Layout({ children }) {
  const serverFunction = async (args) => {
    'use server'
    return handleServerFunctions({ ...args, config, importMap })
  }
  return <RootLayout config={config} importMap={importMap} serverFunction={serverFunction}>{children}</RootLayout>
}
```

**`app/(payload)/admin/[[...segments]]/page.tsx`**
```typescript
import config from '@payload-config'
import { RootPage, generatePageMetadata } from '@payloadcms/next/views'
import { importMap } from '../importMap'

export const generateMetadata = ({ params }) => generatePageMetadata({ config, params })
export default RootPage
```

### 2.6 Create API Client

**`lib/payload.ts`**
- Define TypeScript interfaces for all settings
- Create default values (fallback when CMS unavailable)
- Fetch function with caching and revalidation
- Helper functions for each section

### 2.7 Update Components

For each component that displays editable content:
1. Add props interface with all editable fields
2. Set default values matching the hardcoded content
3. Use props instead of hardcoded strings
4. Update parent page to fetch and pass data

---

## Phase 3: Branding (10 min)

### 3.1 Admin Panel Branding

Create `payload/components/Logo.tsx` and `payload/components/Icon.tsx` with client's logo.

Update `app/(payload)/admin/importMap.js` to include the components.

### 3.2 Environment Variables

Add to Vercel:
- `MONGODB_URI` - MongoDB connection string
- `PAYLOAD_SECRET` - Generated secret

---

## Phase 4: VoiceCraft Integration (20 min)

### 4.1 CMS Integration Module

Create `VoiceCraft/integrations/cms_integration.py`:
- PayloadCMSClient class for API calls
- WebsiteEditor class for natural language parsing
- Field mappings for all editable content

### 4.2 Slack Bot Commands

Update `VoiceCraft/integrations/slack_bot.py`:
- `/site show` - View current settings
- `/site [field] "value"` - Update field
- Natural language: "Change the headline to..."

### 4.3 Environment Variables

```bash
LOUIE_SITE_URL=https://client-domain.com
LOUIE_ADMIN_EMAIL=client@email.com
LOUIE_ADMIN_PASSWORD=xxx
```

---

## Phase 5: Testing Checklist

### Admin Panel
- [ ] Can access /admin
- [ ] Can log in with credentials
- [ ] Can see all Site Settings sections
- [ ] Changes save successfully
- [ ] Changes appear on live site (after ~1 min)

### Components
- [ ] Hero displays CMS content
- [ ] About section displays CMS content
- [ ] Services display from CMS array
- [ ] Process steps display from CMS array
- [ ] FAQ items display from CMS array
- [ ] Awards display CMS content
- [ ] Footer uses CMS contact/social info

### Slack Integration
- [ ] `/site show` returns current settings
- [ ] `/site headline "test"` updates headline
- [ ] Natural language commands work

---

## Phase 6: Client Handoff

### Deliverables
1. **User Manual** (PDF) - How to use admin panel
2. **Login Credentials** - Admin email/password
3. **Quick Reference Card** - Most common edits

### Training Topics
- Logging into admin panel
- Finding Site Settings
- Editing text fields
- Saving changes
- When to contact support

---

## Content Inventory Template

Use this to audit what needs to be editable:

| Section | Field | Current Value | Editable? |
|---------|-------|---------------|-----------|
| Hero | Headline | "..." | ✅ |
| Hero | Tagline | "..." | ✅ |
| Hero | Description | "..." | ✅ |
| Hero | Video ID | "..." | ✅ |
| Hero | CTA Primary Text | "..." | ✅ |
| Hero | CTA Primary URL | "..." | ✅ |
| About | Headline | "..." | ✅ |
| About | Paragraph 1 | "..." | ✅ |
| ... | ... | ... | ... |

---

## Troubleshooting

### "500 Internal Server Error" on /admin
- Check MongoDB Atlas IP whitelist (must include 0.0.0.0/0)
- Verify MONGODB_URI is correct in Vercel env vars
- Check Vercel function logs for specific error

### Changes not appearing on site
- Verify you clicked "Save" in admin
- Wait 60 seconds (revalidation time)
- Check browser cache (try incognito)

### Build failures
- Run `npm run build` locally first
- Check for TypeScript errors in payload.ts
- Ensure all new fields have defaults

---

## Files Checklist

```
project/
├── payload.config.ts              # Main Payload config
├── payload/
│   ├── collections/
│   │   ├── Users.ts
│   │   ├── Articles.ts
│   │   ├── Videos.ts
│   │   └── Testimonials.ts
│   ├── globals/
│   │   └── SiteSettings.ts        # ALL editable content
│   └── components/
│       ├── Logo.tsx               # Client logo for admin
│       └── Icon.tsx               # Client favicon for admin
├── app/
│   ├── (payload)/                 # Admin panel routes
│   │   ├── layout.tsx
│   │   ├── admin/
│   │   │   ├── [[...segments]]/page.tsx
│   │   │   └── importMap.js
│   │   └── api/[...slug]/route.ts
│   └── (site)/                    # Public site routes
│       ├── layout.tsx             # Fetches footer data
│       └── page.tsx               # Fetches all section data
├── lib/
│   └── payload.ts                 # API client + types + defaults
└── components/
    ├── Hero.tsx                   # All accept props
    ├── sections/
    │   ├── About.tsx
    │   ├── Services.tsx
    │   ├── Process.tsx
    │   ├── FAQ.tsx
    │   └── ...
    └── Footer.tsx
```

---

*SOP Version: 1.0*  
*Created: November 25, 2025*  
*First Client: Louie Bernstein (louiebernstein.com)*

