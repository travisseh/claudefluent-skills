---
name: notion-calendar
description: "Add LinkedIn posts, articles, video ideas, and other content entries to the user's Notion Content Calendar database. Use whenever the user says 'add to my content calendar', 'save this to the content calendar', 'put this in the calendar', '/notion-calendar', or after drafting a LinkedIn post / article / video idea / email he'll want to schedule and publish later. Defaults Status to 'Idea' unless specified. Tracks Pillar (mode), Channels, Content Type, CTA, Source, Publish Date."
---

# Notion Content Calendar

Saves content ideas, drafts, and scheduled posts to the **Content Calendar** Notion database. This is the place where every LinkedIn post, article, email, and video idea goes from "thought" → "scheduled" → "posted."

Sibling skills: `/notion-save` for AI Output Library (durable artifacts), `/notion-backlog` for Life Backlog (tasks). Don't confuse the three.

## Database

- **Name:** Content Calendar
- **ID:** `3507bf03-b771-8117-8c47-c70c0ab31112`
- **URL:** https://www.notion.so/example-agency-design/3507bf03b77181178c47c70c0ab31112

## Schema

| Property | Type | Options |
|----------|------|---------|
| Name | title | The post/article/video title or hook |
| Status | select | **Idea** (default), Drafting, Ready, Scheduled, Posted, Repurpose, Generated Ideas, In Progress |
| Pillar | select | Tested Recommendations/Guides, Timely News, Founder Story, Info Gathering |
| Channels | multi_select | LinkedIn, Email List, ClaudeFluent Site, X, YouTube, TikTok, Instagram, Partner/Affiliate |
| Content Type | multi_select | LinkedIn Post, Short Video, Email, Article, Workshop Clip, Testimonial, Case Study, Referral Ask |
| CTA | rich_text | The call-to-action / destination link |
| Notes | rich_text | Anything not in the body |
| Source | rich_text | Where the idea came from (training, X bookmark, podcast, etc.) |
| Publish Date | date | YYYY-MM-DD (optional — leave blank for "Idea" status) |
| Post URL | url | After publishing, the live URL |

The full draft body goes in the **page content** (markdown), not in a property.

## Pillar ↔ LinkedIn mode mapping

The Pillar values mirror the 3 LinkedIn content modes from `travisse-writing-style`:

| LinkedIn mode | Pillar value |
|---|---|
| Mode 1 — Super Timely AI News | `Timely News` |
| Mode 2 — Tested Guides, Tutorials & Recommendations | `Tested Recommendations/Guides` |
| Mode 3 — Founder Journey | `Founder Story` |
| (research / sourcing, not a post) | `Info Gathering` |

When saving a LinkedIn post draft, set `pillar=` to the mode you used.

## CLI Tool

Use `~/.config/notion-tools/notion-calendar.js`. Do NOT use Notion MCP.

```bash
node ~/.config/notion-tools/notion-calendar.js <command> [args]
```

## Adding an Entry

**Default flow — write the draft to a temp file, then pipe it in. Status defaults to `Idea` if not specified:**

```bash
cat > /tmp/post.md <<'EOF'
In a recent corporate ClaudeFluent training I got asked to go deeper on...

So I wrote it down: the AI Builder Technical Stack guide. It's everything you need to understand to build with AI vs. just use it.
...
EOF

node ~/.config/notion-tools/notion-calendar.js create \
  "AI Builder Technical Stack guide launch post" \
  @/tmp/post.md \
  pillar="Tested Recommendations/Guides" \
  channels=LinkedIn \
  type="LinkedIn Post" \
  cta="https://www.claudefluent.com/guides/ai-builder-technical-stack" \
  source="ClaudeFluent guide launch 2026-05-02"
```

Returns `{id, url}`. Always show the Notion URL to the user.

**Args:**
- Positional: `title`, `content` (optional — `@file`, `-` for stdin, or inline string)
- Named: `status=`, `pillar=`, `channels=` (comma-separated), `type=` (comma-separated, alias `content_type=`), `cta=`, `notes=`, `source=`, `publish_date=YYYY-MM-DD`, `post_url=`

**Idea-only entry (no body, no date):**

```bash
node ~/.config/notion-tools/notion-calendar.js create \
  "Why Claude Code Desktop is the wrong starting point for non-devs" \
  pillar="Founder Story" \
  channels=LinkedIn \
  source="from Tuesday's class feedback"
```

This lands as Status=Idea with no publish date — perfect for capturing thoughts mid-conversation.

## Listing

```bash
# All ideas
node ~/.config/notion-tools/notion-calendar.js list status=Idea

# Everything scheduled to publish
node ~/.config/notion-tools/notion-calendar.js list status=Scheduled

# Tested Guides pillar across all statuses
node ~/.config/notion-tools/notion-calendar.js list pillar="Tested Recommendations/Guides"

# LinkedIn-channel content
node ~/.config/notion-tools/notion-calendar.js list channel=LinkedIn
```

Output: `pageId  [status]  pillar  channels  publish-date  title`

## Reading & Updating

```bash
# Full page + block content
node ~/.config/notion-tools/notion-calendar.js read <pageId>

# Append a revision or note to an existing entry
node ~/.config/notion-tools/notion-calendar.js append <pageId> @/tmp/v2.md

# Move a status forward (Idea → Drafting → Ready → Scheduled → Posted)
node ~/.config/notion-tools/notion-calendar.js status <pageId> Drafting
node ~/.config/notion-tools/notion-calendar.js status <pageId> Scheduled

# Inspect the live schema (useful if the user adds new options)
node ~/.config/notion-tools/notion-calendar.js schema
```

## How to Pick Values

- **Title:** the post hook or working title. Be specific. "AI Builder Stack launch" beats "LinkedIn post."
- **Status:** default `Idea`. Bump to `Drafting` when actively writing, `Ready` when fully drafted, `Scheduled` when on a date, `Posted` when live (and add Post URL).
- **Pillar:** the LinkedIn mode mapping above. If it's research/sourcing, use `Info Gathering`.
- **Channels:** where it'll publish. Multi-select — a single piece can go to LinkedIn + Email List + Site.
- **Content Type:** what shape it takes. `LinkedIn Post` is the default for short text, `Article` for long-form, `Short Video` for Tella clips, etc. Multi-select.
- **CTA:** the destination URL the post drives to (a guide, a session signup, a waitlist).
- **Source:** where the idea came from. Be specific: "Reddit research 2026-04-19", "Tuesday class feedback", "Lenny's tweet", "podcast Y episode N".
- **Publish Date:** only set when there's a real schedule. Leave blank for ideas.

## When to Use

**Save proactively when:**
- the user asks to add something to the content calendar
- A LinkedIn post / article / video idea has been drafted he'll want to schedule
- An idea surfaces mid-conversation that's worth capturing for later (Status=Idea, no body needed)
- A recommendation comes out of marketing-brain workflows that should become a post

**Don't save:**
- Stuff that's already a durable research artifact — that's `/notion-save`
- Trivial back-and-forth or in-progress drafts the user hasn't approved
- Tasks that aren't content — use `/notion-backlog`

## Relationship to other Notion DBs

- **Content Calendar** = things to publish (LinkedIn posts, articles, videos, emails)
- **AI Output Library** (`/notion-save`) = research/writeups/drafts that informed content
- **Life Backlog** (`/notion-backlog`) = tasks (do this thing)

A LinkedIn post draft typically: starts as an Idea in the Content Calendar → may pull source material from the AI Output Library → graduates to Scheduled → finally Posted with a Post URL.
