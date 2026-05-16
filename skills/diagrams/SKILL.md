---
name: diagrams
description: "Generate professional diagrams using draw.io (mxGraphModel XML) with export to SVG, PNG, or PDF. Use this skill whenever the user wants to visualize architecture, create flowcharts, draw state machines, map out sequences, build ER diagrams, design system diagrams, create org charts, wireframes, or any visual representation of systems, code, data, or processes. Also trigger when they say 'diagram this', 'draw a flow', 'visualize', 'map out', 'show me how this works', 'diagram the codebase', 'architecture diagram', or want any kind of diagram. Can analyze codebases to auto-generate architecture diagrams. Can embed diagrams in ClaudeFluent presentation slides. Triggers on: diagram, flowchart, visualize, draw, map out, sequence diagram, ER diagram, class diagram, state machine, architecture diagram, data flow, codebase diagram, org chart, wireframe, system design, draw.io."
---

# Diagrams Skill

Generate professional, presentation-quality diagrams using draw.io's native mxGraphModel XML format. Exports to SVG, PNG, or PDF via the draw.io desktop CLI.

## Prerequisites

- **draw.io desktop app** must be installed at `/Applications/draw.io.app/Contents/MacOS/draw.io`
- If not installed: `brew install --cask drawio`

## When to Use

- User asks to "diagram", "visualize", "draw", or "map out" something
- Architecture diagrams, data flows, system designs
- Sequence diagrams for API flows
- ER diagrams for database schemas
- Org charts, wireframes, UI sketches
- Any time a visual would clarify a concept

## Workflow

### Step 1: Understand What to Diagram

If the user wants a codebase architecture diagram, analyze the code first:
1. Use Glob to find key files (entry points, routes, config, schema files)
2. Use Grep to trace imports, exports, and dependencies
3. Identify the main layers: UI, API, Services, Database
4. Note key external integrations

### Step 2: Generate draw.io XML

Write a `.drawio` file containing valid mxGraphModel XML. Every diagram must include:

```xml
<mxfile>
  <diagram name="Diagram Name" id="d1">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1000">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- diagram content here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Step 3: Export and Open

```bash
# Export to SVG (default)
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f svg -b 10 -o output.svg input.drawio

# Export to PNG
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -b 10 --scale 2 -o output.png input.drawio

# Export to PDF
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f pdf -b 10 -o output.pdf input.drawio

# Open result
open output.svg
```

Export flags: `-x` (export), `-f` (format), `-b` (border px), `--scale` (for PNG resolution), `-t` (transparent bg), `--embed-diagram` (embed XML in export for re-editing).

### Step 4: Save to Project (Optional)

If the user wants to keep it, save both the `.drawio` source and the exported file to the project (e.g., `docs/architecture.drawio` + `docs/architecture.svg`).

## XML Reference

### Cell Attributes

| Attribute | Purpose |
|-----------|---------|
| `id` | Unique identifier (required) |
| `value` | Display label (use `&#xa;` for newlines) |
| `style` | Visual properties (semicolon-separated) |
| `vertex="1"` | Marks as shape |
| `edge="1"` | Marks as connector |
| `parent` | Container/layer reference |
| `source`, `target` | Edge endpoints |

### Common Styles

**Shapes:**
```
rounded=1;fillColor=#292e42;strokeColor=#3d59a1;fontColor=#c0caf5;fontSize=11;whiteSpace=wrap;
```

**Database cylinder:**
```
shape=cylinder3;fillColor=#292e42;strokeColor=#9ece6a;fontColor=#c0caf5;fontSize=10;whiteSpace=wrap;size=8;
```

**Container/swimlane:**
```
swimlane;startSize=30;fillColor=#1a1a2e;strokeColor=#4a4a6a;fontColor=#e2e8f0;rounded=1;fontSize=14;fontStyle=1;swimlaneLine=0;container=1;collapsible=0;whiteSpace=wrap;
```

**Diamond (decision):**
```
rhombus;fillColor=#292e42;strokeColor=#ff9e64;fontColor=#c0caf5;whiteSpace=wrap;
```

**Edges:**
```
edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#565f89;fontColor=#565f89;fontSize=9;
```

**Dashed edge:**
```
edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#ff9e64;dashed=1;
```

### Critical Rules

1. **Every edge MUST have an mxGeometry child** — self-closing edge cells fail to render:
   ```xml
   <mxCell id="e1" edge="1" parent="1" source="a" target="b" value="label">
     <mxGeometry relative="1" as="geometry"/>
   </mxCell>
   ```

2. **Never include XML comments** (`<!-- -->`) — they can cause rendering issues

3. **Escape special characters**: `&amp;`, `&lt;`, `&gt;`, `&quot;`

4. **Use `&#xa;` for newlines** in labels, not `\n`

5. **Root cells id="0" and id="1"** are always required

6. **All IDs must be unique** across the entire diagram

### Container Pattern

Group related items using swimlane containers:

```xml
<mxCell id="group1" value="Group Title" style="swimlane;startSize=24;fillColor=#16213e;strokeColor=#3d59a1;fontColor=#7aa2f7;rounded=1;container=1;collapsible=0;" vertex="1" parent="1">
  <mxGeometry x="20" y="50" width="340" height="280" as="geometry"/>
</mxCell>
<mxCell id="child1" value="Item" style="rounded=1;fillColor=#292e42;strokeColor=#3d59a1;fontColor=#c0caf5;" vertex="1" parent="group1">
  <mxGeometry x="20" y="40" width="140" height="36" as="geometry"/>
</mxCell>
```

Children use coordinates **relative to the parent container**.

### Edge Connection Points

Control where edges connect using `exitX`/`exitY` and `entryX`/`entryY` (values 0-1):
- Top center: `exitX=0.5;exitY=0`
- Bottom center: `exitX=0.5;exitY=1`
- Left center: `exitX=0;exitY=0.5`
- Right center: `exitX=1;exitY=0.5`
- Top-right quarter: `entryX=0.75;entryY=0`
- Top-left quarter: `entryX=0.25;entryY=0`
- Bottom-right quarter: `exitX=0.75;exitY=1`
- Bottom-left quarter: `exitX=0.25;exitY=1`

### Preventing Arrow Overlaps (CRITICAL)

**Never let two edges connect to the same point on a node.** When multiple edges touch the same node, each must use a distinct `exitX/exitY` or `entryX/entryY` value. This is the most common visual bug in generated diagrams.

**Pattern: Request/response pairs between columns (e.g., Agent → DB → next Agent step)**

When node A sends to node B, and node B's result feeds into node C below A, use this pattern:
- **Forward arrow** (A → B): `exitX=1;exitY=0.5` → `entryX=0;entryY=0.5` (straight horizontal)
- **Return arrow** (B → C): `exitX=0.5;exitY=1` → `entryX=0.75;entryY=0` (loops down and back)

This creates a clean visual separation — forward arrows go horizontal, return arrows loop underneath.

```xml
<!-- Forward: Agent calls DB (horizontal right) -->
<mxCell id="fwd1" edge="1" source="agent1" target="db1"
  style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#9ece6a;
         exitX=1;exitY=0.5;exitDx=0;exitDy=0;
         entryX=0;entryY=0.5;entryDx=0;entryDy=0;">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- Return: DB result feeds next Agent step (loops down-and-back) -->
<mxCell id="ret1" edge="1" source="db1" target="agent2"
  style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#bb9af7;
         exitX=0.5;exitY=1;exitDx=0;exitDy=0;
         entryX=0.75;entryY=0;entryDx=0;entryDy=0;">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="640" y="175"/>
      <mxPoint x="400" y="175"/>
    </Array>
  </mxGeometry>
</mxCell>
```

**General rules for multi-edge nodes:**
- If a node has both an incoming edge from the left and a return edge from the right, use `entryX=0;entryY=0.5` for the left one and `entryX=0.75;entryY=0` (top-right) for the return
- If a node has both an outgoing edge to the right and a downward edge, use `exitX=1;exitY=0.5` for the right one and `exitX=0.5;exitY=1` for the downward one
- For three or more edges on one side, spread them across 0.25, 0.5, 0.75 increments
- Always use explicit `exitX/exitY/entryX/entryY` on edges — never rely on auto-routing when a node has 2+ connections

## Dark Theme Color Palette

Use this palette for consistent, presentation-quality dark diagrams:

| Purpose | Color |
|---------|-------|
| Background | `#1a1a2e` |
| Surface/fill | `#292e42` |
| Text | `#c0caf5` |
| Heading text | `#e2e8f0` |
| Muted text | `#565f89` |
| Blue accent | `#7aa2f7` / `#3d59a1` |
| Green accent | `#9ece6a` / `#3d8a5a` |
| Purple accent | `#bb9af7` / `#9d7cd8` |
| Red accent | `#f7768e` |
| Orange accent | `#ff9e64` |
| Teal accent | `#73daca` |

Use different accent colors to visually group related sections (e.g., blue for frontend, green for backend, orange for external services).

## Embedding in ClaudeFluent Presentations

Slides use `contentHtml` with `dangerouslySetInnerHTML`, so exported SVGs can be embedded directly:

1. Export the diagram to SVG
2. Read the SVG file contents
3. Use the `cc-slides` skill to update the target slide's `contentHtml`
4. Wrap in a container:

```html
<div style="display:flex;justify-content:center;align-items:center;padding:2rem;">
  <!-- SVG content here -->
</div>
```

For transparent backgrounds, use the `-t` flag when exporting: `-x -f svg -b 10 -t`

## Layout Best Practices

- Space nodes generously (200px horizontal, 120px vertical minimum)
- Leave 20px+ straight segments before arrowheads
- Align to 10px grid
- Use containers/swimlanes to group related items — don't just scatter nodes
- Keep labels short — use `&#xa;` for two-line labels
- Start with high-level view (5-10 nodes max), drill into subsystems on request
- Use consistent colors within a group, different colors across groups
- One clean edge per relationship — don't duplicate arrows
- **No overlapping arrows** — when two+ edges connect to the same node, each MUST use a different `exitX/exitY` or `entryX/entryY` value (see "Preventing Arrow Overlaps" above)

## Diagram Types

| Type | Best For | Key Shapes |
|------|----------|------------|
| Architecture | System overview | Swimlanes, rounded rects, cylinders |
| Flowchart | Business processes | Rounded rects, diamonds, arrows |
| ER Diagram | Database schema | Cylinders, labeled edges |
| Sequence | API flows | Vertical lifelines, horizontal arrows |
| Org Chart | Team structure | Rounded rects, tree layout |
| State Machine | State transitions | Rounded rects, labeled edges, start/end circles |

## Error Handling

- If draw.io CLI is not found, prompt user to install: `brew install --cask drawio`
- If export fails, open the `.drawio` file directly for manual export: `open file.drawio`
- For very complex diagrams, build incrementally — generate a section, verify, then expand
