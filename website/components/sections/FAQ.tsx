import FAQ from '../ui/FAQ';

const faqItems = [
  {
    question: 'What is AEO (Answer Engine Optimization)?',
    answer: 'AEO is the practice of optimizing your website content and structure so that AI search engines like ChatGPT, Perplexity, and Google AI can find, understand, and cite your content when answering user queries. It involves structured data, clear content organization, and FAQ optimization.',
  },
  {
    question: 'How is AEO different from SEO?',
    answer: 'While SEO focuses on ranking in traditional search results, AEO focuses on being cited by AI assistants. AI search engines read and understand content differently than traditional crawlers, prioritizing clear answers, structured data, and authoritative sources. AEO complements SEO—both strategies work together.',
  },
  {
    question: 'Do I need AEO if I already have SEO?',
    answer: 'Yes! SEO helps you rank in search results, but AEO helps you get cited by AI assistants. As AI search grows, businesses need both strategies. The good news is that many AEO optimizations (like schema markup and FAQ pages) also improve your SEO.',
  },
  {
    question: 'How long does it take to see results?',
    answer: 'AI search engines can index and start citing your content much faster than traditional search engines—often within 2-7 days. However, building authority and getting consistent citations takes time, similar to SEO. Most businesses see initial results within 2-4 weeks.',
  },
  {
    question: 'What do I need to get started?',
    answer: 'Start with the basics: add schema markup to your site, create comprehensive FAQ pages, optimize your content for clear answers, and add an llms.txt file. Our free guides and tools will walk you through each step.',
  },
  {
    question: 'Is this free?',
    answer: 'Yes! All our resources, guides, templates, and tools are completely free. We\'re building a community around AEO optimization. In the future, we may offer premium services, but the core resources will always be free.',
  },
];

export default function FAQSection() {
  return (
    <section className="py-16 px-4 sm:px-6 lg:px-8 bg-[#F8F9FA]">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Frequently Asked Questions
          </h2>
          <p className="text-xl text-gray-600">
            Everything you need to know about AEO optimization
          </p>
        </div>
        
        <FAQ items={faqItems} />
      </div>
    </section>
  );
}


