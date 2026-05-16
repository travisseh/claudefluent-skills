---
name: email-inbox-cleanup
description: Clean up unread Gmail inbox messages across the user's Google Workspace accounts by reviewing recent unread mail, archiving low-value items, and verifying what remains. Use when the user asks to archive irrelevant, unimportant, noisy, promotional, newsletter, notification, or unread emails for personal, ExampleCo, Example Workspace, or ReviewCo accounts.
---

# Email Inbox Cleanup

Use this skill with `$g-workspaces`. It is a Gmail triage workflow for the user's account nicknames: `personal`, `exampleco`, `example-workspace`, and `gmr`.

## Default Workflow

1. Resolve the account from the request. If the account is ambiguous, ask a short clarification.
2. Search unread inbox mail for the requested time window:

```bash
node ~/.config/gmail-tools/gmail.js search <account> "in:inbox is:unread newer_than:7d" 50
```

3. Classify each message from sender, subject, date, and snippet. Read full content only when the snippet is not enough:

```bash
node ~/.config/gmail-tools/gmail.js read <account> "from:sender@example.com subject:keyword"
```

4. Archive only the selected message IDs:

```bash
npx --yes tsx ~/Programming/personal-master/personal/.agents/skills/email-inbox-cleanup/scripts/archive_messages.ts <account> "id1,id2,id3"
```

5. Verify the remaining unread inbox for the same time window:

```bash
node ~/.config/gmail-tools/gmail.js search <account> "in:inbox is:unread newer_than:7d" 50
```

## Archive Criteria

Archive when a message is clearly low-signal for the user:

- newsletters, content digests, webinars, sales nurture, referral promos, and product marketing
- routine DMARC or automated reports with no failure/action signal
- generic platform/admin updates with no account-specific risk or deadline
- receipts for known low-risk tools when the user is doing inbox cleanup, not tax/bookkeeping
- duplicate reminders after a newer or more urgent version remains visible

Do not archive by default:

- direct human messages, replies, customer/student/client/vendor threads, or calendar responses
- payroll, tax, banking, legal, security, access, billing failure, domain, deliverability, or infrastructure alerts
- ClaudeFluent sales/session/student messages, unless the user explicitly says to archive that category
- anything with `action required`, `failed`, `overdue`, `suspended`, `refund`, `chargeback`, `invoice due`, `security`, or `vulnerability` unless the user broadens the rule

If the user explicitly selects a category and says to archive it too, archive those messages even if they would normally be preserved.

## Behavior Rules

- Archive means remove `INBOX`; do not mark read unless the user asks.
- Prefer conservative retention when unsure. Summarize ambiguous items instead of archiving them.
- Never send, reply, delete, unsubscribe, or mark as spam during cleanup unless explicitly requested.
- Report how many messages were archived and what categories remain.
