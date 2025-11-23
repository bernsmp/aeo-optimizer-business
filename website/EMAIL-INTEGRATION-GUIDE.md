# Email Integration Guide

The email capture component is ready but needs backend integration. Here are your options:

## Option 1: Beehiiv API

Beehiiv is a modern newsletter platform. To integrate:

1. Get your Beehiiv API key from your dashboard
2. Create an API route at `app/api/subscribe/route.ts`:

```typescript
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const { email } = await request.json();
  
  const response = await fetch('https://api.beehiiv.com/v2/subscribers', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer YOUR_BEEHIIV_API_KEY`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email,
      publication_id: 'YOUR_PUBLICATION_ID',
    }),
  });

  if (response.ok) {
    return NextResponse.json({ success: true });
  }
  
  return NextResponse.json({ success: false }, { status: 400 });
}
```

3. Update `components/ui/EmailCapture.tsx` to use this endpoint

## Option 2: ConvertKit

1. Get your ConvertKit API key and form ID
2. Create API route:

```typescript
export async function POST(request: Request) {
  const { email } = await request.json();
  
  const response = await fetch(
    `https://api.convertkit.com/v3/forms/YOUR_FORM_ID/subscribe`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        api_key: 'YOUR_API_KEY',
        email,
      }),
    }
  );

  return NextResponse.json({ success: response.ok });
}
```

## Option 3: Mailchimp

1. Get your Mailchimp API key and list ID
2. Create API route:

```typescript
export async function POST(request: Request) {
  const { email } = await request.json();
  const API_KEY = process.env.MAILCHIMP_API_KEY;
  const LIST_ID = process.env.MAILCHIMP_LIST_ID;
  const DATACENTER = API_KEY.split('-')[1];

  const response = await fetch(
    `https://${DATACENTER}.api.mailchimp.com/3.0/lists/${LIST_ID}/members`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email_address: email,
        status: 'subscribed',
      }),
    }
  );

  return NextResponse.json({ success: response.ok });
}
```

## Option 4: Custom API Endpoint

Build your own endpoint that stores emails in a database (Supabase, Firebase, etc.):

```typescript
export async function POST(request: Request) {
  const { email } = await request.json();
  
  // Save to your database
  // await db.subscribers.create({ email });
  
  return NextResponse.json({ success: true });
}
```

## Environment Variables

Add to `.env.local`:

```
BEEHIIV_API_KEY=your_key_here
# or
CONVERTKIT_API_KEY=your_key_here
CONVERTKIT_FORM_ID=your_form_id
# or
MAILCHIMP_API_KEY=your_key_here
MAILCHIMP_LIST_ID=your_list_id
```

## Testing

The component currently simulates success. To test with real integration:

1. Uncomment the fetch code in `EmailCapture.tsx`
2. Update the endpoint URL
3. Test the form submission

## Current State

The email capture component is fully functional UI-wise but uses a placeholder backend. It will:
- Show loading state
- Show success message
- Show error handling
- Validate email format

Just needs the actual API integration!


