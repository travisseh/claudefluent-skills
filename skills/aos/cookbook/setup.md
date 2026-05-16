# Setup — Guided Onboarding Wizard

## Context
One-command setup: detect workspace state, let the user choose a team/collection profile, bootstrap infrastructure via the workspace cookbook, and install components via `/aos-library use`. Pure orchestration — setup logic lives in the workspace cookbook, component logic in aos-library.

Can be run directly (`/aos`) or with a team pre-selected (`/aos setup builder`).

## Output Formatting Rules

Follow these formatting rules exactly for all output in this cookbook. This is the first impression for every new user.

1. **Section headers**: Use `─── name ───` padded to ~48 chars with trailing `─`
2. **Status bullets**: `✓` success, `●` exists/done, `○` pending/missing, `✗` failed, `⚠` warning
3. **Grouping**: `◆` for collection names, `▸` for actionable items
4. **Tree lines**: `├──` `└──` for hierarchical lists
5. **Progress bar**: `━` filled, total count at right: `━━━━━━━━━━ 7/7 installed`
6. **Commands**: always indented 4 spaces, left-aligned with description
7. **Tone**: concise, no filler. Each line earns its place.

## Steps

### Step 1 — Detect State

Check current workspace and component state. This is informational only — do NOT branch behavior based on state. All downstream steps are idempotent.

**Check workspace:** Read `.claude/CLAUDE.md` and look for the `# Workspace Conventions` sentinel line.

**Check components:** Scan `.claude/skills/`, `.claude/agents/`, `.claude/hooks/` for installed items.

**Output (fresh):**
```
─── aos setup ───────────────────────────────────

▸ Workspace     ○ not set up
▸ Components    ○ none installed

Starting fresh. I'll set up everything.
```

**Output (existing workspace):**
```
─── aos setup ───────────────────────────────────

▸ Workspace     ● set up
    ├── repos/aos
    ├── justfile
    └── .env

▸ Components    ● 4 installed
    ├── skill: interview-me
    ├── skill: research
    ├── hook: stop-notify
    └── hook: enforce-output-convention

Workspace already set up — skipping infrastructure.
```

### Step 2 — Team/Collection Selection

Read `~/.claude/skills/aos-library/library.yaml` — specifically the `teams` and `collections` sections.

**If a team name was passed as an argument** (e.g. `/aos builder`):
- Validate the name exists in `teams`. If valid, skip the selection UI and hold it for Step 4.
- If invalid, warn and fall through to show options.

**If no teams are defined in library.yaml**, show collections directly (same layout, collection names instead of team names).

**Output:**
```
─── choose a profile ───────────────────────────

  ❶  builder
     workflow + quality-of-life
     ▸ 4 skills   ▸ 3 hooks
     ─────────────────────────

  ❷  go-to-market
     workflow + quality-of-life + connectors + palantir
     ▸ 6 skills   ▸ 1 agent   ▸ 3 hooks
     ─────────────────────────

  ❸  custom — pick individual collections
  ❹  skip — just infrastructure, install components later

Which profile?
```

To build the component counts for each team: resolve teams → collections → items from library.yaml, and count items by type.

Wait for user selection. Hold it for Step 4.

### Step 3 — Workspace Setup

Read and execute [cookbook/workspace.md](workspace.md) — the workspace infrastructure cookbook.

**Output (after setup completes):**
```
─── workspace ──────────────────────────────────

  ✓ Cloned repos/aos
  ✓ Created archive/, artifacts/
  ✓ Wrote .env
  ✓ Copied justfile
  ✓ Wrote .claude/CLAUDE.md

Infrastructure ready.
```

**Output (already set up):**
```
─── workspace ──────────────────────────────────

  ● Already set up — skipping.
```

### Step 4 — Component Installation

Based on the user's selection from Step 2:

**If a team or collection was selected:** Delegate to `/aos-library use <team>` or `/aos-library use <collection>` — read and execute the library use cookbook.

**Output (running list as components install):**
```
─── installing builder ─────────────────────────

  ◆ workflow
    ✓ skill   interview-me
    ✓ skill   research
    ✓ skill   critical-thinking
    ✓ skill   systems-thinking

  ◆ quality-of-life
    ✓ hook   stop-notify
    ✓ hook   permission-notify
    ✓ hook   enforce-output-convention

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7/7 installed
```

**If "custom" was selected:** Show individual collections from library.yaml, let the user pick, then install each selected collection via `/aos-library use <collection>`.

**If "skip" was selected:**
```
─── components ─────────────────────────────────

  Skipped. Install anytime with:

    /aos-library use <name>       single component
    /aos-library use <collection> batch install
    /aos-library use <team>       full profile
    /aos-library list             browse catalog
```

### Step 5 — Orientation

Show a directory tree of what was installed, then the summary and next steps.

**Tree:** Scan the workspace root to discover what exists. Render as a tree using `├──` `└──` `│` characters, limited to 4 levels deep. Include both workspace infrastructure (repos, .env, justfile, archive) and installed components (.claude/ contents). Use `find . -maxdepth 4 | head -60` or equivalent to build the tree. Omit `.git/` directories and the `.ignore` file.

**Output:**
```
─── ready ──────────────────────────────────────

  ./
  ├── .claude/
  │   ├── CLAUDE.md
  │   ├── hooks/
  │   │   ├── enforce-output-convention.sh
  │   │   ├── permission-notify.sh
  │   │   └── stop-notify.sh
  │   ├── scripts/
  │   │   └── resolve-expertise.sh
  │   ├── settings.json
  │   └── skills/
  │       ├── critical-thinking/
  │       ├── interview-me/
  │       ├── research/
  │       └── systems-thinking/
  ├── .env
  ├── archive/
  │   └── manifest.yaml
  ├── artifacts/
  ├── justfile
  └── repos/
      └── aos/

  Setup complete. 7 components installed.

  ▸ /aos-library list            browse the full catalog
  ▸ /aos-library use <name>      install more anytime
  ▸ /aos-library use <team>      refresh a profile

────────────────────────────────────────────────
```

Adjust the tree and count to reflect what was actually installed. Show skill directories without expanding their contents (just the directory name). If "skip" was chosen, still show the infrastructure tree but say "Setup complete. Infrastructure ready." instead of a component count.
