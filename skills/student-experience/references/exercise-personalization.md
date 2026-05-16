# Exercise Personalization Reference

## Current Onboarding Data Model

From `convex/schema.ts`, the `onboardingResponses` table captures:

```typescript
{
  participantId: Id<"participants">,
  broadGoals: string,         // What they want to achieve
  specificProject: string,    // What they want to build
  usedCodeEditor: boolean,    // Technical experience flags
  usedTerminal: boolean,
  usedGithub: boolean,
  usedVercel: boolean,
  testimonialBlurb: string,
  finalProjectDescription: string,
  chatHistory: [{role, content}],  // Full onboarding conversation
}
```

The `participants` table has:
```typescript
{
  name: string,
  email: string,
  linkedin: string,
  sessionId: string,     // Which class session they're in
}
```

## Persona Detection Heuristics

Map `broadGoals` and `specificProject` to personas:

### Product Manager Signals
- Goals mention: "prototype", "validate", "ship without eng", "internal tool", "dashboard", "PRD"
- Projects: admin panels, data tools, workflow automation

### Product Marketer Signals
- Goals mention: "competitive", "battle card", "launch", "positioning", "landing page"
- Projects: marketing sites, comparison tools, content generators

### Founder/Entrepreneur Signals
- Goals mention: "MVP", "startup", "side project", "revenue", "customers", "launch"
- Projects: SaaS apps, marketplaces, automation tools

### Customer Success Signals
- Goals mention: "health score", "QBR", "churn", "retention", "customer data"
- Projects: dashboards, reporting tools, alert systems

### Designer Signals
- Goals mention: "prototype", "portfolio", "interactive", "design system"
- Projects: design tools, portfolio sites, component libraries

### Marketing Manager Signals
- Goals mention: "SEO", "content", "leads", "email", "social", "analytics"
- Projects: content tools, SEO automation, lead gen pages

## Exercise Branch Template

For each exercise in the deck, create variants:

```markdown
### Universal Prompt (everyone follows this)
[Standard exercise that works for any student]

### Personalized Variants
**If PM:** [Modify prompt to reference their internal tool/prototype goal]
**If Marketer:** [Modify prompt to reference their campaign/launch goal]
**If Founder:** [Modify prompt to reference their MVP/product goal]
**If CSM:** [Modify prompt to reference their dashboard/automation goal]
```

## Pre-Class Preparation Script

Before each class session:

1. Query participants for that session (filter by `sessionId`)
2. Pull their onboarding responses
3. Classify each student into a persona
4. For each exercise in the deck, prepare a one-line personalized prompt
5. Create a "class prep" document with:
   - Student name
   - Their persona
   - Their specific project
   - Personalized prompts for each exercise

This doc helps the user (or a TA) quickly give each student their personalized variant during exercises.

## Measuring Exercise Effectiveness

Track in `state/improvements.md`:
- Which exercises were run with personalization
- Student feedback (from post-class survey or Slack)
- Testimonial blurbs that reference specific exercises
- Time-to-completion for exercises (are students finishing? stuck?)
