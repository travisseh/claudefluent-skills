---
name: notion-save-and-text
description: "Save the current AI-generated output to the Notion AI Output Library and text the user the resulting Notion URL. Use when the user says phrases like \"save this and text me the result\", \"save this to notion and text me\", \"notion-save and text me\", or asks for a durable Notion save plus iMessage/SMS follow-up."
---

# Notion Save And Text

Use this skill to combine two existing workflows:

1. Save the current AI output to Notion using the `notion-save` skill.
2. Text the user the resulting Notion URL using the `imessage` skill.

## Workflow

1. Identify the output to save.
   - Default to the most recent substantial answer or analysis in the current conversation.
   - If the target content is ambiguous, ask a concise clarification before saving.

2. Save to Notion.
   - Follow `~/Programming/personal-master/personal/.agents/skills/notion-save/SKILL.md`.
   - Use `node ~/.config/notion-tools/notion-ai.js create`.
   - Pick sensible metadata from the content:
     - Personal admin or household finance: `Area=Life Admin`, `Initiative=Admin`, `Type=Analysis` or `Notes`.
     - Business strategy/research: choose the matching area and initiative from the Notion Save schema.
   - Capture the returned Notion URL.

3. Text the URL to the user.
   - Follow `~/Programming/personal-master/personal/.agents/skills/imessage/SKILL.md`.
   - Use the user's phone number from contacts when available.
   - Default known number: `+18014337874`.
   - Message format:

```text
Saved to Notion: <url>
```

   - If a short title helps, use:

```text
Saved <title> to Notion: <url>
```

4. Confirm both actions.
   - Final response should include the clickable Notion URL and state that it was texted.
   - If either Notion save or text sending fails, report the failure plainly and include any successful artifact.

## Guardrails

- Do not use Notion MCP for the save; use the local Notion CLI.
- Do not send anything except the Notion link and a short label unless the user asks for extra context.
- Do not create a Life Backlog task; this workflow is for AI Output Library artifacts.
