#!/usr/bin/env node
// Post a message file to the user's self-DM in a Slack workspace.
// Usage: node slack-self-dm.js <workspace> <body-file>
// Workspace: exampleco | gmr | example-agency | claudefluent
//
// Self-DM channel IDs are cached at ~/.claude/skills/cron/state/self-dm-channels.json
// On cache miss, attempts discovery via conversations.list. If the workspace has no existing
// self-DM (token lacks im:write so we cannot create one), exits with instructions.

const fs = require('fs');
const path = require('path');
const os = require('os');

const SLACK_TOOLS_DIR = path.join(os.homedir(), '.config/slack-tools');
const SLACK_CONFIG = path.join(SLACK_TOOLS_DIR, 'config.json');
const CACHE_FILE = path.join(os.homedir(), '.claude/skills/cron/state/self-dm-channels.json');

(async () => {
  const [workspace, bodyFile] = process.argv.slice(2);
  if (!workspace || !bodyFile) {
    console.error('Usage: slack-self-dm.js <workspace> <body-file>');
    process.exit(1);
  }
  const text = fs.readFileSync(bodyFile, 'utf8');

  process.chdir(SLACK_TOOLS_DIR);
  const { WebClient } = require(path.join(SLACK_TOOLS_DIR, 'node_modules', '@slack/web-api'));

  const cfg = JSON.parse(fs.readFileSync(SLACK_CONFIG, 'utf8'));
  const ws = cfg.workspaces[workspace];
  if (!ws?.token) { console.error(`Workspace "${workspace}" not configured.`); process.exit(1); }

  fs.mkdirSync(path.dirname(CACHE_FILE), { recursive: true });
  let cache = {};
  try { cache = JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8')); } catch {}

  const client = new WebClient(ws.token);
  let channelId = cache[workspace];

  if (!channelId) {
    const myId = ws.userId;
    let cursor;
    do {
      const r = await client.conversations.list({ types: 'im', limit: 200, cursor });
      const found = r.channels.find(ch => ch.user === myId);
      if (found) { channelId = found.id; break; }
      cursor = r.response_metadata?.next_cursor;
    } while (cursor);

    if (!channelId) {
      console.error(`No self-DM exists yet in "${workspace}".`);
      console.error(`Open Slack → ${workspace} workspace → DM yourself → send any message → re-run this script.`);
      process.exit(1);
    }
    cache[workspace] = channelId;
    fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2) + '\n');
  }

  const CHUNK = 38000;
  const chunks = [];
  for (let i = 0; i < text.length; i += CHUNK) chunks.push(text.slice(i, i + CHUNK));

  let firstTs;
  for (const [i, body] of chunks.entries()) {
    const r = await client.chat.postMessage({
      channel: channelId,
      text: body,
      thread_ts: i === 0 ? undefined : firstTs,
    });
    if (i === 0) firstTs = r.ts;
  }
  console.log(`DM sent to ${workspace} (${channelId}). ts=${firstTs}`);
})().catch(e => { console.error('slack-self-dm failed:', e.message); process.exit(1); });
