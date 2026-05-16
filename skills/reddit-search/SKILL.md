---
name: reddit-search
description: "Search Reddit for a phrase or topic and get back a markdown report of relevant threads with titles, subreddits, scores, snippets, and top comments. Uses Apify trudax/reddit-scraper-lite (no Reddit account or OAuth needed). Use whenever the user wants to see what Reddit is saying about a topic, monitor Reddit mentions of a product/person/phrase, research pain points on a subreddit, or pull the top discussion threads on a keyword. Triggers: 'search reddit for X', 'what is reddit saying about Y', 'reddit threads about Z', 'find reddit discussion on …', 'monitor reddit for …'."
---

# Reddit Search

Search Reddit by phrase/topic and get a structured markdown report. Powered by the **Apify `trudax/reddit-scraper-lite`** actor — no Reddit OAuth, no account, just an Apify token.

## Why Apify and not the official API

The official Reddit Data API (as of March 2026) requires a one-time developer registration that Reddit has been stingy about approving. Apify sidesteps that entirely. Tradeoff: costs ~$0.004 per result item. A typical 10-post search with 5 comments each ≈ $0.25. Fine for personal research; don't run it in a loop.

## Credentials

Reuses the **same `APIFY_API_TOKEN`** stored at:

```
personal/claude_course/website/.env.local
```

Originally added for the `meta-ads` skill on 2026-04-08. If it's rotated, grab a new one at https://console.apify.com/account/integrations.

The script reads the token directly from that file — no `.env` propagation needed.

## Query strategy — READ BEFORE EVERY RUN

You (the invoking agent) pick the query, sort, time window, and subreddit. The user just gives a topic. **Do not blindly pass their phrase verbatim.** Reddit's search is loose and the defaults will often return noise. Follow this decision logic:

### 1. Refine the query string

- **Strip filler words.** "What does reddit think about X" → `"X"`. "Search reddit for people talking about X vs Y" → `"X vs Y"` or `"X" "Y"`.
- **Quote multi-word product names.** `claude code` (unquoted) matches any post with both words anywhere. `"claude code"` matches the phrase. Prefer quoted form for product/brand names.
- **For comparison questions, try both orderings.** If the first run is thin, re-run with the terms swapped.
- **Drop unique jargon unless it's the point.** "Onboarding activation funnel for SaaS" → `"activation funnel" SaaS` or just `activation funnel`.

### 2. Pick sort + time based on intent

| User intent | sort | time | Why |
|---|---|---|---|
| "What does Reddit think about X" (evergreen opinion) | `top` | `year` or `all` | Surfaces the threads that mattered, not memes from last week |
| "What are people saying about X right now" (current pulse) | `hot` | `week` | Active discussion, not old archives |
| "Is anyone complaining about X lately" (monitoring) | `new` | `week` or `month` | Fresh posts, catches tiny subreddits |
| "What are the pain points with X" (research) | `top` | `year` | Best signal on real complaints that resonated |
| "Breaking news about X" | `new` | `day` or `week` | Recency is everything |
| "Has X ever been discussed" (rare topic) | `relevance` | `all` | Widest net |

**The script default is `--sort relevance --time year`.** That's a decent generic starting point but you should override it whenever the user's intent matches a row above.

### 3. Route to a specific subreddit when obvious

If the topic clearly belongs to a niche, pass `--subreddit`. Results are dramatically better because you skip the noise of /all. Common mappings for the user's domains:

| Topic contains… | `--subreddit` |
|---|---|
| Claude Code, Cursor, Windsurf, Cline, AI coding agents | `ClaudeAI` (also try `ChatGPTCoding`, `cursor`, `singularity`) |
| Restaurant marketing / ops / POS / small restaurant | `restaurateur` (also `smallbusiness`, `KitchenConfidential`) |
| SaaS product, pricing, PLG, activation | `SaaS` (also `startups`, `ProductManagement`) |
| Landlord / tenant / rental property | `Landlord` (also `RealEstate`, `realestateinvesting`) |
| LDS / Mormon / bishopric / ward | `latterdaysaints` |
| Course creator, info product, online education | `juststart` (also `Entrepreneur`) |
| Parenting, newborn, baby sleep | `NewParents` (also `beyondthebump`, `daddit`) |

If there's no obvious subreddit match, run against /all first and see where the relevant results are clustered — then re-run targeted at that subreddit for depth.

### 4. Handle thin results

If the first run returns fewer than 3 posts, do ONE of these (in order):
1. **Widen the time window** one step (week → month → year → all)
2. **Drop quotes** from the query if you added them
3. **Try a simpler 1-2 word core query** stripping modifiers
4. **Switch sort** from `relevance` to `top`

Do not escalate to all four — stop when you get meaningful results. Each re-run costs ~$0.08-$0.28.

### 5. Handle fat results with noise

If a run returns posts that are clearly off-topic (memes, tangential keyword matches), do ONE of:
1. **Add a second keyword** to the query to constrain it (`"claude code" pricing` instead of `"claude code"`)
2. **Restrict to a subreddit** using the table above
3. **Switch sort to `top`** with `--time year` — cream rises

## Usage

```bash
cd ~/Programming/personal-master/personal

# Default: relevance sort, past year, all subreddits
python3 .claude/skills/reddit-search/scripts/search.py '"claude code"'

# Quality signal on evergreen opinion (preferred for most "what does reddit think" questions)
python3 .claude/skills/reddit-search/scripts/search.py '"claude code" vs cursor' --sort top --time year

# Subreddit-targeted research
python3 .claude/skills/reddit-search/scripts/search.py "activation funnel" --subreddit SaaS --sort top --time year

# Monitoring: fresh posts across Reddit this week
python3 .claude/skills/reddit-search/scripts/search.py "tapcards" --sort new --time week --no-comments

# All-time top threads on a rare topic
python3 .claude/skills/reddit-search/scripts/search.py "bishopric burnout" --sort top --time all
```

The script prints the report path as its last stdout line. Use the `Read` tool on that path to pull the markdown into context, then synthesize themes for the user rather than dumping the raw report.

## Flags

| Flag | Default | Purpose |
|---|---|---|
| `query` (positional) | — | Search phrase |
| `--subreddit <name>` | all of Reddit | Limit to one community (no `r/` prefix needed) |
| `--sort` | `relevance` | `relevance` / `hot` / `top` / `new` / `rising` / `comments` |
| `--time` | `month` | `all` / `hour` / `day` / `week` / `month` / `year` |
| `--posts <n>` | `10` | Max posts to return |
| `--comments-per-post <n>` | `5` | Comments scraped per post |
| `--max-comments-shown <n>` | `3` | Top comments shown in the report (after sort by score) |
| `--no-comments` | off | Skip comments entirely (much cheaper + faster) |
| `--include-nsfw` | off | Include NSFW results (default: filtered out) |
| `--timeout <secs>` | `240` | Apify actor timeout |
| `--out <dir>` | `artifacts/reddit-search/<slug>` | Output directory |

## Output

```
artifacts/reddit-search/<query-slug>/
├── raw.json      Full Apify response (all posts + comments before parsing)
└── report.md     Human-readable report with top posts + comments sorted by score
```

`report.md` shows per post: title, subreddit, author, score, comment count, date, URL, body snippet (first 600 chars), and the top N comments by score. Read this first — the raw JSON is only useful if you need fields the report omits.

## Cost reality check

- Pricing: **$0.004 per dataset item** (each post and each comment is one item)
- Plus ~$0.04 per run for actor startup (2 GB memory × $0.02/GB)
- 10 posts × 5 comments = 60 items = **~$0.28/search**
- 10 posts with `--no-comments` = 10 items = **~$0.08/search**
- 20 posts with `--no-comments` = 20 items = **~$0.12/search**

Use `--no-comments` when you only need to see *what* is being discussed; use the default when you need to see *what people are actually saying*.

## Gotchas

- **Subreddit filter is strict** — if you pass `--subreddit SaaS` and the phrase isn't in any SaaS thread, you'll get zero results. Check `r/SaaS` is actually active for your topic first.
- **NSFW filtered by default** — re-add with `--include-nsfw` if the topic is adult-adjacent (health, dating, relationships) and you're getting sparse results.
- **Score fields are flaky** — the Apify actor returns different field names across builds (`numberOfupvotes`, `upVotes`, `score`). The script tries all of them.
- **Comment count capped by `maxComments`** — even if a thread has 500 comments, you only get the top N you specified. Increase `--comments-per-post` for hot threads with lots of signal, but watch cost.
- **The Lite actor ignores proxy settings** — proxy config is passed for schema compliance only; the Lite build uses its own proxies.

## When to use vs other tools

- **Use this skill** for *searching* Reddit by phrase/topic — "what is Reddit saying about X"
- **Use `/x-api`** for the same question on X/Twitter
- **Use `/x-bookmarks-to-notion`** for querying the user's saved X bookmarks
- There is currently no dedicated HackerNews or LinkedIn equivalent — ask the user if they want one built

## Typical workflow

1. Run `python3 .claude/skills/reddit-search/scripts/search.py "<topic>"` with appropriate `--sort`/`--time`
2. Read the `report.md` path printed on stdout
3. Summarize themes, surface contrarian takes, flag anything actionable for the user
4. If a specific thread looks high-value, visit the URL directly with `WebFetch` for the full comment tree (the report only shows top 3)
5. If the user wants this on a schedule, wire it to `/schedule` or `plugin-cron` with a specific query
