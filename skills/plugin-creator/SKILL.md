---
name: plugin-creator
description: Create Claude Code plugins with correct structure, marketplace setup, and install flow. Wraps plugin-dev with hard-won knowledge about local plugin distribution. Use when creating a new plugin, setting up a local marketplace, or troubleshooting plugin loading issues.
---

# Plugin Creator

Create Claude Code plugins that actually load correctly. This skill supplements `/plugin-dev:create-plugin` with marketplace and distribution knowledge that `plugin-dev` doesn't cover.

When using this skill from Codex, do not rely on Claude slash commands existing. Perform the equivalent file creation and marketplace edits directly in the workspace, and treat `/plugin...` references below as historical Claude workflows.

## Workflow

### Step 1: Create the plugin with plugin-dev

Invoke `/plugin-dev:create-plugin` to handle the 8-phase plugin creation process (structure, manifest, commands, agents, skills, hooks, validation).

If `plugin-dev` is not installed, tell the user to run:
```
/plugin install plugin-dev@claude-code-marketplace
```

### Step 2: Set up local distribution

After `plugin-dev` finishes creating the plugin, handle the part it doesn't cover — making the plugin actually loadable.

#### Option A: Add to existing local marketplace

If `.claude/plugins/.claude-plugin/marketplace.json` already exists, add the new plugin to it:

1. Move or create the plugin directory under `.claude/plugins/`
2. Add an entry to `.claude/plugins/.claude-plugin/marketplace.json`:
```json
{
  "name": "new-plugin-name",
  "source": "./new-plugin-name",
  "description": "What it does"
}
```
3. Bump the version in the plugin's `.claude-plugin/plugin.json`
4. Run: `/plugin install new-plugin-name@local-plugins --scope local`
5. Restart Claude Code

#### Option B: Create a new local marketplace

If no local marketplace exists yet:

1. Create the plugin under `.claude/plugins/new-plugin-name/`
2. Create `.claude/plugins/.claude-plugin/marketplace.json`:
```json
{
  "name": "local-plugins",
  "owner": { "name": "Your Name" },
  "plugins": [
    {
      "name": "new-plugin-name",
      "source": "./new-plugin-name",
      "description": "What it does"
    }
  ]
}
```
3. Run: `/plugin marketplace add ./.claude/plugins`
4. Run: `/plugin install new-plugin-name@local-plugins --scope local`
5. Restart Claude Code

### Step 3: Verify

After restart, confirm:
- `/plugin` shows the plugin under Installed
- Slash commands appear when typing `/plugin-name:`
- Agents appear in `/agents`

---

## Critical Knowledge (Things That Will Bite You)

### Commands vs Skills vs Agents
- **Commands** (`commands/*.md`) → Show up as `/plugin-name:command-name` slash commands. User-invoked.
- **Skills** (`skills/name/SKILL.md`) → Model-invoked. Claude uses them automatically based on context. They do NOT appear as slash commands.
- **Agents** (`agents/*.md`) → Show up in `/agents`. Can be invoked by user or Claude.

If you want a user-invocable entry point, you MUST put it in `commands/`, not just `skills/`.

### Command frontmatter
```yaml
---
description: What this command does
argument-hint: optional hint for arguments
---
```
Do NOT put `name` in command frontmatter. The filename IS the command name.

### Skill frontmatter
```yaml
---
name: skill-name
description: What this skill does and when to use it
---
```

### Agent frontmatter
```yaml
---
name: agent-name
description: What this agent does and when to invoke it
tools:
  - Read
  - Glob
  - Grep
  - Bash
---
```

### plugin.json manifest
```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "What it does",
  "author": { "name": "Your Name" }
}
```
**`author` MUST be an object** with a `name` field, NOT a string. `"author": "name"` will fail validation.

### Plugin structure
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # ONLY manifest goes here
├── commands/                # At root, NOT inside .claude-plugin/
├── skills/
├── agents/
├── hooks/
├── crons/                   # Scheduled tasks (see /plugin-cron skill)
│   └── <cron-name>/
│       ├── run.sh           # Entry point
│       └── send-email.ts    # Delivery (optional)
└── state/                   # Persistent memory (optional)
```

### You CANNOT manually edit installed_plugins.json
Claude Code manages `~/.claude/plugins/installed_plugins.json` internally. Manual edits are silently ignored or cause weird behavior. Always use the `/plugin install` flow.

### Plugins are cached — BUMP VERSION AFTER ANY CHANGE
When installed, plugins are COPIED to `~/.claude/plugins/cache/marketplace-name/plugin-name/version/`. Editing the source files does nothing until you:
1. Bump the version in `plugin.json`
2. Bump the matching version in `marketplace.json`
3. Run `/plugin update plugin-name@marketplace-name`
4. Restart Claude Code

**This includes adding new commands/skills/agents.** New files won't be discovered until both versions are bumped. Always bump both `plugin.json` AND `marketplace.json` together.

### enabledPlugins
After installing, the plugin must be enabled in settings. The install command usually handles this, but if not, add to the appropriate settings file:
```json
{
  "enabledPlugins": {
    "plugin-name@marketplace-name": true
  }
}
```
- `local` scope → `.claude/settings.local.json`
- `project` scope → `.claude/settings.json`

### Dev testing shortcut
Skip all marketplace setup during development:
```bash
claude --plugin-dir ./path-to-plugin
```
This loads the plugin for that session only. No install, no cache, no version bumping.

### Debugging
- `claude --debug` or `/debug` to see plugin loading details
- `/plugin validate .` inside the plugin directory to check manifest
- Check the Errors tab in `/plugin` UI

---

## Memory Model (Recommended Pattern)

Plugins that need to persist knowledge across sessions should use a two-tier state model:

```
state/
├── insights.md              # Durable strategic knowledge. ALWAYS read first.
└── daily/
    └── YYYY-MM-DD.md        # Session notes, rotated after 7 days.
```

**Protocol (embed in command, agent, AND skill docs):**
1. **Read:** Always read `insights.md` first. Then today + yesterday's daily notes only.
2. **Write:** After every session, update today's daily note. Promote durable learnings to `insights.md`.
3. **Rotate:** When creating today's note, delete daily notes older than 7 days (extract important bits to `insights.md` first).

**Why two tiers:** `insights.md` stays compact and authoritative. Daily notes capture session-specific context without bloating the permanent record. The rotation keeps the daily folder small.

Add supplementary durable files as needed (e.g., `persona-gaps.md`, `audit-log.md`) — but `insights.md` + `daily/` is the core.

**Important:** Reference the memory protocol in ALL entry points — the main command, the agent, AND the skill. Otherwise Claude won't know to read/write state depending on which entry point triggers.

---

## Cron Jobs

Plugins can include scheduled tasks that run `claude -p` on a timer. Use the `/plugin-cron` skill for templates, gotchas, and setup instructions.

Crons live in `crons/<name>/run.sh` within the plugin. They are scheduled via macOS launchd plists in `~/Library/LaunchAgents/`.

When creating a new plugin that needs automation, always ask if the user wants a cron added.

---

## Quick Reference: Full Plugin Lifecycle

```
1. /plugin-dev:create-plugin     ← Structure + content
2. Move to .claude/plugins/      ← Location
3. Add to marketplace.json       ← Discovery
4. /plugin install ... --scope   ← Registration
5. Restart Claude Code           ← Loading
6. Test slash commands + agents  ← Verification

To update after changes:
1. Bump version in plugin.json
2. /plugin update plugin-name@marketplace-name
3. Restart Claude Code
```
