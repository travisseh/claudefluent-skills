---
name: slack
description: "Read and send Slack messages across ExampleCo, ReviewCo, and Example Agency workspaces using custom tools. Use this skill whenever the user wants to check Slack unreads, send a Slack message, search Slack history, read a channel, or manage any Slack communications. Also trigger when they say 'check Slack', 'message X on Slack', 'what did they say on Slack', 'Slack unreads', or reference any ExampleCo/ReviewCo/Example Agency Slack conversation. Triggers on: Slack, check Slack, Slack message, Slack unreads, send on Slack, Slack channel, ExampleCo Slack, ReviewCo Slack, Example Agency Slack, Slack search."
---

# Slack Tools

Use the custom Slack tools at `~/.config/slack-tools/slack.js` for all Slack messaging tasks across ExampleCo, ReviewCo, and Example Agency workspaces.

## Setup

Workspaces must be configured with User OAuth tokens (xoxp-...) before use:

```bash
node ~/.config/slack-tools/slack.js workspaces
```

## Available Commands

```bash
# Get summary of unreads across all workspaces
node ~/.config/slack-tools/slack.js summary

# Get unread messages (all workspaces or specific)
node ~/.config/slack-tools/slack.js unreads
node ~/.config/slack-tools/slack.js unreads exampleco

# Get DM conversations
node ~/.config/slack-tools/slack.js dms
node ~/.config/slack-tools/slack.js dms exampleco 20

# Get starred messages/channels (requires legacy stars:read scope)
node ~/.config/slack-tools/slack.js starred
node ~/.config/slack-tools/slack.js starred gmr

# Get @mentions
node ~/.config/slack-tools/slack.js mentions
node ~/.config/slack-tools/slack.js mentions exampleco 30

# Get messages from a specific channel
node ~/.config/slack-tools/slack.js messages exampleco general 50
node ~/.config/slack-tools/slack.js messages exampleco "#product" 20

# Get thread replies
node ~/.config/slack-tools/slack.js thread exampleco general 1234567890.123456

# Send a message
node ~/.config/slack-tools/slack.js send exampleco "#general" "Hello team!"
node ~/.config/slack-tools/slack.js send exampleco john.doe "Hey John!"

# Reply in a thread
node ~/.config/slack-tools/slack.js send exampleco general --thread 1234567890.123456 "Thread reply"

# Schedule a message
node ~/.config/slack-tools/slack.js send exampleco "#general" --schedule "2025-01-15T09:00:00" "Good morning!"

# Add reaction
node ~/.config/slack-tools/slack.js react exampleco general 1234567890.123456 thumbsup

# Search messages
node ~/.config/slack-tools/slack.js search exampleco "quarterly report"
node ~/.config/slack-tools/slack.js search --all "customer feedback"
```

## Workflow for Responding to Messages

1. **Check summary first:**
   ```bash
   node ~/.config/slack-tools/slack.js summary
   ```

2. **Get unreads for workspaces with activity:**
   ```bash
   node ~/.config/slack-tools/slack.js unreads exampleco
   ```

3. **Read full context if needed:**
   ```bash
   node ~/.config/slack-tools/slack.js messages exampleco product 50
   ```

4. **Send response:**
   ```bash
   node ~/.config/slack-tools/slack.js send exampleco "#product" "Response message"
   ```

## Writing Style

When drafting Slack messages for the user, use `$user-writing-style` as the source of truth:
- Casual, direct tone
- Minimal emoji usage
- Short sentences

## Workspace Names

- `exampleco` - ExampleCo team workspace
- `gmr` - ReviewCo workspace
- `example-agency` - Example Agency Design workspace
