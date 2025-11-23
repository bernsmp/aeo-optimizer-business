#!/usr/bin/env python3
"""
Scrape Louie Bernstein's current website to extract all content.
This will be used to rebuild the site on Vercel with proper AEO optimization.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from firecrawl import FirecrawlApp
from config import FIRECRAWL_API_KEY

class LouieBernsteinSiteScraper:
    """Scrape and organize Louie Bernstein's website content."""
    
    def __init__(self):
        self.firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
        self.base_url = "http://louiebernstein.com"
        self.output_dir = Path("../clients/louiebernstein/scraped-content")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.scraped_pages = []
        self.site_structure = {
            'homepage': None,
            'pages': [],
            'sections': {},
            'navigation': [],
            'content': {}
        }
    
    def scrape_homepage(self):
        """Scrape the homepage."""
        print(f"\n{'='*70}")
        print(f"🏠 Scraping Homepage: {self.base_url}")
        print(f"{'='*70}\n")
        
        try:
            result = self.firecrawl.scrape(self.base_url)
            
            # Handle Firecrawl response
            if hasattr(result, 'markdown'):
                markdown = result.markdown or ''
                html = result.html or result.raw_html or ''
                title = ''
                if hasattr(result, 'metadata') and result.metadata:
                    title = getattr(result.metadata, 'title', '') or getattr(result.metadata, 'og_title', '')
                if not title and hasattr(result, 'title'):
                    title = result.title
                metadata = {
                    'title': title,
                    'url': getattr(result.metadata, 'url', self.base_url) if hasattr(result, 'metadata') and result.metadata else self.base_url,
                    'description': getattr(result.metadata, 'description', '') if hasattr(result, 'metadata') and result.metadata else ''
                }
            elif isinstance(result, dict):
                markdown = result.get('markdown', '')
                html = result.get('html', result.get('content', ''))
                title = result.get('title', result.get('metadata', {}).get('title', ''))
                metadata = result.get('metadata', {})
            else:
                markdown = str(result)
                html = ''
                title = ''
                metadata = {}
            
            homepage_data = {
                'url': self.base_url,
                'title': title or 'Louie Bernstein - Fractional Sales Leadership',
                'markdown': markdown,
                'html': html,
                'metadata': metadata if isinstance(metadata, dict) else {},
                'scraped_at': datetime.now().isoformat()
            }
            
            # Save homepage
            homepage_file = self.output_dir / "homepage.json"
            with open(homepage_file, 'w', encoding='utf-8') as f:
                json.dump(homepage_data, f, indent=2, ensure_ascii=False)
            
            # Save markdown version
            homepage_md = self.output_dir / "homepage.md"
            with open(homepage_md, 'w', encoding='utf-8') as f:
                f.write(f"# {title or 'Homepage'}\n\n")
                f.write(f"**URL:** {self.base_url}\n\n")
                f.write(f"**Scraped:** {datetime.now().isoformat()}\n\n")
                f.write("---\n\n")
                f.write(markdown)
            
            self.site_structure['homepage'] = homepage_data
            self.scraped_pages.append(homepage_data)
            
            print(f"✅ Homepage scraped: {len(markdown)} characters")
            print(f"   Title: {title}")
            print(f"   Saved to: {homepage_file}")
            
            return homepage_data
            
        except Exception as e:
            print(f"❌ Error scraping homepage: {e}")
            return None
    
    def crawl_site(self):
        """Crawl the entire site to find all pages."""
        print(f"\n{'='*70}")
        print(f"🕷️  Crawling Site: {self.base_url}")
        print(f"{'='*70}\n")
        
        try:
            # Use Firecrawl's crawl feature to discover all pages
            crawl_result = self.firecrawl.crawl_url(
                self.base_url,
                {'limit': 50}  # Limit to 50 pages max
            )
            
            if crawl_result:
                print(f"✅ Found pages to scrape")
                return crawl_result
            else:
                print("⚠️  No pages found via crawl, will scrape homepage only")
                return None
                
        except Exception as e:
            print(f"⚠️  Crawl not available or failed: {e}")
            print("   Will scrape homepage and try to extract links manually")
            return None
    
    def scrape_url(self, url: str):
        """Scrape a single URL."""
        if url in [p['url'] for p in self.scraped_pages]:
            print(f"⏭️  Already scraped: {url}")
            return None
        
        print(f"🔍 Scraping: {url}")
        
        try:
            result = self.firecrawl.scrape(url)
            
            # Handle Firecrawl response
            if hasattr(result, 'markdown'):
                markdown = result.markdown or ''
                html = result.html or result.raw_html or ''
                title = ''
                if hasattr(result, 'metadata') and result.metadata:
                    title = getattr(result.metadata, 'title', '') or getattr(result.metadata, 'og_title', '')
                if not title and hasattr(result, 'title'):
                    title = result.title
                metadata = {
                    'title': title,
                    'url': getattr(result.metadata, 'url', url) if hasattr(result, 'metadata') and result.metadata else url,
                    'description': getattr(result.metadata, 'description', '') if hasattr(result, 'metadata') and result.metadata else ''
                }
            elif isinstance(result, dict):
                markdown = result.get('markdown', '')
                html = result.get('html', result.get('content', ''))
                title = result.get('title', result.get('metadata', {}).get('title', ''))
                metadata = result.get('metadata', {})
            else:
                markdown = str(result)
                html = ''
                title = ''
                metadata = {}
            
            page_data = {
                'url': url,
                'title': title or url.split('/')[-1],
                'markdown': markdown,
                'html': html,
                'metadata': metadata if isinstance(metadata, dict) else {},
                'scraped_at': datetime.now().isoformat()
            }
            
            self.scraped_pages.append(page_data)
            print(f"   ✅ Scraped: {title or url} ({len(markdown)} chars)")
            
            return page_data
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def extract_links_from_html(self, html: str):
        """Extract internal links from HTML."""
        from bs4 import BeautifulSoup
        
        links = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                # Convert relative URLs to absolute
                if href.startswith('/'):
                    full_url = f"{self.base_url}{href}"
                elif href.startswith('http://louiebernstein.com') or href.startswith('https://louiebernstein.com'):
                    full_url = href.replace('https://', 'http://')
                elif not href.startswith('http'):
                    continue
                else:
                    continue
                
                # Avoid duplicates and external links
                if full_url not in links and 'louiebernstein.com' in full_url:
                    links.append(full_url)
        except Exception as e:
            print(f"⚠️  Error extracting links: {e}")
        
        return links
    
    def scrape_all_pages(self):
        """Scrape homepage and discover/scrape all other pages."""
        # Scrape homepage first
        homepage = self.scrape_homepage()
        
        if homepage:
            # Extract links from homepage HTML
            links = self.extract_links_from_html(homepage.get('html', ''))
            
            print(f"\n📋 Found {len(links)} internal links")
            
            # Scrape each discovered page
            for link in links[:20]:  # Limit to 20 pages
                page_data = self.scrape_url(link)
                if page_data:
                    # Extract more links from this page
                    more_links = self.extract_links_from_html(page_data.get('html', ''))
                    for new_link in more_links:
                        if new_link not in links:
                            links.append(new_link)
        
        return self.scraped_pages
    
    def organize_content(self):
        """Organize scraped content into a structure for Claude Code."""
        print(f"\n{'='*70}")
        print(f"📦 Organizing Content")
        print(f"{'='*70}\n")
        
        organized = {
            'site_info': {
                'domain': 'louiebernstein.com',
                'base_url': self.base_url,
                'scraped_at': datetime.now().isoformat(),
                'total_pages': len(self.scraped_pages)
            },
            'homepage': None,
            'pages': [],
            'sections': {},
            'content_summary': {}
        }
        
        # Organize homepage
        for page in self.scraped_pages:
            if page['url'] == self.base_url or page['url'] == self.base_url + '/':
                organized['homepage'] = {
                    'title': page.get('title', 'Homepage'),
                    'content': page.get('markdown', ''),
                    'metadata': page.get('metadata', {})
                }
            else:
                organized['pages'].append({
                    'url': page['url'],
                    'title': page.get('title', 'Untitled'),
                    'content': page.get('markdown', ''),
                    'metadata': page.get('metadata', {})
                })
        
        # Extract key sections from homepage
        if organized['homepage']:
            homepage_content = organized['homepage']['content']
            
            # Try to identify sections (this is basic - Claude Code can refine)
            organized['sections'] = {
                'hero': 'Extract hero section content',
                'about': 'Extract about section',
                'services': 'Extract services section',
                'testimonials': 'Extract testimonials',
                'contact': 'Extract contact information',
                'cta': 'Extract call-to-action'
            }
        
        # Save organized structure
        organized_file = self.output_dir / "organized-content.json"
        with open(organized_file, 'w', encoding='utf-8') as f:
            json.dump(organized, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Content organized")
        print(f"   Total pages: {len(self.scraped_pages)}")
        print(f"   Saved to: {organized_file}")
        
        return organized
    
    def create_build_guide(self):
        """Create a guide for Claude Code to build the new site."""
        print(f"\n{'='*70}")
        print(f"📝 Creating Build Guide for Claude Code")
        print(f"{'='*70}\n")
        
        guide = f"""# Louie Bernstein Website Rebuild Guide

## Overview
Rebuild Louie Bernstein's website from {self.base_url} to a modern, AEO-optimized site on Vercel.

## Current Site Analysis
- **Total Pages Scraped:** {len(self.scraped_pages)}
- **Scraped Content Location:** `clients/louiebernstein/scraped-content/`
- **Homepage:** `homepage.json` and `homepage.md`
- **All Pages:** `organized-content.json`

## Content Structure

### Homepage Content
Located in: `scraped-content/homepage.json`

### Additional Pages
Located in: `scraped-content/organized-content.json`

## Build Requirements

### 1. Technology Stack
- **Framework:** Next.js 14+ (App Router)
- **Styling:** Tailwind CSS
- **Deployment:** Vercel
- **Type:** Static site generation (SSG) or Server Components

### 2. AEO Optimization Requirements
- ✅ Schema markup (Organization, Service, FAQPage)
- ✅ robots.txt optimized for AI crawlers
- ✅ llms.txt file
- ✅ Semantic HTML structure
- ✅ Clear heading hierarchy (H1, H2, H3)
- ✅ FAQ sections with FAQPage schema
- ✅ Fast loading (<3 seconds)
- ✅ Mobile-responsive design

### 3. Design Requirements
- Modern, professional design
- Clean, easy to navigate
- Mobile-first responsive
- Fast loading
- Accessible (WCAG 2.1 AA)

### 4. Content Pages Needed
Based on scraped content, create:
- Homepage (main landing page)
- About/Services page
- Contact page
- Any other pages found in scraped content

### 5. Key Sections (from scraped content)
Extract and organize:
- Hero section
- About section
- Services section
- Testimonials (if any)
- Contact information
- Call-to-action sections

## File Structure

```
clients/louiebernstein/
├── scraped-content/          # Original scraped content
│   ├── homepage.json
│   ├── homepage.md
│   └── organized-content.json
├── website/                  # New Next.js site (to be created)
│   ├── app/
│   │   ├── page.tsx         # Homepage
│   │   ├── about/page.tsx    # About page
│   │   ├── contact/page.tsx  # Contact page
│   │   └── layout.tsx
│   ├── components/
│   ├── public/
│   └── package.json
└── vercel.json               # Vercel config
```

## Next Steps for Claude Code

1. **Read Scraped Content:**
   - Read `scraped-content/homepage.json`
   - Read `scraped-content/organized-content.json`

2. **Create Next.js Project:**
   - Initialize Next.js 14+ with TypeScript
   - Set up Tailwind CSS
   - Create basic file structure

3. **Build Pages:**
   - Homepage with hero, about, services, contact sections
   - About page (if separate)
   - Contact page

4. **Add AEO Optimization:**
   - Add schema markup to layout.tsx
   - Create robots.txt
   - Create llms.txt
   - Optimize meta tags

5. **Style & Polish:**
   - Modern, professional design
   - Mobile-responsive
   - Fast loading

6. **Deploy:**
   - Set up Vercel project
   - Deploy and test

## Content Sources
All content is in: `clients/louiebernstein/scraped-content/`

## AEO Deliverables Already Created
- Schema markup files (Organization, Service, FAQ)
- robots.txt
- llms.txt
- Content strategy
- Competitor analysis

These are in: `clients/louiebernstein/`

## Questions for Claude Code
1. What sections should be on the homepage?
2. How should we organize the content?
3. What design style should we use?
4. Should we create separate pages or single-page site?

---
**Created:** {datetime.now().isoformat()}
**Total Pages Scraped:** {len(self.scraped_pages)}
"""
        
        guide_file = self.output_dir / "BUILD-GUIDE.md"
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide)
        
        print(f"✅ Build guide created: {guide_file}")
        
        return guide_file
    
    def run(self):
        """Run the complete scraping and organization process."""
        print(f"\n{'='*70}")
        print(f"🚀 Starting Louie Bernstein Site Scrape")
        print(f"{'='*70}\n")
        
        # Scrape all pages
        pages = self.scrape_all_pages()
        
        # Save all pages
        all_pages_file = self.output_dir / "all-pages.json"
        with open(all_pages_file, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_pages, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ All pages saved to: {all_pages_file}")
        
        # Organize content
        organized = self.organize_content()
        
        # Create build guide
        guide = self.create_build_guide()
        
        # Summary
        print(f"\n{'='*70}")
        print(f"✅ Scraping Complete!")
        print(f"{'='*70}\n")
        print(f"📊 Summary:")
        print(f"   Total pages scraped: {len(self.scraped_pages)}")
        print(f"   Output directory: {self.output_dir}")
        print(f"   Build guide: {guide}")
        print(f"\n📁 Files created:")
        print(f"   - homepage.json")
        print(f"   - homepage.md")
        print(f"   - all-pages.json")
        print(f"   - organized-content.json")
        print(f"   - BUILD-GUIDE.md")
        print(f"\n🎯 Next Step: Review scraped content, then use Claude Code to build!")
        
        return organized

if __name__ == "__main__":
    scraper = LouieBernsteinSiteScraper()
    scraper.run()


