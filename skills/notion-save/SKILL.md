---
name: notion-save
description: Save AI-generated research, writeups, analyses, briefs, or drafts to the Notion AI Output Library database. Use whenever the user says "save this to Notion", "notion-save", "/notion-save", "put this in the AI output library", or after producing a substantial research finding or writeup he'll want to reference later. Tags entries with Area and Initiative (same taxonomy as /notion-backlog).
---

# Notion Save

Saves the current AI output (research, writeup, analysis, brief, draft, notes) to the **AI Output Library** Notion database — a sibling to the Life Backlog that stores durable AI-generated artifacts for later reference.

## Database

- **Name:** AI Output Library
- **ID:** `33c7bf03-b771-8172-8307-d8db699b8703`
- **URL:** https://www.notion.so/33c7bf03b77181728307d8db699b8703
- **Parent page:** https://www.notion.so/example-workspace/Notion-Save-33c7bf03b77180609066e82319e28d7a

## Schema

| Property | Type | Options |
|----------|------|---------|
| Name | title | free text — give it a descriptive title |
| Area | select | ClaudeFluent, ExampleCo, ReviewCo, Bishopric, Steph/Carson, Mother/Padre, Life Admin |
| Initiative | select | Marketing, Ops, Student Experience, Product, Demand Gen, Admin, Sell Prep, Strategic |
| Type | select | Research, Writeup, Analysis, Brief, Draft, Notes |
| Source | rich_text | where it came from (e.g. "Codex session", "codex research", URL) |
| Tags | multi_select | free-form tags |
| Created | created_time | auto |
| Updated | last_edited_time | auto |

The **Area** and **Initiative** taxonomies match `/notion-backlog` exactly — so you can cross-reference tasks and the AI output that informed them.

## CLI Tool

Use `~/.config/notion-tools/notion-ai.js`. Do NOT use Notion MCP.

```bash
node ~/.config/notion-tools/notion-ai.js <command> [args]
```

## Saving an Output

**Preferred pattern — write markdown to a temp file, then pipe it in:**

```bash
cat > /tmp/output.md <<'EOF'
## Summary
Key findings...

## Details
- point one
- point two
EOF

node ~/.config/notion-tools/notion-ai.js create \
  "Descriptive Title" \
  "ClaudeFluent" \
  "Marketing" \
  @/tmp/output.md \
  type=Research \
  source="Codex session 2026-04-08" \
  tags=linkedin,growth
```

Returns the page ID and URL. Always show the URL to the user.

**Args:**
- Positional: `title`, `area`, `initiative`, `content` (optional — omit for empty page, use `@file` for a file, `-` for stdin, or inline string)
- Named: `type=`, `source=`, `tags=comma,separated`

## Images (local files)

To embed a local image (e.g., matplotlib chart PNGs) in an AI Output Library page, use the dedicated uploader — it uses Notion's native `/v1/file_uploads` endpoint, so no external hosting is required. Pass `--workspace personal` so it uses the personal integration token.

```bash
node ~/.config/notion-tools/notion-image-upload.js --workspace personal <pageId> <filepath> "optional caption"
```

Always use this tool for images. Do not reference local paths in markdown (they won't render) and do not try to embed base64. Workflow for a writeup with charts: create the page with `notion-ai.js create`, append markdown tables/text with `notion-ai.js append`, then call `notion-image-upload.js --workspace personal` for each PNG. Blocks land on the page in call order, so interleave to control layout.

## Listing and Reading

```bash
node ~/.config/notion-tools/notion-ai.js list area=ClaudeFluent
node ~/.config/notion-tools/notion-ai.js list initiative=Marketing type=Research
node ~/.config/notion-tools/notion-ai.js read <pageId>
node ~/.config/notion-tools/notion-ai.js append <pageId> @/tmp/more.md
```

## How to Pick Values

- **Area:** which life area does this belong to? Default to `ClaudeFluent` if unclear and it's clearly about the course/business.
- **Initiative:** what's it in service of? Ask if genuinely ambiguous — don't guess.
- **Type:**
  - `Research` — external research, market sizing, competitor analysis
  - `Writeup` — synthesized narrative or explanation
  - `Analysis` — interpretation of data (funnel, revenue, Stripe, etc.)
  - `Brief` — a plan or set of recommendations
  - `Draft` — copy, LinkedIn posts, emails, article drafts
  - `Notes` — loose notes, meeting summaries, ideas
- **Title:** be specific and date-stamped when relevant — e.g. "Google Ads NonBrand QS Analysis 2026-04-06" not "Google Ads stuff"

## When to Use

**Save proactively when:**
- the user asks to save something to Notion / AI output library
- You've produced a substantial research finding he'll want to reference later
- You've written a draft (LinkedIn post, email, article) worth keeping
- An analysis has conclusions that should outlive the chat session

**Don't save:**
- Trivial answers or quick code fixes
- In-progress scratch work (use tasks/plans instead)
- Anything that belongs as a backlog task (use `/notion-backlog`)

## Relationship to /notion-backlog

- **Life Backlog** = things to do (tasks, statuses, assignees)
- **AI Output Library** = things produced (research, writeups, drafts)

If an AI output leads to actionable work, create a backlog task via `/notion-backlog` and reference the AI Output Library URL in the task body.
