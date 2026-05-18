---
name: cf
description: >
  ClaudeFluent repo router. Use when the user says /cf, cf, ClaudeFluent, claude_course,
  update the website, update /admin participants, update marketing-brain plugin, or update
  student-experience plugin. Points Codex at the right ClaudeFluent files, skills, plugins,
  commands, and verification steps.
---

# ClaudeFluent Router

This skill is a fast orientation layer for ClaudeFluent work. Its job is to get into the right directory, read the right context, and avoid wasting time rediscovering the repo.

## Canonical Paths

- Repo root: `/Users/you/Programming/personal-master/personal/claude_course`
- Website app: `/Users/you/Programming/personal-master/personal/claude_course/website`
- Main landing page: `/Users/you/Programming/personal-master/personal/claude_course/website/app/v3/page.tsx`
- V3 homepage content: `/Users/you/Programming/personal-master/personal/claude_course/website/app/v3/HomeContentV3.tsx`
- Sessions config: `/Users/you/Programming/personal-master/personal/claude_course/website/lib/sessions.ts`
- Admin page: `/Users/you/Programming/personal-master/personal/claude_course/website/app/admin/page.tsx`
- Admin participants UI: `/Users/you/Programming/personal-master/personal/claude_course/website/app/admin/ParticipantsView.tsx`
- Admin shared types: `/Users/you/Programming/personal-master/personal/claude_course/website/app/admin/types.ts`
- Convex schema: `/Users/you/Programming/personal-master/personal/claude_course/website/convex/schema.ts`
- Convex participants functions: `/Users/you/Programming/personal-master/personal/claude_course/website/convex/participants.ts`
- Onboarding flow: `/Users/you/Programming/personal-master/personal/claude_course/website/app/onboarding/[token]/`
- Success page: `/Users/you/Programming/personal-master/personal/claude_course/website/app/success/page.tsx`
- Guides registry: `/Users/you/Programming/personal-master/personal/claude_course/website/lib/guides/index.ts`
- Guide content: `/Users/you/Programming/personal-master/personal/claude_course/website/lib/guides/content/`
- Blog registry: `/Users/you/Programming/personal-master/personal/claude_course/website/lib/blog/index.ts`
- Blog content: `/Users/you/Programming/personal-master/personal/claude_course/website/lib/blog/content/`
- Local marketing-brain state: `/Users/you/Programming/personal-master/personal/claude_course/.claude/plugins/marketing-brain/state/`
- Installed marketing-brain plugin: `/Users/you/.codex/plugins/cache/personal-local/marketing-brain/1.4.0/`
- Installed student-experience plugin: `/Users/you/.codex/plugins/cache/personal-local/student-experience/0.2.0/`

## First Moves

1. `cd /Users/you/Programming/personal-master/personal/claude_course`
2. Check `git status --short` at repo root before editing.
3. If touching website code, work from `/Users/you/Programming/personal-master/personal/claude_course/website`.
4. Prefer `rg` and `rg --files`; avoid scanning `node_modules`.
5. Before UI edits, check for local guidance at:
   - `/Users/you/Programming/personal-master/personal/claude_course/.claude/skills/`
   - `/Users/you/Programming/personal-master/personal/claude_course/website/.claude/skills/`

## Routing Rules

### `/cf update the website`

Assume the user means the ClaudeFluent Next.js website.

- Primary cwd: `/Users/you/Programming/personal-master/personal/claude_course/website`
- Read first: `package.json`, relevant `app/**/page.tsx`, relevant `lib/**`, and local `.claude/skills` if present.
- Common targets:
  - Homepage/current main marketing surface: `app/v3/page.tsx`, `app/v3/HomeContentV3.tsx`
  - Deal pages: `app/deal/page.tsx`, `app/deal100/page.tsx`
  - Guides: `lib/guides/index.ts`, `lib/guides/content/*.tsx`, `app/guides/**`
  - Blog: `lib/blog/index.ts`, `lib/blog/content/*.tsx`, `app/blog/**`
  - Checkout/session inventory: `lib/sessions.ts`, session availability libs, Stripe/Convex integration files
- For frontend work, use the front-end skill if available and verify with browser/Playwright.

### `/cf update /admin participants page`

Assume this means the ClaudeFluent admin participants table/workflow.

- Primary files:
  - `website/app/admin/page.tsx`
  - `website/app/admin/ParticipantsView.tsx`
  - `website/app/admin/types.ts`
  - `website/convex/participants.ts`
  - `website/convex/schema.ts`
  - `website/lib/manual-participants.ts`
- Check existing admin tab patterns in:
  - `website/app/admin/CompaniesView.tsx`
  - `website/app/admin/LeadsView.tsx`
  - `website/app/admin/SessionsTab.tsx`
  - `website/app/admin/AffiliatesTab.tsx`
- Be careful with production data paths. Identify whether a change is UI-only, Convex function behavior, or schema/data migration.

### `/cf update marketing-brain plugin`

There are two relevant places:

- Durable ClaudeFluent marketing state in repo: `/Users/you/Programming/personal-master/personal/claude_course/.claude/plugins/marketing-brain/state/`
- Installed plugin source/cache: `/Users/you/.codex/plugins/cache/personal-local/marketing-brain/1.4.0/`

When the ask is strategy, planning, or memory/state updates, read the repo state first:

- `state/insights.md`
- today's `state/daily/YYYY-MM-DD.md` if present
- yesterday's daily note if present

When the ask is changing plugin behavior, inspect/edit the installed plugin files, especially:

- `.codex-plugin/plugin.json`
- `skills/marketing/SKILL.md`
- `skills/google-ads/SKILL.md`
- `skills/meta-ads/SKILL.md`
- `state/`

If modifying an installed plugin cache, call that out in the final response because it is not the same as committing website repo code.

### `/cf update student-experience plugin`

Installed plugin path:

- `/Users/you/.codex/plugins/cache/personal-local/student-experience/0.2.0/`

Read first:

- `skills/student-experience/SKILL.md`
- `skills/student-experience/references/exercise-personalization.md` when exercises or personalization are mentioned
- `state/insights.md`
- `state/persona-gaps.md`
- `state/audit-log.md`
- today's and yesterday's `state/daily/*.md` if present

Common files:

- `skills/student-experience/SKILL.md`
- `skills/slide-style/SKILL.md`
- `skills/grain-testimonials/SKILL.md`
- `.codex-plugin/plugin.json`
- `state/`

For class slides or course experience changes, also consider the standalone skills `cc-slides`, `slide-style`, and `student-experience` when available.

## Commands

Run from `/Users/you/Programming/personal-master/personal/claude_course/website` unless stated otherwise.

- Install deps only if needed: `npm install`
- Dev server: `npm run dev -- --port <random 3001-3999>`
- Production-like dev env: `npm run dev:prod -- --port <random 3001-3999>`
- TypeScript check: `npx tsc --noEmit`
- Build: `npm run build`
- Convex deploy prod: `npm run convex:deploy:prod`

Use a random dev port in the 3001-3999 range. If a port is busy, retry with another.

## Verification Defaults

- For TypeScript or shared logic changes: run `npx tsc --noEmit`.
- For UI changes: run TypeScript, start the dev server on a random port, and verify the relevant URL in a browser/Playwright.
- For admin changes: verify the admin page renders and the touched tab behavior works; avoid mutating production data unless explicitly requested.
- For plugin text/state changes: no build is usually needed; verify paths and summarize exact files changed.

## Git Rules

- Never commit automatically.
- Always show changed files before any requested commit.
- If asked to commit, run `npx tsc --noEmit` first when website code changed.
- Do not revert user changes.

## Useful URLs

When a dev server is running, use full clickable URLs:

- Homepage: `http://localhost:<port>/v3`
- Admin: `http://localhost:<port>/admin`
- Participants admin: `http://localhost:<port>/admin` then select the participants view if tabbed
- Success: `http://localhost:<port>/success`
- Onboarding: `http://localhost:<port>/onboarding/<token>`
