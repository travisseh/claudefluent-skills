---
name: proactive-insights
description: Proactively identify actionable insights from messages, financial data, and calendar events. Use when reading personal data to surface action items for Travisse's to-do list.
---

# Proactive Insights & Action Items

When reading messages, financial data, calendar events, or other personal data, Claude should **proactively identify actionable insights** and ask Travisse if he wants to add them to his to-do list.

## What to Look For

### Financial Patterns (Brex, bank messages)
- **Recurring charges that seem high** - "You're spending $X/mo on [service]. Want to review if you're still using it?"
- **Duplicate subscriptions** - Multiple AI tools, multiple hosting providers, etc.
- **Unusual charges** - Significantly higher than typical amounts
- **Failed payments** - Needs attention
- **Spending trends** - "Your [category] spending increased 30% this month"

### Message-Based Action Items
- **Commitments made** - "I'll send that by Friday" → Add follow-up reminder
- **Requests from others** - Someone asking Travisse to do something
- **Unanswered questions** - Messages that need a response
- **Scheduled meetings mentioned** - "Let's meet Tuesday" → Verify it's on calendar
- **Follow-ups needed** - "I'll check and get back to you" from someone else

### Calendar/Scheduling
- **Prep needed** - Meetings that need preparation
- **Conflicts** - Double-bookings or tight scheduling
- **Missing invites** - Mentioned meetings not on calendar

### Health/Personal Patterns
- **Routine disruptions** - Late nights, skipped workouts mentioned
- **Stress indicators** - Frustration in messages, overwhelm signals

## How to Surface Insights

When you notice something actionable:

1. **Mention it naturally** in your response
2. **Ask if they want to add it** to their to-do list
3. **Be specific** about the action and why

### Example Prompts

```
"I noticed you're paying $591/mo for Figma across 3 charges - that seems like multiple subscriptions. Want me to add 'Review Figma subscriptions for consolidation' to your to-do list?"

"Todd asked you to send the proposal by Friday. Should I add 'Send proposal to Todd (due Friday)' to your tasks?"

"You mentioned you'd follow up with Jamie about the meeting. Want me to track that?"

"Your Brex spending on AI tools is ~$600/mo across Claude, ChatGPT, and OpenAI. Might be worth reviewing which ones you actually use. Add to to-do?"
```

## When to Be Proactive vs. Quiet

**Be proactive when:**
- Clear action item that could be forgotten
- Financial pattern worth reviewing (>$50/mo potential savings)
- Commitment with a deadline
- Something that seems to fall through the cracks

**Stay quiet when:**
- Minor, one-off expenses
- Casual conversation, no action needed
- User is clearly focused on something else
- Already tracking the item

## Integration with TodoWrite

When the user agrees to add something, use TodoWrite to add it:
```
{
  "content": "Review Figma subscriptions - may have duplicates ($591/mo)",
  "status": "pending",
  "activeForm": "Reviewing Figma subscriptions"
}
```

## Daily/Weekly Review Prompt

If Travisse asks for a "daily review" or "weekly review", compile insights from:
- Unread messages needing response
- Upcoming calendar prep
- Financial patterns from recent charges
- Outstanding commitments from messages
