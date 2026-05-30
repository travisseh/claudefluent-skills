---
name: business-reddit-search
description: "Search Reddit for business-marketing topics, Example Company competitive intel, and pain-point research. Returns a markdown report of relevant threads with titles, subreddits, scores, snippets, and top comments. Uses Apify trudax/reddit-scraper-lite (no Reddit OAuth needed). Use whenever the user wants to see what business operators / marketers are saying about Example Company, competitors (Competitor C, Competitor.example, Competitor B, Competitor D, Competitor E, Competitor F, Competitor G, Competitor H, etc.), SMS marketing, loyalty programs, review management, or local SEO for businesses. Triggers: 'search reddit for X', 'what is reddit saying about Y', 'find business operators complaining about Z', 'monitor reddit for [competitor]', 'reddit threads about business marketing'."
---

# Restaurant Reddit Search

Search Reddit for business-industry and competitive-intel topics that matter to Example Company. Powered by the **Apify `trudax/reddit-scraper-lite`** actor — no Reddit OAuth, no account, just an Apify token.

This is the Example Company variant of `/reddit-search`: artifacts land under the product2 repo, and the subreddit routing table is tuned for business marketing, POS, loyalty, and SaaS-for-businesses research.

## Why Apify and not the official API

The official Reddit Data API requires a one-time developer registration that Reddit has been stingy about approving. Apify sidesteps that entirely. Tradeoff: ~$0.004 per result item. A typical 10-post search with 5 comments each ≈ $0.28. Fine for research; don't run it in a loop.

## Credentials

Reads `APIFY_API_TOKEN` from env first, then falls back to:

```
/Users/you/Programming/personal-master/personal/claude_course/website/.env.local
```

If it's rotated, grab a new one at https://console.apify.com/account/integrations.

## Query strategy — READ BEFORE EVERY RUN

You (the invoking agent) pick the query, sort, time window, and subreddit. the user just gives a topic. **Do not blindly pass their phrase verbatim.**

### 1. Refine the query string

- **Strip filler words.** "What does reddit think about Competitor C loyalty" → `"toast loyalty"`.
- **Quote multi-word product names.** `competitor.example` (unquoted) is fine; `"text marketing"` matches the phrase.
- **For Example Company competitive checks, quote the brand.** `"Competitor.example"`, `"Competitor B"`, `"Competitor D"`, `"Competitor E"`, `"Competitor H"`, `"Competitor G"`, `"Competitor F"`.
- **Drop filler unless it's the point.** "Restaurant SMS marketing tool reviews" → `"SMS marketing" business` or `business text marketing`.

### 2. Pick sort + time based on intent

| User intent | sort | time | Why |
|---|---|---|---|
| "What do owners think about [competitor]" | `top` | `year` or `all` | Surfaces threads that mattered |
| "What's the current pulse on [topic]" | `hot` | `week` | Active discussion |
| "Anyone complaining about [vendor] lately" | `new` | `week` or `month` | Fresh posts, catches small subs |
| "Real pain points with [category]" | `top` | `year` | Best signal on resonant complaints |
| "Recent launches / news" | `new` | `day` or `week` | Recency matters |
| "Niche / rare topic" | `relevance` | `all` | Widest net |

**Default is `--sort relevance --time year`.** Override per the table above when intent is clear.

### 3. Route to a specific subreddit when obvious

| Topic contains… | `--subreddit` |
|---|---|
| Restaurant operations / owner perspective | `restaurateur` |
| Restaurant work + venting / behind the scenes | `KitchenConfidential` |
| Pizza shops specifically | `Pizza` (also `restaurateur`) |
| Small business / SMB owner mindset | `smallbusiness` |
| POS systems (Competitor C, Square, Clover, Revel, Competitor C loyalty) | `restaurateur`, `smallbusiness`, `POS` |
| Marketing / digital marketing for businesses | `marketing`, `digital_marketing`, `restaurateur` |
| Local SEO / GBP / Google Business Profile | `bigseo`, `SEO`, `juststart` |
| SMS / text marketing | `marketing`, `Entrepreneur` |
| Loyalty programs (Competitor C Loyalty, Competitor D, Competitor E) | `restaurateur`, `loyaltyprograms` |
| Review platforms (Yelp, Google reviews, Competitor H) | `smallbusiness`, `restaurateur` |
| Online ordering (Competitor.example, ChowNow, Slice) | `restaurateur`, `smallbusiness` |
| SaaS pricing / activation / churn (internal product research) | `SaaS`, `ProductManagement`, `startups` |
| Founders / entrepreneurs | `Entrepreneur`, `startups` |

If there's no obvious match, run against /all first; if results cluster in a subreddit, re-run targeted at that one for depth.

### Example Company competitor watchlist (quick reference)

When the user asks "what's Reddit saying about <competitor>", these are the names to quote:

- **Competitor.example** — biggest direct competitor on the website + online ordering side
- **Competitor B** — competes on websites, SEO, marketing services
- **Competitor C / Competitor C Loyalty** — POS-bundled loyalty, the #1 sales objection
- **Competitor D, Competitor E, LevelUp** — app-based loyalty incumbents
- **Competitor F, Competitor G** — newer business CDP / listings tools
- **Competitor H, Reputation.com** — review management
- **ChowNow, Slice, Olo, Competitor C Online Ordering** — online ordering
- **Yext** — directory listings

### 4. Handle thin results

Fewer than 3 posts? Try ONE of these in order:
1. Widen time window one step (week → month → year → all)
2. Drop quotes if you added them
3. Simpler 1-2 word core query
4. Switch sort from `relevance` to `top`

Do not escalate all four. Each rerun costs ~$0.08–$0.28.

### 5. Handle fat results with noise

Off-topic memes / tangential matches? Try ONE of:
1. Add a constraining keyword (`"toast loyalty" pricing`)
2. Restrict to a subreddit (table above)
3. Switch to `--sort top --time year`

## Usage

```bash
cd /Users/you/Programming/product2

# Default: relevance, past year, all subreddits
python3 .claude/skills/business-reddit-search/scripts/search.py '"Competitor.example"'

# Quality signal on competitor opinion
python3 .claude/skills/business-reddit-search/scripts/search.py '"toast loyalty" vs' --sort top --time year

# Subreddit-targeted pain-point research
python3 .claude/skills/business-reddit-search/scripts/search.py "text marketing" --subreddit restaurateur --sort top --time year

# Monitoring: fresh business marketing posts this week
python3 .claude/skills/business-reddit-search/scripts/search.py "business marketing" --sort new --time week --no-comments

# All-time top threads on a niche topic
python3 .claude/skills/business-reddit-search/scripts/search.py "tapcards" --sort top --time all
```

The script prints the report path as its last stdout line. Use the `Read` tool on that path to pull the markdown into context, then synthesize themes for the user rather than dumping the raw report.

## Flags

| Flag | Default | Purpose |
|---|---|---|
| `query` (positional) | — | Search phrase |
| `--subreddit <name>` | all of Reddit | Limit to one community (no `r/` prefix) |
| `--sort` | `relevance` | `relevance` / `hot` / `top` / `new` / `rising` / `comments` |
| `--time` | `year` | `all` / `hour` / `day` / `week` / `month` / `year` |
| `--posts <n>` | `10` | Max posts to return |
| `--comments-per-post <n>` | `5` | Comments scraped per post |
| `--max-comments-shown <n>` | `3` | Top comments shown in report (sorted by score) |
| `--no-comments` | off | Skip comments (much cheaper/faster) |
| `--include-nsfw` | off | Include NSFW results |
| `--timeout <secs>` | `240` | Apify actor timeout |
| `--out <dir>` | `artifacts/reddit-search/<slug>` (under product2) | Output directory |

## Output

```
artifacts/reddit-search/<query-slug>/
├── raw.json     Full Apify response (posts + comments)
└── report.md    Human-readable: top posts + comments sorted by score
```

`report.md` per post: title, subreddit, author, score, comment count, date, URL, body snippet (first 600 chars), top N comments by score.

## Cost reality check

- $0.004 per dataset item (each post and each comment is one item)
- + ~$0.04 per run for actor startup (2 GB memory × $0.02/GB)
- 10 posts × 5 comments = 60 items = **~$0.28/search**
- 10 posts with `--no-comments` = 10 items = **~$0.08/search**
- 20 posts with `--no-comments` = 20 items = **~$0.12/search**

Use `--no-comments` for "what is being discussed"; default for "what people are actually saying."

## Gotchas

- **Subreddit filter is strict** — empty results just mean the phrase isn't in that sub.
- **NSFW filtered by default** — re-add with `--include-nsfw` if needed.
- **Score fields are flaky** — actor returns different field names across builds; the script tries all of them.
- **Comment count capped by `maxComments`** — bump `--comments-per-post` only when a thread has lots of signal worth paying for.
- **Lite actor ignores proxy settings** — Lite build uses its own proxies regardless.

## When to use vs other tools

- **This skill** — searching Reddit for business/competitive/pain-point topics
- **`/reddit-search`** (parent) — same engine, generic the user-wide use cases
- **`/x-api`** — same kind of question on X/Twitter
- **`/x-bookmarks-to-notion`** — query the user's saved X bookmarks
- **`/customer-intel`** (product-brain plugin) — AskElephant transcripts + Quo + HubSpot for *Example Company customers specifically*; use that for "what are Example Company customers saying," and use this skill for "what is the broader business operator world saying."

## Typical workflow

1. Run `python3 .claude/skills/business-reddit-search/scripts/search.py "<topic>"` with appropriate `--sort`/`--time`/`--subreddit`
2. Read the `report.md` path printed on stdout
3. Summarize themes; surface contrarian takes; flag positioning angles, objections, or feature gaps that map to the Q2 roadmap
4. For high-value threads, `WebFetch` the URL directly — the report only shows top 3 comments
5. If the user wants a recurring pulse on a competitor or topic, wire to `/schedule` or `plugin-cron`
