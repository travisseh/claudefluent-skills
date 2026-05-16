#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen

DB_ID = "3457bf03-b771-814f-944e-c15752949e46"
NOTION_VERSION = "2022-06-28"
NOTION_TOKEN_JS = Path("~/.config/notion-tools/notion-ai.js")
YOUTUBE_TRANSCRIPT_SCRIPT = Path(
    "~/.codex/skills/youtube-transcript/scripts/fetch_youtube_transcript.py"
)
EXCLUDED_PODCASTS = {"TBPN"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect recently synced podcast transcript rows with transcript fallback."
    )
    parser.add_argument("--hours", type=int, default=24, help="Lookback window in hours.")
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of recent rows to return.",
    )
    parser.add_argument(
        "--transcript-char-limit",
        type=int,
        default=16000,
        help="Max chars of transcript text to include per episode.",
    )
    return parser.parse_args()


def notion_token() -> str:
    text = NOTION_TOKEN_JS.read_text()
    match = re.search(r'NOTION_TOKEN\s*=\s*"([^"]+)"', text)
    if not match:
        raise RuntimeError(f"Could not find NOTION_TOKEN in {NOTION_TOKEN_JS}")
    return match.group(1)


def notion_api(method: str, path: str, body: dict | None = None) -> dict:
    request = Request(
        f"https://api.notion.com/v1{path}",
        method=method,
        headers={
            "Authorization": f"Bearer {notion_token()}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
        data=json.dumps(body).encode() if body is not None else None,
    )
    with urlopen(request, timeout=60) as response:
        raw = response.read()
    return json.loads(raw) if raw else {}


def extract_text(parts: list[dict] | None) -> str:
    return "".join((part.get("plain_text") or "") for part in (parts or []))


def prop_value(prop: dict | None):
    if not prop:
        return None
    kind = prop.get("type")
    if kind == "title":
        return extract_text(prop.get("title"))
    if kind == "select":
        return (prop.get("select") or {}).get("name")
    if kind == "date":
        return (prop.get("date") or {}).get("start")
    if kind == "url":
        return prop.get("url")
    if kind == "rich_text":
        return extract_text(prop.get("rich_text"))
    if kind == "checkbox":
        return bool(prop.get("checkbox"))
    return None


def list_recent_pages(hours: int, limit: int) -> list[dict]:
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    body = {
        "page_size": min(limit, 100),
        "filter": {"property": "Synced", "date": {"on_or_after": since}},
        "sorts": [{"property": "Synced", "direction": "descending"}],
    }
    data = notion_api("POST", f"/databases/{DB_ID}/query", body)
    pages = []
    for page in data.get("results", []):
        props = page.get("properties", {})
        pages.append(
            {
                "id": page["id"],
                "url": page.get("url"),
                "episode": prop_value(props.get("Episode")),
                "podcast": prop_value(props.get("Podcast")),
                "synced": prop_value(props.get("Synced")),
                "published": prop_value(props.get("Published")),
                "youtube_url": prop_value(props.get("YouTube URL")),
                "duration": prop_value(props.get("Duration")),
                "has_transcript": prop_value(props.get("Has Transcript")),
            }
        )
    return pages


def read_page_text(page_id: str) -> str:
    blocks = notion_api("GET", f"/blocks/{page_id}/children?page_size=100")
    lines: list[str] = []
    for block in blocks.get("results", []):
        block_type = block.get("type")
        block_data = block.get(block_type or "", {})
        rich_text = block_data.get("rich_text", [])
        text = extract_text(rich_text).strip()
        if text:
            lines.append(text)
    return "\n".join(lines).strip()


def youtube_transcript(youtube_url: str) -> str:
    result = subprocess.run(
        ["python3", str(YOUTUBE_TRANSCRIPT_SCRIPT), youtube_url],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> int:
    args = parse_args()
    pages = list_recent_pages(args.hours, args.limit)
    items = []
    for page in pages:
        if page.get("podcast") in EXCLUDED_PODCASTS:
            continue
        transcript = read_page_text(page["id"])
        source = "notion_page"
        if not transcript and page.get("youtube_url"):
            transcript = youtube_transcript(page["youtube_url"])
            source = "youtube_fallback"
        transcript = transcript[: args.transcript_char_limit].strip()
        items.append(
            {
                **page,
                "source": source,
                "transcript": transcript,
            }
        )

    payload = {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "hours": args.hours,
        "count": len(items),
        "items": items,
    }
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
