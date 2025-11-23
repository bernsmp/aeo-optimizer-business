# Organization Schema Markup

## What This Is
This is structured data that tells AI systems (like ChatGPT, Claude, Perplexity) who your business is - your name, contact info, and what you do. Think of it like a digital business card that AI can read.

## Where to Add This
Add this code to your website's homepage, typically in the `<head>` section or just before the closing `</body>` tag.

## The Code

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Louie Bernstein",
  "url": "http://louiebernstein.com",
  "description": "Louie Bernstein provides fractional sales leadership consulting to organize, optimize and train sales teams. Less spend, more sales.",
  "logo": "https://d1yei2z3i6k35z.cloudfront.net/1671832/64e3c2e5505e3_fourawards.png",
  "email": "Louie@LouieBernstein.com",
  "telephone": "(404)808-5326",
  "industry": "Sales Consulting",
  "sameAs": [
    "https://www.linkedin.com/in/sales-processes/",
    "https://www.youtube.com/playlist?list=PL7HfhnqHyzRmGDUMDhcSgZW8pR7DhW_Hl"
  ]
}
</script>
```

## How to Add It

### If you have access to your website's HTML:
1. Open your homepage HTML file
2. Find the `<head>` section (near the top)
3. Paste the code above just before `</head>`
4. Save and upload

### If you use WordPress:
1. Go to Appearance → Theme Editor
2. Edit `header.php`
3. Paste the code before `</head>`
4. Or use a plugin like "Schema" or "Schema Pro"

### If you use a website builder (Wix, Squarespace, etc.):
- Look for "Custom Code" or "HTML Code" section
- Add it to the header/footer custom code area

## Why This Matters
When someone asks AI "Who is Louie Bernstein?" or "What does Louie Bernstein do?", AI can find and share this verified information, increasing your visibility and credibility.


