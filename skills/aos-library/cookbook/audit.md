# Audit Catalog Dependencies

## Context
Scan catalog entries' source code for dependencies not declared in their `requires` field. Reports gaps so they can be fixed via `/aos-library add` (re-add with correct requires) or direct catalog update.

**Note:** Plugins and MCP servers are skipped during audit. They have no source files to scan for undeclared dependencies.

## Input
- `/aos-library audit` — audit all entries
- `/aos-library audit <name>` — audit a specific entry (if the name exists in multiple types, ask the user to disambiguate)

## Steps

### 1. Read the Catalog
- Read `library.yaml` (colocated with this skill)
- If a specific name was given, find that entry. If not found, tell the user and exit.
- If no name given, collect all entries from `library.skills`, `library.agents`, `library.prompts`, and `library.hooks`
- Skip `library.plugins` and `library.mcp_servers` — these have no source files to audit

### 2. Group by Source Repo
Parse each entry's `source` URL to extract `org`, `repo`, and `branch`. Group entries sharing the same `org/repo/branch`.

### 3. Scan Each Repo Group
For each unique repo group, clone once:
```bash
tmp_dir=$(mktemp -d)
git clone --depth 1 --branch <branch> https://github.com/<org>/<repo>.git "$tmp_dir"
```
If HTTPS fails, fall back to SSH.

For each entry in this repo group, scope the scan by type:
- **Skills** (directories): scan all files in `$tmp_dir/<parent_path>/` recursively
- **Agents, prompts, hooks** (single files): scan only `$tmp_dir/<file_path>`

Scan for:

- **Binary deps**: commands in execution position (shebangs, direct invocation, `command -v`) that aren't shell builtins or standard coreutils
- **Env var deps**: `$VAR` / `${VAR}` reads and `os.getenv()` / `os.environ` patterns for non-standard uppercase variables (ignore shell internals like PATH/HOME/PWD/PPID and Claude internals like CLAUDE_PROJECT_DIR)
- **Catalog deps**: references to other skills, hooks, agents, or prompts by name; `mcp__<server>__` tool patterns

Compare findings against the entry's declared `requires` field. Record any undeclared dependencies.

Clean up after each repo group: `rm -rf "$tmp_dir"`

### 4. Report Findings

If no gaps found:
```
All catalog entries have complete dependency declarations.
```

If gaps found, display a table:
```
## Audit Results

| Entry | Type | Undeclared Dependencies | Evidence |
|-------|------|------------------------|----------|
| enforce-output-convention | hook | bin:jq | line 16: `jq -r '.tool_input...'` |
| hubspot | skill | bin:uv, env:HUBSPOT_SERVICE_KEY | SKILL.md: `uv run ...`, `${HUBSPOT_SERVICE_KEY}` |

X of Y entries have undeclared dependencies.
```

### 5. Offer to Fix

If gaps were found, ask the user: "Update the catalog with these dependencies?"

If yes, use the temp-clone pattern to update `library.yaml`:
```bash
fix_dir=$(mktemp -d)
git clone --depth 1 git@github.com:Example Company/aos.git "$fix_dir"
```

For each entry with gaps:
- Read the entry in `$fix_dir/skills/aos-library/library.yaml`
- Merge undeclared dependencies into the entry's existing `requires` field (don't replace)
- If the entry has no `requires` field, add one
- Deduplicate and sort the final `requires` list alphabetically

Bump the version in `$fix_dir/.claude-plugin/plugin.json`.

```bash
cd "$fix_dir"
git add skills/aos-library/library.yaml .claude-plugin/plugin.json
git commit -m "library: update requires from audit"
git push
rm -rf "$fix_dir"
```

If no, report the findings and exit — the user can fix manually.
