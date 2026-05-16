#!/bin/bash
# Send a body file to the user's own iMessage. Truncates to ~3000 chars.
# Usage: imessage-self.sh <body-file>

set -u

BODY_FILE="${1:-}"
if [ -z "$BODY_FILE" ] || [ ! -f "$BODY_FILE" ]; then
  echo "Usage: imessage-self.sh <body-file>" >&2
  exit 1
fi

PHONE="+18014337874"
LIMIT=3000

BODY="$(cat "$BODY_FILE")"
BYTES=$(printf '%s' "$BODY" | wc -c)
if [ "$BYTES" -gt "$LIMIT" ]; then
  BODY="$(printf '%s' "$BODY" | head -c "$LIMIT")
[…truncated]"
fi

node ~/.config/imessage-tools/imessage.js send "$PHONE" "$BODY"
