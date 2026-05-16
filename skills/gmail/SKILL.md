---
name: gmail
description: Read and send Gmail across personal, ExampleCo, and ReviewCo accounts using custom CLI tools. Use when checking email, sending messages, or managing Gmail.
---

# Gmail Tools

Custom Gmail CLI at `~/.config/gmail-tools/gmail.js` for reading, sending, replying, and downloading attachments.

Prefer this CLI over Gmail MCP/app connectors unless the user explicitly asks for a different path.

## Accounts

- `personal` - userh@gmail.com
- `exampleco` - user@example.com
- `gmr` - user@example.com
- `example-agency` - user@example.com

Use account-specific skills when you need business-specific workflow, but `gmail.js` is the primary CLI reference here.

## Available Commands

```bash
# List accounts
node ~/.config/gmail-tools/gmail.js accounts

# Get inbox from ALL accounts at once
node ~/.config/gmail-tools/gmail.js all 5

# List inbox emails (default: personal, 10)
node ~/.config/gmail-tools/gmail.js inbox personal 10
node ~/.config/gmail-tools/gmail.js inbox exampleco 5

# List unread emails
node ~/.config/gmail-tools/gmail.js unread personal
node ~/.config/gmail-tools/gmail.js unread exampleco 20

# Search emails with Gmail query
node ~/.config/gmail-tools/gmail.js search exampleco "from:shane" 10
node ~/.config/gmail-tools/gmail.js search gmr "subject:update is:unread"

# Read full email content
node ~/.config/gmail-tools/gmail.js read exampleco "from:shane subject:WAGMI"
node ~/.config/gmail-tools/gmail.js read personal "from:greg subject:proposal"

# Send an email
node ~/.config/gmail-tools/gmail.js send personal "john@example.com" "Subject" "Body text here"

# Create a draft (safer - can review before sending)
node ~/.config/gmail-tools/gmail.js draft exampleco "team@exampleco.com" "Update" "Here's the update..."

# Reply to an email (finds email by query, replies in thread)
node ~/.config/gmail-tools/gmail.js reply exampleco "from:shane" "Thanks for sharing!"

# Download all attachments from a matching email
node ~/.config/gmail-tools/gmail.js download personal "from:docusign subject:agreement" /tmp
node ~/.config/gmail-tools/gmail.js download exampleco "has:attachment from:vendor" ~/Downloads
```

## Search Query Syntax

Gmail search operators work:
- `from:email` - From specific sender
- `to:email` - To specific recipient
- `subject:keyword` - Subject contains keyword
- `is:unread` - Unread emails
- `after:2026/01/01` - After date
- `before:2026/01/10` - Before date
- `has:attachment` - Has attachments
- `in:inbox` - In inbox
- `label:name` - With specific label

## Attachment Workflow

Use `download` when the user needs files, not just message text.

```bash
node ~/.config/gmail-tools/gmail.js download <account> "query" [output-dir]
```

- `output-dir` defaults to `/tmp`
- Command returns JSON with message metadata and downloaded file paths
- Use precise Gmail queries to avoid grabbing the wrong message

## Workflow for Responding to Emails

1. **Check all inboxes:**
   ```bash
   node ~/.config/gmail-tools/gmail.js all 5
   ```

2. **Read specific email for context:**
   ```bash
   node ~/.config/gmail-tools/gmail.js read exampleco "from:scott subject:internship"
   ```

3. **Reply in thread:**
   ```bash
   node ~/.config/gmail-tools/gmail.js reply exampleco "from:scott subject:internship" "Thanks Scott, I'll follow up with them today."
   ```

4. **Download attachments if needed:**
   ```bash
   node ~/.config/gmail-tools/gmail.js download exampleco "from:vendor has:attachment" ~/Downloads
   ```

## Writing Style

When drafting emails for the user, use `$user-writing-style` as the source of truth:
- Professional but warm
- Direct and concise
- "Hey [Name]" for casual, "Hi [Name]" for professional

## Token Location

OAuth tokens: `~/.config/gmail-tools/tokens.json`
