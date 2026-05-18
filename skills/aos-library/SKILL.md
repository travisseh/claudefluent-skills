---
name: aos-library
description: Private distribution of agentic components — use, add, push, remove, sync, list, audit, or search skills/agents/prompts/hooks/plugins/MCP servers from the library catalog.
argument-hint: use|add|push|remove|list|sync|audit|search [name]
---

# The Library

A meta-skill for private-first distribution of agentic components (skills, agents, prompts, hooks, plugins, and MCP servers) across agents, devices, and teams.

## How It Works

The Library is a catalog of references to your agentic components. The `library.yaml` file (colocated with this skill) points to where skills, agents, prompts, and hooks live on GitHub, and defines plugins and MCP servers to install. Nothing is fetched until you ask for it.

**The `library.yaml` is a catalog, not a manifest.** Entries define what's *available* — not what gets installed. You pull specific items on demand with `/aos-library use <name>`.

**Git-based updates:** aos self-checks for updates on every invocation via `git fetch`. The `library.yaml` is always current. Catalog mutations (add/remove) use a temp-clone pattern: clone the aos repo → modify → push → cleanup. Changes are pulled on next invocation.

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

## Commands

| Command | Purpose |
| --- | --- |
| `/aos-library use <name>` | Pull from source (install or refresh) |
| `/aos-library add <details>` | Register a new entry in the catalog |
| `/aos-library push <name>` | Push local changes back to source |
| `/aos-library remove <name>` | Remove from catalog and optionally local |
| `/aos-library list` | Show full catalog with install status |
| `/aos-library sync` | Re-pull all installed items from source |
| `/aos-library audit [name]` | Scan source code for undeclared dependencies |
| `/aos-library search <keyword>` | Find entries by keyword |

## Cookbook

Each command has a detailed step-by-step guide. **Read the relevant cookbook file before executing a command.**

| Command | Cookbook | Use When |
| --- | --- | --- |
| use | [cookbook/use.md](cookbook/use.md) | User wants to pull or refresh an item, install a collection, or set up a team |
| add | [cookbook/add.md](cookbook/add.md) | User wants to register a new entry in catalog |
| push | [cookbook/push.md](cookbook/push.md) | User improved a skill locally and wants to update the source |
| remove | [cookbook/remove.md](cookbook/remove.md) | User wants to remove an entry from the catalog |
| list | [cookbook/list.md](cookbook/list.md) | User wants to see what's available and what's installed |
| sync | [cookbook/sync.md](cookbook/sync.md) | User wants to refresh all installed items at once |
| audit | [cookbook/audit.md](cookbook/audit.md) | User wants to check source code for missing dependency declarations |
| search | [cookbook/search.md](cookbook/search.md) | User is looking for an item but doesn't know the exact name |

**When a user invokes a `/aos-library` command, read the matching cookbook file first, then execute the steps.**

## Entry Types

The library supports 6 entry types, each with its own install mechanism:

| Type | Source | Install mechanism |
|------|--------|-------------------|
| Skills | GitHub URL → directory | Copy parent directory to `.claude/skills/<name>/` |
| Agents | GitHub URL → file | Copy file to `.claude/agents/<name>.md` |
| Prompts | GitHub URL → file | Copy file to `.claude/commands/<name>.md` |
| Hooks | GitHub URL → script | Copy to `.claude/hooks/<name>.sh` + register in settings.json |
| Plugins | Plugin identifier (name@marketplace) | `claude plugin install` + `claude plugin enable` |
| MCP Servers | Inline config (type, url/command) | Upsert into `.mcp.json` (read-merge-write) |

**Plugins and MCP servers** differ from the other four types: they have no GitHub source URL, no target directory, and cannot be pushed or synced. They are installed via CLI commands or config file writes.

## Source Format

For skills, agents, prompts, and hooks, the `source` field supports these GitHub URL formats (auto-detected):

- `https://github.com/org/repo/blob/main/path/to/SKILL.md` — GitHub browser URL
- `https://raw.githubusercontent.com/org/repo/main/path/to/SKILL.md` — GitHub raw URL

Parse org, repo, branch, and file path from the URL structure. For private repos, use SSH or `GITHUB_TOKEN` for auth automatically.

**Important:** The source points to a specific file (SKILL.md, AGENT.md, prompt file, or hook script). For skills, we pull the entire parent directory. For agents, prompts, and hooks, we pull just the file.

For reading a single file (e.g., checking metadata), prefer `gh api` over cloning.

**For plugins**, the `source` field is a plugin identifier: `name@marketplace` (e.g., `plugin-dev@claude-plugins-official`). Optional `marketplace` field for custom marketplace registration.

**For MCP servers**, there is no `source` field. Configuration is inline: `type` (http/stdio), `url` (for http), or `command`/`args`/`env` (for stdio).

## Typed Dependencies

The `requires` field uses typed references to avoid ambiguity:

**Prerequisites** (host environment checks):
- `bin:name` — system binary must exist (`command -v name`). **Blocking** — missing binaries stop installation.
- `env:VAR` — environment variable must be set. **Warning** — reports missing vars with guidance, proceeds with install.

**Catalog dependencies** (auto-installed from the library):
- `skill:name` — references a skill in the library catalog
- `agent:name` — references an agent in the library catalog
- `prompt:name` — references a prompt in the library catalog
- `hook:name` — references a hook in the library catalog
- `plugin:name` — references a plugin in the library catalog
- `mcp:name` — references an MCP server in the library catalog

**Resolution order:** `bin:` checks first (blocking), then `env:` checks (warning), then all catalog deps (recursive install). See [cookbook/preflight.md](cookbook/preflight.md) for the prerequisite procedure.

When resolving catalog dependencies: look up each reference in `library.yaml`, install all dependencies first (recursively), then install the requested item. Skip `bin:` and `env:` entries during catalog resolution — they are handled by the preflight step.

## Collections

Collections let you install a group of related entries with a single command. They live in a top-level `collections` section in `library.yaml`.

### Schema

```yaml
collections:
  <collection-name>: [item-a, item-b, plugin-c, mcp-server-d]
```

Collections are flat lists of item names — can reference any entry type (skills, agents, prompts, hooks, plugins, MCP servers). Names must be unique across all types. No nesting — composition happens via teams.

### Resolution Order

When `/aos-library use <name>` is invoked:
1. Look up `<name>` as an entry across all type lists first
2. If no entry match, check if `<name>` is a collection key
3. If no collection match, check if `<name>` is a team key
4. If it's a collection, resolve all items and install them
5. If it's a team, resolve to its collections list, then install each collection

## Teams

Teams compose collections for team-specific use cases. They live in a top-level `teams` section in `library.yaml`.

### Schema

```yaml
teams:
  <team-name>:
    collections: [collection-a, collection-b]
```

When `/aos-library use <team>` is invoked, resolve the team to its collections list and install each collection in order.

## Target Directories

Items are installed to paths defined in `library.yaml` under `default_dirs`:

| Type | Default | Global |
|------|---------|--------|
| Skills | `.claude/skills/` | `~/.claude/skills/` |
| Agents | `.claude/agents/` | `~/.claude/agents/` |
| Prompts | `.claude/commands/` | `~/.claude/commands/` |
| Hooks | `.claude/hooks/` | *(project-local only)* |
| Plugins | *(n/a — installed via CLI)* | |
| MCP Servers | *(n/a — configured in `.mcp.json`)* | |

If the user says "global", use the global path. If they specify a custom path, use it. Otherwise, use the default path.

## Hooks

Hooks are shell scripts that Claude Code runs in response to events (PreToolUse, PostToolUse, Stop, etc.). Unlike skills/agents/prompts which are pure file copies, hooks require **two actions** on install:

1. **Copy the script** to `.claude/hooks/<name>.sh` and make it executable
2. **Register in settings.json** — upsert an entry under `hooks.<event>` so Claude Code knows to run it

### Hook Catalog Entries

Hook entries in `library.yaml` have two extra fields beyond the standard `name`, `description`, `source`:

```yaml
library:
  hooks:
    - name: enforce-output-convention
      description: Blocks writes outside the configured output path
      source: https://github.com/org/repo/blob/main/hooks/enforce-output-convention.sh
      event: PreToolUse
      matcher: "Write|Edit"
```

- **`event`** (required) — the hook event: `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PreCompact`, `Notification`
- **`matcher`** (optional) — tool or command pattern to match (e.g., `"Write|Edit"`, `"Bash"`). If omitted, the hook runs for all invocations of that event.

### Settings.json Registration

When installing a hook, upsert into `.claude/settings.json` (or `settings.local.json`):

```json
{
  "hooks": {
    "<event>": [
      {
        "matcher": "<matcher>",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/<name>.sh"
          }
        ]
      }
    ]
  }
}
```

See the use cookbook (Step 5.5) for the full read-merge-write registration flow and the remove cookbook for deregistration.

## Plugins

Plugin entries define Claude Code plugins to install and enable.

### Plugin Catalog Entries

```yaml
library:
  plugins:
    - name: plugin-dev
      description: Plugin development tools
      source: plugin-dev@claude-plugins-official
    - name: superpowers
      description: Obra superpowers plugin
      source: superpowers@obra
      marketplace: obra/superpowers
```

- **`source`** (required) — plugin identifier: `name@marketplace`
- **`marketplace`** (optional) — GitHub repo for marketplace registration (e.g., `obra/superpowers`). If present and the marketplace isn't registered, add it before installing.

### Plugin Install Logic

1. Run `claude plugin list --json`, check if any entry's `id` starts with `<name>@` and has `"enabled": true`
2. If enabled → skip
3. If exists but disabled → `claude plugin enable <source>`
4. If not installed: register marketplace if needed, then `claude plugin install <source>` + `claude plugin enable <source>`

Plugins cannot be pushed or synced — they are managed by their own marketplace update mechanism.

## MCP Servers

MCP server entries define Model Context Protocol servers to configure in `.mcp.json`.

### MCP Server Catalog Entries

```yaml
library:
  mcp_servers:
    - name: linear
      description: Linear issue tracking
      type: http
      url: https://mcp.linear.app/mcp
    - name: custom-tool
      description: Custom stdio MCP server
      type: stdio
      command: npx
      args: ["-y", "custom-mcp-server"]
      env:
        API_KEY: "${API_KEY}"
```

- **`type`** (required) — `http` or `stdio`
- For `http`: **`url`** (required)
- For `stdio`: **`command`** (required), **`args`** (optional), **`env`** (optional)

### MCP Server Install Logic

1. Read `.mcp.json` in the project root (if missing, start from `{"mcpServers": {}}`)
2. If `mcpServers.<name>` exists with identical config → skip
3. If exists with different config → ask user before overwriting
4. If not present → add entry, write back (read-merge-write — preserve all existing entries)

MCP servers cannot be pushed or synced — they are local configuration, not source files.
