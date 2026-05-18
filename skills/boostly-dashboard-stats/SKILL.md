---
name: boostly-dashboard-stats
description: Query the same Example Company Reporting dashboard stats locally from the boostly-reporting repo. Use when the user asks for Product dashboard stats, Campaigns dashboard stats, customer journey readout data, sales/SDR/CSM/activation transcript dashboard stats, marketing Meta Ads stats, SEO/product funnel stats, or wants to inspect dashboard data without using the browser.
---

# Example Company Dashboard Stats

Use this skill to pull dashboard data locally from `/Users/you/Programming/boostly-reporting` using the same data-loading functions the dashboard uses.

## Quick Command

Run from any directory:

```bash
cd /Users/you/Programming/boostly-reporting/apps/dashboard
npx tsx /Users/you/.codex/skills/boostly-dashboard-stats/scripts/dashboard-stats.ts --section all --format summary
```

Useful variants:

```bash
# Product dashboard only, JSON output
npx tsx /Users/you/.codex/skills/boostly-dashboard-stats/scripts/dashboard-stats.ts --section product --format json

# Campaigns dashboard, default last 7 days
npx tsx /Users/you/.codex/skills/boostly-dashboard-stats/scripts/dashboard-stats.ts --section campaigns --format summary

# Campaigns dashboard for a custom range
npx tsx /Users/you/.codex/skills/boostly-dashboard-stats/scripts/dashboard-stats.ts --section campaigns --start-date 2026-05-01 --end-date 2026-05-07 --format json

# Save full JSON for local inspection
npx tsx /Users/you/.codex/skills/boostly-dashboard-stats/scripts/dashboard-stats.ts --section all --format json --out /tmp/boostly-dashboard-stats.json

# Force the primary database only when you explicitly need it
npx tsx /Users/you/.codex/skills/boostly-dashboard-stats/scripts/dashboard-stats.ts --section campaigns --use-primary
```

## What It Pulls

`--section product` includes:

- Customer Journey Readout
- Marketing / Meta Ads
- Sales, SDR, Inbound, Activation, and CSM transcript dashboard stats
- In-store TapCards, Boxes, Texting, fulfillment, SEO, and Box Economics data

`--section campaigns` includes:

- CSM and account filters
- Campaign details by type and name
- Engagement metrics and promotion names
- Subscriber timeline and rolling growth
- Contact activity, contact sources, and invite eligibility

## Options

- `--section all|product|campaigns` defaults to `all`
- `--format summary|json` defaults to `summary`
- `--days 14` controls transcript segment windows
- `--start-date YYYY-MM-DD` and `--end-date YYYY-MM-DD` control campaign windows; default is the last 7 days
- `--group-by-location` matches the Campaigns dashboard location toggle
- `--csm-id <id>` and `--account-id <id>` apply Campaigns filters
- `--db-url-env <name>` forces a specific env var to be used as `DATABASE_URL`
- `--use-primary` keeps the configured primary `DATABASE_URL`
- `--out <path>` writes JSON to disk

## Notes

- The command expects the repo's `apps/dashboard/.env.local` or shell environment to contain the same DB/API env vars used by the dashboard.
- For local query work, the script prefers a read-only/read-replica database URL over the writable primary. It checks these env vars in order:
  - `BOOSTLY_REPORTING_READONLY_DATABASE_URL`
  - `READONLY_DATABASE_URL`
  - `V2_READ_REPLICA_DATABASE_URL`
  - `V2_READONLY_DATABASE_URL`
  - `V2_DATABASE_URL`
  - `DATABASE_READONLY_URL`
  - `REPLICA_DATABASE_URL`
- When a read-only URL is found, the script routes both `DATABASE_URL` and `SALES_DATABASE_URL` to it for this process only. Use `--use-primary` only if you intentionally need the primary connection.
- The summary prints only the selected env var name and host, never the connection string.
- Do not print secrets from env files. The script only outputs dashboard data.
- Prefer `--format summary` for conversational answers and `--format json --out ...` for deeper local inspection.
