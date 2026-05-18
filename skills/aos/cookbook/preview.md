# Preview — Show Target State for Setup

## Context
Read-only preview of what `/aos workspace` would create. Shows the infrastructure that would be set up (repos, directories, templates). **No files are created, cloned, or modified.**

Component installation (skills, plugins, MCP servers) is handled by the aos-library skill — use `/aos-library list` to see available components.

## Action Vocabulary

Use these tags consistently throughout the tree output:

| Tag | Meaning |
|-----|---------|
| `[create]` | Created with static or minimal content (not from a template) |
| `[write]` | Generated from a template or composed from resolved data |
| `[copy from aos]` | Copied verbatim from the aos directory |
| `[clone]` | `git clone` into the workspace |

## Steps

### 1. Read Workspace Configuration
- Read `workspace.yaml` (colocated with this skill)

### 2. Resolve Repos
For each repo in `workspace.yaml` `repos` section:
- Determine target directory: if the repo has a `default_dir` field, use it; otherwise use `<default_dirs.repos.default><repo-name>/`
- Record: name, target directory

### 3. Discover Assets
Enumerate files that setup copies from aos into the workspace.

List the contents of these directories relative to the aos root (two levels up from this cookbook file):
- **`templates/`** — each file maps to the workspace root. Mapping rules:
  - `CLAUDE.md` → `.claude/CLAUDE.md` with action `[write]`
  - All other files → `./<filename>` with action `[copy from aos]`
- **`scripts/`** — each file maps to `.claude/scripts/<filename>` with action `[copy from aos]`

### 4. Assemble Target State
Build the complete file/directory list:

**Always-created items** (every setup produces these):
- `.claude/CLAUDE.md` — `[write]`
- `.claude/scripts/<each script file>` — `[copy from aos]`
- `.env` — `[create]`
- `.ignore` — `[create]`
- `archive/manifest.yaml` — `[create]`
- `artifacts/` — `[create]`
- `justfile` — `[copy from aos]`

**Repos:**
- `repos/<name>/` — `[clone]` (one per repo)

### 5. Render the Preview Tree
Output the assembled target state using box-drawing tree characters (`├──`, `└──`, `│`).

**Ordering rules:**
- Directories before files at each level
- Alphabetical within directories, alphabetical within files
- Directories end with `/`

**Action tags** appear in square brackets, right-aligned for readability.

**Format:**
```
Workspace Preview

./
├── .claude/
│   ├── CLAUDE.md                         [write]
│   └── scripts/
│       └── <script-name>.sh             [copy from aos]
├── .env                                  [create]
├── .ignore                               [create]
├── archive/
│   └── manifest.yaml                     [create]
├── artifacts/                            [create]
├── justfile                              [copy from aos]
└── repos/
    ├── <repo-name>/                      [clone]
    └── <repo-name>/                      [clone]
```

**After the tree**, add a footer:
```
To install components after setup, run:
  /aos-library list          — see available skills, plugins, MCP servers
  /aos-library use <name>    — install a component, collection, or team
```
