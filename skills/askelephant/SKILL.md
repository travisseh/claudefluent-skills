---
name: askelephant
description: Search AskElephant meetings and transcripts, especially Travisse's meetings. Use when the user asks about AskElephant, AE meetings, meeting transcripts, promises, follow-ups, objections, summaries, or things discussed in recent calls.
---

# AskElephant Meeting Search

Use this skill to search AskElephant meetings/transcripts and answer questions like:

- "What things did I promise in meetings yesterday?"
- "Summarize my calls with customers last week."
- "What objections came up in my AE meetings?"
- "Find calls where we discussed pricing."

## Default Behavior

- Default person: `user.com`
- Default date: yesterday when the user asks a relative daily question.
- Default source: AskElephant engagements with transcripts.
- Prefer meetings where Travisse is owner, host, internal participant, or appears in transcript metadata.

## Quick Commands

Run from any directory:

```bash
python3 /Users/you/.codex/skills/askelephant/scripts/search_meetings.py --person user.com --date yesterday --query "promise promised follow up send I'll I will"
```

For a range:

```bash
python3 /Users/you/.codex/skills/askelephant/scripts/search_meetings.py --person user.com --since 2026-05-06 --until 2026-05-07 --query "pricing objection competitor"
```

To fetch broader context without keyword filtering:

```bash
python3 /Users/you/.codex/skills/askelephant/scripts/search_meetings.py --person user.com --date yesterday --limit 20
```

## Auth

The script reads credentials from environment variables and common local env files. Do not hardcode tokens in this skill.

Preferred:

- `ASKELEPHANT_API_KEY`

Fallback:

- `ASKELEPHANT_REFRESH_TOKEN`
- `ASKELEPHANT_FIREBASE_API_KEY`

Common local files loaded automatically when present:

- `/Users/you/Programming/boostly-reporting/apps/dashboard/.env.local`
- `/Users/you/.config/render/product-analytics.env`

## Answering Follow-Up / Promise Questions

1. Search yesterday's meetings for Travisse with promise/action keywords.
2. Read the returned snippets and transcript excerpts.
3. Extract concrete commitments only:
   - promised sends/docs
   - follow-up tasks
   - introductions
   - pricing/contract items
   - product/support actions
4. Include the meeting title, date/time, external company/contact when available, and a short quoted/paraphrased basis.
5. Separate "clear commitments" from "possible follow-ups" when the transcript is ambiguous.

Never print API keys, refresh tokens, or raw auth headers.
