import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const resourcesDirectory = path.join(process.cwd(), 'content/resources');

export interface Resource {
  slug: string;
  title: string;
  description: string;
  type: 'guide' | 'tool' | 'template' | 'article';
  content: string;
  date?: string;
  downloadCount?: number;
  badge?: string;
}

export function getAllResources(): Resource[] {
  if (!fs.existsSync(resourcesDirectory)) {
    return [];
  }

  const fileNames = fs.readdirSync(resourcesDirectory);
  const resources = fileNames
    .filter((name) => name.endsWith('.md'))
    .map((fileName) => {
      const slug = fileName.replace(/\.md$/, '');
      const fullPath = path.join(resourcesDirectory, fileName);
      const fileContents = fs.readFileSync(fullPath, 'utf8');
      const { data, content } = matter(fileContents);

      return {
        slug,
        title: data.title || '',
        description: data.description || '',
        type: data.type || 'article',
        content,
        date: data.date,
        downloadCount: data.downloadCount,
        badge: data.badge || 'Free',
      };
    });

  return resources.sort((a, b) => {
    if (a.date && b.date) {
      return new Date(b.date).getTime() - new Date(a.date).getTime();
    }
    return 0;
  });
}

export function getResourceBySlug(slug: string): Resource | null {
  const fullPath = path.join(resourcesDirectory, `${slug}.md`);
  
  if (!fs.existsSync(fullPath)) {
    return null;
  }

  const fileContents = fs.readFileSync(fullPath, 'utf8');
  const { data, content } = matter(fileContents);

  return {
    slug,
    title: data.title || '',
    description: data.description || '',
    type: data.type || 'article',
    content,
    date: data.date,
    downloadCount: data.downloadCount,
    badge: data.badge || 'Free',
  };
}

export function getResourcesByType(type: Resource['type']): Resource[] {
  return getAllResources().filter((resource) => resource.type === type);
}


