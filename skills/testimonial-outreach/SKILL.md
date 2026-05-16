---
name: testimonial-outreach
description: Find ClaudeFluent students who agreed to (or are likely to give) testimonials but aren't yet on the site, and draft testimonial-ask emails in Gmail. Use when the user says "find testimonial gaps", "who said yes to a testimonial", "draft testimonial asks", "ask the [class] cohort for testimonials", or wants to compare a Notion participant/stoked list against the live site.
---

# Testimonial Outreach

End-to-end flow for: identifying who agreed to (or is likely to give) a ClaudeFluent testimonial, comparing against the live site, and drafting threaded testimonial-ask emails in Gmail.

## When to use
- "Find people who said yes to testimonials but aren't on the site yet"
- "Draft testimonial asks for the [Solv/ClassDojo/etc] cohort"
- "Who from the [Notion participant table] should I ask for a testimonial?"
- Quarterly testimonial-gap audits

## Step 1: Pull the current site testimonial list

The full testimonial array lives in:
`~/Programming/personal-master/personal/claude_course/website/app/HomeContent.tsx`

Find the `ALL_TESTIMONIALS` constant. Extract `name`, `company`, and a short quote fingerprint for each entry. Treat that as the "already on site" set.

```bash
rg -n "name:" ~/Programming/personal-master/personal/claude_course/website/app/HomeContent.tsx | head -40
```

Also note the `trusted-by` logo array in the same file — those companies have logo presence but not necessarily individual testimonials.

## Step 2: Search Example Agency Gmail for testimonial agreements

the user asks for testimonials almost exclusively from `user@example.com`. Use the gmail CLI.

```bash
# Broad sweep for any testimonial-related thread
node ~/.config/gmail-tools/gmail.js search example-agency "testimonial" 50

# Replies to his standard follow-up template
node ~/.config/gmail-tools/gmail.js search example-agency "subject:Re: Thanks for joining and 3 things for you" 100

# His common testimonial-ask phrasings
node ~/.config/gmail-tools/gmail.js search example-agency "would you be ok if I used" 50
node ~/.config/gmail-tools/gmail.js search example-agency "happy to provide" 30

# Read a specific thread
node ~/.config/gmail-tools/gmail.js read example-agency "from:<person> subject:..."
```

A "yes" looks like:
- Direct: "Yes please use my testimonial", "I gotchu boo", "Yes to both", "Feel free to use my LinkedIn one"
- Constrained: "fine to use if anonymized" — record the constraint
- Pre-committed: "happy to provide a testimonial" before the class (often tied to a discount)
- Edited quote: a verbatim quote the person wrote back — that's a yes plus a deliverable

Skip:
- Replies that are just access/logistics questions
- Replies that didn't address the testimonial ask

## Step 3 (optional): Read a Notion participant table for "stoked" rankings

After private team classes the user sometimes builds a participant table in Notion with a "Stoked?" column (free text — "Yes", "Maybe", "pretty stoked", "probably a solid no", etc.).

```bash
# Top-level page metadata (does NOT render tables)
node ~/.config/notion-tools/notion.js read <page-id>

# Tables are child blocks. Get the block list, find table blocks, then fetch rows directly:
curl -s "https://api.notion.com/v1/blocks/<page-id>/children?page_size=100" \
  -H "Authorization: Bearer <NOTION_API_TOKEN>" \
  -H "Notion-Version: 2022-06-28"

# Then for each table block id, fetch its rows:
curl -s "https://api.notion.com/v1/blocks/<table-block-id>/children?page_size=100" \
  -H "Authorization: Bearer <NOTION_API_TOKEN>" \
  -H "Notion-Version: 2022-06-28" | python3 -c "
import json, sys
d = json.load(sys.stdin)
for row in d.get('results', []):
    cells = row.get('table_row', {}).get('cells', [])
    print(' | '.join(''.join(t.get('plain_text','') for t in cell) for cell in cells))
"
```

Stoked-column heuristics:
- **Ask:** "Yes", "pretty stoked", "Likely", "Medium - down for referral", "seemed to like it"
- **Skip:** "No", "probably a solid no", "I don't think so", "Maybe? I can't remember", blanks

Treat "would be down for a referral but not a testimonial" as a separate bucket — don't put them in the testimonial ask batch; flag them for a different outreach.

## Step 4: Build the gap list

For each "yes" or stoked-enough person, check whether they're already on the site (Step 1 list). The remainder is the gap.

Output for the user: a short bulleted list with name, company, email, verbatim approval (or stoked-column text), and any constraint (e.g., "anonymized only", "logo only").

## Step 5: Draft the asks in Gmail

Use the `gmail.js draft-reply` command for people who got the original "Thanks for joining and 3 things for you" follow-up — it stays in the same thread for context.

**Critical bug to work around:** `gmail.js draft-reply` derives the `To:` from the `From:` of the most recent message in the thread. When the user sent the last message himself (e.g., the original "Thanks for joining" template), the draft will be addressed to the user, not the recipient.

**Workaround:** use the Gmail API directly via a small node script with the Example Agency service account. The example-agency service account's `service-accounts.json` entry only has `https://mail.google.com/` — use that single scope, not the broader list, or auth will fail with `unauthorized_client`.

```js
const { google } = require('~/.config/gmail-tools/node_modules/googleapis');
const key = require('~/.config/example-agency-email/service-account.json');

const auth = new google.auth.JWT({
  email: key.client_email,
  key: key.private_key,
  scopes: ['https://mail.google.com/'], // single broad scope ONLY
  subject: 'user@example.com',
});

// For threaded drafts, fetch original message headers and stitch In-Reply-To / References:
const orig = await gmail.users.messages.get({
  userId: 'me',
  id: threadId,
  format: 'metadata',
  metadataHeaders: ['Subject', 'Message-ID', 'References'],
});
const ohdrs = {};
for (const h of orig.data.payload.headers) ohdrs[h.name] = h.value;
const subject = ohdrs.Subject.startsWith('Re:') ? ohdrs.Subject : `Re: ${ohdrs.Subject}`;
const inReplyTo = ohdrs['Message-ID'] || '';
const refs = ohdrs['References'] ? `${ohdrs['References']} ${inReplyTo}` : inReplyTo;

const raw = Buffer.from(
  `From: user@example.com\r\nTo: ${recipientEmail}\r\nSubject: ${subject}\r\nIn-Reply-To: ${inReplyTo}\r\nReferences: ${refs}\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n${body}`
).toString('base64url');

await gmail.users.drafts.create({
  userId: 'me',
  requestBody: { message: { raw, threadId } },
});
```

For people who never got the original "Thanks for joining" template (e.g., added to a class late), drop the `threadId` and create a fresh draft with subject like `Quick ClaudeFluent follow-up`.

## the user's voice for testimonial asks

Keep it casual, short, no hashtags, lowercase first character of "couple" / "would" after greeting is fine. Pair the ask with a value-add (offer to send a guide/example). Do NOT offer to "jump on a call" — the user cut that line.

### Template — threaded reply (already in the post-class thread)

```
Hey {Name}, couple of things if you're up for them:

1. Would you be down to share a short testimonial about the class for the ClaudeFluent site? Just a sentence or two on what stood out or what you've been able to build/automate since.

2. Anything you've been stuck on or questions that have come up since class? Happy to send over a guide/example if it'd help - I'd rather you actually use this stuff than just have it sit there.

No worries if not.

the user
```

### Template — new email (no prior follow-up thread)

```
Hey {Name},

Quick follow-up from the {ClassName} class - hope things are going well.

Couple of things:

1. Would you be down to share a short testimonial I could put on the ClaudeFluent site? A sentence or two on what stood out or what you've been able to apply since the class{personal-callback-if-known}.

2. Anything you've been stuck on or questions that have come up since class? Happy to send over a guide/example if it'd help - I'd rather you actually use this stuff than just have it sit there.

No sweat if neither - just figured I'd ask.

the user
```

If you have a specific quote candidate (e.g., from a Grain transcript), use the older variant: "Would you be ok if I used the following quote (or whatever you'd like to write) for a testimonial?" and inline the quote.

## Step 6: Verify the drafts

Always confirm the `To:` is correct after creation:

```bash
node ~/.config/gmail-tools/gmail.js search example-agency "in:drafts" 10
```

If any draft shows `to: the user Hansen <user@example.com>`, that's the bug — delete and recreate via the API script above.

## Constraints

- **Never send.** Always drafts only. the user reviews and sends manually.
- **No hashtags** in any draft.
- **Don't offer phone calls** — the user removed that.
- **Respect anonymization requests** — e.g., Denise Lu agreed only if anonymized; that's a different category of testimonial (generic role + quote, no name/LinkedIn).
- **Don't include people from the "referral only / not stoked" buckets** in a testimonial batch — flag them separately so the user can decide on a different ask.
