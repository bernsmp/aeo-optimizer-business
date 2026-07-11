import Link from 'next/link';

const categories = [
  {
    name: 'Guides & Tutorials',
    description: 'Comprehensive guides covering AEO fundamentals and advanced strategies',
    href: '/resources/guides',
    icon: '📚',
    count: 12,
  },
  {
    name: 'Free Tools',
    description: 'Interactive tools to check your AEO score and generate schemas',
    href: '/tools',
    icon: '🛠️',
    count: 5,
  },
  {
    name: 'Templates & Schemas',
    description: 'Ready-to-use schema templates and FAQ generators',
    href: '/resources/templates',
    icon: '📄',
    count: 15,
  },
  {
    name: 'Case Studies',
    description: 'Real examples of AEO optimization results and strategies',
    href: '/resources/case-studies',
    icon: '📊',
    count: 8,
  },
];

export default function ResourceCategories() {
  return (
    <section className="py-16 px-4 sm:px-6 lg:px-8 bg-white">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Browse by Category
          </h2>
          <p className="text-xl text-gray-600">
            Find exactly what you need to optimize your website for AI search
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {categories.map((category) => (
            <Link
              key={category.name}
              href={category.href}
              className="group bg-white border-2 border-gray-200 rounded-xl p-6 hover:border-[#0066FF] hover:shadow-lg transition-all duration-200"
            >
              <div className="text-4xl mb-4">{category.icon}</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-[#0066FF] transition-colors">
                {category.name}
              </h3>
              <p className="text-gray-600 text-sm mb-4">
                {category.description}
              </p>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-[#0066FF] group-hover:underline">
                  Browse →
                </span>
                <span className="text-xs text-gray-500">
                  {category.count} resources
                </span>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}


