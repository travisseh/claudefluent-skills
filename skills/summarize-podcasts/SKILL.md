---
name: summarize-podcasts
description: Summarize podcast transcript rows from the Notion Podcast Transcripts database that synced recently, then send a compact digest to the user on Telegram. Use for the `summarize-podcasts` automation or whenever the user asks for recent podcast summaries from that database.
---

# Summarize Podcasts

Use this skill to avoid re-discovering the podcast database, transcript fallback path, and Telegram delivery.

## Workflow

1. Run the collector script:

```bash
python3 .agents/skills/summarize-podcasts/scripts/collect_recent_podcasts.py --hours 24
```

2. Read the JSON it prints.
   - If `count` is `0`, report that no podcasts synced in the last window and do not send Telegram unless the user asked for a no-op notification.
   - Each item includes:
     - `episode`
     - `podcast`
     - `synced`
     - `youtube_url`
     - `source` (`notion_page` or `youtube_fallback`)
     - `transcript`

3. Summarize only the returned items.
   - Keep each episode summary mobile-friendly.
   - Pull out the actual topics, claims, and notable takeaways.
   - If the transcript came from `youtube_fallback`, mention that briefly at the end of the digest.

4. Send the digest to Telegram with:

```bash
bash ~/.claude/skills/cron/lib/telegram-self.sh claudefluent <body-file>
```

5. Update the automation memory at `~/.codex/automations/summarize-podcasts/memory.md` with:
   - run timestamp
   - how many rows were found
   - which episodes were sent
   - whether any episode needed YouTube fallback

## Notes

- The Notion database is `3457bf03-b771-814f-944e-c15752949e46`.
- The collector extracts the Notion token from `~/.config/notion-tools/notion-ai.js` to match the existing local setup.
- The transcript fallback uses `~/.codex/skills/youtube-transcript/scripts/fetch_youtube_transcript.py`.
- Prefer the local Telegram helper over ad hoc API calls so delivery stays consistent.
- TBPN is intentionally excluded by the collector script before transcript retrieval or summarization.
