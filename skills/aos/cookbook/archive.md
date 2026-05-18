# Archive — Move Infrastructure to Archive

## Context
Move a file or directory to `archive/`, register it in `archive/manifest.yaml` with provenance metadata, and exclude the archive from agent searches via `.ignore`. This is the formal workspace archival mechanism — it ensures archived content stops surfacing in agent tool calls (Glob, Grep).

## Input
The user provides a path to archive (file or directory). The path must exist and be relative to the workspace root.

## Steps

### 1. Validate Target
- **If the path is absolute**, check whether it falls within the workspace root. If so, convert it to a relative path by stripping the workspace root prefix. If not, reject with an error — archiving content from outside the workspace is not supported.
- Strip any leading `./`
- Check the path exists:
  ```bash
  test -e <path>
  ```
- If not found, report the error and stop

### 2. Initialize Archive Infrastructure
- Create the archive directory if it does not exist:
  ```bash
  mkdir -p archive
  ```
- Create the manifest if it does not exist:
  ```bash
  if [ ! -f archive/manifest.yaml ]; then
    echo "entries:" > archive/manifest.yaml
  fi
  ```

### 3. Check for Collisions
- Read `archive/manifest.yaml` to see existing entries
- Determine the basename of the target
- **If a file or directory with that basename already exists under `archive/`**, generate a timestamped name:
  - For directories: `<basename>-<YYYYMMDD>-<HHMMSS>`
  - For files: `<name>-<YYYYMMDD>-<HHMMSS>.<ext>` (preserve extension)
  - Example: `hubspot` → `hubspot-20260321-143022`
- **If no collision**, use the basename as-is

### 4. Capture Provenance
Ask the user two questions before moving or recording anything:

1. **"Why are you archiving this?"** — Record the answer as the `reason` field. This is required. Examples: "Migrated to plugin", "No longer needed after auth rewrite", "Superseded by v2 implementation".

2. **"What replaces it, if anything?"** — Record the answer as the `superseded_by` field. This is optional — if nothing replaces it, set to `null`. Examples: "repos/aos/skills/aos-library/", "the new auth-service module", `null`.

### 5. Execute Archive
- Move the target to the archive directory:
  ```bash
  mv <path> archive/<archived-name>
  ```

### 6. Update Manifest
- Read `archive/manifest.yaml`
- Append a new entry under `entries:`:
  ```yaml
  - original_path: <original-path>
    archived_path: archive/<archived-name>
    archived_at: "<ISO-8601 timestamp>"
    reason: "<user's answer from step 4>"
    superseded_by: "<replacement path or null>"
  ```
- Write the updated manifest back

### 7. Exclude from Agent Searches
Ensure `archive/**` is in the workspace `.ignore` file so archived content is invisible to agent searches (Glob, Grep). Claude Code always respects `.ignore` files, even in non-git workspaces.

1. If `.ignore` already exists, check whether it contains `archive/**`
   - If found, skip — already configured
   - If not found, append `archive/**` to the file
2. If `.ignore` does not exist, create it:
   ```bash
   echo 'archive/**' > .ignore
   ```

### 8. Confirm
Report to the user:
- **Archived**: `<original-path>` → `archive/<archived-name>`
- **Reason**: the recorded reason
- **Superseded by**: the replacement (or "nothing")
- **Collision**: whether renaming was required (and new name if so)
- **Manifest**: confirmation that `archive/manifest.yaml` was updated
- **Excluded**: whether `archive/**` was added to `.ignore` (or was already present)
