---
name: plugin-cron
description: "Create automated cron jobs that live inside Claude Code plugins. Use this skill whenever setting up scheduled tasks, daily briefs, automated reports, recurring prompts, or any time-based automation that runs claude -p. Also trigger when the user says 'add a cron', 'schedule this', 'run daily', 'automate this', 'daily email', or 'morning brief'. Triggers on: cron, schedule, automate, daily, recurring, launchd, timer."
---

# Plugin Cron Jobs

Create scheduled tasks that live inside Claude Code plugins. Crons run `claude -p` on a schedule, capture the output, and deliver it somewhere (email, Slack, file, etc).

When using this skill from Codex, create the cron files directly and treat any Claude-plugin references below as the target plugin layout, not as interactive slash commands.

## Directory Convention

Crons live in the plugin's `crons/` folder:

```
.claude/plugins/<plugin-name>/
  crons/
    <cron-name>/
      run.sh          # Entry point (bash script)
      send-email.ts   # Delivery script (optional, depends on delivery method)
      README.md       # What this cron does, how to test, how to modify
```

Each cron gets its own subfolder. The `run.sh` is always the entry point.

## Shell Script Template

```bash
#!/bin/bash
# <Description of what this cron does>

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="/Users/you/Programming/personal-master/personal"
OUTPUT_FILE="/tmp/<cron-name>-$(date +%Y-%m-%d).txt"
LOG_FILE="/tmp/<cron-name>.log"

echo "$(date): Starting <cron-name>" >> "$LOG_FILE"

export PATH="/opt/homebrew/bin:/Users/you/.nvm/versions/node/v22.17.0/bin:$PATH"
export HOME="/Users/you"
unset CLAUDECODE 2>/dev/null || true

cd "$PROJECT_DIR"

PROMPT='<Your prompt here. Tell Claude exactly what to read, what to do, and what to output.

IMPORTANT: Do NOT ask questions or wait for input. Just run the analysis and output the result.'

# claude -p outputs to stdout+stderr; capture everything
claude -p "$PROMPT" \
  --dangerously-skip-permissions \
  --max-turns 15 \
  > /tmp/<cron-name>-raw.txt 2>&1 || true

if [ -s /tmp/<cron-name>-raw.txt ]; then
  cp /tmp/<cron-name>-raw.txt "$OUTPUT_FILE"
  echo "$(date): Output captured ($(wc -c < "$OUTPUT_FILE") bytes)" >> "$LOG_FILE"
else
  echo "<cron-name> failed to generate output. Check $LOG_FILE" > "$OUTPUT_FILE"
  echo "$(date): No output generated" >> "$LOG_FILE"
fi

# === DELIVERY ===
# Pick one or more:

# Email (using Gmail API service account):
# npx tsx "$SCRIPT_DIR/send-email.ts" "$OUTPUT_FILE" >> "$LOG_FILE" 2>&1

# Slack webhook:
# curl -s -X POST -H 'Content-type: application/json' \
#   --data "{\"text\": \"$(cat "$OUTPUT_FILE")\"}" \
#   "$SLACK_WEBHOOK_URL" >> "$LOG_FILE" 2>&1

# Just log it:
# cat "$OUTPUT_FILE" >> "$LOG_FILE"

echo "$(date): <cron-name> complete" >> "$LOG_FILE"

# Clean up old files
find /tmp -name "<cron-name>-*.txt" -mtime +7 -delete 2>/dev/null || true
find /tmp -name "<cron-name>-raw.txt" -mtime +1 -delete 2>/dev/null || true
```

## Email Delivery Script Template

If delivering via email using the example-agency.com Gmail service account:

```typescript
import { google } from 'googleapis';
import * as fs from 'fs';
import * as path from 'path';

const SERVICE_ACCOUNT_PATH = path.join(process.env.HOME!, '.config/example-agency-email/service-account.json');
const SENDER_EMAIL = 'user@example.com';
const RECIPIENT_EMAIL = 'user@example.com';

async function sendEmail(subject: string, body: string) {
  const credentials = JSON.parse(fs.readFileSync(SERVICE_ACCOUNT_PATH, 'utf8'));
  const auth = new google.auth.JWT({
    email: credentials.client_email,
    key: credentials.private_key,
    scopes: ['https://mail.google.com/'],
    subject: SENDER_EMAIL,
  });

  const gmail = google.gmail({ version: 'v1', auth });

  const email = [
    `To: ${RECIPIENT_EMAIL}`,
    `From: ${SENDER_EMAIL}`,
    `Subject: ${subject}`,
    'Content-Type: text/plain; charset=utf-8',
    '',
    body,
  ].join('\n');

  const encodedEmail = Buffer.from(email)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');

  const result = await gmail.users.messages.send({
    userId: 'me',
    requestBody: { raw: encodedEmail },
  });
  console.log(`Email sent: ${result.data.id}`);
}

async function main() {
  const bodyFile = process.argv[2];
  if (!bodyFile) { console.error('Usage: send-email.ts <body-file> [subject]'); process.exit(1); }
  const body = fs.readFileSync(bodyFile, 'utf8');
  const date = new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' });
  const subject = process.argv[3] || `Daily Brief - ${date}`;
  await sendEmail(subject, body);
}

main().catch(err => { console.error('Failed:', err.message); process.exit(1); });
```

## Scheduling with launchd (macOS)

Create a plist in `~/Library/LaunchAgents/`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.<project>.<cron-name></string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/you/Programming/personal-master/personal/.claude/plugins/<plugin-name>/crons/<cron-name>/run.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/<cron-name>-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/<cron-name>-stderr.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>HOME</key>
        <string>/Users/you</string>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/Users/you/.nvm/versions/node/v22.17.0/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
```

### Managing launchd jobs

```bash
# Load (activate)
launchctl load ~/Library/LaunchAgents/com.<project>.<cron-name>.plist

# Unload (deactivate)
launchctl unload ~/Library/LaunchAgents/com.<project>.<cron-name>.plist

# Check status
launchctl list | grep <cron-name>

# Test run (from a separate terminal, NOT inside Claude Code)
bash /path/to/run.sh

# Check logs
cat /tmp/<cron-name>.log
```

## Key Gotchas

1. **Cannot test from inside Claude Code.** `claude -p` conflicts with the running session. Always test from a separate terminal.
2. **claude -p output capture.** Output goes to a mix of stdout/stderr. Use `> file.txt 2>&1` to capture everything.
3. **Always `unset CLAUDECODE`** in the script so it works whether run from a clean shell or triggered from inside a session.
4. **Always `cd` to the project dir** before running `claude -p` so it picks up CLAUDE.md, skills, and plugins.
5. **Use `--max-turns`** to prevent runaway sessions that burn API credits.
6. **Use `--dangerously-skip-permissions`** since there's no human to approve tool calls.
7. **launchd needs absolute paths** for everything. No `~` or `$HOME` in plists.
8. **googleapis must be in node_modules** of the project dir for send-email.ts to work. Run `npm install googleapis` if not already installed.

## Existing Crons

| Plugin | Cron | Schedule | Delivery | What it does |
|--------|------|----------|----------|--------------|
| marketing-brain | daily-brief | 7am daily | Email (example-agency) | Reads insights + daily notes + Stripe data, generates morning marketing brief |

## Creating a New Cron (Step by Step)

1. Create the directory: `.claude/plugins/<plugin>/crons/<name>/`
2. Copy `run.sh` template, fill in the prompt and delivery method
3. Copy `send-email.ts` if using email delivery
4. `chmod +x run.sh`
5. Test from a separate terminal: `bash /path/to/run.sh`
6. Create launchd plist in `~/Library/LaunchAgents/`
7. `launchctl load` the plist
8. Verify with `launchctl list | grep <name>`
