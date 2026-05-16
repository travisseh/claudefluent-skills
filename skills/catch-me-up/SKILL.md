---
name: catch-me-up
description: Summarize where the current coding thread/project stands after time away, including what changed, what is uncommitted, what was decided in conversation, blockers, verification status, and recommended next steps.
---

# Catch Me Up

Use this skill when the user asks to be caught up, asks "where are we at?", returns after time away, or wants a restart summary before continuing implementation.

## Goal

Give the user a concise operational briefing that lets them resume work without rereading the thread. Prefer concrete state over generic summary.

## Workflow

1. Identify the active repo and current user goal from conversation context.
2. Inspect local repo state:
   - `git status --short`
   - `git branch --show-current`
   - `git diff --stat`
   - If needed, inspect focused diffs with `git diff -- <path>`.
3. Check recent verification only if relevant:
   - Mention known completed checks from the current thread.
   - If uncertain and cheap, run the project’s usual check command.
   - Do not run expensive or destructive commands just to produce a catch-up.
4. Synthesize conversation state:
   - What we built or changed.
   - What decisions were made and why.
   - What is still unresolved or risky.
   - What uncommitted/unpushed work exists.
5. Recommend the next 1-5 concrete actions in order.

## Answer Shape

Use short sections. Default structure:

- **Where We Are**
- **Uncommitted Work**
- **Decisions / Constraints**
- **Risks / Open Items**
- **Recommended Next Steps**

Keep it concise but not vague. Include clickable file links only for files the user is likely to inspect next. Do not dump full diffs.

## Standards

- Do not commit, push, deploy, migrate, or edit files while catching the user up unless they explicitly ask.
- Do not reveal secrets from env files or command output.
- If background processes matter, check and mention the local URL or running process state.
- If the user asks what to do next, give an opinionated recommendation, not a menu of equally weighted options.
- If the repo is dirty, distinguish between uncommitted code changes, untracked files, ignored local secrets, and generated artifacts.
