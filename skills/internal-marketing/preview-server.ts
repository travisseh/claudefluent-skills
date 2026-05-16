import { createServer } from "http";
import { existsSync, readFileSync } from "fs";
import { join, resolve } from "path";
import { execSync } from "child_process";

const PORT = parseInt(process.argv[2] || "3999");
const SKILL_DIR = resolve(import.meta.dirname || __dirname);
const SCREENSHOTS_DIR = join(SKILL_DIR, "screenshots");

interface Message { channel: string; channelName: string; content: string; }

const messagesJson = process.argv[3];
const screenshotsList = process.argv[4]; // optional comma-separated list of screenshot filenames
if (!messagesJson) { console.error('Usage: npx tsx preview-server.ts [port] \'[...]\' [screenshot1.png,screenshot2.png]'); process.exit(1); }
const messages: Message[] = JSON.parse(messagesJson);
const allowedScreenshots: string[] | null = screenshotsList ? screenshotsList.split(",").map(s => s.trim()) : null;
let currentState: Message[] = JSON.parse(JSON.stringify(messages));

function getScreenshots(): string[] {
  if (!existsSync(SCREENSHOTS_DIR)) return [];
  try {
    const all = execSync(`ls "${SCREENSHOTS_DIR}"`).toString().trim().split("\n").filter((f) => /\.(png|jpg|jpeg|gif|webp)$/i.test(f));
    if (allowedScreenshots) return all.filter(f => allowedScreenshots.includes(f));
    return all;
  } catch { return []; }
}

const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Internal Marketing</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, sans-serif; background: #f4f4f4; color: #1d1c1d; padding: 32px; }
  h1 { font-size: 18px; font-weight: 700; margin-bottom: 24px; max-width: 720px; margin-left: auto; margin-right: auto; }
  .channels { display: flex; flex-direction: column; gap: 20px; max-width: 720px; margin: 0 auto; }
  .channel-card { background: #fff; border-radius: 8px; border: 1px solid #e0e0e0; }
  .channel-header { display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; border-bottom: 1px solid #f0f0f0; }
  .channel-name { font-size: 15px; font-weight: 700; }
  .channel-name::before { content: '# '; color: #999; }
  .send-btn { background: #007a5a; color: #fff; border: none; padding: 6px 16px; border-radius: 4px; cursor: pointer; font-size: 13px; font-weight: 700; }
  .send-btn:hover { background: #006a4e; }
  .send-btn:disabled { background: #ccc; cursor: not-allowed; }
  .send-btn.sent { background: #007a5a; opacity: 0.6; }
  .preview-btn-sm { background: #1264a3; color: #fff; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 13px; font-weight: 700; }
  .preview-btn-sm:hover { background: #0b4f8a; }
  .preview-btn-sm:disabled { background: #ccc; cursor: not-allowed; }
  .editor-area { padding: 12px 16px; }
  .editor-box { border: 1px solid #ddd; border-radius: 8px; overflow: hidden; }
  .editor-box:focus-within { border-color: #1264a3; box-shadow: 0 0 0 1px #1264a3; }
  .editor-toolbar { display: flex; gap: 2px; padding: 6px 8px; background: #fafafa; border-bottom: 1px solid #eee; }
  .editor-toolbar button { background: transparent; border: 1px solid transparent; color: #666; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-size: 13px; font-weight: 600; min-width: 28px; }
  .editor-toolbar button:hover { background: #f0f0f0; color: #333; }
  .editor-toolbar .spacer { flex: 1; }
  .rich-editor { min-height: 140px; padding: 12px 14px; font-size: 14px; line-height: 1.55; color: #1d1c1d; outline: none; white-space: pre-wrap; word-wrap: break-word; }
  .rich-editor code { background: #f0f0f0; padding: 2px 4px; border-radius: 3px; font-family: 'SF Mono', Monaco, monospace; font-size: 12px; color: #e01e5a; }
  .rich-editor ul, .rich-editor ol { padding-left: 1.5em; margin: 0.3em 0; }
  .screenshot-section { padding: 8px 16px 14px; }
  .screenshot-section h3 { font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #999; margin-bottom: 8px; font-weight: 600; }
  .screenshot-grid { display: flex; gap: 8px; flex-wrap: wrap; }
  .screenshot-item { position: relative; cursor: pointer; }
  .screenshot-item img { height: 100px; border-radius: 6px; border: 2px solid #e0e0e0; display: block; transition: all 0.15s; }
  .screenshot-item img.selected { border-color: #1264a3; }
  .screenshot-item img:hover { border-color: #1264a3; }
  .screenshot-item .check { position: absolute; top: 4px; right: 4px; width: 22px; height: 22px; background: #1264a3; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 13px; font-weight: 700; opacity: 0; transition: opacity 0.15s; }
  .screenshot-item img.selected + .check { opacity: 1; }
  .status { font-size: 12px; color: #999; padding: 4px 16px 8px; }
  .actions { display: flex; gap: 12px; justify-content: flex-end; align-items: center; margin-top: 20px; max-width: 720px; margin-left: auto; margin-right: auto; }
  .send-all-btn { background: #007a5a; color: #fff; border: none; padding: 8px 20px; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: 700; }
  .send-all-btn:hover { background: #006a4e; }
  .send-all-btn:disabled { background: #ccc; cursor: not-allowed; }
  .preview-btn { background: #1264a3; color: #fff; border: none; padding: 8px 20px; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: 700; }
  .preview-btn:hover { background: #0b4f8a; }
  .preview-btn:disabled { background: #ccc; cursor: not-allowed; }
  .global-status { font-size: 12px; color: #999; }
</style>
</head>
<body>
<h1>Internal Marketing</h1>
<div class="channels" id="channels"></div>
<div class="actions">
  <span class="global-status" id="global-status"></span>
  <button class="preview-btn" id="preview-all" onclick="previewAll()">Preview to Me</button>
  <button class="send-all-btn" id="send-all" onclick="sendAll()">Send All</button>
</div>
<script>
const messages = ${JSON.stringify(messages)};
let screenshots = ${JSON.stringify(getScreenshots())};
const selectedScreenshots = {};
const emojiMap = {':rocket:':'\\u{1F680}',':fire:':'\\u{1F525}',':wave:':'\\u{1F44B}',':warning:':'\\u26A0\\uFE0F',':tada:':'\\u{1F389}',':bulb:':'\\u{1F4A1}'};

messages.forEach((m,i) => { selectedScreenshots[i] = new Set(); });

function slackMrkdwnToHtml(text) {
  let h = text
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/\\*([^*\\n]+)\\*/g, '<strong>$1</strong>')
    .replace(/\`([^\`]+)\`/g, '<code>$1</code>');
  for (const [code, emoji] of Object.entries(emojiMap)) {
    h = h.split(code.replace(/[.*+?^\${}()|[\\]\\\\]/g,'\\\\$&')).join(emoji);
    h = h.replaceAll(code, emoji);
  }
  h = h.replace(/\\n/g, '<br>');
  return h;
}

function htmlToSlackMrkdwn(el) {
  let result = '';
  for (const node of el.childNodes) {
    if (node.nodeType === 3) { result += node.textContent; continue; }
    if (node.nodeType !== 1) continue;
    const tag = node.tagName.toLowerCase();
    if (tag === 'br') { result += '\\n'; }
    else if (tag === 'strong' || tag === 'b') { result += '*' + htmlToSlackMrkdwn(node) + '*'; }
    else if (tag === 'em' || tag === 'i') { result += '_' + htmlToSlackMrkdwn(node) + '_'; }
    else if (tag === 'code') {
      const codeText = node.textContent || '';
      if (codeText.length > 60 || codeText.includes('\\n')) {
        result += '\\n\`\`\`' + codeText + '\`\`\`\\n';
      } else {
        result += '\`' + codeText + '\`';
      }
    }
    else if (tag === 'div' || tag === 'p') {
      const inner = htmlToSlackMrkdwn(node);
      if (result && !result.endsWith('\\n')) result += '\\n';
      result += inner;
    }
    else if (tag === 'ul' || tag === 'ol') {
      const items = node.querySelectorAll(':scope > li');
      items.forEach((li, idx) => {
        if (result && !result.endsWith('\\n')) result += '\\n';
        result += (tag === 'ol' ? (idx+1) + '. ' : '- ') + htmlToSlackMrkdwn(li);
      });
    }
    else { result += htmlToSlackMrkdwn(node); }
  }
  // convert emoji back to shortcodes
  for (const [code, emoji] of Object.entries(emojiMap)) {
    result = result.replaceAll(emoji, code);
  }
  return result;
}

function renderChannels() {
  const container = document.getElementById('channels');
  container.innerHTML = messages.map((msg, i) => {
    const screenshotItems = screenshots.map((s) => {
      const isSelected = selectedScreenshots[i].has(s);
      return '<div class="screenshot-item" onclick="toggleScreenshot(this,' + i + ',\\'' + s + '\\')">' +
        '<img src="/screenshots/' + s + '"' + (isSelected ? ' class="selected"' : '') + ' data-file="' + s + '">' +
        '<div class="check">\\u2713</div></div>';
    }).join('');
    return '<div class="channel-card">' +
      '<div class="channel-header"><span class="channel-name">' + msg.channelName + '</span>' +
      '<div style="display:flex;gap:8px">' +
      '<button class="preview-btn-sm" id="preview-btn-' + i + '" onclick="previewOne(' + i + ')">Preview to Me</button>' +
      '<button class="send-btn" id="btn-' + i + '" onclick="sendOne(' + i + ')">Send</button>' +
      '</div></div>' +
      '<div class="editor-area"><div class="editor-box">' +
      '<div class="editor-toolbar">' +
        '<button onmousedown="event.preventDefault();doFormat(\\'bold\\')" title="Bold"><b>B</b></button>' +
        '<button onmousedown="event.preventDefault();doFormat(\\'italic\\')" title="Italic"><i>I</i></button>' +
        '<button onmousedown="event.preventDefault();doFormat(\\'code\\')" title="Code" style="font-family:monospace">{ }</button>' +
        '<button onmousedown="event.preventDefault();doFormat(\\'insertUnorderedList\\')" title="Bullet list">\\u2022</button>' +
        '<button onmousedown="event.preventDefault();doFormat(\\'insertOrderedList\\')" title="Numbered list">1.</button>' +
        '<div class="spacer"></div>' +
        '<span style="font-size:11px;color:#999;align-self:center">paste an image to attach</span>' +
      '</div>' +
      '<div class="rich-editor" id="editor-' + i + '" contenteditable="true" data-channel-idx="' + i + '">' + slackMrkdwnToHtml(msg.content) + '</div>' +
      '</div></div>' +
      '<div class="screenshot-section" id="screenshots-' + i + '">' + (screenshots.length > 0 ? '<h3>Attachments</h3><div class="screenshot-grid">' + screenshotItems + '</div>' : '') + '</div>' +
      '<div class="status" id="status-' + i + '"></div></div>';
  }).join('');
}

function doFormat(cmd) {
  if (cmd === 'code') {
    const sel = window.getSelection();
    if (sel.rangeCount) {
      const range = sel.getRangeAt(0);
      const code = document.createElement('code');
      range.surroundContents(code);
    }
  } else {
    document.execCommand(cmd, false, null);
  }
}

window.toggleScreenshot = function(el, idx, filename) {
  const img = el.querySelector('img');
  if (selectedScreenshots[idx].has(filename)) { selectedScreenshots[idx].delete(filename); img.classList.remove('selected'); }
  else { selectedScreenshots[idx].add(filename); img.classList.add('selected'); }
};

function getContent(i) {
  return htmlToSlackMrkdwn(document.getElementById('editor-' + i));
}

window.sendOne = async function(i) {
  const btn = document.getElementById('btn-' + i);
  const status = document.getElementById('status-' + i);
  btn.disabled = true; btn.textContent = 'Sending...';
  try {
    const res = await fetch('/send', { method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ channel: messages[i].channel, content: getContent(i), screenshots: Array.from(selectedScreenshots[i]) })
    });
    const data = await res.json();
    if (data.success) { btn.textContent = 'Sent'; btn.classList.add('sent'); status.textContent = 'Sent at ' + new Date().toLocaleTimeString(); }
    else { btn.textContent = 'Failed'; btn.disabled = false; status.textContent = 'Error: ' + (data.error || 'Unknown'); }
  } catch (e) { btn.textContent = 'Failed'; btn.disabled = false; status.textContent = 'Error: ' + e.message; }
};

window.sendAll = async function() {
  const btn = document.getElementById('send-all');
  btn.disabled = true; btn.textContent = 'Sending...';
  for (let i = 0; i < messages.length; i++) {
    if (!document.getElementById('btn-' + i).classList.contains('sent')) {
      await window.sendOne(i); await new Promise(r => setTimeout(r, 500));
    }
  }
  btn.textContent = 'All Sent';
  document.getElementById('global-status').textContent = 'All sent at ' + new Date().toLocaleTimeString();
};

function saveState() {
  const state = messages.map((msg, i) => ({
    channel: msg.channel,
    channelName: msg.channelName,
    content: getContent(i)
  }));
  fetch('/state', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(state) }).catch(() => {});
}

// Auto-save state on every edit
document.addEventListener('input', (e) => {
  if (e.target && e.target.closest && e.target.closest('.rich-editor')) saveState();
}, true);

// Paste handler — intercept image pastes, upload to server, attach to that channel
document.addEventListener('paste', async (e) => {
  const editor = e.target && e.target.closest && e.target.closest('.rich-editor');
  if (!editor) return;
  const items = e.clipboardData && e.clipboardData.items;
  if (!items) return;
  for (const item of items) {
    if (item.kind !== 'file' || !item.type.startsWith('image/')) continue;
    e.preventDefault();
    const file = item.getAsFile();
    if (!file) continue;
    const channelIdx = parseInt(editor.dataset.channelIdx);
    const status = document.getElementById('status-' + channelIdx);
    if (status) status.textContent = 'Uploading pasted image...';
    const reader = new FileReader();
    reader.onload = async () => {
      try {
        const ext = (item.type.split('/')[1] || 'png').replace('jpeg','jpg');
        const res = await fetch('/upload', {
          method: 'POST',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({ dataUrl: reader.result, ext })
        });
        const data = await res.json();
        if (data.success && data.filename) {
          if (!screenshots.includes(data.filename)) screenshots.push(data.filename);
          // select the new image only on the channel where it was pasted
          selectedScreenshots[channelIdx].add(data.filename);
          rerenderAttachments();
          if (status) status.textContent = 'Attached ' + data.filename;
        } else {
          if (status) status.textContent = 'Upload failed: ' + (data.error || 'unknown');
        }
      } catch (err) {
        if (status) status.textContent = 'Upload error: ' + err.message;
      }
    };
    reader.readAsDataURL(file);
    break;
  }
}, true);

function rerenderAttachments() {
  messages.forEach((msg, i) => {
    const section = document.getElementById('screenshots-' + i);
    if (!section) return;
    if (screenshots.length === 0) { section.innerHTML = ''; return; }
    const items = screenshots.map((s) => {
      const isSelected = selectedScreenshots[i].has(s);
      return '<div class="screenshot-item" onclick="toggleScreenshot(this,' + i + ',\\'' + s + '\\')">' +
        '<img src="/screenshots/' + s + '"' + (isSelected ? ' class="selected"' : '') + ' data-file="' + s + '">' +
        '<div class="check">\\u2713</div></div>';
    }).join('');
    section.innerHTML = '<h3>Attachments</h3><div class="screenshot-grid">' + items + '</div>';
  });
}

window.previewOne = async function(i) {
  const btn = document.getElementById('preview-btn-' + i);
  const status = document.getElementById('status-' + i);
  btn.disabled = true; btn.textContent = 'Previewing...';
  const DM_CHANNEL = 'D04PL43A3GF';
  const content = getContent(i);
  const label = '--- Preview for #' + messages[i].channelName + ' ---';
  try {
    await fetch('/send', { method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ channel: DM_CHANNEL, content: content + '\\n\\n' + label, screenshots: Array.from(selectedScreenshots[i]) })
    });
    btn.textContent = 'Previewed';
    if (status) status.textContent = 'Preview sent to your DM at ' + new Date().toLocaleTimeString();
  } catch(e) {
    btn.textContent = 'Failed';
    if (status) status.textContent = 'Preview error: ' + e.message;
  }
  setTimeout(() => { btn.disabled = false; btn.textContent = 'Preview to Me'; }, 3000);
};

window.previewAll = async function() {
  const btn = document.getElementById('preview-all');
  btn.disabled = true; btn.textContent = 'Previewing...';
  const DM_CHANNEL = 'D04PL43A3GF';
  for (let i = 0; i < messages.length; i++) {
    const content = getContent(i);
    const label = '--- Preview for #' + messages[i].channelName + ' ---';
    try {
      await fetch('/send', { method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ channel: DM_CHANNEL, content: content + '\\n\\n' + label, screenshots: Array.from(selectedScreenshots[i]) })
      });
    } catch(e) { console.error(e); }
    await new Promise(r => setTimeout(r, 500));
  }
  btn.textContent = 'Previewed';
  document.getElementById('global-status').textContent = 'Previews sent to your DM at ' + new Date().toLocaleTimeString();
  setTimeout(() => { btn.disabled = false; btn.textContent = 'Preview to Me'; }, 3000);
};

renderChannels();
</script>
</body>
</html>`;

const server = createServer(async (req, res) => {
  if (req.method === "GET" && req.url === "/") { res.writeHead(200, {"Content-Type":"text/html"}); res.end(html); return; }
  if (req.method === "GET" && req.url === "/state") {
    res.writeHead(200, {"Content-Type":"application/json"});
    res.end(JSON.stringify(currentState));
    return;
  }

  if (req.method === "POST" && req.url === "/state") {
    let body = ""; for await (const chunk of req) body += chunk;
    currentState = JSON.parse(body);
    res.writeHead(200, {"Content-Type":"application/json"});
    res.end(JSON.stringify({ success: true }));
    return;
  }

  if (req.method === "POST" && req.url === "/upload") {
    let body = ""; for await (const chunk of req) body += chunk;
    try {
      const { dataUrl, ext } = JSON.parse(body);
      const match = /^data:image\/[^;]+;base64,(.+)$/.exec(dataUrl || "");
      if (!match) {
        res.writeHead(200, {"Content-Type":"application/json"});
        res.end(JSON.stringify({ success: false, error: "Invalid data URL" }));
        return;
      }
      const buffer = Buffer.from(match[1], "base64");
      const safeExt = (ext || "png").replace(/[^a-z0-9]/gi, "").slice(0, 5) || "png";
      const filename = "pasted-" + Date.now() + "." + safeExt;
      const { writeFileSync, mkdirSync } = require("fs");
      mkdirSync(SCREENSHOTS_DIR, { recursive: true });
      writeFileSync(join(SCREENSHOTS_DIR, filename), buffer);
      // also include in allowedScreenshots so getScreenshots() picks it up if filtered
      if (allowedScreenshots && !allowedScreenshots.includes(filename)) allowedScreenshots.push(filename);
      res.writeHead(200, {"Content-Type":"application/json"});
      res.end(JSON.stringify({ success: true, filename }));
    } catch (e: any) {
      res.writeHead(200, {"Content-Type":"application/json"});
      res.end(JSON.stringify({ success: false, error: e.message }));
    }
    return;
  }
  if (req.method === "GET" && req.url?.startsWith("/screenshots/")) {
    const filename = decodeURIComponent(req.url.replace("/screenshots/", ""));
    const filepath = join(SCREENSHOTS_DIR, filename);
    if (existsSync(filepath)) { const ext = filename.split(".").pop()?.toLowerCase(); res.writeHead(200, {"Content-Type": ext === "png" ? "image/png" : "image/jpeg"}); res.end(readFileSync(filepath)); return; }
    res.writeHead(404); res.end("Not found"); return;
  }
  if (req.method === "POST" && req.url === "/send") {
    let body = ""; for await (const chunk of req) body += chunk;
    const { channel, content, screenshots } = JSON.parse(body);
    try {
      const { writeFileSync, unlinkSync } = require("fs");
      const tmpFile = join("/tmp", "slack-msg-" + Date.now() + ".txt");
      writeFileSync(tmpFile, content);
      let cmd: string;
      if (screenshots && screenshots.length > 0) {
        const filePaths = screenshots.map((s: string) => join(SCREENSHOTS_DIR, s)).join(" ");
        cmd = "node ~/.config/slack-tools/slack.js upload exampleco " + channel + " " + filePaths + " --message \"$(cat '" + tmpFile + "')\"";
      } else { cmd = "node ~/.config/slack-tools/slack.js send exampleco " + channel + " \"$(cat '" + tmpFile + "')\""; }
      const result = execSync(cmd, { timeout: 15000, shell: "/bin/bash" }).toString();
      try { unlinkSync(tmpFile); } catch {}
      res.writeHead(200, {"Content-Type":"application/json"}); res.end(JSON.stringify({ success: true, result: JSON.parse(result) }));
    } catch (e: any) { res.writeHead(200, {"Content-Type":"application/json"}); res.end(JSON.stringify({ success: false, error: e.message })); }
    return;
  }
  res.writeHead(404); res.end("Not found");
});
server.listen(PORT, () => { console.log(`Preview server running at http://localhost:${PORT}`); });
