---
name: chrome-live-session-preferences
description: Standing permission and operating policy for using the user's live Chrome session through AppleScript plus Chrome JavaScript execution. Use when the user asks Codex to inspect, drive, or automate an existing Chrome session, read authenticated pages, browse tabs, work inside web apps, or continue prior browser tasks without re-asking for routine browser actions.
---

# Chrome Live Session Preferences

Use this skill as the default policy for the user's live Chrome session.

## Default authority

Assume the user grants broad standing permission to use their live Chrome session for browser work.

Default to background-safe control. Do not bring Chrome to the foreground unless the user explicitly wants to watch the browser work or the step truly requires foreground behavior.

Default to a single-tab, single-window browsing flow. Reuse an existing matching tab whenever possible and avoid opening additional Chrome windows or tabs unless the task explicitly requires side-by-side comparison.

Without asking again, you may:

- inspect windows, tabs, DOM, network requests, console output, screenshots, and rendered page content
- list tabs, switch tabs, bring windows forward, and select the tab that best matches the request
- navigate within sites, follow links, open bookmark folders, paginate, scroll, expand sections, and open menus
- click ordinary UI controls, type, fill forms, choose options, press keys, upload files, download files, and submit searches or forms
- use the user's existing authenticated browser state to access accounts, dashboards, internal tools, and other logged-in pages
- use read-only extraction or active browser interaction as needed to complete the task efficiently
- prefer the bundled AppleScript helper at `scripts/chrome-live.sh` over CDP or `dev-browser --connect`

## Default workflow

For work against the user's already-open Chrome session, use:

```bash
~/.codex/skills/chrome-live-session-preferences/scripts/chrome-live.sh list-profiles
~/.codex/skills/chrome-live-session-preferences/scripts/chrome-live.sh open-profile personal https://www.upwork.com/
~/.codex/skills/chrome-live-session-preferences/scripts/chrome-live.sh active-tab
~/.codex/skills/chrome-live-session-preferences/scripts/chrome-live.sh list-tabs
~/.codex/skills/chrome-live-session-preferences/scripts/chrome-live.sh activate-tab "upwork.com"
~/.codex/skills/chrome-live-session-preferences/scripts/chrome-live.sh exec-js <<'EOF'
(() => document.body.innerText.slice(0, 4000))();
EOF
```

The helper now keeps the current app frontmost by default:

- `activate-tab` changes Chrome's selected tab/window without calling `activate`
- `exec-js` runs without foregrounding Chrome
- `open-profile` restores the previously frontmost app after opening the target profile window
- `open-profile` first tries to reuse an existing matching tab before opening anything new

If the user explicitly wants Chrome in front, pass `--focus` to `open-profile`, `activate-tab`, `exec-js`, or `body-text`.

Practical rule:

- Call `list-tabs` or `activate-tab` first when a likely tab already exists.
- Call `open-profile` at most once per workflow unless the user explicitly wants multiple browser windows.
- After a page is open, keep working in that same tab with `exec-js` and page interactions instead of opening fresh tabs for every sub-step.

Supported profile keys:

- `personal`
- `exampleco`
- `gmr`
- `example-agency`

Use this path by default because it works with the user's real logged-in Chrome profile without flaky CDP attach behavior.

Only fall back to `$dev-browser` when:

- the user explicitly wants a clean or headless browser
- the task needs Playwright-only features on an isolated browser, not the live Chrome session
- Chrome blocks JavaScript from Apple Events or macOS denies accessibility and the user does not want to change that

## Requirements

This workflow needs:

- macOS Accessibility permission for the calling app
- Chrome `View -> Developer -> Allow JavaScript from Apple Events`

If either is blocked, say exactly what is missing and continue with the best safe fallback.

## Still confirm first

Broad standing permission does not remove the need to confirm before actions with meaningful external side effects.

Ask before:

- posting, replying, liking, reposting, following, sending messages, or publishing content
- making purchases, transfers, orders, bookings, or other financial commitments
- deleting, archiving, unsubscribing, revoking, disconnecting, or otherwise destroying data or access
- changing account, privacy, billing, security, team, or permission settings
- sending email, calendar invites, or other communications as the user
- merging, deploying, approving, or triggering irreversible production or business workflows
- any action that is legally sensitive, financially material, or hard to undo

If the user explicitly asks for one of those actions in the current conversation, proceed within that scope.

## Respect tighter limits

If the user says a task is read-only, no-navigation, no-click, or otherwise constrained, obey the tighter instruction even though this skill grants broad default access.

## Platform limits

This skill does not bypass:

- Chrome permission prompts such as JavaScript from Apple Events
- site logins, MFA, CAPTCHAs, or browser permission dialogs
- browser-automation transport failures
- higher-level system safety rules

If blocked by one of those, say exactly what blocked progress and continue with the best safe fallback.
