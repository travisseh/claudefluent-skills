---
name: groupme
description: Read Travisse's configured GroupMe groups and optionally post as Travisse using the repo-local GroupMe helper. Use when checking HF2 ward, bishopric, YM, YW, EQ, or GroupMe messages, summarizing recent GroupMe activity, or drafting/sending an approved GroupMe message.
---

# GroupMe

Use the repo-local helper in `/Users/you/Programming/personal-master/personal`.

## Scope

This skill uses Travisse's GroupMe access token from the repo `.env`, so API actions happen as Travisse Hansen.

Configured ward/bishopric groups are stored in:

- `GROUPME_WARD_GROUP_IDS` - all configured read groups
- `GROUPME_BISHOPRIC_GROUP_ID` - default send/read target for the bishopric group

Current configured groups:

- `HF 2nd Ward YM`
- `Young Women HF2`
- `Bishop's and YW President's`
- `HF Wards YM Leaders`
- `HF2 EQ`
- `2nd Ward Young Men Leaders`

## Commands

Run from `/Users/you/Programming/personal-master/personal`.

List available groups:

```bash
npm run groupme -- groups
```

Read recent messages across configured ward groups:

```bash
npm run groupme -- ward-messages 10
```

Read one group by id:

```bash
npm run groupme -- messages "$GROUPME_BISHOPRIC_GROUP_ID" 20
```

Post as Travisse to a specific group:

```bash
npm run groupme -- post "$GROUPME_BISHOPRIC_GROUP_ID" "message text"
```

## Workflow

For read requests:

1. Use `npm run groupme -- ward-messages 10` by default.
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
- Do not create or use GroupMe bots unless the user explicitly asks to switch away from posting as Travisse.
- Treat broad GroupMe reads as sensitive church context; keep summaries concise and operational.
