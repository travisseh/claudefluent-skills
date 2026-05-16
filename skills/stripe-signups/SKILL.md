---
name: stripe-signups
description: Query Stripe for ClaudeFluent course signups, waitlist subscribers, session data, and customer information. Use when checking enrollment numbers, revenue, or customer data.
---

# Stripe Signups - Claude Code Course

Query and analyze Stripe checkout data for the Claude Code course.

## Configuration

- **Product ID (metadata):** `claude-code-course`
- **Session IDs:**
  - `weekday` - Wed Jan 21 + Thu Jan 22, 2026
  - `saturday1` - Saturday, January 24, 2026
  - `saturday2` - Saturday, January 31, 2026
- **Stripe API Keys:** Stored in `~/Programming/personal-master/personal/claude_course/website/.env.local`
  - `STRIPE_SECRET_KEY` - Production key (use this for real signups)

## Quick Query Script

```typescript
import Stripe from 'stripe';
import * as dotenv from 'dotenv';
import * as path from 'path';

// Load env vars from .env.local
dotenv.config({ path: path.join(__dirname, '.env.local') });

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
});

async function getSignups(sessionId?: string) {
  const sessions = await stripe.checkout.sessions.list({
    limit: 100,
    status: 'complete',
  });

  const courseSessions = sessions.data.filter(
    session => session.metadata?.product === 'claude-code-course'
  );

  if (sessionId) {
    return courseSessions.filter(s => s.metadata?.session === sessionId);
  }

  return courseSessions;
}

// Get all signups
const allSignups = await getSignups();

// Get specific session
const saturdaySignups = await getSignups('saturday1');

// Extract customer data
const customers = allSignups.map(session => ({
  name: session.customer_details?.name,
  email: session.customer_details?.email,
  sessionId: session.metadata?.session,
  amount: session.amount_total / 100,
  created: new Date(session.created * 1000),
  // Custom metadata fields if available
  linkedin: session.metadata?.linkedin,
  company: session.metadata?.company,
}));
```

## Common Queries

### Count Signups by Session

```typescript
async function countBySession() {
  const sessions = await getSignups();
  const counts: Record<string, number> = {};

  for (const session of sessions) {
    const sessionId = session.metadata?.session || 'unknown';
    counts[sessionId] = (counts[sessionId] || 0) + 1;
  }

  return counts;
}

// Example output:
// { weekday: 4, saturday1: 2, saturday2: 0 }
```

### Get Email List for Session

```typescript
async function getEmails(sessionId: string) {
  const sessions = await getSignups(sessionId);
  return sessions
    .map(s => s.customer_details?.email)
    .filter(Boolean);
}

// Usage:
const saturdayEmails = await getEmails('saturday1');
// ['dasha@proton.ai', 'jonathan.blank@gmail.com']
```

### Get Full Customer Details

```typescript
async function getCustomerDetails(sessionId?: string) {
  const sessions = await getSignups(sessionId);

  return sessions.map(session => ({
    name: session.customer_details?.name,
    email: session.customer_details?.email,
    phone: session.customer_details?.phone,
    session: session.metadata?.session,
    amountPaid: session.amount_total / 100,
    currency: session.currency,
    created: new Date(session.created * 1000).toISOString(),
    // Metadata (if set during checkout)
    linkedin: session.metadata?.linkedin,
    company: session.metadata?.company,
    role: session.metadata?.role,
  }));
}
```

### Search by Email

```typescript
async function findByEmail(email: string) {
  const allSessions = await getSignups();
  return allSessions.find(s =>
    s.customer_details?.email?.toLowerCase() === email.toLowerCase()
  );
}
```

## Working Directory

Run scripts from: `~/Programming/personal-master/personal/claude_course/website/`

This directory has:
- `node_modules` with Stripe SDK installed
- `.env.local` with production Stripe API key

## Example: Quick Signup Report

```typescript
import Stripe from 'stripe';
import * as fs from 'fs';
import * as dotenv from 'dotenv';
import * as path from 'path';

// Load env vars
dotenv.config({ path: path.join(__dirname, '.env.local') });

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
});

async function generateReport() {
  const sessions = await stripe.checkout.sessions.list({
    limit: 100,
    status: 'complete',
  });

  const courseSessions = sessions.data.filter(
    s => s.metadata?.product === 'claude-code-course'
  );

  // Count by session
  const counts: Record<string, number> = {};
  const bySession: Record<string, any[]> = {};

  for (const session of courseSessions) {
    const sessionId = session.metadata?.session || 'unknown';
    counts[sessionId] = (counts[sessionId] || 0) + 1;

    if (!bySession[sessionId]) bySession[sessionId] = [];
    bySession[sessionId].push({
      name: session.customer_details?.name,
      email: session.customer_details?.email,
      amount: session.amount_total / 100,
      date: new Date(session.created * 1000).toLocaleDateString(),
    });
  }

  console.log('=== Claude Code Course Signups ===\n');
  console.log('Total signups:', courseSessions.length);
  console.log('\nBy session:');
  Object.entries(counts).forEach(([session, count]) => {
    console.log(`  ${session}: ${count}`);
  });
  console.log('\n');

  for (const [sessionId, people] of Object.entries(bySession)) {
    console.log(`${sessionId.toUpperCase()}:`);
    people.forEach(p => {
      console.log(`  - ${p.name} (${p.email}) - $${p.amount} on ${p.date}`);
    });
    console.log('');
  }

  // Save to file
  fs.writeFileSync(
    '/tmp/stripe-signups.json',
    JSON.stringify({ counts, bySession }, null, 2)
  );
  console.log('Full report saved to /tmp/stripe-signups.json');
}

generateReport().catch(console.error);
```

## Running Scripts

```bash
# From the website directory
cd ~/Programming/personal-master/personal/claude_course/website

# Run TypeScript directly
npx tsx script-name.ts

# Or compile and run
npx tsc script-name.ts && node script-name.js
```

## Additional Customer Data

If you need more customer information (like from the actual Customer object), you can fetch it:

```typescript
async function getFullCustomerData(sessionId: string) {
  const sessions = await getSignups(sessionId);
  const customerData = [];

  for (const session of sessions) {
    if (session.customer) {
      // Fetch full customer object
      const customer = await stripe.customers.retrieve(session.customer as string);
      customerData.push({
        ...session.customer_details,
        stripeCustomerId: session.customer,
        description: 'description' in customer ? customer.description : null,
        metadata: 'metadata' in customer ? customer.metadata : {},
      });
    } else {
      customerData.push(session.customer_details);
    }
  }

  return customerData;
}
```

## Notes

- All completed checkout sessions have `status: 'complete'`
- Customer details are in `customer_details` object (name, email, phone)
- Custom data (LinkedIn, etc.) must be added as metadata during checkout
- The `metadata.product` field identifies course purchases
- The `metadata.session` field identifies which class session they chose
- Stripe API has rate limits: ~100 requests/second
- Use `limit` parameter to fetch more than 10 results (max 100 per request)

## Extending Checkout to Capture LinkedIn

To capture LinkedIn profiles during checkout, modify the checkout flow:

```typescript
// In create-checkout route
const session = await stripe.checkout.sessions.create({
  // ... other params
  custom_fields: [
    {
      key: 'linkedin',
      label: { type: 'custom', custom: 'LinkedIn Profile URL' },
      type: 'text',
      optional: true,
    },
  ],
  // Store in metadata
  metadata: {
    product: 'claude-code-course',
    session: sessionId,
    // LinkedIn will be available after checkout
  },
});
```

After checkout completes, access custom fields via webhook or session retrieval.
