# Add a New Entry to the Library

## Context
Register a new skill, agent, prompt, hook, plugin, or MCP server in the library catalog. Since the catalog lives inside the aos repo (which updates via git self-check), mutations use the temp-clone pattern.

## Input
The user provides: name, description, source, and optionally type and dependencies.

## Steps

### 1. Determine the Type
Figure out the type from the user's prompt or the source:
- If the source path contains `SKILL.md` or user says "skill" → type is `skill`
- If the source path contains `AGENT.md` or user says "agent" → type is `agent`
- If user says "prompt" → type is `prompt`
- If the source path ends in `.sh` or user says "hook" → type is `hook`
- If the source matches a plugin identifier (`name@marketplace`) or user says "plugin" → type is `plugin`
- If user says "mcp" or "mcp server" → type is `mcp_server`
- If ambiguous, ask the user

**For hooks**, also collect:
- **`event`** (required) — which hook event: `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PreCompact`, `Notification`
- **`matcher`** (optional) — tool/command pattern (e.g., `"Write|Edit"`, `"Bash"`)

### 2. Validate the Source
- **GitHub URL** (skills, agents, prompts, hooks): Verify the URL is well-formed (matches browser or raw URL patterns). Confirm the source points to a specific file, not a directory.
- **Plugin identifier** (plugins): Verify it matches `name@marketplace` format. No URL validation needed.
- **MCP servers**: No source to validate — configuration is inline. Collect `type` (http/stdio), and either `url` (http) or `command`/`args`/`env` (stdio).

**For plugins and MCP servers**, skip Steps 3 (Parse Dependencies) — they have no source files to scan. Proceed directly to Step 4.

### 3. Parse Dependencies
First, fetch the component's source files to scan for dependencies. Parse the source URL to extract org, repo, branch, and file path.

Shallow-clone the source repo to get the full file tree:
```bash
scan_dir=$(mktemp -d)
git clone --depth 1 --branch <branch> https://github.com/<org>/<repo>.git "$scan_dir"
```
If HTTPS fails, fall back to SSH. If both fail, skip the automatic scan and rely on the user's input in the confirmation step below.

For **skills** (directories), scan all files in `$scan_dir/<parent_path>/` recursively. For **single-file types** (hooks, agents, prompts), scan only the specific file at `$scan_dir/<file_path>`.

Clean up when done: `rm -rf "$scan_dir"`

Scan the fetched source files for:
- **Binary deps**: commands in execution position (shebangs, direct invocation, `command -v`) that aren't shell builtins or standard coreutils
- **Env var deps**: `$VAR` / `${VAR}` reads and `os.getenv()` / `os.environ` patterns for non-standard uppercase variables
- **Catalog deps**: references to other skills, hooks, agents, or prompts by name; `mcp__<server>__` tool patterns

Format findings as typed references in the `requires` list. Present scan results to the user: "Detected these dependencies: [list]. Confirm, edit, or add more?"

**Catalog references** (`skill:name`, `agent:name`, `prompt:name`, `hook:name`):
- Verify each dependency already exists in `library.yaml` or warn the user
  - If they don't exist, add them to `library.yaml` first. If those files have dependencies, add them recursively.
  - You can detect these sometimes by looking at the frontmatter, and then in the file content look for `/<prompt|agent|skill>:name` references.

**Environmental prerequisites** (`bin:name`, `env:VAR`, `plugin:name`, `mcp:name`):
- Do **not** validate these against the catalog — they reference the host environment, not library entries.
- Validate tokens are non-empty — reject bare `bin:`, `env:`, `plugin:`, or `mcp:` (ask user to provide the name).
- These go in the same `requires` list: `requires: [bin:ffmpeg, env:API_KEY, plugin:superpowers, mcp:linear, skill:other-skill]`

**No preflight execution** — `add` registers a catalog entry; it does not install. Prerequisites are checked on the consumer's machine at `/aos-library use` time.

### 4. Clone the Marketplace Repo
```bash
tmp_dir=$(mktemp -d)
git clone --depth 1 git@github.com:Example Company/aos.git "$tmp_dir"
```

### 5. Add the Entry to library.yaml
Read `$tmp_dir/skills/aos-library/library.yaml`, add the new entry under the correct section:

```yaml
# Under library.skills, library.agents, library.prompts, or library.hooks
- name: <name>
  description: <description>
  source: <source>
  requires: [<typed:refs>]  # omit if no dependencies
```

For hooks, add the extra fields:
```yaml
# Under library.hooks
- name: <name>
  description: <description>
  source: <source>
  event: <event>             # required for hooks
  matcher: "<pattern>"       # optional — omit if hook should run for all invocations
  requires: [<typed:refs>]   # omit if no dependencies
```

For plugins:
```yaml
# Under library.plugins
- name: <name>
  description: <description>
  source: <name>@<marketplace>
  marketplace: <github-repo>  # optional — only if custom marketplace
```

For MCP servers:
```yaml
# Under library.mcp_servers — http type
- name: <name>
  description: <description>
  type: http
  url: <url>

# Under library.mcp_servers — stdio type
- name: <name>
  description: <description>
  type: stdio
  command: <command>
  args: [<args>]    # optional
  env:              # optional
    KEY: value
```

**YAML formatting rules:**
- 2-space indentation
- List items use `- ` prefix
- Properties are indented under the list item
- Keep entries alphabetically sorted by name within each section
- For skills reference the `.../<skill-name>/SKILL.md` file
- For agents reference the `.../<agent name>.md` file
- For prompts reference the `.../<prompt name>.md` file
- For hooks reference the `.../<hook-name>.sh` file

### 5.5. Offer Collection Membership
If `collections` exists in `library.yaml` and is non-empty:
- Show the existing collections and their items
- Ask the user: "Add **<name>** to any collections?"
- If the user picks one or more collections, append the entry's name to the relevant collection list in `library.yaml`
- If the user declines, continue without changes

### 6. Commit and Push
```bash
cd "$tmp_dir"
git add skills/aos-library/library.yaml
git commit -m "library: added <type> <name>"
git push
```

### 7. Clean Up
```bash
rm -rf "$tmp_dir"
```

### 8. Confirm
Tell the user the entry has been added and is now available for others to use via `/aos-library use <name>`. Note: changes are pulled on next invocation via self-check.
