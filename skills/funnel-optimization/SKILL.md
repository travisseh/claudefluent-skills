---
name: funnel-optimization
description: "Check ClaudeFluent conversion funnel data, diagnose drop-offs, and find optimization opportunities using PostHog analytics. Use this skill whenever the user mentions conversion rates, funnel analysis, drop-off points, PostHog data, signup flow performance, page analytics, event tracking, A/B test results, or asks questions like 'how is the site converting', 'where are we losing people', 'what does PostHog say', or 'check analytics'. Triggers on: funnel, conversion, PostHog, analytics, drop-off, signup rate, page performance, event tracking."
---

# Funnel Optimization - ClaudeFluent PostHog Analytics

Use this skill to check in on ClaudeFluent conversion funnel data, diagnose drop-offs, and find optimization opportunities using PostHog.

## PostHog Access

- **API Key**: stored in `claude_course/website/.env.local` as `POSTHOG_API_KEY`
- **Project ID**: `299795`
- **Host**: `https://app.posthog.com`
- **Auth header**: `Authorization: Bearer <POSTHOG_API_KEY>`

Read the API key from the env file before making requests:
```bash
API_KEY=$(grep POSTHOG_API_KEY claude_course/website/.env.local | cut -d= -f2)
```

## Custom Events Tracked

| Event | Page | What It Captures |
|-------|------|-----------------|
| `affiliate_ref_captured` | `/` | Visitor arrived via affiliate link. Props: `affiliate_ref` |
| `session_selected` | `/`, `/deal` | User picked a class time slot. Props: `session_id`, `session_label`, `page` |
| `checkout_initiated` | `/`, `/deal` | User clicked "Reserve Your Spot". Props: `session_id`, `price`, `affiliate_ref`, `page` |
| `checkout_completed` | `/success` | User returned from Stripe (purchased). Also calls `posthog.identify(email)` |
| `team_inquiry_submitted` | `/teams` | Team form submitted. Props: `company`, `team_size` |
| `waitlist_signup` | `/premium-resources` | Email captured for premium waitlist. Props: `email` |
| `setup_prompt_copied` | `/success` | Student copied an onboarding prompt. Props: `step_number`, `prompt_text` |

## Auto-Captured Events (PostHog defaults)

- `$pageview` - every page load, with `$pathname`, `$referrer`, `$device_type`, `$geoip_country_name`
- `$autocapture` - clicks on buttons/links, with `$el_text`, `tag_name`, `$pathname`
- `$pageleave` - when user navigates away
- `$rageclick` - frustrated clicking (UX friction indicator)
- `$web_vitals` - Core Web Vitals performance

## Key API Endpoints

### Get recent events
```bash
curl -s "https://app.posthog.com/api/projects/299795/events/?event=EVENT_NAME&limit=500&orderBy=%5B%22-timestamp%22%5D" \
  -H "Authorization: Bearer $API_KEY"
```

### Get event definitions
```bash
curl -s "https://app.posthog.com/api/projects/299795/event_definitions/" \
  -H "Authorization: Bearer $API_KEY"
```

### Get persons
```bash
curl -s "https://app.posthog.com/api/projects/299795/persons/?search=EMAIL" \
  -H "Authorization: Bearer $API_KEY"
```

## Analysis Playbooks

### 1. Conversion Funnel Check
Pull last N pageviews, group by `distinct_id`, trace journeys:
- Homepage (`/`) visitors
- Who selected a session (`session_selected`)
- Who initiated checkout (`checkout_initiated`)
- Who completed (`checkout_completed`)
- Calculate drop-off at each step

### 2. Traffic Source Analysis
From `$pageview` events, group by `$referrer`:
- `linkedin.com` / `lnkd.in` / `com.linkedin.android` = LinkedIn
- `google.com` = Google (check if brand search vs organic)
- `$direct` = Direct / bookmarks / links
- `checkout.stripe.com` = Returning from Stripe
- `t.co` = Twitter/X

Cross-reference with `checkout_completed` to get conversion rate per source.

### 3. Affiliate Performance
Query `affiliate_ref_captured` events grouped by `affiliate_ref`, then cross-reference with `checkout_initiated` and `checkout_completed` to get per-affiliate conversion rates.

### 4. Session Popularity
Query `session_selected` events grouped by `session_id` to see which time slots get the most interest vs. actual checkouts.

### 5. Onboarding Completion
Query `setup_prompt_copied` grouped by `step_number` to see how far students get in setup. Drop-off between steps indicates where they get stuck.

### 6. UX Friction Detection
Query `$rageclick` events grouped by `$pathname` to find pages with frustrated users.

## Site Architecture (for context)

**Conversion pages:**
- `/` - Homepage with hero, testimonials, session picker, checkout
- `/deal` - Special offer page (via `/d/[slug]`)
- `/success` - Post-purchase, redirects to onboarding
- `/onboarding/[token]` - Post-purchase environment setup

**Consideration pages:**
- `/free-resources` - Free guides and resources hub
- `/guides/[slug]` - SEO guide pages
- `/teams` - Team training inquiry form
- `/premium-resources` - Coming soon skills with waitlist

**PostHog config:**
- Initialized in `app/providers.tsx` with `person_profiles: "always"`
- Identifies users by email on `/success` page after Stripe redirect
- All pages wrapped in `PostHogProvider`

## Known Data Quirks

- Pre-March 2026 data had `person_profiles: "identified_only"` which broke cross-session identity. Post-purchase sessions were split from pre-purchase browsing. Fixed now.
- Google referrer traffic is mostly brand searches, not organic keyword discovery (as of March 2026).
- `$direct` referrer includes: actual direct visits, bookmarks, links from apps (Slack, iMessage), and any HTTPS→HTTPS referrer that browsers strip.
