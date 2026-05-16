---
name: tella
description: "Query Tella video recordings, list videos, fetch full video detail, pull transcripts, and list chapters via the Tella public API. Use whenever the user wants to find a Tella recording, get a transcript, look up chapters, or pull source material from a Tella video for content (guides, articles, summaries). Triggers: tella, tella.tv, get tella transcript, find my tella video, list tella recordings, tella chapters, transcribe tella, become an AI builder video."
---

# Tella API Skill

CLI wrapper around the Tella public API. Same shape as the `grain` skill, different platform.

## Auth

API key stored in workspace `.env` as `TELLA_API_KEY=tella_pk_...`. The script auto-loads it.

Format: `Authorization: Bearer tella_pk_xxxxx`. Rate limit: 100 req/min per workspace.

## Capabilities

| Action | Notes |
|--------|-------|
| List videos | Paginated. Filter by playlist or substring search (post-filter). |
| Get video detail | Full payload incl. transcript, chapters, links. |
| Pull transcript | Plain text, with timestamps, JSON (with `sentences[].startSeconds`), or WEBVTT. |
| List chapters | Just titles + start times. |
| List playlists | Workspace metadata. |

Not yet wired (extend the script if needed): create/update/delete videos, manage collaborators, webhooks, exports.

## Usage

```bash
TELLA=~/Programming/personal-master/personal/.claude/skills/tella/scripts/tella.py

# List recent videos
python3 $TELLA --format md list

# Search by title (post-filter, single page)
python3 $TELLA list --search "AI Builder" --limit 50

# Get full detail (incl. transcript + chapters)
python3 $TELLA get vid_cmokgwr0n000j07ji96gm2blf
python3 $TELLA get https://www.tella.tv/video/become-an-ai-builder-ai-stack-2blf
python3 $TELLA get 2blf   # short suffix also works (scans pages)

# Pull just the transcript (plain text)
python3 $TELLA transcript vid_cmokgwr0n000j07ji96gm2blf > /tmp/aistack.txt

# Transcript with per-sentence timestamps
python3 $TELLA transcript vid_xxx --timestamps

# Transcript as WEBVTT (for editors)
python3 $TELLA --format vtt transcript vid_xxx
```

## ID resolution

The `id` argument accepts any of:

- A canonical id: `vid_cmokgwr0n000j07ji96gm2blf`
- A full URL: `https://www.tella.tv/video/become-an-ai-builder-ai-stack-2blf`
- The slug suffix: `2blf` (script will scan up to ~500 most recent videos)

Prefer the canonical `vid_...` id when you have it — the slug-suffix path makes extra list calls.

## Common workflows

**Pull transcripts to feed a guide / article draft:**
```bash
python3 $TELLA transcript vid_xxxxx > /tmp/transcript-1.txt
python3 $TELLA transcript vid_yyyyy > /tmp/transcript-2.txt
# Then read both with the Read tool and rewrite into the guide's voice
```

**Find a video by topic:**
```bash
python3 $TELLA list --search "ai builder" --limit 50 --format md
```

**Inspect a video before quoting it:**
```bash
python3 $TELLA --format md get vid_xxxxx | less
```

## Notes

- Transcripts have a `status` field — `ready`, `processing`, or `failed`. The `transcript` subcommand exits if not ready.
- Don't paste transcripts verbatim into customer-facing content. They contain filler words ("um", "like", repeated phrases) and wrong-word artifacts. Always rewrite in the user's voice using `/user-writing-style`.
- `--format json` returns the raw API payload, useful when you need timestamps or want to script further.
