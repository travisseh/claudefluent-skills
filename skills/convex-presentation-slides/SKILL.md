---
name: convex-presentation-slides
description: Edit and manage presentation slides through Convex production functions. Use when Codex needs to list presentations, inspect slide order/content, or insert/update/delete slides in the presentations app via `npx convex run --prod`.
---

# Convex Presentation Slides

Use this workflow to edit slides directly in the presentations app backend.

## Non-Negotiable Rule

Always run Convex commands with `--prod`.

Do not omit `--prod`. The default dev deployment contains different data.

## Core Workflow

### 1) List presentations

```bash
npx convex run --prod presentations:getAll '{}'
```

### 2) Fetch slides for one presentation

Write output to a file because payload size is large:

```bash
npx convex run --prod slidesV3:getByPresentation '{"presentationId":"PRESENTATION_ID"}' > /tmp/slides.json
```

### 3) List slide IDs, order, and inferred titles

```bash
python3 scripts/list_slides.py /tmp/slides.json
```

or

```bash
python3 scripts/list_slides.py < /tmp/slides.json
```

### 4) Inspect one slide's `contentJson`

```bash
python3 -c "
import json
with open('/tmp/slides.json') as f:
    slides = json.load(f)
for s in slides:
    if s['order'] == SLIDE_ORDER:
        print(json.dumps(s['contentJson'], indent=2))
        break
"
```

## Edit Operations

### Update existing slide

Prepare payload in `/tmp/update_slide.json`:

```json
{
  "id": "SLIDE_ID",
  "contentJson": {},
  "contentHtml": ""
}
```

Apply update:

```bash
npx convex run --prod slidesV3:updateContent '$(cat /tmp/update_slide.json)'
```

Keep `contentJson` and `contentHtml` synchronized.

### Insert new slide after existing slide

Create blank slide:

```bash
npx convex run --prod slidesV3:addSlide '{"afterId":"SLIDE_ID","presentationId":"PRESENTATION_ID"}'
```

Then update the returned new slide ID with `slidesV3:updateContent`.

### Delete slide

```bash
npx convex run --prod slidesV3:deleteSlide '{"id":"SLIDE_ID"}'
```

## Tiptap JSON Quick Reference

Use these common node shapes in `contentJson`.

Heading:

```json
{"type":"heading","attrs":{"level":1},"content":[{"type":"text","text":"Title"}]}
```

Paragraph:

```json
{"type":"paragraph","content":[{"type":"text","text":"Hello"}]}
```

Bold text:

```json
{"type":"text","marks":[{"type":"bold"}],"text":"bold"}
```

Inline code:

```json
{"type":"text","marks":[{"type":"code"}],"text":"code"}
```

Code block:

```json
{"type":"codeBlock","attrs":{"language":null},"content":[{"type":"text","text":"code here"}]}
```

Ordered list:

```json
{"type":"orderedList","attrs":{"start":1},"content":[{"type":"listItem","content":[{"type":"paragraph","content":[]}]}]}
```

Bullet list:

```json
{"type":"bulletList","content":[{"type":"listItem","content":[{"type":"paragraph","content":[]}]}]}
```

## Known Presentation IDs (CC Course)

- `CC - Simplified`: `jh77fnmn1gm6zkpbwghkwz3qgn8147sr`
- `Master Claude Code`: `jh7f66pe23ytnzq0pzszbzdg4581489q`
