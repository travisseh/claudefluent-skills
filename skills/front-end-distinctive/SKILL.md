---
name: front-end-distinctive
description: Use this skill when designing or restyling frontend pages that should look intentional and non-generic. Applies strong typography, cohesive visual direction, atmospheric backgrounds, and concise high-impact motion while avoiding common AI-style defaults.
---

# Front-End Distinctive

Build interfaces with clear visual authorship. Prioritize confidence and memorability over generic safety.

## When To Use
Use this skill when:
- The user asks for better visual quality, branding, or “less AI-like” design.
- A report/dashboard page needs stronger hierarchy and clearer storytelling.
- Existing UI looks generic or template-like.

## Core Rules

### Typography
- Do not default to Inter/Roboto/Arial/system-only stacks.
- Pair one expressive display face with one highly readable text face.
- Keep hierarchy obvious: headline, section title, body, metadata.

### Visual Direction
- Pick a single aesthetic and commit to it.
- Use CSS variables for palette, spacing, and radii.
- Favor a dominant tone + accent instead of evenly mixed colors.
- Avoid purple-on-white default gradients and generic SaaS palettes.

### Layout
- Make the primary decision obvious above the fold.
- Organize dense content into tabs or compact sections.
- Keep line lengths and table density readable on desktop and mobile.

### Motion
- Use a small number of meaningful CSS animations:
  - page/section reveal
  - staggered card entry
  - subtle hover emphasis
- Avoid constant micro-animation noise.

### Backgrounds
- Avoid flat single-color backgrounds.
- Add depth with layered gradients, subtle textures, or geometric overlays.
- Keep contrast and readability high.

## Anti-Patterns
- Cookie-cutter dashboard styling.
- Over-long verbose sections with no visual hierarchy.
- Too many equal-weight cards competing for attention.
- Decorative motion without information value.

## Implementation Checklist
1. Establish design tokens in `:root` (color, type, spacing, radius, shadow).
2. Apply strong typography pair and scale.
3. Rebuild page around decision-first flow.
4. Compress copy to short, explicit statements.
5. Add 1-2 meaningful animations.
6. Verify responsive behavior at mobile widths.
