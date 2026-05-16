---
name: team-pitch
description: Draft ClaudeFluent team/private training pitches and replies in the user's voice. Use whenever a team inquiry comes in (form submission, referral, LinkedIn DM, email) and the user needs a first-touch reply, a follow-up, a pricing answer, a curriculum explanation, or a scheduling message. Trigger on phrases like "team inquiry", "private class", "team training", "group training", "company training", "team pitch", "reply to team lead", or any mention of team/cohort seats for ClaudeFluent. Covers DocuSketch/Solv/PayPal/ClassDojo-style inbound threads.
---

# ClaudeFluent Team Pitch & Reply Skill

the user gets the same 6–8 questions on every team inquiry. This skill gives him the answers, pre-written in his voice, so he can paste, tweak a line, and send.

## MANDATORY: filter final output through `/user-writing-style`

Before showing the user any draft produced from this skill, you MUST load the `user-writing-style` skill and run the draft through it. The templates below are structural scaffolding — the final send must match the user's master writing style guide. If the two conflict, `user-writing-style` wins.

Workflow:
1. Pick template from this file, fill in specifics.
2. Load `user-writing-style` skill.
3. Rewrite the draft to conform.
4. THEN show the user for approval.

## Voice rules (non-negotiable)

Pulled from the actual DocuSketch, Solv, PayPal, ClassDojo threads:

- **Opens casual, no fluff.** "Hey [Name]," (never "Hi" unless it's very formal / enterprise procurement). Never "I hope this finds you well."
- **One sentence of warm framing** about the fit ("Sounds like a good fit — you'll get huge leverage for a team at that stage, especially on a [X] team.")
- **Numbered lists for logistics.** Two short lists max: "Couple of questions" and "Logistics on my end."
- **Short sentences.** No paragraphs over 3 lines. No em-dash-heavy marketing prose.
- **Asks what they want to build.** Always. This is the signature move — the pitch pivots from "training" to "custom to your team."
- **Closes with a single question.** Either scheduling ("Any times in mind?") or discovery ("What are you looking to automate?") — never both, never none.
- **Never moralizes, never over-explains, never apologizes for pricing.** State it flat.
- **No emojis. No sign-off beyond "the user" or nothing at all.** Most replies end with the question, no signature.

## The facts (keep these straight)

| Thing | Current answer |
|---|---|
| Private team price | **$799/seat** (20% off the $999 list price). Flat for now — don't quote the 5/6-10/11+ tiers unless the memory file has been updated and confirmed with the user. |
| Minimum team size | No hard min, but "team discount" framing starts at ~5. Solo buyers go to public sessions. |
| Length | 5 hours, typically split across 2 days (matches Grain recordings he sends) |
| Default times | Nights + Saturdays for public; weekdays available for private |
| Pre-call | Yes, included. the user prefers it — it's how he customizes the through-line. |
| Recordings | Grain links he's sent before: Day 1 https://grain.com/share/recording/5dcf5f9d-ae9f-40a0-9ed5-c389e02da497/vNAyAnK2IHAfAZgYgwzK9pEu4J0VunN7K2ALTNU1  ·  Day 2 https://grain.com/share/recording/59e088f5-8c29-4bd4-8aa9-8db93040242d/nVoD0Uu9o9y30eXe9dOHJfOupMNUwuEueFCI4ycj . Tell people to start with the last 10 min of Day 2. |
| Curriculum through-line | One progressive example that builds across every module (setup/testing, deploying, md files + composition, skills/plugins/CLAUDE.md, APIs). Standard track ends in a **programmatic SEO skill** (searches competitors, finds high-ROI keywords, generates landing pages + blog posts + images in brand voice). Customizable. |
| Build time | Office-hours format at the end — everyone builds a shippable project of their choice. |
| Teaching style | Hands-on, live demo, debug-in-public when students get stuck. Not lecture. |
| Alumni benefit | Slack group with past students. Follow-on courses coming but not live. |
| Onboarding | After close: collect team member list → each gets onboarding flow → pre-call. |

## Template 1 — First-touch reply to a team inquiry form

Use when someone fills the team inquiry form (name/email/company/team size/message). This is the DocuSketch-pattern reply.

```
Hey [Name],

Great to meet you and hear about your team. Sounds like a good fit — you'll get huge leverage for a team at that stage, especially on a [marketing/product/ops] team.

Couple of questions:
1. Would you rather do the training all together or have team members join public sessions individually? I typically run nights and Saturdays, but for a private group I can fit a time during the week.
2. Any timing in mind?

Logistics on my end:
1. Team pricing is 20% off — $799/seat.
2. I do a pre-call (or send over a few questions if easier) so we can hone in on what you'd like to build and make it custom to your team.
3. Once we finalize, I'll get the team member list from you and send everyone an onboarding flow.

What else would be helpful to know?
```

**Tweaks by signal:**
- If their inquiry already mentioned specific tools (Jira, Excel, PowerPoint, etc.), drop the "especially on a [X] team" line and replace with: "Connecting Claude to [their tool] is exactly the kind of thing we'd build in the custom track."
- If team size < 5: soften pricing line to "I run team pricing at $799/seat for groups — happy to extend it to your group of [N]."
- If enterprise/formal tone from them: change "Hey" to "Hi" and add "the user" at the bottom.

## Template 2 — "What's your approach?" (curriculum/teaching style question)

This is the Nick Keyko / DocuSketch second-touch question. Paste this almost verbatim.

```
On the teaching approach:

1. There's one through-line example that builds progressively across each module — setup and testing locally, deploying, CLAUDE.md files and composition, skills/plugins, APIs. In the standard track it ends in a programmatic SEO skill that searches competitors, finds high-ROI keywords, and generates custom landing pages and blog posts with brand-voice images for those keywords. The through-line can be customized to your team's use cases.

2. We have build time at the end in an office-hours format where everyone ships a project of their choice.

I lean heavily toward getting hands dirty with exercises and live-demoing what students build or get stuck on. Not lecture.

What sorts of things is your team looking to automate or build?
```

## Template 3 — Pricing-only reply

When the question is just "how much?" or "how does it work — individual vs private?"

```
Two options:

1. Individual seats in public sessions — $999/seat, runs nights or Saturdays.
2. Private training for your team — $799/seat (20% off), 5 hours, scheduled whenever works for your team. Includes a pre-call so I can customize the build track to your use cases.

For a group of [N] the private option usually makes more sense — the whole class ends up aimed at your workflows instead of a mixed room.

[Scheduling question: "Any timing in mind?" OR discovery: "What are the main things you'd want them building by the end?"]
```

## Template 4 — "Can you share recordings?" (PayPal pattern)

```
Sure — here's a recorded class you can explore:

Day 1: https://grain.com/share/recording/5dcf5f9d-ae9f-40a0-9ed5-c389e02da497/vNAyAnK2IHAfAZgYgwzK9pEu4J0VunN7K2ALTNU1
Day 2: https://grain.com/share/recording/59e088f5-8c29-4bd4-8aa9-8db93040242d/nVoD0Uu9o9y30eXe9dOHJfOupMNUwuEueFCI4ycj

It's about 5 hours total. I'd start with the last 10 minutes of Day 2 — that's where students share what they found most useful — and then work backward from there.

This particular recording leans heavy on Claude Code. For your team I'd put more weight on [plugins / MCPs / Claude in the browser / Cowork / whatever their ask was], based on what you mentioned.

Do you have a timeframe you're hoping to pick a training partner by?
```

## Template 5 — Scheduling / close

```
Great — would [Date A], [Date B], or [Date C] work? I'll be unavailable [blackout dates if any].

Once you pick a date, send me the team member list and I'll get the onboarding flow out to everyone. I'll also schedule the pre-call with you (and whoever on your side should be in it) so we can lock in the through-line.
```

## Template 6 — Short warm ping back (Solv pattern)

Use when someone you already know DMs/emails with "do you still do private walkthroughs for teams?"

```
Hey [Name] — I do. For a group of ~[N] it's $799/seat (20% off list), 5 hours, whenever works for your team. I do a pre-call beforehand to tailor the build track to what the team actually wants to walk out with.

What's the team, and what are you hoping they'd be able to do after?
```

## Example: real reply to a warm alum (Solv / Evan Cory, Apr 9 2026)

Context: Evan took the public class already. He emailed asking if the user still does private walkthroughs for a group of ~10 on his product ops / partner success team, with Teresa cc'd. This is the approved reply the user sent. Use it as the reference for short, warm, alum-inbound pattern.

Key moves:
- Greets both people by name ("Hey Evan ... And nice to meet you Teresa.")
- Skips the full logistics list. Alum already knows teaching style, so it's cut entirely.
- Pricing quoted as "20% off the list price per seat" rather than a dollar number. Keeps flexibility.
- "Similar to what you went through but pointed at their workflows" — explicitly references shared context.
- Single discovery question at close, no scheduling question.
- ~95 words.

```
Hey Evan, good to hear from you. And nice to meet you Teresa.

Yep, still doing private team trainings. For a group of ~10 it'd be 20% off the list price per seat. 5 hours total, scheduled whenever works for your team. I'd do a pre-call with you and Teresa beforehand so we can tailor the build track to what product ops and partner success actually wants to walk out being able to do, similar to what you went through but pointed at their workflows.

What are the main things you'd want the team doing differently after the class?
```

**Generalizable lesson:** For alum inbounds, cut the teaching-style paragraph entirely. They already bought it once. Lead with "yep", price, pre-call, and the tailoring hook. Quote price as "20% off the list price" unless they ask for the exact number.

## FAQ micro-answers (drop-in lines)

Use inline when a thread has a specific question, instead of re-pasting a whole template.

- **"Is the pre-call included?"** → "Yes, included. I actually prefer it — it's how I customize the through-line so the class lands on your team's actual workflows instead of a generic demo."
- **"Do you have follow-on courses?"** → "Alumni get a Slack group with past students. Follow-on courses are planned but not live yet."
- **"Can we do it on a weekday?"** → "Yes — public sessions are nights and Saturdays, but private team trainings I schedule whenever works for your group."
- **"Can you connect Claude to [Jira/Slack/Gmail/Excel]?"** → "Yes — connecting to [tool] is a good fit for the custom track. We'd cover MCPs and build at least one working integration during class."
- **"How custom is 'custom'?"** → "The skeleton is the same — setup, deploying, CLAUDE.md, skills/plugins, APIs — but the example we build as we go gets swapped for something your team will actually use. Past teams have built programmatic SEO skills, internal research tools, lead-gen automations, monthly newsletter pipelines."
- **"Why should we pick you over [Anthropic docs / learnclaude / internal L&D]?"** → "Docs teach syntax. This class teaches you how to ship something real by the end of Day 2. The audience is also built for PMs, marketers, and operators — not engineers — so the examples aren't throwaway todo apps."
- **"Can we get a discount beyond 20%?"** → "The $799 is already the team rate. If you're doing 10+ I can look at it — what size group are we talking?"

## Workflow for this skill

When the user says "draft a reply to [the team lead]" or "write the pitch for [X]":

1. Pull the latest inbound from `gmail-example-agency` (or wherever the thread lives). Read the full thread, not just the latest message.
2. Identify which template fits (first-touch / approach / pricing / recordings / scheduling / short ping).
3. Fill in the name, company, team-size signal, and ONE specific hook from their message ("marketing team", "Jira integration", "pretty busy next month").
4. Keep total length under ~180 words unless the user asks for more.
5. Show the draft. Do NOT send. (See memory: `feedback_never_send_without_approval.md`.)
6. After the user approves, send via the `gmail-example-agency` skill.

## Things to NOT do

- Don't use "I hope this finds you well," "Thanks for reaching out!," "I'd love to jump on a call to discuss further." the user doesn't talk like that.
- Don't sell features — sell leverage and what they'll walk out with.
- Don't list 6 questions. Two max.
- Don't quote pricing tiers that aren't in the "facts" table above without checking with the user.
- Don't offer the $699/deal link to team inquiries — that's reserved for public session fill urgency.
- Don't invent testimonials. If you want social proof, pull a real name from `.claude/plugins/marketing-brain/state/insights.md` (Dasha/Kevin/Jake/Seth/Evan Cory/AJ/Jonathan/Danilo).
