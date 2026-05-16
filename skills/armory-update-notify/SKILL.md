---
name: armory-update-notify
description: Notify Slack channels after pushing changes to the ExampleCo Armory. Use when changes have been deployed to the armory and sales/CS teams need to be informed. Trigger with '/armory-notify' or 'notify slack about armory changes'.
---

# Armory Update Notification Skill

Use this skill after pushing changes to the ExampleCo Armory to notify Slack channels.

## Invocation
`/armory-notify` or "notify slack about armory changes"

## Workflow

### Step 1: Gather Changes
Run the following to get recent commits affecting the Armory:

```bash
cd ~/Programming/product2
git log --oneline -10 -- public/apps/exampleco-armory/
```

Also check what specifically changed:
```bash
git diff HEAD~1 --stat -- public/apps/exampleco-armory/
```

### Step 2: Generate Summary
Create a concise, sales-friendly summary of the changes. Format:

```
🚀 Release notes: *Bold headline summarizing the change*

[Body text explaining what changed and why it matters]

View the changes here: https://armory.exampleco.com/#[section]
```

Guidelines for the summary:
- Start with 🚀 Release notes: followed by a *bold headline*
- Keep body text conversational and brief
- Focus on what's useful for sales/CS, not technical details
- Don't mention code changes, file names, or technical implementation
- Include the direct link to the relevant Armory section
- Can @mention people who contributed

### Step 3: Show for Review
Display the draft message to the user and ask for approval or edits using AskUserQuestion.

### Step 4: Send to Channels
Once approved, send to all three channels:

```bash
node ~/.config/slack-tools/slack.js send exampleco pulse-prod-updates "[MESSAGE]"
node ~/.config/slack-tools/slack.js send exampleco home-sales "[MESSAGE]"
node ~/.config/slack-tools/slack.js send exampleco home-cs "[MESSAGE]"
```

### Step 5: Confirm
Tell the user the message was sent to all three channels.

## Target Channels
- `pulse-prod-updates` - Product updates channel
- `home-sales` - Sales team home channel
- `home-cs` - Customer Success team home channel

## Example Output

```
🚀 Release notes: *Pricing section now pulls directly from Stripe*

You'll now see the exact same products and descriptions in the enrollment form and on the armory. Thank you @Braden York for the initiative on getting Stripe super clean!

View the changes here: https://armory.exampleco.com/#price-sheet
```
