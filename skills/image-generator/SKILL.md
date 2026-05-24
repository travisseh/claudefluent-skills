---
name: image-generator
description: Generate images from text prompts using OpenAI gpt-image-2 (primary) with Gemini fallback. Use whenever the user wants to create, make, or generate an image, hero banner, illustration, screenshot mockup, blog header, logo concept, or any visual asset. Also supports editing/remixing a reference image.
---

# Image Generator

Generates images via OpenAI's `gpt-image-2-2026-04-21` (primary) with Google Gemini `gemini-3-pro-image-preview` as fallback. Script and API keys live alongside this SKILL.md.

## How to run

```bash
cd ~/.claude/skills/image-generator && npx tsx generate-image.ts "<prompt>" [options]
```

By default images save to `./generated/` relative to cwd. Override with `--out <dir>` to write to the current project (pass an absolute path to avoid confusion).

## Options

- `--ratio <r>` — `1:1`, `16:9`, `9:16`, `3:4`, `4:3`, `21:9`, `2:3`, `3:2`, `4:5`, `5:4`. Aliases: `square`, `wide`, `ultrawide`, `tall`, `portrait`, `landscape`. Default `1:1`.
- `--res <1K|2K|4K>` — default `1K`. Maps to OpenAI quality: 1K=medium, 2K/4K=high.
- `--ref <file>` — reference image for editing/remixing.
- `--out <dir>` — output directory (default `./generated`).
- `--name <name>` — filename without extension (default: timestamp).
- `--provider <openai|gemini>` — force a specific provider. Default: tries OpenAI first, falls back to Gemini.

## Provider notes

- **OpenAI (gpt-image-2)** — supports ratios `1:1`, `16:9`, `9:16` only. Other ratios auto-fallback to Gemini.
- **Gemini** — supports all aspect ratios. Used as fallback when OpenAI is unavailable or doesn't support the requested ratio.

## Examples

```bash
# Hero banner (OpenAI primary)
cd ~/.claude/skills/image-generator && npx tsx generate-image.ts \
  "moody dark SaaS hero banner, abstract gradient mesh" \
  --ratio wide --res 2K \
  --out /Users/you/Programming/personal-master/personal/artifacts/image-generator \
  --name hero

# Force Gemini for unsupported ratio
cd ~/.claude/skills/image-generator && npx tsx generate-image.ts \
  "portrait photo style headshot" \
  --ratio 3:4 --provider gemini \
  --out /Users/you/Programming/personal-master/personal/artifacts/image-generator

# Edit a reference image
cd ~/.claude/skills/image-generator && npx tsx generate-image.ts \
  "make the background midnight blue and add soft bokeh" \
  --ref ./input.png --ratio wide
```

## Notes

- First run may need `npm i -g tsx` or install locally in the skill dir if tsx isn't available.
- If a provider declines a prompt, the script logs details so you can iterate.
- Per workspace convention, prefer writing output to `./artifacts/image-generator/` in the active project.
