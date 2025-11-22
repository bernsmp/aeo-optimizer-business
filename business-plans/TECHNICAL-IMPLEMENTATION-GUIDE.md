# Technical Implementation Guide
## Building the AEO Optimization Platform

---

## Shared Core Components (Both Options)

### 1. Website Analysis Engine

```python
# core/analyzer.py
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json
from typing import Dict, List, Optional

class WebsiteAnalyzer:
    def __init__(self, url: str):
        self.url = url
        self.content = {}
        self.schemas = []
        self.meta_data = {}

    async def analyze(self) -> Dict:
        """Complete website analysis pipeline"""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Fetch page
            await page.goto(self.url, wait_until='networkidle')

            # Extract content
            html = await page.content()
            self.content = self._parse_content(html)

            # Extract schemas
            self.schemas = await self._extract_schemas(page)

            # Extract meta
            self.meta_data = await self._extract_meta(page)

            # Calculate AEO score
            aeo_score = self._calculate_aeo_score()

            await browser.close()

        return {
            'url': self.url,
            'content': self.content,
            'schemas': self.schemas,
            'meta': self.meta_data,
            'aeo_score': aeo_score,
            'recommendations': self._generate_recommendations()
        }

    def _parse_content(self, html: str) -> Dict:
        """Extract content structure"""
        soup = BeautifulSoup(html, 'html.parser')

        return {
            'title': soup.find('title').text if soup.find('title') else '',
            'h1': [h.text for h in soup.find_all('h1')],
            'h2': [h.text for h in soup.find_all('h2')],
            'paragraphs': len(soup.find_all('p')),
            'images': len(soup.find_all('img')),
            'images_without_alt': len([img for img in soup.find_all('img') if not img.get('alt')]),
            'links': len(soup.find_all('a')),
            'forms': len(soup.find_all('form'))
        }

    async def _extract_schemas(self, page) -> List[Dict]:
        """Extract JSON-LD schemas"""
        schemas = await page.evaluate('''
            () => {
                const scripts = document.querySelectorAll('script[type="application/ld+json"]');
                return Array.from(scripts).map(script => {
                    try {
                        return JSON.parse(script.textContent);
                    } catch {
                        return null;
                    }
                }).filter(Boolean);
            }
        ''')
        return schemas

    async def _extract_meta(self, page) -> Dict:
        """Extract meta tags"""
        meta = await page.evaluate('''
            () => {
                const metas = document.querySelectorAll('meta');
                const result = {};
                metas.forEach(meta => {
                    const name = meta.getAttribute('name') || meta.getAttribute('property');
                    const content = meta.getAttribute('content');
                    if (name && content) {
                        result[name] = content;
                    }
                });
                return result;
            }
        ''')
        return meta

    def _calculate_aeo_score(self) -> int:
        """Calculate AEO readiness score"""
        score = 0
        max_score = 100

        # Schema scoring (40 points)
        if self.schemas:
            score += 10
            schema_types = [s.get('@type') for s in self.schemas if isinstance(s, dict)]
            if 'Organization' in schema_types: score += 10
            if 'WebSite' in schema_types: score += 5
            if 'FAQPage' in schema_types: score += 10
            if any('Article' in str(t) for t in schema_types): score += 5

        # Content structure (30 points)
        if self.content.get('h1'): score += 10
        if len(self.content.get('h2', [])) >= 3: score += 10
        if self.content.get('paragraphs', 0) >= 5: score += 10

        # Accessibility (20 points)
        total_images = self.content.get('images', 1)
        images_without_alt = self.content.get('images_without_alt', 0)
        if total_images > 0:
            alt_ratio = 1 - (images_without_alt / total_images)
            score += int(alt_ratio * 20)

        # Meta data (10 points)
        if self.meta_data.get('description'): score += 5
        if self.meta_data.get('og:title'): score += 5

        return min(score, max_score)

    def _generate_recommendations(self) -> List[str]:
        """Generate specific recommendations"""
        recommendations = []

        # Schema recommendations
        schema_types = [s.get('@type') for s in self.schemas if isinstance(s, dict)]
        if 'FAQPage' not in schema_types:
            recommendations.append("Add FAQPage schema for better answer engine visibility")
        if 'Organization' not in schema_types:
            recommendations.append("Add Organization schema to establish entity")

        # Content recommendations
        if not self.content.get('h1'):
            recommendations.append("Add clear H1 heading")
        if self.content.get('images_without_alt', 0) > 0:
            recommendations.append(f"Add alt text to {self.content['images_without_alt']} images")

        # Meta recommendations
        if not self.meta_data.get('description'):
            recommendations.append("Add meta description")

        return recommendations

# Usage
async def analyze_website(url: str):
    analyzer = WebsiteAnalyzer(url)
    results = await analyzer.analyze()
    return results
```

### 2. Schema Generator

```python
# core/schema_generator.py
from typing import Dict, List, Optional
import json
from datetime import datetime

class SchemaGenerator:
    def __init__(self, website_data: Dict, industry: str = 'general'):
        self.data = website_data
        self.industry = industry

    def generate_organization(self, details: Dict) -> Dict:
        """Generate Organization schema"""
        return {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": details.get('name', ''),
            "url": details.get('url', ''),
            "logo": details.get('logo', ''),
            "description": details.get('description', ''),
            "sameAs": details.get('social_links', []),
            "contactPoint": {
                "@type": "ContactPoint",
                "contactType": "customer service",
                "availableLanguage": "English"
            }
        }

    def generate_website(self, details: Dict) -> Dict:
        """Generate WebSite schema with search action"""
        return {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "url": details.get('url', ''),
            "name": details.get('name', ''),
            "description": details.get('description', ''),
            "potentialAction": {
                "@type": "SearchAction",
                "target": {
                    "@type": "EntryPoint",
                    "urlTemplate": f"{details.get('url', '')}?s={{search_term_string}}"
                },
                "query-input": "required name=search_term_string"
            }
        }

    def generate_faq(self, questions: List[Dict]) -> Dict:
        """Generate FAQPage schema"""
        return {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q['question'],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": q['answer']
                    }
                } for q in questions
            ]
        }

    def generate_article(self, article_data: Dict) -> Dict:
        """Generate Article schema"""
        return {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": article_data.get('title', ''),
            "description": article_data.get('description', ''),
            "image": article_data.get('image', ''),
            "datePublished": article_data.get('date_published', datetime.now().isoformat()),
            "dateModified": article_data.get('date_modified', datetime.now().isoformat()),
            "author": {
                "@type": "Person",
                "name": article_data.get('author', '')
            },
            "publisher": {
                "@type": "Organization",
                "name": article_data.get('publisher', ''),
                "logo": {
                    "@type": "ImageObject",
                    "url": article_data.get('publisher_logo', '')
                }
            }
        }

    def generate_local_business(self, business_data: Dict) -> Dict:
        """Generate LocalBusiness schema"""
        return {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": business_data.get('name', ''),
            "image": business_data.get('image', ''),
            "url": business_data.get('url', ''),
            "telephone": business_data.get('phone', ''),
            "address": {
                "@type": "PostalAddress",
                "streetAddress": business_data.get('street', ''),
                "addressLocality": business_data.get('city', ''),
                "addressRegion": business_data.get('state', ''),
                "postalCode": business_data.get('zip', ''),
                "addressCountry": business_data.get('country', 'US')
            },
            "openingHoursSpecification": business_data.get('hours', [])
        }

    def validate_schema(self, schema: Dict) -> tuple[bool, List[str]]:
        """Validate schema structure"""
        errors = []

        # Check required fields
        if '@context' not in schema:
            errors.append("Missing @context field")
        if '@type' not in schema:
            errors.append("Missing @type field")

        # Validate specific types
        if schema.get('@type') == 'FAQPage':
            if 'mainEntity' not in schema:
                errors.append("FAQPage requires mainEntity field")
            elif not isinstance(schema['mainEntity'], list):
                errors.append("mainEntity must be an array")

        return len(errors) == 0, errors
```

### 3. FAQ Generator with AI

```python
# core/faq_generator.py
import openai
from typing import List, Dict
import json

class FAQGenerator:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.industry_templates = self._load_industry_templates()

    def _load_industry_templates(self) -> Dict:
        """Load industry-specific FAQ templates"""
        return {
            'photography': [
                "What services do you offer?",
                "How much do your services cost?",
                "What is included in a session?",
                "How long does a session take?",
                "When will I receive my photos?"
            ],
            'restaurant': [
                "What are your hours?",
                "Do you take reservations?",
                "Do you offer delivery?",
                "What dietary options do you have?",
                "Do you cater events?"
            ],
            'ecommerce': [
                "What is your return policy?",
                "How long does shipping take?",
                "Do you ship internationally?",
                "What payment methods do you accept?",
                "How do I track my order?"
            ]
            # Add more industries
        }

    async def generate_faqs(self,
                           website_content: str,
                           industry: str = 'general',
                           count: int = 15) -> List[Dict]:
        """Generate industry-specific FAQs using AI"""

        # Get industry template
        template_questions = self.industry_templates.get(industry, [])

        prompt = f"""
        You are an SEO expert creating FAQs for a {industry} website.

        Website content summary:
        {website_content[:2000]}

        Industry template questions to consider:
        {json.dumps(template_questions, indent=2)}

        Generate {count} frequently asked questions and detailed answers that:
        1. Are specific to this business/website
        2. Include relevant keywords naturally
        3. Provide genuine value to visitors
        4. Are optimized for voice search and AI answer engines
        5. Are between 40-150 words each answer

        Return as JSON array with 'question' and 'answer' keys.
        """

        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an SEO and content expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=3000
        )

        faqs = json.loads(response.choices[0].message.content)

        # Validate and clean
        validated_faqs = []
        for faq in faqs:
            if 'question' in faq and 'answer' in faq:
                validated_faqs.append({
                    'question': faq['question'].strip(),
                    'answer': faq['answer'].strip()
                })

        return validated_faqs[:count]

    def customize_for_brand(self, faqs: List[Dict], brand_voice: str) -> List[Dict]:
        """Adjust FAQ answers to match brand voice"""
        # This could use AI to rewrite in brand voice
        # For now, just return as-is
        return faqs
```

---

## Option B: Template Service Implementation

### 1. Order Processing System

```python
# option_b/order_processor.py
from typing import Dict
import stripe
from datetime import datetime
import asyncio
from core.analyzer import WebsiteAnalyzer
from core.schema_generator import SchemaGenerator
from core.faq_generator import FAQGenerator

class OrderProcessor:
    def __init__(self, config: Dict):
        self.config = config
        stripe.api_key = config['stripe_key']
        self.faq_generator = FAQGenerator(config['openai_key'])

    async def process_order(self, order_data: Dict) -> Dict:
        """Process a new order end-to-end"""

        # 1. Create order record
        order_id = self._create_order_record(order_data)

        # 2. Process payment
        payment_status = self._process_payment(order_data)
        if not payment_status['success']:
            return {'error': 'Payment failed', 'details': payment_status}

        # 3. Run analysis
        analysis_results = await self._run_analysis(order_data['url'])

        # 4. Generate deliverables
        deliverables = await self._generate_deliverables(
            analysis_results,
            order_data['industry'],
            order_data['package']
        )

        # 5. Create Google Docs package
        docs_links = self._create_google_docs(deliverables)

        # 6. Send delivery email
        self._send_delivery_email(order_data['email'], docs_links)

        # 7. Schedule follow-ups
        self._schedule_follow_ups(order_id)

        return {
            'success': True,
            'order_id': order_id,
            'delivery_links': docs_links
        }

    def _create_order_record(self, order_data: Dict) -> str:
        """Create order in database"""
        # Implementation for database insert
        pass

    def _process_payment(self, order_data: Dict) -> Dict:
        """Process Stripe payment"""
        try:
            charge = stripe.Charge.create(
                amount=order_data['amount'],
                currency='usd',
                source=order_data['stripe_token'],
                description=f"AEO Package - {order_data['package']}"
            )
            return {'success': True, 'charge_id': charge.id}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def _run_analysis(self, url: str) -> Dict:
        """Run website analysis"""
        analyzer = WebsiteAnalyzer(url)
        return await analyzer.analyze()

    async def _generate_deliverables(self,
                                    analysis: Dict,
                                    industry: str,
                                    package: str) -> Dict:
        """Generate all deliverables based on package"""

        deliverables = {}

        # Generate schemas
        schema_gen = SchemaGenerator(analysis, industry)
        deliverables['schemas'] = {
            'organization': schema_gen.generate_organization(analysis),
            'website': schema_gen.generate_website(analysis)
        }

        # Generate FAQs
        faq_count = 15 if package == 'core' else 30
        deliverables['faqs'] = await self.faq_generator.generate_faqs(
            str(analysis),
            industry,
            faq_count
        )
        deliverables['faq_schema'] = schema_gen.generate_faq(deliverables['faqs'])

        # Generate implementation plan
        deliverables['implementation_plan'] = self._create_implementation_plan(
            analysis,
            industry
        )

        # Add templates if premium/enterprise
        if package in ['premium', 'enterprise']:
            deliverables['templates'] = self._get_industry_templates(industry)

        return deliverables

    def _create_google_docs(self, deliverables: Dict) -> Dict:
        """Create Google Docs from deliverables"""
        # Implementation using Google Docs API
        pass

    def _send_delivery_email(self, email: str, links: Dict):
        """Send delivery email with links"""
        # Implementation using SendGrid/similar
        pass

    def _schedule_follow_ups(self, order_id: str):
        """Schedule automated follow-up emails"""
        # Implementation for scheduling
        pass
```

### 2. Automation Pipeline

```yaml
# option_b/automation_config.yaml
name: AEO Service Automation
version: 1.0

triggers:
  - type: webhook
    endpoint: /api/orders/new
    actions:
      - analyze_website
      - generate_schemas
      - generate_faqs
      - create_package

workflows:
  standard_delivery:
    steps:
      - name: analyze
        timeout: 60s
        retries: 3
      - name: generate
        timeout: 120s
        retries: 2
      - name: review
        type: manual
        assignee: qa_team
      - name: deliver
        timeout: 30s

integrations:
  stripe:
    webhook_endpoint: /api/webhooks/stripe
    events:
      - payment_intent.succeeded
      - payment_intent.failed

  google_docs:
    scopes:
      - https://www.googleapis.com/auth/documents
      - https://www.googleapis.com/auth/drive

  sendgrid:
    templates:
      - delivery: d-12345
      - follow_up: d-67890
      - testimonial_request: d-11111

monitoring:
  alerts:
    - type: error_rate
      threshold: 5%
      window: 5m
    - type: delivery_time
      threshold: 2h
      action: escalate
```

### 3. Template Management System

```javascript
// option_b/template_manager.js
class TemplateManager {
    constructor() {
        this.templates = this.loadTemplates();
    }

    loadTemplates() {
        return {
            photography: {
                faqs: require('./templates/photography/faqs.json'),
                schemas: require('./templates/photography/schemas.json'),
                content: require('./templates/photography/content.json')
            },
            restaurant: {
                faqs: require('./templates/restaurant/faqs.json'),
                schemas: require('./templates/restaurant/schemas.json'),
                content: require('./templates/restaurant/content.json')
            }
            // Add more industries
        };
    }

    getIndustryTemplate(industry, type) {
        return this.templates[industry]?.[type] || this.templates.general[type];
    }

    customizeTemplate(template, businessData) {
        // Replace placeholders with actual data
        let customized = JSON.stringify(template);

        Object.keys(businessData).forEach(key => {
            const placeholder = `{{${key}}}`;
            customized = customized.replace(
                new RegExp(placeholder, 'g'),
                businessData[key]
            );
        });

        return JSON.parse(customized);
    }

    validateCustomization(customized) {
        // Ensure all placeholders were replaced
        const hasPlaceholders = JSON.stringify(customized).includes('{{');
        return !hasPlaceholders;
    }
}

module.exports = TemplateManager;
```

---

## Option C: SaaS Tool Implementation

### 1. Next.js App Structure

```typescript
// option_c/app/api/analyze/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { analyzeWebsite } from '@/lib/analyzer';
import { rateLimit } from '@/lib/rate-limit';
import { trackUsage } from '@/lib/usage';

export async function POST(req: NextRequest) {
    // Check authentication
    const session = await getServerSession();
    if (!session) {
        return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Rate limiting
    const rateLimitResult = await rateLimit(session.user.id);
    if (!rateLimitResult.allowed) {
        return NextResponse.json(
            { error: 'Rate limit exceeded' },
            { status: 429 }
        );
    }

    // Get request data
    const { url, options } = await req.json();

    // Check usage limits
    const canUse = await trackUsage(session.user.id, 'analysis');
    if (!canUse) {
        return NextResponse.json(
            { error: 'Usage limit exceeded' },
            { status: 402 }
        );
    }

    // Run analysis
    try {
        const results = await analyzeWebsite(url, options);

        // Store in database
        await storeAnalysis(session.user.id, results);

        return NextResponse.json(results);
    } catch (error) {
        return NextResponse.json(
            { error: 'Analysis failed', details: error.message },
            { status: 500 }
        );
    }
}
```

### 2. React Components

```tsx
// option_c/components/AnalysisDashboard.tsx
import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { useAnalysis } from '@/hooks/useAnalysis';

export function AnalysisDashboard({ url }: { url: string }) {
    const { analysis, loading, error, refetch } = useAnalysis(url);
    const [generatingSchemas, setGeneratingSchemas] = useState(false);

    const handleGenerateSchemas = async () => {
        setGeneratingSchemas(true);
        try {
            const response = await fetch('/api/generate/schemas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ analysisId: analysis.id })
            });
            const schemas = await response.json();
            // Handle schemas
        } finally {
            setGeneratingSchemas(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center p-8">
                <div className="space-y-4">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
                    <p>Analyzing {url}...</p>
                    <Progress value={33} className="w-[200px]" />
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <Card className="border-red-200 bg-red-50">
                <CardContent className="pt-6">
                    <p className="text-red-600">Analysis failed: {error.message}</p>
                    <Button onClick={refetch} className="mt-4">Retry</Button>
                </CardContent>
            </Card>
        );
    }

    return (
        <div className="space-y-6">
            {/* AEO Score Card */}
            <Card>
                <CardHeader>
                    <CardTitle>AEO Score</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex items-center space-x-4">
                        <div className="text-4xl font-bold">
                            {analysis.aeoScore}/100
                        </div>
                        <Progress value={analysis.aeoScore} className="flex-1" />
                    </div>
                </CardContent>
            </Card>

            {/* Schemas Found */}
            <Card>
                <CardHeader>
                    <CardTitle>Existing Schemas</CardTitle>
                </CardHeader>
                <CardContent>
                    {analysis.schemas.length > 0 ? (
                        <ul className="space-y-2">
                            {analysis.schemas.map((schema, i) => (
                                <li key={i} className="flex items-center">
                                    <span className="text-green-500 mr-2">✓</span>
                                    {schema['@type']}
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p className="text-gray-500">No schemas found</p>
                    )}
                </CardContent>
            </Card>

            {/* Recommendations */}
            <Card>
                <CardHeader>
                    <CardTitle>Recommendations</CardTitle>
                </CardHeader>
                <CardContent>
                    <ul className="space-y-2">
                        {analysis.recommendations.map((rec, i) => (
                            <li key={i} className="flex items-start">
                                <span className="text-yellow-500 mr-2 mt-1">⚠</span>
                                <span>{rec}</span>
                            </li>
                        ))}
                    </ul>
                </CardContent>
            </Card>

            {/* Actions */}
            <div className="flex space-x-4">
                <Button
                    onClick={handleGenerateSchemas}
                    disabled={generatingSchemas}
                >
                    {generatingSchemas ? 'Generating...' : 'Generate Schemas'}
                </Button>
                <Button variant="outline">Generate FAQs</Button>
                <Button variant="outline">Export Report</Button>
            </div>
        </div>
    );
}
```

### 3. Database Schema (Prisma)

```prisma
// option_c/prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id            String    @id @default(cuid())
  email         String    @unique
  name          String?
  subscription  Subscription?
  projects      Project[]
  usage         Usage[]
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
}

model Subscription {
  id            String    @id @default(cuid())
  userId        String    @unique
  user          User      @relation(fields: [userId], references: [id])
  tier          String    // starter, professional, business, enterprise
  status        String    // active, cancelled, past_due
  currentPeriodStart DateTime
  currentPeriodEnd   DateTime
  stripeCustomerId   String?
  stripeSubscriptionId String?
}

model Project {
  id            String    @id @default(cuid())
  userId        String
  user          User      @relation(fields: [userId], references: [id])
  domain        String
  industry      String?
  analyses      Analysis[]
  schemas       Schema[]
  faqs          FAQ[]
  lastAnalysis  DateTime?
  aeoScore      Int?
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt

  @@unique([userId, domain])
}

model Analysis {
  id            String    @id @default(cuid())
  projectId     String
  project       Project   @relation(fields: [projectId], references: [id])
  url           String
  content       Json
  existingSchemas Json
  metaData      Json
  aeoScore      Int
  recommendations String[]
  createdAt     DateTime  @default(now())
}

model Schema {
  id            String    @id @default(cuid())
  projectId     String
  project       Project   @relation(fields: [projectId], references: [id])
  type          String    // Organization, FAQPage, etc
  content       Json
  validated     Boolean   @default(false)
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
}

model FAQ {
  id            String    @id @default(cuid())
  projectId     String
  project       Project   @relation(fields: [projectId], references: [id])
  question      String
  answer        String    @db.Text
  order         Int
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
}

model Usage {
  id            String    @id @default(cuid())
  userId        String
  user          User      @relation(fields: [userId], references: [id])
  action        String    // analysis, schema_generation, faq_generation, export
  count         Int       @default(1)
  createdAt     DateTime  @default(now())

  @@index([userId, createdAt])
}
```

### 4. API Rate Limiting & Usage Tracking

```typescript
// option_c/lib/rate-limit.ts
import { Redis } from '@upstash/redis';

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_URL!,
  token: process.env.UPSTASH_REDIS_TOKEN!,
});

export async function rateLimit(userId: string, limit: number = 10) {
  const key = `rate_limit:${userId}:${Math.floor(Date.now() / 60000)}`;

  const current = await redis.incr(key);

  if (current === 1) {
    await redis.expire(key, 60);
  }

  return {
    allowed: current <= limit,
    remaining: Math.max(0, limit - current),
    reset: new Date(Math.ceil(Date.now() / 60000) * 60000)
  };
}

// option_c/lib/usage.ts
import { prisma } from '@/lib/prisma';

export async function trackUsage(userId: string, action: string) {
  // Get user's subscription
  const user = await prisma.user.findUnique({
    where: { id: userId },
    include: { subscription: true }
  });

  if (!user?.subscription) {
    return false;
  }

  // Check limits based on tier
  const limits = {
    starter: { analysis: 5, schema_generation: 10, faq_generation: 5 },
    professional: { analysis: 50, schema_generation: 100, faq_generation: 50 },
    business: { analysis: -1, schema_generation: -1, faq_generation: -1 } // unlimited
  };

  const tierLimits = limits[user.subscription.tier];
  const actionLimit = tierLimits[action];

  // Unlimited
  if (actionLimit === -1) {
    await prisma.usage.create({
      data: { userId, action }
    });
    return true;
  }

  // Check current usage this billing period
  const currentUsage = await prisma.usage.count({
    where: {
      userId,
      action,
      createdAt: {
        gte: user.subscription.currentPeriodStart
      }
    }
  });

  if (currentUsage >= actionLimit) {
    return false;
  }

  // Track usage
  await prisma.usage.create({
    data: { userId, action }
  });

  return true;
}
```

---

## Deployment & Infrastructure

### Option B Deployment (Simple)

```yaml
# option_b/docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/aeo
      - REDIS_URL=redis://redis:6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
    depends_on:
      - db
      - redis

  db:
    image: postgres:14
    environment:
      - POSTGRES_DB=aeo
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  worker:
    build: .
    command: npm run worker
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/aeo
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

### Option C Deployment (Scalable)

```typescript
// option_c/vercel.json
{
  "functions": {
    "app/api/analyze/route.ts": {
      "maxDuration": 60
    },
    "app/api/generate/*/route.ts": {
      "maxDuration": 30
    }
  },
  "crons": [
    {
      "path": "/api/cron/monitor",
      "schedule": "0 */6 * * *"
    },
    {
      "path": "/api/cron/usage-reset",
      "schedule": "0 0 1 * *"
    }
  ]
}
```

---

## Monitoring & Analytics

```typescript
// shared/monitoring.ts
import { PostHog } from 'posthog-node';

const posthog = new PostHog(process.env.POSTHOG_API_KEY!);

export function trackEvent(userId: string, event: string, properties?: any) {
  posthog.capture({
    distinctId: userId,
    event,
    properties: {
      ...properties,
      timestamp: new Date().toISOString(),
      environment: process.env.NODE_ENV
    }
  });
}

export function trackConversion(userId: string, value: number, plan: string) {
  trackEvent(userId, 'conversion', {
    value,
    plan,
    source: 'organic' // or paid, referral, etc
  });
}

export function trackChurn(userId: string, reason?: string) {
  trackEvent(userId, 'churn', {
    reason,
    lifetime_value: calculateLTV(userId)
  });
}
```

---

This technical implementation guide provides the core components needed to build both Option B (Template Service) and Option C (SaaS Tool). The shared components can be used for both, while each option has its specific implementation details for order processing, automation, and scaling.