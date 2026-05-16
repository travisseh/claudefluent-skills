# Push an Item to the Library Source

## Context
The user has improved a skill, agent, prompt, or hook locally and wants to push changes back to the source repo.

**Note:** Plugins and MCP servers cannot be pushed. They have no source repo — plugins are managed by their marketplace and MCP servers are local configuration. If the user tries to push a plugin or MCP server, explain this and suggest alternative approaches (e.g., updating the catalog entry via `/aos-library add`).

## Input
The user provides an item name or description.

## Steps

### 1. Find the Entry
- Read `library.yaml` (colocated with this skill)
- Search across all sections (`library.skills`, `library.agents`, `library.prompts`, `library.hooks`, `library.plugins`, `library.mcp_servers`) for the matching entry
- If no match, tell the user the item wasn't found in the catalog
- If the entry is a plugin or MCP server, tell the user: "Plugins and MCP servers cannot be pushed — they have no source repo. Use `/aos-library add` to update the catalog entry." and return.

### 2. Locate the Local Copy
- Check the default directory for the type (from `default_dirs`)
- Check the global directory
- If found in multiple places, ask which one to push
- If not found locally, tell the user there's nothing to push

### 3. Check for Conflicts
Clone the source repo to a temp directory (shallow):
```bash
tmp_dir=$(mktemp -d)
git clone --depth 1 --branch <branch> <clone_url> "$tmp_dir"
```
- Compare the skill directory in the clone with the local copy
- If they differ AND the remote has changes not in the local copy, warn about conflict
- Ask the user to resolve before continuing

### 4. Push to Source
- If we don't already have a tmp clone from step 3, clone now:
  ```bash
  tmp_dir=$(mktemp -d)
  git clone --depth 1 --branch <branch> <clone_url> "$tmp_dir"
  ```
- For skills: remove the old directory and copy the local version:
  ```bash
  rm -rf "$tmp_dir/<path_in_repo>"
  cp -R <local_directory>/ "$tmp_dir/<path_in_repo>/"
  ```
- For agents/prompts: copy just the file:
  ```bash
  cp <local_file> "$tmp_dir/<path_in_repo>"
  ```
- For hooks: copy just the script file:
  ```bash
  cp <local_file> "$tmp_dir/<path_in_repo>"
  ```
- Stage ONLY the relevant changes:
  ```bash
  cd "$tmp_dir"
  git add <path_in_repo>
  ```
- Commit with the standard format:
  ```bash
  git commit -m "library: updated <name> <brief description of what changed>"
  ```
- Push:
  ```bash
  git push
  ```
- Clean up:
  ```bash
  rm -rf "$tmp_dir"
  ```

### 5. Confirm
Tell the user:
- What was pushed and where
- The commit message used
