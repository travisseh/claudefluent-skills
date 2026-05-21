---
name: copilot-money
description: Log into Copilot Money, export transactions, review spending data, find uncategorized transactions, and suggest category cleanup using email magic-link login and CSV transaction exports.
---

# Copilot Money

Use this when a user asks to inspect Copilot Money, pull transactions, review categories, find uncategorized items, analyze spending, or categorize new transactions.

## Login

Copilot web app:

```text
https://app.copilot.money/
```

Typical flow:

1. Open Copilot in browser automation.
2. Click `Continue with email`.
3. Use the user's Copilot login email.
4. Read the magic-link email with the user's approved email tool.
5. Navigate to the `https://auth.copilot.money/__/auth/action?...` link.

Useful Gmail commands:

```bash
node path/to/gmail-cli.js search personal "from:noreply-copilotmoney@copilot.money newer_than:10m" 5
node path/to/gmail-cli.js read personal "from:noreply-copilotmoney@copilot.money subject:\"Sign in to Copilot Money\""
```

If the CLI read output hides the link, fetch the raw Gmail message with `googleapis` and decode MIME parts.

## Export Transactions

After login:

1. Go to `https://app.copilot.money/transactions`.
2. Click `Download transactions`.
3. The CSV lands in `/Users/you/Downloads/transactions*.csv`.
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
with open("/Users/you/Downloads/transactions (2).csv", newline="", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        if "2024-01-01" <= row["date"] <= "2024-12-31" and row["excluded"] == "false":
            row["amt"] = float(row["amount"])
            rows.append(row)
```

Common filters:

- Uncategorized: `category == ""` or category looks like `Other` and the merchant/note is specific enough to classify.
- Needs review: tags or notes containing `review`, user-specific review markers, or category mismatch.
- Internal transfers: `type == "internal transfer"`; do not categorize as spending without intent.
- Pending: decide whether to include based on the user request.

## Spend Breakdown

When reviewing a time period or a recurring daily export, include a spend breakdown for the same analyzed period in addition to category cleanup.

Use the reviewed transaction set, not the whole export, unless the user asks for a broader period. If comparing against a prior export, this is the new/since-prior transaction set plus relevant pending-to-posted transitions you explicitly reviewed. If prior-run state is unavailable, use the last-24-hours fallback set.

Breakdown rules:

- Include regular expense transactions where `excluded == "false"` and `amount` is positive.
- Exclude `type == "internal transfer"`, credit card payments, reimbursements, income, refunds/negative amounts, and ambiguous Venmo/person payments unless they are already categorized as spending.
- Separate pending and posted if both appear and that distinction matters; otherwise state the combined reviewed-period total.
- Group by `category` first, then call out the largest merchants or unusual charges if useful.
- Mention skipped non-spend separately so the total is easy to trust.

## Categorization Rules

Default behavior:

- Make obvious category suggestions from merchant/name/note/category history.
- Do not silently mutate Copilot categories unless the user explicitly asks to apply changes.
- If ambiguous, ask for clarification with a short list of transactions and candidate categories.
- For recurring obvious merchants, state the pattern and ask once before bulk-applying.

High-confidence example patterns:

- Local utility, mortgage, HOA, and internet merchants often map to a specific property or household bucket.
- Preserve account masks and notes only long enough to distinguish between similar recurring bills.
- If a merchant can belong to multiple homes, rentals, businesses, or family members, ask before applying a category.

Do not over-classify:

- `Target`, `Amazon`, `U-Haul`, `Geometry`, `Zurchers`, and Venmo/person payments often need notes/context.
- `Other` is not always wrong; small one-off personal transactions may remain `Other`.
- Bank transfers and credit-card payments are usually not expenses.

## Daily Review Output

For a recurring review, produce:

1. Count of new/posted transactions reviewed.
2. Total reviewed-period spend and category breakdown, using the spend breakdown rules above.
3. Transactions confidently categorizable, grouped by proposed category.
4. Ambiguous transactions needing the user.
5. Any suspicious duplicates, reversals, or large uncategorized items.

Keep it short. Ask clarification only for transactions where the answer changes downstream reporting.
