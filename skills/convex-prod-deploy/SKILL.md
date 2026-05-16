---
name: convex-prod-deploy
description: "Use this skill when changes touch `claude_course/website/convex/` and the work will be committed or pushed. Before push, make sure production Convex is deployed with `npm run convex:deploy:prod`. The repo also has a pre-push hook for this, but this skill exists as a second guard and for manual deploys. Triggers on: convex changes, deploy convex, push convex code, commit convex updates."
---

# Convex Production Deploy

When work changes Convex source files in `claude_course/website/convex/`, production Convex must be deployed before or as part of push.

## Required command

From `claude_course/website` run:

```bash
npm run convex:deploy:prod
```

## Scope

Treat these as Convex source changes:

- `claude_course/website/convex/**`

Ignore generated-only changes under:

- `claude_course/website/convex/_generated/**`

## Repo behavior

This repo uses a `pre-push` hook to auto-run the production deploy when pushed commits include Convex source changes. If the deploy fails, the push should stop.

## Manual fallback

If the hook is missing or bypassed:

1. Run `npm run convex:deploy:prod`
2. Verify with `npm run convex:function-spec:prod`
3. Then push
