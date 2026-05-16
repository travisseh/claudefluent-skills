---
name: cron
description: Create a local cron job that runs `claude -p` on a schedule and delivers output to a chosen destination (Slack DM, Slack channel, or self-iMessage). Use whenever the user says 'create a cron', 'schedule a job', 'run this daily/weekly', 'add a recurring task', 'automate this on a schedule', or wants any time-based local automation. Wraps the plugin-cron pattern with destination helpers, repo selection, and a required-fields checklist.
---

# Cron — Local Scheduled Jobs

Create a launchd-driven local cron job that fires `claude -p` on a schedule, then delivers output to a destination the user picks.

This skill is **local-only** by design. If a job has no skill/MCP/file-system dependencies and could run remotely, suggest `/schedule` (Anthropic remote routines) instead — but most of the user's crons need local skills, so default to local.

## Required Fields — gather these before writing any files

Always confirm with the user before generating files. Use AskUserQuestion to fill gaps.

1. **Name.** Short kebab-case slug (e.g. `daily-release-notes`, `weekly-bishopric-followups`).
2. **Schedule.** Time(s) of day + days of week. Default: daily at a specific hour. Convert anything fuzzy ("every morning") into an explicit hour:minute.
3. **Repo / host directory.** Determines which `.claude/skills/` and `.claude/plugins/` are loaded by `claude -p`. Default by topic:
   - **ExampleCo product / strategy / launches / scorecard / customer intel** → `~/Programming/product2`
   - **ExampleCo app code search / git inspection** → `~/Programming/exampleco`
   - **Personal life-OS / family / bishopric / chief-of-staff / property** → `~/Programming/personal-master/personal`
   - **ReviewCo marketing / sales** → `~/Programming/gmr-marketing`
   - If the cron needs skills from multiple repos, host it in the repo that has the *primary* skills. Crons can shell out to other repos for data.
4. **Destination.** Pick one (or more). Default: Slack self-DM in ExampleCo.
   - **Slack DM to self** in a workspace → see [Destination: Slack self-DM](#destination-slack-self-dm)
   - **Slack channel** in a workspace → see [Destination: Slack channel](#destination-slack-channel)
   - **iMessage to self** → see [Destination: iMessage self](#destination-imessage-self)
5. **What does the prompt do?** A clear one-paragraph description Claude will execute. Pin it down before writing the run.sh — vague prompts produce vague outputs.

If the user has not specified one of the five, ask. Don't invent.

## Directory Layout

```
<repo>/.claude/plugins/<plugin-name>/
  .claude-plugin/plugin.json
  commands/<cron-name>.md     # manual trigger as a slash command (mandatory)
  crons/<cron-name>/
    run.sh                    # cron entry point (chmod +x)
    README.md                 # what it does, how to test, how to reset
    [helpers]                 # fetch.js, dm.js, etc. as needed
  state/                      # any persistent state for this plugin
```

**Prefer adding a cron to an existing topical plugin over creating a new plugin per cron.** Crons are jobs, not topics. If a plugin already covers the domain (e.g. `product-brain` for ExampleCo product, `marketing-brain` for marketing, `bishopric` for ward, `provo-house` for the rental), drop the cron there as a sibling `crons/<cron-name>/` folder. State files for the cron go in that plugin's existing `state/` folder, namespaced clearly (e.g. `release-notes-shas.json`, not `last-shas.json`). Only create a new plugin when there's no existing topical home.

## File Templates

### `commands/<name>.md` (manual-trigger slash command — REQUIRED)

Every cron must have a sibling slash command in the plugin's `commands/` folder so the user can run it on demand without waiting for launchd. The slash command runs the **same pipeline** as `run.sh` but executes inside the active Claude Code session — so it must NOT call `claude -p` (would conflict). Instead, it shells out to the cron's helper scripts (fetch.js, dm.js, etc.) and Claude does the prompt work directly in the session.

The command file should:

1. Have YAML frontmatter with `description` (mirrors the cron's purpose) and `argument-hint` (commonly `force` for backfill, `no-dm` to skip delivery).
2. Reference the cron's helper scripts and state file by absolute-from-plugin paths.
3. Walk Claude through the same steps `run.sh` does, but inline:
   - Optionally backdate state if `force` was passed
   - Run any fetch/data-gathering helpers as subprocesses
   - Branch on empty vs non-empty results
   - Do the analysis/drafting in-session (no `claude -p`)
   - Print results inline so the user can read them in chat
   - Ask via AskUserQuestion before invoking the delivery helper (skip ask if `no-dm`)
4. Explicitly forbid invoking `claude -p` and forbid auto-sending to anything beyond the chosen self-destination.

See `~/Programming/product2/.claude/plugins/product-brain/commands/daily-release-notes.md` for a complete worked example.

### `crons/<name>/run.sh`

Use [`templates/run.sh.template`](templates/run.sh.template) as the starting point. Substitute:
- `__CRON_NAME__` — the slug
- `__PROJECT_DIR__` — absolute path to the chosen repo
- `__PROMPT__` — the prompt to run via `claude -p`
- `__DELIVERY_BLOCK__` — the destination snippet (see below)
- `__MAX_TURNS__` — default 15 unless the prompt is heavier

### Plist (`~/Library/LaunchAgents/com.user.<cron-name>.plist`)

Use [`templates/plist.template`](templates/plist.template). Substitute the slug, absolute run.sh path, and `Hour`/`Minute` (or use `StartCalendarInterval` array for multiple times / weekday filtering).

For a weekday-only 9 AM job:
```xml
<key>StartCalendarInterval</key>
<array>
  <dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
  <dict><key>Weekday</key><integer>2</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
  <dict><key>Weekday</key><integer>3</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
  <dict><key>Weekday</key><integer>4</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
  <dict><key>Weekday</key><integer>5</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
</array>
```

## Delivery: how to send output

Each helper takes one argument: a path to a text file containing the message.

### Destination: Slack self-DM

Use the global helper. Workspace = `exampleco | gmr | example-agency | claudefluent`.

```bash
node ~/.claude/skills/cron/lib/slack-self-dm.js <workspace> <body-file>
```

**Channel discovery.** The first time a workspace is used, the helper looks up the self-DM channel ID and caches it at `~/.claude/skills/cron/state/self-dm-channels.json`. If the workspace has no existing self-DM (the user has never DMed himself there), the helper exits with an error and tells him to open Slack → message himself → re-run. Currently cached:

| Workspace | Self-DM channel | Status |
|-----------|-----------------|--------|
| exampleco | `D04PL43A3GF` | confirmed working |
| gmr | — | OAuth token not yet configured in `~/.config/slack-tools/config.json`. Run `node ~/.config/slack-tools/slack.js workspaces` and add the token before using. |
| example-agency | — | OAuth token not yet configured. Same as above. |
| claudefluent | — | OAuth token not yet configured. Same as above. |

If a workspace is configured but the self-DM channel hasn't been opened, the helper exits and tells the user to DM himself once in Slack, then run `node ~/.claude/skills/cron/lib/find-self-dm.js <workspace>` to cache the ID.

The ExampleCo Slack token is missing the `im:write` scope, so the helper cannot *open* a new self-DM — it can only post to one that already exists. If the user picks a workspace with no self-DM yet, walk him through creating it once, then run `node ~/.claude/skills/cron/lib/find-self-dm.js <workspace>` to cache it.

### Destination: Slack channel

```bash
node ~/.claude/skills/cron/lib/slack-channel.js <workspace> <channel-name-or-id> <body-file>
```

Channel can be `#home-cs`, `home-cs`, or a channel ID like `C012345`. The helper resolves the name to an ID via the API.

### Destination: iMessage self

Sends to the user's number `+18014337874` (his iCloud-linked phone). Useful for high-priority alerts that should buzz his phone.

```bash
bash ~/.claude/skills/cron/lib/imessage-self.sh <body-file>
```

Requires the user's Mac to be awake and signed into iMessage. If the cron output is long, the helper truncates to ~3000 chars and appends `[…truncated]`.

### Destination: Telegram self

Sends a Telegram DM to the user via the project-specific bot. Bot tokens are baked into the helper; chat ID is `1611615328`. Bots already configured:

| Bot name | Telegram handle | Best for |
|----------|-----------------|----------|
| `personal` | @claude_personal_bot | Life-OS, family, bishopric, chief-of-staff crons |
| `gmr` | @claude_gmr_bot | ReviewCo-related crons |
| `product2` | @claude_product2_bot (ExampleCo) | ExampleCo product/strategy crons |
| `claudefluent` | @cc_marketing_bot | ClaudeFluent marketing crons |

```bash
bash ~/.claude/skills/cron/lib/telegram-self.sh <bot-name> <body-file>
```

The helper auto-chunks at 4000 chars, sends with `parse_mode=Markdown`, and uses `*x*` for bold and `_x_` for italics (NOT Slack syntax). It's quieter than iMessage (Telegram is muted on the user's phone unless he opens the app), so prefer Telegram for daily intel/digests and iMessage for things that should actually buzz him.

## Required Run.sh Behaviors

Every cron run.sh must:

1. Set `PATH` and `HOME` explicitly. launchd has minimal env.
2. `unset CLAUDECODE` so `claude -p` works whether or not the parent shell is a Claude session.
3. `cd "$PROJECT_DIR"` before invoking `claude -p` — this loads the right CLAUDE.md, skills, and plugins.
4. Use `--dangerously-skip-permissions` and `--max-turns N` (no human to approve, prevent runaway).
5. Capture output with `> "$RAW_OUT" 2>&1 || true` — never let the cron crash mid-run.
6. Log every run to `/tmp/<cron-name>.log` with timestamps.
7. Always send *some* delivery, even on failure — the user needs to know if a cron silently dies.
8. Clean up old `/tmp/<cron-name>-*.txt` files (`-mtime +14 -delete`).

## Testing

**Cannot test from inside Claude Code.** `claude -p` conflicts with the running session. Always tell the user to test from a separate terminal:

```bash
bash <repo>/.claude/plugins/<plugin>/crons/<cron-name>/run.sh
tail -50 /tmp/<cron-name>.log
```

Helper components (fetch scripts, DM helpers) CAN be tested from inside Claude Code if they don't invoke `claude -p`. Always test those before scheduling.

## Loading the launchd Job

```bash
launchctl unload ~/Library/LaunchAgents/com.user.<cron-name>.plist 2>/dev/null
launchctl load   ~/Library/LaunchAgents/com.user.<cron-name>.plist
launchctl list | grep <cron-name>
```

A `0` in the second column means "not currently running, load OK." A negative number means launchd refused — check the plist.

## Pre-flight Checklist (before declaring done)

- [ ] All five required fields confirmed with the user
- [ ] Plugin folder + crons subfolder created in the chosen repo
- [ ] `run.sh` is executable (`chmod +x`)
- [ ] Helper scripts (fetch.js, etc.) are executable
- [ ] State files (if any) are seeded sensibly (first run shouldn't drown in backlog)
- [ ] Destination helper chosen and tested with a small payload
- [ ] launchd plist created, loaded, listed
- [ ] **Sibling `commands/<cron-name>.md` slash command created** so the user can manually trigger the same pipeline in-session
- [ ] the user told how to test from a separate terminal
- [ ] README in the cron folder so future-Claude can modify it without spelunking

## Existing Crons (registry)

| Repo | Plugin | Cron | Manual command | Schedule | Destination | What it does |
|------|--------|------|----------------|----------|-------------|--------------|
| `personal-master/personal` | marketing-brain | daily-brief | _(none yet — backfill recommended)_ | 7am daily | Email (example-agency) | Marketing brief from insights + Stripe |
| `product2` | product-brain | daily-release-notes | `/daily-release-notes` | 9am daily | Slack DM (exampleco) | ExampleCo/exampleco + exampleco-consumers merge scan, classifies user-visible vs internal, drafts internal-marketing messages |
| `product2` | product-brain | lennys-podcast-daily | `/lennys-podcast-daily` | 7am daily | Telegram (product2 bot) | Scans Lenny's podcast (lennysdata MCP) for new episodes since last run, scores ExampleCo/CF relevance, sends digest |
| `personal-master/personal` | marketing-brain | daily-content-ideas | `/daily-content-ideas` | 9am daily | Telegram (claudefluent bot) | Pulls last-24h cc-experts panel + Notion Podcast Transcripts, dedups against existing Generated Ideas, drafts 3-5 LinkedIn ideas (varied modes) via user-writing-style, writes to Notion Content Calendar with Status="Generated Ideas" |

When adding a new cron, append a row including the slash command name.

## What This Skill Does NOT Do

- **Vercel cron / remote routines.** Local-only. For remote, use `/schedule`.
- **Email delivery.** Existing pattern lives in `plugin-cron` skill. Reference that if needed.
- **Long-running daemons.** launchd `KeepAlive` is out of scope.
- **Self-DM bootstrap in new Slack workspaces.** Token lacks `im:write`. User has to open the DM manually first.
