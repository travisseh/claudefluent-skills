---
name: get-askelephant-token
description: Extract authentication token from AskElephant.ai using browser automation. Use when the AskElephant AUTH_TOKEN is expired or missing. Trigger with '/get-askelephant-token'.
---

# Get AskElephant Token

This skill uses browser automation to extract your AskElephant.ai authentication token from network requests.

## What it does

1. Opens AskElephant.ai in Chrome (or uses existing tab)
2. Injects JavaScript to intercept GraphQL requests
3. Navigates to trigger network requests
4. Captures the Bearer token from request headers via console logs
5. Saves the token to `.env` file for use with the transcript extractor

## How to use

Just invoke this skill:
```
/get-askelephant-token
```

Or say: "Get my AskElephant token"

## Output

The token will be:
- Captured from browser console logs
- Saved to `.env` as `AUTH_TOKEN`
- Ready to use with `npm run extract` or `npx ts-node extract-filtered.ts`

## Requirements

- Must be logged into AskElephant.ai in Chrome
- Chrome extension must be running

## Implementation Notes

The skill:
1. Hooks into `window.fetch` to intercept GraphQL requests
2. Logs the `authorization` header to console when a request is made
3. Navigates to meetings page to trigger requests
4. Reads console logs to extract the token (browser security blocks direct access)
5. Writes token to `.env` file in this directory

The token is a Firebase JWT that expires after ~1 hour. When it expires, just run this skill again to get a fresh token.
