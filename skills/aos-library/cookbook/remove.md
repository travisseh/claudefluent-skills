# Remove an Entry from the Library

## Context
The user wants to remove a skill, agent, prompt, hook, plugin, or MCP server from the library catalog and optionally undo the local installation. Since the catalog lives inside the aos repo (which updates via git self-check), mutations use the temp-clone pattern.

## Input
The user provides an item name or description.

## Steps

### 1. Find the Entry
- Read `library.yaml` (colocated with this skill)
- Search across all sections (`library.skills`, `library.agents`, `library.prompts`, `library.hooks`, `library.plugins`, `library.mcp_servers`) for the matching entry
- Determine the type
- If no match, tell the user the item wasn't found in the catalog

### 2. Confirm with User
Show the entry details and ask:
- "Remove **<name>** from the library catalog?"
- If installed locally, also ask: "Also delete the local copy at `<path>`?"

### 3. Clone the Marketplace Repo
```bash
tmp_dir=$(mktemp -d)
git clone --depth 1 git@github.com:Example Company/aos.git "$tmp_dir"
```

### 4. Remove from library.yaml
- Edit `$tmp_dir/skills/aos-library/library.yaml`
- Remove the entry from the appropriate section (`library.skills`, `library.agents`, `library.prompts`, `library.hooks`, `library.plugins`, or `library.mcp_servers`)
- If other entries depend on this one (via `requires`), warn the user before proceeding

### 4.5. Clean Collection and Team References
After removing the entry, scan all collections for references to the removed name.
- If found, warn the user: `"<name>" is referenced in collection(s): <list>`
- Ask: "Remove from these collections too?"
- If yes, remove the name from each collection's list in `library.yaml`

Also scan all teams for collections that reference this entry (indirectly). No action needed for teams — they reference collections, not entries directly.

### 5. Undo Local Installation (if requested)
If the user confirmed local removal:

**For skills, agents, prompts, hooks:**
- Check the default directory for the type (from `default_dirs`)
- Check the global directory
- Remove the directory or file:
  ```bash
  rm -rf <target_directory>/<name>
  ```

**For plugins:**
- Run `claude plugin disable <source>` to disable the plugin
- Optionally run `claude plugin uninstall <source>` if the user wants full removal

**For MCP servers:**
- Read `.mcp.json`, remove `mcpServers.<name>`, write back
- If `mcpServers` is now empty, the file can remain with `{"mcpServers": {}}`

### 5.5. Deregister Hook from Settings (hooks only)
If the removed item is a hook and was installed locally:
1. Read `.claude/settings.json`
2. Find the entry under `hooks.<event>` whose `command` matches the hook's install path (`$CLAUDE_PROJECT_DIR/.claude/hooks/<name>.sh`)
3. Remove that entry
4. If the event's array is now empty, remove the event key
5. If the `hooks` object is now empty, remove it
6. Write the updated settings back

### 6. Commit and Push
```bash
cd "$tmp_dir"
git add skills/aos-library/library.yaml
git commit -m "library: removed <type> <name>"
git push
```

### 7. Clean Up
```bash
rm -rf "$tmp_dir"
```

### 8. Confirm
Tell the user:
- The entry has been removed from the catalog
- Whether the local copy was also deleted
- If other entries depended on it, remind them to update those entries
- For hooks: note that a session restart may be needed for the deregistration to take effect
- Note: changes are pulled on next invocation via self-check
