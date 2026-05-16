---
name: render-readonly
description: Reporting-only Render operations for inspecting and maintaining the ExampleCo Reporting Render project. Use when the user asks about Render deploys, Render logs, Render service status, production deploy investigation, Render API inspection, or Reporting cron environment variables.
---

# Render Reporting

Use this skill for Render observability, deploy investigation, and narrowly scoped maintenance of the ExampleCo Reporting Render project.

This skill is no longer globally read-only. It is **Reporting-only**:

- Allowed target repo: `https://github.com/ExampleCo/exampleco-reporting`
- Allowed owner/team: `ExampleCo`
- Allowed service family: Reporting services/cron jobs for this repo, currently `cron - sales call reporting`
- Do not create, update, restart, scale, suspend, delete, or mutate any non-Reporting Render resource.
- Do not update env vars on shared ExampleCo app services, staging services, customer-facing services, or unrelated cron jobs.

## Setup

The bundled script uses only Python standard library.

Required environment:

```bash
export RENDER_API_KEY="..."
```

Optional, useful for logs and scoping:

```bash
export RENDER_OWNER_ID="..."
export RENDER_REPORTING_OWNER_ID="tea-cbfgtpl0malclpe38gu0"
export RENDER_REPORTING_SERVICE_ID="crn-d7sbr1vlk1mc73dmtu70"
```

Create the API key at:

[https://dashboard.render.com/account/api-keys](https://dashboard.render.com/account/api-keys)

If Render supports scoped keys for the account/workspace, choose the narrowest scope that can manage the Reporting cron's environment variables. Treat the key as sensitive because the underlying API can do more than this skill allows.

## Commands

Run from any directory:

```bash
python3 ~/.codex/skills/render-readonly/scripts/render_read.py owners
python3 ~/.codex/skills/render-readonly/scripts/render_read.py services
python3 ~/.codex/skills/render-readonly/scripts/render_read.py services --name exampleco
python3 ~/.codex/skills/render-readonly/scripts/render_read.py service <serviceId>
python3 ~/.codex/skills/render-readonly/scripts/render_read.py deploys <serviceId> --limit 10
python3 ~/.codex/skills/render-readonly/scripts/render_read.py deploy <serviceId> <deployId>
python3 ~/.codex/skills/render-readonly/scripts/render_read.py logs --owner <ownerId> --resource <serviceId> --minutes 60 --text error --limit 50
python3 ~/.codex/skills/render-readonly/scripts/render_read.py env-vars <serviceId>
python3 ~/.codex/skills/render-readonly/scripts/render_read.py set-env-var <serviceId> <KEY> --value "$VALUE"
```

## Investigation Flow

1. Run `owners` if `RENDER_OWNER_ID` is unknown.
2. Run `services --name <app-name>` to find the target service ID.
3. Run `deploys <serviceId> --limit 5` to inspect recent deploy status.
4. Run `deploy <serviceId> <deployId>` for details on a suspicious deploy.
5. Run `logs --owner <ownerId> --resource <serviceId> --minutes 30 --text <term>` for runtime or deploy errors.
6. For Reporting cron env maintenance, run `service <serviceId>` first and confirm:
   - `repo` is `https://github.com/ExampleCo/exampleco-reporting`
   - `rootDir` is `apps/dashboard`
   - service name is a Reporting service, currently `cron - sales call reporting`
7. Run `env-vars <serviceId>` to inspect only variable names or redacted values.
8. Use `set-env-var <serviceId> <KEY> --value "$VALUE"` only for Reporting cron variables needed by the reporting dashboard jobs.

## Reporting Cron Required Env Vars

The Reporting sales cron expects these env vars:

- `SALES_DATABASE_URL` — primary V2 PostgreSQL connection string, not Supabase and not the read replica.
- `ASKELEPHANT_API_KEY` — AskElephant REST API key.
- `HUBSPOT_API_KEY` — HubSpot private app token for CRM matching.
- `ANTHROPIC_API_KEY` — Anthropic key for transcript analysis.
- `SALES_ANALYSIS_MODEL` — currently `claude-sonnet-4-6`.
- `SALES_ANALYSIS_CONCURRENCY` — bounded concurrent per-call analysis, default `5`.
- `SALES_ANALYSIS_NEW_CALL_LIMIT` — daily new-call analysis cap, default `20`.

The cron reads/writes these Reporting tables:

- `reporting.call_transcripts`
- `reporting.call_transcript_bodies`
- `reporting.call_transcript_crm_matches`
- `reporting.sales_call_outcomes`
- `reporting.call_transcript_analysis`
- `reporting.call_transcript_analysis_snapshots`

## Safety Rules

- Only use bundled script commands unless the user explicitly asks for broader Render API work.
- Write operations are allowed only for the Reporting service guardrails above.
- Before any write operation, the script must fetch the service and verify it belongs to `ExampleCo/exampleco-reporting`.
- Never call `POST`, `PATCH`, `PUT`, or `DELETE` Render endpoints for non-Reporting services.
- Do not print API keys, env vars, connection strings, or secrets in the final answer.
- Summarize findings with service/deploy IDs and timestamps, but redact sensitive values.
