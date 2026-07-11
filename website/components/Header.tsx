import Link from 'next/link';

export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-white border-b border-gray-200">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="text-2xl font-bold text-gray-900">
            AEO Optimizer
          </Link>
          
          <nav className="hidden md:flex items-center gap-8">
            <Link href="/resources" className="text-gray-600 hover:text-gray-900 transition-colors">
              Resources
            </Link>
            <Link href="/tools" className="text-gray-600 hover:text-gray-900 transition-colors">
              Tools
            </Link>
            <Link href="/articles" className="text-gray-600 hover:text-gray-900 transition-colors">
              Articles
            </Link>
            <Link href="/about" className="text-gray-600 hover:text-gray-900 transition-colors">
              About
            </Link>
          </nav>
          
          <Link
            href="/#subscribe"
            className="px-4 py-2 bg-[#0066FF] text-white rounded-lg font-semibold hover:bg-[#0052CC] transition-colors text-sm"
          >
            Subscribe
          </Link>
        </div>
      </div>
    </header>
  );
}


