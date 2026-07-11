# robots.txt File

## What This Is
This file tells AI crawlers (ChatGPT, Claude, Perplexity, Google AI) which parts of your website they're allowed to read. This version is **optimized for AI** - it explicitly invites AI systems to crawl your content.

## Where to Add This
Upload this file to the **root** of your website so it's accessible at: `http://louiebernstein.com/robots.txt`

## The File Content

```
# robots.txt for Louie Bernstein
# Optimized for AI crawlers (ChatGPT, Claude, Perplexity, Google AI)

User-agent: *
Allow: /

# AI Crawlers - Explicitly allow
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: CCBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Googlebot
Allow: /

# Sitemap
Sitemap: http://louiebernstein.com/sitemap.xml
```

## How to Add It

### Step 1: Check If You Already Have One
1. Visit `http://louiebernstein.com/robots.txt` in your browser
2. If you see a file, download it first (backup)
3. If you see a 404 error, you don't have one yet

### Step 2: Create/Update the File
1. Copy the content above (everything between the ``` markers)
2. Create a new text file called `robots.txt`
3. Paste the content into it
4. Save it

### Step 3: Upload to Your Website
1. Log into your website hosting (cPanel, FTP, or your hosting dashboard)
2. Navigate to the **root directory** (usually `public_html` or `www`)
3. Upload `robots.txt` to the root (replace existing if you have one)
4. Test it by visiting: `http://louiebernstein.com/robots.txt`

### If You Use WordPress:
- Use an FTP client or File Manager in cPanel
- Upload to the root directory (same level as `wp-config.php`)
- Or use a plugin like "Yoast SEO" which has a robots.txt editor

### If You Use a Website Builder:
- Most builders have a "File Manager" or "Upload Files" option
- Upload to the root/public directory

## Why This Matters
Many websites accidentally block AI crawlers. This file **explicitly invites** AI systems to read your content, which is critical for getting cited in AI answers. Without this, AI might not be able to access your content at all.

## Important Notes
- **If you already have a robots.txt:** Review it first - you may need to merge this with your existing rules
- **Sitemap:** Make sure you have a sitemap.xml file (or update the Sitemap line to match your actual sitemap URL)
- **Test:** After uploading, visit `http://louiebernstein.com/robots.txt` - you should see the file contents

## What Each Section Does
- `User-agent: *` - Applies to all crawlers
- `Allow: /` - Allows access to everything
- The specific AI crawler sections explicitly invite ChatGPT, Claude, Perplexity, etc.
- `Sitemap:` - Tells crawlers where to find your sitemap


