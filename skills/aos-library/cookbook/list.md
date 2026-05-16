# List Available Items

## Context
Show the full library catalog with install status.

## Steps

### 1. Read the Catalog
- Read `library.yaml` (colocated with this skill)
- Parse all entries from `library.skills`, `library.agents`, `library.prompts`, `library.hooks`, `library.plugins`, and `library.mcp_servers`

### 2. Check Install Status

**Important:** The Glob tool matches files, not directories. Always check for a known file inside the expected path — never glob for a directory with a trailing slash.

For each entry, determine the type and use the corresponding detection pattern:

| Type | Detection pattern (default) | Detection pattern (global) |
|------|----------------------------|---------------------------|
| Skills | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/SKILL.md` |
| Agents | `.claude/agents/<name>.md` | `~/.claude/agents/<name>.md` |
| Prompts | `.claude/commands/<name>.md` | `~/.claude/commands/<name>.md` |
| Hooks | `.claude/hooks/<name>.sh` | *(n/a)* |
| Plugins | `claude plugin list --json` | *(n/a)* |
| MCP Servers | `.mcp.json` | *(n/a)* |

For each entry:
- **Skills, agents, prompts**: Check default and global directories for the detection pattern file. Mark as `installed (default)`, `installed (global)`, or `not installed`.
- **Hooks**: Check if file exists and is registered in `.claude/settings.json`. Mark as `installed + registered`, `installed (not registered)`, or `not installed`.
- **Plugins**: Run `claude plugin list --json` once (cache for all plugins). Check if any entry's `id` starts with `<name>@` and has `"enabled": true`. Mark as `enabled`, `disabled`, or `not installed`.
- **MCP Servers**: Read `.mcp.json` once (cache). Check if `mcpServers.<name>` exists. Mark as `configured` or `not configured`.

### 3. Display Results

Format the output as tables grouped by type:

```
## Skills
| Name | Description | Source | Status |
|------|-------------|--------|--------|
| skill-name | skill-description | github.com/... | installed (default) |

## Agents
| Name | Description | Source | Status |
|------|-------------|--------|--------|
| agent-name | agent-description | github.com/... | installed (global) |

## Prompts
| Name | Description | Source | Status |
|------|-------------|--------|--------|
| prompt-name | prompt-description | github.com/... | not installed |

## Hooks
| Name | Description | Event | Matcher | Status |
|------|-------------|-------|---------|--------|
| hook-name | hook-description | PreToolUse | Write|Edit | installed + registered |

## Plugins
| Name | Description | Source | Status |
|------|-------------|--------|--------|
| plugin-dev | Plugin development tools | plugin-dev@claude-plugins-official | enabled |

## MCP Servers
| Name | Description | Type | Status |
|------|-------------|------|--------|
| linear | Linear issue tracking | http | configured |
```

If a section is empty, show: `No <type> in catalog.`

### 3.5. Display Collections
If `collections` exists in `library.yaml` and is non-empty, display a Collections table:

```
## Collections

| Collection | Items |
|------------|-------|
| workflow | interview-me, research, critical-thinking, systems-thinking |
| quality-of-life | stop-notify, permission-notify, enforce-output-convention |
```

### 3.6. Display Teams
If `teams` exists in `library.yaml` and is non-empty, display a Teams table:

```
## Teams

| Team | Collections |
|------|-------------|
| go-to-market | workflow, quality-of-life, connectors |
```

If no teams are defined, omit this section.

### 4. Summary
At the bottom, show:
- Total entries in catalog (across all 6 types)
- Total installed/enabled/configured locally
- Total not installed
- Total collections
- Total teams (if any)
