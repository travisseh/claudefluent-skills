# Integration Registry

Complete reference for all tools available to the chief-of-staff plugin.

## Email

| Account | Address | Tool | Command |
|---------|---------|------|---------|
| Personal | userh@gmail.com | gmail CLI | `node ~/.config/gmail-tools/gmail.js inbox personal 10` |
| ExampleCo | user@example.com | gmail CLI | `node ~/.config/gmail-tools/gmail.js inbox exampleco 10` |
| ReviewCo | user@example.com | gmail CLI | `node ~/.config/gmail-tools/gmail.js inbox gmr 10` |
| Example Agency | user@example.com | gmail CLI (service account) | `node ~/.config/gmail-tools/gmail.js inbox example-agency 10` |

**Quick scan all:** `node ~/.config/gmail-tools/gmail.js all 5`
**Reply (ALWAYS use this for existing threads):** `node ~/.config/gmail-tools/gmail.js reply [account] "[search query to find original msg]" "[reply body]"`
**Send (ONLY for brand-new emails, never for replies):** `node ~/.config/gmail-tools/gmail.js send [account] "[to]" "[subject]" "[body]"`
**Draft:** `node ~/.config/gmail-tools/gmail.js draft [account] "[to]" "[subject]" "[body]"`
**Download attachments:** `node ~/.config/gmail-tools/gmail.js download [account] "[search query]" [output-dir]`

> **CRITICAL:** When replying to an existing email thread, ALWAYS use `reply` not `send`. The `send` command creates a brand-new unthreaded email. The `reply` command finds the original message, sets In-Reply-To/References headers, and passes the threadId so Gmail properly threads the conversation.

## Slack

| Workspace | Tool | Unreads | Send |
|-----------|------|---------|------|
| ExampleCo | slack CLI | `node ~/.config/slack-tools/slack.js unreads exampleco` | `node ~/.config/slack-tools/slack.js send exampleco "#channel" "msg"` |
| ReviewCo | slack CLI | `node ~/.config/slack-tools/slack.js unreads gmr` | `node ~/.config/slack-tools/slack.js send gmr "#channel" "msg"` |
| Example Agency | slack CLI | `node ~/.config/slack-tools/slack.js unreads example-agency` | `node ~/.config/slack-tools/slack.js send example-agency "#channel" "msg"` |

**Summary:** `node ~/.config/slack-tools/slack.js summary`
**Search:** `node ~/.config/slack-tools/slack.js search [workspace] "query"`
**Read channel:** `node ~/.config/slack-tools/slack.js messages [workspace] [channel] [limit]`

## iMessage

| Action | Command |
|--------|---------|
| Unreads | `node ~/.config/imessage-tools/imessage.js unreads [limit]` |
| Messages from contact | `node ~/.config/imessage-tools/imessage.js messages "[Name]" [limit]` |
| Search contacts | `node ~/.config/imessage-tools/imessage.js search-contacts "query"` |
| Send | `node ~/.config/imessage-tools/imessage.js send "+1XXXXXXXXXX" "message"` |
| Groups | `node ~/.config/imessage-tools/imessage.js groups` |

**Key contacts:**
- Steph: `node ~/.config/imessage-tools/imessage.js messages "Stephanie Hansen" 10`

## Calendar

Use the local Google Calendar CLI, not Calendar MCP tools.

**CLI:** `node ~/.config/google-calendar-tools/calendar.js`

**Accounts:** `personal`, `exampleco`, `example-agency`, `gmr`

**List accounts:** `node ~/.config/google-calendar-tools/calendar.js list-accounts`
**List calendars:** `node ~/.config/google-calendar-tools/calendar.js list-calendars personal`
**Current time:** `node ~/.config/google-calendar-tools/calendar.js get-current-time personal America/Denver`
**List events:** `node ~/.config/google-calendar-tools/calendar.js list-events personal '{"calendarId":"primary","timeMin":"2026-04-19T00:00:00","timeMax":"2026-04-19T23:59:59","timeZone":"America/Denver"}'`
**Search events:** `node ~/.config/google-calendar-tools/calendar.js search-events personal '{"calendarId":"primary","query":"dentist","timeMin":"2026-04-01T00:00:00","timeMax":"2026-04-30T23:59:59","timeZone":"America/Denver"}'`
**Create event:** `node ~/.config/google-calendar-tools/calendar.js create-event personal '{"calendarId":"the user HF2","summary":"Building cleaning","start":"2026-04-25T08:30:00","end":"2026-04-25T09:30:00","timeZone":"America/Denver"}'`
**Update event:** `node ~/.config/google-calendar-tools/calendar.js update-event personal '{"calendarId":"the user HF2","eventId":"abc123","summary":"Updated title"}'`

The CLI accepts calendar IDs or calendar names like `primary` or `the user HF2`. It auto-refreshes OAuth tokens from `~/.config/google-calendar-mcp/tokens.json` and blocks exact duplicate event creation unless `allowDuplicates` is set.

## Apple Notes

| Note | ID | Purpose |
|------|-----|---------|
| Bishopric Meeting | 8144 | Running checklist for bishopric |
| Poasts | 7805 | LinkedIn post ideas |
| ClaudeFluent Next Up | 9302 | ClaudeFluent priorities |
| Next Up ReviewCo | 8369 | ReviewCo priorities |
| Life Next Up | 9349 | Overall life priorities |
| 2026 Goals | 5898 | Annual goals |
| Change Log | 6074 | Lessons learned / retrospectives |

**Read:** `python3 ~/.claude/tools/apple-notes.py read [ID]`
**Search:** `python3 ~/.claude/tools/apple-notes.py search "query"`

## Life Backlog (Notion)

the user's unified backlog across all life areas. Use the local Life Backlog CLI, not the old Notion MCP flow.

- **Database URL:** https://www.notion.so/6014a1b687444e26bee8002a1a80b7fc
- **Database ID:** `6014a1b687444e26bee8002a1a80b7fc`
- **Status property type:** `select`
- **Query tasks:** `node ~/.config/notion-tools/notion.js tasks [area=X] [status=X] [assignee=X]`
- **Read task body:** `node ~/.config/notion-tools/notion.js read <pageId>`
- **Search:** `node ~/.config/notion-tools/notion.js search "query"`
- **Create:** `node ~/.config/notion-tools/notion.js create "title" "area" "status"`
- **Append markdown update:** `node ~/.config/notion-tools/notion.js append <pageId> "markdown content"`
- **Replace body with markdown:** `node ~/.config/notion-tools/notion.js update <pageId> "markdown content"`
- **Update status:** `node ~/.config/notion-tools/notion.js status <pageId> "Backlog|To Do|In Progress|Review|Done"`

**Statuses (board columns):** Backlog, To Do, In Progress, Review, Done
**Assignees:** the user, cc, codex, marketing-brain, student-experience, dev
**Areas:** ClaudeFluent, ExampleCo, ReviewCo, Bishopric, Steph/Carson, Mother/Padre, Life Admin
**Initiatives:** Marketing, Ops, Student Experience, Product, Demand Gen, Admin, Sell Prep, Strategic

When writing task content, always write markdown. The CLI converts markdown to proper Notion block types.

When creating tasks, always set Area and Status at minimum. When an agent completes a task, move it to Review (for the user to verify) or Done (if trivial), and prefer appending a short dated markdown update instead of replacing the full page body.

## Writing Style

Before any outbound communication, read:
`$user-writing-style`

## Other Plugins

| Plugin | Command | Purpose |
|--------|---------|---------|
| Marketing Brain | `/marketing-brain:marketing` | ClaudeFluent marketing |
| Marketing Status | `/marketing-brain:marketing-status` | Revenue/funnel dashboard |
| Student Experience | `/student-experience:student-experience` | Class improvements |
| Stripe | `/stripe` | Revenue/customer data |
| Project Selection | `/project-selection` | Evaluate opportunities |
