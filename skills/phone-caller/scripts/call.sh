#!/bin/bash
set -euo pipefail

# Bland.ai outbound phone caller
# Usage: call.sh <phone_number> <task> [voice] [max_duration]

PHONE="$1"
TASK="$2"
VOICE="${3:-josh}"
MAX_DURATION="${4:-10}"

source "$(git rev-parse --show-toplevel)/.env" 2>/dev/null || true

if [ -z "${BLAND_API_KEY:-}" ]; then
  echo '{"error": "BLAND_API_KEY not set in .env"}'
  exit 1
fi

RESPONSE=$(curl -s -X POST "https://api.bland.ai/v1/calls" \
  -H "authorization: $BLAND_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg phone "$PHONE" \
    --arg task "$TASK" \
    --arg voice "$VOICE" \
    --argjson max_duration "$MAX_DURATION" \
    '{
      phone_number: $phone,
      task: $task,
      voice: $voice,
      max_duration: $max_duration,
      wait_for_greeting: true,
      summary_prompt: "Summarize: was an appointment scheduled? Date/time? Cost estimate? Any prep instructions or next steps?"
    }'
  )")

CALL_ID=$(echo "$RESPONSE" | jq -r '.call_id // empty')

if [ -z "$CALL_ID" ]; then
  echo "$RESPONSE"
  exit 1
fi

echo "Call queued: $CALL_ID"
echo "Polling for results..."

for i in $(seq 1 40); do
  sleep 15
  RESULT=$(curl -s "https://api.bland.ai/v1/calls/$CALL_ID" \
    -H "authorization: $BLAND_API_KEY")

  STATUS=$(echo "$RESULT" | jq -r '.status // "unknown"')

  if [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ] || [ "$STATUS" = "no-answer" ] || [ "$STATUS" = "busy" ] || [ "$STATUS" = "canceled" ]; then
    echo "$RESULT" | jq '{
      status,
      answered_by,
      summary,
      call_length,
      price,
      concatenated_transcript,
      recording_url
    }'
    exit 0
  fi

  echo "  ...still in progress ($STATUS) - check $i/40"
done

echo '{"error": "Timed out waiting for call to complete", "call_id": "'"$CALL_ID"'"}'
exit 1
