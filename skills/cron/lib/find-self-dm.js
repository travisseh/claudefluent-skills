#!/usr/bin/env node
// Discover and cache the self-DM channel ID for a Slack workspace.
// Usage: node find-self-dm.js [workspace]   — omit to scan all workspaces

const fs = require('fs');
const path = require('path');
const os = require('os');

const SLACK_TOOLS_DIR = path.join(os.homedir(), '.config/slack-tools');
const SLACK_CONFIG = path.join(SLACK_TOOLS_DIR, 'config.json');
const CACHE_FILE = path.join(os.homedir(), '.claude/skills/cron/state/self-dm-channels.json');

(async () => {
  const target = process.argv[2];
  process.chdir(SLACK_TOOLS_DIR);
  const { WebClient } = require(path.join(SLACK_TOOLS_DIR, 'node_modules', '@slack/web-api'));
  const cfg = JSON.parse(fs.readFileSync(SLACK_CONFIG, 'utf8'));

  fs.mkdirSync(path.dirname(CACHE_FILE), { recursive: true });
  let cache = {};
  try { cache = JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8')); } catch {}

  const names = target ? [target] : Object.keys(cfg.workspaces);
  for (const name of names) {
    const ws = cfg.workspaces[name];
    if (!ws?.token || !ws.userId) { console.log(`${name}: not configured`); continue; }
    const client = new WebClient(ws.token);
    let cursor, found;
    try {
      do {
        const r = await client.conversations.list({ types: 'im', limit: 200, cursor });
        found = r.channels.find(ch => ch.user === ws.userId);
        if (found) break;
        cursor = r.response_metadata?.next_cursor;
      } while (cursor);
    } catch (e) {
      console.log(`${name}: ERROR ${e.message}`);
      continue;
    }
    if (found) {
      cache[name] = found.id;
      console.log(`${name}: ${found.id}`);
    } else {
      console.log(`${name}: no self-DM yet — open Slack and DM yourself once, then re-run`);
    }
  }
  fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2) + '\n');
})().catch(e => { console.error('find-self-dm failed:', e.message); process.exit(1); });
