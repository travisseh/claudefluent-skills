---
name: personal-finance-review
description: "Review personal or household spending from Chase credit-card exports and logged-in retailer history. Use when the user asks about budget, finances, personal spend, credit-card categories, DoorDash, Walmart, Instacart, where the money is going, or wants a spouse-shareable spending report with examples and cost-cutting recommendations."
---

# Personal Finance Review

Use this skill for repeat household-spend reviews from the user's live Chase session and exported Chase CSVs.

Default convention for this user:

- treat `Walmart` as groceries/household unless order-history evidence shows otherwise
- treat `Instacart` as groceries
- explicitly call out whether `Food & drink` includes `DoorDash`

## Workflow

1. Use `Computer Use` if the user wants fresh data from logged-in accounts.
2. On Chase, prefer the card-specific view plus Spending Planner for quick totals, then export account activity CSV for exact analysis.
3. Run the bundled parser:

```bash
python3 ~/.codex/skills/personal-finance-review/scripts/analyze_chase_csv.py
```

You can also pass a specific file:

```bash
python3 ~/.codex/skills/personal-finance-review/scripts/analyze_chase_csv.py ~/Downloads/Chase....CSV
```

4. If the user asks whether `Walmart` is really groceries vs discretionary shopping, inspect `https://www.walmart.com/orders` in the logged-in browser session and sample recent and larger orders.
5. Synthesize the results into plain-English conclusions and likely cut levers.

## Chase Flow

- Navigate to the requested Chase card or account summary.
- Use Spending Planner when you need quick category and merchant summaries.
- Use account activity CSV when you need exact totals, category examples, or merchant rollups.
- Ignore `Payment` rows. For Chase exports, net spend is typically `-Amount` for `Sale` and negative spend for `Return`.

## Walmart / Instacart Rules

- Reclassify all descriptions containing `walmart` or `instacar` to `Groceries` by default.
- Also treat `Walmart+ Member` as groceries/household overhead unless the user wants a stricter view.
- Chase often labels Walmart as `Shopping`; do not accept that at face value.
- For Walmart order-history review, classify orders into:
  - `essential`: groceries, formula, baby items, medicine, household basics
  - `mixed`: mostly essentials with some discretionary add-ons
  - `discretionary`: apparel, party supplies, convenience drinks/snacks, hobby or impulse items

## Output Requirements

When preparing a shareable report, include:

- period reviewed
- total spend reviewed
- top categories after the Walmart/Instacart grocery reclassification
- examples of what is inside each major category
- DoorDash total and its share of `Food & drink`
- a direct answer on whether Walmart looks mostly essential or mostly discretionary
- the clearest areas to cut, stated plainly

Keep the tone factual and spouse-shareable. Avoid sounding accusatory. The useful distinction is:

- what looks necessary
- what looks optional
- what is large enough to matter

## Script Output

The bundled script prints:

- total spend
- category totals and shares
- top merchants per category
- example transactions per category
- explicit notes for DoorDash and Walmart/Instacart grocery reclassification

Use the script output as the baseline, then layer in browser findings for SKU-level questions such as Walmart order makeup.
