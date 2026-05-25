---
name: notion-product-backlog
description: Create, read, and update pages in the Example Company Notion workspace. Use when the user asks to publish docs, PRDs, roadmaps, meeting notes, or any content to Example Company Notion — or to search/read existing Example Company pages. Separate from /notion-backlog (which is scoped to the personal Life Backlog DB).
---

# Notion Example Company Workspace

General-purpose Notion tool for the **Example Company workspace**. Unlike `/notion-backlog`, this is not tied to a database — it operates on arbitrary pages and hierarchies so you can create PRDs, docs, roadmaps, and nested child pages.

## Workspace

- **Workspace:** Example Company
- **Integration name:** Claude Code - the user
- **Bot user id:** `53dd4859-7446-4409-b95f-4646842f30b1`

**IMPORTANT — sharing requirement.** The integration only sees pages it has been explicitly connected to. If a `read`/`create`/`search` returns nothing or says "object not found", the page hasn't been shared yet: open it in Notion → `⋯` menu → **Connections** → add **Claude Code - the user**. Access inherits to children, so connecting at the highest allowed ancestor is best.

## CLI Tool

**Always use the CLI at `~/.config/notion-tools/notion-product-backlog.js`. Do NOT use the Notion MCP — it is unreliable for this workspace. Do NOT use the Life Backlog CLI (`notion.js`), which points at the personal workspace.**

```bash
node ~/.config/notion-tools/notion-product-backlog.js <command> [args]
```

## Commands

| Command | Purpose |
|---|---|
| `whoami` | Verify the integration token |
| `search "query" [page\|database]` | Find pages/databases the integration can see |
| `read <pageId>` | Read a page's content, properties, and URL |
| `children <pageId>` | List child pages/databases nested under a page |
| `create <parentPageId> "Title" [content\|@file\|-]` | Create a new child page under a parent |
| `append <pageId> <content\|@file\|->` | Append markdown to an existing page |
| `update <pageId> <content\|@file\|->` | Replace a page's body (child pages preserved) |
| `create-db <parentPageId> "Title" "cat1,cat2,cat3"` | Create an inline database on a page with a `Category` select property |
| `db-add <databaseId> "Entry title" "Category"` | Add a new row to a database created via `create-db` |

## the user AI Output database

Default dumping ground for AI-generated artifacts in Example Company Notion.

- **Parent page id:** `33bc831c-671e-8079-948d-c824b98f58d0`
- **Database id:** `33bc831c-671e-8137-a524-f62347485d71`
- **URL:** https://www.notion.so/33bc831c671e8137a524f62347485d71
- **Category options:** `research`, `prds`, `marketing`

When the user says "put this in the user AI Output" (or similar), use `db-add` against this database id and pick the appropriate category. Example:

```bash
node ~/.config/notion-tools/notion-product-backlog.js db-add 33bc831c671e8137a524f62347485d71 "Tapcards onboarding PRD" "prds"
```

The command returns the new page's id/url — then use `append` or `update` on that id to fill in the body content.

Content arguments accept three forms:
- Inline string: `"# Heading\n- bullet"`
- File reference: `@/tmp/draft.md`
- Stdin: `-` (pipe content in)

## Images (local files)

The markdown converter does NOT support images. To embed a local image (e.g., a matplotlib chart PNG) into a Notion page, use the dedicated image uploader — it uses Notion's native `/v1/file_uploads` endpoint, so no external hosting is required.

```bash
node ~/.config/notion-tools/notion-image-upload.js --workspace example-company <pageId> <filepath> "optional caption"
```

Always use this tool for images in Example Company pages. Do not reference local paths in markdown (they won't render) and do not try to embed base64 (Notion API rejects it). If the user asks for "charts/screenshots in Notion", generate the PNG (e.g., with matplotlib), then call this uploader for each file. The block is appended to the page in call order — interleave `append` (for text/tables) and `notion-image-upload.js` (for images) to control layout.

## Markdown Support

The converter handles: `#`/`##`/`###` headings, `-` / `*` bullets, `1.` numbered lists, `[ ]` / `[x]` todos, `> quote`, `---` divider, inline `**bold**`, `*italic*`, `` `code` ``, `[text](url)`, and **markdown tables** (first row = header, second row = `|---|---|` separator, remaining rows = body — rendered as native Notion table blocks). Fenced code blocks are stripped.

## Typical Workflows

### Creating a new doc in Example Company
1. `search "Parent Area Name"` to find where it belongs.
2. Copy the `id` of the target parent page.
3. `create <parentId> "New Doc Title" @/tmp/draft.md`
4. Share the returned URL with the user.

### Nesting pages (page within page within page)
Each `create` call returns an `id`. Pass that id as the parent for the next `create` to nest deeper. Example:
```bash
ROOT=$(node ~/.config/notion-tools/notion-product-backlog.js create <example-companyParentId> "Q2 Planning" @/tmp/overview.md | jq -r .id)
SUB=$(node ~/.config/notion-tools/notion-product-backlog.js create $ROOT "Workstream: Tapcards" @/tmp/tapcards.md | jq -r .id)
node ~/.config/notion-tools/notion-product-backlog.js create $SUB "Rollout Notes" @/tmp/rollout.md
```

### Updating an existing doc
Prefer `append` for adding new sections (non-destructive). Use `update` only when the user explicitly wants the body rewritten — it deletes existing non-child-page blocks.

### Drafting long content
Write the markdown to a temp file (`/tmp/<name>.md`) and pass with `@/tmp/<name>.md`. This avoids shell-escaping issues and handles >100-block content correctly (the CLI auto-chunks).

## Gotchas

- **Permission errors** = page not shared with the integration. Don't assume the token is broken — try `whoami` first, then check connections on the target page.
- **Search returns empty** = nothing has been shared yet, or the query is too narrow. Try broader terms, or ask the user which top-level page/teamspace to connect.
- **Don't confuse with `/notion-backlog`** — that skill writes to the user's personal Life Backlog database. This one writes to the Example Company workspace. Keep them separate.
- **Child pages are preserved on `update`** — the CLI skips `child_page` / `child_database` blocks when clearing body content, so nested docs aren't lost.
