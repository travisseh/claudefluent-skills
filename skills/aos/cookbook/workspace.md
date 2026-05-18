# Setup — Bootstrap Workspace Infrastructure

## Context
Bootstrap workspace infrastructure: clone repos, set up directory structure, copy templates. Component installation (skills, agents, hooks, plugins, MCP servers) is handled separately by the aos-library skill via `/aos-library use`.

Can be run directly (`/aos workspace`) or as part of the `/aos setup` wizard.

## Steps

### 1. Read Workspace Configuration
- Read `workspace.yaml` (colocated with this skill)

### 2. Create Directory Structure
Create the workspace infrastructure directories:
```bash
mkdir -p archive
```
Initialize the archive manifest if it does not exist:
```bash
if [ ! -f archive/manifest.yaml ]; then
  echo "entries:" > archive/manifest.yaml
fi
```

### 3. Clone Repos
For each repo in `workspace.yaml` `repos` section:
- Determine the target directory:
  - If the repo has a `default_dir` field, use that
  - Otherwise, use `<default_dirs.repos.default>/<repo-name>/`
- If the directory already exists, skip cloning and notify the user
- Clone the repo:
  ```bash
  git clone <source> <target_directory>
  ```
- **If clone fails** (e.g., SSH permission denied), convert the URL to HTTPS and retry:
  - `git@github.com:org/repo.git` → `https://github.com/org/repo.git`
  - `ssh://git@github.com/org/repo.git` → `https://github.com/org/repo.git`
  ```bash
  git clone <https_url> <target_directory>
  ```
- If both fail, report the error and continue with remaining repos

### 4. Copy Workspace Template
Copy the justfile template from aos:
- The template is at `templates/justfile` relative to the **aos root** (not the skill directory — go up two levels from the cookbook)
- Copy to `./justfile` in the workspace
- If a justfile already exists, ask the user before overwriting

### 5. Create .env
Create a `.env` file with output convention in the workspace root:
```bash
# Create .env with output convention if it doesn't exist
if [ ! -f .env ]; then
  cat > .env << 'EOF'
DEFAULT_AGENT_OUTPUT_PATH=./artifacts/
EOF
  mkdir -p artifacts
fi
```
If `.env` already exists, check for `DEFAULT_AGENT_OUTPUT_PATH` and append if missing:
```bash
if [ -f .env ] && ! grep -q 'DEFAULT_AGENT_OUTPUT_PATH' .env; then
  echo 'DEFAULT_AGENT_OUTPUT_PATH=./artifacts/' >> .env
  mkdir -p artifacts
fi
```

### 6. Configure Archive Exclusion
Create a `.ignore` file in the workspace root so archived content is invisible to agent searches (Glob, Grep). Claude Code always respects `.ignore` files (gitignore syntax), even in non-git workspaces.

1. If `.ignore` already exists, check whether it contains `archive/**`
   - If found, skip — already configured
   - If not found, append `archive/**` to the file
2. If `.ignore` does not exist, create it:
   ```bash
   echo 'archive/**' > .ignore
   ```

**Why `.ignore` instead of permission deny rules:** Deny rules block the tool entirely, preventing intentional reads (e.g., restoring archived components). `.ignore` only affects search/discovery — explicit `Read` of a known archive path still works.

### 7. Write Workspace Conventions
Copy the conventions template to `.claude/CLAUDE.md`:
- The template is at `templates/CLAUDE.md` relative to the **aos root** (same resolution as Step 4)
- If `.claude/CLAUDE.md` does not exist, create it (ensure `.claude/` exists with `mkdir -p .claude`) by copying the template
- If `.claude/CLAUDE.md` exists, check for the sentinel: `grep -q "# Workspace Conventions" .claude/CLAUDE.md`
  - If found, skip — conventions are already written
  - If not found, append the template contents to the end of the file

### 8. Install Workspace Scripts
Copy all utility scripts from aos to `.claude/scripts/`:
```bash
mkdir -p .claude/scripts
cp "${AOS_ROOT}"/scripts/* .claude/scripts/
chmod +x .claude/scripts/*
```
Always overwrite — use latest from aos.

**Where is `AOS_ROOT`?** The aos root is two levels up from the cookbook directory (this file lives at `skills/aos/cookbook/workspace.md`). Use the same path resolution as Step 4 (justfile copy).

### 9. Summary
Report what was set up:
- **Repos cloned**: list each repo and its target directory (or "already exists")
- **Files created**: list directories and files that were created

Then tell the user:
```
Infrastructure ready. To install components, run:
  /aos-library list          — see available skills, plugins, MCP servers
  /aos-library use <name>    — install a component, collection, or team
```
