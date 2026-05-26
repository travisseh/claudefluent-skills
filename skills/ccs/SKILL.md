---
name: ccs
description: Retrieve the user's saved ccs details from macOS Keychain for checkout, billing, subscription setup, or payment form tasks. Use when the user references ccs, a saved checkout profile, or a saved payment method.
---

# CCS

Use this skill when the user references `ccs` or asks to use a saved checkout/payment profile.

## Storage

Details are stored in macOS Keychain as generic passwords. The skill file must never contain card numbers, CVVs, or billing secrets.

Known Keychain items:

- ClaudeFluent: service `ccs-cf`, account `cf`
- Personal: service `ccs-personal`, account `personal` (may not exist yet)

Stored JSON fields may include:

- `label`
- `number`
- `exp_month`
- `exp_year`
- `last4`
- `cardholder_name`
- `billing_zip`
- `billing_address`

CVV/CVC must not be stored. If a checkout requires CVV/CVC, ask the user for it live and use it only for that transaction.

## Retrieval

Retrieve a card with:

```sh
security find-generic-password -s ccs-cf -a cf -w
```

For personal:

```sh
security find-generic-password -s ccs-personal -a personal -w
```

Do not print full card numbers back to the user. If confirming access, show only label, expiration, last four, and whether the number exists.

## Checkout Workflow

1. Select the card based on the user request. Default to ClaudeFluent only when the task is clearly ClaudeFluent/business related.
2. Retrieve the Keychain item at the moment it is needed.
3. Fill the payment form using the stored fields.
4. If the form asks for CVV/CVC, ask the user for it live.
5. After submitting or saving payment details, report the outcome without exposing the full card number.

## Adding or Updating Cards

When the user provides card details, store them in Keychain, not in this skill:

```sh
security add-generic-password -U -s ccs-cf -a cf -w '<json>'
```

Set the JSON with full card number and non-CVV billing details only. Immediately verify retrieval by parsing and printing only safe metadata.
