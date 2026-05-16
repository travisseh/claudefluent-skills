---
name: user-linkedin-style
description: "Compatibility wrapper for LinkedIn writing requests on the user's behalf. Keep triggering on LinkedIn posts, threads, comments, or similar prompts, but use $user-writing-style as the source of truth for voice, hooks, structure, tone, and formatting. Triggers on: LinkedIn post, LinkedIn content, draft for LinkedIn, write on LinkedIn, LinkedIn thread, LinkedIn comment, share on LinkedIn, post about."
---

# the user LinkedIn Style

This skill is now a compatibility wrapper.

Use `$user-writing-style` as the only source of truth for the user's writing voice.

## Workflow

1. Read `$user-writing-style`.
2. Apply the `### LINKEDIN` section for hooks, post formats, engagement patterns, and formatting.
3. Apply the `### LONG-FORM ARTICLES / BLOG POSTS` section when the deliverable is longer than a normal LinkedIn post.
4. Always apply the ExampleCo safety check before suggesting or drafting public-facing content.

## Important

- If an older prompt or skill calls for `$user-linkedin-style`, treat it as an alias for `$user-writing-style`.
- Do not maintain separate LinkedIn voice rules here.
- If LinkedIn guidance needs to change, update `$user-writing-style` instead of this file.
