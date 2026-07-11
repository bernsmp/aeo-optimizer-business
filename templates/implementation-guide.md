# AEO Implementation Guide: {{client_name}}

## Quick Start Checklist
- [ ] Add Organization schema to site header
- [ ] Add FAQ schema to relevant pages
- [ ] Create/update robots.txt
- [ ] Create llms.txt
- [ ] Add Service schema
- [ ] Implement FAQ content sections
- [ ] Submit sitemap

## Step 1: Schema Implementation
### Organization Schema
Copy this code into your site's header (or Yoast/RankMath custom scripts):
{{organization_schema}}

### FAQ Schema
Add to pages with FAQ content:
{{faq_schema}}

### Service Schema
Add to service pages:
{{service_schema}}

## Step 2: AI Crawler Access
### robots.txt
Replace your current robots.txt with:
{{robots_txt}}

### llms.txt
Create a new file at yourdomain.com/llms.txt:
{{llms_txt}}

## Step 3: Content Optimization
### FAQ Content
Add these FAQ sections to your site:
{{faq_content}}

## Step 4: Verification
After implementing, run /score-site to verify improvements.
Expected score improvement: {{expected_improvement}}
