// Guide template for ClaudeFluent
// File location: claude_course/website/lib/guides/content/[slug].tsx
//
// CANONICAL REFERENCE: /guides/ai-builder-technical-stack defines the look and
// feel for every new guide. Spacing, hierarchy, video embeds, HTML embeds, and
// images are all standardized via:
//   1. .guide-content CSS in app/globals.css (h2/h3 rhythm, paragraph spacing,
//      lists, links, code blocks).
//   2. Shared components in @/lib/content-components (TellaEmbed, HtmlEmbed,
//      SlideImage, StackTable). Always import these instead of writing custom
//      figure/iframe markup.
//
// Instructions:
// 1. Replace all [PLACEHOLDER] values
// 2. Write Content() JSX with short paragraphs, no em dashes
// 3. Use shared components for ALL videos, images, HTML embeds, comparison tables
// 4. Write matching markdown string
// 5. Include 2-3 internal links to other guides
// 6. Add CTA to ClaudeFluent at the bottom
// 7. Verify: metaTitle < 60 chars, metaDescription < 160 chars

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
      {/* OPTIONAL: Walkthrough video at the top of the guide.
          Place a TellaEmbed under the H1 so readers can watch instead of read.
          Caption tells them they can also keep scrolling. */}
      <TellaEmbed
        videoId="[tella-video-id]"
        title="[Video title for accessibility]"
        caption="The full walkthrough on video. Or keep scrolling for the written version."
      />

      {/* Opening paragraph: include target keyword, establish authority */}
      <p>
        [Opening that hooks the reader. Include target keyword. Establish
        credibility: &quot;I&apos;ve taught over 100 people...&quot;]
      </p>

      {/* Main sections: use h2 for major sections, h3 for subsections.
          Spacing is handled automatically by .guide-content CSS. Don't add
          margin classes to headings. */}
      <h2>[Section Title]</h2>
      <p>
        [Short paragraphs. 1-3 sentences max. Be specific with numbers and examples.]
      </p>

      {/* OPTIONAL: Comparison table. Use StackTable for any "tool / what / analogy"
          breakdown. Pass custom headers if your columns aren't tool/what/analogy. */}
      <StackTable
        rows={[
          { tool: "[Tool name]", what: "[What it does]", analogy: "[Analogy]" },
          { tool: "[Tool name]", what: "[What it does]", analogy: "[Analogy]" },
        ]}
      />

      {/* OPTIONAL: Slide or screenshot image. Pass a Convex storageId by default,
          or set external={true} to use a full URL. */}
      <SlideImage
        id="[convex-storage-id]"
        caption="[Caption explaining what the image shows.]"
      />

      {/* OPTIONAL: Interactive HTML embed (e.g. /embeds/terminal-demo.html).
          Pass an explicit pixel height. */}
      <HtmlEmbed
        src="/embeds/[your-embed].html"
        height={400}
        title="[Title for accessibility]"
        caption="[Caption explaining what the embed demonstrates.]"
      />

      {/* Code examples: use pre > code with {"\n"} for newlines */}
      <pre>
        <code>
          {"example-command --flag value"}
          {"\n"}
          {"another-command"}
        </code>
      </pre>

      {/* Lists: use ul/ol with li elements */}
      <ul>
        <li>
          <strong>Key point.</strong> Explanation in 1-2 sentences.
        </li>
      </ul>

      {/* Internal links to other guides */}
      <p>
        Learn more about{" "}
        <a href="/guides/[related-slug]">related topic</a>.
      </p>

      {/* CTA at the bottom */}
      <p>
        Want to see this in action? Check out our{" "}
        <a href="/">ClaudeFluent training</a> where we go from setup to
        shipping in one live session.
      </p>
    </>
  );
}

// Markdown version of the same content (for LLM/sitemap consumption).
// Skip the video/image/embed components in markdown - just describe what they showed.
const markdown = `# [Guide Title]

[Opening paragraph with target keyword.]

## [Section Title]

[Content matching the JSX above but in markdown format.]

\`\`\`
example-command --flag value
\`\`\`

- **Key point.** Explanation.

Learn more about [related topic](/guides/[related-slug]).
`;

export const guide: Guide = {
  // URL-safe slug (lowercase, hyphens, no special chars)
  slug: "[slug]",

  // Full title for h1 and OG tags
  title: "[Full Guide Title]",

  // 1-2 sentence description for cards and OG description
  description: "[Description for cards and social sharing]",

  // < 60 characters, for browser tab and search results
  metaTitle: "[Meta Title Under 60 Chars (Year)]",

  // < 160 characters, for search result snippet
  metaDescription: "[Meta description under 160 chars. Include keyword. Make it compelling.]",

  // ISO date format
  datePublished: "2026-03-03",
  dateModified: "2026-03-03",

  Content,
  markdown,

  // 2-3 slugs of related guides from the existing set
  relatedGuides: ["[slug-1]", "[slug-2]", "[slug-3]"],
};
