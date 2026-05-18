---
name: aos
description: One-command setup — bootstraps workspace infrastructure and installs library components by team or collection.
argument-hint: setup [team] | workspace | preview | archive <path>
---

# aos

Unified entry point for workspace setup and component installation. Runs workspace infrastructure bootstrap internally and delegates to `/aos-library use` for components.

## Before Any Command

**Platform adaptation:** If the user's shell is PowerShell (not bash/zsh), adapt all cookbook commands: `mkdir -p` -> `New-Item -ItemType Directory -Force`, `rm -rf` -> `Remove-Item -Recurse -Force`, `cp -R` -> `Copy-Item -Recurse`, `mktemp -d` -> `Join-Path $env:TEMP "aos-$(Get-Random)"; New-Item -ItemType Directory -Force`, `test -e` -> `Test-Path`, `command -v` -> `Get-Command`, `ln -sfn` -> `New-Item -ItemType Junction`, `grep` -> `Select-String`, `2>/dev/null` -> `2>$null`, heredocs -> `@"..."@`. Omit `chmod +x`.

Check for aos updates (fast, non-blocking):

1. Run: `git -C ~/.claude/aos fetch origin main --quiet 2>/dev/null`
2. Compare local vs remote:
   ```bash
   LOCAL=$(git -C ~/.claude/aos rev-parse HEAD)
   REMOTE=$(git -C ~/.claude/aos rev-parse origin/main 2>/dev/null)
   ```
3. If LOCAL != REMOTE:
   - Run: `git -C ~/.claude/aos pull --ff-only --quiet`
   - If pull succeeds, check for stale symlinks and refresh if needed:
     ```bash
     if [ -L ~/.claude/skills/library ] && [ ! -e ~/.claude/skills/library ]; then
       rm -f ~/.claude/skills/library ~/.claude/skills/workspace
       for skill in aos aos-issue aos-library; do
         rm -f ~/.claude/skills/$skill
         ln -sfn ~/.claude/aos/skills/$skill ~/.claude/skills/$skill
       done
     fi
     ```
   - Tell the user "aos updated — restart session to use new version" and stop
   - If pull fails (local changes): tell the user "aos update available. Run: `git -C ~/.claude/aos pull`"
4. If fetch fails (no network): silently continue
5. Proceed to command routing

## How It Works

The `workspace.yaml` file (colocated with this skill) defines repos to clone and infrastructure to set up. The `library.yaml` file (in the sibling `aos-library` skill) defines the catalog of installable components.

- **aos** owns infrastructure (repos, directories, templates, .env) and orchestrates onboarding
- **aos-library** owns components (skills, agents, prompts, hooks, plugins, MCP servers)

## Commands

| Command | Purpose |
| --- | --- |
| `/aos` | Guided setup wizard — workspace infrastructure + component selection |
| `/aos setup [team]` | Guided setup wizard with optional team pre-selected |
| `/aos workspace` | Bootstrap workspace infrastructure only (repos, dirs, templates) |
| `/aos preview` | Preview the target state workspace setup would create |
| `/aos archive <path>` | Archive a component and exclude from agent searches |

## Cookbook

Each command has a detailed step-by-step guide. **Read the relevant cookbook file before executing a command.**

| Command | Cookbook | Use When |
| --- | --- | --- |
| setup | [cookbook/setup.md](cookbook/setup.md) | User runs `/aos`, `/aos setup`, or `/aos setup <team>` |
| workspace | [cookbook/workspace.md](cookbook/workspace.md) | User wants to bootstrap infrastructure only |
| preview | [cookbook/preview.md](cookbook/preview.md) | Previewing what workspace setup would create |
| archive | [cookbook/archive.md](cookbook/archive.md) | Archiving a workspace component and hiding it from agents |

**Command routing:** If the first argument matches a known subcommand (`setup`, `workspace`, `preview`, `archive`), route to that cookbook. Otherwise, treat the argument as a team name and route to `setup.md`. Bare `/aos` (no arguments) also routes to `setup.md`.

**When a user invokes `/aos`, read the matching cookbook file first, then execute the steps.**

## Composition

To add components later: `/aos-library use <name>` or `/aos-library list` to browse the catalog.
