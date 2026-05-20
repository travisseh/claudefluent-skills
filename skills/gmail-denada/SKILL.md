---
name: gmail-example-agency
description: "Send/read email and manage Google Drive files for user.com using service account authentication. Use this skill whenever the user wants to send emails from Denada, check the Denada inbox, search Denada messages, draft emails for Denada Design business, upload files to Denada Drive, create Google Docs/Sheets in Denada Drive, or search/manage Denada Drive files. Also trigger when they mention 'example-agency email', 'email from example-agency', 'send as example-agency', 'example-agency drive', 'example-agency.design drive', or reference the example-agency.design account. Triggers on: example-agency email, example-agency.design, send email example-agency, check example-agency inbox, example-agency messages, example-agency drive, upload to example-agency drive."
---

# Gmail and Drive - example-agency.design

Send/read emails and manage Google Drive files for `user.com`.

Prefer the shared Gmail CLI first:

`node ~/.config/gmail-tools/gmail.js`

## Preferred Email Usage

```bash
# Inbox / unread
node ~/.config/gmail-tools/gmail.js inbox example-agency 10
node ~/.config/gmail-tools/gmail.js unread example-agency 20

# Search / read
node ~/.config/gmail-tools/gmail.js search example-agency "from:client" 10
node ~/.config/gmail-tools/gmail.js read example-agency "from:client subject:proposal"

# Draft / send / reply
node ~/.config/gmail-tools/gmail.js draft example-agency "client@example.com" "Subject" "Body"
node ~/.config/gmail-tools/gmail.js send example-agency "client@example.com" "Subject" "Body"
node ~/.config/gmail-tools/gmail.js reply example-agency "from:client subject:proposal" "Reply body"

# Download attachments
node ~/.config/gmail-tools/gmail.js download example-agency "has:attachment from:client" /tmp
```

## Email Search Query Examples

- `from:someone@example.com` - emails from specific sender
- `to:someone@example.com` - emails to specific recipient
- `subject:invoice` - emails with subject containing "invoice"
- `is:unread` - unread emails
- `after:2026/01/01` - emails after date
- `has:attachment` - emails with attachments
- `label:inbox` - emails in inbox

## Drive Access

The same Denada service account now has Google Drive domain-wide delegation for `user.com`.

Use the local `googleapis` package from the Gmail tools install:

```js
const { google } = require("/Users/you/.config/gmail-tools/node_modules/googleapis");
const key = require("/Users/you/.config/example-agency-email/service-account.json");

const auth = new google.auth.JWT({
  email: key.client_email,
  key: key.private_key,
  scopes: ["https://www.googleapis.com/auth/drive"],
  subject: "user.com",
});

const drive = google.drive({ version: "v3", auth });
```

Common Drive operations:

```js
// Verify the impersonated account
await auth.authorize();
await drive.about.get({ fields: "user" });

// Upload a CSV as a native Google Sheet
await drive.files.create({
  requestBody: {
    name: "Report Name",
    mimeType: "application/vnd.google-apps.spreadsheet",
  },
  media: {
    mimeType: "text/csv",
    body: fs.createReadStream("/absolute/path/report.csv"),
  },
  fields: "id,name,mimeType,webViewLink,parents",
});

// Upload Markdown/text as a native Google Doc
await drive.files.create({
  requestBody: {
    name: "Doc Name",
    mimeType: "application/vnd.google-apps.document",
  },
  media: {
    mimeType: "text/markdown",
    body: fs.createReadStream("/absolute/path/doc.md"),
  },
  fields: "id,name,mimeType,webViewLink,parents",
});

// Search Drive files
await drive.files.list({
  q: "name contains 'ClaudeFluent' and trashed = false",
  fields: "files(id,name,mimeType,webViewLink,parents)",
  pageSize: 20,
});

// Trash a Drive file
await drive.files.update({
  fileId: "<file_id>",
  requestBody: { trashed: true },
  fields: "id,name,trashed",
});
```

## Legacy Implementation Reference

If the shared CLI is unavailable, the underlying service account setup is:

- Service account uses domain-wide delegation to impersonate user.com
- Key file: `~/.config/example-agency-email/service-account.json`
- Full Gmail scope: `https://mail.google.com/`
- Drive scope: `https://www.googleapis.com/auth/drive`

Prefer `gmail.js` for email work unless you are debugging the Denada integration itself. For Drive work, use the `googleapis` JWT pattern above.
