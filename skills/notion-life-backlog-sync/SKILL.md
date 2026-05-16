---
name: notion-life-backlog-sync
description: "Sync progress into the user's Notion Life Backlog. Use when the user asks to update a Notion/Life Backlog task, or when a feature, fix, submission, or other meaningful task has just been completed or materially advanced and there is a reasonable chance the user will want the matching Life Backlog item updated. After substantial completion, ask once: Do you want me to update the Life Backlog task in Notion? Then update the matching task if the user says yes."
---

# Notion Life Backlog Sync

Use this skill to keep the user's Notion Life Backlog current without over-editing the task page.

Use the local CLI, not browser editing or the old Notion MCP flow:

`node ~/.config/notion-tools/notion.js`

## Completion Prompt

When a substantial task is done or materially advanced, ask once at the end of the work:

`Do you want me to update the Life Backlog task in Notion?`

Do not ask this for tiny read-only answers or casual discussion.

If the user already asked for the Notion update, skip the question and proceed.

## Default Update Style

Prefer appending a concise dated markdown update to the existing task instead of rewriting the task body.

Good update contents:

- what was completed
- concrete date if relevant
- next directories, next steps, or blockers

Keep comments short and factual. Use absolute dates when useful.

## CLI Workflow

1. Find the task with:
   `node ~/.config/notion-tools/notion.js tasks ...`
   or
   `node ~/.config/notion-tools/notion.js search "query"`
2. Read the current body if needed:
   `node ~/.config/notion-tools/notion.js read <pageId>`
3. Append a short markdown update:
   `node ~/.config/notion-tools/notion.js append <pageId> "## Update\n..."`
4. If needed, move status with:
   `node ~/.config/notion-tools/notion.js status <pageId> "Review"`

Always write body updates as markdown. The CLI converts markdown into proper Notion blocks.

## Task-Matching Heuristic

Pick the most obvious matching task based on title and current context.

Examples:

- directory submission work -> `Submit site to a bunch of directory listings?`
- indexing work -> indexing/GSC task
- affiliate workflow work -> affiliate task

If there are multiple plausible matches and none is clearly best, ask one concise question before editing Notion.

If the user specifically asks for a body rewrite, use `update`. Otherwise prefer `append`.

## Example Markdown Update

```md
## Update - March 21, 2026

- Submitted ClaudeFluent to Future Tools.
- Next likely directories: SaaSHub, There's An AI For That, Toolify (paid), and Futurepedia (paid).
```

## Completion Response

After updating Notion, tell the user the task was updated and summarize the appended note in one sentence.
