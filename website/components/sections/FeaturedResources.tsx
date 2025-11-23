import ResourceCard from '../ui/ResourceCard';

const featuredResources = [
  {
    title: 'Complete AEO Guide',
    description: 'A comprehensive 30-page guide covering everything you need to know about Answer Engine Optimization, from technical implementation to content strategy.',
    href: '/resources/complete-aeo-guide',
    type: 'guide' as const,
    downloadCount: 1247,
  },
  {
    title: 'AEO Score Checker',
    description: 'Enter your website URL and get an instant AEO score with actionable recommendations for improvement.',
    href: '/tools/aeo-checker',
    type: 'tool' as const,
  },
  {
    title: 'Schema Markup Templates',
    description: 'Ready-to-use schema templates for Organization, FAQ, Service, and more. Copy, paste, customize.',
    href: '/resources/schema-templates',
    type: 'template' as const,
    downloadCount: 892,
  },
  {
    title: 'AEO vs SEO: What\'s the Difference?',
    description: 'Understand how AI search optimization differs from traditional SEO and why you need both strategies.',
    href: '/articles/aeo-vs-seo',
    type: 'article' as const,
  },
];

export default function FeaturedResources() {
  return (
    <section className="py-16 px-4 sm:px-6 lg:px-8 bg-[#F8F9FA]">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Featured Resources
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Start with these essential resources to optimize your website for AI search engines
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {featuredResources.map((resource, index) => (
            <ResourceCard key={index} {...resource} />
          ))}
        </div>
      </div>
    </section>
  );
}


