#!/usr/bin/env python3
"""Sync X bookmarks to a Notion database with AI-tagged categories.

Runs incrementally: fetches newest bookmarks, stops on first one already in Notion.
First run creates the database under the configured parent page.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# ---------- Config ----------

REPO_ROOT = Path("~/Programming/personal-master/personal")
X_SCRIPT = REPO_ROOT / ".claude/skills/x-api/scripts/x.py"
STATE_DIR = REPO_ROOT / ".claude/skills/x-bookmarks-to-notion/state"
DB_ID_FILE = STATE_DIR / "db_id.txt"

PARENT_PAGE_ID = "33c7bf03b77180609066e82319e28d7a"
NOTION_VERSION = "2022-06-28"
NOTION_TOKEN_JS = Path("~/.config/notion-tools/notion-ai.js")
ANTHROPIC_ENV = REPO_ROOT / "marketing-brain-bot/.env"
MODEL = "claude-sonnet-4-6"

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

# ---------- Secrets loading ----------


def notion_token() -> str:
    text = NOTION_TOKEN_JS.read_text()
    m = re.search(r'NOTION_TOKEN\s*=\s*"([^"]+)"', text)
    if not m:
        sys.exit(f"could not find NOTION_TOKEN in {NOTION_TOKEN_JS}")
    return m.group(1)


def anthropic_key() -> str:
    if os.environ.get("ANTHROPIC_API_KEY"):
        return os.environ["ANTHROPIC_API_KEY"]
    if not ANTHROPIC_ENV.exists():
        sys.exit(f"missing {ANTHROPIC_ENV}")
    for line in ANTHROPIC_ENV.read_text().splitlines():
        line = line.strip()
        if line.startswith("ANTHROPIC_API_KEY"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("ANTHROPIC_API_KEY not found")


# ---------- HTTP helpers ----------


def http(method: str, url: str, headers: dict, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = Request(url, data=data, method=method, headers=headers)
    for attempt in range(3):
        try:
            with urlopen(req, timeout=60) as r:
                raw = r.read()
                return json.loads(raw) if raw else {}
        except HTTPError as e:
            err = e.read().decode(errors="replace")
            if e.code in (429, 502, 503) and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            sys.exit(f"{method} {url} -> HTTP {e.code}: {err}")
    return {}


def notion_api(method: str, path: str, body: dict | None = None) -> dict:
    return http(
        method,
        f"https://api.notion.com/v1{path}",
        headers={
            "Authorization": f"Bearer {notion_token()}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
        body=body,
    )


# ---------- Notion DB management ----------


def create_database() -> str:
    props = {
        "Text": {"title": {}},
        "Author": {"rich_text": {}},
        "Tweet URL": {"url": {}},
        "External Link": {"url": {}},
        "Posted": {"date": {}},
        "Synced": {"date": {}},
        "Likes": {"number": {}},
        "Reposts": {"number": {}},
        "Replies": {"number": {}},
        "Categories": {
            "multi_select": {"options": [{"name": c} for c in CATEGORIES]}
        },
        "Tweet ID": {"rich_text": {}},
    }
    payload = {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
        "title": [{"type": "text", "text": {"content": "X Bookmarks"}}],
        "properties": props,
    }
    resp = notion_api("POST", "/databases", payload)
    return resp["id"]


def ensure_database() -> str:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if DB_ID_FILE.exists():
        db_id = DB_ID_FILE.read_text().strip()
        # verify it still exists
        try:
            notion_api("GET", f"/databases/{db_id}")
            return db_id
        except SystemExit:
            print(f"stored DB id {db_id} is invalid, recreating...", file=sys.stderr)
    print("creating new Notion database under parent page...", file=sys.stderr)
    db_id = create_database()
    DB_ID_FILE.write_text(db_id)
    print(f"created DB {db_id}", file=sys.stderr)
    return db_id


def fetch_existing_tweet_ids(db_id: str) -> set[str]:
    ids: set[str] = set()
    cursor = None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        resp = notion_api("POST", f"/databases/{db_id}/query", body)
        for row in resp.get("results", []):
            rt = row["properties"].get("Tweet ID", {}).get("rich_text", [])
            if rt:
                ids.add(rt[0]["plain_text"])
        if not resp.get("has_more"):
            break
        cursor = resp.get("next_cursor")
    return ids


def create_row(db_id: str, tweet: dict, categories: list[str]):
    author = tweet.get("author", {}).get("username", "unknown")
    tweet_id = tweet["id"]
    text = tweet.get("text", "") or ""
    metrics = tweet.get("public_metrics", {})
    urls = (tweet.get("entities") or {}).get("urls") or []
    external = urls[0].get("expanded_url") or urls[0].get("url") if urls else None
    tweet_url = f"https://x.com/{author}/status/{tweet_id}"
    posted = tweet.get("created_at")
    synced = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # Notion title rich_text is capped per chunk at 2000 chars
    def chunks(s: str, n: int = 1990) -> list[dict]:
        s = s or ""
        if not s:
            return [{"type": "text", "text": {"content": ""}}]
        return [{"type": "text", "text": {"content": s[i : i + n]}} for i in range(0, len(s), n)]

    props = {
        "Text": {"title": chunks(text)},
        "Author": {"rich_text": [{"type": "text", "text": {"content": f"@{author}"}}]},
        "Tweet URL": {"url": tweet_url},
        "External Link": {"url": external},
        "Posted": {"date": {"start": posted} if posted else None},
        "Synced": {"date": {"start": synced}},
        "Likes": {"number": metrics.get("like_count", 0)},
        "Reposts": {"number": metrics.get("retweet_count", 0)},
        "Replies": {"number": metrics.get("reply_count", 0)},
        "Categories": {"multi_select": [{"name": c} for c in categories if c in CATEGORIES]},
        "Tweet ID": {"rich_text": [{"type": "text", "text": {"content": tweet_id}}]},
    }
    # strip None-valued date/url props (Notion rejects null for url/date when property exists)
    if props["External Link"]["url"] is None:
        del props["External Link"]
    if props["Posted"]["date"] is None:
        del props["Posted"]

    notion_api(
        "POST",
        "/pages",
        {"parent": {"database_id": db_id}, "properties": props},
    )


# ---------- Categorization ----------


def classify(tweet_text: str, author: str) -> list[str]:
    """Call Sonnet 4.6 to pick 1-3 categories from the taxonomy."""
    prompt = (
        "You are tagging an X/Twitter bookmark for later retrieval. "
        "Choose 1-3 categories from this exact list that best describe it:\n"
        + "\n".join(f"- {c}" for c in CATEGORIES)
        + f'\n\nTweet by @{author}:\n"""\n{tweet_text}\n"""\n\n'
        + "Respond with ONLY a JSON array of chosen category strings, e.g. [\"Claude Code\", \"AI Tools & Workflows\"]. "
        + "No prose, no markdown, no extra keys."
    )
    body = {
        "model": MODEL,
        "max_tokens": 120,
        "messages": [{"role": "user", "content": prompt}],
    }
    resp = http(
        "POST",
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": anthropic_key(),
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        body=body,
    )
    text = resp["content"][0]["text"].strip()
    # Strip code fences if Claude added them despite instructions
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text).strip()
    try:
        cats = json.loads(text)
    except json.JSONDecodeError:
        return ["Personal / Reference"]
    return [c for c in cats if isinstance(c, str) and c in CATEGORIES] or ["Personal / Reference"]


# ---------- X fetch ----------


def fetch_bookmarks(max_n: int) -> list[dict]:
    result = subprocess.run(
        ["python3", str(X_SCRIPT), "bookmarks", "--max", str(max_n)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.exit(f"x-api failed: {result.stderr}")
    payload = json.loads(result.stdout)
    users = {u["id"]: u for u in (payload.get("includes") or {}).get("users", [])}
    tweets = payload.get("data") or []
    for t in tweets:
        u = users.get(t.get("author_id"))
        if u:
            t["author"] = {"username": u["username"], "name": u.get("name")}
    return tweets


# ---------- Main ----------


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=100)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    db_id = ensure_database()
    known = fetch_existing_tweet_ids(db_id)
    print(f"DB {db_id}: {len(known)} existing bookmarks", file=sys.stderr)

    tweets = fetch_bookmarks(args.max)
    print(f"fetched {len(tweets)} bookmarks from X", file=sys.stderr)

    added = 0
    skipped = 0
    for t in tweets:
        if t["id"] in known:
            skipped += 1
            # Stop early: X returns newest-first, so first known means we're caught up
            print(f"hit known tweet {t['id']}, stopping", file=sys.stderr)
            break
        categories = classify(t.get("text", ""), t.get("author", {}).get("username", ""))
        if args.verbose or args.dry_run:
            print(f"  + @{t.get('author', {}).get('username')}: {categories} — {t.get('text','')[:80]}", file=sys.stderr)
        if not args.dry_run:
            create_row(db_id, t, categories)
        added += 1

    mode = "would add" if args.dry_run else "added"
    print(f"done. {mode} {added}, skipped {skipped} already-known", file=sys.stderr)


if __name__ == "__main__":
    main()
