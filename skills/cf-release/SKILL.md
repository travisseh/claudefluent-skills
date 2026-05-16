---
name: cf-release
description: >
  ClaudeFluent production release checklist. Use for any ClaudeFluent / cf /
  claude_course production deploy, release, cron enablement, Vercel deploy,
  Convex deploy, env var change, schema/function change, admin workflow change,
  email automation, Stripe/payment change, onboarding/session change, or
  production-impact review before shipping ClaudeFluent work.
---

# ClaudeFluent Release

Use with `cf` and `code-review` whenever ClaudeFluent work is going to production
or could affect production users/data.

## Scope

Canonical paths:

- Repo: `~/Programming/personal-master/personal/claude_course`
- Website: `~/Programming/personal-master/personal/claude_course/website`
- Vercel project: linked from `website/.vercel/project.json`
- Production Convex URL: usually `https://polite-toad-76.convex.cloud`

## Pre-Release Checklist

1. Git hygiene:
   - Run `git status --short` at repo root.
   - Stage/commit only files relevant to the release.
   - Do not include unrelated dirty worktree changes.

2. TypeScript/build:
   - Run from `website`: `npx tsc --noEmit`.
   - For larger frontend/runtime changes, also run `npm run build` when practical.

3. Convex dependency check:
   - If `website/convex/**` changed, production Convex must be deployed.
   - If a Vercel route calls new Convex functions or depends on new schema fields,
     deploy Convex production before or alongside Vercel.
   - Preferred command:
     `CONVEX_DEPLOYMENT=prod:polite-toad-76 npx convex deploy -y`
   - If local env has `CONVEX_DEPLOYMENT`, `npm run convex:deploy:prod` is fine.
   - Confirm deploy output includes schema validation and finalized push.

4. Vercel env vars:
   - Verify required vars in the linked Vercel project with `vercel env ls`.
   - Check Production, Preview, and Development scopes when the code can run there.
   - Never assume local `.env` values exist in Vercel.
   - Common ClaudeFluent vars:
     - `CRON_SECRET`
     - `NEXT_PUBLIC_CONVEX_URL`
     - `NEXT_PUBLIC_CONVEX_SITE_URL`
     - `GOOGLE_SERVICE_ACCOUNT_JSON`
     - `STRIPE_SECRET_KEY`
     - `STRIPE_WEBHOOK_SECRET`
     - `ANTHROPIC_API_KEY`
     - `OPENAI_API_KEY`
     - `TELEGRAM_BOT_TOKEN`
     - `ALLOWED_TELEGRAM_USERS` or `TELEGRAM_CHAT_ID`
     - `GRAIN_API_TOKEN` / `GRAIN_PAT`

5. Production impact:
   - Identify side effects: sends, writes, charges, deletes, public content, cron runs.
   - Query production-shaped data when possible to estimate affected records.
   - For email/message/payment/data mutations, require:
     - launch cutoff or allowlist
     - dry-run mode where practical
     - durable idempotency marker
     - duplicate prevention across retries
     - alerting on material success/failure
     - rollback/disable path

6. Crons and automations:
   - Confirm `vercel.json` changes are intentional and not carrying unrelated cron edits.
   - Check cron route authorization with `CRON_SECRET`.
   - Avoid hourly alert spam; use cooldowns or state markers.
   - Confirm no historical rows can be swept in accidentally.

7. Email/customer communication:
   - Inspect templates and merge fields.
   - Verify production recipients/scope.
   - Ensure audit logging failure cannot cause duplicate sends.
   - For automated sends, mark/lock before or immediately around delivery in a way
     that prevents retries from resending.

8. Deploy ordering:
   - Convex first when Convex functions/schema changed.
   - Then Vercel deploy or push-triggered deployment.
   - After deploy, inspect the relevant Vercel deployment/build logs if anything
     touches runtime routes, cron jobs, or env vars.

## Final Release Report

Before saying the release is done, include:

- `Committed/pushed:` commit hash and branch, if applicable
- `Convex:` deployed/not needed, with deployment URL if deployed
- `Vercel:` deployed/push-triggered/not deployed
- `Env vars:` verified names and scopes, without values
- `Production impact:` scope and guardrails
- `Rollback:` exact disable/revert path
- `Verification:` TypeScript/build/browser/data checks performed

## Hard Stop Conditions

Do not recommend production deploy until resolved:

- Convex changed but production Convex has not been deployed.
- Required Vercel env vars are missing.
- A cron scans old data without cutoff/window/allowlist.
- A send/charge/delete mutation can retry without durable idempotency.
- Customer-facing automation has no alerting or no disable path.
- Unrelated dirty files are staged for the release.
