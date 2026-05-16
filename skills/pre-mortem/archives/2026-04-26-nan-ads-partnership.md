# Pre-Mortem: Nan (Kaiyo Ventures) advertising partnership for ClaudeFluent
**Date:** 2026-04-26 | **Event date:** kickoff TBD (assumed ~mid-May 2026) | **Stakes:** $5-30k of ad spend, 5-10 hrs/wk of the user's attention, brand integrity, partnership precedent (sets the template for any future Cam deal)

## Context and assumptions

Working from memory dated 2026-03-15. Verify before final commit:
- Structure: Nan starts on revenue share (20-25% of ad-driven revenue), no equity yet
- Path to equity: 3 months of proven performance, then re-evaluate
- the user stays at ExampleCo until $25k/mo for 2 consecutive months with 30%+ from non-network channels
- Nan's role: paid ads operations (Meta, Google, LinkedIn likely)

If any of those have changed (e.g., already gave Nan equity, already authorized big spend, already running campaigns), the analysis below needs adjustment.

## The ways this fails

### 1. Unit economics don't work — paid CAC > what the $999 product can sustain
- **Likelihood:** High
- **Impact:** High — quietly bleeds money for 3-6 months while you tell yourself it's "early"
- **Why it's the #1 risk:** Your 4.5% conversion rate was built on warm referrals and LinkedIn intent traffic. Cold paid traffic typically converts at 0.5-2% on landing pages designed for warm. At a $999 one-time product with limited repeat purchase, your CAC ceiling is roughly $200-350. Meta/Google CACs for premium B2C info products in adjacent niches (cohort-based courses, $500-1500 price points) usually land at $400-900 in the first 90 days before optimization. You are very likely going to spend $5-15k before learning whether ads can be profitable, and there's a real chance the answer is "no, not at this price."
- **Early warning signs:** First 2 weeks of campaigns show CAC > $500. Funnel-stage drop-off concentrated at landing page (visitor-to-signup), not at checkout.
- **Leading indicator:** Has Nan run paid ads for a similar high-ticket B2C info product (cohort course / training, $500-2000 price point) and hit a CAC < $400? If he has examples, ask for the screenshots. If he doesn't, you're his learning case.
- **Mitigation (do this now):** Set a hard CAC ceiling in writing ($300 is my recommendation). If 60-day rolling CAC exceeds it, spend pauses automatically. Cap monthly spend at a number you can lose 100% of without flinching ($3-5k for first 60 days). No "scale it up" conversations until CAC is proven for 30 consecutive days.

### 2. Misaligned incentives — Nan paid on revenue, not profit
- **Likelihood:** High (this is structural, not behavioral)
- **Impact:** High
- **Why it bites:** Nan gets 20-25% of "ad-driven revenue." He's incentivized to maximize attributed revenue, not your margin. If ads break even at $999 CAC = $999 revenue, he gets $200-250 and you got nothing for your time, money, and customer service load. He has a short-term incentive to keep spending past the point you should stop.
- **Early warning signs:** Nan's reports lead with "revenue generated" and bury "spend" or "ROAS." He pushes to scale before unit economics are proven. He resists or delays installing a hard CAC ceiling.
- **Leading indicator:** What does the first reporting template he sends you look like? Profit-first or revenue-first?
- **Mitigation (do this now):** Restructure the deal. Two cleaner options:
  - Option A: Nan paid only on **profitable** customer acquisition. Define profit = revenue minus ad spend minus payment processing. He gets 25% of profit, not revenue.
  - Option B: Nan paid a flat retainer + bonus on hitting a CAC target. Removes the spend-more incentive entirely.
  - If he refuses both, that tells you he expects ads to be marginal and wants to be paid regardless. That's the answer.

### 3. Time tax on you that you don't see coming
- **Likelihood:** Very High
- **Impact:** High — directly competes with your stated focus list (Steph/Carson, bishopric, ExampleCo)
- **Why it bites:** "Nan handles ads" sounds hands-off. In practice you'll spend 5-10 hrs/wk on: creative reviews (your face, your voice, your positioning), landing page changes, attribution debugging, weekly check-ins, deciding what to do when a campaign tanks, brand-voice calls, fielding new audience segments that need new copy. Your attention is the bottleneck on the rest of your life right now, not your money.
- **Early warning signs:** First week kicks off with 3+ Slack pings/day. He requests a recurring weekly meeting. He asks you to record new video creative.
- **Leading indicator:** Within the first 14 days, total hours you spend on ads work. If it's > 10 in two weeks, this is going to eat your focus.
- **Mitigation (do this now):** Pre-commit a weekly time budget — "I will spend max 2 hrs/week on this." Put it in the deal terms. Async-default communication: Loom updates, not meetings. One weekly digest, not daily Slack. If Nan needs more of your time than that to make ads work, the partnership has the wrong shape.

### 4. Brand voice / positioning erosion
- **Likelihood:** Medium-High
- **Impact:** Medium — recoverable but expensive in trust
- **Why it bites:** Your positioning is sharp ("knowledge workers, not engineers") and your voice rules are strict (no hashtags, no em-dashes, specific cadence). Performance ad copy is its own dialect — short, punchy, often clickbait-adjacent. The version that converts cold traffic may not be the version your warm audience respects. If a current customer sees a "5 SECRETS to 10x YOUR CODING with AI" ad with your face on it, the $999 trust premium starts leaking.
- **Early warning signs:** First creative drafts use language you wouldn't write. Hooks that feel "guru-y." Pressure to "test it and see" instead of writing on-brand from the start.
- **Leading indicator:** Send Nan your user-writing-style guide and the ClaudeFluent content charter BEFORE he writes a line of copy. Watch what comes back.
- **Mitigation (do this now):** Brand-voice approval is non-negotiable: every piece of creative ships with your sign-off, no exceptions. Make this the easiest possible workflow (Loom approval, not meeting) but never delegate brand voice. Add to the deal: "All creative requires the user approval before launch."

### 5. Attribution disputes that poison the relationship
- **Likelihood:** Medium-High
- **Impact:** Medium — friction over months, not a single blowup
- **Why it bites:** "Ad-driven revenue" is rarely clean. Someone sees an ad, then comes through a referral 2 weeks later — does Nan get paid? Multi-touch journeys, retargeting, branded search ("ClaudeFluent" Google searches that may have been demand you generated) all create gray zones. As your organic and referral channels grow in parallel, attribution arguments will eat real time.
- **Leading indicator:** Whether you write the attribution definition BEFORE the first dollar is spent.
- **Mitigation (do this now):** Single-attribution model in writing before launch. Recommend: "Last non-organic click within 30 days, branded search excluded." If Nan wants a softer model, that tells you he expects to need it, which tells you the campaigns may not have clean attribution.

### 6. Nan's accountability is fuzzy because Kaiyo Ventures is a portfolio
- **Likelihood:** Medium
- **Impact:** Medium-High at the 60-90 day mark when something needs to be fixed urgently
- **Why it bites:** Nan runs multiple bets. ClaudeFluent is one of them. When a campaign tanks on a Tuesday, what's his SLA? When you need new creative for a launch, where are you in his queue? Without explicit terms, you're a low-priority side project for him while he's a high-priority dependency for you.
- **Mitigation (do this now):** Define minimum effort floor in writing (e.g., "20 hrs/month minimum, weekly campaign reviews, 24-hr response on flagged issues"). Add a 60-day no-fault exit clause for both sides.

### 7. Path dependence — you can't easily fire him
- **Likelihood:** Medium | **Impact:** High at the breakup point
- **Why it bites:** Once Nan owns the ad accounts, knows the audiences that work, has the creative library, and has built the attribution flow, replacing him is months of work. If the partnership goes sour in month 4 and you're already at $30k MRR with 30% from ads, you're stuck.
- **Mitigation (do this now):** Ad accounts in YOUR name from day 1 (the user / ClaudeFluent LLC), Nan as user with admin access. All creative assets stored in YOUR Google Drive. Documented playbook of audiences, hooks, and what works — updated monthly. Treat him like a contractor whose work product you own, even though he's a partner.

## Worst case: the story of how this goes wrong

Mid-May 2026. Nan launches three Meta campaigns aimed at "developers and tech-curious knowledge workers." Spend ramps to $4k in week one. Click-through is decent but landing page conversion is 1.1%, vs the 4.5% you're used to. CAC comes in at $620. Nan reports "we're seeing strong intent signals" and asks to scale spend to $8k/month so the algo has room to optimize. You agree because the alternative is admitting two months of work was wasted. By July you've spent $18k and acquired 22 students at a blended CAC of $810. Your P&L is bleeding. You have a hard conversation with Nan that drags across two weeks of Slack threads. The partnership ends in August. You spent the May-August window on creative reviews, attribution arguments, and landing page rebuilds instead of finishing the post-class testimonial pipeline, recording a self-paced course, or doing the team training follow-up from Solv. Your focus list got starved. Steph noticed.

## Questions before I forecast the win

I need answers to these before I can project specifically. Best guesses inline if you don't know.

1. **What's Nan's track record on similar products?** Has he hit < $400 CAC on a $500-2000 cohort/training product before? Show-me-the-screenshots level of evidence, not vibes.
2. **What budget are you authorizing for the first 60 days?** (Recommendation: $3-5k cap, period.)
3. **Is the structure still 20-25% of ad-driven revenue?** Or has it moved? (Recommended pivot: 25% of *profit*, or flat retainer + CAC bonus.)
4. **Who controls the ad accounts and creative library?** (Must be you.)
5. **Has he sent you a sample reporting template yet?** (If yes, what does it lead with?)
6. **What's a realistic CAC ceiling for ClaudeFluent at $999 with current repeat / upsell?** (My estimate: $300. If you have follow-up courses or recurring offer in flight, could stretch to $400-500.)

## If this works: the next year

These projections assume: $300 CAC achieved by month 2, $5k/mo spend ramping to $15k/mo by month 6, you maintain brand voice approval, attribution model is clean.

### 1 month from now (late May 2026)
- **What's true:** ~$3-5k spent. 8-15 ad-attributed signups. CAC sitting at $400-600 (still in learning phase). Three creative variants tested, one front-runner. Landing page has been rebuilt once. Two attribution gray zones already debated.
- **Where your time goes:** 4-6 hrs/wk on ads — creative review, weekly check-in, landing page edits. LinkedIn cadence slipped to 3-4x/week (was 5).
- **What's getting hard:** Deciding whether early CAC is "learning curve" or "structural ceiling." Nan wants to scale. You're not sure yet.

### 3 months from now (late July 2026)
- **What's true:** $20-30k cumulative spend. CAC stabilized at $300-400. Paid is driving 25-35% of monthly signups. ClaudeFluent at $30-40k MRR. You've shipped one new creative angle that's working ("Claude Code for product managers" or similar). Affiliate concentration risk down from 31% to ~15%.
- **Where your time goes:** 3-4 hrs/wk on ads (less than at start, more systematized). LinkedIn cadence recovered. Live workshop delivery is 2-3x/week. Less time on ExampleCo product strategy than you'd like.
- **What's getting hard:** Live delivery capacity. You're running every workshop. Booking calendar is jammed. Quit-ExampleCo conversation is plausible by Q4 and you don't have a transition plan.

### 6 months from now (late October 2026)
- **What's true:** Paid is $15-25k/mo spend, $50-80k/mo attributed revenue. ClaudeFluent at $50-70k MRR total. You've crossed the quit-trigger threshold (>$25k/mo with >30% non-network) for one or two months. Nan has earned formal equity discussion. A self-paced product or follow-up course exists (because you needed something to reduce live delivery load). You've hired or contracted at least one person — likely a community manager or part-time TA.
- **Where your time goes:** 30% live delivery, 25% sales/closing (team trainings + cohorts), 15% product/curriculum, 15% content, 15% partner/admin (Nan, Cam if active, contractors). ExampleCo is a real squeeze.
- **What's getting hard:** Your bandwidth as the only senior face of the brand. Customer success / post-sale handoff is all you. Cam (if engaged) wants formal status. Steph wants an answer on ExampleCo.

### 1 year from now (April 2027)
- **What's true:** Paid is $30-50k/mo spend, $100-150k/mo attributed revenue. ClaudeFluent at $120-180k MRR. Paid + referrals + LinkedIn each contributing meaningfully (no single channel > 50%). You have made the ExampleCo decision (likely left or downshifted to advisor). Nan has formal equity (recommend you held to 50/25/25 if he and Cam both stayed). Team of 2-3 contractors plus you. Self-paced course launched, generating 15-20% of revenue.
- **Where your time goes:** Strategy, brand voice, flagship workshops, hiring decisions, Cam-style enterprise closing. Less hands-on creative.
- **What's getting hard:** Operational debt (billing, scheduling, onboarding all you-shaped). Curriculum staleness — Claude Code releases faster than you can update slides. Personal taxes / entity structure as ClaudeFluent crosses $1.5M ARR.

## Best case: the story of how this works

By August 2026, Nan has dialed in a "Claude Code for non-engineers" creative that's pulling $250 CAC on Meta. You hit $35k MRR for two months running with 35% from ads. You and Steph have the ExampleCo conversation. By October you've shipped a self-paced course because live delivery capacity capped you at $50k MRR and you needed a way to keep growing without burning out. By February 2027 ClaudeFluent is at $120k MRR, you've left ExampleCo (or gone advisor), and you have two contractors plus a community manager. The flood debt is paid off in March. The inflection point you'll point to a year from now: the day Nan agreed to a CAC-ceilinged budget and a profit-based commission structure, which forced him to actually optimize rather than spend.

## Next bottlenecks (10x test)

**The key input here is: paid-acquired customers per month.**
**If that 10x'd tomorrow (e.g., from 10 ad signups/mo to 100/mo), here's what breaks first:**

### Bottleneck 1: Live workshop delivery capacity (you)
- **Why it breaks:** You personally lead every cohort. At ~10 signups/mo you can run a workshop a week. At 100 signups/mo you'd need 4-5 cohorts/week and you cannot physically do that. Quality drops, you burn out, refund rate spikes.
- **Systematize now:** Record the core curriculum as on-demand video THIS QUARTER. Test a model where live becomes "workshop + Q&A on top of pre-watched videos" — cuts your live time per cohort by 50%+. Identify a co-instructor profile (Claude-Code-fluent, comfortable on camera, 10 hrs/wk capacity). Don't wait until you're drowning to start the search.

### Bottleneck 2: Post-class follow-up + testimonial harvest
- **Why it breaks:** This was the leverage build we already identified. Currently manual. At 10 students/mo you can hand-write thank-yous and chase quotes. At 100 students/mo you can't, and you lose the testimonial flywheel that's driving 50% testimonial rate today.
- **Systematize now:** Build the post-class thank-you + testimonial automation we already discussed. Make it the next leverage project (the one you'd build in your one-per-week exploration block). Ship it before paid ads scale, not after.

### Bottleneck 3: Customer support / community
- **Why it breaks:** Students currently DM you, email you, ask questions in office hours. At 10x volume, your inbox is the bottleneck. Response times slip from hours to days. Refund risk grows.
- **Systematize now:** Spin up a Discord or Circle community now (low maintenance at current volume, lifesaver at 10x). Recruit 1-2 alumni as volunteer mods in exchange for free follow-up courses. Build an FAQ doc from your most common 20 questions. By month 6 budget for a part-time community manager (10 hrs/wk).

### Bottleneck 4: Brand voice / creative throughput
- **Why it breaks:** Every ad needs your sign-off. At 3 creatives/week you can review. At 30 creatives/week the bottleneck IS your review queue. Either you stop approving (brand drifts) or you become a full-time creative reviewer.
- **Systematize now:** Codify your brand voice into a creative checklist Nan (and any future creative person) can self-screen against. Pre-approve a library of hooks, language, and visual templates. Move from "approve every ad" to "approve every new pattern."

## Contingency checklist

**Next 24 hours:**
- [ ] Verify the partnership status — is the structure still rev-share-on-revenue, or has it changed since March 15? (Ask Nan in Kaiyo Slack #project-claude-fluent if unclear.)
- [ ] Decide your maximum 60-day spend authorization — pick a number you can lose 100% of and write it down

**Next 48-72 hours:**
- [ ] Send Nan the structural pivot ask: 25% of *profit* OR retainer + CAC bonus, not 25% of revenue
- [ ] Send Nan your user-writing-style guide and ClaudeFluent content charter — see what comes back
- [ ] Ask Nan for screenshots / proof of similar ($500-2000 cohort/training) results he's hit
- [ ] Set a single attribution model in writing — last non-organic click, 30 days, branded search excluded

**Before kickoff (whenever launch is):**
- [ ] Hard CAC ceiling in deal terms, with auto-pause trigger
- [ ] Monthly spend cap in deal terms
- [ ] Ad accounts in your name, you as owner, Nan as admin
- [ ] Weekly time-cap commitment (yours, not his) — no more than 2 hrs/wk on this
- [ ] 60-day no-fault exit clause for both sides
- [ ] Reporting template that leads with profit / CAC, not gross revenue
- [ ] Ship the post-class thank-you + testimonial automation BEFORE ads scale

## Gut check: would you still do this?

**Yes, but only if you renegotiate the structure first AND ship the post-class automation before scaling spend.**

The original idea is sound — diversify off the 31% affiliate concentration, prove paid as a channel, get to the quit-ExampleCo trigger faster. But the deal as memo'd (Nan gets 20-25% of *revenue*) has the wrong incentives baked in. He'll be paid for spending whether ads are profitable or not, and your downside (money + attention + brand) is asymmetric to his upside.

Three non-negotiables before kickoff:
1. **Profit-based or CAC-bonused commission**, not revenue-based. If he refuses, that's information.
2. **Hard CAC ceiling and monthly spend cap**, in writing, with auto-pause if exceeded.
3. **Your weekly time on this capped at 2 hrs**, declared upfront. If the work needs more, the deal doesn't fit your focus list.

If you can get those three, proceed at $3-5k/mo for 60 days, then re-evaluate with hard data. If you can't get those three, walk — and push the diversification problem with cheaper, less-attention-eating channels first (more affiliates, more LinkedIn, the team training motion from the Solv pre-mortem).

The bigger risk than Nan failing is Nan partially succeeding — generating just enough signal to keep you spending money and attention on something that never quite breaks profitable, while your real focus list (Steph, Carson, bishopric, ExampleCo) and your highest-leverage CF work (post-class automation, self-paced course) get starved.
