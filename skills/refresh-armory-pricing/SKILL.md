---
name: refresh-armory-pricing
description: Update the ExampleCo Armory's pricing data by fetching from Stripe. Use when Stripe products/prices have changed and the armory needs to reflect current pricing. Trigger with '/refresh-pricing'.
---

# Refresh Armory Pricing from Stripe

Use this skill to update the Armory's pricing data from Stripe.

## Invocation
`/refresh-pricing` or "refresh armory pricing from stripe"

## Prerequisites
- Stripe API key must be available (stored in environment or provided)
- Node.js must be installed

## Workflow

### Step 1: Run the fetch script
```bash
STRIPE_SECRET_KEY="sk_live_..." node ~/Programming/product2/public/apps/exampleco-armory/scripts/fetch-stripe-pricing.js
```

Or if the key is passed as argument:
```bash
node ~/Programming/product2/public/apps/exampleco-armory/scripts/fetch-stripe-pricing.js "sk_live_..."
```

### Step 2: Verify the update
Check the generated JSON file:
```bash
head -20 ~/Programming/product2/public/apps/exampleco-armory/data/stripe-pricing.json
```

### Step 3: Report results
Tell the user:
- When the data was last updated
- How many products were found in each category
- Any errors that occurred

## Security Note
The Stripe secret key should NOT be committed to git. The script reads from environment variable `STRIPE_SECRET_KEY` or accepts it as a command-line argument.

## Files
- **Script**: `~/Programming/product2/public/apps/exampleco-armory/scripts/fetch-stripe-pricing.js`
- **Output**: `~/Programming/product2/public/apps/exampleco-armory/data/stripe-pricing.json`

## Stripe Key Location
The ExampleCo Stripe live key can be found in 1Password or the ExampleCo admin dashboard.
