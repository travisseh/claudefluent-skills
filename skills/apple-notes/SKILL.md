---
name: apple-notes
description: Work with the user's Apple Notes - search, read, and reference personal notes. Use when accessing, searching, or referencing Apple Notes content.
allowed-tools: Bash
---

# Apple Notes Skill

Access the user's Apple Notes via local script at `~/.claude/tools/apple-notes.py`

## Commands

```bash
# Search notes by title or content
python3 ~/.claude/tools/apple-notes.py search "query"

# Read a specific note by ID
python3 ~/.claude/tools/apple-notes.py read <id>

# List recent notes
python3 ~/.claude/tools/apple-notes.py list [limit]

# Prepend text to top of a note (by title)
python3 ~/.claude/tools/apple-notes.py prepend "Note Title" "text to add"

# Append text to end of a note (by title)
python3 ~/.claude/tools/apple-notes.py append "Note Title" "text to add"
```

## Key Notes

| Note | ID | Purpose |
|------|-----|---------|
| ClaudeFluent Next Up | 9302 | ClaudeFluent task list and workload planning |
| Change Log | 6074 | Retrospectives using "What happened / Counterfactual / Core Problem" framework |
| 2026 GOALS | 5898 | Current year goals |
| Conference, April 2025 | 8279 | Bishopric, ExampleCo strategy, spiritual goals |

## When to Use

- the user asks about patterns/lessons → `read 6074` (Change Log)
- the user asks to search notes → `search "keyword"`
- the user wants to reference a note → `read <id>`
- Add tasks to ClaudeFluent workload → `prepend "ClaudeFluent Next Up" "task here"`

## Context

the user uses Apple Notes for:
- Personal reflection and journaling (Change Log)
- Work retrospectives
- Conference/church notes
- Life planning and goal tracking
