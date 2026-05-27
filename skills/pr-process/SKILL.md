---
name: pr-process
description: Prepare, review, or publish pull requests for the product repository using the repo-specific contribution workflow. Use when Codex needs to create a branch, verify PR readiness, draft a PR title/body, check required local validation, confirm reviewer routing, explain how Example Company expects contribution work to be packaged and reviewed, or produce a PR scope explainer for changed/planned files.
---

# PR Process

Read the current repository rules before doing PR work. Do not rely on memory if the repo docs may have changed.

## Modes

Use the mode that matches the ask:

- **Full PR prep:** Default mode for branch, validation, commit guidance, PR body, and reviewer routing.
- **PR scope explainer:** Use before implementation, during review, or after implementation when the user asks what changed, why a file changed, whether the PR is too big, whether tests are oversized, or how to make the PR smaller. This mode can run even when no PR is being opened yet.

## Read These Files First

Open these files from the product repo before preparing or reviewing a PR:

- `CONTRIBUTING.md`
- `.github/pull_request_template.md`
- `.github/CODEOWNERS`

Use the current file contents as the source of truth. If any of those files conflict with general habits, follow the repo files.

## Follow This Workflow

### 1. Tie the work to one Linear issue

Confirm that the change maps to exactly one Linear issue.

- If no issue exists, say that Example Company expects one before PR work proceeds.
- If the diff covers multiple concerns, call that out and recommend splitting the work into separate PRs.

### 2. Verify branch naming

Ensure the branch name follows:

`{LINEAR_ISSUE_ID}-short-description`

Examples:

- `ISSUE-154-invite_links`
- `ISSUE-287-fix_campaign_scheduling`

If the current branch does not match, recommend renaming or creating the correctly named branch from `main`.

### 3. Check scope before PR prep

Inspect the diff and confirm that the change is reviewable as one issue.

- Flag unrelated edits.
- Flag opportunistic refactors that should be split out.
- Flag missing tests when behavior changed.

### 3.5. Run the Example Company architecture pass

Before PR prep, inspect the changed files for product codebase fit. The goal is not abstract purity; it is to keep new work shaped like the surrounding app so reviewers do not have to unwind architectural drift.

Check these points explicitly:

- **Component vs hook boundaries:** Components should mostly render UI from props/state and wire simple interactions. If a component owns debouncing, async server action calls, request race handling, form import logic, or larger business rules, recommend extracting that behavior to a focused hook near the component.
- **Form hook responsibilities:** Existing edit/create form hooks should stay centered on form defaults, save/submit behavior, routing, breadcrumbs, and unsaved-change handling. If a feature adds substantial domain-specific orchestration, such as Google listing refresh/import behavior, prefer a sibling hook that the form hook composes.
- **Shared component blast radius:** Treat edits to shared hooks/components, especially `src/hooks/use-multistep-dialog.tsx`, as high-friction. Keep shared changes small, generic, and useful beyond one screen. If the change exists only for one flow, first try a local wrapper or explicit prop/render callback before adding context, global state, or broad API changes.
- **Avoid copying shared UI:** Do not create a one-off copy of a large shared wizard/dialog just to avoid a small shared API extension. A small, generic extension is better than forking a complex component.
- **Server action shape:** Compare new server actions to nearby actions. Use existing helpers such as `withFormValidation`, `ServerActionResult`, `handleServerErrors`, and `getErrorMessage` where they fit. Avoid ad hoc error/result shapes when a local convention already exists.
- **Domain logic placement:** Put integration-specific behavior in the integration layer. For example, Google Places API error translation, stale Place ID messaging, response parsing, and supported-field mapping belong near `src/lib/google-places.ts` or a focused Google Places utility, not scattered through page actions or components.
- **Thin action payloads:** Avoid wrapper result types that only contain one property, such as `{ formValues: Partial<FormData> }`, unless the wrapper adds real meaning or room for planned metadata. Return the useful value directly to reduce drilling and mental overhead.
- **Shared utility placement and naming:** Standalone helper files under feature `_shared` should normally live in `_shared/_utils/`. Name utilities for what they do, not vaguely for the domain. For example, a helper that computes field diffs should read like `google-place-changes`, not `google-place-fields`.
- **UI guardrails are not data integrity:** If the feature assumes uniqueness, ownership, idempotency, or one-to-one mapping, prefer enforcing it at the database or mutation boundary. UI-only disabled states, gray cards, and duplicate warnings improve UX but are not sufficient protection.
- **External API cancellation:** For external API calls that can hang, especially fan-out calls such as photo thumbnails, prefer real request cancellation with `AbortController` over only racing a timeout. `Promise.race` can stop waiting while the underlying request still burns quota or resources.
- **Single branch point for UI configs:** If a component assembles an action/config object through several ternaries based on the same condition, move that assembly into the hook that owns the state. Components should receive the final config and render it.
- **Avoid premature schema abstractions:** Do not introduce named schema/helper abstractions used exactly once unless they clarify meaning. Inline one-off transforms if that matches nearby schema style; extract only when there is reuse or a strong domain name.
- **Prop drilling vs context:** Passing a few explicit props through one layer is fine. If many props are threaded through several unrelated components, consider a local hook, render callback, or narrow context. Do not add context for a single direct call site unless it clearly reduces complexity.
- **Review diff size by responsibility:** Large diffs are acceptable when behavior is large, but each changed file should have a clear reason to change. Flag files that mix presentation, data fetching, form mutation, and confirmation logic all at once.

### 3.6. Run the tiny PR critic pass

Before validation or PR drafting, explicitly challenge whether the diff is as small and conventional as it should be for Example Company review.

Answer these questions in the PR-readiness notes:

- **Smallest PR:** Is this the smallest coherent PR that solves the Linear issue? If not, identify exactly what should be split out.
- **New files justified:** Are every new source file, helper, hook, test, fixture, script, and config file necessary for this issue? If a new file mostly exists because the agent preferred a fresh abstraction, recommend folding it into the nearest existing pattern.
- **Artifacts removed:** Are screenshots, generated images, debug dumps, logs, temp files, local browser artifacts, and exploratory scripts absent from the commit? If present, remove them or call them out as blockers.
- **Nearby patterns matched:** Does the implementation follow the closest existing Example Company patterns for file placement, naming, server actions, tests, hooks, and component boundaries? Prefer the local pattern over a generic "best practice."
- **Commit contents clear:** What exactly would be committed? Summarize the changed files by responsibility before recommending commit or PR creation.

If the answer to any item is weak, treat the PR as not ready until the scope is tightened or the tradeoff is explicitly accepted.

### 3.7. PR scope explainer mode

When running in PR scope explainer mode, produce a file-by-file explanation of the current or planned diff instead of a full PR package.

Use this workflow:

1. **Identify the scope:** Inspect `git status --short`, `git diff --stat`, `git diff --name-status`, staged changes, and untracked files. If implementation has not started, use the current plan or Linear issue to describe the intended files and likely risks.
2. **Separate file categories:** Group files as app/source, tests, fixtures/mocks, config, generated artifacts, docs, and unrelated/local files.
3. **Explain each changed file:** For every changed file, state what changed, why it changed for this issue, whether it is necessary, and the smallest credible alternative.
4. **Challenge tests directly:** Call out test files that look oversized for the behavior, especially new top-level test files, broad fixtures, snapshot churn, unrelated coverage, or tests that do not match nearby Example Company conventions. Recommend smaller colocated or existing-pattern coverage when appropriate.
5. **Find shrink opportunities:** Identify exact files, helpers, tests, artifacts, or refactors that can be removed, folded into existing files, deferred, or split into a follow-up PR.
6. **End with a recommendation:** Say whether to keep the PR as-is, shrink before commit, split into multiple PRs, or proceed with a noted tradeoff.

Preferred output for this mode:

1. **Scope verdict:** One direct sentence on whether the PR is appropriately sized.
2. **Changed files:** Bullets in the format `path` - why it changed - keep/remove/split guidance.
3. **Test footprint:** Whether the test changes are right-sized, too broad, missing, or should be moved.
4. **How to make it smaller:** Concrete deletions, folds, or split-outs.
5. **Next action:** What the user or Codex should do before commit/PR.

### 4. Run the required local checks

Run the repo’s required validation before presenting the PR as ready:

```bash
npm run lint
npm run typecheck
npm run test:run
npm run build
```

Report failures clearly and do not present the PR as ready until they pass or the user explicitly accepts the risk.

### 5. Prepare commit guidance

Draft descriptive commit messages that explain both what changed and why.

- Avoid vague messages like `fix`, `updates`, or `WIP`.
- Respect the user preference not to commit automatically unless explicitly asked.
- If the user asks to commit, show what would be committed first.

### 6. Draft the PR

Produce a PR title and body aligned to `.github/pull_request_template.md`.

Include:

- Summary of what changed and why
- Linked Linear issue
- Type of change
- Checklist status
- Database change note
- Screenshots reminder for UI changes
- Breaking change note
- Additional notes for reviewers

Keep the title clear and specific. Keep the PR focused on the single issue.

### 7. Route review correctly

Use `.github/CODEOWNERS` to determine likely required reviewers.

Current notable routing:

- Default: `@example-company/core`
- `prisma/schema.prisma`: `@jimmycozza @braindev`
- `prisma/migrations/`: `@jimmycozza @braindev`
- `*.sql`: `@jimmycozza @braindev`

If database or Prisma files changed, explicitly call out that backend review is required.

### 8. Respect review and merge rules

After a PR is opened:

- Respond to all review comments
- Push fixes as new commits
- Do not force-push during review
- Re-request review after fixes
- Do not merge without approval
- Expect squash merge to `main`

## Preferred Output

When using this skill, respond with a practical PR-prep package:

1. PR readiness status
2. Missing blockers or policy violations
3. Proposed branch name if relevant
4. Proposed commit message if relevant
5. Proposed PR title
6. Proposed PR body matching the repo template
7. Tiny PR critic notes: smallest PR, new files, artifacts, nearby patterns, exact commit contents
8. PR scope explainer when requested or when the diff looks larger than necessary
9. Reviewer guidance from `CODEOWNERS`

## Reference

If a quick reminder is enough, consult [references/current-rules.md](references/current-rules.md). If anything seems stale, re-read the repo files listed above.
