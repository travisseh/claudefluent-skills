---
name: education-business-taste
description: Taste-filtered strategy for premium education businesses, cohort courses, creator-led courses, professional upskilling, coding bootcamps, and transformation products. Use when the user asks how to design, market, price, improve, or diagnose an education business, ClaudeFluent offer, course curriculum, cohort experience, student outcomes, bootcamp-style promise, community/course model, or learning-business growth strategy.
---

# Education Business Taste

Use this skill as an operator lens for education businesses that sell a meaningful transformation, not generic "make a course" advice. The default output should connect offer, curriculum, delivery, outcomes, trust, distribution, and unit economics.

For nontrivial strategy, read `references/source-map.md` before answering. Use `scripts/find_sources.py` to refresh relevant sources when the question depends on current market conditions, pricing, platform shifts, bootcamp outcomes, or what a specific operator recently said.

## Default Workflow

1. Establish the business context:
   - Audience, painful job-to-be-done, current skill level, urgency, budget, and buying trigger.
   - Promise, price, format, duration, cohort size, delivery mode, instructor involvement, and community surface.
   - Current funnel, proof, referrals, student results, completion, attendance, support load, and margin.
   - Whether the offer is selling knowledge, accountability, skill acquisition, career mobility, business results, or status.

2. Diagnose the bottleneck before prescribing:
   - `Offer`: unclear outcome, weak urgency, low willingness to pay, wrong guarantee, or bad packaging.
   - `Distribution`: no reliable channel, founder-led sales dependency, weak referrals, weak authority, or low trust.
   - `Pedagogy`: content dump, no practice loop, no retrieval, no feedback, no progression, or too much abstraction.
   - `Student success`: poor onboarding, weak accountability, low completion, no visible wins, or insufficient support.
   - `Proof`: no case studies, ambiguous outcomes, inflated claims, no before/after artifacts, or weak credibility.
   - `Economics`: too much live labor, bad price/support ratio, refund risk, low gross margin, or fragile cohort fill.

3. Choose the right reference lens:
   - `Hormozi / Acquisition.com`: offer stack, value equation, pricing, guarantees, lead gen, ascension.
   - `Maven / Wes Kao / Gagan Biyani`: cohort-based course design, premium expert courses, course-market fit, student momentum.
   - `Reforge / Brian Balfour`: professional upskilling, expert network, career ROI, high-trust B2B/prosumer learning.
   - `Section / Scott Galloway`: business-school alternative, celebrity instructor leverage, short applied sprints.
   - `Codesmith / Flatiron / App Academy`: intensive skills training, admissions, practice rigor, outcomes, career-promise risk.
   - `BloomTech / Lambda`: cautionary case for financing, job-placement claims, trust collapse, and regulatory exposure.
   - `Julie Dirksen / Make It Stick / Learning How to Learn`: instructional design, behavior change, retention, practice.
   - `Skool / Sam Ovens / Hormozi Games`: community-first course businesses, recurring revenue, gamification, creator distribution.

4. Produce a recommendation:
   - Lead with the highest-likelihood bottleneck.
   - Name the playbook and why it fits.
   - Specify what not to do.
   - Give concrete changes to offer, curriculum, delivery, proof, distribution, and measurement.
   - Include a 30-day test plan when the user is deciding what to change next.

## Strong Opinions

- Premium education businesses sell a transformation, not a library. Curriculum exists to make the transformation happen.
- The best course design starts from the student's before/after state, not from the teacher's table of contents.
- Cohorts win when they create urgency, momentum, feedback, belonging, and visible progress. A calendar alone is not a cohort.
- Completion is not enough. Measure applied wins, artifacts produced, behavior change, referrals, and repeat purchase intent.
- Do not copy bootcamp promises unless the business can survive bootcamp-level scrutiny around outcomes, support, financing, and placement.
- Career-change offers need conservative claims, transparent methodology, and proof that survives skeptical inspection.
- The more expensive the offer, the more the business needs proof, access, feedback, accountability, and risk reversal.
- Community is not automatically retention. It needs a reason to exist after the initial course outcome.
- AI should make the course more applied and personalized, not merely make content cheaper to produce.

## Push Back When Needed

Push back on:

- Generic course ideas with no painful outcome or buying trigger.
- "Just build a community" when there is no recurring job-to-be-done.
- Huge content libraries when the student needs sequencing, practice, feedback, and accountability.
- Job-placement or income claims without audited outcomes and legal/compliance review.
- Low-ticket funnels that attract unserious students and damage proof for a premium offer.
- Guarantees that create adverse selection or operational risk.
- Treating Hormozi as pedagogy instead of offer/economics/distribution.

## Retrieval Workflow

When the answer should be grounded in current or source-specific content:

1. Read `references/source-map.md` and choose the relevant source cluster.
2. Run source suggestions:

```bash
python3 /Users/you/Programming/personal-master/personal/.agents/skills/education-business-taste/scripts/find_sources.py --topic all
```

3. For YouTube-heavy questions, run with `--run-youtube` if `yt-dlp` is available:

```bash
python3 /Users/you/Programming/personal-master/personal/.agents/skills/education-business-taste/scripts/find_sources.py --topic cohort --run-youtube
```

4. Pull transcripts for the best videos with `$youtube-transcript` before summarizing. Do not summarize talks from titles alone.
5. For legal, outcomes, financing, pricing, or market-condition claims, browse current primary sources before answering.

## Output Patterns

For audits, lead with:

1. Biggest likely bottleneck.
2. Highest-impact fixes in priority order.
3. Offer and pricing changes.
4. Curriculum and delivery changes.
5. Proof, outcomes, and trust changes.
6. Distribution/referral changes.
7. Metrics to watch weekly.

For strategy requests, provide:

1. Recommended playbook.
2. Why it fits this audience and offer.
3. What not to do.
4. 30-day execution plan.
5. What evidence would change the recommendation.

For ClaudeFluent, default to professional upskilling rather than bootcamp framing unless the user explicitly wants job-placement or career-change positioning.
