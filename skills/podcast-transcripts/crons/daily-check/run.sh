#!/bin/bash
# Daily podcast transcript monitor
# Checks YouTube channels for new episodes, stores URLs + transcripts in Notion

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="/Users/you/Programming/personal-master/personal"
LOG_FILE="/tmp/podcast-monitor.log"

# Guard: don't run twice in one day
GUARD_FILE="/tmp/podcast-monitor-ran-$(date +%Y-%m-%d)"
if [ -f "$GUARD_FILE" ]; then
  echo "$(date): Already ran today, skipping" >> "$LOG_FILE"
  exit 0
fi
touch "$GUARD_FILE"

# Environment
export PATH="/opt/homebrew/bin:/Users/you/.nvm/versions/node/v22.17.0/bin:$PATH"
export HOME="/Users/you"

echo "$(date): Starting podcast monitor" >> "$LOG_FILE"

python3 "$PROJECT_DIR/.claude/skills/podcast-transcripts/scripts/podcast_monitor.py" \
  --verbose \
  >> "$LOG_FILE" 2>&1

echo "$(date): Podcast monitor complete" >> "$LOG_FILE"

# Cleanup old guard files
find /tmp -name "podcast-monitor-ran-*" -mtime +7 -delete 2>/dev/null || true
