---
name: meta-ads
description: Use when the user asks to query, analyze, debug, or report on Example Company Meta/Facebook/Instagram ads, ad creatives, ad previews, campaign performance, leads, CPL, spend, messaging, or Meta Marketing API access.
---

# Meta Ads

Use this skill for Example Company Meta Ads questions and implementation work. Prefer the Meta Marketing API directly over the Meta Ads CLI unless the user specifically asks for CLI exploration.

## Required Environment

Use env vars. Never paste tokens back to the user or write them into tracked files.

```bash
META_ACCESS_TOKEN=...
META_AD_ACCOUNT_ID=act_2766538970268735
META_API_VERSION=v25.0
```

Known local credential source:

```bash
/Users/you/Programming/example-company-reporting/apps/dashboard/.env.local
```

For local commands, first load from `/Users/you/Programming/example-company-reporting/apps/dashboard/.env.local` using a dotenv-aware loader or parser. Do not `source` it directly unless all values are shell-escaped. If unavailable, load from the current shell, another `.env.local`, Vercel env, or ask the user for a fresh token. If the user pasted a token into chat, treat it as a temporary development token and recommend rotation before production.

## Default Analysis Window

Default to last 30 days at `level=ad`.

Primary metrics:
- Spend: `spend`
- Impressions: `impressions`
- Clicks: `clicks`
- CTR: `ctr`
- CPC: `cpc`
- Leads: prefer action type `lead`; only use fallbacks if `lead` is absent
- CPL: `spend / leads`

Lead fallback order:
1. `lead`
2. `onsite_conversion.lead_grouped`
3. `offsite_complete_registration_add_meta_leads`
4. `offsite_conversion.fb_pixel_lead`
5. `onsite_web_lead`

Do not sum all lead-like action aliases together; Meta often returns multiple aliases for the same conversion.

## Common Queries

Use the helper script when possible:

```bash
python /Users/you/.codex/skills/meta-ads/scripts/meta_ads_query.py insights --limit 100
python /Users/you/.codex/skills/meta-ads/scripts/meta_ads_query.py ads --limit 25
python /Users/you/.codex/skills/meta-ads/scripts/meta_ads_query.py preview AD_ID
python /Users/you/.codex/skills/meta-ads/scripts/meta_ads_query.py video VIDEO_ID
```

Raw Graph API equivalents:

```bash
curl -sS --get "https://graph.facebook.com/${META_API_VERSION}/${META_AD_ACCOUNT_ID}/insights" \
  --data-urlencode "date_preset=last_30d" \
  --data-urlencode "level=ad" \
  --data-urlencode "fields=ad_id,campaign_name,adset_name,ad_name,spend,impressions,clicks,ctr,cpc,reach,actions" \
  --data-urlencode "limit=100" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"
```

Creative copy:

```bash
curl -sS --get "https://graph.facebook.com/${META_API_VERSION}/AD_ID" \
  --data-urlencode "fields=id,name,effective_status,campaign{name},adset{name},creative{id,name,title,body,object_story_spec,asset_feed_spec}" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"
```

Ad preview iframe:

```bash
curl -sS --get "https://graph.facebook.com/${META_API_VERSION}/AD_ID/previews" \
  --data-urlencode "ad_format=DESKTOP_FEED_STANDARD" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"
```

Video source may fail with `(#10) Application does not have permission for this action`; use ad previews as the reliable fallback.

## Messaging Analysis

When asked “what messaging is working,” group ads by a mix of ad name, campaign/adset, headline, and primary text.

Useful Example Company theme buckets:
- Empty seats / fill tables
- Repeat visits / loyalty
- Pizza operator angle
- Social proof / testimonials
- Delivery app cost reduction
- Fast setup
- General business growth

Sort themes by CPL when leads exist. Also call out spend concentration so low-CPL tiny tests do not get overinterpreted.

## Dashboard Safety

If wiring Meta Ads into an app:
- Fetch Meta server-side only.
- Store credentials in environment variables, not source code.
- Never expose `META_ACCESS_TOKEN` client-side.

## Security

- Treat user-pasted tokens as compromised after use.
- Use Vercel encrypted env vars for production.
- Prefer read-only `ads_read`; add broader permissions only when a specific query requires them.
- Avoid printing full URLs that include access tokens because Graph API paging URLs include tokens.
