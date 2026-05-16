---
name: grain
description: Query Grain meeting recordings, pull transcripts, search by date/title/team, upload recordings, and share with teammates. Use whenever the user wants to find a meeting, get a transcript, check action items, search recordings, upload a recording, or share one. Examples — "find my meetings this week", "get the transcript from yesterday's standup", "what action items came out of the ExampleCo sync", "search grain for onboarding", "upload this recording to grain", "share this meeting with the team".
---

# Grain API Skill

Query and manage meeting recordings via the Grain API v2.

## IMPORTANT: Never use Grain's AI summaries or action items

Grain's built-in summaries and action items are unreliable. Always pull the raw transcript and do your own summarizing, action item extraction, and analysis. Never pass `--summaries` or `--action-items` flags. The workflow is:
1. Find the recording (use `list` to search/filter)
2. Pull the transcript (`transcript <id>`)
3. Read the transcript yourself and answer the user's question directly

## Auth

Personal Access Token stored in `.env` as `GRAIN_PAT` or at `~/.grain-pat`.

## Capabilities

| Action | What it does |
|--------|-------------|
| **List/search recordings** | Filter by date range, title, team, meeting type. Include participants for finding the right meeting. |
| **Get recording details** | Full detail on a single recording — calendar event, participants, private notes. |
| **Pull transcripts** | JSON (structured with speakers + timestamps), plain text, VTT, or SRT. |
| **Upload recordings** | Upload audio/video files to Grain for processing. |
| **Share/unshare** | Share recordings with specific users or teams, or revoke access. |
| **List users/teams/meeting types** | Workspace metadata for filtering. |
| **Tag recordings** | Add or remove tags. |
| **Update recordings** | Rename titles. |

## Usage

Run the CLI at `~/.codex/skills/grain/scripts/grain.py`:

```bash
GRAIN=~/.codex/skills/grain/scripts/grain.py

# List recent recordings
python3 $GRAIN --format md list --participants

# Search by title
python3 $GRAIN --format md list --search "standup" --participants

# Recordings from this week
python3 $GRAIN --format md list --after "2026-04-14T00:00:00Z" --participants

# Get recording metadata (no AI summary — pull transcript instead)
python3 $GRAIN --format md get <recording_id>

# Pull transcript as markdown
python3 $GRAIN --format md transcript <recording_id>

# Pull transcript as plain text
python3 $GRAIN transcript <recording_id> --transcript-format txt

# Upload a recording file
python3 $GRAIN upload /path/to/meeting.mp4
python3 $GRAIN upload /path/to/audio.m4a --filename "Team Standup 2026-04-20.m4a"

# Share a recording with a user
python3 $GRAIN share <recording_id> --user <user_id>

# Share with a team
python3 $GRAIN share <recording_id> --team <team_id>

# Unshare from a user or team
python3 $GRAIN unshare <recording_id> --user <user_id>
python3 $GRAIN unshare <recording_id> --team <team_id>

# List workspace users (to find user IDs for sharing)
python3 $GRAIN --format md users

# List teams
python3 $GRAIN --format md teams

# List meeting types (useful for filtering)
python3 $GRAIN --format md meeting-types

# Add a tag
python3 $GRAIN tag <recording_id> important

# Remove a tag
python3 $GRAIN tag <recording_id> old-tag --remove

# Rename a recording
python3 $GRAIN update <recording_id> --title "Better Title"
```

## Output formats

- `--format json` (default) — raw JSON, good for piping/parsing
- `--format md` — clean markdown, good for reading in conversation

## Pagination

List endpoints return a `cursor` field when more results exist. Pass `--cursor <value>` to get the next page.

## Rate limits

300 requests/minute. No per-call cost (unlike X API).

## Common workflows

**"What happened in my meetings this week?"**
```bash
# Step 1: Find the meetings
python3 $GRAIN --format md list --after "2026-04-14T00:00:00Z" --participants
# Step 2: Pull each transcript and summarize yourself
python3 $GRAIN --format md transcript <id>
```

**"What action items do I have from a meeting?"**
```bash
# Pull the transcript and extract action items yourself — don't use Grain's AI
python3 $GRAIN --format md transcript <id>
```

**"Upload a recording and share it with the team"**
```bash
python3 $GRAIN upload ./recording.mp4
python3 $GRAIN share <recording_id> --team <team_id>
```
