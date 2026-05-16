---
name: inbox-watch
description: Hourly email watch. Scans unread Gmail across personal/exampleco/gmr/example-agency, marks noise as read, drafts threaded replies to anything important needing a response, and pings Telegram if a real human is waiting on the user. Use when running an hourly routine, when the user says "watch my inbox", "check email and draft replies", "see if anyone important emailed", or any unattended/scheduled email triage. Designed to be safe to run on a recurring schedule — does NOT send anything, drafts only, and dedupes via state file so it never double-drafts.
---

# Inbox Watch

Unattended email triage. Designed to run hourly via a routine but also safe to run manually.

## What this skill does (and does not do)

**DOES:**
- List unread Gmail across all 4 accounts (does NOT auto-mark)
- Classify each unread as **noise** (spam/marketing/automated/transactional/cold outreach) vs **needs-attention** (real human, addressed to the user, not already replied)
- Mark NOISE as read so the inbox clears
- For needs-attention items: create a **threaded Gmail draft** via `draft-reply` (NEVER sends)
- Send a single Telegram notification summarizing what's waiting on the user, with one line per important email

**DOES NOT:**
- Send any email
- Mark important emails as read (they stay unread so the user sees them in his inbox)
- Re-draft emails it already drafted in a prior run (uses state file to dedupe)
- Answer questions or interact — runs end-to-end without input

## State

Path: `~/.claude/state/inbox-watch/handled.json`

Format:
```json
{
  "handled": [
    {
      "messageId": "abc123",
      "threadId": "thread-abc",
      "account": "exampleco",
      "draftId": "draft-xyz",
      "from": "person@example.com",
      "subject": "...",
      "drafted_at": "2026-05-08T11:00:00Z"
    }
  ]
}
```

Garbage-collect entries older than 7 days at the start of each run (the user will have either sent or deleted the draft by then; if not, re-drafting is fine).

If the file doesn't exist, treat as empty and create it after the run.

## Steps

### 1. Load state
```bash
mkdir -p ~/.claude/state/inbox-watch
test -f ~/.claude/state/inbox-watch/handled.json || echo '{"handled":[]}' > ~/.claude/state/inbox-watch/handled.json
```

Read the JSON. Build a Set of `messageId` values already handled in the last 7 days. Drop entries older than 7 days.

### 2. Pull unread from all 4 accounts (parallel)

Only look at the last 5 days. This skill runs hourly so older unread emails are either already-handled or stale and not worth re-processing every cycle.

```bash
node ~/.config/gmail-tools/gmail.js search personal "is:unread newer_than:5d" 30
node ~/.config/gmail-tools/gmail.js search exampleco "is:unread newer_than:5d" 30
node ~/.config/gmail-tools/gmail.js search gmr "is:unread newer_than:5d" 30
node ~/.config/gmail-tools/gmail.js search example-agency "is:unread newer_than:5d" 30
```

If any account fails (auth error, etc.), record it and continue with the others. Include the failure in the Telegram notification at the end.

### 3. Classify each unread

For every message, decide: NOISE or NEEDS-ATTENTION.

**NOISE (mark as read, do not draft, do not notify):**
- Cold outreach / sales pitches / vendor spam
- Automated notifications: DMARC, Zapier, Instagram, Substack, newsletters, SaaS product updates, GitHub digests
- Mass emails / mailing lists / group CCs where the user isn't specifically addressed
- Transactional: receipts, password resets, shipping notifications, payment confirmations
- Anything from a no-reply / noreply / do-not-reply address
- Doctor Kiltz / political fundraising / generic SaaS pitches the user never engaged with
- Gusto/payroll for the dormant Example Agency LLC entity (per chief-of-staff insights — always ignore)

**NEEDS-ATTENTION (draft a reply, notify the user):**
- Real human sender (named, real domain, not a no-reply)
- the user is in TO (not BCC/mass-CC)
- Asks a question, requests action, expects a reply, or someone is blocked on him
- Sender is family, colleague, student, customer, church member, partner, investor, or anyone he has an existing relationship with

When in doubt: lean toward NEEDS-ATTENTION. False-positive notifications are cheap; missing a real email is expensive.

### 4. Skip drafted-already

Filter out any NEEDS-ATTENTION message whose `messageId` is already in the state file. Those still go in the Telegram summary as "still waiting on you to send" but skip the drafting step.

### 5. Verify no reply already sent

For each NEEDS-ATTENTION message NOT already in state, do a fast check that the user hasn't already replied (sometimes he replies on his phone before the cron runs):

```bash
node ~/.config/gmail-tools/gmail.js search <account> "from:me to:<sender-email> subject:<subject> after:<message-date>" 1
```

If a sent reply exists in that thread already, mark the original message as read (it's handled) and move on — do not draft, do not notify.

### 6. Mark noise as read (batch per account)

Collect all NOISE message IDs per account and run one `mark-read` per account:
```bash
node ~/.config/gmail-tools/gmail.js mark-read <account> <id1>,<id2>,<id3>
```

### 7. Draft replies for new NEEDS-ATTENTION items

For each new (not-already-drafted, not-already-replied) NEEDS-ATTENTION message:

1. Read full content for context:
   ```bash
   node ~/.config/gmail-tools/gmail.js read <account> "rfc822msgid:<message-id>"
   ```
   (Or fall back to a `from:sender subject:topic` query.)

2. Compose a reply in the user's voice. Reference `~/.claude/skills/user-writing-style/SKILL.md` and `~/.claude/CLAUDE.md` for tone:
   - "Hey [first name]" opener for people he knows
   - Warm but direct, concise, minimal emoji
   - Adjust formality: casual for family, warm-professional for church, direct for work
   - **NEVER use em-dashes** — use hyphens with spaces or restructure
   - Don't promise specifics (dates, numbers) the user hasn't authorized — write a placeholder like "[I'll confirm the date by Friday]" so he can edit before sending
   - For genuinely ambiguous emails where any reply would be guessing, write a short "received, will respond properly soon" holding reply, NOT a substantive answer

3. Create the threaded draft:
   ```bash
   node ~/.config/gmail-tools/gmail.js draft-reply <account> "from:sender subject:topic" "Reply body"
   ```
   Capture the returned `draftId`.

4. Append to the state file:
   ```json
   {
     "messageId": "<original message id>",
     "threadId": "<thread id>",
     "account": "<account>",
     "draftId": "<returned draft id>",
     "from": "<from header>",
     "subject": "<subject>",
     "drafted_at": "<ISO timestamp>"
   }
   ```

### 8. Persist state

Write the updated state back to `~/.claude/state/inbox-watch/handled.json` (pruned to last 7 days + any new entries).

### 9. Telegram notification (only if there's something to say)

Build a summary in `/tmp/inbox-watch-msg.txt`. If the count of NEEDS-ATTENTION is **zero** AND there were no auth failures, skip Telegram entirely (don't spam the user with "all clear" pings every hour).

Otherwise, format:

```
📬 Inbox Watch — <Day> <HH:MM> MT

NEW (drafts ready to review):
- [exampleco] Brixton: Q2 roadmap question
- [example-agency] Sarah Lin: ClassDojo training scope

STILL PENDING (drafted earlier, you haven't sent yet):
- [example-agency] Ana Dacol: Refund follow-up (drafted 2h ago)

NOISE CLEARED: 14 emails marked read.

Auth issues: gmr (token expired)
```

Send via:
```bash
bash ~/.claude/skills/cron/lib/telegram-self.sh personal /tmp/inbox-watch-msg.txt
```

(Default bot: `personal`. The routine prompt may override by passing a different bot name.)

Keep the body under 4000 chars (`telegram-self.sh` chunks but readability degrades). If there are >10 NEW items, list the top 5 by urgency and append "(+N more in inbox)".

## Operating rules (do not violate)

- **NEVER use `gmail.js reply` or `gmail.js send`** in this skill. Always `draft-reply` or `draft`.
- **NEVER mark a needs-attention message as read.** the user must see them in his inbox.
- **NEVER drop a message silently.** Either NOISE → mark-read, or NEEDS-ATTENTION → draft + notify, or already-handled → record in summary as pending.
- **NEVER skip the dedupe check.** Re-drafting the same email every hour will pollute Drafts and erode trust in the system.
- **NEVER promise specifics in drafts.** Use placeholders the user can fill in before sending.
- **If unsure whether to mark as read, leave it unread.** Erring on the side of "the user sees it" is always correct.

## Manual test (before scheduling hourly)

Run once interactively:
```
/inbox-watch
```
or have the user invoke this skill directly. Verify:
1. Drafts appear in Gmail Drafts folder (correctly threaded)
2. Noise emails get marked read
3. Important emails stay unread
4. Telegram message arrives with a clean summary
5. State file at `~/.claude/state/inbox-watch/handled.json` is populated
6. A second run within 5 minutes does NOT re-draft the same items (dedupe works)
