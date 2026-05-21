---
name: groupme
description: Read configured GroupMe groups and optionally post through an approved local GroupMe helper. Use when checking organization messages, summarizing recent GroupMe activity, or drafting/sending an approved GroupMe message.
---

# GroupMe

Use the repo-local helper from the user's project checkout.

## Scope

This skill uses the user's GroupMe access token from the repo `.env`, so API actions happen as the authenticated user.

Configured groups are stored in:

- `GROUPME_GROUP_IDS` - all configured read groups
- `GROUPME_DEFAULT_GROUP_ID` - default send/read target

Do not include real group names, IDs, member names, or private organization context in the public skill.

## Commands

Run from the user's project checkout.

List available groups:

```bash
npm run groupme -- groups
```

Read recent messages across configured groups:

```bash
npm run groupme -- group-messages 10
```

Read one group by id:

```bash
npm run groupme -- messages "$GROUPME_DEFAULT_GROUP_ID" 20
```

Post as the authenticated user to a specific group:

```bash
npm run groupme -- post "$GROUPME_DEFAULT_GROUP_ID" "message text"
```

## Workflow

For read requests:

1. Use `npm run groupme -- group-messages 10` by default, or the equivalent command in the local helper.
2. Increase the limit only when the user asks for more history or the context is incomplete.
3. Inspect the `attachments` array as well as `text`. Image attachments include a direct `url`; file attachments include a `file_id`.
4. Summarize by group, sender, timestamp, attachments, and action needed.

For send requests:

1. Draft the message first unless the user explicitly says to send the exact text.
2. Confirm the target group when ambiguous.
3. Send only after explicit approval in the current conversation.
4. After sending, report the target group and a short confirmation, not the access token.

## Safety

- Never print or expose `GROUPME_ACCESS_TOKEN`.
- Do not create or use GroupMe bots unless the user explicitly asks to switch away from posting as the authenticated user.
- Treat broad GroupMe reads as sensitive private organization context; keep summaries concise and operational.
