---
name: imessage
description: "Read and send iMessages using custom SQLite-based tools (more reliable than MCP). Use this skill whenever Travisse wants to check unread texts, send a text/iMessage, search contacts, read message history, look up a conversation, or find a specific message. Also trigger when he says 'text', 'message', 'iMessage', 'check my texts', 'send a text to', 'what did X say', or references any messaging conversation. Triggers on: iMessage, text, send text, check texts, unread messages, message history, send a message to, what did they say, search messages, contacts."
---

# iMessage Tools

Use the custom iMessage tools at `~/.config/imessage-tools/imessage.js` for all messaging tasks. These are MORE RELIABLE than any MCP server because they use direct SQLite database access.

## Features
- Reads messages from `attributedBody` blobs (newer macOS stores text there)
- Extracts **voice memo transcriptions** automatically (marked with `[Voice Memo]` prefix)
- Resolves phone numbers to contact names across all iCloud contact sources
- Copies DB files to temp for latest WAL data

## Available Commands

```bash
# Get unread messages (with contact name resolution)
node ~/.config/imessage-tools/imessage.js unreads [limit]

# Search contacts by name, phone, or email
node ~/.config/imessage-tools/imessage.js search-contacts "query"

# Find contact by phone number
node ~/.config/imessage-tools/imessage.js find-contact 8015551234

# Get recent messages from a contact or group chat
node ~/.config/imessage-tools/imessage.js messages "Stephanie Hansen" 20
node ~/.config/imessage-tools/imessage.js messages "Bishopric-SM" 50
node ~/.config/imessage-tools/imessage.js messages +18015551234 20

# List all group chats
node ~/.config/imessage-tools/imessage.js groups

# Send a message
node ~/.config/imessage-tools/imessage.js send "+18015551234" "Hey, running late!"
```

## Workflow for Sending Messages

1. **Find the recipient's phone number:**
   ```bash
   node ~/.config/imessage-tools/imessage.js search-contacts "Steph"
   ```

2. **Send the message using their phone number:**
   ```bash
   node ~/.config/imessage-tools/imessage.js send "+14358622448" "Hey!"
   ```

3. **Always use the phone number for sending**, not the contact name.

## Writing Style

When drafting messages for Travisse, use `$travisse-writing-style` for tone and patterns:
- Default opener: "Hey" or "Hey [Name]"
- Warm but direct
- Minimal emoji usage
- Use softeners like "just" and "would you be up for..."

## When to Use These Tools vs MCP

**Always prefer the custom tools.** The iMessage MCP has issues:
- Requires Contacts.app to be running
- AppleScript is flaky and fails silently
- Can't search contacts by phone number

The custom tools use direct SQLite access to:
- `~/Library/Messages/chat.db` - Messages
- `~/Library/Application Support/AddressBook/Sources/*/AddressBook-v22.abcddb` - Contacts (multiple iCloud sources)

## Troubleshooting

If you get permission errors, ensure the terminal app has:
- Full Disk Access (System Settings → Privacy & Security)
- Automation permissions for Messages app
