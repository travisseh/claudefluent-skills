#!/usr/bin/env node
// Post a message file to a Slack channel.
// Usage: node slack-channel.js <workspace> <channel> <body-file>
//   workspace: exampleco | gmr | example-agency | claudefluent
//   channel:   #name | name | C0123ABC

const fs = require('fs');
const path = require('path');
const os = require('os');

const SLACK_TOOLS_DIR = path.join(os.homedir(), '.config/slack-tools');
const SLACK_CONFIG = path.join(SLACK_TOOLS_DIR, 'config.json');

(async () => {
  const [workspace, channelArg, bodyFile] = process.argv.slice(2);
  if (!workspace || !channelArg || !bodyFile) {
    console.error('Usage: slack-channel.js <workspace> <channel> <body-file>');
    process.exit(1);
  }
  const text = fs.readFileSync(bodyFile, 'utf8');

  process.chdir(SLACK_TOOLS_DIR);
  const { WebClient } = require(path.join(SLACK_TOOLS_DIR, 'node_modules', '@slack/web-api'));

  const cfg = JSON.parse(fs.readFileSync(SLACK_CONFIG, 'utf8'));
  const ws = cfg.workspaces[workspace];
  if (!ws?.token) { console.error(`Workspace "${workspace}" not configured.`); process.exit(1); }

  const client = new WebClient(ws.token);
  let channelId = channelArg;

  if (!/^[CGD][A-Z0-9]+$/.test(channelArg)) {
    const wanted = channelArg.replace(/^#/, '').toLowerCase();
    let cursor;
    do {
      const r = await client.conversations.list({ types: 'public_channel,private_channel', limit: 1000, cursor });
      const found = r.channels.find(c => c.name?.toLowerCase() === wanted);
      if (found) { channelId = found.id; break; }
      cursor = r.response_metadata?.next_cursor;
    } while (cursor);
    if (channelId === channelArg) {
      console.error(`Channel "${channelArg}" not found in ${workspace}.`);
      process.exit(1);
    }
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
  console.log(`Posted to ${workspace} ${channelArg} (${channelId}). ts=${firstTs}`);
})().catch(e => { console.error('slack-channel failed:', e.message); process.exit(1); });
