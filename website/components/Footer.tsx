import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-gray-50 border-t border-gray-200 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div>
            <h3 className="text-lg font-bold text-gray-900 mb-4">AEO Optimizer</h3>
            <p className="text-sm text-gray-600">
              Free resources to optimize your website for AI search engines.
            </p>
          </div>
          
          <div>
            <h4 className="font-semibold text-gray-900 mb-4">Resources</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/resources/guides" className="text-gray-600 hover:text-gray-900">Guides</Link></li>
              <li><Link href="/resources/templates" className="text-gray-600 hover:text-gray-900">Templates</Link></li>
              <li><Link href="/resources/case-studies" className="text-gray-600 hover:text-gray-900">Case Studies</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-semibold text-gray-900 mb-4">Tools</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/tools/aeo-checker" className="text-gray-600 hover:text-gray-900">AEO Checker</Link></li>
              <li><Link href="/tools/schema-generator" className="text-gray-600 hover:text-gray-900">Schema Generator</Link></li>
              <li><Link href="/tools/faq-generator" className="text-gray-600 hover:text-gray-900">FAQ Generator</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-semibold text-gray-900 mb-4">Company</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/about" className="text-gray-600 hover:text-gray-900">About</Link></li>
              <li><Link href="/articles" className="text-gray-600 hover:text-gray-900">Articles</Link></li>
              <li><Link href="/contact" className="text-gray-600 hover:text-gray-900">Contact</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-200 pt-8 text-center text-sm text-gray-600">
          <p>© {new Date().getFullYear()} AEO Optimizer. All resources are free and open.</p>
        </div>
      </div>
    </footer>
  );
}


