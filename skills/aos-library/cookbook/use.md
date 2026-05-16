# Use an Item from the Library

## Context
Pull a skill, agent, prompt, hook, plugin, or MCP server from the catalog into the local environment. If already installed locally, overwrite with the latest from the source (refresh). Also handles collections (batch install) and teams (install multiple collections).

## Input
The user provides an item name or description.

## Steps

### 1. Read the Catalog
- Read `library.yaml` (colocated with this skill)
- Search across `library.skills`, `library.agents`, `library.prompts`, `library.hooks`, `library.plugins`, and `library.mcp_servers`
- Match by name (exact) or description (fuzzy/keyword match)
- If multiple matches, show them and ask the user to pick one
- If no match, continue to Step 2 (collection/team check)

### 2. Check Collections & Teams
If an entry was found in Step 1, skip this step — proceed to Step 2.5.

If no entry was found, check if the name matches a key in `collections`. If it matches a collection, proceed to sub-step 2a. If not, check if the name matches a key in `teams`. If it matches a team, proceed to sub-step 2b. If neither matches, tell the user and suggest `/aos-library search`.

#### 2a. Install Collection
1. **Resolve** the collection — it's a flat list of entry names (e.g., `core: [interview-me, research, plugin-dev]`)
2. **Look up** each name across all type lists (`library.skills`, `library.agents`, `library.prompts`, `library.hooks`, `library.plugins`, `library.mcp_servers`). If a name has no match in any list, warn: `"Warning: '<name>' not found in catalog — skipping"` and continue. If zero items remain after filtering, report `"Collection '<name>' resolved to 0 items — nothing to install"` and return.
3. **Show** the resolved list. If this is a direct user invocation, confirm before proceeding. If called from a parent workflow, skip confirmation and proceed automatically.
   ```
   Collection "<name>" contains N items:
   - skill: interview-me
   - plugin: plugin-dev
   - mcp_server: linear
   Install all? (y/n)
   ```
3.5. **Prerequisite Preflight (collection)** — Run the [Prerequisite Preflight](preflight.md) across all resolved collection items. The install set is every item in the collection plus their transitive catalog dependencies (read-only walk of `library.yaml`).
   - If any `bin:` checks fail → **stop**. Do not proceed to installation.
   - If any `env:` checks warn → **continue**.

4. **Separate by install mechanism** — Split resolved items into two groups:
   - **Source-based** (skills, agents, prompts, hooks): have GitHub source URLs, installed via clone + copy
   - **Config-based** (plugins, MCP servers): no source URL, installed via CLI commands or config file writes

5. **Install source-based items by repo batch** — For each resolved source-based entry, parse the `source` URL to extract `org`, `repo`, and `branch`. Group all entries that share the same `org/repo/branch` combination. Build a set of all item names in this collection for dependency dedup.

   For each unique `org/repo/branch` group:
   a. Clone the repo once into a temp directory:
      ```bash
      tmp_dir=$(mktemp -d)
      git clone --depth 1 --branch <branch> https://github.com/<org>/<repo>.git "$tmp_dir"
      ```
      If clone fails, try SSH: `git clone --depth 1 --branch <branch> git@github.com:<org>/<repo>.git "$tmp_dir"`
   b. For each entry in this repo group, using the already-cloned `$tmp_dir`:
      - Run Step 3 (Resolve Dependencies) — skip `bin:` and `env:` entries (already checked in sub-step 3.5), and skip any dependency whose name is already in the collection's item set (it will be installed when the batch loop reaches it). Only resolve catalog dependencies that are NOT in this collection.
      - Run Step 4 (Determine Target Directory)
      - Run Step 5's type-specific copy logic using `$tmp_dir` as the already-cloned source (skip Step 5's clone — the repo is already available in `$tmp_dir`)
      - Run Step 5.5 (Register Hook in Settings) if the entry is a hook
      - Run Step 6 (Verify Installation)
   c. Clean up: `rm -rf "$tmp_dir"`
   d. Move to the next repo group.

6. **Install config-based items** — For each plugin and MCP server in the collection:
   - For plugins: run Step 5P (Install Plugin)
   - For MCP servers: run Step 5M (Install MCP Server)

7. **Summary** table when done:
   ```
   | Type | Name | Status |
   |------|------|--------|
   | skill | interview-me | installed |
   | plugin | plugin-dev | enabled |
   | mcp_server | linear | configured |
   ```
8. Return (do not fall through to Step 3).

#### 2b. Install Team
1. **Resolve** the team — read its `collections` list from `library.yaml` `teams` section
2. **Look up** each collection name in the `collections` section. If a name has no match, warn: `"Warning: collection '<name>' not found — skipping"` and continue.
3. **Show** the resolved collections and their items. If this is a direct user invocation, confirm before proceeding.
   ```
   Team "<name>" includes N collections:
   - workflow (4 items)
   - quality-of-life (3 items)
   Install all? (y/n)
   ```
4. **Install each collection** — For each collection in the team's list, run sub-step 2a (Install Collection) with confirmation skipped (already confirmed at team level).
5. **Summary** — aggregate results across all collections.
6. Return.

### 2.5. Prerequisite Preflight (single item)

Before resolving catalog dependencies or fetching, run the [Prerequisite Preflight](preflight.md) for this entry. The install set is this single entry plus its transitive catalog dependencies (read-only walk of `library.yaml`).

- If any `bin:` checks fail → **stop**. Do not continue to Step 3.
- If any `env:` checks warn → **continue** to Step 3.
- If the entry has no `bin:` or `env:` entries in its dependency tree, skip this step.

### 3. Resolve Dependencies
If the entry has a `requires` field:
- **Skip** `bin:` and `env:` entries — already checked in Step 2.5.
- For each catalog reference (`skill:name`, `agent:name`, `prompt:name`, `hook:name`, `plugin:name`, `mcp:name`):
  - Look it up in `library.yaml`
  - If found, recursively run the `use` workflow for that dependency first
  - If not found, warn the user: "Dependency <ref> not found in library catalog"
- Process all dependencies before the requested item

### 4. Determine Target Directory
- Read `default_dirs` from `library.yaml`
- If user said "global" or "globally" → use the `global` path
- If user specified a custom path → use that path
- Otherwise → use the `default` path
- Select the correct section based on type (skills/agents/prompts/hooks)
- Hooks do not have a global directory — always use `default`
- **Plugins and MCP servers have no target directory** — skip this step for those types

### 5. Fetch from Source

**For skills, agents, prompts, and hooks** (source is a GitHub URL):
- Parse the URL to extract: `org`, `repo`, `branch`, `file_path`
  - Browser URL pattern: `https://github.com/<org>/<repo>/blob/<branch>/<path>`
  - Raw URL pattern: `https://raw.githubusercontent.com/<org>/<repo>/<branch>/<path>`
- Determine the clone URL: `https://github.com/<org>/<repo>.git`
- Determine the parent directory path within the repo (everything before the filename)
- Clone into a temporary directory:
  ```bash
  tmp_dir=$(mktemp -d)
  git clone --depth 1 --branch <branch> https://github.com/<org>/<repo>.git "$tmp_dir"
  ```
- For skills: ensure the target directory exists and copy the entire parent directory:
  ```bash
  mkdir -p <target_directory>
  cp -R "$tmp_dir/<parent_path>/" <target_directory>/<name>/
  ```
- For agents: ensure the target directory exists and copy the agent file:
  ```bash
  mkdir -p <target_directory>
  cp "$tmp_dir/<file_path>" <target_directory>/<agent_name>.md
  ```
- For prompts: ensure the target directory exists and copy the prompt file:
  ```bash
  mkdir -p <target_directory>
  cp "$tmp_dir/<file_path>" <target_directory>/<prompt_name>.md
  ```
- For hooks: copy the script file to the target and make executable:
  ```bash
  mkdir -p <target_directory>
  cp "$tmp_dir/<file_path>" <target_directory>/<name>.sh
  chmod +x <target_directory>/<name>.sh
  ```
- If the agent or prompt is nested in a subdirectory, copy the subdirectory to keep grouping.
- Clean up:
  ```bash
  rm -rf "$tmp_dir"
  ```

**If clone fails (private repo)**, try SSH:
  ```bash
  git clone --depth 1 --branch <branch> git@github.com:<org>/<repo>.git "$tmp_dir"
  ```

**For plugins**, skip this step — proceed to Step 5P.

**For MCP servers**, skip this step — proceed to Step 5M.

### 5P. Install Plugin

1. Run `claude plugin list --json` and cache the output
2. Check if any entry's `id` starts with `<name>@` (the `id` field is `name@marketplace`, e.g., `plugin-dev@claude-plugins-official`)
3. If the entry exists and `"enabled": true` → skip, report "already enabled"
4. If the entry exists but `"enabled": false` → run `claude plugin enable <source>`, report "enabled"
5. If not found in the list (not installed):
   a. If the plugin definition has a `marketplace` field: run `claude plugin marketplace list --json` — if no entry has a matching `repo` field, run `claude plugin marketplace add <marketplace>` first
   b. Run `claude plugin install <source>`, then `claude plugin enable <source>`
6. If install fails → report the error

### 5M. Install MCP Server

1. Read `.mcp.json` in the project root. If the file does not exist, create it — start from `{"mcpServers": {}}`.
2. If `mcpServers.<name>` exists with identical config → skip, report "already configured"
3. If `mcpServers.<name>` exists with different config → ask the user before overwriting
4. If `mcpServers.<name>` is not present → add the entry:
   - For `type: http`: `{ "type": "http", "url": "<url>" }`
   - For `type: stdio`: `{ "command": "<command>", "args": [<args>], "env": {<env>} }` (omit `args`/`env` if not defined)
5. Write the updated JSON to `.mcp.json` — create the file if it doesn't exist, or merge into the existing file preserving all other entries. No special permissions are needed for this file.

### 5.5. Register Hook in Settings (hooks only)

If the item is a hook, register it in `.claude/settings.json` so Claude Code activates it.

1. Read the hook's `event` and `matcher` fields from its `library.yaml` entry
2. Read `.claude/settings.json` (create the file and `.claude/` directory if they don't exist, starting from `{}`)
3. Upsert a hook entry so the file contains this structure:
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
4. Follow these rules:
   - If `matcher` is not set on the catalog entry, omit the `"matcher"` field entirely
   - Deduplicate: if an entry with the same `command` path already exists under that event, update it in place — do not create a second entry
   - If the event key doesn't exist under `hooks`, create it
   - **Preserve everything else** in the file — permissions, other hook events, other entries under the same event, all other top-level keys
5. Write the updated JSON back to `.claude/settings.json`

### 6. Verify Installation
- For skills: confirm SKILL.md exists in the target directory
- For agents: confirm the agent .md file exists in the target
- For prompts: confirm the prompt file exists in the target
- For hooks: confirm the .sh file exists, is executable, and has an entry in settings.json
- For plugins: confirm the plugin is enabled via `claude plugin list --json`
- For MCP servers: confirm the entry exists in `.mcp.json`
- Report success with the installed path or status

### 7. Confirm
Tell the user:
- What was installed and where
- Any dependencies that were also installed
- If this was a refresh (overwrite), mention that
- For hooks: note that a session restart may be needed for the hook to take effect
- For plugins: note that a session restart may be needed
