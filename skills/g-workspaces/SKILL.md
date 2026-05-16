---
name: g-workspaces
description: Use the user's Google Workspace accounts across Gmail, Google Calendar, and Google Drive with the consolidated local auth layer. Trigger when the user asks to use Google Workspace, Gmail, email, Calendar, Drive, Docs, Sheets, uploads, downloads, search, or account-specific Google operations across personal, ExampleCo, Example Workspace, or ReviewCo accounts.
---

# Google Workspaces

Use the local Google tools, not app connectors, when the target account matters.

## Accounts

- `personal` - `user@example.com`
- `exampleco` - `user@example.com`
- `example-workspace` - `user@example.com`
- `gmr` - `user@example.com`

## Shared Auth

The consolidated OAuth token store is:

```bash
~/.config/google-tools/tokens.json
```

Auth helper:

```bash
node ~/.config/google-tools/google.js list-accounts
node ~/.config/google-tools/google.js add personal
```

Use this shared auth layer for OAuth accounts. Do not assume Google app connectors are authenticated to the intended account.

## Route By Task

### Gmail

Use:

```bash
node ~/.config/gmail-tools/gmail.js check
node ~/.config/gmail-tools/gmail.js all 5
node ~/.config/gmail-tools/gmail.js inbox personal 10
node ~/.config/gmail-tools/gmail.js search gmr "from:mercury" 10
node ~/.config/gmail-tools/gmail.js read example-workspace "subject:proposal"
node ~/.config/gmail-tools/gmail.js draft exampleco "person@example.com" "Subject" "Body"
node ~/.config/gmail-tools/gmail.js send personal "person@example.com" "Subject" "Body"
node ~/.config/gmail-tools/gmail.js reply gmr "from:client subject:reviews" "Reply body"
node ~/.config/gmail-tools/gmail.js download personal "has:attachment subject:statement" /tmp
```

Notes:
- `example-workspace` and `gmr` Gmail may use service accounts where configured.
- Ask before sending externally visible emails unless the user explicitly asked to send.

### Calendar

Use:

```bash
node ~/.config/google-calendar-tools/calendar.js list-accounts
node ~/.config/google-calendar-tools/calendar.js list-calendars personal
node ~/.config/google-calendar-tools/calendar.js get-current-time personal America/Denver
node ~/.config/google-calendar-tools/calendar.js list-events personal '{"calendarId":"primary","timeMin":"2026-05-07T00:00:00","timeMax":"2026-05-07T23:59:59","timeZone":"America/Denver"}'
node ~/.config/google-calendar-tools/calendar.js search-events exampleco '{"calendarId":"primary","query":"roadmap","timeMin":"2026-05-01T00:00:00","timeMax":"2026-05-31T23:59:59","timeZone":"America/Denver"}'
node ~/.config/google-calendar-tools/calendar.js create-event personal '{"calendarId":"primary","summary":"Event title","start":"2026-05-08T09:00:00","end":"2026-05-08T09:30:00","timeZone":"America/Denver"}'
```

Workflow:
- Call `get-current-time` first when relative dates matter.
- Call `list-calendars` before creating events on an unfamiliar account/calendar.

### Drive

Use:

```bash
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js list-accounts
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js profile personal
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js upload-spreadsheet example-workspace /absolute/path/report.csv "Report Title"
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js upload-file personal /absolute/path/file.pdf "Optional Title"
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js search gmr "name contains 'invoice' and trashed = false" 20
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js list exampleco root 50
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js trash exampleco <fileId>
```

Workflow:
- Run `profile <account>` before uploads when account correctness matters.
- Return Drive URLs as clickable Markdown links.

## Health Check

When debugging account access, check all three surfaces:

```bash
node ~/.config/google-tools/google.js list-accounts
node ~/.config/gmail-tools/gmail.js check
node ~/.config/google-calendar-tools/calendar.js get-current-time personal America/Denver
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js profile personal
```

If an OAuth account fails with `invalid_grant` or insufficient scopes, run:

```bash
node ~/.config/google-tools/google.js add <account>
```

Then verify Gmail, Calendar, and Drive for that account.

