---
name: example-skill
description: Replace this with a one-sentence trigger description for when the assistant should use this skill.
---

# Example Skill

Use this skill when the user asks for: describe the specific task, workflow, or outcome.

## Workflow

1. Confirm the relevant project, file, or source context.
2. Gather only the information needed for the task.
3. Make the smallest useful change or produce the requested artifact.
4. Verify the result.
5. Report what changed and any follow-up needed.

## Guardrails

- Do not include secrets, API keys, private account IDs, or private customer data.
- Prefer project-local conventions over generic advice.
- Keep generated output concise unless the user asks for detail.

## Optional Files

Add these only when useful:

- `scripts/`: repeatable commands or data-processing helpers.
- `references/`: longer examples, checklists, or source material.
- `templates/`: reusable output formats.
