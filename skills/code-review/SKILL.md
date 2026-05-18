---
name: code-review
description: >
  Use when reviewing code, checking a diff before deploy, preparing a PR,
  validating a feature/fix, or assessing changes that may affect production.
  Prioritizes bugs, regressions, security/privacy issues, missing tests, and
  production impact. For automations, cron jobs, webhooks, migrations, bulk
  sends, billing, external API calls, or production data mutations, requires
  an expected-impact review covering scope, guardrails, dry-run, alerting,
  rollout, and rollback. For ClaudeFluent / cf / claude_course work, also use
  the cf-release skill before approving or deploying production changes. For
  Example Company / boostly repo work, also use the boostly-pr-process skill.
---

# Code Review

Use this skill for review-oriented work and for final pre-deploy checks on code
you changed. Lead with concrete risks, not a general summary.

## Related Skills

- For ClaudeFluent / `cf` / `claude_course` production changes, also use
  `cf-release` and apply its release checklist. This is required when the diff
  touches Vercel, Convex, cron jobs, env vars, email sends, Stripe, sessions,
  onboarding, admin workflows, or anything customer-facing.
- For Example Company / `boostly` repo work, also use `boostly-pr-process` and apply
  its repo-specific PR workflow. This is required when reviewing Example Company diffs,
  preparing PRs, checking PR readiness, validating branch naming, routing
  reviewers, or deciding whether a Example Company change is ready to publish. Always
  include the tiny PR critic pass from that skill: smallest coherent PR, new
  files justified, artifacts removed, nearby patterns matched, and exact commit
  contents understood.

## Standard Review

When asked to review code, inspect the actual diff and surrounding code. Report
findings first, ordered by severity, with file and line references.

Look for:

- correctness bugs and behavioral regressions
- data loss, duplicate sends, duplicate charges, or broken idempotency
- security, privacy, auth, and secret-handling issues
- production configuration assumptions
- edge cases around nulls, old data, migrations, retries, concurrency, and time zones
- missing tests or verification for risky paths
- over-complex code that obscures failure modes

If there are no findings, say that clearly and mention remaining test gaps or
residual risk.

## Example Company-Specific Review Checks

For Example Company / `boostly` repo diffs, apply these checks in addition to the
standard review. These are concrete codebase-fit checks, not generic style
preferences.

- **Tiny PR shape:** Check whether the diff is the smallest coherent PR for the
  Linear issue. Flag unrelated edits, opportunistic refactors, and files that
  should be split into a follow-up PR.
- **New files and artifacts:** Verify that every new file is justified by local
  patterns and that screenshots, generated images, logs, temp files, debug
  artifacts, local browser artifacts, and exploratory scripts are excluded.
- **Commit contents clarity:** Summarize what exactly would be committed and why
  each changed file belongs in this PR before calling it ready.
- **Components vs hooks:** Flag components that own debouncing, async server
  action orchestration, request race handling, form import/export logic, or
  larger business rules. Prefer a focused colocated hook so the component mostly
  renders.
- **Form hook scope:** Existing edit/create form hooks should stay centered on
  form defaults, save behavior, routing, breadcrumbs, and unsaved-change
  handling. Flag substantial domain-specific workflows that should be extracted
  to sibling hooks.
- **Domain logic location:** Integration-specific behavior belongs in the
  integration layer. For example, Google Places stale-ID messaging, API response
  parsing, error translation, and supported-field mapping should live near
  `src/lib/google-places.ts` or a focused Google utility, not in page actions or
  presentation components.
- **Server action conventions:** Compare new actions to nearby actions. Prefer
  `withFormValidation`, `ServerActionResult`, `FieldError`, `handleServerErrors`,
  and `getErrorMessage` where they match the local pattern. Flag hand-rolled
  result and error shapes that duplicate existing helpers.
- **Thin data shapes:** Flag wrapper types that only wrap one useful value, such
  as `{ formValues: Partial<FormData> }`, unless they add real meaning. Prefer
  returning the useful value directly.
- **DB-backed invariants:** If the feature depends on uniqueness, ownership,
  idempotency, or one-to-one mapping, check whether that is enforced at the DB or
  mutation boundary. UI-only states such as disabled buttons or "already added"
  cards are useful UX but not sufficient protection.
- **External API cancellation:** For fan-out or optional external calls, such as
  thumbnail fetches, check that timeouts cancel the underlying request with
  `AbortController` where feasible. A plain `Promise.race` can still leave the
  request running and consuming quota.
- **Shared component blast radius:** Treat edits to shared hooks/components as
  high-risk review areas. Ask whether the new API is generic and useful beyond
  one screen. Avoid context/global state for one direct call site; avoid copying
  a shared wizard just to dodge a small generic extension.
- **Utility naming and placement:** Standalone feature helpers under `_shared`
  should generally live in `_shared/_utils/` and be named for what they do. Flag
  vague utility names that hide whether the file parses data, computes changes,
  maps fields, or renders UI.
- **One-off abstractions:** Flag named helpers introduced for a single use when
  nearby code uses inline transforms. Prefer small inline code unless the helper
  has reuse or a strong domain concept.

## Production Impact Section

For changes that can affect real users, money, data, emails/messages, external
APIs, scheduled jobs, or production state, include a compact production impact
review before finalizing.

Minimum fields:

- `Side effect:` what the change can do
- `Estimated scope:` count of affected records/users/actions, or why it could not be counted
- `Eligibility:` exact predicates deciding inclusion
- `Guardrails:` idempotency marker, cutoff date/window, allowlist, dry-run, and duplicate prevention
- `Alerts:` what notifies on success, partial failure, suspicious skip, or crash
- `Rollback:` how to stop the job and repair bad effects

## Required Data Checks

When feasible, inspect production-shaped data before approving risky changes.

- Query counts of records that match the eligibility rules.
- Check whether durable markers are populated on historical records.
- Break counts down by useful grouping: tenant, company, session, status, age,
  environment, or owner.
- Verify required deployment env vars in the actual target environment.

Do not print secrets.

## Red Flags

Stop and fix before deploy if any of these are true:

- A cron scans all rows without a launch cutoff, time window, or allowlist.
- Historical records can be swept in accidentally.
- A durable marker exists in schema but is sparsely populated in production.
- Retrying can resend, recharge, recreate, delete, or re-notify.
- A job sends to customers with no dry-run or no alerting.
- Required env vars are assumed but not verified in the target deployment.
- Failure handling marks work complete before the side effect succeeds.
- Migration/backfill logic relies on null/default values without checking old rows.

## Final Shape

For pure reviews:

1. Findings
2. Open questions or assumptions
3. Test gaps / residual risk

For implementation work with risky production impact:

1. What changed
2. Verification
3. Production Impact
4. Remaining risks / next deploy steps
