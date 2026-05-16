---
name: v2-database
description: Query the ExampleCo V2 production database for campaign data, accounts, locations, contacts, users, messaging metrics, MCP activity logs, and reporting-schema analytics. Use when needing V2 platform data for product analytics, PMF survey targeting, understanding customer lifecycle, analyzing MCP tool usage, or distinguishing the primary production instance from the read replica.
enabled: true
tags: [exampleco, v2, database, campaigns, accounts]
---

# ExampleCo V2 Database

Production PostgreSQL database for the ExampleCo V2 texting platform.

## Connection

Credentials stored in `.local/v2-db.env` (gitignored).

```bash
source .local/v2-db.env && PGPASSWORD="$V2_DB_PASSWORD" psql "postgresql://$V2_DB_USER@$V2_DB_HOST:$V2_DB_PORT/$V2_DB_NAME?sslmode=require" -c "QUERY"
```

Default posture: **read-only unless the user explicitly asks for reporting-schema writes**. Never write to `public` app tables, `airbyte_raw`, or the read replica.

## Database Instances, Schemas, and Grants

ExampleCo has two production PostgreSQL database instances:

### Primary production instance
- This is the live production Postgres server that runs the application.
- Use this instance when a task requires writing to `reporting.*`.
- Primary host to use for that work: `136.117.42.254`.
- It has the same three main schemas:
  - `public` — live app data. Most users can query this. Only a small set of app/migration users write here, including `exampleco_migration`, `exampleco_app`, and `exampleco_consumers`.
  - `airbyte_raw` — Airbyte-ingested raw data. Only the Airbyte user writes here; most users cannot read it.
  - `reporting` — analytics/reporting schema. `ops` and `user` can write here.
- User/grant notes:
  - `ops` can write to `reporting.*` and can select from `public` and `airbyte_raw`.
  - `user` can write to `reporting.*`.
  - `david` is highly restricted. David the person connects using the `ops` database user for broader production/reporting work.

### Production read-replica instance
- This is a completely separate Postgres server with its own host/IP and process.
- It receives data from the primary with near-real-time replication, typically around 30-90 seconds of lag for large queries or mutations.
- It inherits the same users, passwords, schemas, and grants as the primary, but the server itself rejects all writes.
- By definition, nobody can write to `public`, `airbyte_raw`, or `reporting` on the read replica, regardless of grants.
- Use the read replica for read-only analytics queries when no reporting write is needed.

Practical rule:
- Querying existing V2 data: prefer the read replica / current `.local/v2-db.env` host.
- Creating or refreshing reporting tables/materialized data: use the primary production host (`136.117.42.254`) with a user that has `reporting.*` write access.
- Never point write workflows at the read replica; they will fail even if the user appears to have write grants.

## Schema Overview (73 tables)

### Core Entities
- **accounts** — restaurant accounts (id, name, primary_user_id, hubspot_company_id, status, billing_model)
- **locations** — physical restaurant locations (id, account_id, name, timezone, sender_number_id, hubspot_company_id)
- **users** — ExampleCo users/staff (id, name, email, phone, openphone_number, is_admin)
- **account_users** — maps users to accounts with roles (user_id, account_id, role, is_primary_account)
- **contacts** — restaurant's subscribers/customers (id, location_id, first_name, last_name, opt_in_state, source)

### Campaigns & Messaging
- **campaigns** — text campaigns (id, account_id, status [cancelled/completed/failed/scheduled/sending], type [claim_race/inform/invite/lottery/promotional/caller_99/bday_poll/pick_a_promo/trick_or_treat/gameday], sent_at, scheduled_for, location_ids)
- **campaign_templates** — reusable campaign templates
- **campaign_rotations** — rotation schedules
- **messages** — individual sent messages
- **message_counts** — per-location message volume
- **billable_message_counts** — billing-relevant message counts

### Onboarding & Launch
- **launches** — location launch records (id, location_id, launched_at) — NOTE: launched_at is often NULL, use first completed campaign as proxy
- **enrollment_sessions** — onboarding enrollment tracking

### Reviews & Engagement
- **reviews** — internal sentiment survey responses (id, location_id, contact_id, promotion_id, sentiment_overall [great/okay/bad], sentiment_product, sentiment_service, comment, source [campaign/touchpoint], started_google_review bool — flags click-through to Google CTA, not actual Google post)
- **offers** — issued offers per contact per campaign (id, account_id, location_id, contact_id, campaign_id, promotion_id, issued_on, status [active/redeemed/expired], redeemed_at, redemption_method [online/in_store/phone], clicked_at, click_count)
- **promotions** — promotion definitions
- **subscribe_links** / **subscribe_link_events** — opt-in link tracking
- **subscribe_widgets** / **subscribe_widget_events** — embeddable widget opt-in tracking

### Integrations
- **toast_integrations** — Toast POS connections
- **chownow_integrations** — ChowNow connections

### Toll-Free Verification (TFV)
- **tfv_submissions** — TFV registration submissions to Twilio (id, sender_number_id, business_name, business_ein, contact_email, contact_phone, business_website, inquiry_id [Twilio's id], submitted_at, submitted_by_user_id, notes)
- **tfv_status_logs** — Twilio webhook events for TFV state changes (id, sender_number_id, previous_status, current_status [PENDING_REVIEW/IN_REVIEW/TWILIO_APPROVED/TWILIO_REJECTED/DELETED], event_type, rejection_reason, event_payload jsonb, created_at)

### MCP (Model Context Protocol)
- **mcp_api_keys** — API keys for MCP access (id, user_id, name, key_prefix, last_used_at, expires_at, revoked_at, created_at)
- **mcp_activity_logs** — every MCP tool call (id, mcp_api_key_id, user_id, tool_name, arguments_json, result_status [success/error], error_message, duration_ms, created_at)

## Product Metrics

Canonical definitions and reusable queries for the metrics that show up in dashboards, scorecards, and ad-hoc product analytics.

### Active Account (canonical)

An **active account** is `status='enabled'` AND has at least one `completed` campaign with `sent_at` in the last 90 days, with `deleted_at IS NULL`.

- Status enum: `enabled`, `disabled`, `pending`, `paused` — there is no `'active'` value, "active" is a derived metric
- 90-day window picks up restaurants on slow/seasonal cadences while still excluding lapsed accounts
- ~868 active accounts as of 2026-04-28

```sql
WITH active_accounts AS (
  SELECT a.id, a.name, a.created_at
  FROM accounts a
  WHERE a.deleted_at IS NULL
    AND a.status = 'enabled'
    AND EXISTS (
      SELECT 1 FROM campaigns c
      WHERE c.account_id = a.id
        AND c.status = 'completed'
        AND c.sent_at >= NOW() - INTERVAL '90 days'
    )
)
SELECT COUNT(*) FROM active_accounts;
```

Use this CTE as the leading definition of "account" for any time-to-value, retention, or activation metric.

### Time to Value: First N Subscribers

Days from `account.created_at` to the Nth opted-in contact. Reach rate, mean, median, P90.

```sql
-- Replace :N (5, 10, 25...) and the cohort filter window as needed
WITH active_accounts AS (
  SELECT a.id, a.created_at FROM accounts a
  WHERE a.deleted_at IS NULL AND a.status='enabled'
    AND a.created_at >= NOW() - INTERVAL '6 months'   -- cohort window
    AND EXISTS (SELECT 1 FROM campaigns c WHERE c.account_id=a.id
                AND c.status='completed' AND c.sent_at >= NOW()-INTERVAL '90 days')
),
ranked_subs AS (
  SELECT aa.id AS account_id, aa.created_at AS account_created, ct.created_at AS sub_at,
         ROW_NUMBER() OVER (PARTITION BY aa.id ORDER BY ct.created_at) AS n
  FROM active_accounts aa
  JOIN locations l ON l.account_id = aa.id
  JOIN contacts  ct ON ct.location_id = l.id
  WHERE ct.deleted_at IS NULL
    AND ct.opt_in_state='opted_in'
    AND ct.created_at >= aa.created_at  -- exclude V1 migration artifacts
)
SELECT
  (SELECT COUNT(*) FROM active_accounts) AS active_accounts,
  COUNT(*) FILTER (WHERE n=:N) AS reached_n,
  ROUND(100.0*COUNT(*) FILTER (WHERE n=:N)/(SELECT COUNT(*) FROM active_accounts), 1) AS pct_reached,
  ROUND(AVG(EXTRACT(EPOCH FROM (sub_at-account_created))/86400) FILTER (WHERE n=:N)::numeric,1) AS avg_days,
  ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (sub_at-account_created))/86400) FILTER (WHERE n=:N)::numeric,1) AS median_days,
  ROUND(PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (sub_at-account_created))/86400) FILTER (WHERE n=:N)::numeric,1) AS p90_days
FROM ranked_subs;
```

Reference numbers (active accounts created in last 6 months, n=227, as of 2026-04-28):
- First **5** subs: median 1.6 days
- First **10** subs: median 7.0 days, avg 13.2, P90 31.1, 85.5% reach it

### Time to Value: First N Redemptions

Days from `account.created_at` to the Nth offer with `redeemed_at IS NOT NULL`. Same shape as subscribers.

```sql
-- Replace :N (5, 10...) and cohort window as needed
WITH active_accounts AS (
  SELECT a.id, a.created_at FROM accounts a
  WHERE a.deleted_at IS NULL AND a.status='enabled'
    AND a.created_at >= NOW() - INTERVAL '6 months'
    AND EXISTS (SELECT 1 FROM campaigns c WHERE c.account_id=a.id
                AND c.status='completed' AND c.sent_at >= NOW()-INTERVAL '90 days')
),
ranked_red AS (
  SELECT aa.id AS account_id, aa.created_at AS account_created, o.redeemed_at,
         ROW_NUMBER() OVER (PARTITION BY aa.id ORDER BY o.redeemed_at) AS n
  FROM active_accounts aa
  JOIN offers o ON o.account_id = aa.id
  WHERE o.deleted_at IS NULL
    AND o.redeemed_at IS NOT NULL
    AND o.redeemed_at >= aa.created_at
)
SELECT
  (SELECT COUNT(*) FROM active_accounts) AS active_accounts,
  COUNT(*) FILTER (WHERE n=:N) AS reached_n,
  ROUND(100.0*COUNT(*) FILTER (WHERE n=:N)/(SELECT COUNT(*) FROM active_accounts), 1) AS pct_reached,
  ROUND(AVG(EXTRACT(EPOCH FROM (redeemed_at-account_created))/86400) FILTER (WHERE n=:N)::numeric,1) AS avg_days,
  ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (redeemed_at-account_created))/86400) FILTER (WHERE n=:N)::numeric,1) AS median_days,
  ROUND(PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (redeemed_at-account_created))/86400) FILTER (WHERE n=:N)::numeric,1) AS p90_days
FROM ranked_red;
```

Reference numbers (active accounts created in last 6 months, n=227, as of 2026-04-28):
- First **5** redemptions: median 40.8 days, avg 47.3, P90 103.7, 82.8% reach it

Important caveats when interpreting redemption metrics:
- `bday_poll` and `inform` campaign types generate **zero** offers — accounts that lean on those early will have artificially delayed first redemption
- Underlying redeem-rate is ~3.83% (1 in 26 offers). Click rate is ~21%
- Redemption methods: 60% online (auto-tracked), 39% in_store (requires staff to mark), 1% phone — in-store likely under-counted

### Time to Value: First N Reviews (sentiment survey responses)

The `reviews` table is **ExampleCo's internal sentiment survey** — customers respond `great` / `okay` / `bad` to the post-experience text. It's not an external Google review platform. When a customer answers `great`, they get a CTA to leave a Google review; `started_google_review = true` flags the click-through (not the actual Google post).

```sql
-- Replace :N (5, 10...) and cohort window
WITH active_accounts AS (
  SELECT a.id, a.created_at FROM accounts a
  WHERE a.deleted_at IS NULL AND a.status='enabled'
    AND a.created_at >= NOW() - INTERVAL '6 months'
    AND EXISTS (SELECT 1 FROM campaigns c WHERE c.account_id=a.id
                AND c.status='completed' AND c.sent_at >= NOW()-INTERVAL '90 days')
),
ranked_reviews AS (
  SELECT aa.id AS account_id, aa.created_at AS account_created, r.created_at AS review_at,
         ROW_NUMBER() OVER (PARTITION BY aa.id ORDER BY r.created_at) AS n
  FROM active_accounts aa
  JOIN locations l ON l.account_id = aa.id
  JOIN reviews    r ON r.location_id = l.id
  WHERE r.deleted_at IS NULL AND r.created_at >= aa.created_at
)
SELECT
  (SELECT COUNT(*) FROM active_accounts) AS active_accounts,
  COUNT(*) FILTER (WHERE n=:N) AS reached_n,
  ROUND(100.0*COUNT(*) FILTER (WHERE n=:N)/(SELECT COUNT(*) FROM active_accounts), 1) AS pct_reached,
  ROUND(AVG(EXTRACT(EPOCH FROM (review_at-account_created))/86400) FILTER (WHERE n=:N)::numeric,1) AS avg_days,
  ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (review_at-account_created))/86400) FILTER (WHERE n=:N)::numeric,1) AS median_days,
  ROUND(PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (review_at-account_created))/86400) FILTER (WHERE n=:N)::numeric,1) AS p90_days
FROM ranked_reviews;
```

Reference numbers (active accounts created in last 6 months, n=227, as of 2026-04-28):
- First **5** reviews: median 14.3 days, avg 21.9, P90 55.4, 69.2% reach it

### Time to Value: First N Google Review Click-Throughs

Same shape but filtered to `started_google_review = true`. This is the closest proxy for "the customer left a Google review" — but only counts the *click* on the Google CTA, not the actual posted review (ExampleCo doesn't ingest Google's review platform data).

```sql
WITH active_accounts AS (
  SELECT a.id, a.created_at FROM accounts a
  WHERE a.deleted_at IS NULL AND a.status='enabled'
    AND a.created_at >= NOW() - INTERVAL '6 months'
    AND EXISTS (SELECT 1 FROM campaigns c WHERE c.account_id=a.id
                AND c.status='completed' AND c.sent_at >= NOW()-INTERVAL '90 days')
),
ranked_google AS (
  SELECT aa.id AS account_id, aa.created_at AS account_created, r.created_at AS review_at,
         ROW_NUMBER() OVER (PARTITION BY aa.id ORDER BY r.created_at) AS n
  FROM active_accounts aa
  JOIN locations l ON l.account_id = aa.id
  JOIN reviews    r ON r.location_id = l.id
  WHERE r.deleted_at IS NULL
    AND r.started_google_review = true
    AND r.created_at >= aa.created_at
)
SELECT
  (SELECT COUNT(*) FROM active_accounts) AS active_accounts,
  COUNT(*) FILTER (WHERE n=:N) AS reached_n,
  ROUND(100.0*COUNT(*) FILTER (WHERE n=:N)/(SELECT COUNT(*) FROM active_accounts), 1) AS pct_reached,
  ROUND(AVG(EXTRACT(EPOCH FROM (review_at-account_created))/86400) FILTER (WHERE n=:N)::numeric,1) AS avg_days,
  ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (review_at-account_created))/86400) FILTER (WHERE n=:N)::numeric,1) AS median_days,
  ROUND(PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (review_at-account_created))/86400) FILTER (WHERE n=:N)::numeric,1) AS p90_days
FROM ranked_google;
```

Reference numbers (active accounts created in last 6 months, n=227, as of 2026-04-28):
- First **5** Google review click-throughs: median 16.2 days, avg 23.8, P90 58.0, 55.9% reach it

Approximate funnel context: ~85% of survey responses are `great`, ~30% of `great` responses click through to Google. So expect Google clicks to track at ~25% of total review volume.

### TFV (Toll-Free Verification) Metrics

Twilio compliance: every sender number ExampleCo provisions has to clear TFV before it can send. The dashboard tracks rejection rate and cycle times.

**Latest status per sender_number** (the building block for everything below):
```sql
WITH latest_tfv AS (
  SELECT DISTINCT ON (sender_number_id)
         sender_number_id, current_status, created_at AS status_at, rejection_reason
  FROM tfv_status_logs
  ORDER BY sender_number_id, created_at DESC
)
SELECT current_status, COUNT(*) FROM latest_tfv GROUP BY 1 ORDER BY 2 DESC;
```

**Accounts awaiting TFN approval** (PENDING_REVIEW or IN_REVIEW):
```sql
WITH latest_tfv AS (
  SELECT DISTINCT ON (sender_number_id) sender_number_id, current_status, created_at AS status_at
  FROM tfv_status_logs ORDER BY sender_number_id, created_at DESC
)
SELECT a.id, a.name, sub.business_name, lt.current_status, lt.status_at,
       NOW() - lt.status_at AS waiting_for
FROM latest_tfv lt
JOIN tfv_submissions sub ON sub.sender_number_id = lt.sender_number_id
JOIN locations l ON l.sender_number_id = lt.sender_number_id
JOIN accounts  a ON a.id = l.account_id
WHERE lt.current_status IN ('PENDING_REVIEW','IN_REVIEW')
  AND a.deleted_at IS NULL
ORDER BY lt.status_at ASC;
```

**First-decision rejection rate** — share of senders whose first non-pending decision was a rejection:
```sql
WITH first_decision AS (
  SELECT DISTINCT ON (sender_number_id)
         sender_number_id, current_status AS first_decision, created_at AS decided_at
  FROM tfv_status_logs
  WHERE current_status IN ('TWILIO_APPROVED','TWILIO_REJECTED')
  ORDER BY sender_number_id, created_at ASC
)
SELECT
  COUNT(*) AS total_decided,
  COUNT(*) FILTER (WHERE first_decision='TWILIO_REJECTED') AS first_rejected,
  ROUND(100.0*COUNT(*) FILTER (WHERE first_decision='TWILIO_REJECTED')/NULLIF(COUNT(*),0),1) AS rejection_rate_pct
FROM first_decision;
```

**Avg/median days Submitted → Verified** (overall cycle time):
```sql
WITH first_approval AS (
  SELECT DISTINCT ON (sender_number_id)
         sender_number_id, created_at AS approved_at
  FROM tfv_status_logs
  WHERE current_status='TWILIO_APPROVED'
  ORDER BY sender_number_id, created_at ASC
)
SELECT
  COUNT(*) AS verified,
  ROUND(AVG(EXTRACT(EPOCH FROM (fa.approved_at - sub.submitted_at))/86400)::numeric, 1) AS avg_days,
  ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (fa.approved_at - sub.submitted_at))/86400)::numeric, 1) AS median_days
FROM tfv_submissions sub
JOIN first_approval fa ON fa.sender_number_id = sub.sender_number_id
WHERE sub.submitted_at IS NOT NULL;
```

**Avg days Closed (rejected) → Verified** (resubmit cycle time after a rejection):
```sql
-- For each sender that was rejected then later approved, time from latest rejection to first approval after it
WITH rejections AS (
  SELECT sender_number_id, MAX(created_at) AS last_rejected_at
  FROM tfv_status_logs WHERE current_status='TWILIO_REJECTED'
  GROUP BY sender_number_id
),
post_reject_approval AS (
  SELECT r.sender_number_id, r.last_rejected_at,
         MIN(l.created_at) AS approved_at
  FROM rejections r
  JOIN tfv_status_logs l ON l.sender_number_id = r.sender_number_id
   AND l.current_status='TWILIO_APPROVED'
   AND l.created_at > r.last_rejected_at
  GROUP BY r.sender_number_id, r.last_rejected_at
)
SELECT
  COUNT(*) AS rejected_then_verified,
  ROUND(AVG(EXTRACT(EPOCH FROM (approved_at - last_rejected_at))/86400)::numeric, 1) AS avg_days,
  ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (approved_at - last_rejected_at))/86400)::numeric, 1) AS median_days
FROM post_reject_approval;
```

**Total verified this week + share verified in <5 days**:
```sql
WITH this_week AS (
  SELECT DISTINCT ON (l.sender_number_id)
         l.sender_number_id, l.created_at AS approved_at, sub.submitted_at
  FROM tfv_status_logs l
  JOIN tfv_submissions sub ON sub.sender_number_id = l.sender_number_id
  WHERE l.current_status='TWILIO_APPROVED'
    AND l.created_at >= date_trunc('week', NOW())
  ORDER BY l.sender_number_id, l.created_at ASC
)
SELECT
  COUNT(*) AS verified_this_week,
  COUNT(*) FILTER (WHERE EXTRACT(EPOCH FROM (approved_at - submitted_at))/86400 < 5) AS verified_lt_5_days,
  ROUND(100.0*COUNT(*) FILTER (WHERE EXTRACT(EPOCH FROM (approved_at - submitted_at))/86400 < 5)/NULLIF(COUNT(*),0),1) AS pct_lt_5_days
FROM this_week;
```

**Common rejection reasons** (last 90 days):
```sql
SELECT rejection_reason, COUNT(*) AS rejections
FROM tfv_status_logs
WHERE current_status='TWILIO_REJECTED'
  AND created_at >= NOW() - INTERVAL '90 days'
  AND rejection_reason IS NOT NULL
GROUP BY rejection_reason ORDER BY 2 DESC;
```

## Key Queries

### PMF Survey Targeting — Accounts eligible for survey
```sql
-- Accounts with first campaign 14+ days ago, with primary user phone
SELECT a.id, a.name, u.name as owner_name, u.phone as owner_phone, u.email,
       MIN(c.sent_at) as first_campaign_sent,
       COUNT(c.id) as total_campaigns,
       NOW() - MIN(c.sent_at) as days_since_first
FROM accounts a
JOIN campaigns c ON c.account_id = a.id AND c.status = 'completed' AND c.sent_at IS NOT NULL
LEFT JOIN users u ON u.id = a.primary_user_id
WHERE a.deleted_at IS NULL
GROUP BY a.id, a.name, u.name, u.phone, u.email
HAVING MIN(c.sent_at) <= NOW() - INTERVAL '14 days'
ORDER BY first_campaign_sent DESC;
```

### Account health snapshot
```sql
SELECT a.id, a.name, a.status,
       (SELECT COUNT(*) FROM locations l WHERE l.account_id = a.id) as location_count,
       (SELECT COUNT(*) FROM campaigns c WHERE c.account_id = a.id AND c.status = 'completed') as completed_campaigns,
       (SELECT COUNT(*) FROM contacts ct JOIN locations l ON l.id = ct.location_id WHERE l.account_id = a.id AND ct.opt_in_state = 'opted_in') as opted_in_contacts
FROM accounts a
WHERE a.deleted_at IS NULL
ORDER BY a.created_at DESC
LIMIT 20;
```

### Recent campaign volume (last 30 days)
```sql
SELECT DATE(sent_at) as day, COUNT(*) as campaigns,
       COUNT(DISTINCT account_id) as unique_accounts
FROM campaigns
WHERE sent_at >= NOW() - INTERVAL '30 days' AND status = 'completed'
GROUP BY DATE(sent_at) ORDER BY day DESC;
```

### New accounts by week, segmented by location count
```sql
-- Multi-loc vs single-loc account creation, last N weeks
WITH account_locs AS (
  SELECT a.id, a.created_at,
         date_trunc('week', a.created_at)::date AS week_start,
         COUNT(l.id) AS location_count
  FROM accounts a
  LEFT JOIN locations l ON l.account_id = a.id
  WHERE a.created_at >= NOW() - INTERVAL '8 weeks'
    AND a.deleted_at IS NULL
  GROUP BY a.id, a.created_at
)
SELECT week_start,
       COUNT(*) AS total_new,
       COUNT(*) FILTER (WHERE location_count >= 2) AS multi_loc,
       COUNT(*) FILTER (WHERE location_count = 1)  AS single_loc,
       COUNT(*) FILTER (WHERE location_count = 0)  AS no_loc
FROM account_locs
GROUP BY week_start ORDER BY week_start;
```

### Locations-per-account distribution (whole base)
```sql
SELECT CASE
         WHEN loc_count = 1 THEN '1 location'
         WHEN loc_count BETWEEN 2 AND 5 THEN '2-5 locations'
         WHEN loc_count BETWEEN 6 AND 10 THEN '6-10 locations'
         ELSE '11+ locations'
       END AS segment,
       COUNT(*) AS account_count,
       SUM(loc_count) AS total_locations
FROM (
  SELECT a.id, COUNT(l.id) AS loc_count
  FROM accounts a JOIN locations l ON l.account_id = a.id
  WHERE a.deleted_at IS NULL
  GROUP BY a.id
) sub
GROUP BY 1 ORDER BY MIN(loc_count);
```

### Account churn by week (deleted_at)
```sql
SELECT date_trunc('week', deleted_at)::date AS week,
       COUNT(*) AS churned
FROM accounts
WHERE deleted_at >= NOW() - INTERVAL '12 weeks'
GROUP BY 1 ORDER BY 1;
```

### Activation: time from account creation to first completed campaign
```sql
SELECT date_trunc('month', a.created_at)::date AS cohort_month,
       COUNT(DISTINCT a.id) AS accounts,
       PERCENTILE_CONT(0.5) WITHIN GROUP (
         ORDER BY EXTRACT(EPOCH FROM (MIN(c.sent_at) - a.created_at))/86400
       ) AS median_days_to_first_campaign
FROM accounts a
LEFT JOIN campaigns c ON c.account_id = a.id AND c.status = 'completed'
WHERE a.created_at >= NOW() - INTERVAL '6 months'
  AND a.deleted_at IS NULL
GROUP BY a.id, cohort_month;
```

### Contact opt-in stats by location
```sql
SELECT l.name, l.id,
       COUNT(*) FILTER (WHERE c.opt_in_state = 'opted_in') as opted_in,
       COUNT(*) FILTER (WHERE c.opt_in_state = 'opted_out') as opted_out,
       COUNT(*) as total
FROM contacts c
JOIN locations l ON l.id = c.location_id
GROUP BY l.id, l.name
ORDER BY opted_in DESC
LIMIT 20;
```

### MCP usage overview — everyone with a key, whether or not they've made calls
```sql
SELECT u.name, u.email, mak.name AS key_name, mak.key_prefix,
       mak.created_at AS key_created, mak.expires_at, mak.revoked_at,
       COUNT(mal.id) AS total_calls,
       COUNT(mal.id) FILTER (WHERE mal.result_status = 'success') AS successes,
       COUNT(mal.id) FILTER (WHERE mal.result_status = 'error') AS errors,
       ROUND(100.0 * COUNT(mal.id) FILTER (WHERE mal.result_status = 'success') / NULLIF(COUNT(mal.id), 0), 1) AS success_pct,
       ROUND(AVG(mal.duration_ms)) AS avg_duration_ms,
       MAX(mal.created_at) AS last_call
FROM mcp_api_keys mak
JOIN users u ON u.id = mak.user_id
LEFT JOIN mcp_activity_logs mal ON mal.mcp_api_key_id = mak.id
GROUP BY mak.id, u.name, u.email, mak.name, mak.key_prefix, mak.created_at, mak.expires_at, mak.revoked_at
ORDER BY total_calls DESC, mak.created_at DESC;
```

### MCP most common tool calls (last 30 days)
```sql
SELECT mal.tool_name,
       COUNT(*) AS call_count,
       COUNT(DISTINCT mal.user_id) AS unique_users,
       ROUND(AVG(mal.duration_ms)) AS avg_duration_ms,
       COUNT(*) FILTER (WHERE mal.result_status = 'error') AS errors
FROM mcp_activity_logs mal
WHERE mal.created_at >= NOW() - INTERVAL '30 days'
GROUP BY mal.tool_name
ORDER BY call_count DESC;
```

### MCP daily volume (last 30 days)
```sql
SELECT DATE(mal.created_at) AS day,
       COUNT(*) AS total_calls,
       COUNT(DISTINCT mal.user_id) AS unique_users,
       COUNT(*) FILTER (WHERE mal.result_status = 'error') AS errors
FROM mcp_activity_logs mal
WHERE mal.created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(mal.created_at)
ORDER BY day DESC;
```

### MCP errors — recent failures with user and tool details
```sql
SELECT mal.created_at, u.name, mal.tool_name,
       mal.error_message, mal.duration_ms,
       mal.arguments_json
FROM mcp_activity_logs mal
JOIN users u ON u.id = mal.user_id
WHERE mal.result_status = 'error'
ORDER BY mal.created_at DESC
LIMIT 25;
```

### MCP usage by user per day (last 7 days)
```sql
SELECT DATE(mal.created_at) AS day, u.name,
       COUNT(*) AS calls,
       COUNT(*) FILTER (WHERE mal.result_status = 'error') AS errors,
       ROUND(AVG(mal.duration_ms)) AS avg_ms
FROM mcp_activity_logs mal
JOIN users u ON u.id = mal.user_id
WHERE mal.created_at >= NOW() - INTERVAL '7 days'
GROUP BY DATE(mal.created_at), u.name
ORDER BY day DESC, calls DESC;
```

### MCP API keys — active keys with usage stats
```sql
SELECT mak.name AS key_name, mak.key_prefix, u.name AS owner,
       mak.created_at, mak.last_used_at, mak.expires_at,
       COUNT(mal.id) AS total_calls,
       COUNT(*) FILTER (WHERE mal.result_status = 'error') AS errors
FROM mcp_api_keys mak
JOIN users u ON u.id = mak.user_id
LEFT JOIN mcp_activity_logs mal ON mal.mcp_api_key_id = mak.id
WHERE mak.revoked_at IS NULL
GROUP BY mak.id, mak.name, mak.key_prefix, u.name, mak.created_at, mak.last_used_at, mak.expires_at
ORDER BY mak.last_used_at DESC NULLS LAST;
```

### MCP slowest calls (p95+ latency, last 7 days)
```sql
SELECT mal.tool_name, u.name, mal.duration_ms,
       mal.result_status, mal.created_at,
       LEFT(mal.arguments_json::text, 200) AS args_preview
FROM mcp_activity_logs mal
JOIN users u ON u.id = mal.user_id
WHERE mal.created_at >= NOW() - INTERVAL '7 days'
  AND mal.duration_ms > (
    SELECT PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY duration_ms)
    FROM mcp_activity_logs
    WHERE created_at >= NOW() - INTERVAL '7 days'
  )
ORDER BY mal.duration_ms DESC
LIMIT 20;
```

## Stats (as of 2026-03-19)
- 1,156 accounts with completed campaigns
- Campaign types: claim_race, inform, invite, lottery, promotional, caller_99, bday_poll, pick_a_promo, trick_or_treat, gameday
- Campaign statuses: cancelled, completed, failed, scheduled, sending
- Users have phone and openphone_number fields (for Quo matching)

## Notes
- `primary_user_id` on accounts is often NULL — fall back to account_users with is_primary_account = true
- `launches.launched_at` is mostly NULL — use first completed campaign `sent_at` as the real "text launch" date
- All IDs are text (cuid-style), not integers
- Timestamps are `timestamp without time zone` (assumed UTC)
