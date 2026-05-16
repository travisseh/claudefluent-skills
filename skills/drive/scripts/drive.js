#!/usr/bin/env node

const fs = require("fs");
const http = require("http");
const os = require("os");
const path = require("path");
const url = require("url");

const { google } = require(path.join(
  os.homedir(),
  ".config",
  "gmail-tools",
  "node_modules",
  "googleapis"
));
const googleAuth = require(path.join(os.homedir(), ".config", "google-tools", "auth"));

const CONFIG_DIR = path.join(os.homedir(), ".config", "drive-tools");
const TOKENS_FILE = path.join(CONFIG_DIR, "tokens.json");
const OAUTH_KEYS = path.join(
  os.homedir(),
  ".config",
  "google-calendar-mcp",
  "gcp-oauth.keys.json"
);
const GMAIL_SERVICE_ACCOUNTS = path.join(
  os.homedir(),
  ".config",
  "gmail-tools",
  "service-accounts.json"
);
const DENADA_KEY = path.join(os.homedir(), ".config", "example-workspace-email", "service-account.json");

const SCOPES = googleAuth.ALL_SCOPES;
const LOGIN_HINTS = googleAuth.LOGIN_HINTS;
const DEFAULT_SERVICE_ACCOUNT_ACCOUNTS = new Set([]);

function ensureConfigDir() {
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
}

function readJsonIfExists(file, fallback = {}) {
  if (!fs.existsSync(file)) return fallback;
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function writeJson(file, data) {
  ensureConfigDir();
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
}

function loadOAuthClient(overrideRedirectUri) {
  return null;
}

function loadTokens() {
  return googleAuth.loadTokens();
}

function saveTokens(tokens) {
  googleAuth.saveTokens(tokens);
}

function loadServiceAccountConfig(accountId) {
  const registry = readJsonIfExists(GMAIL_SERVICE_ACCOUNTS, {});
  if (registry[accountId]) {
    return registry[accountId];
  }
  if (accountId === "example-workspace" && fs.existsSync(DENADA_KEY)) {
    return { email: "user@example.com", keyFile: DENADA_KEY };
  }
  return null;
}

function getServiceAuthClient(accountId) {
  const cfg = loadServiceAccountConfig(accountId);
  if (!cfg) return null;
  const creds = readJsonIfExists(cfg.keyFile);
  if (!creds.client_email || !creds.private_key) {
    throw new Error(`Invalid service-account key for ${accountId}: ${cfg.keyFile}`);
  }
  return new google.auth.JWT({
    email: creds.client_email,
    key: creds.private_key,
    scopes: SCOPES,
    subject: cfg.email || LOGIN_HINTS[accountId],
  });
}

async function getOAuthAuthClient(accountId) {
  return googleAuth.getOAuthAuthClient(accountId);
}

async function getAuthClient(accountId) {
  if (DEFAULT_SERVICE_ACCOUNT_ACCOUNTS.has(accountId)) {
    const sa = getServiceAuthClient(accountId);
    if (sa) return sa;
  }
  return getOAuthAuthClient(accountId);
}

async function getDrive(accountId) {
  const auth = await getAuthClient(accountId);
  return google.drive({ version: "v3", auth });
}

function parseFolderRef(folderRef) {
  if (!folderRef || folderRef === "root") return "root";
  const match = String(folderRef).match(/\/folders\/([a-zA-Z0-9_-]+)/);
  return match ? match[1] : folderRef;
}

function fileNameForPath(filePath, title) {
  return title || path.basename(filePath);
}

async function addAccount(accountId) {
  return googleAuth.addAccount(accountId, {
    redirectUri: process.env.DRIVE_OAUTH_REDIRECT_URI,
    port: process.env.DRIVE_OAUTH_PORT ? Number(process.env.DRIVE_OAUTH_PORT) : 3999,
  });
}

async function listAccounts() {
  const tokens = loadTokens();
  const registry = readJsonIfExists(GMAIL_SERVICE_ACCOUNTS, {});
  const accounts = new Set([...Object.keys(LOGIN_HINTS), ...googleAuth.getKnownAccounts(), ...Object.keys(registry)]);
  const rows = [...accounts].sort().map((account) => ({
    account,
    email: registry[account]?.email || LOGIN_HINTS[account] || null,
    oauth: !!tokens[account],
    serviceAccount: !!loadServiceAccountConfig(account),
    defaultAuth: DEFAULT_SERVICE_ACCOUNT_ACCOUNTS.has(account) && loadServiceAccountConfig(account) ? "service-account" : "oauth",
  }));
  console.log(JSON.stringify(rows, null, 2));
}

async function profile(accountId) {
  const drive = await getDrive(accountId);
  const response = await drive.about.get({ fields: "user,storageQuota" });
  console.log(JSON.stringify(response.data, null, 2));
}

async function uploadSpreadsheet(accountId, sourceFile, title, folderRef) {
  const drive = await getDrive(accountId);
  const requestBody = {
    name: fileNameForPath(sourceFile, title),
    mimeType: "application/vnd.google-apps.spreadsheet",
  };
  if (folderRef) requestBody.parents = [parseFolderRef(folderRef)];
  const response = await drive.files.create({
    requestBody,
    media: {
      mimeType: sourceFile.endsWith(".tsv") ? "text/tab-separated-values" : "text/csv",
      body: fs.createReadStream(sourceFile),
    },
    fields: "id,name,mimeType,webViewLink,parents",
  });
  console.log(JSON.stringify(response.data, null, 2));
}

async function uploadFile(accountId, sourceFile, title, folderRef) {
  const drive = await getDrive(accountId);
  const requestBody = { name: fileNameForPath(sourceFile, title) };
  if (folderRef) requestBody.parents = [parseFolderRef(folderRef)];
  const response = await drive.files.create({
    requestBody,
    media: { body: fs.createReadStream(sourceFile) },
    fields: "id,name,mimeType,webViewLink,parents",
  });
  console.log(JSON.stringify(response.data, null, 2));
}

async function search(accountId, query, pageSize = 20) {
  const drive = await getDrive(accountId);
  const response = await drive.files.list({
    q: query,
    pageSize: Number(pageSize),
    fields: "files(id,name,mimeType,webViewLink,parents,createdTime,modifiedTime,trashed)",
    supportsAllDrives: true,
    includeItemsFromAllDrives: true,
  });
  console.log(JSON.stringify(response.data.files || [], null, 2));
}

async function listFolder(accountId, folderRef = "root", pageSize = 50) {
  const folderId = parseFolderRef(folderRef);
  await search(accountId, `'${folderId}' in parents and trashed = false`, pageSize);
}

async function trash(accountId, fileId) {
  const drive = await getDrive(accountId);
  const response = await drive.files.update({
    fileId,
    requestBody: { trashed: true },
    fields: "id,name,trashed",
    supportsAllDrives: true,
  });
  console.log(JSON.stringify(response.data, null, 2));
}

async function main() {
  const [command, accountId, ...args] = process.argv.slice(2);
  if (!command) {
    throw new Error("Usage: drive.js <list-accounts|add|profile|upload-spreadsheet|upload-file|search|list|trash> ...");
  }
  if (command === "list-accounts") return listAccounts();
  if (command === "add") return addAccount(accountId);
  if (!accountId) throw new Error(`Command "${command}" requires an account.`);

  if (command === "profile") return profile(accountId);
  if (command === "upload-spreadsheet") return uploadSpreadsheet(accountId, args[0], args[1], args[2]);
  if (command === "upload-file") return uploadFile(accountId, args[0], args[1], args[2]);
  if (command === "search") return search(accountId, args[0], args[1]);
  if (command === "list") return listFolder(accountId, args[0], args[1]);
  if (command === "trash") return trash(accountId, args[0]);
  throw new Error(`Unknown command: ${command}`);
}

main().catch((error) => {
  const detail = error?.response?.data || error.message || error;
  console.error(typeof detail === "string" ? detail : JSON.stringify(detail, null, 2));
  process.exit(1);
});
