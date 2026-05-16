---
name: linkedin-content-strategy
description: ClaudeFluent's LinkedIn content engine. Pulls timely sources (X bookmarks, podcasts, Anthropic builder tweets, Lenny's), maps findings to high-reach topics, and outputs ranked post ideas + drafts in the user's voice. Use when planning a LinkedIn sprint, drafting a post about a fresh Claude/Anthropic launch, asking "what should I post on LinkedIn this week?", or when there's a model/feature/pricing announcement to react to fast.
---

# LinkedIn Content Strategy

The operating system for ClaudeFluent's LinkedIn content. Built on five principles, fed by automated source pulls, and tied directly to the product loop.

## The Five Principles

### 1. Be more timely than anyone

Twitter-like timeliness on Claude / Anthropic / Codex / Cowork drops. Not summaries. Tested, opinionated takes. Big publications need a week. YouTubers need days. ClaudeFluent ships a LinkedIn post in **hours** and a guide in **a day**.

Speed is the moat. If a launch is more than 24 hours old, the timeliness window is closed. Pivot to a different angle (contrarian, retrospective, or a "here's what nobody's talking about" reframe).

### 2. Be more useful than any other content

Every post leaves the reader with something they can use today. Content is not a separate function from the product. Every insight should feed back into class, cowork sessions, and community. **The content strategy IS the product strategy.** They're the same loop.

If a post wouldn't make a current student say "oh, that's the thing he taught us," cut it.

### 3. Automate the source pulls

Speed comes from never having to hunt for material. The skill assumes these sources are already populated and just queries them.

| Source | What it's for | How to query |
|---|---|---|
| X bookmarks | the user's curated take-pile, refreshed continuously | `/x-bookmarks` or `python3 .claude/skills/x-bookmarks-to-notion/query.py --since YYYY-MM-DD` |
| Lenny's Podcast | Best product/growth thinking. Apply frameworks to ClaudeFluent's own growth | `/podcast-transcripts` (or query Notion DB directly, see below) |
| Limitless / TBPN / MFM | Supplement to bookmarks for fast-moving AI news | Same Notion DB, filter by `Podcast = "Limitless"` |
| Anthropic builder tweets | Boris Cherny, Cat Wu, Felix Rieseberg, Andrew Morris (amorriscode), what's shipping before it ships | `/cc-experts` |
| Codex / OpenAI builders | Théobald + Codex team (when OpenAI side matters) | `/cc-experts` |

### 4. Play the algorithm

LinkedIn's reality, not preference:

- **Link in comments, not in body.** Or require a comment for the link. Trying to fight this is futile.
- **Affiliates amplify.** Active affiliates should be nudged to engage on launch posts within the first hour. (Mechanism TBD: DM list, Slack, or Notion sub-database.)
- **First-hour engagement is the leverage point.** Drafts ready in advance so post timing is deliberate, not whenever you finish writing.

### 5. Toe the line on technical content

Posts that lead with terminal output, MCP configs, or tool plumbing keep the audience small (< 500 reach, audit confirmed). They serve existing followers. Necessary but not the growth engine.

**Rule:** Lead with the benefit or outcome. Show the automation only as proof of difficulty conquered. Never as the topic itself.

> ❌ "I added 3 plugins to my CLAUDE.md and it now…"
> ✅ "Here's a 5-min routine that handles my whole calendar inbox. The scary part: it runs while I sleep."

## Voice Philosophy (read this before drafting OR generating ideas)

**Engineer at the topic level, never at the writing level.**

Post genuine things, not things engineered for reach. Consciously choose TOPICS that have higher reach potential, but the content itself should always sound like the user sharing what he genuinely thinks, learned, or experienced. Never engineer the writing for engagement. The engineering happens at the topic level only.

**Anti-pattern to avoid:** Don't rewrite genuine insights into "thought leadership" framing. Lines like "This is what using AI actually looks like in 2026" sound just as fake as AI-generated text. Just say what you think plainly.

This is the rule that separates Tier 1 ideas from Tier 1 posts. A great topic ruined by performative writing underperforms a B-tier topic written honestly.

## MANDATORY: Apply user-writing-style at IDEA TIME, not just at draft time

Voice rules apply to the hooks, theses, titles, and section headers you generate, not only to finished drafts. Polishing a slop hook into a the user-voice draft does not work. The idea has to start in his voice.

**Before producing any post or article idea, read** `.claude/skills/user-writing-style/SKILL.md` and apply these to every line of output:

1. **Zero em-dashes.** Not in hooks, not in theses, not in headers, not anywhere. Use commas, periods, colons, or restructure. Scan the output for the character `—` (U+2014) before returning. If any are found, rewrite.
2. **Write to the one reader, not a category.** The reader is one specific mid-career operator who feels dumb about the parts outside their lane and suspects AI is making generalists valuable again. Never "PMs/marketers/operators" as a group.
3. **Kill guru-voice openers.** No "Most X are doing Y wrong." No "the ones winning vs. the ones losing." No "here's the playbook." Replace with a concrete moment, a number, or a sentence the user would actually say to a peer at dinner.
4. **Mode-tag every idea.** Mode 1 (learning in public, primary), Mode 2 (defended opinion), Mode 3 (work in public, rare), Mode 4 (AI news for operators).
5. **Mode 1 ideas need a specific click moment.** "Here's a framework I noticed" is a generalization, not a click. Reject and rewrite.
6. **Mode 2 ideas pass the dinner-table test.** If the contrarian take has been softened so it's palatable on LinkedIn, kill it and rewrite undiluted.
7. **No staccato cadence.** Three short declarative sentences in a row reads as machine-generated. Vary length even in idea hooks.
8. **No consultant section labels in output.** Drop "Distribution playbook," "Recommended sequencing," "Why it works." Just say what to ship and why, in flowing prose.

If any idea violates rules 1-3, the whole idea is slop. Reject and rewrite the idea, do not pass it to drafting and hope the next step fixes it.

## High-Reach Topics (from insights.md audit)

When choosing what to post, weight toward these:

1. How AI is changing the PM/marketer/operator role and what skills matter now
2. Hiring opinions from the other side of the table
3. Fatherhood, ambition, work-life honesty
4. What he built this week and why it surprised him
5. Contrarian takes on conventional career/tech wisdom

Low-reach but still valuable (1x/week max):
- Tool tips, tactics, screenshots with pro-tips
- Direct offer / session fill (1x every 2 weeks max)

## Cadence Targets

- **4-5 posts/week.** Below 4, audience attention drops. Above 6, signal dilutes.
- **Never go 2+ weeks without an identity / opinion / personal post.** That's what caused the 2025-Q4 reach drought.
- **~1 social proof post/week** (student outcome, "what they built").
- **Direct offer max once every 2 weeks.** Accept low reach when you do.

## The Workflow

When the user says "what should I post on LinkedIn this week?" or "give me LinkedIn ideas," run this exact sequence.

### Step 1: Pull sources (parallel)

Run all source queries for the last 7-10 days simultaneously:

```bash
# X bookmarks (synced date matters more than posted date, the user bookmarks asynchronously)
python3 .claude/skills/x-bookmarks-to-notion/query.py --limit 100 --sort synced --format json > /tmp/bm.json

# Podcast transcripts, query Notion DB
# (DB ID cached in .claude/skills/podcast-transcripts/state/db_id.txt)

# CC Experts, recent posts from Boris/Felix/Andrew + Peter Yang/Grace Leung videos
# /cc-experts route, or x-api directly:
python3 .agents/skills/x-api/scripts/x.py --format md user-tweets felixrieseberg --max 25
python3 .agents/skills/x-api/scripts/x.py --format md user-tweets bcherny --max 25
python3 .agents/skills/x-api/scripts/x.py --format md user-tweets amorriscode --max 25
```

Filter for high-signal items only:
- Bookmarks: `Claude Code | AI Tools & Workflows | Product & PM | Marketing & Growth | AI / Models` categories
- Podcasts: episodes whose title plausibly matches a high-reach topic above
- Expert tweets: original posts, not replies, > 50 likes (or any from Boris/Felix/Cat Wu)

### Step 2: Map to high-reach topics

For each high-signal item, ask:
1. Which high-reach topic does this map to?
2. What's the one-sentence opinionated take?
3. Is it timely (< 7 days old) or evergreen?
4. Mode: 1 (learning in public), 2 (defended opinion), or 3 (work in public)?

Discard anything that doesn't map cleanly.

### Step 3: Rank into tiers

- **Tier 1.** Career identity / hiring authority / contrarian PM-role takes. Highest reach potential.
- **Tier 2.** Fresh launches with a defended angle. Strong, time-sensitive.
- **Tier 3.** Tactical / work-in-public / build proof. Solid, lower ceiling.

A week of 4-5 posts should weight ~60% Tier 1+2, 40% Tier 3.

### Step 4: Sprint recommendation

Output: 4-5 posts for the week with hook material, source attribution, mode, and the angle. Do **not** draft full posts in this step. the user picks the ones to draft.

### Step 5: Draft on demand

When the user picks one or more, **before drafting**:
1. Read `.claude/skills/user-writing-style/SKILL.md` (mandatory).
2. Apply the relevant Mode pattern.
3. No hashtags. No engagement-engineered language. No ReviewCo mentions.

### Step 6: Save to Notion AI Output Library (optional)

For ideas the user wants to keep: invoke `/notion-save` so the ideas live alongside other research/drafts.

## What to Avoid

From `insights.md` and `feedback_*` memories. These will be auto-rejected by the skill:

- **Hashtags.** Zero, ever.
- **Engineered "thought leadership" framing.** Don't rewrite genuine insights into "this is what X actually looks like in 2026." Just say what the user thinks plainly.
- **ReviewCo mentions.** ExampleCo knows about ClaudeFluent and Example Agency. Not ReviewCo.
- **Direct selling/session fill posts** as growth content. They underperform (<200 impressions). Only deploy when actively running a Session Fill Push.
- **Niche technical observations** as primary content. Audience is PMs/marketers/operators, not engineers.
- **Sending without approval.** Every post draft must be shown to the user for explicit go-ahead before scheduling or publishing.

## State Tracking

To avoid duplicate ideas or repeat themes:

- Add posted ideas to today's daily note in `.claude/plugins/marketing-brain/state/daily/YYYY-MM-DD.md`
- After 7 days, durable lessons (e.g., "Cat Wu Anthropic posts overperform") roll up to `state/insights.md`
- Before recommending a topic, check the last 3 daily notes for "Posted:" entries

## Quick Reference: Source Owners

| Person | Handle | Bias / use case |
|---|---|---|
| Boris Cherny | @bcherny | Claude Code lead at Anthropic. Releases, post-mortems, eng quality |
| Cat Wu | (no public handle confirmed) | Head of Product, Claude Code & Cowork. Surfaces via Lenny's |
| Felix Rieseberg | @felixrieseberg | Cowork lead, desktop apps. Quietly drops mental-model gems |
| Andrew Morris | @amorriscode | Claude Code product, lots of customer support replies. Skim for original posts |
| Théobald | (Codex team) | OpenAI / Codex side. Use when comparing |
| Lenny Rachitsky | @lennysan | Lenny's Podcast. Best PM/growth thinking, $30B Anthropic ARR scoops |
| Peter Yang | @PeterYangYT | Long-form interviews with operators (Tibo, Geoff Charles at Ramp) |
| Grace Leung | @graceleungyl | Marketing-specific Claude Skills demos |

## When to NOT use this skill

- the user asks for a specific post on a topic he's already chosen → go straight to `/user-writing-style`
- It's a session-fill push → use the Session Fill Push workflow in `/marketing` instead
- It's an article or guide → use `/article-writer` or `/guide-writer`
- It's an internal Slack announcement or team email → use `/internal-marketing`
