---
name: taxes
description: Help the user get behind-tax filings unstuck, especially 2024-style tax prep using Google Drive folders, rental spreadsheets, Avail exports, Copilot Money transaction exports, Gmail with Cody Gamboa, Apple Notes, and rental P&L cleanup.
---

# Taxes

Use this when the user asks for help getting taxes done, finding missing tax docs, cleaning rental P&Ls, reviewing Cody Gamboa context, checking Drive tax folders, Avail history, Copilot Money, or figuring out what is left for a tax year.

Use `$g-workspaces` for Google account work. Prefer local CLIs/tools over Google app connectors when account correctness matters.

## Core Sources

Default account: `personal` / `userh@gmail.com`.

Known 2024 sources:

- Tax Drive folder: `https://drive.google.com/drive/u/0/folders/1_nOQBbXCzvf8C2Yfb04nslIREd0BUyV6`
- Done folder: `https://drive.google.com/drive/folders/1S3VpWF0KV4zrspjVvCLwp7_F_dZFEonn`
- Rental workbook: `https://docs.google.com/spreadsheets/d/1Cn3TIqNWyNOTYuwAZaLgK-5lZeSIimER2qo3ZiagGnI/edit`
- Credential/source page: `https://www.notion.so/example-workspace/Running-My-Life-213bf517cb774d859a84c2cd08a89b9a`
- Apple Note: local note title `TAXES 2024`, note id observed as `7853`
- Avail archive folder: `Avail History Download`
- Avail archive files observed:
  - `avail-units-all.json`
  - `avail-leases-all.json`
  - `avail-charges-all.json`
- Cody Gamboa:
  - Gmail: `c.gamboacpa@gmail.com`
  - iMessage contact: Cody Gamboa / `+12082067451`

## Credential Source

Do not store raw usernames/passwords in this skill. When tax work requires portal access, use `$notion-backlog` and read the Notion page `Running My Life` at `213bf517cb774d859a84c2cd08a89b9a`.

That page has observed access details for tax-relevant systems including mortgage portals, Lehi/Provo utilities, Dominion/Questar, Xfinity, HOA portals, HSA/HealthEquity, Chase, property-tax parcel IDs, Provo house Gmail, and related finance/admin systems.

## First Pass Workflow

1. Inventory the Drive folder and `Done`.
2. Read/search the Apple Note for the current checklist.
3. Search Gmail and iMessage for Cody context.
4. Export any Google Sheets to local XLSX before analysis.
5. Compare the sheet summaries against source tabs and exported data.
6. Report only actionable missing items, separated from harmless messy rows.

Useful commands:

```bash
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js list personal 1_nOQBbXCzvf8C2Yfb04nslIREd0BUyV6 100
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js list personal 1S3VpWF0KV4zrspjVvCLwp7_F_dZFEonn 200
python3 ~/.claude/tools/apple-notes.py search "tax"
python3 ~/.claude/tools/apple-notes.py read 7853
node ~/.config/gmail-tools/gmail.js search personal "from:c.gamboacpa@gmail.com OR from:link@intuit.com after:2025/01/01" 20
node ~/.config/imessage-tools/imessage.js messages "+12082067451" 80
```

## Exporting Google Sheets

The local Google OAuth project may not have Sheets API enabled. If Sheets API fails, use Drive export with Google APIs instead.

```js
const fs = require("fs");
const path = require("path");
const os = require("os");
const { google } = require(path.join(os.homedir(), ".config", "gmail-tools", "node_modules", "googleapis"));
const auth = require(path.join(os.homedir(), ".config", "google-tools", "auth"));

const client = await auth.getOAuthAuthClient("personal");
const drive = google.drive({ version: "v3", auth: client });
const res = await drive.files.export(
  { fileId: "1Cn3TIqNWyNOTYuwAZaLgK-5lZeSIimER2qo3ZiagGnI", mimeType: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" },
  { responseType: "stream" }
);
```

Use bundled Python `openpyxl` when available:

```bash
~/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
```

## 2024 Rental Workbook Notes

Relevant tabs observed:

- `Provo 2024`
- `Lehi 2024`
- `Provo-Avail`
- `USAA Transactions (Lehi)`
- `Wells Fargo (Provo) Transaction`

Ignore old/noisy tabs unless needed:

- `Lehi ` is a 2023-ish old tab.
- `Provo Pricing (Ignore for Taxes` is not tax input.

Known cleaned 2024 summary state after the May 2026 cleanup:

- Provo gross income: `$39,720`
- Provo total expenses: `$31,266.55`
- Provo net income: `$8,453.45`
- Provo deposits collected through Avail in 2024: `$465`
- Lehi gross income: `$21,365`
- Lehi total expenses: `$22,072.16`
- Lehi net income: `-$707.16`
- Lehi deposit remains unverified.

Formula pattern used:

- Provo `F2`: `=C5`
- Provo `J2`: `=SUM(C8:N16)+O31+D44+D45`
- Provo `N2`: `=C5-J2`
- Lehi `C18`: `=SUM(C8:N17)`
- Lehi `J2`: `=C18`
- Lehi `N2`: `=C5-J2`

Always make a Drive backup before replacing a Google Sheet via XLSX upload.

## Avail Deposit Workflow

Search Drive:

```bash
node ~/Programming/personal-master/personal/.agents/skills/drive/scripts/drive.js search personal "name contains 'Avail' and trashed = false" 50
```

Download `avail-units-all.json`, `avail-leases-all.json`, and `avail-charges-all.json` with Drive `files.get alt=media`.

For deposits, prefer paid charge records over lease-stated deposit totals. In 2024, the Provo export showed paid security deposit charges:

- `2024-05-01`, Upstairs West Room, `$10`, paid
- `2024-05-01`, Upstairs Middle Room, `$10`, paid
- `2024-05-01`, Downstairs Middle, `$5`, paid
- `2024-07-01`, Downstairs West, `$440`, paid

Total Provo deposits collected in Avail during 2024: `$465`.

Important gotcha: `Lehi`, `4203`, and `1630` can appear in Avail lease JSON as `landlord.address1` / `landlord.city`. That does not mean the Lehi property is in the export. Check `unit.building.address1`, `unit.full_address`, and charge `street_address`. The observed archive only had Provo units/charges.

## Copilot Money Workflow

Use browser login if needed. Copilot may send a Gmail sign-in link to `userh@gmail.com`; read with the local Gmail CLI and navigate to the auth link.

Once logged in:

1. Open Transactions.
2. Use the download button to export CSV.
3. Parse `~/Downloads/transactions*.csv`.
4. Filter the relevant tax year and scan for rental keywords.

Useful filters:

- Names/categories: `lehi`, `provo`, `house`, `home`, `mortgage`, `roundpoint`, `uwm`, `provo city`, `lehi city`, `dominion`, `questar`, `enbridge`, `xfinity`, `wasatch`, `hoa`, `exchange`, `pioneer`, `avail`, `rent`, `deposit`, `cleaning`, `repair`, `restoration`, `mint`, `carpet`, `diego`, `handyman`, `furnace`, `finco`, `home depot`, `lowe`, `zumper`, `rentler`, `property`, `utility`, `utilities`.
- Exclude obvious St. George when focused on Provo/Lehi: `Red Rock`, `Dixie Power`, `City Of St George`, `Centurylink`, `Quantum`.

Known Copilot review findings from 2024:

- Diego Macdonald cleaning Oct-Dec: `$1,169`
- Helen Jessop cleaning Jan-Sep: `$1,480`
- Wasatch Broadband Sep-Dec actuals: `$242`
- Possible September house/move expenses from U-Haul / Geometry / Zurchers: `$1,236.22`
- Possible Sep-Dec Target house-improvement items: `$389.29`

Do not blindly add these. Determine whether they are already included in `Venmo`, `Repairs`, `House Improvement`, or personal/move/new-home spend.

## Interpretation Rules

- Refundable security deposits are usually not rental income unless retained or applied to rent/damages. Show them separately for Cody rather than mixing into rent unless he asks.
- If a transaction is a transfer, do not count it as expense/income without confirming the counterparty.
- If a row is visually messy but the top summary is correct, say that. Do not create work just to make the sheet pretty unless the user asks.
- Separate “missing actuals” from “needs Cody judgment.”

## Communication

the user is overwhelmed by this work. Keep summaries short and concrete:

- What is done.
- What is still missing.
- What evidence supports each number.
- The next 1-3 actions.

When materially advancing the task, ask once: `Do you want me to update the Life Backlog task in Notion?`
