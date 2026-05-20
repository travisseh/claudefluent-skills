---
name: digitalocean-app-platform
description: Manage and monitor Example Company DigitalOcean App Platform apps from Codex. Use for listing apps, inspecting in-store-reporting/in-store-dashboard, checking deployments after git pushes, triggering deployments, and updating App Platform specs/env vars/secrets.
enabled: true
tags: [digitalocean, app-platform, deployments, boostly, doctl, mcp]
---

# DigitalOcean App Platform

Use this skill when Travisse asks about DigitalOcean App Platform apps, deploys, environment variables, secrets, or monitoring after a git push.

## Auth

DigitalOcean auth is stored outside the repo:

```bash
source ~/.config/digitalocean/env
```

That file should export `DIGITALOCEAN_API_TOKEN`. Never print the token, paste it into responses, commit it, or write it into repo files.

Codex MCP is configured globally in `~/.codex/config.toml`:

```toml
[mcp_servers.digitalocean]
command = "zsh"
args = ["-lc", "source ~/.config/digitalocean/env && exec npx -y @digitalocean/mcp --services apps"]
```

Prefer the `digitalocean` MCP tools when they are available in a thread. If not available, use `doctl` with `--access-token "$DIGITALOCEAN_API_TOKEN"`.

## Known Example Company Apps

Primary TapCards / in-store app:

- DigitalOcean live app name: `in-store-reporting`
- Local spec name: `in-store-dashboard`
- App ID: `5172b789-9b54-4c11-ba7c-c6ac49070335`
- Default URL: `https://in-store-reporting-5tmly.ondigitalocean.app`
- Source repo: `Example Company/product`
- Branch: `main`
- Source dir: `public/apps/tapcards-dashboard`
- Local spec: `/Users/you/Programming/product2/public/apps/tapcards-dashboard/.do/app.yaml`

Other apps currently seen:

- `etc-web-client`
- `etc-api`

## Standard Commands

List apps:

```bash
source ~/.config/digitalocean/env
doctl apps list --access-token "$DIGITALOCEAN_API_TOKEN"
```

Inspect the TapCards / in-store app:

```bash
source ~/.config/digitalocean/env
doctl apps get 5172b789-9b54-4c11-ba7c-c6ac49070335 --access-token "$DIGITALOCEAN_API_TOKEN"
```

List recent deployments:

```bash
source ~/.config/digitalocean/env
doctl apps list-deployments 5172b789-9b54-4c11-ba7c-c6ac49070335 --access-token "$DIGITALOCEAN_API_TOKEN"
```

Trigger a deployment:

```bash
source ~/.config/digitalocean/env
doctl apps create-deployment 5172b789-9b54-4c11-ba7c-c6ac49070335 --access-token "$DIGITALOCEAN_API_TOKEN"
```

Update app from the local spec:

```bash
source ~/.config/digitalocean/env
doctl apps update 5172b789-9b54-4c11-ba7c-c6ac49070335 \
  --spec /Users/you/Programming/product2/public/apps/tapcards-dashboard/.do/app.yaml \
  --access-token "$DIGITALOCEAN_API_TOKEN"
```

## Deployment Monitoring Workflow

After a git push to `Example Company/product` `main`:

1. List deployments for app `5172b789-9b54-4c11-ba7c-c6ac49070335`.
2. Find the newest deployment whose cause mentions the pushed commit.
3. Poll until `Phase` is `ACTIVE`, `ERROR`, `CANCELED`, or `SUPERSEDED`.
4. Report the deployment ID, phase, progress, cause, and timestamps.

Example:

```bash
source ~/.config/digitalocean/env
doctl apps list-deployments 5172b789-9b54-4c11-ba7c-c6ac49070335 \
  --access-token "$DIGITALOCEAN_API_TOKEN"
```

## Env Vars And Secrets

Relevant spec file:

```bash
/Users/you/Programming/product2/public/apps/tapcards-dashboard/.do/app.yaml
```

Known envs in the app spec:

- `TAPCARDS_DB_HOST` secret
- `TAPCARDS_DB_PORT`
- `TAPCARDS_DB_NAME`
- `TAPCARDS_DB_USER` secret
- `TAPCARDS_DB_PASSWORD` secret
- `V2_DATABASE_URL` secret

For secret changes, prefer updating the App Platform spec through DigitalOcean tooling without exposing secret values in command output. If a secret value must be entered, ask Travisse for it at action time and do not echo it. Do not write secret values into the repo.

Before applying an app spec update, show the non-secret spec diff or summarize the exact env keys being added/changed. Updating the live app spec can trigger deployments and affect production.

## Safety Rules

- Never print `DIGITALOCEAN_API_TOKEN` or secret env var values.
- Never commit `~/.config/digitalocean/env`, `.env`, or generated files containing secrets.
- Use the app ID for production actions to avoid the `in-store-reporting` vs `in-store-dashboard` naming mismatch.
- Treat `doctl apps update` and secret/env changes as production changes. Confirm the exact intended change before applying.
- If `doctl auth init` is awkward in non-interactive terminal sessions, skip persisted `doctl` auth and use `--access-token "$DIGITALOCEAN_API_TOKEN"` per command.
