---
name: focus
description: "Ruthlessly narrow the user's commitments to what can actually fit in a day, week, month, quarter, or year. Use when he asks to focus, trim scope, choose what not to do, plan a realistic period, reduce overwhelm, or convert a large plate into a small executable stack. Pull importance ranking and priority tiers from the daily-prioritizer skill."
---

# Focus

Help the user cut his active commitments down to a realistic focus stack for a specific time horizon. This is a capacity and tradeoff skill, not a motivation skill.

Use `daily-prioritizer` for the definition of "important": priority tiers, urgency overrides, tiebreaker rule, and the 6-dimension scoring rubric. Do not recreate full source-gathering unless the user asks for a full scan; this skill usually works from what he says is on his plate plus any obvious calendar/backlog context.

## Core Principle

The output is not a ranked wish list. It is a constrained commitment list:

- **Day:** 1 main outcome, 1-2 secondary tasks, minimum health/family/service constraints.
- **Week:** 1-2 primary outcomes, 2-4 support commitments, explicit drop list.
- **Month:** 1 primary theme, 2-3 measurable outcomes, 3-5 maintenance lanes.
- **Quarter/Year:** 1 strategic bet, 2-4 supporting bets, clear kill criteria.

If the list still feels expensive, it is not focused enough.

## Workflow

### 1. Establish the Container

Ask only what changes the decision:

- "What time horizon are we focusing: today, this week, this month, quarter, or year?"
- "How much real discretionary capacity do you have in that period?"
- "What fixed obligations are already non-negotiable?"

If the user gave enough context, infer the horizon and capacity. State assumptions.

### 2. Inventory the Plate

Get everything competing for attention into one list. Include:

- hard commitments
- mentally salient projects
- people waiting on him
- financial/income risks or opportunities
- family, bishopric, health, and maintenance obligations
- tasks he feels guilty about but may not actually need to do

For each item, capture:

- **Outcome:** what "done enough" means
- **Horizon fit:** day, week, month, quarter, year, someday
- **Estimate:** real time/energy cost
- **Deadline:** hard, soft, or none
- **Consequence of not doing:** specific, not vague
- **Owner:** the user, someone else, or unclear

### 3. Pull Importance From Daily Prioritizer

Apply the `daily-prioritizer` tiers and urgency overrides:

1. Family Safety & Wellbeing
2. Income Protection & Growth
3. Financial & Strategic Thinking
4. Family Thriving
5. Bishopric & Service
6. ReviewCo & Work Excellence
7. Personal Health

Use its tiebreaker: "Which one has consequences I can't undo if I skip it today?"

Promote any item with an urgency override:

- threatens job security or loses money
- time-sensitive upside
- a person is in genuine need
- imminent deadline with real consequences

For a small list, score compactly with the daily-prioritizer dimensions: irreversibility, tier alignment, people impact, compounding value, effort-to-impact, and decay risk.

### 4. Capacity Cut

Force the list through a capacity gate.

Use these rough caps unless the user gives a better one:

- **Day:** 60-70% of open hours can be planned; leave buffer.
- **Week:** 3-4 serious outcomes max outside fixed obligations.
- **Month:** 2-3 major pushes max, plus maintenance.
- **Quarter/Year:** no more than 3 active strategic bets.

Classify every item:

- **Commit:** fits capacity and matters enough.
- **Schedule:** important, but not in the current container.
- **Delegate/Ask:** someone else should own or unblock it.
- **Shrink:** only a smaller version belongs in this horizon.
- **Kill:** not worth carrying.

If committed work exceeds capacity, do not soften it. Say exactly what must move.

### 5. Progressive Grilling

Use increasingly pointed questions until the focus stack is small enough:

- "What breaks if this waits?"
- "Who is actually harmed if this is not done?"
- "Is this income-protecting, relationship-protecting, or mostly anxiety relief?"
- "What is the 30-minute version?"
- "What would make this obviously not worth doing?"
- "Is this a commitment or just an open loop?"
- "What are you pretending is optional but is actually fixed?"
- "What are you pretending is fixed but is actually optional?"
- "If you could only finish one thing in this horizon, which consequence would you most want to avoid?"

Stop grilling when the stack fits the container.

## Output Format

Use this shape:

```markdown
# Focus Stack — [Horizon]

## Capacity Assumption
[Realistic available time/energy and fixed constraints.]

## Commit
1. [Outcome] — [why it survives; estimated effort]
2. [Outcome] — [why it survives; estimated effort]

## Schedule
- [Item] — [when/why]

## Shrink
- [Original item] -> [smaller version that fits]

## Delegate/Ask
- [Item] — [who/what ask]

## Kill
- [Item] — [blunt reason]

## Tradeoff
[One paragraph naming what this focus stack sacrifices.]

## Next Action
[The first concrete action, ideally <=30 minutes.]
```

For high-friction decisions, add a compact scoring table before the final stack. Avoid long tables unless scoring is the point of the request.

## Tone

Direct and unsentimental. Name overcommitment plainly. Respect that the user may override the recommendation, but do not hide the tradeoff. The skill should feel like an executive operator forcing a real plan, not a productivity coach giving encouragement.
