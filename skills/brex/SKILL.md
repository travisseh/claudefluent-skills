---
name: brex
description: "Access Denada Brex financial data through the Brex API. Use this skill whenever the user asks about Denada Brex, Brex transactions, Brex expenses, Brex balances, Brex accounts, Brex vendors, Brex payments, company card spend, cash movement, receipts, statements, spend limits, or money flowing through Denada."
---

# Brex - Denada

Use this skill to query Denada Brex data.

## Security

- The Brex API token is stored in macOS Keychain, not in this skill or any repo.
- Keychain service: `codex-brex-example-agency-api-key`
- Keychain account: `travisse`
- Never print the raw token.
- Default to read-only operations.
- For write or money-moving operations, explain the action and ask for explicit confirmation first. This includes creating payments, updating vendors, changing spend limits, locking cards, creating cards, uploading receipts, or modifying expenses.
- Do not save API responses containing sensitive financial data into repos unless the user explicitly asks and the file is added to `.gitignore`.

## Token Access

Use this shell snippet when making API calls:

```bash
BREX_TOKEN="$(security find-generic-password -a travisse -s codex-brex-example-agency-api-key -w)"
```

Then call Brex with:

```bash
curl -sS "https://api.brex.com/v1/expenses?limit=100" \
  -H "Authorization: Bearer ${BREX_TOKEN}" \
  -H "Accept: application/json"
```

## API Base

- Production base URL: `https://api.brex.com`
- Auth header: `Authorization: Bearer ${BREX_TOKEN}`
- Official docs:
  - Authentication: `https://developer.brex.com/docs/authentication/`
  - Transactions API: `https://developer.brex.com/openapi/transactions_api/`
  - Expenses API: `https://developer.brex.com/openapi/expenses_api/expenses/listexpenses`
  - Transactions examples: `https://developer.brex.com/docs/transactions_examples/`

## Common Read Queries

### List Expenses

```bash
BREX_TOKEN="$(security find-generic-password -a travisse -s codex-brex-example-agency-api-key -w)"
curl -sS "https://api.brex.com/v1/expenses?limit=100" \
  -H "Authorization: Bearer ${BREX_TOKEN}" \
  -H "Accept: application/json"
```

### Get One Expense

```bash
BREX_TOKEN="$(security find-generic-password -a travisse -s codex-brex-example-agency-api-key -w)"
curl -sS "https://api.brex.com/v1/expenses/{expense_id}" \
  -H "Authorization: Bearer ${BREX_TOKEN}" \
  -H "Accept: application/json"
```

### List Card Transactions

The Transactions API supports pagination with `cursor` and `limit`.

```bash
BREX_TOKEN="$(security find-generic-password -a travisse -s codex-brex-example-agency-api-key -w)"
curl -sS "https://api.brex.com/v2/transactions/card/primary?limit=100" \
  -H "Authorization: Bearer ${BREX_TOKEN}" \
  -H "Accept: application/json"
```

### Last 30 Days Vendor Spend

Use this when asked for recent vendors, company card spend, SaaS spend, or "what are we spending on?" Brex may reject date query params on this endpoint, so page recent card transactions and filter locally by `posted_at_date`. This intentionally excludes card payments/credits and counts only `PURCHASE` rows.

```bash
BREX_TOKEN="$(security find-generic-password -a travisse -s codex-brex-example-agency-api-key -w)"
CUTOFF="$(date -u -v-30d '+%Y-%m-%d')"
url="https://api.brex.com/v2/transactions/card/primary?limit=100"

while [ -n "$url" ]; do
  response="$(curl -sS "$url" \
    -H "Authorization: Bearer ${BREX_TOKEN}" \
    -H "Accept: application/json")"

  printf '%s\n' "$response" | jq -c '.items[]?'

  old_count="$(printf '%s\n' "$response" | jq --arg cutoff "$CUTOFF" '[.items[]? | select((.posted_at_date // .initiated_at_date // "9999-99-99") < $cutoff)] | length')"
  cursor="$(printf '%s\n' "$response" | jq -r '.next_cursor // empty')"

  if [ -n "$cursor" ] && [ "$old_count" = "0" ]; then
    url="https://api.brex.com/v2/transactions/card/primary?limit=100&cursor=${cursor}"
  else
    url=""
  fi
done | jq -s --arg cutoff "$CUTOFF" '
  def dollars: ((.amount.amount // .amount // 0) / 100);
  def raw_vendor: (.merchant.raw_descriptor // .description // "Unknown");
  def vendor_name:
    if (raw_vendor | test("^SQSP\\* WORKSP")) then "Squarespace"
    elif (raw_vendor | test("^OPENAI")) then "OpenAI"
    elif (raw_vendor | test("^GOOGLE\\*CLOUD")) then "Google Cloud"
    elif (raw_vendor | test("^LEMSQZY")) then "Lemon Squeezy"
    elif (raw_vendor | test("^HEROKU")) then "Heroku"
    elif raw_vendor == "Illustrator" then "Adobe Illustrator"
    else raw_vendor end;

  map(select((.posted_at_date // .initiated_at_date // "0000-00-00") >= $cutoff))
  | map(select((.type // "") == "PURCHASE"))
  | {
      total_transactions: length,
      total_spend: ((map(dollars) | add // 0) | .*100 | round / 100),
      start_date: $cutoff,
      end_date: (now | strftime("%Y-%m-%d")),
      vendors: (
        group_by(vendor_name)
        | map({
            vendor: (.[0] | vendor_name),
            transactions: length,
            total: ((map(dollars) | add) | .*100 | round / 100),
            latest: (map(.posted_at_date // .initiated_at_date) | max)
          })
        | sort_by(.total)
        | reverse
      )
    }
'
```

If the user asks for "last N days", replace `-v-30d` with the requested range, for example `-v-7d` or `-v-90d`.

### List Accounts

```bash
BREX_TOKEN="$(security find-generic-password -a travisse -s codex-brex-example-agency-api-key -w)"
curl -sS "https://api.brex.com/v2/accounts/cash" \
  -H "Authorization: Bearer ${BREX_TOKEN}" \
  -H "Accept: application/json"
```

## Pagination Pattern

Brex list endpoints commonly return a `next_cursor`. Keep fetching while it is present.

```bash
BREX_TOKEN="$(security find-generic-password -a travisse -s codex-brex-example-agency-api-key -w)"
url="https://api.brex.com/v1/expenses?limit=100"

while [ -n "$url" ]; do
  response="$(curl -sS "$url" \
    -H "Authorization: Bearer ${BREX_TOKEN}" \
    -H "Accept: application/json")"

  printf '%s\n' "$response" | jq '.items // .data // .'

  cursor="$(printf '%s\n' "$response" | jq -r '.next_cursor // empty')"
  if [ -n "$cursor" ]; then
    url="https://api.brex.com/v1/expenses?limit=100&cursor=${cursor}"
  else
    url=""
  fi
done
```

## Useful Analysis Workflow

1. Fetch only the date range and object type needed.
2. Summarize totals by merchant, category, cardholder, month, or account.
3. Redact or avoid displaying full IDs, account numbers, receipts, and employee-sensitive details unless needed.
4. When exporting, write to a local scratch path outside repos, such as `/tmp/brex-example-agency-report.json` or `/tmp/brex-example-agency-report.csv`.

## Verification

To verify the token exists without exposing it:

```bash
security find-generic-password -a travisse -s codex-brex-example-agency-api-key -w >/dev/null && echo "Brex token found"
```
