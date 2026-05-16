#!/usr/bin/env python3
"""Query the X Bookmarks Notion database.

Filters: category (multi_select), author (rich_text), search (text in tweet body),
since/until (date), limit. Outputs markdown by default, JSON with --format json.

Examples:
  python3 query.py --category "Claude Code" --limit 20
  python3 query.py --author rahulvohra
  python3 query.py --search "prompt caching"
  python3 query.py --since 2026-04-01 --category "AI / Models"
  python3 query.py --format json --limit 5
"""
from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# macOS Python 3.13 ships without cert bundle; point to system certs
if not os.environ.get("SSL_CERT_FILE") and Path("/etc/ssl/cert.pem").exists():
    os.environ["SSL_CERT_FILE"] = "/etc/ssl/cert.pem"

REPO_ROOT = Path("~/Programming/personal-master/personal")
DB_ID_FILE = REPO_ROOT / ".claude/skills/x-bookmarks-to-notion/state/db_id.txt"
NOTION_TOKEN_JS = Path("~/.config/notion-tools/notion-ai.js")
NOTION_VERSION = "2022-06-28"

CATEGORIES = [
    "AI / Models",
    "AI Tools & Workflows",
    "Claude Code",
    "Design & UX",
    "Product & PM",
    "Marketing & Growth",
    "Business & Startups",
    "Engineering",
    "Writing & Content",
    "Personal / Reference",
    "Humor / Misc",
]


def notion_token() -> str:
    text = NOTION_TOKEN_JS.read_text()
    m = re.search(r'NOTION_TOKEN\s*=\s*"([^"]+)"', text)
    if not m:
        sys.exit(f"could not find NOTION_TOKEN in {NOTION_TOKEN_JS}")
    return m.group(1)


def db_id() -> str:
    if not DB_ID_FILE.exists():
        sys.exit(f"missing {DB_ID_FILE} — run sync.py once first")
    return DB_ID_FILE.read_text().strip()


def notion_query(body: dict) -> dict:
    url = f"https://api.notion.com/v1/databases/{db_id()}/query"
    req = Request(
        url,
        data=json.dumps(body).encode(),
        method="POST",
        headers={
            "Authorization": f"Bearer {notion_token()}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except HTTPError as e:
        sys.exit(f"Notion query failed: HTTP {e.code}: {e.read().decode(errors='replace')}")


def build_filter(args) -> dict | None:
    conds = []
    if args.category:
        for c in args.category:
            conds.append({"property": "Categories", "multi_select": {"contains": c}})
    if args.author:
        handle = args.author.lstrip("@")
        # Match with or without @ prefix since we store as "@handle"
        conds.append({"property": "Author", "rich_text": {"contains": handle}})
    if args.search:
        conds.append({"property": "Text", "title": {"contains": args.search}})
    if args.since:
        conds.append({"property": "Posted", "date": {"on_or_after": args.since}})
    if args.until:
        conds.append({"property": "Posted", "date": {"on_or_before": args.until}})

    if not conds:
        return None
    if len(conds) == 1:
        return conds[0]
    return {"and": conds}


def extract_row(row: dict) -> dict:
    p = row["properties"]
    def rt(prop):
        arr = p.get(prop, {}).get("rich_text") or []
        return "".join(x.get("plain_text", "") for x in arr)
    def title(prop):
        arr = p.get(prop, {}).get("title") or []
        return "".join(x.get("plain_text", "") for x in arr)
    def num(prop):
        return p.get(prop, {}).get("number") or 0
    def url(prop):
        return p.get(prop, {}).get("url")
    def date(prop):
        d = p.get(prop, {}).get("date")
        return d.get("start") if d else None
    def multi(prop):
        return [x["name"] for x in p.get(prop, {}).get("multi_select", [])]
    return {
        "text": title("Text"),
        "author": rt("Author"),
        "tweet_url": url("Tweet URL"),
        "external_link": url("External Link"),
        "posted": date("Posted"),
        "synced": date("Synced"),
        "likes": num("Likes"),
        "reposts": num("Reposts"),
        "replies": num("Replies"),
        "categories": multi("Categories"),
        "tweet_id": rt("Tweet ID"),
    }


def to_md(rows: list[dict]) -> str:
    if not rows:
        return "_No matches._"
    out = []
    for r in rows:
        cats = " · ".join(f"`{c}`" for c in r["categories"]) or "_uncategorized_"
        meta = f"♥ {r['likes']} · 🔁 {r['reposts']} · 💬 {r['replies']}"
        header = f"### {r['author']} — {r['posted'] or '?'}"
        body = r["text"].strip()
        url_line = f"[tweet]({r['tweet_url']})"
        if r["external_link"]:
            url_line += f" · [link]({r['external_link']})"
        out.append(f"{header}\n{body}\n\n{cats}\n{meta} · {url_line}")
    return "\n\n---\n\n".join(out)


def to_compact(rows: list[dict]) -> str:
    if not rows:
        return "(no matches)"
    lines = []
    for r in rows:
        snippet = re.sub(r"\s+", " ", r["text"]).strip()[:100]
        lines.append(f"{r['author']:20s} | {r['likes']:5d}♥ | {snippet}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Query X Bookmarks in Notion.")
    ap.add_argument("--category", "-c", action="append", help="filter by category (repeatable). Exact match.")
    ap.add_argument("--author", "-a", help="filter by author handle (with or without @)")
    ap.add_argument("--search", "-s", help="text contains (searches the tweet body)")
    ap.add_argument("--since", help="posted on/after YYYY-MM-DD")
    ap.add_argument("--until", help="posted on/before YYYY-MM-DD")
    ap.add_argument("--limit", "-n", type=int, default=25, help="max results (default 25, max 100 per Notion page)")
    ap.add_argument("--sort", choices=["posted", "synced", "likes"], default="posted", help="sort field")
    ap.add_argument("--asc", action="store_true", help="ascending order (default descending)")
    ap.add_argument("--format", choices=["md", "json", "compact"], default="md")
    ap.add_argument("--list-categories", action="store_true", help="print the fixed category taxonomy and exit")
    args = ap.parse_args()

    if args.list_categories:
        for c in CATEGORIES:
            print(c)
        return

    sort_prop = {"posted": "Posted", "synced": "Synced", "likes": "Likes"}[args.sort]
    body: dict = {
        "page_size": min(max(args.limit, 1), 100),
        "sorts": [{"property": sort_prop, "direction": "ascending" if args.asc else "descending"}],
    }
    filt = build_filter(args)
    if filt:
        body["filter"] = filt

    resp = notion_query(body)
    rows = [extract_row(r) for r in resp.get("results", [])]

    if args.format == "json":
        print(json.dumps(rows, indent=2))
    elif args.format == "compact":
        print(to_compact(rows))
    else:
        print(to_md(rows))

    if resp.get("has_more"):
        print(f"\n_...more results available. Re-run with --limit {args.limit + 25} or narrower filters._", file=sys.stderr)


if __name__ == "__main__":
    main()
