---
name: guide-writer
description: "Create evergreen Claude Code guides for ClaudeFluent. Use this skill whenever writing how-to guides, feature deep dives, setup guides, tutorials, or comprehensive reference content for the ClaudeFluent website. Also trigger when the user asks to 'write a guide', 'create a guide', 'new guide about', 'add a guide for', or wants to create SEO-friendly educational content about Claude Code features or use cases. Triggers on: write a guide, create a guide, new guide about, ClaudeFluent guide, how-to guide, feature guide, tutorial, deep dive, setup guide, reference content."
---

# Guide Writer

Create evergreen reference content for ClaudeFluent. Guides should be useful 6 months from now. They teach someone how to do something specific with Claude Code.

Examples: how to use Claude Code, setting up MCP servers, plan mode deep dive, best practices, tutorials.

## Audience

Read `references/personas.md` for full persona details.

**Primary targets:**
- **Priya** (Senior PM): Wants to reduce eng dependency. Frustrated she has to wait on engineers. Write for her by showing what she can build herself, with concrete PM workflows.
- **Derek** (Solo Founder): Vets everything, wants practitioner credibility. Write for him by proving you've actually built things, with specific technical outcomes.

**Secondary:**
- **Ashley** (Dir PMM): Team-level thinking. Frame as "here's what your team can do."
- **Sandra** (VP CS): Needs ROI framing and non-technical entry points.

## Content Principles

- Extremely practical, hands-on, zero fluff
- Every section answers "what do I do with this?"
- Real examples from teaching 100+ students
- Opinionated: take a stance, don't hedge
- If a section doesn't help someone get productive faster, cut it
- Teach by showing, not by explaining abstractly
- Use first-person authority: "I've taught over 100 people..."
- Include concrete numbers, real student outcomes, specific tool names

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
- `metaDescription` < 160 characters
- 2-3 internal links to other guides using `<a href="/guides/[slug]">text</a>`
- CTA to ClaudeFluent course at the bottom of the guide
- `relatedGuides` array with 2-3 slugs from existing guides
- Existing slugs: `what-is-vibe-coding`, `claude-code-vs-cursor`, `what-is-claude-code`, `ai-for-product-managers`, `claude-code-mcp-servers`, `claude-code-agents`, `claude-code-plan-mode`, `claude-code-skills`, `codex-inside-claude-code`, `claude-code-best-practices`, `claude-code-tutorial`, `claude-code-setup`, `openclaw-vs-claude-code`, `claude-code-battle-cards`, `claude-code-launch-briefs`, `claude-code-win-loss-analysis`, `claude-code-competitive-intelligence`, `claude-code-internal-dashboards`, `claude-code-first-automation`, `claude-code-churn-detection`, `claude-code-onboarding-playbooks`, `claude-code-qbr-automation`, `claude-code-health-scoring`, `claude-code-release-notes`, `claude-code-data-pulls`, `claude-code-research-synthesizer`, `claude-code-prd-writing`, `claude-code-feature-prioritization`, `claude-code-sprint-retros`, `claude-code-landing-page`, `claude-code-stripe-mvp`, `claude-code-cold-outreach`, `claude-code-feedback-dashboard`, `claude-code-competitor-teardowns`, `claude-code-invoice-generator`, `claude-code-slack-bot`, `claude-code-api-prototyping`, `claude-code-chief-of-staff-plugin`, `claude-code-synthetic-user-feedback`, `agent-orchestration-guide`, `claude-code-terminal-feel-like-browser`, `claude-code-desktop-setup`

## Quality Gates

Before delivering, verify ALL of these:

- [ ] Unique intent (no other guide covers this exact angle)
- [ ] 800+ words of substantive content
- [ ] No banned phrases, no em dashes in prose
- [ ] 2+ concrete examples or code snippets
- [ ] Internal links to 2-3 other guides
- [ ] CTA at bottom linking to ClaudeFluent homepage or course
- [ ] Both `Content()` JSX and `markdown` string present
- [ ] TypeScript compiles clean (`npx tsc --noEmit`)
- [ ] `metaTitle` < 60 chars, `metaDescription` < 160 chars
- [ ] First paragraph contains target keyword

## Technical Wiring (6 steps)

After writing the guide content, do these steps in order:

### Step 1: Create the content file
Create `claude_course/website/lib/guides/content/[slug].tsx` using the template at `references/guide-template.tsx`.

### Step 2: Register in guides index
Add import and entry to `claude_course/website/lib/guides/index.ts`:
```typescript
import { guide as yourGuide } from "./content/[slug]";
// Add to the guides array:
const guides: Guide[] = [
  // ... existing guides
  yourGuide,
];
```

### Step 3: Add slug to SEO config
Add the slug string to the `GUIDE_SLUGS` array in `claude_course/website/lib/seo-config.ts`.

### Step 4: (Optional) Add card to free-resources page
If the guide should be discoverable from the resources page, add a card to `claude_course/website/app/free-resources/page.tsx`. Note: guide cards are currently hidden behind `{false && <>...</>}`.

### Step 5: Update LLM discovery files
Add a new bullet to the `## Guides` section in both:
- `claude_course/website/public/llms.txt`
- `claude_course/website/public/llms-full.txt`

Format: `- [Guide Title](https://claudefluent.com/guides/[slug]) - Brief description`

### Step 6: Verify
Run `npx tsc --noEmit` from `claude_course/website/` to confirm TypeScript compiles. Then `npx next build` to confirm the full build passes.

## Guide Interface (TypeScript reference)

```typescript
export interface Guide {
  slug: string;           // URL-safe slug, e.g. "claude-code-hooks"
  title: string;          // Full title, e.g. "Claude Code Hooks: Automate Your Workflow"
  description: string;    // 1-2 sentence description for cards and OG tags
  metaTitle: string;      // < 60 chars, for <title> tag
  metaDescription: string; // < 160 chars, for meta description
  datePublished: string;  // ISO date, e.g. "2026-03-03"
  dateModified: string;   // ISO date, update when content changes
  Content: () => ReactNode; // JSX function component
  markdown: string;       // Raw markdown version of same content
  relatedGuides: string[]; // 2-3 slugs of related guides
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

The canonical reference is **`/guides/ai-builder-technical-stack`**. Every new guide should match its look and feel.

### Where the styles live

1. **Spacing + hierarchy** — `claude_course/website/app/globals.css` under `.guide-content`. Sets H2/H3 rhythm, paragraph spacing, list indents, code blocks, link colors. Don't override per-guide.
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

- **`<TellaEmbed videoId title caption />`** — Tella video. Standard placement: under the H1 as a "watch instead of read" CTA, or at the top of any major section that has a walkthrough video.
- **`<HtmlEmbed src height title caption />`** — interactive HTML iframe (`/embeds/*.html`). Pass an explicit pixel height.
- **`<SlideImage id caption />`** — Convex-hosted image (storageId). Add `external` for a full URL, `fullWidth` to drop the `max-w-2xl` cap.
- **`<StackTable rows />`** — three-column tool/what/analogy comparison table. Pass `headers` to relabel columns.

All four use the same outer rhythm (`mt-4 mb-10`), card chrome (rounded-xl border on `#0f0f0f`), hover state (`#222 -> #333`), and centered captions in `#666`. That's what gives every guide the same quiet, captioned cadence.

### Hierarchy rules

- One `<h1>` is rendered automatically by the page shell. Start your `Content()` with body copy or an embed, not an `<h2>` against the title.
- Major sections: `<h2>`. Subsections inside them: `<h3>`. Don't nest deeper.
- Headings hug their first paragraph automatically (CSS handles `h2 + p`, `h3 + p`). Don't add wrapper divs that break that adjacency.

### When you really do need a custom embed

Match the existing rhythm: wrap in a `<figure className="mt-4 mb-10">`, give it a rounded-xl border on a `#0f0f0f` surface, add a centered `figcaption` in `text-sm text-[#666] mt-3`. Then consider promoting it into `lib/content-components.tsx` so future guides get it too.
