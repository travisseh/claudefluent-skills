# Prerequisite Preflight

## Context
Before fetching or installing anything, check that the host environment meets the entry's prerequisites. This procedure is referenced by [use.md](use.md) (Step 2.5 and sub-step 3.5) and [sync.md](sync.md) (Step 2.5). It is **not** run during `add` — `add` only validates syntax.

Only `bin:` and `env:` are prerequisites (host environment checks). Other typed references (`plugin:`, `mcp:`, `skill:`, `agent:`, `prompt:`, `hook:`) are catalog dependencies — they are resolved during the install flow, not during preflight.

## Input
An **install set** — one or more library entries about to be installed or refreshed.

## Steps

### 1. Collect Prerequisites
Walk the `requires` field of every entry in the install set. For each catalog reference (`skill:name`, `agent:name`, `prompt:name`, `hook:name`, `plugin:name`, `mcp:name`), also walk that dependency's `requires` field recursively in `library.yaml`. This is a **read-only** pass — no cloning, no fetching.

Extract all `bin:X` and `env:Y` entries. Deduplicate. Track which entries require each prerequisite (for attribution in error messages).

Skip malformed entries (`bin:` or `env:` with no token after the colon) — warn once and continue.

### 2. Check Binaries
For each unique `bin:X`:
```bash
command -v X
```
Collect all that fail (exit code ≠ 0).

### 3. Report Missing Binaries
If any binaries are missing, report **all** at once and **stop** — do not proceed to installation:
```
Missing required system binaries:
- google-chrome (required by: browser-automation)
- ffmpeg (required by: video-processing, media-tools)

Install them and try again.
```
Return. Do not continue to Step 4.

### 4. Check Environment Variables
For each unique `env:Y`:
```bash
[ -n "${Y}" ]
```
Collect all that are unset or empty.

### 5. Report Missing Environment Variables
If any env vars are missing, report **all** with guidance and **continue** with installation:
```
Warning — missing environment variables:
- HUBSPOT_SERVICE_KEY (required by: hubspot) — set in .env or shell profile
- FIRECRAWL_API_KEY (required by: browser-automation) — set in .env or shell profile

Proceeding with installation. These components may not work correctly until the variables are set.
```
