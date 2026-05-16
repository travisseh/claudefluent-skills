---
name: chrome-cdp
description: Deprecated browser skill. Do not use this for normal automation. If older instructions mention chrome-cdp, translate the task to `chrome-live-session-preferences` and its AppleScript helper, not CDP.
---

# Chrome CDP

This skill is deprecated and should not be chosen for normal Codex work.

Going forward, use `$chrome-live-session-preferences` for the user's real Chrome session:

```bash
~/.codex/skills/chrome-live-session-preferences/scripts/chrome-live.sh active-tab
~/.codex/skills/chrome-live-session-preferences/scripts/chrome-live.sh exec-js <<'EOF'
(() => document.body.innerText.slice(0, 2000))();
EOF
```

## Policy

- Do not choose `chrome-cdp` as the primary browser workflow.
- If an older skill or note says to use `chrome-cdp`, translate that request into `chrome-live-session-preferences`.
- Only use the legacy `scripts/cdp.mjs` helper if the user explicitly asks for CDP or if you are debugging browser tooling itself.

## Legacy Helper

```bash
scripts/cdp.mjs list
```

Keep this around only as a last-resort fallback or for debugging old workflows.
