#!/usr/bin/env npx --yes tsx
import { google } from "googleapis";
import os from "node:os";
import path from "node:path";

type ModifyResult = {
  id: string;
  status: "archived" | "dry_run";
};

const googleAuth = require(path.join(os.homedir(), ".config", "google-tools", "auth"));

function usage(): never {
  console.error(
    [
      "Usage:",
      "  npx --yes tsx archive_messages.ts <account> <id1,id2,...> [--dry-run]",
      "",
      "Example:",
      "  npx --yes tsx archive_messages.ts example-workspace \"19e2796096d4c699,19e2655d0cb2a1d7\"",
    ].join("\n"),
  );
  process.exit(1);
}

function parseArgs() {
  const args = process.argv.slice(2);
  const dryRun = args.includes("--dry-run");
  const positional = args.filter((arg) => arg !== "--dry-run");

  const account = positional[0];
  const ids = (positional[1] || "")
    .split(",")
    .map((id) => id.trim())
    .filter(Boolean);

  if (!account || ids.length === 0) usage();

  return { account, ids, dryRun };
}

async function main() {
  const { account, ids, dryRun } = parseArgs();
  const auth = await googleAuth.getOAuthAuthClient(account);
  const gmail = google.gmail({ version: "v1", auth });
  const results: ModifyResult[] = [];

  for (const id of ids) {
    if (!dryRun) {
      await gmail.users.messages.modify({
        userId: "me",
        id,
        requestBody: { removeLabelIds: ["INBOX"] },
      });
    }
    results.push({ id, status: dryRun ? "dry_run" : "archived" });
  }

  console.log(
    JSON.stringify(
      {
        account,
        dryRun,
        archived: dryRun ? 0 : results.length,
        checked: results.length,
        ids: results.map((result) => result.id),
      },
      null,
      2,
    ),
  );
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
