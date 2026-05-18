---
name: add-cf-skills
description: Publish an existing local skill to the public ClaudeFluent skills repo. Use when Travisse asks to share, publish, add, or upload a skill for ClaudeFluent students.
---

# Add ClaudeFluent Skills

Use this skill to publish an existing local skill into the public ClaudeFluent Skills repo.

## Command

Run:

```bash
/Users/you/.claude/scripts/add-to-cf-skills.sh "<skill-name-or-path>"
```

The argument can be:

- a global skill name, such as `front-end`
- a path to a skill folder containing `SKILL.md`
- a path to a standalone `.md` skill file

## What The Script Does

- Resolves the source skill from common Claude and Codex skill roots.
- Copies it into `/Users/you/Programming/claudefluent-skills/skills/<skill-name>` as the public staging copy.
- Removes common junk and private artifacts from that copied public version.
- Scans the copied public version for likely sensitive content.
- Stages, commits, and pushes to `https://github.com/travisseh/claudefluent-skills`.

## Sensitive Content Review

If the script prints `REVIEW_REQUIRED`, inspect and sanitize only the copied files under:

```text
/Users/you/Programming/claudefluent-skills/skills/<skill-name>
```

Do **not** sanitize or simplify the source skill in `~/.codex/skills`, `~/.claude/skills`, or the repo-local skill tree unless Travisse explicitly asks to change the source too.

After reviewing the copied public version, rerun with:

```bash
CF_SKILLS_FORCE=1 /Users/you/.claude/scripts/add-to-cf-skills.sh "<skill-name-or-path>"
```

When `CF_SKILLS_FORCE=1` is set and the copied public version already exists, the script reuses that sanitized copy instead of recopying from the source skill. Only use `CF_SKILLS_FORCE=1` after removing or intentionally accepting the flagged content in the copied public version.

## Final Response

Report the published GitHub URL:

```text
https://github.com/travisseh/claudefluent-skills/tree/main/skills/<skill-name>
```
