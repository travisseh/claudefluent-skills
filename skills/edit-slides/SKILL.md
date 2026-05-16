---
name: edit-slides
description: "Edit presentation slides in the presentations app via npx convex run --prod. Use when listing presentations, inspecting slide content, inserting slides, updating slides, or deleting slides from the ClaudeFluent deck."
---

# Edit Presentation Slides via CLI

Edit slides in the presentations app directly from Claude Code using `npx convex run --prod`.

**Important:** Always use the `--prod` flag. Without it, Convex targets the dev deployment which has different data.

## List All Presentations

```bash
npx convex run --prod presentations:getAll '{}'
```

## List Slides in a Presentation

Save slides to a file first (output is too large to pipe):

```bash
npx convex run --prod slidesV3:getByPresentation '{"presentationId": "PRESENTATION_ID"}' > /tmp/slides.json
```

Then list with titles:

```bash
python3 /tmp/list_slides.py < /tmp/slides.json
```

Helper script at `/tmp/list_slides.py`:
```python
import json, sys
slides = json.load(sys.stdin)
slides.sort(key=lambda s: s['order'])
for i, s in enumerate(slides):
    title = '(no title)'
    cj = s.get('contentJson', {})
    if cj and 'content' in cj:
        for node in cj['content']:
            if node.get('type') in ('heading', 'paragraph') and node.get('content'):
                for t in node['content']:
                    if t.get('text', '').strip():
                        title = t['text'][:50]
                        break
                if title != '(no title)':
                    break
    print(f"  {i+1:3d}. [{s['order']:3d}] {s['_id']} | {title}")
```

## Read a Specific Slide's Content

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

## Insert a New Slide After an Existing One

1. Insert a blank slide after a given slide ID:
```bash
npx convex run --prod slidesV3:addSlide '{"afterId": "SLIDE_ID", "presentationId": "PRESENTATION_ID"}'
```
This returns the new slide's ID and automatically bumps the order of all subsequent slides.

2. Update the new slide's content:
```bash
npx convex run --prod slidesV3:updateContent '$(cat /tmp/update_slide.json)'
```

Write the update payload to a JSON file first since it's usually too large for inline args:
```json
{
  "id": "NEW_SLIDE_ID",
  "contentJson": { ... },
  "contentHtml": "..."
}
```

## Update an Existing Slide's Content

Same as step 2 above - use `updateContent` with the slide's ID.

## Delete a Slide

```bash
npx convex run --prod slidesV3:deleteSlide '{"id": "SLIDE_ID"}'
```

## Tiptap JSON Format Reference

Slides use Tiptap/ProseMirror JSON. Common node types:

- **Heading**: `{"type": "heading", "attrs": {"level": 1}, "content": [{"type": "text", "text": "Title"}]}`
- **Paragraph**: `{"type": "paragraph", "content": [{"type": "text", "text": "Hello"}]}`
- **Bold text**: `{"type": "text", "marks": [{"type": "bold"}], "text": "bold"}`
- **Inline code**: `{"type": "text", "marks": [{"type": "code"}], "text": "code"}`
- **Code block**: `{"type": "codeBlock", "attrs": {"language": null}, "content": [{"type": "text", "text": "code here"}]}`
- **Ordered list**: `{"type": "orderedList", "attrs": {"start": 1}, "content": [{"type": "listItem", "content": [{"type": "paragraph", "content": [...]}]}]}`
- **Bullet list**: `{"type": "bulletList", "content": [{"type": "listItem", ...}]}`
- **Table**: See table section below

The `contentHtml` field should be the HTML rendering of the JSON. Keep them in sync.

## Tables

Table cells use `tableHeader` (for header row) or `tableCell` (for data rows):

```json
{"type": "tableHeader", "attrs": {"colspan": 1, "colwidth": null, "rowspan": 1},
 "content": [{"type": "paragraph", "content": [{"type": "text", "marks": [{"type": "bold"}], "text": "Header"}]}]}
```

**IMPORTANT: Never use empty text nodes with marks.** Tiptap will silently fail to render the entire slide. For an empty cell, use an empty paragraph with no content array:

```json
// WRONG - breaks the whole slide:
{"type": "paragraph", "content": [{"type": "text", "marks": [{"type": "bold"}], "text": ""}]}

// CORRECT - empty cell:
{"type": "paragraph"}
```

This applies to any cell or paragraph — if the text is empty, omit the content array entirely rather than including a text node with `"text": ""`.

## Key Presentation IDs (CC Course)

- **CC - Simplified**: `jh77fnmn1gm6zkpbwghkwz3qgn8147sr`
- **Master Claude Code**: `jh7f66pe23ytnzq0pzszbzdg4581489q`
- **Claude Class - Feb 25 & 26**: `jh75abzbje56jam37gwxapvv9581tpqa`
- **CC - Generalized Prompts**: `jh71g2kmwq7syzvhsy6rpndyhh81kang`
