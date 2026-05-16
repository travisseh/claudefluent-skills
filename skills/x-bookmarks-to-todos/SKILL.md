---
name: x-bookmarks-to-todos
description: "Extract X/Twitter bookmarks via the official X API, read linked content, and create actionable todo lists with summaries. Incremental by default — only processes new bookmarks since last extraction. Use this skill whenever the user wants to process their X/Twitter bookmarks, extract saved tweets, create todos from bookmarks, or catch up on saved content. Also trigger when they say 'check my bookmarks', 'process my X bookmarks', 'what did I save on Twitter', or '/x-bookmarks'."
---

# X Bookmarks to Actionable Todos

Extract X bookmarks via the official **X API v2** (pay-per-use, $0.005/bookmark), read linked content, and produce a categorized markdown todo list.

This skill **delegates fetching to the `x-api` skill** — no browser automation, no GraphQL hash hacks. The `x-api` skill handles OAuth2 PKCE auth and token refresh.

## Prerequisites

The `x-api` skill must be set up:
- `~/.x-api-oauth-client.json` exists (client_id + secret)
- First run will open a browser to authorize; subsequent runs use the cached token at `~/.x-api-oauth-token.json`

If those files don't exist, point the user at `.claude/skills/x-api/SKILL.md` to set up.

## Usage

Invoke with `/x-bookmarks` or "extract my X bookmarks".

Optional parameters:
- `max` — how many bookmarks to fetch this run (default: 100, max per call: 100)
- `pages` — how many pages of 100 to pull (default: 1, so 100 bookmarks)
- `output` — output file path (default: `artifacts/x-bookmarks-to-todos/todos-from-bookmarks.md`)
- `full` — if `true`, ignore prior state and reprocess everything
- `read-links` — if `true`, fetch each linked URL and summarize (slower, more useful)

**Cost reminder:** $0.005 per bookmark. 100 bookmarks = $0.50. Confirm with the user before pulling more than 200 in a single run.

## Workflow

### Phase 1 — Detect what's already processed

1. Read the existing output file if it exists
2. Extract all tweet URLs (`https://x.com/.../status/\d+`) into a `knownTweetUrls` set
3. If `full=true`, skip this and treat everything as new

### Phase 2 — Fetch bookmarks via x-api

Run the `x-api` script directly. JSON output is easier to filter:

```bash
python3 .claude/skills/x-api/scripts/x.py bookmarks --max 100
```

The `bookmarks` command auto-paginates — pass `--max 500` and it will fetch 5 pages of 100 transparently.

Parse the JSON. Each tweet has: `id`, `text`, `created_at`, `public_metrics`, `author.username`, `entities.urls` (linked URLs).

### Phase 3 — Dedup against known URLs

For each tweet from the API response, build the URL `https://x.com/{author.username}/status/{id}` and skip if it's already in `knownTweetUrls`. Stop early if 10 consecutive bookmarks are already known (we've caught up).

### Phase 4 — (Optional) Read linked content

If `read-links=true`, for each new bookmark with an external URL in `entities.urls`:
- Fetch the page (use WebFetch)
- Pull title + 1-2 sentence summary
- Cap at ~10 link reads per run to avoid bloat

### Phase 5 — Categorize

Bucket each bookmark into one of:
- **AI / Claude / Tooling** — anything about Claude, Codex, agents, models, dev tooling
- **Business / Growth** — marketing, pricing, sales, distribution, founder content
- **Personal / Reference** — design, writing, life, books, anything else worth saving

Use the tweet text + linked content to decide. Default to "Personal / Reference" if unclear.

### Phase 6 — Generate todo entries

For each new bookmark, write a markdown entry:

```markdown
- [ ] **@{author}**: {1-line gist}
  - 🔗 [tweet]({tweet_url}){if external link: ` · [link]({external_url})`}
  - {if read-links: 2-sentence summary of the linked content}
  - **Why it matters:** {what action this implies — read, try, share, file away}
```

Group by category. Within each category, sort by tweet `created_at` desc.

### Phase 7 — Append to output file

Prepend a new section to the top of the output file:

```markdown
## Extraction: {YYYY-MM-DD HH:MM}
*{N} new bookmarks · ${cost} spent*

### AI / Claude / Tooling
{entries...}

### Business / Growth
{entries...}

### Personal / Reference
{entries...}

---

```

Existing content stays below. If the file doesn't exist, create it under `artifacts/x-bookmarks-to-todos/` (per workspace convention).

### Phase 8 — Report to user

Print:
- Number of new bookmarks added
- Cost spent (count × $0.005)
- File path
- Top 3 highest-leverage items (your judgment) with one-line "why"

## Failure modes

- **OAuth token expired and no refresh token** → re-run will trigger PKCE flow automatically (browser will pop)
- **403 from x-api** → bookmarks scope wasn't granted during auth. Delete `~/.x-api-oauth-token.json` and re-run to re-authorize
- **No new bookmarks** → report "all caught up since {lastRunDate}" and exit

## Notes

- The old version of this skill used GraphQL scraping with a hardcoded endpoint hash and browser automation. That approach was brittle and never deployed. The official API is now cheap enough ($0.005/post) to make it the right choice.
- For just *viewing* recent bookmarks without writing anywhere, use the `x-api` skill directly: `python3 .claude/skills/x-api/scripts/x.py --format md bookmarks --max 10`. This skill is for the categorize-and-file workflow.
