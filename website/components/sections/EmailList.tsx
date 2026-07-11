import EmailCapture from '../ui/EmailCapture';

export default function EmailList() {
  return (
    <section className="py-16 px-4 sm:px-6 lg:px-8 bg-white">
      <div className="max-w-4xl mx-auto">
        <div className="bg-gradient-to-br from-[#0066FF] to-[#0052CC] rounded-2xl p-8 sm:p-12 text-white text-center">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            Join 1,000+ marketers optimizing for AI search
          </h2>
          
          <p className="text-lg sm:text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Get weekly insights, free templates, early access to tools, and real case studies delivered to your inbox.
          </p>
          
          <div className="mb-6">
            <EmailCapture variant="inline" className="bg-white rounded-lg p-2" />
          </div>
          
          <div className="flex flex-wrap justify-center gap-6 text-sm text-blue-100">
            <div className="flex items-center gap-2">
              <span>✓</span>
              <span>Weekly AEO insights</span>
            </div>
            <div className="flex items-center gap-2">
              <span>✓</span>
              <span>Free templates & guides</span>
            </div>
            <div className="flex items-center gap-2">
              <span>✓</span>
              <span>Early access to tools</span>
            </div>
            <div className="flex items-center gap-2">
              <span>✓</span>
              <span>Case studies & examples</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}


