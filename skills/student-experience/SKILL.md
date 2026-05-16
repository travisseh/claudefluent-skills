---
name: student-experience
description: >
  Orchestrate and improve the ClaudeFluent student journey end-to-end — website, purchase, onboarding,
  class slides, exercises, and post-class community. Use this skill whenever thinking about student experience,
  class improvements, exercise personalization, onboarding flow, student success, or the ClaudeFluent Slack
  community. Also trigger when the user mentions improving the class, making exercises better, checking on
  students, or planning community engagement.
---

# Student Experience Orchestrator

This skill coordinates all aspects of the ClaudeFluent student experience. It doesn't duplicate other skills — it references them and adds the student-experience lens.

In Codex, interpret any historical `/skill-name` references inside this skill as explicit skill usage with `$skill-name`.

## Memory

Memory lives in `.claude/plugins/student-experience/state/`:

1. `state/insights.md` — Durable strategic knowledge (class structure, exercises, personas, onboarding). ALWAYS read first.
2. `state/daily/YYYY-MM-DD.md` — Today + yesterday's notes only.
3. `state/persona-gaps.md` — Per-persona coverage tracker.
4. `state/audit-log.md` — Audit history.

**Write protocol:** After every session, update today's daily note. Promote durable learnings to insights.md. Rotate daily notes older than 7 days (extract important bits first).

## The Core Metric

**Transformational value in 6 hours.** Every student should leave having:
1. Built something real that matters to their specific role
2. Understood Claude Code well enough to keep building independently
3. Felt like the class was designed for them personally

## Student Journey Touchpoints

### 1. Website (pre-purchase)
- Homepage messaging and testimonials
- Guide library targeting different personas
- Free resources for trust-building
- **Skills to use:** `behavior-design`, `synthetic-user-feedback`, `funnel-optimization`

### 2. Purchase → Onboarding
- Success page with setup instructions
- AI chat to learn about the student (goals, project, experience)
- Setup verification
- **Key files:** `app/success/page.tsx`, `app/onboarding/[token]/`
- **Goal:** Technical readiness + excitement before class

### 3. Pre-Class Gap (days/weeks between purchase and class)
- Currently underutilized
- Opportunity: drip content, persona-specific prep, Slack community welcome
- Share relevant guides based on their stated goals

### 4. Core Class Experience (P1 — highest priority)
- Slide deck with concepts and exercises
- **Skills to use:** `cc-slides`, `slide-style`
- **Key principle:** Fast time-to-value. Students should build something meaningful in the first 30 minutes.
- Exercise personalization is the primary lever (see below)

### 5. Post-Class Community (P3)
- Slack community: share updates, guides, foster conversation
- Follow-up based on what they built in class
- Testimonial extraction from Grain recordings (use `grain-testimonials` skill)
- Eventually: paid community tier

## Exercise Personalization Strategy

The slides stay universal (concepts apply to everyone). Exercises branch per student.

### How It Works

**Before class:**
1. Pull onboarding data for upcoming cohort from Convex (`participants` + `onboardingResponses` tables)
2. For each student, identify their persona and specific project
3. Prepare a personalized exercise brief that maps each class exercise to their project

**During class:**
Each exercise slide has a universal prompt PLUS a "Build YOUR Thing" variant:
- **Universal:** "Build a marketing landing page" (everyone can follow along)
- **Personalized:** "Build [their specific project from onboarding]" (for students ready to go deeper)

**After class:**
Follow up with next steps specific to what they built.

### Persona Exercise Mapping

When creating or reviewing exercises, ensure each has a clear value path for:

| Persona | They Want To Build | Exercise Angle |
|---------|-------------------|----------------|
| **PM** | Prototypes, PRDs, internal tools | "Build the tool your eng team keeps deprioritizing" |
| **Product Marketer** | Battle cards, competitive pages, launch materials | "Build your next launch asset" |
| **Founder** | MVP, landing page, automation | "Build the first version of your product" |
| **CSM** | Health dashboards, QBR decks, churn alerts | "Build the dashboard you wish you had" |
| **Designer** | Interactive prototypes, portfolio pieces | "Build a working version of your latest design" |
| **Marketing Manager** | SEO tools, content generators, lead magnets | "Build the tool that replaces your most tedious workflow" |

### Tracking Coverage

Maintain `state/persona-gaps.md` to track which personas have good exercise coverage and which need work.

## Convex Data for Personalization

```typescript
// Get upcoming cohort's onboarding data
import { ConvexHttpClient } from "convex/browser";
import { api } from "../convex/_generated/api";

const client = new ConvexHttpClient("https://polite-toad-76.convex.cloud");

// Get all participants
const participants = await client.query(api.participants.getAll);

// Get onboarding responses (has broadGoals, specificProject, experience flags)
// Cross-reference with participants table for names/emails
```

## Community Engagement Playbook

### What to Post to Slack
1. **Slide updates** — When new slides are added (use cc-slides to check recent changes)
2. **New guides** — When guide-writer creates content, share to community
3. **Feature announcements** — When Claude Code ships something new
4. **Student wins** — Reshare testimonials and project showcases
5. **Discussion prompts** — "What did you build this week?" type engagement

### Cadence
- 2-3 posts per week minimum
- Respond to all student messages within 24 hours
- Monthly "what's new" roundup

## Working With Other Skills

This skill coordinates but doesn't duplicate:
- **cc-slides** — For any slide modifications (always reference `slide-style` for formatting)
- **x-bookmarks-to-todos** — Surface new Claude Code features from Twitter for potential slides
- **guide-writer** — Create guides that serve both marketing AND student value
- **behavior-design** — Evaluate onboarding and success page UX
- **synthetic-user-feedback** — Test pages through persona lenses
- **funnel-optimization** — Check conversion data for experience friction points
- **stripe** — Check enrollment data to understand who's signing up
- **grain-testimonials** — Extract testimonials from Grain recordings and save to participant records
