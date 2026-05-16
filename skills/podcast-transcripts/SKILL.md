---
description: Monitor YouTube podcast channels for new episodes and store transcripts in Notion. Use when checking for new podcast episodes, pulling transcripts, or querying the podcast transcript database.
---

# Podcast Transcripts

Monitors YouTube channels for new podcast episodes and stores URLs + full transcripts in a Notion database.

## Tracked Podcasts
- Lenny's Podcast (@LennysPodcast)
- Limitless: An AI Podcast (@Limitless-FT)
- TBPN (@TBPNLive)
- My First Million (@myfirstmillionpod)

## Usage

### Manual run (all channels)
```bash
python3 .claude/skills/podcast-transcripts/scripts/podcast_monitor.py --verbose
```

### Dry run (preview without writing to Notion)
```bash
python3 .claude/skills/podcast-transcripts/scripts/podcast_monitor.py --dry-run --verbose
```

### Single channel
```bash
python3 .claude/skills/podcast-transcripts/scripts/podcast_monitor.py --channel "TBPN" --verbose
```

### Skip transcript fetch (just create rows)
```bash
python3 .claude/skills/podcast-transcripts/scripts/podcast_monitor.py --skip-transcript --verbose
```

## Notion Database
- Parent page: `33c7bf03b77180609066e82319e28d7a` (Notion Save page)
- Database name: "Podcast Transcripts"
- DB ID cached in `state/db_id.txt`

### Schema
- **Episode** (title) — episode title
- **Podcast** (select) — channel name
- **YouTube URL** (url) — link to episode
- **Video ID** (rich_text) — dedup key
- **Published** (date) — upload date
- **Synced** (date) — when we captured it
- **Duration** (rich_text) — formatted duration
- **Has Transcript** (checkbox) — whether transcript was stored

Transcripts are stored as page content (paragraph blocks).

## Cron
Daily at 9:00 AM via launchd: `~/Library/LaunchAgents/com.user.podcast-monitor.plist`

## Adding a new podcast
Edit `CHANNELS` dict in `scripts/podcast_monitor.py`. Value is the YouTube channel videos URL.
