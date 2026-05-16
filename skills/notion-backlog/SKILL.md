---
name: notion-backlog
description: Work with the user's Notion Life Backlog task database across life areas. Use for backlog lookup, task status, task creation, task updates, and coordinating work across chief-of-staff, marketing, student experience, and dev agents.
---

# Notion Life Backlog

the user's unified task/backlog system across all life areas. Used by chief-of-staff, marketing-brain, student-experience, and dev agents.

## Database Reference

- **Database URL:** https://www.notion.so/6014a1b687444e26bee8002a1a80b7fc
- **Database ID:** `6014a1b687444e26bee8002a1a80b7fc`

## Schema

| Property | Type | Options |
|----------|------|---------|
| Name | title | (free text) |
| Status | select | Backlog, To Do, In Progress, Review, Done |
| Assignee | select | the user, marketing-brain, student-experience, dev |
| Area | select | ClaudeFluent, ExampleCo, ReviewCo, Bishopric, Steph/Carson, Mother/Padre, Life Admin |
| Initiative | select | Marketing, Ops, Student Experience, Product, Demand Gen, Admin, Sell Prep, Strategic |
| Due | date | optional |
| ID | auto_increment | LB-1, LB-2, etc. |
| Added | created_time | auto |
| Updated | last_edited_time | auto |

## CLI Tool

**ALWAYS use the CLI tool at `~/.config/notion-tools/notion.js` for all Notion operations. Do NOT use Notion MCP tools.**

```bash
node ~/.config/notion-tools/notion.js <command> [args]
```

## How to Read Tasks

Query all tasks (with optional filters):
```bash
node ~/.config/notion-tools/notion.js tasks
node ~/.config/notion-tools/notion.js tasks status="To Do"
node ~/.config/notion-tools/notion.js tasks area="Life Admin"
node ~/.config/notion-tools/notion.js tasks assignee=the user status="To Do"
```

Read a specific page by ID:
```bash
node ~/.config/notion-tools/notion.js read <pageId>
```

Search for pages:
```bash
node ~/.config/notion-tools/notion.js search "query"
```

## How to Create Tasks

```bash
node ~/.config/notion-tools/notion.js create "Task name" "Area" "Status"
```

Example:
```bash
node ~/.config/notion-tools/notion.js create "Fix login bug" "ClaudeFluent" "To Do"
```

**Always set at minimum:** Name, Area, Status.

## How to Update Tasks

Update task status:
```bash
node ~/.config/notion-tools/notion.js status <pageId> "In Progress"
```

Replace page content (markdown):
```bash
node ~/.config/notion-tools/notion.js update <pageId> "## Update\nWhat was done."
```

Append to page content:
```bash
node ~/.config/notion-tools/notion.js append <pageId> "## Update\nNew notes here."
```

## Agent Workflow

When an agent (marketing-brain, student-experience, dev) is invoked:

1. **Check for assigned tasks:** Query the backlog, filter for your Assignee name where Status is "To Do" or "Backlog"
2. **Pick up work:** Move Status to "In Progress" before starting
3. **Clarify if needed:** Update the page body with questions, move to "Review"
4. **Complete:** Move to "Review" for the user to verify, or "Done" if trivial
5. **Log what you did:** Always update the page body with what was done

## Creating Tasks from Comms Sweeps

When the chief-of-staff daily brief or sweep surfaces action items that aren't quick replies, create backlog items for them. Set:
- **Assignee:** the user (unless it's clearly a marketing-brain or student-experience task)
- **Area:** Match to the life area the item relates to
- **Initiative:** Match to the workstream (Marketing, Product, Ops, etc.)
