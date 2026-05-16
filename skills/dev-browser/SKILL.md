---
name: dev-browser
description: Browser automation for headless or isolated browser work. Use when users ask to navigate websites, fill forms, take screenshots, extract web data, test web apps, or automate browser workflows and a clean browser is fine. For the user's already-open Chrome session, prefer `chrome-live-session-preferences` and its AppleScript helper instead of CDP attach.
---

# Dev Browser

Use this for headless browsing or isolated profile-scoped Chrome sessions, not for the user's main live Chrome window.

`dev-browser` runs sandboxed JavaScript against a persistent browser session and exposes full Playwright `Page` objects.

## Default Modes

- Do not use `dev-browser --connect` as the default path for the user's main live Chrome session. Use `~/.codex/skills/chrome-live-session-preferences/scripts/chrome-live.sh` instead.
- Use `dev-browser --headless` when a clean browser is fine.
- Reuse named pages with `browser.getPage("name")` so state persists across runs.
- If you need an isolated authenticated browser without touching the user's main Chrome window, launch a profile-scoped debug Chrome with `scripts/launch-profile-debug-chrome.sh` and connect `dev-browser` to that port.
- For unattended backlog, cron, or background agent runs, prefer the profile-scoped debug Chrome path over the live Chrome session. It is the safer default for "work in the background without taking over my screen."

## Profile Mode

Use the helper script when the user wants a specific Chrome profile or when headless or isolated browser control is preferable to the user's main Chrome session.

Supported profile names:

- `personal` -> `Profile 1` (`the user`)
- `exampleco` -> `Profile 10` (`ExampleCo.com`)
- `gmr` -> `Profile 15` (`ReviewCo`)
- `example-agency` -> `Profile 3` (`example.com`)

List the supported profiles:

```bash
~/.codex/skills/dev-browser/scripts/launch-profile-debug-chrome.sh --list
```

Launch a profile-scoped debug Chrome and open a starting URL:

```bash
~/.codex/skills/dev-browser/scripts/launch-profile-debug-chrome.sh personal https://x.com/i/bookmarks
```

The script prints JSON with `port`, `endpoint`, `tmp_dir`, `profile`, and `reused_existing`. Feed that `endpoint` or `port` into `dev-browser --connect`.

Clean up the isolated Chrome when you are done with it:

```bash
~/.codex/skills/dev-browser/scripts/launch-profile-debug-chrome.sh --cleanup personal
```

If a wrapper or automation launched multiple helper Chromes for a single run, it can clean up only the ones it owns:

```bash
LIFE_BACKLOG_BROWSER_OWNER=run-123 ~/.codex/skills/dev-browser/scripts/launch-profile-debug-chrome.sh personal https://example.com
~/.codex/skills/dev-browser/scripts/launch-profile-debug-chrome.sh --cleanup-owner run-123
```

Clean up all isolated helper Chromes and old orphaned temp profiles:

```bash
~/.codex/skills/dev-browser/scripts/launch-profile-debug-chrome.sh --cleanup-all
```

Use this mode when:

- `dev-browser --connect` against the main Chrome session hangs or times out
- the user wants a specific persona/account such as `Personal`, `ExampleCo`, `ReviewCo`, or `Example Agency`
- the task needs authenticated browsing but not the user's entire overloaded browser graph
- the task is being run unattended and should not steal focus from the user's main workspace

Implementation note:

- The helper does a minimal profile clone of `Local State`, `Cookies`, `Preferences`, and `Secure Preferences` into a temp user-data-dir. This is much faster than cloning the full Chrome profile and was enough to preserve X login in testing.

## Core Pattern

```bash
dev-browser --connect <<'EOF'
const page = await browser.getPage("main");
await page.goto("https://example.com");
console.log(await page.title());
EOF
```

## Common Operations

```bash
# List tabs in the connected browser
dev-browser --connect <<'EOF'
console.log(JSON.stringify(await browser.listPages(), null, 2));
EOF

# Save a screenshot
dev-browser --connect <<'EOF'
const page = await browser.getPage("main");
await page.goto("https://example.com");
const path = await saveScreenshot(await page.screenshot({ fullPage: true }), "example.png");
console.log(path);
EOF

# Use a specific named Chrome profile when live Chrome is too heavy
INFO=$(~/.codex/skills/dev-browser/scripts/launch-profile-debug-chrome.sh personal https://x.com/i/bookmarks)
PORT=$(printf '%s\n' "$INFO" | jq -r '.port')
tmp=$(mktemp /tmp/dev-browser-profile.XXXXXX)
cat > "$tmp" <<'EOF'
const page = await browser.getPage("x-bookmarks");
await page.goto("https://x.com/i/bookmarks", { waitUntil: "domcontentloaded" });
console.log(JSON.stringify({ url: page.url(), title: await page.title() }, null, 2));
EOF
dev-browser --connect "http://127.0.0.1:$PORT" run "$tmp"
```

## Guidance

- Prefer `locator()`-based interactions over coordinate clicks.
- Use named pages like `browser.getPage("linkedin")`, `browser.getPage("grain")`, or `browser.getPage("x-bookmarks")` for persistent workflows.
- When you need a structured AI-friendly page dump, use `page.snapshotForAI(...)`.
- When you need the exact API surface or flags, run `dev-browser --help`.
- If the user wants the already-open Chrome profile or existing tabs, do not attach to live Chrome. Use the AppleScript helper from `chrome-live-session-preferences`.
- If a user asks to choose between `Personal`, `ExampleCo`, `ReviewCo`, or `Example Agency`, prefer the profile helper over the main live Chrome session.
- If the helper is used repeatedly in a turn, reuse the same returned `port` rather than launching a fresh Chrome each time.
- Do not relaunch helper Chrome for every step. Launch once, keep the returned `port`, and reuse the same connected browser/page through the whole workflow.
- If you launched a helper Chrome for a bounded task, clean it up when the task ends. Prefer `--cleanup <profile>` over leaving temp-profile Chromes running.

## Installation

```bash
npm install -g dev-browser
dev-browser install
```

## Usage

Run `dev-browser --help` to learn more.
