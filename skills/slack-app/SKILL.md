---
name: slack-app
description: Create and configure Slack AI agents with the fewest manual steps, especially agent_view manifests, Socket Mode, Slack agent container events, OAuth scopes, app-level tokens, top-bar enablement, and env vars for Node/TypeScript Slack agents. Use when the user asks to create a Slack app, Slack bot, Slackbot, Slack agent, Slack AI app, app manifest, Socket Mode setup, or Slack app setup instructions.
---

# Slack App

## Default Approach

Build Slack AI agent experiences by default, not slash-command-first bots.

The preferred UX is:

- Slack top-bar agent picker.
- Side-by-side agent chat.
- App Chat and History tabs.
- Suggested prompts for common tasks.
- Socket Mode for internal tools so no public request URL or ngrok is needed.

Use `agent_view` as the default manifest feature. Do not recommend `assistant_view` as the primary path. If Slack's manifest validator rejects `agent_view`, treat that as a workspace/settings blocker to resolve, not as a reason to teach the older assistant framing.

Slash commands and app mentions are optional compatibility surfaces. Add them only when the user specifically wants them or when channel mentions are materially better than the agent panel.

## Setup Mode Gate

Before touching Slack settings, browser profiles, or secrets, ask which setup mode to use unless the user already made it explicit:

- **Share-safe mode**: generate the manifest and concise human steps. The user creates tokens, installs the app, and pastes env vars themselves. Use this by default when the skill may be shared, demoed, or reused outside your own machine.
- **Aggressive local mode**: use Browser/Computer Use to create tokens, reveal/capture secrets, install the app, write env vars into a gitignored local `.env`, restart the agent, and test it. Only use this when the user explicitly approves local automation and secret handling.

Phrase the question briefly, for example: "Do you want share-safe mode, where I give you the manifest and steps, or aggressive local mode, where I use your browser to create/install the app and write the env vars locally?"

## Fast Path

1. Generate an agent-first manifest with `scripts/generate_manifest.py`.
2. In share-safe mode, give the user the manifest and tell them to choose **From a manifest** in [Slack API Apps](https://api.slack.com/apps).
3. In aggressive local mode, use Browser/Computer Use to paste the manifest, create the app, create the App-Level Token with `connections:write`, install it, and collect/write env vars.
4. After install, open Slack workspace app management for the installed app and verify:
   - **Agents & AI Apps** is enabled.
   - **Show <app> on Slack's top bar** is enabled.
5. Run/restart the Socket Mode agent and test from the Slack top-bar agent picker or the app Chat tab.

## Generate Manifest

Run from the skill directory or use the absolute path:

```bash
python3 scripts/generate_manifest.py \
  --name "ClaudeFluent Agent" \
  --description "Ask ClaudeFluent operational questions from Slack." \
  --agent-description "Ask ClaudeFluent operational questions, including status, sessions, customers, emails, and what to do next." \
  --prompt "ClaudeFluent status|status" \
  --prompt "Next session|next" \
  --prompt "What should I do next?|What should I do next for ClaudeFluent?"
```

For a generic internal agent:

```bash
python3 scripts/generate_manifest.py \
  --name "Team Agent" \
  --description "Ask operational questions from Slack." \
  --agent-description "Ask team operational questions and get workspace-aware answers." \
  --prompt "Status|status" \
  --prompt "What needs attention?|What needs attention today?"
```

If the user explicitly wants a slash command too, add `--command "/team"` and `--usage "status | ask <question>"`. Keep the agent UX as the primary surface.

## Required Env Vars

For a Socket Mode Slack AI agent, collect:

- `SLACK_BOT_TOKEN`: OAuth & Permissions -> Bot User OAuth Token (`xoxb-...`)
- `SLACK_SIGNING_SECRET`: Basic Information -> Signing Secret
- `SLACK_APP_TOKEN`: Basic Information -> App-Level Tokens -> generate token with `connections:write` (`xapp-...`)
- `SLACK_ALLOWED_TEAM_ID`: workspace/team ID for the intended workspace

For project-specific agents, append project env vars after these. Example for ClaudeFluent:

```bash
CF_CONVEX_URL=https://polite-toad-76.convex.cloud
CF_TIMEZONE=America/Denver
ANTHROPIC_API_KEY=
CLAUDE_MANAGED_AGENT_ID=
CLAUDE_MANAGED_ENVIRONMENT_ID=
```

## Browser-Assisted Setup

Only use this section in aggressive local mode. Use Computer Use against the correct Chrome profile and keep secrets out of chat unless the user explicitly needs paste-ready env values.

Recommended flow:

1. Open the correct browser profile for the target Slack workspace and go to the Slack app URL.
2. Create the app from the agent-first manifest at [Slack API Apps](https://api.slack.com/apps).
3. In Slack app settings, verify the app is the intended app and workspace. The team ID appears in app settings URLs like `app.slack.com/app-settings/<TEAM_ID>/<APP_ID>/...`.
4. Basic Information -> App Credentials -> click **Show** beside **Signing Secret** and capture `SLACK_SIGNING_SECRET`.
5. Basic Information -> App-Level Tokens -> **Generate Token and Scopes**:
   - Token name: use a project-specific name, e.g. `cf-slack-agent-socket-mode`.
   - Scope: `connections:write`.
   - Capture the resulting `SLACK_APP_TOKEN` (`xapp-...`).
6. Install App -> **Install to <workspace>** -> **Allow**.
7. Installed App Settings -> OAuth Tokens -> capture **Bot User OAuth Token** as `SLACK_BOT_TOKEN` (`xoxb-...`).
8. Open Slack workspace app management for the installed app:
   - Manage apps -> Installed Apps -> `<App Name>` -> App Settings.
   - Confirm **Agents & AI Apps** is **Enabled**.
   - Click **Show <App Name> on Slack's top bar**, choose **Enabled**, and save.
9. Write the four Slack env vars into the local agent `.env` only if that `.env` is gitignored. Verify with `git check-ignore -v path/to/.env` before saving secrets.
10. Restart the Socket Mode agent and confirm the log says it is running.
11. Test from Slack's top-bar agent picker or the app Chat tab. If the picker does not appear, reload Slack desktop/web and re-check the top-bar setting.

If using Computer Use, start each browser automation turn with `get_app_state` before clicking, prefer element-index clicks, and verify after each action. Do not use the clipboard unless the user asks.

## Runtime Expectations

Implement the app as a chat-first Slack agent:

- Listen for `assistant_thread_started`. Slack still uses this event name for the agent container.
- Listen for `assistant_thread_context_changed` when context matters.
- Listen for `message.im` so users can chat from the app Chat tab.
- Acknowledge quickly and post/update a "working" message for slow operations.
- Return generic user-facing errors and log detailed internal errors server-side.

For Bolt/TypeScript apps, the manifest should include:

- `features.agent_view`
- `features.app_home.messages_tab_enabled: true`
- `oauth_config.scopes.bot`: `assistant:write`, `chat:write`, `im:history`
- `settings.socket_mode_enabled: true`
- `settings.event_subscriptions.bot_events`: `assistant_thread_started`, `assistant_thread_context_changed`, `message.im`

## Optional Surfaces

Add these only when needed:

- Slash command: add `commands` scope and `features.slash_commands`.
- Public-channel mentions: add `app_mentions:read`, `channels:read`, and `channels:join`, reinstall the app, then join the bot to all non-archived public channels with `conversations.join`.
- Channel history: add `channels:history`, `groups:history`, or `mpim:history` only when the agent truly needs to read those conversations.
- User lookup: add `users:read` only if resolving user IDs or names is required.
- Files: add `files:read` or `files:write` only if file access is explicitly needed.

Keep write scopes minimal. Do not add admin scopes by default. Private channels cannot be joined automatically by a normal bot token; a member must invite the app.

## Minimal User Instructions

When handing this to the user, keep it short:

1. Paste this manifest into Slack's **From a manifest** flow.
2. Create an App-Level Token with `connections:write`.
3. Install the app and paste the four Slack env vars into `.env`.
4. In Manage apps -> Installed Apps -> `<App Name>` -> App Settings, enable top-bar display.
5. Run the agent locally or deploy it.

Do not include a long Slack UI tutorial unless he gets stuck.

## Verification

After setup:

- Start the agent process.
- Confirm logs say the Socket Mode app is running.
- Test from Slack's top-bar agent picker.
- Test the app Chat tab.
- In app management, verify **Agents & AI Apps** is enabled.
- In app management, verify **Show <App Name> on Slack's top bar** is enabled.
- If events do not arrive, check Socket Mode is enabled and the app token starts with `xapp-`.
- If messages cannot post, reinstall the app after adding `chat:write`.
- If the top-bar picker does not show, reload Slack desktop/web and re-check the installed app's App Settings.
