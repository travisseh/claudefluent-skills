---
name: internal-marketing
description: "Produce internal Slack announcements for a feature release — tailored messages for CS (activation/retention), Sales (pitching/positioning), Marketing (ads/campaigns), plus a combined update. Use this skill whenever the user says 'internal marketing', 'internal launch', 'write a battlecard', 'CS enablement', 'sales enablement', 'feature announcement for the team', 'prep CS and sales', 'how do we tell the team about this feature', 'write release comms', 'internal marketing for this feature', or when a feature ships and internal teams need to know about it. Also trigger on '/internal-marketing'."
---

# Internal Launch

Take a feature release and produce Slack announcements that help CS activate and retain customers, and help Sales pitch confidently. The goal is to make every internal stakeholder care about this feature — not because product told them to, but because they can see exactly how it helps them do their job better.

## Workflow

### Step 1: Gather Context (ask until you have enough)

Start with whatever the user gives you — even a single sentence is fine. Then ask targeted follow-up questions using AskUserQuestion until you can confidently write for both audiences. Fill in what you can from the ExampleCo codebase, git history, or product context before asking.

**Where to look in the codebase:** The ExampleCo v2 app lives at `~/Programming/exampleco`. Before searching, always pull latest main:
```bash
git -C ~/Programming/exampleco fetch origin main && git -C ~/Programming/exampleco reset --hard origin/main
```
Search routes, components, and schemas there to understand how features work, what the UI looks like, and what the setup steps are. This is the source of truth for how things work in-product.

You need to understand these things before drafting. Ask about whichever ones you can't figure out yourself:

**For CS (activation & retention):**
- How does CS turn this on for a customer? Walk me through the exact steps — what do they click, toggle, or configure? (This is critical — CS needs a concrete how-to, not a concept explanation. Always ask for this.)
- Which customers benefit most — net-new accounts in onboarding, active accounts, or at-risk/low-engagement accounts?
- Are there any gotchas or limitations CS should set expectations on?
- Does this change how CS should talk to customers at different lifecycle stages?

**For Sales (pitching & positioning):**
- What customer objection or competitor gap does this address?
- How does this compare to what Owner.com / SpotHopper / competitors offer?
- What's the one-liner a rep could drop into a pitch without prep?
- Does this change the overall value story or packaging?

**For Marketing (ads, campaigns, website):**
- Is there a compelling external-facing angle — something that would work in an ad or on the website?
- Does this create a new differentiator we should be shouting about vs. competitors?
- Is there a customer-facing name or framing that's different from the internal name?

**For all:**
- Is there a URL or screen path to link to or demo?
- Are there screenshots in `.claude/skills/internal-marketing/screenshots/`?

Keep the questions conversational and batched (2-3 at a time max, not a wall of questions). If the user's answers are brief, that's fine — work with what you get. The point is to ask the right questions, not to extract a PRD.

### Step 2: Prepare Demo Data, Screenshots, and Armory Assets

Before drafting, create a screenshot package that tells the feature story clearly. Do this proactively unless the user explicitly says he only wants copy.

1. **Seed a compelling local demo**
   - Use the ExampleCo app at `~/Programming/exampleco`.
   - Pull latest main first, then get the app running locally.
   - Prefer the repo's normal seed flow (`make setup-db`, `make seed`, or `npm run seed`) when available.
   - If the default seed data makes the feature look empty, weak, or confusing, add local-only demo rows that tell a better story:
     - Use realistic restaurant/account/location names already in seed data when possible.
     - Create enough records to show the real workflow, not just a happy-path shell.
     - For leaderboards, dashboards, analytics, activity feeds, and similar surfaces, use credible high numbers and enough participants/items to make the UI persuasive.
     - Keep this to local/dev data unless the user explicitly asks for durable seed changes in the product repo.
   - Document any local-only data changes in the response so the user knows what was staged for screenshots.

2. **Capture high-ish resolution screenshots**
   - Use Playwright/browser automation rather than manual screenshots.
   - Capture the screens a teammate would need to understand and reuse the feature:
     - Admin/configuration surface.
     - Customer/user-facing surface.
     - Any dashboard, leaderboard, preview, or result state that sells the value.
     - Mobile views when the product surface is mobile-first.
   - Use high-resolution captures:
     - Desktop: wide viewport with 2x DPR when practical.
     - Mobile: phone-shaped viewport with 3x DPR when practical.
   - Avoid screenshots that cut off the thing being announced. If the valuable part is below the fold, use a taller viewport, scroll intentionally, or take a second screenshot.
   - Put launch-relevant screenshots in `.claude/skills/internal-marketing/screenshots/` with descriptive filenames. Screenshots accumulate there, so never delete old launches.

3. **Add reusable assets to Armory**
   - The Armory repo lives at `~/Programming/armory`.
   - Add the screenshots under the Armory Visual Assets area, usually as a feature folder such as `visual-assets/<FeatureName>/`.
   - Update Armory's `index.html` so Visual Assets shows a folder/card for the feature, and clicking into it reveals the screenshots.
   - Verify locally with a static server and browser automation that:
     - The folder/card appears under Visual Assets.
     - Clicking it reveals only the relevant screenshots.
     - Clicking an image opens the existing preview modal or direct image view.
   - If the user asked to publish Armory changes, commit and push only the relevant Armory files. Leave unrelated dirty files untouched.

4. **Make screenshots available in the Slack preview**
   - Include the relevant screenshot filenames in the preview server `screenshot_filter` argument.
   - In each drafted Slack message, include a short `[Screenshot: filename]` or `[Screenshots available in preview]` placeholder where the image should be attached.
   - If the assets were added to Armory, include the Armory path or URL in the messages when useful, especially for Sales/Marketing reuse.
   - The preview UI starts with screenshots unselected, so tell the user which screenshots to attach to each channel if the choice matters.

### Step 3: Draft the Three Slack Messages

Once you have enough context, draft all three messages and present them for review. Do NOT send anything yet.

Present them clearly labeled so the user can scan and edit:

---

**Message 1 — #home-sales**

Framed as "here's a new weapon for your pitch." Lead with the competitive angle or objection it handles. Include a one-liner and brief talk track.

```
[emoji] *Bold headline — what this means for sales*

[2-3 sentences: what customer problem this solves, how to pitch it, what competitor gap it fills]

[One-liner a rep can use on a call]

[Screenshot if available]

[Link to feature or demo path]
```

---

**Message 2 — #home-cs**

Framed as "here's how to activate this with your customers." Lead with the customer segment that benefits most and what CS should actually do.

```
[emoji] *Bold headline — what this means for CS*

[2-3 sentences: what it does, which customers to tell first, how to introduce it]

*How to turn it on:*
1. [Exact step — e.g. "Go to Settings > Features > Toggle on Review Responder"]
2. [Next step]
3. [How to verify it's working]

[Screenshot if available]

[Link to feature]
```

The how-to steps are the most important part of the CS message. CS reps need to know exactly what to click — don't skip this or make it vague. If the user hasn't provided the steps yet, always ask before drafting.

---

**Message 3 — #ids-marketing**

Framed as "here's something you can use in marketing." Lead with what's compelling about this for ads, social, website copy, or campaigns. Help marketing understand the story they can tell externally.

```
[emoji] *Bold headline — what this means for marketing*

[2-3 sentences: what the feature does in customer-facing language, why it's a differentiator, how it could show up in ads/campaigns/website]

[Suggested angle or headline for external use]

[Screenshot if available]

[Link to feature]
```

---

**Message 4 — #pulse-prod-updates**

Combined version for the broader team. Brief summary, then a bullet each for CS, Sales, and Marketing so anyone scanning gets all angles.

```
[emoji] *Bold headline — what shipped*

[1-2 sentences: what was built and the customer problem it solves]

- *For CS:* [one line on how to activate with customers]
- *For Sales:* [one line on how to pitch it]
- *For Marketing:* [one line on how to use in ads/campaigns]

[Screenshot if available]

[Link to feature]
```

---

### Step 4: Launch Preview Server

Launch the preview server so the user can edit messages in a browser UI and send them himself. The server provides a WYSIWYG editor for each channel, screenshot selection, a "Preview to Me" button (sends to the user's DM), and a "Send All" button (sends to real channels).

```bash
npx tsx .claude/skills/internal-marketing/preview-server.ts [port] '[messages_json]' '[screenshot_filter]'
```

- **port**: random port (3990-3999)
- **messages_json**: JSON array of `{channel, channelName, content}` objects
- **screenshot_filter** (optional): comma-separated list of screenshot filenames to include. Only pass screenshots relevant to this launch - don't include screenshots from previous launches. If omitted, all screenshots in the folder are shown. Prefer passing the filter every time.

Example:
```bash
npx tsx .claude/skills/internal-marketing/preview-server.ts 3991 '[
  {"channel": "home-sales", "channelName": "home-sales", "content": ":rocket: *Feature is live*\n\nMessage here"},
  {"channel": "home-cs", "channelName": "home-cs", "content": ":rocket: *Feature is live*\n\nCS message here"},
  {"channel": "ids-marketing", "channelName": "ids-marketing", "content": ":rocket: *Feature is live*\n\nMarketing message here"},
  {"channel": "pulse-prod-updates", "channelName": "pulse-prod-updates", "content": ":rocket: *Feature is live*\n\nCombined message here"}
]' 'screenshot1.png,screenshot2.png'
```

Then open the URL in the browser. The UI has:
- WYSIWYG contenteditable editors with formatting toolbar (bold, italic, code, lists)
- **Paste an image** directly into any editor — it uploads to the screenshots folder and auto-attaches to that channel
- Screenshot thumbnails — all unselected by default, click to attach
- Per-channel "Preview to Me" and "Send" buttons
- "Preview to Me" button - sends all messages to the user's DM (`D04PL43A3GF`) for Slack preview
- "Send All" button - sends to the real channels

After launching, tell the user: "Preview server is running at http://localhost:[port] - edit the messages there, hit Preview to Me to check how they look in Slack, then Send All when ready."

### Step 5: Handle Feedback

If the user comes back with feedback (e.g. "change X on the sales message"), first pull his current edits from the preview server before making changes:

```bash
curl -s http://localhost:[port]/state
```

This returns the current state of all messages as edited in the browser. Use this as the starting point for any changes - don't overwrite his edits by starting from scratch. Apply his feedback to the current state, then relaunch the preview server with the updated messages.

### Step 6: Done

Once the user sends from the UI, confirm the server can be killed. No further action needed from Claude.

## Tone and Voice

- **Always run messages through `/user-writing-style` before previewing.** The messages should sound like the user wrote them, not a press release.
- Use :rocket: emoji on the headline. No other emojis.
- Write for teammates, not press releases. Casual, direct, no buzzwords.
- CS materials should feel like a helpful playbook — "here's exactly what to do."
- Sales materials should feel like ammunition — "here's how to win with this."
- Always lead with the customer problem, never the feature name.
- Use restaurant-industry language where possible (guests, regulars, locations, operators).
- **Don't embellish or overstate what a feature does.** Describe it accurately. If it's a phone tree, call it a phone tree — don't call it an "AI-powered phone system" unless it actually is.
- **Don't add unsolicited sales advice** like "this isn't something to lead with" or "only mention this if..." — just give them the pitch and let them decide when to use it.
- **CS setup steps should be concise and direct** — numbered steps with exact clicks, no extra explanation. If the feature was discussed in a team meeting (WAGMI, standup, etc.), reference it.

## ExampleCo Context

Reference these when framing features:

- **Core purpose**: Find new guests, turn them into regulars.
- **Value delivery**: Turn guest touch-points into ongoing connection. Employ behavioral design to create profitable relationships. Overwhelm operators with competence. Orient on measurable outcomes.
- **Current competitive frame**: ExampleCo vs Owner.com and SpotHopper — we differentiate through gamification, in-store physical touchpoints (tapcards/signage), and text-based engagement.
- **Product surface areas**: Texting/campaigns, TapCards, review management, SEO, signage, onboarding, websites (coming).

## Screenshots

The skill has a screenshots folder at `.claude/skills/internal-marketing/screenshots/`. This folder may contain screenshots from multiple launches - always filter to only the ones relevant to the current launch.

1. Check if the user has dropped screenshots into this folder for the current feature.
2. If screenshots exist, determine which ones are relevant (by filename or by reading them). Only pass relevant screenshots to the preview server via the filter argument.
3. If no relevant screenshots exist, ask the user if he wants to add some before launching the preview server.
4. Screenshots accumulate across launches - never delete old ones, but always filter when launching the preview server.

## Optional Extras

After sending, offer these if relevant (don't push them every time):

- Save a battlecard to Notion using `/notion-exampleco`
- Record a walkthrough using `/record-demo`
- Generate sales validation questions to send to a rep for messaging feedback
