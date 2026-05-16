---
name: pre-mortem
description: Stress-test high-stakes plans by predicting failure modes, mapping the golden path, forecasting success, and naming the next bottlenecks. Use for trainings, paid engagements, pitches, partnerships, equity deals, real estate purchases, hires, launches, product bets, talks, contracts, career decisions, or multi-day engagements. Trigger on "pre-mortem this", "stress test this plan", "what could go wrong", "golden path", "10x agency", "next bottleneck", "red-team this", or stakes language like "big week ahead", "important meeting", "pitching X", "signing with Y", or "launching Z". Apply when cost of failure exceeds cost of planning, including over $10k revenue/spend/risk, more than 1 day prep, customer-facing, partnership/contract, or irreversible decisions. Skip low-stakes reversible choices.
---

# Pre-Mortem

## Origin story

This skill exists because on **April 22, 2026** the user ran a team training for Solv Health where the MCP access his exercises depended on wasn't confirmed beforehand. Session 1 was hobbled — participants couldn't run the core exercises and he had to scramble. A 30-minute pre-mortem two weeks earlier ("what has to be true for each exercise to work?") would have surfaced the MCP access question and let him resolve it ahead of time.

the user defaults to optimism. He commits fast and assumes things will work. That's a strength when pursuing opportunities and a liability when the downside is asymmetric.

But pure adversarial thinking is also incomplete. The real job is not only "don't fail." It is to find the **golden path**: the version where things work out unusually well, then reason backward to the moves that make that outcome more likely. If a plan works, the version of him a year from now needs to know what to systematize **now** so the success doesn't break him. So this skill does four things:

1. **Pre-mortem (failure side):** what kills this, ranked, with leading indicators
2. **Golden path (agency side):** what would perfect-but-plausible success look like, and what actions increase the odds
3. **Pre-success (forecast side):** what does the win actually look like at 1m / 3m / 6m / 1y
4. **Bottleneck radar:** if the key input or the user's agency 10x'd tomorrow, what breaks first — that's what to systematize now

## When to invoke this

**Apply it when the cost of failure or the cost of unprepared success exceeds the cost of planning.** Specifically:

- Anything >$10k in revenue, spend, or risk
- Anything requiring >1 day of focused prep
- Customer-facing events (trainings, demos, pitches, workshops)
- Partnership decisions or contract signings
- Irreversible decisions (hires, firings, equity deals, major purchases, public launches)
- Anything where a 10x increase in scale is plausible within 12 months and would expose hidden bottlenecks (course growth, lead volume, headcount, ops load)
- Any strategic moment where the user is choosing between paths and needs the "golden path" rather than merely a risk list

**Skip it for:**

- Daily operational decisions
- Reversible, low-stakes choices
- Anything under the thresholds above

If in doubt, ask: *"If this goes sideways OR goes much better than expected, will I wish I'd spent 30 minutes thinking about it first?"* If yes, run it.

## Tone

**On failure side: direct, skeptical, adversarial.** Not reassuring. The whole point is to counteract the user's optimism — if he's doing something dumb, say so plainly. No sycophancy. No "this looks great, but here are some minor considerations."

**On success side: ambitious, concrete, specific.** Not cheerleading. Project realistic outcomes if execution holds — name the numbers, the customers, the calendar pressure, the staffing implications. Make the future visible enough that he can prepare for it.

**On golden-path side: agentic, causal, practical.** Ask: "If things worked out perfectly, what would have happened?" Then work backward to the few moves that made it happen. Do not merely recommend doing more of everything. Name the decisive moves, negotiation frames, partnerships, offers, proof points, and constraints that matter.

**On bottleneck side: physical, mechanical, unromantic.** A bottleneck is a machine part that breaks. Name it. ("Sales calls is the next break point — at 10x leads you'd need 4 closers and you have zero.")

Signs you're doing it wrong:
- Listing risks without ranking them
- Suggesting mitigations without early warning signs
- Hedging ("it could go well, but...")
- Avoiding naming the real problem
- Golden path is generic ("focus more") instead of causal ("secure $30k/month guaranteed revenue through a PE portfolio training deal, then quit safely")
- Success forecast is generic ("growth continues") instead of specific (numbers, names, calendar load)
- Bottleneck list is just "do better at X" instead of "X function/system breaks at this volume"

## Workflow

### 1. Capture the event

If the user hasn't already described it, ask in a single batched message:

- **What is it?** (training / pitch / deal / launch / hire / etc.)
- **When is it?** (date + time-to-event)
- **Who else is involved?** (counterparty, attendees, decision-makers)
- **What's at stake?** ($ amount, reputation risk, opportunity cost)
- **What does success look like?** (concrete outcome — be specific)
- **If things worked out perfectly, what would be true?** (the golden path)
- **What would you do if you had 10x the agency?** (the bold move, deal, ask, hire, package, or constraint change)

If the event is already clearly described, skip straight to analysis. Don't make the user repeat himself.

### 2. Run the failure analysis (pre-mortem)

Same structure as before — 5-8 failure modes, ranked, with leading indicators and concrete mitigations. See "Output structure" below.

### 3. Find the golden path

Before forecasting, force the perfect-but-plausible case:

> **"How would this look if things worked out perfectly?"**

Then answer:

- **Perfect outcome:** the concrete state the user actually wants, not the polite compromise
- **Backward chain:** the 3-5 things that had to happen to create that outcome
- **Decisive move:** the one move that most increases the odds
- **Non-obvious constraint:** the hidden blocker that must be removed
- **What to stop doing:** the activity that feels productive but does not move the golden path

Then apply the agency lens:

> **"What would I do if I had 10x the agency?"**

This is not fantasy bravado. It means: if the user assumed he could make bold asks, structure deals, recruit help, impose constraints, and create leverage, what would he do? Look for guaranteed revenue, asymmetric partnerships, sharper negotiation asks, distribution shortcuts, pricing changes, and ways to buy back time.

### 4. Ask the success-projection questions

Before forecasting, ask **only the questions you actually need** to project the success case with specificity. Pick the 3-6 most load-bearing. Examples by event type:

- **Course / training launch:** What's a realistic conversion rate from the audience you're reaching? What's your pricing? What's your delivery capacity per month before quality degrades? Who's the next-hire trigger?
- **Partnership / co-founder deal:** What does month-1 success output look like? At what revenue level does this person become full-time? What's the equity vesting cadence? Who owns which decisions?
- **Product launch:** What's the activation rate you'd consider successful? How many customers in the addressable base? What's the support load per active customer? At what MAU does the current infra/team break?
- **Sales engagement:** What's the deal size? What's the typical sales cycle? How many similar deals are in the pipeline? What's the expansion path post-close?
- **Hire:** What does a "this hire is working" outcome look like at 90 days? What's the manager's capacity to onboard? What does this role unlock at 6 months?

Ask these as a single batched question. Don't drip them. If the user can't answer one, note it as an unknown and project a range.

### 5. Generate the success forecast

Project at **1 month, 3 months, 6 months, 1 year**. Each window should include:

- **What's true by then** (concrete numbers, customers, milestones)
- **What you're spending time on** (calendar shift)
- **What's getting hard** (early stress signs)

This isn't a happy-path fantasy. It's the realistic outcome **if execution holds.** Include the strain that comes with success, not just the wins.

### 6. Run the 10x bottleneck and agency check

For the key input that drives this initiative — leads, customers, hires, deals, projects, hours — ask:

> **"If I 10x'd this input tomorrow, what would break first?"**

Also ask:

> **"If I had 10x the agency, what would I do differently?"**

Use this to surface the bolder version of the plan: the guaranteed-revenue deal, bigger equity ask, sharper customer segment, narrower offer, hired operator, affiliate army, calendar boundary, or direct conversation the user is avoiding.

Identify the **next 2-3 bottlenecks**. For each:

- **The bottleneck** (the specific function/system/person that breaks)
- **Why it breaks at 10x** (the mechanical reason)
- **What to systematize now** (concrete prep work — hire, doc, automate, partner, redesign)

Examples of well-named bottlenecks:
- "Sales-call capacity. You'd need 4 closers; you have zero. Systematize: build a 3-call qualification → close playbook now so a contractor can run it later."
- "Onboarding live touch. You're in every kickoff. Record an async onboarding sequence + a 'first 10 minutes of class' video so cohorts >30 don't require you."
- "Code review queue. You're the only senior. Document the top 5 review patterns and pair-review with a junior weekly so they can lead reviews by Q3."

### 7. Save it to the Notion AI Output Library

Save the pre-mortem as a page in the **AI Output Library** Notion database so it lives alongside other durable AI outputs and is searchable across sessions. Do NOT save to the local `archives/` directory — Notion is the system of record now.

**Steps:**

1. Write the full markdown to a temp file:
   ```bash
   cat > /tmp/pre-mortem.md <<'EOF'
   <full pre-mortem content>
   EOF
   ```

2. Save via the notion-ai CLI (do NOT use Notion MCP):
   ```bash
   node ~/.config/notion-tools/notion-ai.js create \
     "Pre-Mortem: <event name>" \
     "<Area>" \
     "<Initiative>" \
     @/tmp/pre-mortem.md \
     type=Brief \
     source="Claude Code /pre-mortem session YYYY-MM-DD" \
     tags=pre-mortem,<other-relevant-tags>
   ```

   **Title format:** `Pre-Mortem: <event name>` — e.g. `Pre-Mortem: Solv Health team training`, `Pre-Mortem: Nan (Kaiyo) Ads Partnership for ClaudeFluent`.

   **Area:** ClaudeFluent / ExampleCo / ReviewCo / Bishopric / Steph-Carson / Mother-Padre / Life Admin (pick the closest).

   **Initiative:** Marketing / Ops / Student Experience / Product / Demand Gen / Admin / Sell Prep / Strategic (pick the closest — partnerships → Demand Gen or Strategic, hires → Ops, product launches → Product).

   **Type:** Always `Brief` (pre-mortems are recommendation/plan documents).

   **Tags:** Always include `pre-mortem`. Add 2-4 more (e.g. `partnership`, `team-training`, `hire`, `launch`, `paid-ads`, counterparty name).

3. The CLI returns the page ID and URL. Show the URL to the user.

4. Tell the user: *"Saved to Notion AI Output Library: <url>. After the event, run `/pre-mortem compare <url-or-page-id>` to see which risks materialized and which success projections played out."*

### 8. Post-mortem compare (when invoked with `compare` or `review`)

If the user asks to review a past pre-mortem after the event:
- Find the page: list with `node ~/.config/notion-tools/notion-ai.js list area=<Area>` and grep for `pre-mortem`, OR if he gives the URL/ID, use it directly.
- Read the page: `node ~/.config/notion-tools/notion-ai.js read <pageId>`
- Ask him (briefly) what actually happened
- Append a "## Post-Mortem" section via:
  ```bash
  cat > /tmp/post-mortem.md <<'EOF'
  ## Post-Mortem (added YYYY-MM-DD)
  <which risks materialized, which were overblown, which were missed;
   which success projections played out, which were optimistic, which were under-called;
   which bottlenecks actually broke;
   what pattern to add to future runs>
  EOF
  node ~/.config/notion-tools/notion-ai.js append <pageId> @/tmp/post-mortem.md
  ```

## Output structure

```
# Pre-Mortem: <event name>
**Date:** YYYY-MM-DD | **Event date:** YYYY-MM-DD | **Stakes:** <$ / reputation / other>

## The ways this fails
<5-8 failure modes, ranked by likelihood × impact. Most dangerous first.>

### 1. <Failure mode — short declarative name>
- **Likelihood:** High / Medium / Low
- **Impact:** High / Medium / Low
- **Early warning signs:** <what would you see in the days before that signals this is about to happen>
- **Leading indicator:** <the single specific thing to watch now>
- **Mitigation (do this now):** <concrete action, not "think about X">

### 2. <next failure mode>
...

## Worst case: the story of how this goes wrong
<A 4-6 sentence narrative. Past tense, as if recapping the disaster a week later. Concrete details. Name the moment things turned.>

## Golden path: if this works perfectly
- **Perfect outcome:** <the concrete outcome the user actually wants>
- **Backward chain:** <3-5 conditions/actions that created it>
- **Decisive move:** <the highest-leverage move to make now>
- **Non-obvious constraint:** <the blocker to remove>
- **What to stop doing:** <the attractive distraction or low-leverage activity to cut>

## 10x agency lens
**If the user had 10x the agency, he would:**
- <bold but practical move: guaranteed revenue deal, bigger ask, partner structure, hire, pricing shift, distribution shortcut>
- <second move>
- <third move>

## Questions before I forecast the win
<3-6 batched questions you need answered to project specifically. Skip this section in the saved archive once answered — keep the answers inline below.>

## If this works: the next year
### 1 month from now
- **What's true:** <concrete state — numbers, customers, milestones>
- **Where your time goes:** <calendar shift>
- **What's getting hard:** <early strain>

### 3 months from now
- **What's true:**
- **Where your time goes:**
- **What's getting hard:**

### 6 months from now
- **What's true:**
- **Where your time goes:**
- **What's getting hard:**

### 1 year from now
- **What's true:**
- **Where your time goes:**
- **What's getting hard:**

## Best case: the story of how this works
<A 4-6 sentence narrative. Past tense, as if recapping the win a year later. Concrete numbers. Name the inflection point.>

## Next bottlenecks (10x test)
**The key input here is: <leads / customers / cohorts / deals / projects / hours / hires>.**
**If that 10x'd tomorrow, here's what breaks first:**

### Bottleneck 1: <name the function/system/person>
- **Why it breaks:** <mechanical reason at 10x>
- **Systematize now:** <concrete prep work>

### Bottleneck 2: <name>
- **Why it breaks:**
- **Systematize now:**

### Bottleneck 3 (if applicable): <name>
- **Why it breaks:**
- **Systematize now:**

## Make the golden path more likely
- **Do now:** <1-3 actions that directly increase odds of the perfect outcome>
- **Negotiate/ask:** <the explicit ask, deal structure, or boundary>
- **Systematize:** <what needs to exist so success does not remain the user-shaped>
- **Kill/defer:** <what to stop spending attention on>

## Contingency checklist
**Next 24 hours:**
- [ ] <specific action — failure-side prep>
- [ ] <specific action — golden-path prep>
- [ ] <specific action — bottleneck-side prep>

**Next 48-72 hours:**
- [ ] <specific action>
- [ ] <specific action>

**Before the event:**
- [ ] <specific action>

## Gut check: would you still do this?
<Honest take. Given what surfaced on BOTH sides, is this still the right call? Options:
- "Yes, proceed — but do X, Y, Z first (failure prep) and start systematizing A (bottleneck prep)"
- "Yes, but renegotiate scope/price/timing"
- "No — the downside isn't worth it. Here's how to exit cleanly"
- "Yes, and the success case is bigger than you're acting on — staff/invest harder now"
- "Not enough info — get answers to these questions before committing"

Pick one. Don't hedge across multiple.>
```

## Quality bar — examples

Study these to calibrate output quality. The examples show specificity, adversarial-on-failure tone, ambitious-on-success tone, and bottleneck discipline.

### Example 1 — Team training (the Solv Health case)

```
# Pre-Mortem: Solv Health team training (4-hour Claude Code workshop, 15 engineers)
**Date:** 2026-04-08 | **Event date:** 2026-04-22 | **Stakes:** $15k + reference customer for future team deals

## The ways this fails

### 1. Exercises require tools participants can't access
- **Likelihood:** High
- **Impact:** High — kills the session, I look unprepared, no referral
- **Early warning signs:** Nobody has asked about setup yet. I haven't sent a pre-session checklist. I haven't seen one participant's terminal.
- **Leading indicator:** No confirmation email from their IT/eng-ops about MCP server whitelisting in the last 7 days.
- **Mitigation (do this now):** Send a 5-item pre-flight checklist TODAY — Claude Code installed, MCP servers whitelisted (list specific ones), GitHub access, sandbox repo cloned, API key issued. Require a green reply from at least 10/15 by April 18 or cut MCP exercises.

### 2. The "right" use case doesn't match their actual work
- **Likelihood:** Medium
- **Impact:** High — they leave thinking "cute demo, doesn't apply to us"
- **Leading indicator:** No 15-minute call scheduled with a rank-and-file engineer before April 18.
- **Mitigation (do this now):** Schedule two 15-min calls with engineers on the team this week. Ask: "What did you ship last week? What slowed you down?" Rewrite one exercise to match.

### 3. Room/AV setup eats the first 20 minutes
- **Likelihood:** Medium | **Impact:** Medium
- **Mitigation:** Book a 15-min tech check with their IT for April 21. Bring HDMI + USB-C dongles. Have a backup hotspot.

### 4. One vocal skeptic derails the room
- **Likelihood:** Medium | **Impact:** Medium
- **Mitigation:** Prepare the "here's what Claude Code is NOT" slide. Name the skepticism before a skeptic does.

### 5. They love it but don't convert to ongoing engagement
- **Likelihood:** High | **Impact:** Low short-term, High for business model
- **Mitigation:** End with a clear CTA. "Office hours for 2 weeks post-training, $X for 5 seats on the monthly cohort, $Y for a custom MCP build."

## Worst case: the story of how this goes wrong

April 22, 9:05am. I open the laptop, pull up exercise 1. Participants get stuck on step 2 — the MCP server isn't whitelisted on their network. I improvise but three people tune out and open Slack. By the break I've lost the room. Session 2 dumps MCP content, but they leave thinking "Claude Code is kinda cool." The champion is polite. No referral. The reference customer pipeline I was building dies on the vine.

## Questions before I forecast the win
1. If Solv refers 1 team training in the next quarter, what's a realistic close rate on those referrals?
2. What's the right price for a follow-on engagement (custom MCP build, monthly cohort seats, ongoing office hours)?
3. How many team trainings can you deliver per month before quality degrades or it eats ExampleCo time?
4. Is the goal of this channel to build a teaching business or to source 1-2 high-leverage relationships?

## If this works: the next year

### 1 month from now
- **What's true:** Solv has an internal "Claude Code is now standard" announcement. 8/15 engineers have shipped at least one Claude-Code-built feature. You have 1-2 testimonial quotes and a written case study draft.
- **Where your time goes:** 2 follow-up office hours (1hr/wk), case study writing, 1 referral intro from Solv to another mid-size eng team.
- **What's getting hard:** Outbound is replaced by referral inbound but you have no qualification process — every intro consumes 90 minutes.

### 3 months from now
- **What's true:** 3 team-training engagements closed at $15-25k each. Cohort sales lifted 20% from referral halo. ClaudeFluent at $35-40k MRR.
- **Where your time goes:** 60% delivery (training + cohorts), 20% sales calls, 20% content. ExampleCo is a real squeeze.
- **What's getting hard:** Sales-call capacity. You're the only person who can close. Content production is slipping because delivery is up.

### 6 months from now
- **What's true:** 8-10 team trainings delivered. ClaudeFluent at $60-80k MRR. You've hired 1 contractor for either delivery or sales.
- **Where your time goes:** 30% delivery (you only run flagship sessions), 30% sales, 20% product/curriculum, 20% content.
- **What's getting hard:** Curriculum staleness — Claude Code releases faster than your slides. Quit-ExampleCo conversation is no longer hypothetical.

### 1 year from now
- **What's true:** ClaudeFluent at $120k+ MRR with team trainings as the primary channel. 2-3 named reference customers (Solv was the first). You've made the ExampleCo decision.
- **Where your time goes:** Setting standards, closing flagship deals, managing a small team or contractor bench.
- **What's getting hard:** Operational debt — billing, scheduling, customer-success handoffs are all you-shaped and don't survive scale.

## Best case: the story of how this works

April 22, 4pm. The room ships a small feature live during the workshop. Three engineers DM you that night asking how to do X with Claude. The Solv champion intros you to a peer at a Y Combinator company in early May. You close that deal at $20k. By July you've delivered 4 team trainings, all sourced from the Solv halo. The case study lives on the homepage. The cohort fills automatically.

## Next bottlenecks (10x test)

**The key input here is: team-training inbound leads.**
**If that 10x'd tomorrow:**

### Bottleneck 1: Sales-call capacity
- **Why it breaks:** You're the only person who can run a discovery → close call. At 10 leads you handle it; at 100 leads you can't, and you start dropping intros.
- **Systematize now:** Document a 3-call qualification → demo → close playbook. Record one of each call type as a training reference. Identify the contractor or junior closer profile you'd hire (likely SDR-level + Claude-Code-fluent).

### Bottleneck 2: Custom-curriculum delivery
- **Why it breaks:** Each team wants their stack reflected in exercises. At 10 trainings/year you can hand-tailor; at 100 you can't.
- **Systematize now:** Build a modular exercise library indexed by stack (Python/Django, Node/React, Go, Ruby). Pre-record stack-specific intros. Make tailoring a 2-hour swap, not a 2-day rewrite.

### Bottleneck 3: Reference-customer follow-through
- **Why it breaks:** Case studies and testimonials are written by you, manually. At 10 customers you can; at 100 you can't.
- **Systematize now:** Build a post-engagement template — auto-survey at day 30, structured testimonial prompt, case-study skeleton — so 80% of the writeup is filled in by the customer.

## Contingency checklist

**Next 24 hours:**
- [ ] Draft + send the 5-item pre-flight checklist to the Solv champion (failure prep)
- [ ] Sketch the 3-call sales playbook in a Google Doc — even a rough v1 (bottleneck prep)

**Next 48-72 hours:**
- [ ] Confirm MCP server whitelist status in writing
- [ ] Run the two 15-min engineer calls
- [ ] Identify your first stack-specific exercise template (Solv's stack) so it's reusable

**Before the event:**
- [ ] Tech check on April 21
- [ ] Dry run both sessions with a stopwatch
- [ ] Prep the "what Claude Code is NOT" opener
- [ ] Draft the post-training CTA email AND the testimonial-request template

## Gut check: would you still do this?

Yes, proceed — but **do not run this training with MCP exercises until you have written confirmation of whitelisting.** And: the success case here is bigger than you're acting on. If this works, your bottleneck within 6 months is sales-call capacity, not lead volume. Start documenting the playbook NOW so the contractor/closer hire in month 4 isn't from-scratch. The $15k fee is the smallest stake in this room — the channel is the prize.
```

## Notes on applying these examples

- **Specificity matters on both sides.** "Growth continues" is not a forecast. "$60-80k MRR with 8-10 trainings delivered, you've hired 1 contractor" is.
- **Rank failure modes ruthlessly.** Don't list 12 risks equally. Top 2-3 are almost always what kills it.
- **Forecast the strain, not just the wins.** A success case where everything is rosy is a fantasy. Name what gets hard.
- **Bottlenecks are mechanical, not motivational.** "Be more disciplined" is not a bottleneck. "Sales-call capacity at 4 closers needed, 0 hired" is.
- **Leading indicators beat lagging ones** on both failure and success sides.
- **The gut check is the output.** Everything above it is evidence. the user should walk away knowing what to do differently — both to avoid the failure and to be ready for the win.

## Notion page title format

Use: `Pre-Mortem: <event name>`

Examples:
- `Pre-Mortem: Solv Health team training`
- `Pre-Mortem: Cam partnership equity deal`
- `Pre-Mortem: ExampleCo websites launch`
- `Pre-Mortem: Nan (Kaiyo) Ads Partnership for ClaudeFluent`

Keep titles specific and recognizable — the user should be able to find a past pre-mortem by skimming the Notion list. Don't date-stamp the title (the Notion `Created` field handles that).

## Legacy local archives

The pre-2026-04-26 pre-mortems live at `~/.claude/skills/pre-mortem/archives/`. New pre-mortems should NOT be saved there — Notion is the system of record going forward. If you need to migrate an old archive into Notion, read the file and run the same `notion-ai.js create` flow described in step 6.
