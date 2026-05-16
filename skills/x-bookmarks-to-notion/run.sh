#!/bin/bash
# Daily X bookmarks → Notion sync. Runs headless via launchd.

set -u
PROJECT_DIR="~/Programming/personal-master/personal"
LOG_FILE="$PROJECT_DIR/artifacts/x-bookmarks-to-notion/cron.log"
SCRIPT="$PROJECT_DIR/.claude/skills/x-bookmarks-to-notion/sync.py"

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
export HOME="~"

mkdir -p "$(dirname "$LOG_FILE")"
cd "$PROJECT_DIR"

{
  echo ""
  echo "=== $(date '+%Y-%m-%d %H:%M:%S') ==="
  /usr/bin/python3 "$SCRIPT" --max 100 2>&1
  echo "exit=$?"
} >> "$LOG_FILE"
