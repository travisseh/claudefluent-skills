---
name: x-api
description: Search X/Twitter, read posts, look up users, fetch bookmarks, and pull conversations via the official X API v2 (pay-per-use tier). Use whenever the user wants to monitor mentions of a keyword/product/person on X, search for tweets, check what people are saying about a launch, pull a thread, look up a user's recent posts, or fetch his bookmarks. Examples — "search X for mentions of Mythos", "what's being said about Claude on X today", "pull this tweet thread", "grab my X bookmarks".
---

# X API skill

Wraps the official X API v2 on the **pay-per-use tier** (launched April 2026).

## Pricing (so you know what each call costs)

- $0.005 per post **read**
- $0.01 per post **created**
- 2M post reads/month cap before Enterprise required
- Up to 20% back as xAI/Grok credits

A `search/recent` call returning 100 tweets = **$0.50**. Be deliberate about `max_results`.

## Setup (one-time)

1. Sign in at https://developer.x.com → create a project + app on the **Pay-Per-Use** tier
2. Generate a **Bearer Token** (App-only auth — works for search, user lookup, post read)
3. Save it to `~/.x-api-bearer` (chmod 600) OR export `X_BEARER_TOKEN`
4. For **bookmarks** specifically, you need OAuth2 user-context (PKCE flow) — see `bookmarks.md` (only build this when needed; bearer is enough for everything else)

## Usage

Run the CLI wrapper at `scripts/x.py`:

```bash
# Search recent posts (last 7 days) — defaults to 25 results
python3 scripts/x.py search "mythos anthropic" --max 50

# Search with filters
python3 scripts/x.py search "claude code" --lang en --no-retweets --min-likes 5

# Look up a user
python3 scripts/x.py user elonmusk

# Get a user's recent tweets
python3 scripts/x.py user-tweets elonmusk --max 20

# Pull a single tweet by ID or URL
python3 scripts/x.py tweet https://x.com/anthropicai/status/123456

# Pull a full conversation thread
python3 scripts/x.py thread <tweet_id>
```

All commands print JSON to stdout by default. Pass `--format md` **before the subcommand** for a clean markdown digest:

```bash
python3 scripts/x.py --format md search "mythos anthropic" --max 50
```

## Endpoints covered

| Command | Endpoint | Cost per result |
|---|---|---|
| `search` | `GET /2/tweets/search/recent` | $0.005/post |
| `user` | `GET /2/users/by/username/:name` | $0.005 |
| `user-tweets` | `GET /2/users/:id/tweets` | $0.005/post |
| `tweet` | `GET /2/tweets/:id` | $0.005 |
| `thread` | `search/recent` w/ `conversation_id:` | $0.005/post |
| `bookmarks` | `GET /2/users/:id/bookmarks` | $0.005/post (needs OAuth2) |

## Common search operators

- `from:username` — by author
- `to:username` — replies to user
- `"exact phrase"`
- `keyword1 OR keyword2`
- `-filter:retweets` — exclude RTs (or use `--no-retweets`)
- `min_faves:10` — minimum likes (or `--min-likes`)
- `lang:en`
- `has:links`, `has:images`, `has:videos`
- `since:2026-04-01 until:2026-04-07`

Full reference: https://docs.x.com/x-api/posts/search/integrate/build-a-query

## Output conventions

- Default JSON output is the raw API response (so other tools can pipe it)
- Markdown output (`--format md`) lists each post as: author handle, timestamp, text, like/repost counts, URL
- Save monitoring runs to `artifacts/x-api/<topic>-<date>.md` when running a recurring sweep

## Failure modes

- **401** → bearer token missing or revoked. Re-check `~/.x-api-bearer` / env var
- **429** → rate limited (search/recent is 60 req / 15min on pay-per-use). Back off
- **Empty results for recent topic** → search/recent only covers last 7 days; older posts need full-archive (Enterprise only)
- **Bookmarks fails with bearer** → bookmarks require OAuth2 user-context, not app-only bearer

## Cost guardrails

Before any large pull, estimate: `posts × $0.005`. Anything over **$2/run** (400 posts) — confirm with the user first.
