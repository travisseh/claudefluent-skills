---
name: x-bookmarks-to-notion
description: "Sync and query X/Twitter bookmarks in Notion. Use when the user wants to: search his saved tweets ('what did I bookmark about X?', 'show me bookmarks tagged Claude Code', 'bookmarks by @author'), run the bookmark sync manually, check what's synced, or re-run after a failure. Triggers: 'search my bookmarks', 'query bookmarks', 'what did I bookmark about', 'bookmarks tagged', 'bookmarks by', 'sync my bookmarks', '/x-bookmarks-notion'."
---

# X Bookmarks → Notion

Syncs X bookmarks into a Notion database so they're queryable from Claude Code and browseable in Notion. Runs on a 24h cron. Uses the official X API (pay-per-use, ~$0.005/post) and Anthropic (Sonnet 4.6) for auto-categorization.

## Architecture

- **Source**: `x-api` skill (`~/.x-api-oauth-token.json` handles auth)
- **Destination**: Notion DB, child of page `33c7bf03b77180609066e82319e28d7a` on example-workspace workspace
- **Dedup**: query Notion DB for existing `Tweet ID`s, stop X pagination on first known ID
- **Categorization**: Anthropic `claude-sonnet-4-6` picks 1–3 categories from a fixed taxonomy per tweet
- **State**: single file `state/db_id.txt` holds the DB ID after first-run creation (so we don't recreate)

## Secrets (already configured)

- **Notion token**: read from `~/.config/notion-tools/notion-ai.js` (same token as `/notion-save`)
- **Anthropic key**: read from `~/Programming/personal-master/personal/marketing-brain-bot/.env`
- **X API**: via `x-api` skill's cached OAuth2 user token at `~/.x-api-oauth-token.json`

## Usage

First run (creates the DB):
```bash
python3 .claude/skills/x-bookmarks-to-notion/sync.py
```

Flags:
- `--max N` — cap bookmarks fetched (default 100)
- `--dry-run` — fetch + classify but don't write to Notion
- `--verbose` — print each tweet as it's processed

## Cost per run

- X API: typically < $0.05/day (stops on first known bookmark)
- Anthropic: ~$0.002 per tweet classified → < $0.02/day at 10 new/day
- Notion: free

## Schema (auto-created on first run)

| Property | Type | Purpose |
|---|---|---|
| Text | title | Full tweet body |
| Author | rich_text | `@handle` |
| Tweet URL | url | link back to X |
| External Link | url | first URL in entities (if any) |
| Posted | date | tweet `created_at` |
| Synced | date | when we grabbed it |
| Likes / Reposts / Replies | number | `public_metrics` |
| Categories | multi_select | AI-assigned, 1–3 per tweet |
| Tweet ID | rich_text | dedup key |

Category taxonomy: `AI / Models`, `AI Tools & Workflows`, `Claude Code`, `Design & UX`, `Product & PM`, `Marketing & Growth`, `Business & Startups`, `Engineering`, `Writing & Content`, `Personal / Reference`, `Humor / Misc`.

## Cron

Set up via `plugin-cron` skill — runs `python3 .claude/skills/x-bookmarks-to-notion/sync.py` daily.

## Failure modes

- **Notion 401** → token rotated; update `~/.config/notion-tools/notion-ai.js`
- **Notion 404 on DB** → DB was deleted; delete `state/db_id.txt` and re-run to recreate
- **X 401** → OAuth token expired; next run auto-refreshes, or delete `~/.x-api-oauth-token.json` to re-auth
- **Anthropic 401** → key rotated; update `marketing-brain-bot/.env`
