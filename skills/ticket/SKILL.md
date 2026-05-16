---
name: ticket
description: >
  Start implementation work from a Linear ticket. Use when Claude is asked to
  begin a ticket such as CORE-123, DEV-1878, or another Linear issue: fetch
  ticket context, create an issue-named branch from fresh main, inspect repo
  docs and existing code structure, ask clarifying questions, and produce an
  implementation plan before coding.
---

# Start Ticket

Use this skill at the beginning of feature or bug work driven by a Linear issue. The goal is to start with strong inputs: ticket context, current main, repo conventions, nearby code patterns, and explicit scope boundaries.

Do not start coding during this skill unless the user explicitly asks to proceed after the plan.

## 1. Fetch The Linear Ticket

Use the Linear MCP tools to fetch the issue matching the user's ticket ID.

Fetch:

- Title
- Description
- Priority
- Labels
- Status
- Assignee if present
- Parent issue if present
- Sub-issues if present
- Relevant comments if available

Summarize the ticket for the user in practical terms:

- What the ticket asks for
- What success appears to mean
- Known constraints or missing information
- Any sub-issues or dependencies

## 2. Sync Main And Create A Branch

Before creating a branch, check git state.

If the worktree is dirty, stop and tell the user what is dirty. Do not stash or discard changes unless the user explicitly approves.

If clean:

```bash
git checkout main
git pull
```

Generate a concise branch name from the ticket title.

Daniel branch format:

```text
CORE-<number>/short-kebab-description
```

Examples:

- `CORE-1878/add-google-places-search-location-flow`
- `CORE-456/add-campaign-scheduling`

Use the ticket number from Linear and prefix it with `CORE-`. Keep the description short, usually 3-6 words.

Create and switch:

```bash
git checkout -b <branch-name>
```

Tell the user the branch name created.

## 3. Read Repo Instructions And Structure Docs

Read repo-level instructions before planning. In ExampleCo, use at least:

- `AGENTS.md` or `CLAUDE.md` if present
- `CONTRIBUTING.md`
- `README.md`

For frontend or App Router work, specifically inspect README sections about project structure, entity folder structure, routing, and shared component organization if they exist.

Also inspect:

- `.github/pull_request_template.md` when the ticket is likely to become a PR
- `.github/CODEOWNERS` when the ticket may touch owned areas such as Prisma, migrations, SQL, billing, messaging, or integrations

Do not paste long doc sections back to the user. Extract only the relevant rules that affect this ticket.

## 4. Inspect Nearby Code Patterns

Before asking final questions or planning, inspect the existing implementation around the likely code areas.

Look for:

- Existing routes, components, hooks, actions, schemas, and utilities for the same entity or workflow
- Create/edit/list/detail patterns for the same domain
- Nearby server action result and error handling conventions
- Existing validation schemas and form hooks
- Existing tests or factories for the touched domain
- Whether logic is normally colocated under `_components`, `_hooks`, `_utils`, `_shared`, or `src/lib`

For Next.js app structure:

- Treat `(group)` folders as route groups that do not change URL paths.
- Treat `[id]` folders as dynamic route segments.
- Treat `_components`, `_hooks`, `_utils`, and `_shared` as non-routed implementation folders.
- Prefer colocating feature-specific code under the relevant route/entity tree.
- Promote code to global/shared only when there is current reuse or a clearly justified shared API.

For utilities:

- Use `src/lib/utils` for broadly reusable pure helpers.
- Use feature-local `_utils` for pure helpers specific to one feature area.
- Do not create utilities for tiny one-off transforms unless it improves readability or testability.

## 5. Gather User Context

Ask one open-ended question before planning:

```text
Do you have any additional context, constraints, or preferences for this ticket? For example: specific approach, related code areas, screenshots, edge cases, things to avoid, or how you want the PR scoped.
```

If the user has already provided this context, summarize it and ask only for missing high-value information.

## 6. Ask Targeted Follow-Up Questions

Ask 2-3 targeted questions only when the answer materially affects implementation. Avoid questionnaire bloat.

Good question areas:

- Ambiguous requirements
- Scope boundaries and non-goals
- UI/UX expectations
- Data model or migration expectations
- Error handling and edge cases
- Existing customer/data constraints
- Whether behavior should be automatic, manual, or confirmed

Prefer concise free-form questions unless there are obvious mutually exclusive options.

## 7. Produce An Implementation Plan

After reading the ticket, repo docs, nearby code, and user context, produce a concrete implementation plan.

The plan should include:

- Files or areas likely to change
- Existing patterns that should be followed
- Data model or migration needs
- Server action/API/integration approach if relevant
- Frontend flow and component/hook boundaries if relevant
- Tests or verification to run
- Scope risks or things to split out
- Open questions that remain

Apply these ExampleCo planning rules:

- Keep components mostly presentational; put business logic in hooks or server actions.
- Keep form hooks focused on form setup/save/routing; extract domain-specific workflows into sibling hooks.
- Keep shared component changes small and generic; avoid broad shared API changes for one screen.
- Prefer database or mutation-level enforcement for uniqueness/idempotency assumptions; UI-only guardrails are not enough.
- For external API calls, plan timeout and cancellation behavior when requests can hang or fan out.
- Do not make global components or utilities for speculative future reuse.
- If the plan is large enough to produce a hard-to-review PR, recommend splitting the work.

Stop after the plan and ask whether the user wants to proceed with implementation.

