# Slack → CMS Automation (via Activepieces)

## Overview

This integration lets clients update their website directly from Slack - no need to learn the CMS admin panel.

```
Slack Message → Activepieces → Payload CMS API → Website Updates
```

## Supported Commands

### Content Updates
```
@website update hero tagline to "Less Spend. More Sales."
@website update newsletter description to "Join thousands of leaders..."
```

### Add Content
```
@website add testimonial "Great results!" - John Smith, CEO at Acme
@website add faq "How much does it cost?" → "Pricing varies based on scope..."
```

### VoiceCraft Integration
```
@voicecraft write article about cold email mistakes
@voicecraft draft newsletter intro about Q4 planning
```

### Publishing
```
@website publish article "cold-email-mistakes"
@website unpublish article "old-post"
```

---

## Setup Instructions

### Step 1: Activepieces Account

1. Log into [Activepieces](https://www.activepieces.com/)
2. Create a new project: "Louie Bernstein CMS"

### Step 2: Connect Slack

1. In Activepieces, go to **Connections**
2. Add **Slack** connection
3. Authorize with your Slack workspace
4. Note the bot token for later

### Step 3: Create Slack App (if needed)

If you don't have a Slack app yet:

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Create New App → From Scratch
3. Name: "Website Bot"
4. Add Bot Token Scopes:
   - `app_mentions:read`
   - `chat:write`
   - `channels:history`
5. Install to Workspace
6. Copy Bot User OAuth Token

### Step 4: Payload CMS API Key

1. Go to `louiebernstein.com/admin`
2. Settings → API Keys (or use your admin credentials)
3. Create an API key for automation
4. Save the key securely

---

## Activepieces Workflows

### Flow 1: Update Site Settings

**Trigger:** Slack - New Message in Channel
**Filter:** Message contains "@website update"

**Steps:**
1. **Parse Command** (Code step)
   - Extract: field path, new value
   - Example: "update hero tagline to X" → {path: "hero.tagline", value: "X"}

2. **HTTP Request** to Payload API
   - Method: PATCH
   - URL: `https://louiebernstein.com/api/globals/site-settings`
   - Headers: Authorization with API key
   - Body: Parsed update

3. **Slack Reply**
   - "✅ Updated {field}! Live in ~60 seconds."

---

### Flow 2: Add Testimonial

**Trigger:** Slack - Message contains "@website add testimonial"

**Steps:**
1. **Parse Testimonial** (Code step)
   - Extract: quote, author, role, company

2. **HTTP Request** - POST to Payload
   - URL: `https://louiebernstein.com/api/testimonials`
   - Body: { quote, author, role, company }

3. **Slack Reply**
   - "✅ Added testimonial from {author}!"

---

### Flow 3: VoiceCraft Content Generation

**Trigger:** Slack - Message contains "@voicecraft"

**Steps:**
1. **Parse Request** (Code step)
   - Extract: content type (article/newsletter), topic

2. **Call VoiceCraft API** (HTTP or custom)
   - Generate content in Louie's voice

3. **Create Draft in Payload**
   - POST to `/api/articles` with status: "draft"

4. **Slack Reply**
   - "📝 Draft created: {title}\nReview: louiebernstein.com/admin/articles/{id}"

---

## Code: Command Parser

Use this in Activepieces "Code" step:

```javascript
// Parse Slack commands for CMS updates
function parseCommand(message) {
  const text = message.toLowerCase();
  
  // Update command: "@website update {field} to {value}"
  const updateMatch = text.match(/@website\s+update\s+(.+?)\s+to\s+["']?(.+?)["']?$/i);
  if (updateMatch) {
    return {
      action: 'update',
      field: updateMatch[1].trim(),
      value: updateMatch[2].trim()
    };
  }
  
  // Add testimonial: "@website add testimonial "quote" - Author, Role at Company"
  const testimonialMatch = text.match(/@website\s+add\s+testimonial\s+["'](.+?)["']\s*[-–]\s*(.+)/i);
  if (testimonialMatch) {
    const [author, roleCompany] = testimonialMatch[2].split(/,\s*at\s*/i);
    return {
      action: 'add_testimonial',
      quote: testimonialMatch[1],
      author: author?.trim(),
      company: roleCompany?.trim()
    };
  }
  
  // VoiceCraft: "@voicecraft write article about {topic}"
  const voicecraftMatch = text.match(/@voicecraft\s+(write|draft)\s+(article|newsletter|post)\s+about\s+(.+)/i);
  if (voicecraftMatch) {
    return {
      action: 'voicecraft',
      type: voicecraftMatch[2],
      topic: voicecraftMatch[3].trim()
    };
  }
  
  return { action: 'unknown', original: message };
}

// Map friendly field names to Payload paths
const fieldMappings = {
  'hero tagline': 'hero.tagline',
  'hero headline': 'hero.headline',
  'hero description': 'hero.description',
  'newsletter description': 'newsletterPage.description',
  'newsletter headline': 'newsletterPage.headline',
  'newsletter tagline': 'newsletterPage.tagline',
  'cta text': 'newsletterPage.ctaText',
  // Add more as needed
};

function getPayloadPath(friendlyName) {
  return fieldMappings[friendlyName.toLowerCase()] || friendlyName;
}
```

---

## Payload API Reference

### Update Global Settings
```bash
PATCH https://louiebernstein.com/api/globals/site-settings
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "hero": {
    "tagline": "New Tagline Here"
  }
}
```

### Add Testimonial
```bash
POST https://louiebernstein.com/api/testimonials
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "quote": "Great results!",
  "author": "John Smith",
  "role": "CEO",
  "company": "Acme Inc",
  "featured": true
}
```

### Create Article Draft
```bash
POST https://louiebernstein.com/api/articles
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "title": "Cold Email Mistakes to Avoid",
  "slug": "cold-email-mistakes",
  "content": "Article content here...",
  "status": "draft"
}
```

---

## Testing

1. In Slack, send: `@website update newsletter tagline to "Start Your Week Strong"`
2. Check Activepieces logs for flow execution
3. Verify change at `louiebernstein.com/newsletter`

---

## Security Notes

- API keys stored securely in Activepieces (encrypted)
- Limit Slack commands to specific channels
- Add user allowlist if needed (only Louie can trigger updates)
- All changes logged in Activepieces for audit trail

---

## Next Steps

1. [ ] Set up Activepieces Slack connection
2. [ ] Create Payload API key
3. [ ] Build "Update Settings" flow
4. [ ] Test with simple command
5. [ ] Add more flows (testimonials, articles, etc.)
6. [ ] Integrate VoiceCraft for AI content generation



