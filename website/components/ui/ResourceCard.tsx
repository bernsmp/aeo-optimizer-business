import Link from 'next/link';

interface ResourceCardProps {
  title: string;
  description: string;
  href: string;
  type: 'guide' | 'tool' | 'template' | 'article';
  badge?: string;
  downloadCount?: number;
}

export default function ResourceCard({
  title,
  description,
  href,
  type,
  badge = 'Free',
  downloadCount,
}: ResourceCardProps) {
  const typeIcons = {
    guide: '📚',
    tool: '🛠️',
    template: '📄',
    article: '📝',
  };

  const typeColors = {
    guide: 'bg-blue-100 text-blue-800',
    tool: 'bg-purple-100 text-purple-800',
    template: 'bg-green-100 text-green-800',
    article: 'bg-orange-100 text-orange-800',
  };

  return (
    <Link
      href={href}
      className="group block bg-white rounded-xl border border-gray-200 hover:border-[#0066FF] hover:shadow-lg transition-all duration-200 p-6 h-full"
    >
      <div className="flex items-start justify-between mb-4">
        <span className="text-3xl">{typeIcons[type]}</span>
        <span className={`px-2 py-1 rounded-md text-xs font-semibold ${typeColors[type]}`}>
          {badge}
        </span>
      </div>
      
      <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-[#0066FF] transition-colors">
        {title}
      </h3>
      
      <p className="text-gray-600 text-sm mb-4 line-clamp-2">
        {description}
      </p>
      
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-[#0066FF] group-hover:underline">
          {type === 'tool' ? 'Try Tool' : type === 'article' ? 'Read More' : 'Download'}
        </span>
        {downloadCount && (
          <span className="text-xs text-gray-500">
            {downloadCount}+ downloads
          </span>
        )}
      </div>
    </Link>
  );
}


