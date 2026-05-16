---
name: calendar
description: Read and manage Google Calendar across personal, ExampleCo, Example Agency, and ReviewCo accounts using the local calendar CLI. Use when checking schedules, listing calendars, searching events, creating calendar events, or updating calendar events.
---

# Calendar CLI

Use the local Google Calendar CLI at `~/.config/google-calendar-tools/calendar.js`.

Prefer this CLI over Calendar MCP/app connectors unless the user explicitly asks for a different path.

## Accounts

- `personal` - userh@gmail.com
- `exampleco` - user@example.com
- `example-agency` - user@example.com
- `gmr` - user@example.com

## Available Commands

```bash
# List configured calendar accounts
node ~/.config/google-calendar-tools/calendar.js list-accounts

# List calendars on an account
node ~/.config/google-calendar-tools/calendar.js list-calendars personal

# Get current time in a timezone
node ~/.config/google-calendar-tools/calendar.js get-current-time personal America/Denver

# List events in a time window
node ~/.config/google-calendar-tools/calendar.js list-events personal '{"calendarId":"primary","timeMin":"2026-04-19T00:00:00","timeMax":"2026-04-19T23:59:59","timeZone":"America/Denver"}'

# Search events by text query
node ~/.config/google-calendar-tools/calendar.js search-events personal '{"calendarId":"primary","query":"bishopric","timeMin":"2026-04-01T00:00:00","timeMax":"2026-04-30T23:59:59","timeZone":"America/Denver"}'

# Create an event
node ~/.config/google-calendar-tools/calendar.js create-event personal '{"calendarId":"the user HF2","summary":"Building cleaning","start":"2026-04-25T08:30:00","end":"2026-04-25T09:30:00","timeZone":"America/Denver"}'

# Update an event
node ~/.config/google-calendar-tools/calendar.js update-event personal '{"calendarId":"the user HF2","eventId":"abc123","summary":"Updated title"}'

# Delete an event
node ~/.config/google-calendar-tools/calendar.js delete-event personal '{"calendarId":"the user HF2","eventId":"abc123"}'
```

## Workflow

1. Call `get-current-time` first when relative dates like "today", "tomorrow", or "next Saturday" matter.
2. Call `list-calendars` before scheduling on an unfamiliar account so you pick the right calendar.
3. Use calendar names like `primary` or `the user HF2` when convenient; the CLI resolves them to IDs.
4. When creating events, pass local times with `timeZone` such as `America/Denver`.
5. The CLI blocks exact duplicate events by default. Set `allowDuplicates` in the JSON payload only when duplication is intentional.

## Notes

- OAuth credentials live at `~/.config/google-calendar-mcp/gcp-oauth.keys.json`.
- Tokens live at `~/.config/google-calendar-mcp/tokens.json`.
- The CLI auto-refreshes OAuth tokens when needed.
