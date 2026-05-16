---
name: article-writer
description: "Write opinionated Claude Code articles for ClaudeFluent. Use this skill whenever writing comparison pieces, hot takes, tool reviews, trend commentary, opinion pieces, or anything timely about Claude Code or AI coding tools. Also trigger when the user asks to compare tools (X vs Y), write a blog post, create content about a new feature release, or draft thought leadership content for ClaudeFluent. Triggers on: write an article, new article about, compare X vs Y, blog post, opinion piece, hot take, tool review, trend piece, ClaudeFluent content."
---

# Article Writer

Create timely, opinionated content for ClaudeFluent. Articles take a strong stance, may reference current events or new tool releases, and have a shelf life (may need `dateModified` updates as tools evolve).

Examples: comparison pieces (X vs Claude Code), hot takes on trends, tool reviews, industry commentary, "why the consensus is wrong" pieces.

## Audience

Read `.claude/skills/guide-writer/references/personas.md` for full persona details.

**Primary targets:**
- **Derek** (Solo Founder): Vets everything. Wants practitioner credibility, not corporate polish. Articles should feel like reading a smart friend's take, not a blog post.
- **Ashley** (Dir PMM): Team leader wondering if this is worth investing in. Wants evidence and clear reasoning, not hype.

**Secondary:**
- **Priya** (Senior PM): Time-starved, needs the bottom line fast.
- **Sandra** (VP CS): Needs business case framing she can share internally.

## Article Angle

Every article needs these elements:

- **A clear thesis.** State it in the first 2 paragraphs. Example: "Claude Code is better for 99% of people."
- **Contrarian when possible.** "The consensus says X, here's why that's wrong." Challenge popular assumptions with evidence.
- **Pick a side with reasoning.** Be fair to competitors but don't be neutral. Show your work.
- **Address the content ecosystem honestly.** When relevant, call out who benefits from complexity, hype, or confusion (influencers, content creators, vendors).
- **Include a "who should actually use [competitor]" section.** This builds credibility. Acknowledging where competitors win makes your argument stronger.

## Content Principles

- Every section answers "so what?" or "what does this mean for me?"
- Real examples from teaching 100+ students and building real products
- Opinionated: take a stance, don't hedge
- If a paragraph doesn't advance the argument, cut it
- Show, don't tell. Specific numbers, specific tools, specific outcomes.
- Use first-person authority: "I've used both extensively..."

## Writing Style

Reference the `travisse-writing-style` skill for full Voice DNA (see Long-Form Articles section). Key rules inline:

### Formatting
- Short paragraphs (1-2 sentences default, 3 max)
- Numbers as digits
- Contractions always
- NO em dashes ever. Use commas, periods, colons, semicolons, or parentheses.
- Bold sparingly, 1-2 key moments per section
- Code blocks for specific prompts, commands, or tool outputs
- Use physical verbs: "bolted on" not "added", "stripped back" not "simplified", "sanded down" not "improved"
- Parenthetical asides for editorial commentary and honest reactions

### Banned Phrases (FATAL: if any appear, the output fails)
- "Delve" / "Dive into" / "Unpack"
- "Harness" / "Leverage" / "Utilize" / "Robust"
- "Game-changer" / "Cutting-edge" / "Straightforward"
- "In today's [anything]..."
- "It's important to note..." / "It's worth noting..."
- "Furthermore" / "Additionally" / "Moreover"
- "Supercharge" / "Unlock" / "Future-proof"
- "10x your productivity"
- "The AI revolution" / "In the age of AI"
- "Here's the part nobody's talking about" / "What nobody tells you"
- "This changes everything" / "Let that sink in" / "Read that again"
- **THE BIG ONE:** "This isn't X. This is Y." and ALL variations ("Not X. Y.", "Forget X. This is Y.", "Less X, more Y."). ANY sentence that negates one framing then asserts a corrected one. Delete the negation, just state the positive claim.

## SEO Requirements

- Target keyword in title, meta title, and first paragraph
- `metaTitle` < 60 characters
- `metaDescription` < 160 characters, punchier and more opinionated than a guide's
- 2-3 internal links to other guides using `<a href="/guides/[slug]">text</a>`
- CTA to ClaudeFluent course at the bottom
- `relatedGuides` array with 2-3 slugs from existing content
- Existing slugs: `google-search-console`, `what-is-vibe-coding`, `claude-code-vs-cursor`, `what-is-claude-code`, `ai-for-product-managers`, `how-to-use-claude-code`, `claude-code-mcp-servers`, `claude-code-agents`, `claude-code-plan-mode`, `claude-code-skills`, `codex-vs-claude-code`, `claude-code-best-practices`, `claude-code-tutorial`, `claude-code-setup`, `openclaw-vs-claude-code`

## Quality Gates

Before delivering, verify ALL of these:

- [ ] Unique intent (no other article covers this exact angle)
- [ ] 600+ words of substantive content
- [ ] Clear thesis stated in first 2 paragraphs
- [ ] No banned phrases, no em dashes in prose
- [ ] 2+ concrete examples, comparisons, or evidence points
- [ ] Internal links to 2-3 other guides
- [ ] CTA at bottom linking to ClaudeFluent homepage or course
- [ ] Both `Content()` JSX and `markdown` string present
- [ ] TypeScript compiles clean (`npx tsc --noEmit`)
- [ ] `metaTitle` < 60 chars, `metaDescription` < 160 chars
- [ ] First paragraph contains target keyword

## Technical Wiring (6 steps)

Articles use the exact same file format and registration as guides.

### Step 1: Create the content file
Create `claude_course/website/lib/guides/content/[slug].tsx` using the template at `references/article-template.tsx`.

### Step 2: Register in guides index
Add import and entry to `claude_course/website/lib/guides/index.ts`:
```typescript
import { guide as yourArticle } from "./content/[slug]";
// Add to the guides array:
const guides: Guide[] = [
  // ... existing guides
  yourArticle,
];
```

### Step 3: Add slug to SEO config
Add the slug string to the `GUIDE_SLUGS` array in `claude_course/website/lib/seo-config.ts`.

### Step 4: (Optional) Add card to free-resources page
If the article should be discoverable from the resources page, add a card to `claude_course/website/app/free-resources/page.tsx`. Note: guide cards are currently hidden behind `{false && <>...</>}`.

### Step 5: Update LLM discovery files
Add a new bullet to the `## Guides` section in both:
- `claude_course/website/public/llms.txt`
- `claude_course/website/public/llms-full.txt`

Format: `- [Article Title](https://claudefluent.com/guides/[slug]) - Brief description`

### Step 6: Verify
Run `npx tsc --noEmit` from `claude_course/website/` to confirm TypeScript compiles. Then `npx next build` to confirm the full build passes.

## Guide Interface (TypeScript reference)

Articles use the same `Guide` interface as guides:

```typescript
export interface Guide {
  slug: string;           // URL-safe slug, e.g. "windsurf-vs-claude-code"
  title: string;          // Full title, e.g. "Windsurf vs Claude Code: My Take"
  description: string;    // 1-2 sentence description for cards and OG tags
  metaTitle: string;      // < 60 chars, for <title> tag
  metaDescription: string; // < 160 chars, punchier/more opinionated
  datePublished: string;  // ISO date, e.g. "2026-03-03"
  dateModified: string;   // ISO date, update when content changes
  Content: () => ReactNode; // JSX function component
  markdown: string;       // Raw markdown version of same content
  relatedGuides: string[]; // 2-3 slugs of related content
}
```

## JSX Conventions

- Use `<p>`, `<h2>`, `<h3>`, `<ul>`, `<ol>`, `<li>`, `<code>`, `<strong>`, `<a>`, `<pre><code>` elements
- Use `&apos;` for apostrophes and `&quot;` for quotes in JSX
- Use `{"\n"}` inside `<pre><code>` blocks for newlines
- Internal links: `<a href="/guides/[slug]">link text</a>`
- External links: `<a href="https://..." target="_blank" rel="noopener noreferrer">text</a>`
- Wrap everything in `<>...</>` fragment
- Don't add margin classes to headings or paragraphs. Spacing is handled by `.guide-content` CSS in `app/globals.css`. Just write semantic HTML.

## Visual Defaults (Spacing, Hierarchy, Embeds, Images)

The canonical reference is **`/guides/ai-builder-technical-stack`**. Every new article should match its look and feel.

### Where the styles live

1. **Spacing + hierarchy** — `claude_course/website/app/globals.css` under `.guide-content`. Sets H2/H3 rhythm, paragraph spacing, list indents, code blocks, link colors. Don't override per-article.
2. **Video / HTML / image / table chrome** — `claude_course/website/lib/content-components.tsx`. Always import from here. Don't write custom `<figure>` or `<iframe>` markup.

### Shared components — use these by default

```tsx
import {
  TellaEmbed,
  HtmlEmbed,
  SlideImage,
  StackTable,
} from "@/lib/content-components";
```

- **`<TellaEmbed videoId title caption />`** — Tella video.
- **`<HtmlEmbed src height title caption />`** — interactive HTML iframe (`/embeds/*.html`). Pass an explicit pixel height.
- **`<SlideImage id caption />`** — Convex-hosted image (storageId). Add `external` for a full URL, `fullWidth` to drop the `max-w-2xl` cap.
- **`<StackTable rows />`** — three-column comparison table. Pass `headers` to relabel columns (handy for `Feature / Claude Code / Competitor` style comparisons in vs-articles).

All four use the same outer rhythm (`mt-4 mb-10`), card chrome (rounded-xl border on `#0f0f0f`), hover state (`#222 -> #333`), and centered captions in `#666`. That's what gives every guide and article the same quiet, captioned cadence.

### Hierarchy rules

- One `<h1>` is rendered automatically by the page shell. Start your `Content()` with the opening paragraph (thesis hook), not an `<h2>` against the title.
- Major sections: `<h2>`. Subsections inside them: `<h3>`. Don't nest deeper.
- Headings hug their first paragraph automatically (CSS handles `h2 + p`, `h3 + p`). Don't add wrapper divs that break that adjacency.

### When you really do need a custom embed

Match the existing rhythm: wrap in a `<figure className="mt-4 mb-10">`, give it a rounded-xl border on a `#0f0f0f` surface, add a centered `figcaption` in `text-sm text-[#666] mt-3`. Then consider promoting it into `lib/content-components.tsx` so future content gets it too.
