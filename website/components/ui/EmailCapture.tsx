'use client';

import { useState } from 'react';

interface EmailCaptureProps {
  variant?: 'hero' | 'sidebar' | 'inline';
  className?: string;
}

export default function EmailCapture({ variant = 'hero', className = '' }: EmailCaptureProps) {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');

    // TODO: Replace with your email service integration
    // Options: Beehiiv API, ConvertKit, Mailchimp, or custom API endpoint
    // For now, this is just a placeholder that simulates success
    
    setTimeout(() => {
      setStatus('success');
      setEmail('');
      // Reset after 3 seconds
      setTimeout(() => setStatus('idle'), 3000);
    }, 1000);

    // Example integration (uncomment and modify when ready):
    /*
    try {
      const response = await fetch('/api/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });
      
      if (response.ok) {
        setStatus('success');
        setEmail('');
      } else {
        setStatus('error');
      }
    } catch (error) {
      setStatus('error');
    }
    */
  };

  const variants = {
    hero: 'max-w-2xl mx-auto',
    sidebar: 'w-full',
    inline: 'w-full max-w-md',
  };

  return (
    <div className={variants[variant] + ' ' + className}>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex flex-col sm:flex-row gap-3">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            required
            className="flex-1 px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#0066FF] focus:border-transparent text-base"
            disabled={status === 'loading' || status === 'success'}
          />
          <button
            type="submit"
            disabled={status === 'loading' || status === 'success'}
            className="px-8 py-3 bg-[#0066FF] text-white rounded-lg font-semibold hover:bg-[#0052CC] transition-colors disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
          >
            {status === 'loading' ? 'Subscribing...' : status === 'success' ? '✓ Subscribed!' : 'Subscribe'}
          </button>
        </div>
        
        {status === 'success' && (
          <p className="text-sm text-green-600 text-center">
            Thanks! Check your email to confirm.
          </p>
        )}
        
        {status === 'error' && (
          <p className="text-sm text-red-600 text-center">
            Something went wrong. Please try again.
          </p>
        )}
        
        <p className="text-xs text-gray-500 text-center">
          No spam. Unsubscribe anytime.
        </p>
      </form>
    </div>
  );
}


