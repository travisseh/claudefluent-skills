---
name: stripe
description: "Query Stripe for ClaudeFluent course signups, waitlist subscribers, session data, and customer information. Use this skill whenever the user asks about enrollment numbers, revenue, customer data, signups, payments, subscription status, or any financial data for ClaudeFluent. Also trigger when they ask 'how many signups', 'check revenue', 'who signed up', 'Stripe data', 'how much have we made', or want to look up any customer or payment information. Triggers on: Stripe, signups, revenue, enrollment, customers, payments, waitlist, subscribers, how many signed up, check revenue, customer data, ClaudeFluent revenue, course signups."
---

# Stripe - ClaudeFluent

Query Stripe for course signups, waitlist subscribers, and customer data.

## Configuration

- **Product ID (metadata):** `claude-code-course`
- **Waitlist metadata:** `waitlist: 'premium-skills'`
- **Stripe API Keys:** `~/Programming/personal-master/personal/claude_course/website/.env.local`
- **Working Directory:** `~/Programming/personal-master/personal/claude_course/website/`

## Session IDs

- `weekday` - Wed Jan 21 + Thu Jan 22, 2026 (6:30-9pm MST)
- `saturday1` - Saturday, January 24, 2026 (10am-3pm MST)
- `saturday2` - Saturday, January 31, 2026 (10am-3pm MST)
- `weekday2` - Wed Feb 4 + Thu Feb 5, 2026 (6:30-9pm MST)
- `weekday3` - Wed Feb 11 + Thu Feb 12, 2026 (6:30-9pm MST)
- `weekday4` - Wed Feb 18 + Thu Feb 19, 2026 (6:30-9pm MST)
- `saturday3` - Saturday, February 21, 2026 (12-5pm MST)
- `weekday5` - Wed Feb 25 + Thu Feb 26, 2026 (6:30-9pm MST)

---

## Waitlist Queries

### Get All Waitlist Emails

```typescript
import Stripe from 'stripe';
import * as dotenv from 'dotenv';
dotenv.config({ path: '.env.local' });

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
});

async function getWaitlist() {
  const customers: { email: string; name: string | null; date: string }[] = [];
  let hasMore = true;
  let startingAfter: string | undefined;

  while (hasMore) {
    const response = await stripe.customers.list({
      limit: 100,
      starting_after: startingAfter,
    });

    for (const customer of response.data) {
      if (customer.metadata?.waitlist === 'premium-skills') {
        customers.push({
          email: customer.email!,
          name: customer.name,
          date: customer.metadata.waitlist_date || 'unknown',
        });
      }
    }

    hasMore = response.has_more;
    if (response.data.length > 0) {
      startingAfter = response.data[response.data.length - 1].id;
    }
  }

  return customers;
}

// Usage
const waitlist = await getWaitlist();
console.log(`Waitlist count: ${waitlist.length}`);
waitlist.forEach(c => console.log(`${c.email} (joined ${c.date})`));
```

### Get Waitlist Emails Only (for bulk email)

```typescript
async function getWaitlistEmails(): Promise<string[]> {
  const waitlist = await getWaitlist();
  return waitlist.map(c => c.email);
}
```

---

## Course Signup Queries

### Get All Course Signups

```typescript
async function getSignups(sessionId?: string) {
  const allSessions: Stripe.Checkout.Session[] = [];
  let hasMore = true;
  let startingAfter: string | undefined;

  while (hasMore) {
    const response = await stripe.checkout.sessions.list({
      limit: 100,
      status: 'complete',
      starting_after: startingAfter,
    });

    const courseSessions = response.data.filter(
      s => s.metadata?.product === 'claude-code-course'
    );
    allSessions.push(...courseSessions);

    hasMore = response.has_more;
    if (response.data.length > 0) {
      startingAfter = response.data[response.data.length - 1].id;
    }
  }

  if (sessionId) {
    return allSessions.filter(s => s.metadata?.session === sessionId);
  }
  return allSessions;
}
```

### Get Customer Details

```typescript
async function getCustomerDetails(sessionId?: string) {
  const sessions = await getSignups(sessionId);

  return sessions.map(session => ({
    name: session.customer_details?.name,
    email: session.customer_details?.email,
    session: session.metadata?.session,
    amount: (session.amount_total || 0) / 100,
    created: new Date(session.created * 1000).toISOString(),
    linkedin: session.custom_fields?.find(f => f.key === 'linkedin')?.text?.value,
    referredBy: session.metadata?.ref,
  }));
}
```

### Count by Session

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
```

### Get Emails for a Session

```typescript
async function getEmailsForSession(sessionId: string): Promise<string[]> {
  const sessions = await getSignups(sessionId);
  return sessions
    .map(s => s.customer_details?.email)
    .filter((e): e is string => !!e);
}
```

---

## Referral/Affiliate Queries

### Get Referral Stats

```typescript
async function getReferralStats() {
  const sessions = await getSignups();
  const referrals: Record<string, { count: number; revenue: number }> = {};

  for (const session of sessions) {
    const ref = session.metadata?.ref;
    if (ref) {
      if (!referrals[ref]) referrals[ref] = { count: 0, revenue: 0 };
      referrals[ref].count++;
      referrals[ref].revenue += (session.amount_total || 0) / 100;
    }
  }

  return referrals;
}
```

---

## Full Report Script

Save as `scripts/stripe-report.ts` and run with `npx tsx scripts/stripe-report.ts`:

```typescript
import Stripe from 'stripe';
import * as dotenv from 'dotenv';
dotenv.config({ path: '.env.local' });

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
});

async function main() {
  // Get all course signups
  const sessions = await stripe.checkout.sessions.list({ limit: 100, status: 'complete' });
  const courseSessions = sessions.data.filter(s => s.metadata?.product === 'claude-code-course');

  // Get waitlist
  const customers = await stripe.customers.list({ limit: 100 });
  const waitlist = customers.data.filter(c => c.metadata?.waitlist === 'premium-skills');

  console.log('=== ClaudeFluent Report ===\n');
  console.log(`Course signups: ${courseSessions.length}`);
  console.log(`Waitlist subscribers: ${waitlist.length}\n`);

  // Group by session
  const bySession: Record<string, any[]> = {};
  for (const session of courseSessions) {
    const sid = session.metadata?.session || 'unknown';
    if (!bySession[sid]) bySession[sid] = [];
    bySession[sid].push({
      name: session.customer_details?.name,
      email: session.customer_details?.email,
      amount: (session.amount_total || 0) / 100,
    });
  }

  console.log('--- Course Signups by Session ---');
  for (const [sessionId, people] of Object.entries(bySession)) {
    console.log(`\n${sessionId.toUpperCase()} (${people.length}):`);
    people.forEach(p => console.log(`  - ${p.name} <${p.email}> — $${p.amount}`));
  }

  console.log('\n--- Waitlist ---');
  waitlist.forEach(c => console.log(`  - ${c.email} (joined ${c.metadata?.waitlist_date || 'unknown'})`));
}

main().catch(console.error);
```

---

## API Endpoint: Get Waitlist

Add to `app/api/waitlist/route.ts`:

```typescript
export async function GET() {
  const customers = await stripe.customers.list({ limit: 100 });
  const waitlist = customers.data
    .filter(c => c.metadata?.waitlist === 'premium-skills')
    .map(c => ({
      email: c.email,
      name: c.name,
      joinedAt: c.metadata?.waitlist_date,
    }));

  return NextResponse.json({ count: waitlist.length, subscribers: waitlist });
}
```

Access at: `GET /api/waitlist`

---

## Running Scripts

```bash
cd ~/Programming/personal-master/personal/claude_course/website
npx tsx scripts/stripe-report.ts
```

## Bulk / Team Purchases

Bulk purchases create ONE Stripe checkout session for the buyer with `quantity > 1`. Only the buyer appears in Stripe; team members are tracked separately in `lib/manual-participants.ts`.

**Revenue counting:** The buyer's Stripe `amount_total` covers all seats. Team members in the manual file have $0 in Stripe. Don't double-count.

**How /participants works:**
- `/api/participants` fetches all Stripe checkout sessions with `product === 'claude-code-course'`
- Then merges in entries from `lib/manual-participants.ts`, deduplicating by email
- Manual entries have `paymentIntentId` starting with `manual_` (no Stripe record)
- The `paidBy` field on manual entries indicates who bought their seat

**Bulk purchase log:**
- **2026-02-09 — AcuityMD PMM** (6 seats): Buyer: Kirsten Lundquist (kirsten.lundquist@acuitymd.com). $599/seat × 6 = $3,594. Session: weekday4. Checkout page: `/acuity-pmm`. Team: Luke Peddemors, Ramya Rajan, Seth Engel, Natalie Berkowitz, Gagan Bhatia.

**To add future bulk purchases:**
1. Add entries to `lib/manual-participants.ts` with `paidBy` for team members
2. Use `/api/send-welcome` (POST, password-protected) to send welcome emails
3. The buyer's Stripe session handles revenue; manual entries handle team roster

---

## Notes

- Checkout sessions: `metadata.product === 'claude-code-course'`
- Waitlist customers: `metadata.waitlist === 'premium-skills'`
- LinkedIn URL captured via `custom_fields` during checkout
- Affiliate tracking via `metadata.ref`
- Stripe rate limit: ~100 requests/second
- Use pagination (`starting_after`) for large datasets
- **Bulk purchases:** quantity stored on line item, only buyer in Stripe. See "Bulk / Team Purchases" above.
