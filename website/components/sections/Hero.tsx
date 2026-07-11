import EmailCapture from '../ui/EmailCapture';

export default function Hero() {
  return (
    <section className="pt-20 pb-16 px-4 sm:px-6 lg:px-8 bg-white">
      <div className="max-w-6xl mx-auto">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight">
            Everything You Need to{' '}
            <span className="text-[#0066FF]">Optimize for AI Search</span>
          </h1>
          
          <p className="text-xl sm:text-2xl text-gray-600 mb-8 leading-relaxed">
            Free guides, tools, and resources to make your website visible to{' '}
            <span className="font-semibold text-gray-900">ChatGPT, Perplexity, and Google AI</span>
          </p>
          
          <div className="mb-12">
            <EmailCapture variant="hero" />
          </div>
          
          <div className="flex flex-wrap justify-center gap-6 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <span className="text-green-500">✓</span>
              <span>Free resources</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-green-500">✓</span>
              <span>No credit card required</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-green-500">✓</span>
              <span>Weekly insights</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}


