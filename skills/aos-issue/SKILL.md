---
name: aos-issue
description: File an issue when a library skill, agent, command, hook, or plugin produces errors or wrong output — proactively offer when the user corrects or reports broken behavior in a library component.
argument-hint: [description]
---

# aos-issue

File GitHub issues to Example Company/aos when library components (skills, agents, prompts, hooks, plugins, MCP servers) aren't working as expected. Two trigger modes: agent-initiated (proactive) and user-initiated (explicit `/aos-issue`).

## Before Any Command

**Platform adaptation:** If the user's shell is PowerShell (not bash/zsh), adapt all cookbook commands: `mkdir -p` → `New-Item -ItemType Directory -Force`, `rm -rf` → `Remove-Item -Recurse -Force`, `cp -R` → `Copy-Item -Recurse`, `mktemp -d` → `Join-Path $env:TEMP "aos-$(Get-Random)"; New-Item -ItemType Directory -Force`, `test -e` → `Test-Path`, `command -v` → `Get-Command`, `ln -sfn` → `New-Item -ItemType Junction`, `grep` → `Select-String`, `2>/dev/null` → `2>$null`, heredocs → `@"..."@`. Omit `chmod +x`.

Check for aos updates (fast, non-blocking):

1. Run: `git -C ~/.claude/aos fetch origin main --quiet 2>/dev/null`
2. Compare local vs remote:
   ```bash
   LOCAL=$(git -C ~/.claude/aos rev-parse HEAD)
   REMOTE=$(git -C ~/.claude/aos rev-parse origin/main 2>/dev/null)
   ```
3. If LOCAL != REMOTE:
   - Run: `git -C ~/.claude/aos pull --ff-only --quiet`
   - If pull succeeds: tell the user "aos updated — restart session to use new version" and stop
   - After successful pull, check for stale symlinks:
     ```bash
     if [ -L ~/.claude/skills/library ] && [ ! -e ~/.claude/skills/library ]; then
       rm -f ~/.claude/skills/library ~/.claude/skills/workspace
       for skill in aos aos-issue aos-library; do
         rm -f ~/.claude/skills/$skill
         ln -sfn ~/.claude/aos/skills/$skill ~/.claude/skills/$skill
       done
     fi
     ```
   - If pull fails (local changes): tell the user "aos update available. Run: `git -C ~/.claude/aos pull`"
4. If fetch fails (no network): silently continue
5. Proceed to command routing

## Prerequisites

- **`gh` CLI** (blocking) — required for issue filing. Install: `brew install gh`
- **`gh auth`** — user must be authenticated. Run: `gh auth login`

Check both before any filing attempt:
```bash
command -v gh >/dev/null 2>&1 || { echo "gh CLI required: brew install gh"; exit 1; }
gh auth status 2>/dev/null || { echo "Run: gh auth login"; exit 1; }
```

## Trigger Modes

### Proactive (agent-initiated)

Offer to file an issue when you detect a **library component** failing. High bar — only trigger on:

- A library skill/agent/hook/plugin/MCP server errors out or produces clearly wrong output
- The user corrects a component's behavior ("no, that's not what hubspot should do", "slack sent to the wrong channel")
- The user says a component is broken, wrong, or not working ("library use isn't installing", "quo keeps timing out")

**Do NOT trigger on:**
- Your own mistakes using a skill (wrong arguments, misunderstanding the user's intent)
- General user frustration unrelated to a specific library component
- Minor friction or first-time setup issues
- Prerequisite problems (missing binaries, env vars) — these are user environment issues, not component bugs

**When triggering proactively:**
1. Identify which library component is suspected
2. Form a brief assessment of what went wrong
3. Ask the user: "I noticed [component] may not be working as expected — [observation]. Would you like me to file an issue to the aos repo?"
4. Only proceed if the user confirms

### Explicit (user-initiated)

The user runs `/aos-issue` or `/aos-issue [description]`. Proceed directly to the gather cookbook.

## Identifying Library Components

A component is a library component if it matches one of these:

1. **Catalog entry** — exists in `~/.claude/skills/aos-library/library.yaml` under any type list (`library.skills`, `library.agents`, `library.prompts`, `library.hooks`, `library.plugins`, `library.mcp_servers`)
2. **aos-internal skill** — one of: `aos`, `aos-library`, `aos-issue` (source: `https://github.com/Example Company/aos`)

For catalog entries, extract the `source` URL from library.yaml — this tells the triaging agent which repo to investigate.

For aos-internal skills, the source is the aos repo itself: `https://github.com/Example Company/aos`

If the problem is not attributable to a library-managed component, do not trigger proactively. For explicit `/aos-issue`, allow the user to describe any aos-related problem.

## Commands

| Command | Purpose |
| --- | --- |
| `/aos-issue` | File an issue — interactive context gathering |
| `/aos-issue [description]` | File with initial description context |

## Cookbook

| Command | Cookbook | Use When |
| --- | --- | --- |
| gather | [cookbook/gather.md](cookbook/gather.md) | Triggered proactively or explicitly — collect issue context |
| file | [cookbook/file.md](cookbook/file.md) | Context gathered and confirmed — execute the filing pipeline |

**When triggered (proactively or explicitly), read the gather cookbook first to collect context. Then read the file cookbook to execute the filing procedure.**
