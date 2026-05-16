---
name: sync-skills
description: "Sync skill directories between global Claude skills, global Codex/OpenAI skills, and repo-local skills in ExampleCo, product2, personal-master/personal, and gmr-marketing. Use when the user asks to sync skills, mirror Claude skills to OpenAI/Codex, mirror Codex/OpenAI skills to Claude, compare skill inventories, or keep repo skills aligned. Global roots are canonical; repo-local duplicates should be promoted to global and removed locally."
---

# Sync Skills

Use this skill to keep Claude and OpenAI/Codex skills aligned across global and repo-local skill directories.

Global roots are canonical. Repo-local skill roots are only for repo-specific skills that do not belong globally.

## Core Rule

Sync has two modes:

- Global sync is additive:
  - Copy missing skills and missing files between the global Claude and global Codex roots.
  - Update a destination file only when the source file is newer or the user explicitly asks to make one side match another.
- Local dedupe is promotive:
  - If a skill exists in both a global root and any repo-local root, treat the local copy as a duplicate.
  - Merge any newer local files into the global copies first.
  - After promotion, remove the duplicate repo-local skill directory.
  - Keep repo-local skills only when they are genuinely repo-specific and absent from both global roots.
- Never overwrite secrets with placeholders.
- Do not sync transient cache/plugin-generated skills unless the user explicitly asks.
- Preserve local-only additions when merging manually.

## Skill Roots

Global roots:

- Claude: `~/.claude/skills`
- OpenAI/Codex: `~/.codex/skills`

Repo roots to check:

- ExampleCo: `~/Programming/exampleco`
- product2: `~/Programming/product2`
- personal-master/personal: `~/Programming/personal-master/personal`
- gmr-marketing: `~/Programming/gmr-marketing`

If a canonical repo path is missing, search under `~/Programming` for that repo name, excluding hidden directories and cache/worktree folders.

Within each repo, look for:

- `.claude/skills`
- `.codex/skills`
- `.openai/skills`

## Inventory Command

Use this first to find available roots:

```bash
find ~/.claude/skills ~/.codex/skills \
  -maxdepth 2 -name SKILL.md -print 2>/dev/null

find ~/Programming -maxdepth 6 -type d \
  \( -path '*/.claude/skills' -o -path '*/.codex/skills' -o -path '*/.openai/skills' \) \
  \( -path '*/exampleco/*' -o -path '*/product2/*' -o -path '*/personal-master/personal/*' -o -path '*/gmr-marketing/*' \) \
  -print 2>/dev/null
```

## Global Sync + Local Dedupe Script

Run this when the user asks to sync. It first aligns the two global roots, then promotes duplicate repo-local skills into the global roots and removes the local duplicate directories. It does not delete global skills.

```bash
python3 - <<'PY'
from __future__ import annotations

import filecmp
import shutil
from pathlib import Path

GLOBAL_ROOTS = [
    Path("~/.claude/skills"),
    Path("~/.codex/skills"),
]
CANONICAL_REPOS = [
    Path("~/Programming/exampleco"),
    Path("~/Programming/product2"),
    Path("~/Programming/personal-master/personal"),
    Path("~/Programming/gmr-marketing"),
]
LOCAL_SKILL_DIRS = [".claude/skills", ".codex/skills", ".openai/skills"]


def repo_roots() -> list[Path]:
    roots: set[Path] = set()
    for repo in CANONICAL_REPOS:
        if repo.exists():
            roots.add(repo)
    return sorted(roots)


def global_roots() -> list[Path]:
    return [root for root in GLOBAL_ROOTS if root.exists()]


def local_skill_roots() -> list[Path]:
    roots: set[Path] = set()
    for repo in repo_roots():
        for rel in LOCAL_SKILL_DIRS:
            root = repo / rel
            if root.exists():
                roots.add(root)
    return sorted(roots)


def skill_dirs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.iterdir() if path.is_dir() and (path / "SKILL.md").exists())


def copy_additive(src_dir: Path, dst_dir: Path) -> list[str]:
    changes: list[str] = []
    for src in sorted(src_dir.rglob("*")):
        rel = src.relative_to(src_dir)
        dst = dst_dir / rel
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
            continue
        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            changes.append(f"added {dst}")
        elif not filecmp.cmp(src, dst, shallow=False) and src.stat().st_mtime > dst.stat().st_mtime:
            shutil.copy2(src, dst)
            changes.append(f"updated {dst} from newer {src}")
    return changes


globals = global_roots()
locals_ = local_skill_roots()

print("Global skill roots:")
for root in globals:
    print(f"- {root}")
print("\nRepo-local skill roots:")
for root in locals_:
    print(f"- {root}")

changes: list[str] = []
removed: list[str] = []

for src in globals:
    for dst in globals:
        if src == dst:
            continue
        for skill in skill_dirs(src):
            target = dst / skill.name
            target.mkdir(parents=True, exist_ok=True)
            changes.extend(copy_additive(skill, target))

global_names = {
    skill.name
    for root in globals
    for skill in skill_dirs(root)
}

local_by_name: dict[str, list[Path]] = {}
for root in locals_:
    for skill in skill_dirs(root):
        local_by_name.setdefault(skill.name, []).append(skill)

for name, sources in sorted(local_by_name.items()):
    if name in global_names:
        for src in sources:
            for dst_root in globals:
                target = dst_root / name
                target.mkdir(parents=True, exist_ok=True)
                changes.extend(copy_additive(src, target))
        for src in sources:
            shutil.rmtree(src)
            removed.append(str(src))
    else:
        for src in sources:
            for dst_root in globals:
                target = dst_root / name
                target.mkdir(parents=True, exist_ok=True)
                changes.extend(copy_additive(src, target))
                global_names.add(name)

print("\nPromoted or synced changes:")
if changes:
    for change in changes:
        print(f"- {change}")
else:
    print("- no file changes needed")

print("\nRemoved local duplicates:")
if removed:
    for path in removed:
        print(f"- {path}")
else:
    print("- no local duplicate skill directories removed")
PY
```

## Manual Merge Guidance

If two `SKILL.md` files have different useful content and neither should win wholesale:

1. Read both files.
2. Merge missing sections additively into the richer version.
3. Copy the merged file to both global destinations.
4. Keep secret references indirect, such as Keychain service names or env var names.
5. If the conflict came from a repo-local duplicate, delete that local skill directory after promotion.
6. Re-run `diff -u` on the two global files to confirm expected alignment.

## Useful Diff Commands

Compare global Claude and Codex skills by name:

```bash
comm -3 \
  <(find ~/.claude/skills -maxdepth 1 -mindepth 1 -type d -exec basename {} \; | sort) \
  <(find ~/.codex/skills -maxdepth 1 -mindepth 1 -type d -exec basename {} \; | sort)
```

Compare a specific global skill:

```bash
diff -u ~/.claude/skills/SKILL_NAME/SKILL.md ~/.codex/skills/SKILL_NAME/SKILL.md
```

Find repo-local duplicates that already exist globally:

```bash
python3 - <<'PY'
from pathlib import Path

globals_ = [
    Path("~/.claude/skills"),
    Path("~/.codex/skills"),
]
locals_ = [
    Path("~/Programming/exampleco/.claude/skills"),
    Path("~/Programming/product2/.claude/skills"),
    Path("~/Programming/product2/.codex/skills"),
    Path("~/Programming/personal-master/personal/.claude/skills"),
    Path("~/Programming/gmr-marketing/.claude/skills"),
    Path("~/Programming/gmr-marketing/.codex/skills"),
    Path("~/Programming/gmr-marketing/.openai/skills"),
]

global_names = {
    path.name
    for root in globals_
    if root.exists()
    for path in root.iterdir()
    if path.is_dir() and (path / "SKILL.md").exists()
}

for root in locals_:
    if not root.exists():
        continue
    dupes = sorted(
        path.name
        for path in root.iterdir()
        if path.is_dir() and (path / "SKILL.md").exists() and path.name in global_names
    )
    if dupes:
        print(root)
        for name in dupes:
            print(f"  - {name}")
PY
```

## After Syncing

- Report which roots were included.
- Report created or updated global skill names.
- Report which repo-local duplicate skill directories were removed.
- Call out conflicts that need human judgment.
- Do not commit anything unless the user explicitly asks.
