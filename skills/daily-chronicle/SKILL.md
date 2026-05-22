---
name: daily-chronicle
description: Build and save a chronological timeline of the user's day from calendar, Grain, AskElephant, Slack, sent Gmail, sent iMessage, Codex sessions, and Claude Code threads. Defaults to today but accepts dates and ranges like yesterday, 2026-05-21, last 3 days, this week, or May 20-21. Use when the user asks for a daily chronicle, day timeline, what happened today/yesterday, or to save a timeline of his work/meetings/messages/agent activity.
---

# Daily Chronicle

Create a chronological record of the user's day and save it to the Notion AI Output Library. This is not a prioritizer or promise extractor. It is an evidence-backed timeline of meetings, messages, emails, and agent work.

## Date Window

Default to **today** in `America/Denver` unless the user gives a date or range.

Accept:

- `today`
- `yesterday`
- exact dates: `2026-05-21`
- natural ranges: `last 3 days`, `this week`, `May 20-21`

Always confirm the local clock before resolving relative dates:

```bash
node ~/.config/google-calendar-tools/calendar.js get-current-time personal America/Denver
```

For a single day, use local midnight to local midnight. For ranges, create one combined timeline, grouped by date if the range is longer than one day. State the exact local date window in the saved output and final response.

Use UTC equivalents for tools that expect UTC timestamps, such as Grain, iMessage DB scans, Codex session timestamps, and Claude Code logs.

## Source Sweep

Use the same personal source surface as `/what-i-promised`, plus Codex and Claude Code threads.

### 1. Automation Memory

If running as an automation, read `$CODEX_HOME/automations/<automation_id>/memory.md` first. If `CODEX_HOME` is unset, use `/Users/you/.codex`.

Use memory only for prior caveats and previous output URLs. Do not reuse old timeline items as current evidence.

### 2. Calendar

Use the local Calendar CLI, not Calendar MCP, unless explicitly requested.

Check calendars across:

- `personal`
- `boostly`
- `example-agency`
- `gmr`

Start by listing calendars for each account when unfamiliar or when a prior run might have missed non-primary calendars:

```bash
node ~/.config/google-calendar-tools/calendar.js list-calendars <account>
node ~/.config/google-calendar-tools/calendar.js list-events <account> '{"calendarId":"<calendar_id>","timeMin":"YYYY-MM-DDT00:00:00","timeMax":"YYYY-MM-DDT23:59:59","timeZone":"America/Denver"}'
```

Include non-obviously-irrelevant calendars, especially Example Company Engineering and personal/Leadership calendars such as `the user Example Group`.

Calendar items provide the skeleton. Mark future calendar events as `Scheduled Later` or clearly say they are calendar-derived if the day is still in progress.

### 3. Grain

Use raw Grain data, not Grain AI summaries or AI action items.

```bash
/Users/you/.codex/skills/grain/scripts/grain.py --format json list --after <UTC_ISO> --before <UTC_ISO> --participants
/Users/you/.codex/skills/grain/scripts/grain.py --format json transcript <recording_id>
```

For relevant meetings, summarize:

- who the meeting was with
- what was decided/discussed
- action items / open loops
- any notable commitment or blocker

If no recordings are returned, record `Grain: no recordings found`.

### 4. AskElephant

Use the local AskElephant transcript search.

```bash
/Users/you/.codex/skills/askelephant/scripts/search_meetings.py --since YYYY-MM-DD --until YYYY-MM-DD --limit 30 --fetch-limit 300 --include-transcript
```

If needed, add targeted searches for people/projects discovered from calendar or Slack.

Summarize only substantive meeting content. If no meetings are returned, record `AskElephant: no meetings found`.

### 5. Slack

Use the local Slack CLI across all configured workspaces.

```bash
node ~/.config/slack-tools/slack.js workspaces
node ~/.config/slack-tools/slack.js search --all 'from:me after:YYYY-MM-DD before:YYYY-MM-DD'
node ~/.config/slack-tools/slack.js search <workspace> 'from:travisse after:YYYY-MM-DD before:YYYY-MM-DD'
```

Configured workspaces commonly include:

- `boostly`
- `gmr`
- `claudefluent`
- `example-agency`

Extract sent-message activity into timeline entries such as:

- "Messaged Shane/Jared about GoDaddy/domain access."
- "Told team there was nothing for today."
- "Release-note automation sent fallback output."

Ignore bot noise unless it represents a failed or successful automation the user should know about.

### 6. Sent Gmail

Use the local Gmail CLI. Check sent mail for:

- `personal`
- `boostly`
- `example-agency`
- `gmr`

```bash
node ~/.config/gmail-tools/gmail.js search <account> 'in:sent after:YYYY/M/D before:YYYY/M/D' 30
```

Use snippets for light evidence. Read full messages only when the snippet is insufficient and the email is important.

Summarize email activity by recipient/topic, not every automated marketing email unless it is notable.

### 7. Sent iMessage

Prefer the custom iMessage tools. If broad day-bounded sent-message search is needed and `imessage.js` cannot do it directly, query `~/Library/Messages/chat.db` from a temporary copy. Use Node 22 for `better-sqlite3` if needed:

```bash
~/.nvm/versions/node/v22.17.0/bin/node <script>
```

When querying directly:

- copy `chat.db`, `chat.db-wal`, and `chat.db-shm` to `/tmp`
- filter `message.is_from_me = 1`
- use local day boundaries converted to Apple nanoseconds
- decode `attributedBody` when `text` is empty, using the extraction pattern from `~/.config/imessage-tools/imessage.js`
- resolve key phone numbers with:

```bash
node ~/.config/imessage-tools/imessage.js find-contact <phone>
```

Summarize meaningful sent texts, especially family, church, financial, and work coordination. Ignore pure automation self-notifications unless they explain an automation outcome.

### 8. Codex Sessions

Inspect local Codex sessions for the window:

```bash
find /Users/you/.codex/sessions -type f -name '*.jsonl' -newermt 'YYYY-MM-DD 00:00:00' ! -newermt 'YYYY-MM-DD 23:59:59'
```

For each relevant session, extract:

- session start time
- cwd
- user ask
- major assistant outcome/final response
- blockers or in-progress state
- artifacts, Notion pages, PRs, commits, deploys, screenshots, or messages sent

Use `jq` to pull only `session_meta`, user messages, assistant progress, and final messages. Do not paste whole prompts or system instructions.

### 9. Claude Code Threads

Inspect Claude project logs across all repos:

```bash
find /Users/you/.claude/projects -type f -name '*.jsonl' -newermt 'YYYY-MM-DD 00:00:00' ! -newermt 'YYYY-MM-DD 23:59:59'
```

Extract the same fields as Codex. If no files were modified in the window, record that Claude Code had no modified project threads.

## Timeline Writing Rules

Produce a Notion-ready markdown artifact with:

1. Title: `Daily Chronicle - YYYY-MM-DD` or `Daily Chronicle - YYYY-MM-DD to YYYY-MM-DD`
2. Exact window and timezone
3. Chronological timeline
4. `Scheduled Later` section for future calendar items when the day is still in progress
5. `Source Coverage` or `Notes / Gaps`

Timeline entries should look like:

```markdown
### 9:11-9:13 AM - ClassDojo follow-up emails sent

Denada sent individualized ClaudeFluent follow-up emails to Lorna, Dave, Sejin, Jeff, Amy, and Vin.

Core message: Ali mentioned they might be interested in additional 1:1 help after class; I asked what their biggest blocker is and what follow-up support would be most useful.
```

Guidelines:

- Be chronological first, topical second.
- Merge duplicate evidence from calendar/email/Codex into one entry when they describe the same activity.
- Separate observed actions from future scheduled items.
- Include concise meeting summaries and action items when transcripts exist.
- If a meeting has only calendar evidence, say so.
- Preserve useful links: Notion URLs, production URLs, local artifact paths, PR URLs, event links.
- Keep the page detailed enough to reconstruct the day, but avoid raw transcript dumps.

## Save To Notion

Use the `notion-save` pattern and local Notion AI CLI, not Notion MCP:

```bash
node ~/.config/notion-tools/notion-ai.js create \
  "Daily Chronicle - YYYY-MM-DD" \
  "Life Admin" \
  "Admin" \
  @/path/to/artifact.md \
  type=Notes \
  source="Codex Daily Chronicle YYYY-MM-DD" \
  tags=daily-chronicle,timeline,YYYY-MM-DD
```

For multi-day ranges, use a range title and tags:

```bash
tags=daily-chronicle,timeline,YYYY-MM-DD,range
```

Always show the Notion URL in the final response.

## Automation Memory

When running as an automation, append a short run note before finishing:

- run timestamp
- exact date window
- artifact path
- Notion URL
- source coverage
- caveats, especially if the day was still in progress

Path:

```bash
/Users/you/.codex/automations/<automation_id>/memory.md
```

## Final Response

Keep the final short:

- link to Notion page
- link to local markdown artifact
- exact date window
- major coverage caveat if any

If the run materially advanced a substantial task, ask once:

`Do you want me to update the Life Backlog task in Notion?`
