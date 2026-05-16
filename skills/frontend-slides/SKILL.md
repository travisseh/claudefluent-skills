---
name: frontend-slides
description: "Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use this skill whenever the user wants to build a presentation, create slides, convert a PPT/PPTX to web, or prepare a deck for a talk, pitch, workshop, or class. Also trigger when they mention 'slide deck', 'presentation', 'keynote', 'make slides', or want to present information visually. Helps non-designers discover their aesthetic through visual exploration. Triggers on: presentation, slides, slide deck, PPT, PPTX, PowerPoint, keynote, pitch deck, workshop slides, make a deck, create slides, convert presentation."
---

# Frontend Slides Skill

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser. This skill helps non-designers discover their preferred aesthetic through visual exploration ("show, don't tell"), then generates production-quality slide decks.

## Core Philosophy

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** — People don't know what they want until they see it. Generate visual previews, not abstract choices.
3. **Distinctive Design** — Avoid generic "AI slop" aesthetics. Every presentation should feel custom-crafted.
4. **Production Quality** — Code should be well-commented, accessible, and performant.

---

## Phase 0: Detect Mode

First, determine what the user wants:

**Mode A: New Presentation**
- User wants to create slides from scratch
- Proceed to Phase 1 (Content Discovery)

**Mode B: PPT Conversion**
- User has a PowerPoint file (.ppt, .pptx) to convert
- Proceed to Phase 4 (PPT Extraction)

**Mode C: Existing Presentation Enhancement**
- User has an HTML presentation and wants to improve it
- Read the existing file, understand the structure, then enhance

---

## Phase 1: Content Discovery (New Presentations)

Before designing, understand the content. Ask the user directly with concise plain-text questions, or make a reasonable default if the user already gave enough context:

### Step 1.1: Presentation Context

**Question 1: Purpose**
- Header: "Purpose"
- Question: "What is this presentation for?"
- Options:
  - "Pitch deck" — Selling an idea, product, or company to investors/clients
  - "Teaching/Tutorial" — Explaining concepts, how-to guides, educational content
  - "Conference talk" — Speaking at an event, tech talk, keynote
  - "Internal presentation" — Team updates, strategy meetings, company updates

**Question 2: Slide Count**
- Header: "Length"
- Question: "Approximately how many slides?"
- Options:
  - "Short (5-10)" — Quick pitch, lightning talk
  - "Medium (10-20)" — Standard presentation
  - "Long (20+)" — Deep dive, comprehensive talk

**Question 3: Content**
- Header: "Content"
- Question: "Do you have the content ready, or do you need help structuring it?"
- Options:
  - "I have all content ready" — Just need to design the presentation
  - "I have rough notes" — Need help organizing into slides
  - "I have a topic only" — Need help creating the full outline

If user has content, ask them to share it (text, bullet points, images, etc.).

---

## Phase 2: Style Discovery (Visual Exploration)

**CRITICAL: This is the "show, don't tell" phase.**

Most people can't articulate design preferences in words. Instead of asking "do you want minimalist or bold?", we generate mini-previews and let them react.

### Step 2.1: Mood Selection

**Question 1: Feeling**
- Header: "Vibe"
- Question: "What feeling should the audience have when viewing your slides?"
- Options:
  - "Impressed/Confident" — Professional, trustworthy, this team knows what they're doing
  - "Excited/Energized" — Innovative, bold, this is the future
  - "Calm/Focused" — Clear, thoughtful, easy to follow
  - "Inspired/Moved" — Emotional, storytelling, memorable
- multiSelect: true (can choose up to 2)

### Step 2.2: Generate Style Previews

Based on their mood selection, generate **3 distinct style previews** as mini HTML files in a temporary directory. Each preview should be a single title slide showing:

- Typography (font choices, heading/body hierarchy)
- Color palette (background, accent, text colors)
- Animation style (how elements enter)
- Overall aesthetic feel

**Preview Styles to Consider (pick 3 based on mood):**

| Mood | Style Options |
|------|---------------|
| Impressed/Confident | "Corporate Elegant", "Dark Executive", "Clean Minimal" |
| Excited/Energized | "Neon Cyber", "Bold Gradients", "Kinetic Motion" |
| Calm/Focused | "Paper & Ink", "Soft Muted", "Swiss Minimal" |
| Inspired/Moved | "Cinematic Dark", "Warm Editorial", "Atmospheric" |

**IMPORTANT: Never use these generic patterns:**
- Purple gradients on white backgrounds
- Inter, Roboto, or system fonts
- Standard blue primary colors
- Predictable hero layouts

**Instead, use distinctive choices:**
- Unique font pairings (Clash Display, Satoshi, Cormorant Garamond, DM Sans, etc.)
- Cohesive color themes with personality
- Atmospheric backgrounds (gradients, subtle patterns, depth)
- Signature animation moments

### Step 2.3: Present Previews

Create the previews in: `.claude-design/slide-previews/`

```
.claude-design/slide-previews/
├── style-a.html   # First style option
├── style-b.html   # Second style option
├── style-c.html   # Third style option
└── assets/        # Any shared assets
```

Each preview file should be:
- Self-contained (inline CSS/JS)
- A single "title slide" showing the aesthetic
- Animated to demonstrate motion style
- ~50-100 lines, not a full presentation

Present to user:
```
I've created 3 style previews for you to compare:

**Style A: [Name]** — [1 sentence description]
**Style B: [Name]** — [1 sentence description]
**Style C: [Name]** — [1 sentence description]

Open each file to see them in action:
- .claude-design/slide-previews/style-a.html
- .claude-design/slide-previews/style-b.html
- .claude-design/slide-previews/style-c.html

Take a look and tell me:
1. Which style resonates most?
2. What do you like about it?
3. Anything you'd change?
```

Then ask the user directly in plain language:

**Question: Pick Your Style**
- Header: "Style"
- Question: "Which style preview do you prefer?"
- Options:
  - "Style A: [Name]" — [Brief description]
  - "Style B: [Name]" — [Brief description]
  - "Style C: [Name]" — [Brief description]
  - "Mix elements" — Combine aspects from different styles

If "Mix elements", ask for specifics.

---

## Phase 3: Generate Presentation

Now generate the full presentation based on:
- Content from Phase 1
- Style from Phase 2

### File Structure

For single presentations:
```
presentation.html    # Self-contained presentation
assets/              # Images, if any
```

For projects with multiple presentations:
```
[presentation-name].html
[presentation-name]-assets/
```

### HTML Architecture

Follow this structure for all presentations:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation Title</title>

    <!-- Fonts (use Fontshare or Google Fonts) -->
    <link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=...">

    <style>
        /* ===========================================
           CSS CUSTOM PROPERTIES (THEME)
           Easy to modify: change these to change the whole look
           =========================================== */
        :root {
            /* Colors */
            --bg-primary: #0a0f1c;
            --bg-secondary: #111827;
            --text-primary: #ffffff;
            --text-secondary: #9ca3af;
            --accent: #00ffcc;
            --accent-glow: rgba(0, 255, 204, 0.3);

            /* Typography */
            --font-display: 'Clash Display', sans-serif;
            --font-body: 'Satoshi', sans-serif;

            /* Spacing */
            --slide-padding: clamp(2rem, 5vw, 4rem);

            /* Animation */
            --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
            --duration-normal: 0.6s;
        }

        /* ===========================================
           BASE STYLES
           =========================================== */
        * { margin: 0; padding: 0; box-sizing: border-box; }

        html {
            scroll-behavior: smooth;
            scroll-snap-type: y mandatory;
        }

        body {
            font-family: var(--font-body);
            background: var(--bg-primary);
            color: var(--text-primary);
            overflow-x: hidden;
        }

        .slide {
            min-height: 100vh;
            padding: var(--slide-padding);
            scroll-snap-align: start;
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }

        .reveal {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity var(--duration-normal) var(--ease-out-expo),
                        transform var(--duration-normal) var(--ease-out-expo);
        }

        .slide.visible .reveal {
            opacity: 1;
            transform: translateY(0);
        }

        .reveal:nth-child(1) { transition-delay: 0.1s; }
        .reveal:nth-child(2) { transition-delay: 0.2s; }
        .reveal:nth-child(3) { transition-delay: 0.3s; }
        .reveal:nth-child(4) { transition-delay: 0.4s; }
    </style>
</head>
<body>
    <div class="progress-bar"></div>

    <section class="slide title-slide">
        <h1 class="reveal">Presentation Title</h1>
        <p class="reveal">Subtitle or author</p>
    </section>

    <section class="slide">
        <h2 class="reveal">Slide Title</h2>
        <p class="reveal">Content...</p>
    </section>

    <script>
        class SlidePresentation {
            constructor() { /* ... */ }
        }
        new SlidePresentation();
    </script>
</body>
</html>
```

### Required JavaScript Features

Every presentation should include:

1. **SlidePresentation Class** — Main controller
   - Keyboard navigation (arrows, space)
   - Touch/swipe support
   - Mouse wheel navigation
   - Progress bar updates
   - Navigation dots

2. **Intersection Observer** — For scroll-triggered animations
   - Add `.visible` class when slides enter viewport
   - Trigger CSS animations efficiently

3. **Optional Enhancements** (based on style):
   - Custom cursor with trail
   - Particle system background (canvas)
   - Parallax effects
   - 3D tilt on hover
   - Magnetic buttons
   - Counter animations

### Code Quality Requirements

**Comments:** Every section should have clear comments explaining what it does, why it exists, how to modify it.

**Accessibility:**
- Semantic HTML (`<section>`, `<nav>`, `<main>`)
- Keyboard navigation works
- ARIA labels where needed
- Reduced motion support: `@media (prefers-reduced-motion: reduce)`

**Responsive:**
- Mobile-friendly (single column, adjusted spacing)
- Disable heavy effects on mobile
- Touch-friendly interactions

---

## Phase 4: PPT Conversion

When converting PowerPoint files:

### Step 4.1: Extract Content

Use Python with `python-pptx` to extract text, images, and notes from each slide. Save images to an assets directory.

### Step 4.2: Confirm Content Structure

Present extracted content to user for confirmation before proceeding.

### Step 4.3: Style Selection

Proceed to Phase 2 (Style Discovery) with extracted content in mind.

### Step 4.4: Generate HTML

Convert extracted content into chosen style, preserving all text, images, slide order, and speaker notes.

---

## Phase 5: Delivery

1. Clean up temporary files (`.claude-design/slide-previews/`)
2. Open the presentation with `open [filename].html`
3. Provide navigation instructions and customization tips

---

## Style Reference: Effect to Feeling Mapping

- **Dramatic/Cinematic:** Slow fade-ins, large scale transitions, dark backgrounds with spotlight, parallax
- **Techy/Futuristic:** Neon glow, particle systems, grid patterns, monospace accents, glitch effects
- **Playful/Friendly:** Bouncy easing, rounded corners, pastel colors, floating animations
- **Professional/Corporate:** Subtle fast animations, clean sans-serif, navy/slate, data viz focus
- **Calm/Minimal:** Very slow subtle motion, high whitespace, muted palette, serif typography
- **Editorial/Magazine:** Strong type hierarchy, pull quotes, image-text interplay, grid-breaking layouts

---

## Style Presets Reference

### Dark Themes

**1. Neon Cyber** — Futuristic, techy, confident
- Fonts: Clash Display + Satoshi (Fontshare)
- Colors: `#0a0f1c` bg, `#00ffcc` accent, `#ff00aa` secondary
- Effects: Particle system, neon glow, custom cursor, grid overlay, glitch text

**2. Midnight Executive** — Premium, sophisticated, corporate
- Fonts: Libre Baskerville + Source Sans 3
- Colors: `#0f172a` bg, `#3b82f6` accent, `#fbbf24` gold
- Effects: Subtle gradients, thin gold accent lines, data visualizations

**3. Deep Space** — Inspiring, vast, visionary
- Fonts: Space Grotesk + DM Sans
- Colors: `#030712` bg, `#818cf8` accent, `#c084fc` secondary
- Effects: Starfield background, radial spotlight, floating elements, parallax

**4. Terminal Green** — Developer-focused, hacker, retro-tech
- Fonts: JetBrains Mono (display + body)
- Colors: `#0d1117` bg, `#39d353` accent
- Effects: Scan line overlay, blinking cursor, ASCII art, typewriter reveals

### Light Themes

**5. Paper & Ink** — Editorial, literary, refined
- Fonts: Cormorant Garamond + Source Serif 4
- Colors: `#faf9f7` bg, `#c41e3a` accent
- Effects: Drop caps, pull quotes, paper texture, elegant rules

**6. Swiss Modern** — Clean, precise, Bauhaus-inspired
- Fonts: Archivo + Nunito
- Colors: `#ffffff` bg, `#ff3300` accent
- Effects: Visible grid, asymmetric layouts, geometric shapes

**7. Soft Pastel** — Friendly, approachable, playful
- Fonts: Nunito (display + body)
- Colors: `#fef3f2` bg, `#f472b6` / `#a78bfa` / `#34d399` accents
- Effects: Rounded corners, blob shapes, bouncy spring physics

**8. Warm Editorial** — Human, storytelling, magazine
- Fonts: Playfair Display + Work Sans
- Colors: `#fffbf5` bg, `#b45309` accent
- Effects: Large hero images, image overlays, Ken Burns effect

### Specialty Themes

**9. Brutalist** — Raw, bold, unconventional
- Fonts: Anton/Bebas Neue + IBM Plex Mono
- Colors: `#ffffff` bg, `#ff0000` accent, `#000000` border
- Effects: Thick borders, chaotic layouts, oversized type, hard cuts

**10. Gradient Wave** — Modern SaaS, energetic
- Fonts: Cabinet Grotesk + Inter
- Colors: `#0f0f1a` bg, `#667eea` / `#764ba2` / `#f472b6` gradients
- Effects: Animated gradient meshes, glass-morphism, floating orbs

---

## Font Pairing Quick Reference

- Techy/Modern: Clash Display + Satoshi (Fontshare)
- Professional: Libre Baskerville + Source Sans 3
- Space/Future: Space Grotesk + DM Sans
- Developer: JetBrains Mono + JetBrains Mono
- Editorial: Cormorant Garamond + Source Serif 4
- Swiss/Minimal: Archivo + Nunito
- Playful: Nunito + Nunito
- Magazine: Playfair Display + Work Sans
- Brutalist: Anton + IBM Plex Mono
- SaaS Modern: Cabinet Grotesk + Inter

---

## DO NOT USE (Generic AI Patterns)

- Inter, Roboto, Arial/Helvetica as display fonts (except Gradient Wave)
- `#6366f1` generic indigo, purple/violet gradients on white
- Centered everything, generic hero layouts, standard 3-column grids
- Identical timing on all elements, linear easing, excessive bounce
- Gratuitous glassmorphism, shadows/blurs without intention
