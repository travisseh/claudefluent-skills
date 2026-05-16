---
name: gsc-submit
description: "Submit new guides/pages to Google Search Console for indexing. Use this skill after deploying new content to claudefluent.com, or whenever the user asks about indexing, GSC submission, sitemap status, or whether Google knows about new pages. Also trigger when they say 'submit to Google', 'are these indexed', 'submit sitemap', 'check indexing status', or just deployed new guides and need to notify Google. Triggers on: GSC, Google Search Console, submit to Google, index new guides, submit sitemap, check indexing, are these indexed, deploy and submit, sitemap status."
---

# GSC Submit Skill

Submit ClaudeFluent URLs to Google Search Console after deploying new content.

## When to Use

Run this after:
- Deploying new guides or articles
- Updating existing content significantly
- Adding new pages to the site

## Script Location

```
scripts/gsc/submit-urls.ts
```

Run from the `claude_course/website` directory.

## Commands

### Submit/refresh the sitemap (do this after every deploy with new pages)

```bash
npx tsx scripts/gsc/submit-urls.ts --sitemap
```

### List current sitemaps

```bash
npx tsx scripts/gsc/submit-urls.ts --list
```

### Inspect all guide URLs (check indexing status)

```bash
npx tsx scripts/gsc/submit-urls.ts --guides
```

### Inspect a single URL

```bash
npx tsx scripts/gsc/submit-urls.ts --url=https://claudefluent.com/guides/some-slug
```

## Standard Post-Deploy Workflow

After deploying new guides, run these in order:

1. **Submit sitemap** to notify Google of new URLs:
   ```bash
   npx tsx scripts/gsc/submit-urls.ts --sitemap
   ```

2. **Inspect new guide URLs** to verify they're discoverable:
   ```bash
   npx tsx scripts/gsc/submit-urls.ts --guides
   ```

3. Check the summary output. New pages typically show "URL is not on Google" initially, which is expected. Google processes sitemap submissions within hours to days.

## How It Works

- Reads guide slugs from `lib/seo-config.ts` (GUIDE_SLUGS array) so it stays in sync automatically
- Uses Google Search Console API with service account auth
- Credentials: reads `credentials.json` in `scripts/gsc/` or falls back to `GOOGLE_SERVICE_ACCOUNT_JSON` in `.env.local`
- Rate limited to 1 request/second for URL inspection

## Credentials Setup

The service account needs "Full" access in GSC:
1. Go to https://search.google.com/search-console
2. Settings > Users and permissions > Add user
3. Add the service account email with "Full" access

## Important Notes

- Sitemap submission is the primary indexing mechanism. URL inspection just checks status.
- There's no penalty for resubmitting sitemaps. Do it freely after deploys.
- New URLs typically take hours to days to get indexed after sitemap submission.
- The script reads GUIDE_SLUGS dynamically, so new guides added to seo-config.ts are automatically included.
