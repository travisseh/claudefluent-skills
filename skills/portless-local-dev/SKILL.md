---
name: portless-local-dev
description: Use when starting, stopping, restarting, debugging, or explaining the user's common local dev servers through portless/local .localhost URLs.
---

# Portless Local Dev

Use portless for the user's common local web apps unless the user asks for a raw framework port.

## Commands

```bash
portless list
portless proxy stop
portless clean
PORTLESS=0 npm run dev
```

- `portless list`: show active named local routes.
- `portless proxy stop`: stop the shared local proxy.
- `portless clean`: remove portless state, trust entry, and hosts entries. Use only when resetting.
- `PORTLESS=0 npm run dev`: bypass portless and run the repo's raw dev script behavior.

## Common Apps

- product app: `/Users/you/Programming/example-company` -> `https://example-company.localhost`
- Example Company website: `/Users/you/Programming/example-company-website-v2` -> `https://example-company-website.localhost`
- Product2 risk dashboard: `/Users/you/Programming/product2/public/apps/example-company-risk-dashboard` -> `https://example-company-risk-dashboard.localhost`
- Product Analytics: `/Users/you/Programming/product2/public/apps/tapcards-dashboard` -> `https://product-analytics.localhost`
- Product2 Figma plugin: `/Users/you/Programming/product2/shared/apps/brand-extractor-figma` -> `https://example-company-figma-plugin.localhost`
- Product2 Figma plugin v2: `/Users/you/Programming/product2/shared/apps/brand-extractor-figma-codex-v2` -> `https://example-company-figma-plugin-v2.localhost`
- ClaudeFluent website: `/Users/you/Programming/personal-master/personal/claude_course/website` -> `https://claudefluent.localhost`

## Default Workflow

1. `cd` to the app directory.
2. Run `npm run dev` for web apps or `npm run serve` for the Figma plugin service.
3. Use the named `https://*.localhost` URL instead of a numeric port.
4. If startup behaves strangely, run `portless list`, inspect logs, then try the raw fallback with `PORTLESS=0 npm run dev`.
