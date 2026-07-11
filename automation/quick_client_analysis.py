"""
Quick Client Analysis - Core Package Deliverables
Generates all core deliverables for a client without dashboard.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from firecrawl import FirecrawlApp
from config import FIRECRAWL_API_KEY, CLAUDE_API_KEY
from anthropic import Anthropic

class QuickClientAnalysis:
    """Generate core AEO deliverables for a client."""
    
    def __init__(self, website_url: str, client_name: str, industry: str, output_dir: str):
        self.website_url = website_url
        self.client_name = client_name
        self.industry = industry
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
        self.claude = Anthropic(api_key=CLAUDE_API_KEY)
        
        self.site_data = {}
    
    def scrape_homepage(self):
        """Scrape homepage to understand site structure."""
        print(f"🔍 Scraping homepage: {self.website_url}")
        try:
            result = self.firecrawl.scrape(self.website_url)
            
            if hasattr(result, 'markdown'):
                markdown = result.markdown or ''
                title = ''
                if hasattr(result, 'metadata') and result.metadata:
                    title = getattr(result.metadata, 'title', '') or getattr(result.metadata, 'og_title', '')
                html = result.html or result.raw_html or ''
            else:
                markdown = result.get('markdown', '') if isinstance(result, dict) else str(result)
                title = result.get('title', '') if isinstance(result, dict) else ''
                html = result.get('html', '') if isinstance(result, dict) else ''
            
            self.site_data = {
                'url': self.website_url,
                'title': title,
                'markdown': markdown,
                'html': html,
                'scraped_at': datetime.now().isoformat()
            }
            
            print(f"✅ Scraped {len(markdown)} characters")
            return True
        except Exception as e:
            print(f"❌ Error scraping: {e}")
            return False
    
    def generate_aeo_score_analysis(self):
        """Generate AEO score analysis."""
        print("\n📊 Generating AEO Score Analysis...")
        
        prompt = f"""Analyze the AEO (Answer Engine Optimization) score for this website:

Website: {self.website_url}
Client: {self.client_name}
Industry: {self.industry}

Site Content:
{self.site_data.get('markdown', '')[:2000]}

Evaluate the site on these AEO factors (0-100 scale):
1. Technical Foundation (schemas, robots.txt, llms.txt)
2. Content Structure (headings, FAQs, clear information)
3. AI Crawler Access (robots.txt, sitemap)
4. Schema Markup (Organization, Service, FAQ)
5. Content Quality (clarity, depth, value)

Provide:
- Overall AEO Score (0-100)
- Breakdown by category
- Top 5 priority fixes
- Gap analysis

Format as markdown report."""

        try:
            response = self.claude.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            
            output_file = self.output_dir / "aeo-score-analysis.md"
            output_file.write_text(content)
            print(f"✅ Saved: {output_file}")
            return content
        except Exception as e:
            print(f"❌ Error generating AEO score: {e}")
            return None
    
    def generate_schemas(self):
        """Generate schema markup files."""
        print("\n🏗️  Generating Schema Markup...")
        
        schemas = {
            'organization': self._generate_organization_schema(),
            'service': self._generate_service_schema(),
            'faq': self._generate_faq_schema()
        }
        
        for schema_type, content in schemas.items():
            if content:
                output_file = self.output_dir / f"schema-{schema_type}.html"
                output_file.write_text(content)
                print(f"✅ Saved: schema-{schema_type}.html")
        
        return schemas
    
    def _generate_organization_schema(self):
        """Generate Organization schema."""
        prompt = f"""Create JSON-LD Organization schema markup for:

Business: {self.client_name}
Website: {self.website_url}
Industry: {self.industry}

Based on the site content:
{self.site_data.get('markdown', '')[:1500]}

Include:
- Business name
- Website URL
- Description
- Contact information (if available)
- Logo (if available)
- SameAs (social media links if mentioned)

Output ONLY valid JSON-LD schema markup, wrapped in <script type="application/ld+json"> tags."""

        try:
            response = self.claude.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"❌ Error generating Organization schema: {e}")
            return None
    
    def _generate_service_schema(self):
        """Generate Service schema."""
        prompt = f"""Create JSON-LD Service schema markup for:

Business: {self.client_name}
Services: Fractional Sales Leadership / Sales Consulting
Industry: {self.industry}

Based on the site content:
{self.site_data.get('markdown', '')[:1500]}

Include:
- Service name
- Description
- Service type
- Provider (organization)
- Area served
- Price range (if mentioned)

Output ONLY valid JSON-LD schema markup, wrapped in <script type="application/ld+json"> tags."""

        try:
            response = self.claude.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"❌ Error generating Service schema: {e}")
            return None
    
    def _generate_faq_schema(self):
        """Generate FAQ schema."""
        prompt = f"""Create JSON-LD FAQPage schema markup with 10-15 relevant FAQs for:

Business: {self.client_name}
Services: Fractional Sales Leadership
Industry: {self.industry}

Based on the site content:
{self.site_data.get('markdown', '')[:1500]}

Create FAQs that potential clients would ask about:
- What is fractional sales leadership?
- How does it work?
- Who is it for?
- Pricing/cost
- Time commitment
- Results/outcomes
- Process/methodology

Output ONLY valid JSON-LD schema markup, wrapped in <script type="application/ld+json"> tags."""

        try:
            response = self.claude.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"❌ Error generating FAQ schema: {e}")
            return None
    
    def generate_llms_txt(self):
        """Generate llms.txt file."""
        print("\n📄 Generating llms.txt...")
        
        prompt = f"""Create an llms.txt file for AI crawlers for:

Website: {self.website_url}
Business: {self.client_name}
Industry: {self.industry}

Site content:
{self.site_data.get('markdown', '')[:1500]}

Include:
- Site information
- Key pages
- Business description
- Services offered
- Contact information
- Important facts about the business

Format as llms.txt (see llms.txt specification)."""

        try:
            response = self.claude.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            output_file = self.output_dir / "llms.txt"
            output_file.write_text(content)
            print(f"✅ Saved: llms.txt")
            return content
        except Exception as e:
            print(f"❌ Error generating llms.txt: {e}")
            return None
    
    def generate_robots_txt(self):
        """Generate robots.txt optimized for AI crawlers."""
        print("\n🤖 Generating robots.txt...")
        
        content = f"""# robots.txt for {self.client_name}
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
Sitemap: {self.website_url}/sitemap.xml
"""

        output_file = self.output_dir / "robots.txt"
        output_file.write_text(content)
        print(f"✅ Saved: robots.txt")
        return content
    
    def generate_implementation_guide(self):
        """Generate implementation guide."""
        print("\n📖 Generating Implementation Guide...")
        
        prompt = f"""Create a comprehensive implementation guide for AEO optimization for:

Website: {self.website_url}
Business: {self.client_name}
Industry: {self.industry}

The guide should include:
1. How to add schema markup (Organization, Service, FAQ)
2. How to add llms.txt file
3. How to update robots.txt
4. How to optimize content for AI platforms
5. Step-by-step instructions for common platforms (WordPress, Shopify, custom HTML)

Make it practical and easy to follow for non-technical users.

Format as markdown."""

        try:
            response = self.claude.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            output_file = self.output_dir / "implementation-guide.md"
            output_file.write_text(content)
            print(f"✅ Saved: implementation-guide.md")
            return content
        except Exception as e:
            print(f"❌ Error generating implementation guide: {e}")
            return None
    
    def generate_content_strategy(self):
        """Generate content strategy."""
        print("\n📝 Generating Content Strategy...")
        
        prompt = f"""Create a content strategy for AEO optimization for:

Business: {self.client_name}
Services: Fractional Sales Leadership
Industry: {self.industry}
Target Audience: CEOs/Founders of $1M-$10M ARR companies

Based on the site:
{self.site_data.get('markdown', '')[:1500]}

Create:
1. Topic clusters (3-5 main topics)
2. Content ideas (10-15 article/blog topics)
3. FAQ topics to cover
4. Content calendar suggestions
5. Platform-specific optimization tips

Focus on topics that would help CEOs/founders understand:
- Fractional sales leadership
- Sales team building
- Sales process optimization
- When to hire fractional vs full-time

Format as markdown."""

        try:
            response = self.claude.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            output_file = self.output_dir / "content-strategy.md"
            output_file.write_text(content)
            print(f"✅ Saved: content-strategy.md")
            return content
        except Exception as e:
            print(f"❌ Error generating content strategy: {e}")
            return None
    
    def run_full_analysis(self):
        """Run complete analysis and generate all deliverables."""
        print(f"\n🚀 Starting AEO Analysis for {self.client_name}")
        print(f"Website: {self.website_url}")
        print("=" * 60)
        
        # Step 1: Scrape homepage
        if not self.scrape_homepage():
            print("❌ Failed to scrape homepage. Cannot continue.")
            return False
        
        # Step 2: Generate all deliverables
        self.generate_aeo_score_analysis()
        self.generate_schemas()
        self.generate_llms_txt()
        self.generate_robots_txt()
        self.generate_implementation_guide()
        self.generate_content_strategy()
        
        print("\n" + "=" * 60)
        print("✅ Analysis Complete!")
        print(f"📁 All files saved to: {self.output_dir}")
        print("\nGenerated Files:")
        for file in sorted(self.output_dir.glob("*")):
            print(f"  - {file.name}")
        
        return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python3 quick_client_analysis.py <website_url> <client_name> <industry> [output_dir]")
        print("\nExample:")
        print("  python3 quick_client_analysis.py http://louiebernstein.com 'Louie Bernstein' 'Sales Consulting' ../clients/louiebernstein")
        sys.exit(1)
    
    website_url = sys.argv[1]
    client_name = sys.argv[2]
    industry = sys.argv[3]
    output_dir = sys.argv[4] if len(sys.argv) > 4 else f"../clients/{client_name.lower().replace(' ', '')}"
    
    analyzer = QuickClientAnalysis(website_url, client_name, industry, output_dir)
    analyzer.run_full_analysis()

