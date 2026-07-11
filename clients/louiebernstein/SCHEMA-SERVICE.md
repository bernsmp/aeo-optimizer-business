# Service Schema Markup

## What This Is
This tells AI systems what services you offer. When people ask AI "What is fractional sales leadership?" or "Who provides sales consulting?", AI can recommend your services.

## Where to Add This
Add this to your homepage or services page, in the `<head>` section or just before the closing `</body>` tag.

## The Code

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Fractional Sales Leadership",
  "description": "Louie Bernstein provides fractional sales leadership and consulting services to organize, optimize, and train sales teams. He helps drive sales results for clients.",
  "serviceType": "Sales consulting",
  "provider": {
    "@type": "Person",
    "name": "Louie Bernstein"
  },
  "areaServed": {
    "@type": "Place",
    "name": "Worldwide"
  }
}
</script>
```

## How to Add It
Same as Organization Schema - add to your homepage `<head>` section or use a plugin if you're on WordPress.

## Why This Matters
This helps AI understand exactly what you do, making it more likely that AI will recommend your services when people ask relevant questions.


