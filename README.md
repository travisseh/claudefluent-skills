# ClaudeFluent Skills

Shareable Claude Code and Codex skills for ClaudeFluent students.

This repo is meant to be a clean public shelf for skills students can copy, inspect, modify, and use in their own projects. Each skill lives in its own folder under `skills/`.

## How To Use A Skill

Copy a skill folder into your local skills directory:

```bash
mkdir -p ~/.claude/skills
cp -R skills/example-skill ~/.claude/skills/example-skill
```

Then restart Claude Code or ask it to use the skill by name.

For Codex, copy the same folder into:

```bash
mkdir -p ~/.codex/skills
cp -R skills/example-skill ~/.codex/skills/example-skill
```

## Recommended Skill Shape

Use one folder per skill:

```text
skills/
  my-skill/
    SKILL.md
    scripts/
    references/
    templates/
```

Only `SKILL.md` is required. Add `scripts/`, `references/`, or `templates/` when they make the skill easier to reuse.

## What Makes A Good Student Skill

A good shareable skill is:

- Specific: it has a narrow job.
- Portable: it avoids private paths, secrets, and company-specific assumptions.
- Teachable: it explains the workflow clearly enough that a student can modify it.
- Executable: if there are repeated commands, put them in scripts instead of prose.

## Add A New Skill

1. Copy `skills/_template` to `skills/your-skill-name`.
2. Edit `SKILL.md`.
3. Remove private context, secrets, account IDs, and local machine paths.
4. Test the skill in a fresh project before sharing it with students.

## License

MIT. Students can use, copy, and modify these skills.
