// Article template for ClaudeFluent
// File location: claude_course/website/lib/guides/content/[slug].tsx
//
// Articles use the same Guide interface as guides.
// The difference is editorial: articles are opinionated, timely, and take a stance.
//
// CANONICAL VISUAL REFERENCE: /guides/ai-builder-technical-stack defines the
// look and feel for every guide and article. Spacing, hierarchy, video embeds,
// HTML embeds, and images are standardized via:
//   1. .guide-content CSS in app/globals.css (h2/h3 rhythm, paragraph spacing,
//      lists, links, code blocks). Don't override per-article.
//   2. Shared components in @/lib/content-components (TellaEmbed, HtmlEmbed,
//      SlideImage, StackTable). Import these instead of writing custom
//      <figure>/<iframe> markup.
//
// Instructions:
// 1. Replace all [PLACEHOLDER] values
// 2. State your thesis in the first 2 paragraphs
// 3. Write Content() JSX with short paragraphs, no em dashes
// 4. Use shared components for ALL videos, images, HTML embeds, comparison tables
// 5. Write matching markdown string
// 6. Include 2-3 internal links to other guides
// 7. Include a "who should actually use [competitor]" section for credibility
// 8. Add CTA to ClaudeFluent at the bottom
// 9. Verify: metaTitle < 60 chars, metaDescription < 160 chars

import type { Guide } from "../index";
import {
  TellaEmbed,
  HtmlEmbed,
  SlideImage,
  StackTable,
} from "@/lib/content-components";

function Content() {
  return (
    <>
      {/* Opening: hook with a specific claim or surprising fact */}
      <p>
        [Opening that hooks. Specific number, surprising claim, or contrarian
        statement. Include target keyword.]
      </p>
      {/* Thesis: state your position clearly in paragraph 2 */}
      <p>
        I&apos;ve used both [tools]. I&apos;ve also taught over 100 people to
        build with Claude Code. Here&apos;s what I actually think: [clear thesis
        statement].
      </p>

      {/* OPTIONAL: Walkthrough or comparison video. Use TellaEmbed if there's
          a recorded version. */}
      {/* <TellaEmbed
        videoId="[tella-video-id]"
        title="[Video title for accessibility]"
        caption="The full comparison on video. Or keep scrolling for the written take."
      /> */}

      {/* What [competitor] actually is: fair, specific, no strawmanning */}
      <h2>What [Competitor] Actually Is</h2>
      <p>
        [Fair description. Be specific about capabilities. Don&apos;t strawman.]
      </p>

      {/* OPTIONAL: Side-by-side comparison via StackTable. Pass custom headers
          to fit a vs-style frame. */}
      {/* <StackTable
        headers={{ col1: "Feature", col2: "Claude Code", col3: "[Competitor]" }}
        rows={[
          { tool: "[Feature]", what: "[Claude Code take]", analogy: "[Competitor take]" },
        ]}
      /> */}

      {/* Your argument sections: each h2/h3 advances the thesis */}
      <h2>[Argument Section]</h2>
      <p>
        [Evidence, examples, specific numbers. Short paragraphs.]
      </p>

      {/* OPTIONAL: Screenshot or diagram backing the argument */}
      {/* <SlideImage
        id="[convex-storage-id]"
        caption="[Caption explaining what the image shows.]"
      /> */}

      {/* Code comparison if relevant */}
      <pre>
        <code>
          {"# Claude Code setup"}
          {"\n"}
          {"npm install -g @anthropic-ai/claude-code"}
          {"\n"}
          {"claude"}
        </code>
      </pre>

      {/* Why Claude Code wins: numbered or bulleted arguments */}
      <h2>Why Claude Code Wins for [Audience]</h2>

      <h3>1. [First argument]</h3>
      <p>[Evidence with specifics.]</p>

      <h3>2. [Second argument]</h3>
      <p>[Evidence with specifics.]</p>

      {/* Fair competitor section: builds credibility */}
      <h2>Who Should Actually Use [Competitor]</h2>
      <ul>
        <li>[Legitimate use case 1]</li>
        <li>[Legitimate use case 2]</li>
      </ul>

      {/* Internal links to related guides */}
      <p>
        Learn more about{" "}
        <a href="/guides/[related-slug]">related topic</a> and{" "}
        <a href="/guides/[related-slug-2]">another topic</a>.
      </p>

      {/* CTA */}
      <p>
        Want to see what productive AI coding actually looks like? Check out
        our <a href="/">ClaudeFluent training</a> where we go from setup to
        shipping in one live session.
      </p>
    </>
  );
}

// Markdown version of the same content (for LLM/sitemap consumption).
// Skip the video/image/embed components in markdown - just describe what they showed.
const markdown = `# [Article Title]

[Opening with target keyword and thesis.]

## What [Competitor] Actually Is

[Fair description.]

## [Argument Section]

[Content matching JSX above.]

## Why Claude Code Wins for [Audience]

1. **[First argument]** - [Evidence]
2. **[Second argument]** - [Evidence]

## Who Should Actually Use [Competitor]

- [Legitimate use case 1]
- [Legitimate use case 2]

Learn more about [related topic](/guides/[related-slug]).
`;

export const guide: Guide = {
  // URL-safe slug (lowercase, hyphens, no special chars)
  slug: "[slug]",

  // Full title, often "[X] vs Claude Code: [Opinionated Take]"
  title: "[Full Article Title]",

  // 1-2 sentence description, opinionated
  description: "[Description that takes a stance]",

  // < 60 characters, include year for comparison pieces
  metaTitle: "[Punchy Meta Title (Year)]",

  // < 160 characters, more opinionated than a guide's meta description
  metaDescription: "[Opinionated meta description. Pick a side. Include keyword.]",

  // ISO date format
  datePublished: "2026-03-03",

  // Update this when the article content changes (tools evolve, new info)
  dateModified: "2026-03-03",

  Content,
  markdown,

  // 2-3 slugs of related content
  relatedGuides: ["[slug-1]", "[slug-2]", "[slug-3]"],
};
