---
name: check-email
description: Check unread emails from ReviewCo accounts (user@example.com). Use when checking email or reviewing incoming messages for Get More Reviews.
---

# Check Email

Use this skill for ReviewCo mailbox work. Prefer the shared Gmail CLI first:

`node ~/.config/gmail-tools/gmail.js`

## Preferred Usage

```bash
# Unread / inbox
node ~/.config/gmail-tools/gmail.js unread gmr 20
node ~/.config/gmail-tools/gmail.js inbox gmr 10

# Search / read / reply
node ~/.config/gmail-tools/gmail.js search gmr "from:customer is:unread" 10
node ~/.config/gmail-tools/gmail.js read gmr "from:customer subject:question"
node ~/.config/gmail-tools/gmail.js reply gmr "from:customer subject:question" "Reply body"

# Download attachments
node ~/.config/gmail-tools/gmail.js download gmr "has:attachment from:vendor" /tmp
```

## Legacy Fallback

Use this only if `gmail.js` is unavailable or broken:

```bash
cd ~/Programming/personal-master/gmr-marketing/apps/cold-email
npx tsx src/email-engine/check-unread.ts user@example.com 7
```

## Notes

- `gmail.js` is now the source of truth for normal ReviewCo inbox work
- The legacy script is still useful for quick unread sweeps if the shared CLI is down
