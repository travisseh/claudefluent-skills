---
name: slide-style
description: >
  Writing style guide for ClaudeFluent presentation slides. Reference this skill whenever writing or reviewing
  slide content to ensure consistent voice, structure, and formatting. Use alongside cc-slides for any slide
  creation or modification.
---

# ClaudeFluent Slide Style Guide

Reference this when writing slide content. These patterns were derived from the current deck and should be followed for consistency.

## Slide Structure Template

Every slide follows this skeleton:

```
[H1] Topic Title (2-5 words)
[H3] Subtitle or key question (5-12 words)
[HR]
[H3] Section 1
[Bullet list, 3-5 items]
[HR]
[H3] Section 2
[Bullet list or code block]
[HR] (optional)
[H3] Closing section ("Try It", "When to Use", "Why This Matters")
```

## Heading Rules

- **H1:** Exactly once, at the top. Concise and concept-focused.
  - Good: "Claude Code Memory", "Thinking Levels & Ultrathink", "Plugins vs Skills"
  - Bad: "An Introduction to How Claude Code Memory Works"
- **H3:** All section headers. Never use H2 — skip from H1 to H3.
  - Good: "What Is It?", "Key Commands", "When to Use What"
- **No H2s.** The deck uses H1 → H3 for visual hierarchy.

## Bullet Point Patterns

**Structure each bullet as: Bold label + explanation**
```
- **Create** — Interview-driven skill generation with test cases
- **CLAUDE.md** = instructions *you* write and maintain
- **Stable patterns** confirmed across multiple interactions
```

**Density:** 3-5 items per list. Max 25 words per bullet. Each bullet is 1-2 sentences.

**Use ordered lists** for sequential steps. **Unordered lists** for feature groupings.

## Code Formatting

**Inline code** for: commands, file paths, variable names, CLI flags
- `code(/effort low)`, `code(~/.claude/CLAUDE.md)`, `code(SKILL.md)`

**Code blocks** for: shell commands, config examples, prompts to try
- Keep to 3-5 lines
- Include `#` comments for clarity
- Example:
```
/effort low        # Fastest, cheapest
/effort high       # Default for complex work
/effort ultrathink # Deepest reasoning
```

## Tone & Voice

- **Professional but conversational.** Not academic, not casual.
- **Direct and prescriptive:** "Use this for X", "Think of it as Y"
- **Action-oriented:** Active voice, command form when appropriate
- **Practical trade-offs:** "Fastest, cheapest" vs "Deepest reasoning"
- **Explain the why**, not just the what

**Good:** "Think of it as a mini agent you can install"
**Bad:** "Plugins are software components that extend functionality"

## Formatting Emphasis

- **Bold** — Key concepts, action labels at bullet start, important nouns
- *Italic* — Rare. For philosophical distinctions ("*you* write" vs "*Claude* writes")
- `Code` — Liberally for anything typed in a terminal or editor
- **Bold + italic** — Very rare, for critical distinctions only

## Section Separators

Use `<hr>` (horizontal rules) between every major section. Creates visual breathing room.

Standard placement:
1. After the H3 subtitle
2. Between each H3 content section
3. Optionally before closing section

## Closing Sections

End slides with one of these patterns:
- **"Try It"** — Concrete prompts students can copy-paste
- **"When to Use What"** — Decision guide with bold labels
- **"Why This Matters"** — Philosophical/practical context
- **"Pro Tips"** — Power-user insights, 3-4 bullets

## Word Count Guidelines

- **Total slide:** 200-400 words (including headers)
- **H1 title:** 2-5 words
- **H3 headers:** 5-12 words
- **Bullet items:** 10-25 words each
- **Code blocks:** 3-5 lines

## Anti-Patterns (Don't Do These)

- Walls of paragraph text (use bullets instead)
- More than 6 bullets in a single list
- H2 headings (always H3)
- Slides without a code block or "try it" section
- Generic descriptions without concrete examples
- Marketing language ("revolutionary", "game-changing")
