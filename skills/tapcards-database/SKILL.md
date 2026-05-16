---
name: tapcards-database
description: Query the TapCards production database (PostgreSQL on DigitalOcean) for analytics and reporting. Use when needing to access TapCards data including accounts, units, users, cards, interactions, conversions, reviews, and referrals.
---

# TapCards Database Access

Query the TapCards production database (PostgreSQL on DigitalOcean).

## Connection Details

Credentials stored in `.local/tapcards-db.env` (gitignored).

## Quick Query Command

```bash
source .local/tapcards-db.env && PGPASSWORD="$TAPCARDS_DB_PASSWORD" psql -h "$TAPCARDS_DB_HOST" -p "$TAPCARDS_DB_PORT" -U "$TAPCARDS_DB_USER" -d "$TAPCARDS_DB_NAME" --set=sslmode=require -c "YOUR_QUERY_HERE"
```

## Schema Overview

**17 tables in `public` schema:**

| Table | Purpose |
|-------|---------|
| `accounts` | Restaurant/business accounts |
| `units` | Individual locations/units within accounts |
| `users` | End users (customers) |
| `staffs` | Staff members |
| `unit_staff` | Staff-to-unit relationships |
| `cards` | Loyalty/tap cards |
| `cards_orders` | Card order tracking |
| `interactions` | User interactions/engagements |
| `touchpoints` | Customer touchpoints |
| `conversions` | Conversion events |
| `referrals` | Referral tracking |
| `reviews` | Customer reviews |
| `downloads` | App downloads |
| `winners` | Contest/game winners |
| `remember_me_tokens` | Auth tokens |
| `adonis_schema` | Migration tracking |
| `adonis_schema_versions` | Migration versions |

## Safety Guidelines

- **READ-ONLY queries only** - This is production data
- Avoid `SELECT *` on large tables without `LIMIT`
- Use `EXPLAIN` before running complex queries if concerned about performance
- Never run `UPDATE`, `DELETE`, `DROP`, or `TRUNCATE`

## Common Queries

### Count all users
```sql
SELECT COUNT(*) FROM users;
```

### Recent interactions (last 7 days)
```sql
SELECT * FROM interactions
WHERE created_at > NOW() - INTERVAL '7 days'
ORDER BY created_at DESC
LIMIT 100;
```

### Account overview
```sql
SELECT a.id, a.name, COUNT(u.id) as unit_count
FROM accounts a
LEFT JOIN units u ON u.account_id = a.id
GROUP BY a.id, a.name;
```
