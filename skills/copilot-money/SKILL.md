---
name: copilot-money
description: Log into Copilot Money, export transactions, review spending data, find uncategorized transactions, and categorize or ask the user for clarification using Gmail magic-link login and CSV transaction exports.
---

# Copilot Money

Use this when the user asks to inspect Copilot Money, pull transactions, review categories, find uncategorized items, analyze spending, or categorize new transactions.

## Login

Copilot web app:

```text
https://app.copilot.money/
```

Typical flow:

1. Open Copilot in browser automation.
2. Click `Continue with email`.
3. Use `userh@gmail.com`.
4. Read the magic-link email with the local Gmail CLI.
5. Navigate to the `https://auth.copilot.money/__/auth/action?...` link.

Useful Gmail commands:

```bash
node ~/.config/gmail-tools/gmail.js search personal "from:noreply-copilotmoney@copilot.money newer_than:10m" 5
node ~/.config/gmail-tools/gmail.js read personal "from:noreply-copilotmoney@copilot.money subject:\"Sign in to Copilot Money\""
```

If the CLI read output hides the link, fetch the raw Gmail message with `googleapis` and decode MIME parts.

## Export Transactions

After login:

1. Go to `https://app.copilot.money/transactions`.
2. Click `Download transactions`.
3. The CSV lands in `~/Downloads/transactions*.csv`.
4. Use the newest matching file unless the user points to another export.

CSV fields observed:

```text
date,name,amount,status,category,parent category,excluded,tags,type,account,account mask,note,recurring
```

Amounts are signed from Copilot's perspective. Inspect `type`, `category`, `account`, and `name` before interpreting income vs expense.

## Pulling Data

For a date range:

```python
import csv
rows = []
with open("~/Downloads/transactions (2).csv", newline="", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        if "2024-01-01" <= row["date"] <= "2024-12-31" and row["excluded"] == "false":
            row["amt"] = float(row["amount"])
            rows.append(row)
```

Common filters:

- Uncategorized: `category == ""` or category looks like `Other` and the merchant/note is specific enough to classify.
- Needs review: tags or notes containing `review`, `steph review`, or category mismatch.
- Internal transfers: `type == "internal transfer"`; do not categorize as spending without intent.
- Pending: decide whether to include based on the user request.

## Categorization Rules

Default behavior:

- Make obvious category suggestions from merchant/name/note/category history.
- Do not silently mutate Copilot categories unless the user explicitly asks to apply changes.
- If ambiguous, ask for clarification with a short list of transactions and candidate categories.
- For recurring obvious merchants, state the pattern and ask once before bulk-applying.

High-confidence examples from prior usage:

- Wasatch Broadband -> Lehi internet / rental internet when reviewing 2024 rentals.
- Roundpoint Mtg -> Lehi mortgage if tied to the Lehi rental account.
- Provo City / Dominion account ending `2402` / UWM / Pioneer HOA -> Provo rental.
- Lehi City / Dominion account ending `9901` / The Exchange HOA / Wasatch Broadband -> Lehi rental.
- Red Rock Property, Dixie Power, City Of St George, Centurylink, Quantum Fiber -> St. George; ignore when the user asks only about Provo/Lehi.

Do not over-classify:

- `Target`, `Amazon`, `U-Haul`, `Geometry`, `Zurchers`, and Venmo/person payments often need notes/context.
- `Other` is not always wrong; small one-off personal transactions may remain `Other`.
- Bank transfers and credit-card payments are usually not expenses.

## Daily Review Output

For a recurring review, produce:

1. Count of new/posted transactions reviewed.
2. Transactions confidently categorizable, grouped by proposed category.
3. Ambiguous transactions needing the user.
4. Any suspicious duplicates, reversals, or large uncategorized items.

Keep it short. Ask clarification only for transactions where the answer changes downstream reporting.
