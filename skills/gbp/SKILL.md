---
name: gbp
description: Use ExampleCo's Google Business Profile API credentials to audit managed GBP listings, count locations, search by restaurant name or Google place ID, and compare ExampleCo product database locations against current GBP access.
---

# GBP

Use this skill when the user asks whether ExampleCo manages SEO/GBP for a restaurant, wants counts of GBP listings, or wants to inspect current Google Business Profile listing data.

## Source of Truth

Default project:

```text
~/Programming/exampleco-reporting/apps/dashboard
```

Credentials live in `.env.local`:

- `GOOGLE_OAUTH_CLIENT_ID`
- `GOOGLE_OAUTH_CLIENT_SECRET`
- `GBP_REFRESH_TOKEN`
- optional `DATABASE_URL` for matching product locations to GBP access

Do not print raw credentials or tokens.

## Quick Commands

From the repo root or dashboard app:

```bash
node ~/.codex/skills/gbp/scripts/gbp-report.mjs summary
node ~/.codex/skills/gbp/scripts/gbp-report.mjs search "Round Bites"
node ~/.codex/skills/gbp/scripts/gbp-report.mjs search-place ChIJ08QphHuBUocRZIP583h8K6w
node ~/.codex/skills/gbp/scripts/gbp-report.mjs product-search "Zulu"
node ~/.codex/skills/gbp/scripts/gbp-report.mjs product-gbp-check "Zulu"
```

## Workflow

1. Use `product-search` to find ExampleCo product DB records and their `google_place_id`.
2. Use `search-place` for each `google_place_id` to verify whether the current GBP credentials can see/manage that listing.
3. If a product DB record has `google_place_id` but `search-place` returns no match, report it as not currently visible in ExampleCo's GBP management account.
4. If `search` finds a listing by name, report the listing title, Google resource name, place ID, maps URL, address, phone, website, primary category, and open status.
5. Use `summary` for total account/listing counts.

## Interpretation

- A location is "GBP managed by ExampleCo" only if it appears in the Google Business Profile API results from the project credentials.
- A location can exist in ExampleCo's product DB with a `google_place_id` and still not be visible through current GBP access.
- The dashboard's SEO "Managed" state is based on matching ordered SEO bundle locations to GBP locations by `google_place_id`.

