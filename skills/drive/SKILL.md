---
name: drive
description: Save, upload, search, list, and manage Google Drive files across the user's personal, ExampleCo, Example Workspace, and ReviewCo Google accounts. Use when uploading CSVs, spreadsheets, docs, PDFs, or other files to personal Drive, ExampleCo Drive, Example Workspace Drive, or ReviewCo Drive; searching Drive; listing Drive folders; checking which account is authenticated; or cleaning up mistaken Drive uploads.
---

# Drive CLI

Use the bundled Drive helper:

```bash
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js <command> <account> ...
```

Prefer this helper over the Google Drive app connector when the target account matters. The app connector may be authenticated to the wrong Google Workspace account.

## Accounts

- `personal` - `user@example.com`
- `exampleco` - `user@example.com`
- `example-workspace` - `user@example.com`
- `gmr` - `user@example.com`

## Auth Model

- `example-workspace` currently works through the existing Example Workspace service account with Drive domain-wide delegation.
- `personal`, `exampleco`, and `gmr` should use this Drive helper's OAuth token store with Drive scope.
- Do not assume Gmail or Calendar tokens can write Drive files. They usually have insufficient scopes.
- If an account is missing or expired, run `add <account>` and complete the browser OAuth flow.

## Commands

```bash
# Show known accounts and auth source
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js list-accounts

# Verify which Google identity an account resolves to
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js profile example-workspace

# Add or refresh OAuth Drive access for personal/exampleco/gmr
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js add personal

# Upload CSV/XLSX/etc. as native Google Sheet
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js upload-spreadsheet example-workspace /absolute/path/report.csv "Report Title"

# Upload any file without conversion
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js upload-file personal /absolute/path/file.pdf "Optional Title"

# Search files
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js search gmr "name contains 'invoice' and trashed = false" 20

# List root or a folder
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js list example-workspace root 50
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js list example-workspace 1abcFolderId 50

# Trash a mistaken upload
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js trash exampleco 1abcFileId
```

## Workflow

1. For uploads, first run `profile <account>` unless the account was verified earlier in the same task.
2. Use `upload-spreadsheet` for CSV/TSV/XLS/XLSX files when the desired result is a native Google Sheet.
3. Use `upload-file` for PDFs, images, text files, or when preserving the original file type matters.
4. Return the `webViewLink` as a clickable Markdown link.
5. If a file is uploaded to the wrong account, use `trash <account> <fileId>` from that same account.
6. If auth fails with insufficient scopes, run `add <account>`; if it is a Workspace service-account error, report that domain-wide delegation needs Drive scope enabled for that account.

## Credential Locations

- Drive OAuth tokens: `~/.config/drive-tools/tokens.json`
- OAuth client: `~/.config/google-calendar-mcp/gcp-oauth.keys.json`
- Existing service-account registry: `~/.config/gmail-tools/service-accounts.json`
- Example Workspace direct key fallback: `~/.config/example-workspace-email/service-account.json`

