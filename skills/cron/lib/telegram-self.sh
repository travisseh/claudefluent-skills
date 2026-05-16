#!/usr/bin/env bash
# Send a Telegram message to the user via one of the project bots.
# Usage: telegram-self.sh <bot-name> <body-file>
#   bot-name: personal | copilot | gmr | product2 | claudefluent
#   body-file: path to text file containing the message body
#
# Reads bot tokens from ~/Programming/personal-master/personal/apps/telegram-claude/.env
# (TELEGRAM_BOT_TOKEN env var) and from the BOTS array in index.js for project-specific tokens.
# Owner chat id is hardcoded to the user's chat (1611615328).

set -euo pipefail

BOT_NAME="${1:?usage: telegram-self.sh <bot-name> <body-file>}"
BODY_FILE="${2:?usage: telegram-self.sh <bot-name> <body-file>}"
OWNER_ID="1611615328"
ENV_FILE="~/Programming/personal-master/personal/apps/telegram-claude/.env"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

case "$BOT_NAME" in
  personal)
    TOKEN="8508335378:AAEw6zDhZNj0o0uEnlFy6fq1_kLFg5hZwWI"
    ;;
  copilot)
    TOKEN="${TELEGRAM_COPILOT_BOT_TOKEN:-}"
    ;;
  gmr)
    TOKEN="7585966353:AAHp_S5jnZABFk7zQ2Wy37Gzo1aFOmxKAF8"
    ;;
  product2|exampleco)
    TOKEN="8599395082:AAGRp20W5hFta4wG3HkbRkErnJk2fu_DaxI"
    ;;
  marketing|claudefluent)
    TOKEN="8626541338:AAFNfW-dRX0RyOa6Gn7aV4TNuBAHyH1n60M"
    ;;
  *)
    echo "Unknown bot name: $BOT_NAME (expected: personal|copilot|gmr|product2|claudefluent)" >&2
    exit 2
    ;;
esac

if [[ -z "${TOKEN:-}" ]]; then
  echo "Missing Telegram token for bot: $BOT_NAME" >&2
  if [[ "$BOT_NAME" == "copilot" ]]; then
    echo "Set TELEGRAM_COPILOT_BOT_TOKEN in $ENV_FILE." >&2
  fi
  exit 2
fi

if [[ ! -f "$BODY_FILE" ]]; then
  echo "Body file not found: $BODY_FILE" >&2
  exit 2
fi

BODY="$(cat "$BODY_FILE")"
LEN=${#BODY}
MAX=4000

send_chunk() {
  local chunk="$1"
  curl -sS -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
    --data-urlencode "chat_id=${OWNER_ID}" \
    --data-urlencode "text=${chunk}" \
    --data-urlencode "parse_mode=Markdown" \
    --data-urlencode "disable_web_page_preview=true" \
    > /tmp/telegram-self-response.json
  if ! grep -q '"ok":true' /tmp/telegram-self-response.json; then
    echo "Telegram send failed:" >&2
    cat /tmp/telegram-self-response.json >&2
    return 1
  fi
}

if (( LEN <= MAX )); then
  send_chunk "$BODY"
else
  start=0
  total=$LEN
  while (( start < total )); do
    chunk="${BODY:start:MAX}"
    send_chunk "$chunk"
    start=$((start + MAX))
  done
fi

echo "telegram-self: sent $LEN chars to $BOT_NAME bot"
