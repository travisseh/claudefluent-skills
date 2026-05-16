# Sync All Installed Items

## Context
Refresh every locally installed skill, agent, prompt, and hook by re-pulling from its source. A fast, lazy "make sure everything is up to date" command.

**Note:** Plugins and MCP servers are skipped during sync. They are stateless configuration — plugins are managed by their own marketplace update mechanism, and MCP servers are local config entries with nothing to re-pull.

## Steps

### 1. Read the Catalog
- Read `library.yaml` (colocated with this skill)
- Parse all entries from `library.skills`, `library.agents`, `library.prompts`, and `library.hooks`
- Skip `library.plugins` and `library.mcp_servers` — these are not syncable

### 2. Find All Installed Items
For each entry in the catalog:
- Determine the type (skill, agent, prompt) and corresponding directories from `default_dirs`
- Check if a directory or file matching the entry name exists in the **default** directory
- Check if a directory or file matching the entry name exists in the **global** directory
- Search recursively for name matches
- Collect every entry that is installed locally (either default or global)
- If nothing is installed, tell the user and exit

### 2.5. Prerequisite Preflight

Before re-pulling, run the [Prerequisite Preflight](preflight.md) across all installed items. The install set is every installed entry plus their transitive catalog dependencies (read-only walk of `library.yaml` — this catches prerequisites from dependencies that aren't yet installed but will be pulled in Step 4).

- If any `bin:` checks fail → **stop**. Do not proceed to Step 3.
- If any `env:` checks warn → **continue** to Step 3.

### 3. Batch-Pull by Source Repo

Group installed items by source repo to minimize clones:

1. **Parse and group** — For each installed entry, parse its `source` URL to extract `org`, `repo`, and `branch`. Group all entries sharing the same `org/repo/branch`.

2. **For each unique repo group**, clone the repo once:
   ```bash
   tmp_dir=$(mktemp -d)
   git clone --depth 1 --branch <branch> https://github.com/<org>/<repo>.git "$tmp_dir"
   ```
   If HTTPS fails (private repo), fall back to SSH:
   ```bash
   git clone --depth 1 --branch <branch> git@github.com:<org>/<repo>.git "$tmp_dir"
   ```

3. **For each entry in this repo group**, using the already-cloned `$tmp_dir`:
   - **Skills**: `cp -R "$tmp_dir/<parent_path>/" <target_directory>/<name>/`
   - **Agents**: `cp "$tmp_dir/<file_path>" <target_directory>/<agent_name>.md`
   - **Prompts**: `cp "$tmp_dir/<file_path>" <target_directory>/<prompt_name>.md`
   - **Hooks**: `cp "$tmp_dir/<file_path>" <target_directory>/<name>.sh && chmod +x`, then re-register in settings.json:
     - Read `event` and `matcher` from the hook's entry in `library.yaml`
     - Read `.claude/settings.json` (create with `{}` if missing)
     - Upsert entry under `hooks.<event>` using `$CLAUDE_PROJECT_DIR/.claude/hooks/<name>.sh` as the command path (see SKILL.md's Hooks section for the JSON structure)
     - If `matcher` is not set in `library.yaml`, omit the `matcher` field entirely
     - Deduplicate by command path; preserve all other settings
     - Write back
     - **Verify**: re-read settings.json and confirm the hook's command path appears under `hooks.<event>`. If missing, warn the user that re-registration failed for this hook.

4. **Clean up**: `rm -rf "$tmp_dir"`, then move to the next repo group.

### 4. Resolve Dependencies
For each installed entry that has a `requires` field:
- **Skip** `bin:` and `env:` entries — already checked in Step 2.5.
- For each catalog dependency (`skill:name`, `agent:name`, `prompt:name`, `hook:name`, `plugin:name`, `mcp:name`), check if it is also installed
- If a dependency is not installed, pull it as well
- Process dependencies before the items that require them

### 5. Report Results
Display a summary table:

```
## Sync Complete

| Type | Name | Status |
|------|------|--------|
| skill | skill-name | refreshed |
| agent | agent-name | refreshed |
| skill | other-skill | failed: <reason> |

Synced: X items
Failed: Y items
```

If any items failed (e.g., network error, missing source), list them with the reason so the user can fix individually.
