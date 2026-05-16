---
name: cc-slides
description: >
  Manage ClaudeFluent course presentation slides stored in Convex — add, modify, delete, and reorder slides.
  Use this skill whenever the user asks to add slides to a presentation, update slide content, remove slides,
  add a new topic to the deck, or manage the ClaudeFluent course slides in any way. Also trigger when he mentions
  "presentation", "slides", "deck", "add a slide about", "update the slide on", or references a specific
  presentation by name or URL (e.g., "Claude Class - March 7"). When adding slides about a new topic, always
  research the topic first using WebSearch/WebFetch to get the latest information before creating content.
---

# CC-Slides: ClaudeFluent Presentation Manager

## Quick Reference

- **Working directory:** `~/Programming/personal-master/personal/claude_course/website`
- **Production Convex URL:** `https://polite-toad-76.convex.cloud`
- **Convex API imports:** `convex/browser` for `ConvexHttpClient`, `../convex/_generated/api` for `api`, `../convex/_generated/dataModel` for `Id`
- **Slide table:** `slidesV3` with fields: `order`, `slideId`, `contentJson` (Tiptap JSON), `contentHtml`, `presentationId`, `sideImageId`
- **Existing script with examples:** `scripts/add-march7-slides.ts`

## Workflow

### Step 1: Identify the Target Presentation

Use the ConvexHttpClient to query all presentations and find the right one:

```typescript
import { ConvexHttpClient } from "convex/browser";
import { api } from "../convex/_generated/api";
import { Id } from "../convex/_generated/dataModel";

const client = new ConvexHttpClient("https://polite-toad-76.convex.cloud");
const presentations = await client.query(api.presentations.getAll);
// Returns: [{_id, title, slideCount, theme, ...}]
```

**Important:** The local `npx convex run` command uses the dev deployment (`notable-peccary-161`), which has different data than production. Always use `ConvexHttpClient` pointed at `https://polite-toad-76.convex.cloud` to hit the real data.

If the user provides a URL like `/presentations/<id>`, extract the presentation ID from it. If they mention a presentation by name, search through `getAll` results. If unclear, default to the **most recently updated** presentation (first result from `getAll`, which is sorted by `updatedAt` desc).

### Step 2: Get Current Slides

```typescript
const slides = await client.query(api.slidesV3.getByPresentation, {
  presentationId: presentationId as Id<"presentations">
});
slides.sort((a, b) => a.order - b.order);
```

Print the slide list with order numbers and titles (extracted from HTML) so you can identify where to insert, modify, or delete.

### Step 3: Research the Topic (for new slides)

Before creating slide content about any topic, **always research it first** using WebSearch and/or WebFetch:
- Search for the latest announcements, docs, and blog posts
- Read the official documentation or GitHub README
- Get current syntax, commands, and features
- Note any recent changes or updates

This ensures slide content is accurate and up-to-date, not based on potentially stale training data.

### Step 4: Create Slide Content

See `references/tiptap-helpers.md` for the full Tiptap JSON helper reference.

Every slide needs both `contentJson` (Tiptap JSON — the primary storage) and `contentHtml` (generated HTML for rendering). The HTML should mirror the JSON structure exactly.

**Slide content guidelines:**
- Start with an `h1` title
- Include an `h3` subtitle when helpful
- Use `hr()` to create visual section breaks
- Include setup commands in `codeBlock()` format
- Add concrete use cases and examples
- Keep slides scannable — use bullet lists, not paragraphs

**Example prompt / use case pattern** — for topics involving tools or commands, include:
- The setup/install command
- A concrete example of using it
- When/why you'd use it vs alternatives

### Step 5: Insert the Slide

```typescript
// Add after a specific slide
const newId = await client.mutation(api.slidesV3.addSlide, {
  afterId: targetSlideId as Id<"slidesV3">,
  presentationId: presentationId as Id<"presentations">,
});

// Update with content
await client.mutation(api.slidesV3.updateContent, {
  id: newId,
  contentJson: contentJson,
  contentHtml: contentHtml,
});
```

### Step 6: Evaluate Exercise Impact

After inserting a new topic slide, scan the surrounding slides in that module section for exercises. Consider:
- Does this new topic render any existing exercise outdated or incomplete?
- Should the exercise be updated to incorporate this new tool/concept?
- Should a new exercise replace or supplement the existing one?

**Always ask the user** before modifying or replacing any exercise. Present your recommendation with reasoning.

## Available Convex APIs

### Queries
- `presentations.getAll` — List all presentations (sorted by updatedAt desc), includes slideCount
- `presentations.getById({id})` — Get single presentation
- `slidesV3.getByPresentation({presentationId})` — Get all slides for a presentation
- `slidesV3.getById({id})` — Get single slide
- `slidesV3.getAll()` — Get all slides (legacy, no presentation filter)

### Mutations
- `slidesV3.addSlide({afterId?, presentationId?})` — Add blank slide (after a specific slide or at end)
- `slidesV3.updateContent({id, contentJson, contentHtml})` — Update slide content
- `slidesV3.deleteSlide({id})` — Delete a slide
- `slidesV3.duplicate({id})` — Duplicate a slide right after original
- `slidesV3.reorder({orderedIds})` — Reorder slides by passing array of IDs in new order
- `slidesV3.setSideImage({id, storageId?})` — Set/remove side image
- `presentations.updateTheme({id, theme})` — Update presentation theme
- `presentations.setShareEnabled({id, enabled})` — Toggle sharing

## Modifying Existing Slides

To modify a slide's content, read the current slide first, then update:

```typescript
const slide = await client.query(api.slidesV3.getById, { id: slideId });
// Modify slide.contentJson and regenerate contentHtml
await client.mutation(api.slidesV3.updateContent, {
  id: slideId,
  contentJson: modifiedJson,
  contentHtml: modifiedHtml,
});
```

## Deleting Slides

```typescript
await client.mutation(api.slidesV3.deleteSlide, {
  id: slideId as Id<"slidesV3">
});
```

## Looking Up Participant Data (for personalized slides)

When the user references a student by name, query their onboarding data to personalize slide content:

```typescript
// Get all participants and find by name
const allParticipants = await client.query(api.participants.getAll);
const participant = allParticipants.find(p => p.name?.toLowerCase().includes("firstname"));

// Get their onboarding responses (goals, project, tech experience)
if (participant) {
  const onboarding = await client.query(api.onboarding.getByParticipant, {
    participantId: participant._id
  });
  // onboarding.broadGoals — career goals
  // onboarding.specificProject — what they want to build
  // onboarding.usedCodeEditor / usedTerminal / usedGithub / usedVercel — tech experience
  // onboarding.chatHistory — full conversation transcript (has the most detail)
}
```

**Available Convex APIs for participants:**
- `participants.getAll` — All participants
- `participants.getByEmail({email})` — Find by email
- `participants.getBySessionId({sessionId})` — All participants in a session (e.g., "saturday6")
- `onboarding.getByParticipant({participantId})` — Onboarding responses for a participant
- `onboarding.getAllWithParticipants()` — All onboarding responses joined with participant data

## HTML Embeds (interactive mini-apps)

Slides can include a full-width `htmlEmbed` block that renders a
sandboxed iframe — useful for interactive demos, visualizations, or any
self-contained mini-app. The node is a top-level block (not allowed
inside column layouts).

Shape in `contentJson`:

```typescript
{ type: "htmlEmbed", attrs: { mode: "srcdoc", html, url: "", height: "70vh" } }
// or: { mode: "url", html: "", url: "https://…", height: "70vh" }
```

The matching `contentHtml` wraps an `<iframe>` in a `div[data-type="html-embed"]`
with data-* attributes that round-trip the authoring state. Srcdoc mode
applies a no-same-origin sandbox; URL mode does not. See
`references/tiptap-helpers.md` for the helper functions (`htmlEmbedSrcdoc`,
`htmlEmbedUrl`, `htmlEmbedHtml`) that produce both sides correctly,
plus authoring rules for the HTML you put inside.

## Writing the Script

For any slide operation, write a TypeScript script in the `scripts/` directory and run it with `npx tsx scripts/<name>.ts`. This gives you type safety from the Convex generated types. See `scripts/add-march7-slides.ts` for a complete working example.
