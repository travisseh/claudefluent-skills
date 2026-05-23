---
name: linkedin
description: "Check and respond to LinkedIn messages and notifications using dev-browser browser automation. Use when checking LinkedIn inbox, drafting replies, or following up on conversations."
---

# LinkedIn Messages

Use `$dev-browser` for LinkedIn messages and notifications.

## Check Messages Workflow

1. Use `dev-browser --connect`.
2. Reuse a named page such as `browser.getPage("linkedin")`.
3. Navigate to `https://www.linkedin.com/messaging/` if needed.
4. Use Playwright locators to inspect the conversation list, open a thread, and read the message pane.
5. Draft replies in the thread box, but do not send without explicit approval.

## Check Notifications

1. Use the same named page or a second named page like `browser.getPage("linkedin-notifications")`.
2. Navigate to `https://www.linkedin.com/notifications/`.
3. Read the page with locators, `textContent`, or `snapshotForAI`.

## Writing Style

Before drafting ANY LinkedIn message or reply:
- Read `$travisse-writing-style` and use it as the only source of truth
- Apply the `### LINKEDIN` section for hooks, structure, and formatting
- Apply the Example Company safety check before proposing anything public-facing
- Keep DMs warm, direct, and concise
- Match the user's casual-professional style

## Output Format

After scanning messages, present:

```
## LinkedIn Messages

### Needs Response
- [Name]: [Topic/last message summary] — [Suggested action]
- [Name]: [Topic/last message summary] — [Suggested action]

### FYI (no response needed)
- [Name]: [Summary]

### Draft Replies
[If asked to draft, present each draft for approval before sending]
```

## Important Notes

- Prefer `browser.listPages()` if you need to inspect existing tabs
- LinkedIn may require being logged in — if you see a login page, tell the user
- Don't send messages without explicit approval
- For LinkedIn posts/content creation, use `$travisse-writing-style`
