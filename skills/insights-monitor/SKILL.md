---
name: insights-monitor
description: Automated analysis of messages and data to surface actionable items. Use when running diagnostics on incoming data or checking for insights.
---

# Insights Monitor

Automated analysis of messages and data to surface actionable items.

## Quick Check

Run manually to get current insights:
```bash
node ~/.config/insights-monitor/analyze.js
```

## What It Analyzes

1. **Brex spending** - High spend, duplicate subscriptions
2. **Unread messages** - Multiple unreads from same person, unanswered questions
3. **Commitments** - Things you said you'd do (searches for "I'll send", "by Friday", etc.)

## Output

Reports saved to: `~/.config/insights-monitor/reports/`

## Setting Up Automated Monitoring (Optional)

To run daily at 8am:
```bash
crontab -e
# Add:
0 8 * * * /usr/local/bin/node ~/.config/insights-monitor/analyze.js >> ~/.config/insights-monitor/cron.log 2>&1
```

## Integration with Claude

When user asks for:
- "daily review"
- "what should I focus on?"
- "any insights?"
- "check my messages"

Run the analyzer and present findings, asking if they want to add items to their to-do list.

## Example Workflow

```
User: "What should I focus on today?"

Claude:
1. Runs: node ~/.config/insights-monitor/analyze.js --json
2. Parses high/medium priority items
3. Presents them:
   "Based on your messages and spending:
   - Stephanie has 3 unread messages (might be waiting on you)
   - Figma spending is $591/mo - worth reviewing
   - You told Todd you'd send the proposal by Friday

   Want me to add any of these to your to-do list?"
```
