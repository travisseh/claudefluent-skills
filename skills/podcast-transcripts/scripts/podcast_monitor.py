#!/usr/bin/env python3
"""Monitor YouTube channels for new podcast episodes and store transcripts in Notion.

Runs daily. For each configured channel:
1. Fetch latest videos via yt-dlp --flat-playlist
2. Check Notion database for already-synced video IDs
3. For new episodes: create Notion row, fetch transcript, append as page content
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
from urllib.error import HTTPError
from urllib.request import Request, urlopen

REPO_ROOT = Path("/Users/you/Programming/personal-master/personal")
TRANSCRIPT_SCRIPT = Path("/Users/you/.codex/skills/youtube-transcript/scripts/fetch_youtube_transcript.py")
STATE_DIR = REPO_ROOT / ".claude/skills/podcast-transcripts/state"
DB_ID_FILE = STATE_DIR / "db_id.txt"

PARENT_PAGE_ID = "33c7bf03b77180609066e82319e28d7a"
NOTION_VERSION = "2022-06-28"
NOTION_TOKEN_JS = Path("/Users/you/.config/notion-tools/notion-ai.js")

CHANNELS = {
    "Lenny's Podcast": "https://www.youtube.com/@LennysPodcast/videos",
    "Limitless": "https://www.youtube.com/@Limitless-FT/videos",
    "TBPN": "https://www.youtube.com/@TBPNLive/videos",
    "My First Million": "https://www.youtube.com/@myfirstmillionpod/videos",
}

MAX_EPISODES_PER_CHANNEL = 5


# ---------- Secrets ----------


def notion_token() -> str:
    text = NOTION_TOKEN_JS.read_text()
    m = re.search(r'NOTION_TOKEN\s*=\s*"([^"]+)"', text)
    if not m:
        sys.exit(f"could not find NOTION_TOKEN in {NOTION_TOKEN_JS}")
    return m.group(1)


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
                time.sleep(2**attempt)
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


# ---------- Notion DB ----------


def create_database() -> str:
    props = {
        "Episode": {"title": {}},
        "Podcast": {
            "select": {"options": [{"name": name} for name in CHANNELS]}
        },
        "YouTube URL": {"url": {}},
        "Video ID": {"rich_text": {}},
        "Published": {"date": {}},
        "Synced": {"date": {}},
        "Duration": {"rich_text": {}},
        "Has Transcript": {"checkbox": {}},
    }
    payload = {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
        "title": [{"type": "text", "text": {"content": "Podcast Transcripts"}}],
        "properties": props,
    }
    resp = notion_api("POST", "/databases", payload)
    return resp["id"]


def ensure_database() -> str:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if DB_ID_FILE.exists():
        db_id = DB_ID_FILE.read_text().strip()
        try:
            notion_api("GET", f"/databases/{db_id}")
            return db_id
        except SystemExit:
            print(f"stored DB id {db_id} is invalid, recreating...", file=sys.stderr)
    print("creating new Notion database...", file=sys.stderr)
    db_id = create_database()
    DB_ID_FILE.write_text(db_id)
    print(f"created DB {db_id}", file=sys.stderr)
    return db_id


def fetch_existing_video_ids(db_id: str) -> set[str]:
    ids: set[str] = set()
    cursor = None
    while True:
        body: dict = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        resp = notion_api("POST", f"/databases/{db_id}/query", body)
        for row in resp.get("results", []):
            rt = row["properties"].get("Video ID", {}).get("rich_text", [])
            if rt:
                ids.add(rt[0]["plain_text"])
        if not resp.get("has_more"):
            break
        cursor = resp.get("next_cursor")
    return ids


# ---------- Notion page creation ----------


def format_duration(seconds: int | float | None) -> str:
    if not seconds:
        return ""
    total = int(seconds)
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def create_page(db_id: str, video: dict, podcast_name: str) -> str:
    video_id = video["id"]
    title = video.get("title", "Untitled")
    url = f"https://www.youtube.com/watch?v={video_id}"
    duration = format_duration(video.get("duration"))
    upload_date = video.get("upload_date")
    published = None
    if upload_date and len(upload_date) == 8:
        published = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
    synced = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def chunks(s: str, n: int = 1990) -> list[dict]:
        s = s or ""
        if not s:
            return [{"type": "text", "text": {"content": ""}}]
        return [
            {"type": "text", "text": {"content": s[i : i + n]}}
            for i in range(0, len(s), n)
        ]

    props: dict = {
        "Episode": {"title": chunks(title)},
        "Podcast": {"select": {"name": podcast_name}},
        "YouTube URL": {"url": url},
        "Video ID": {
            "rich_text": [{"type": "text", "text": {"content": video_id}}]
        },
        "Synced": {"date": {"start": synced}},
        "Duration": {
            "rich_text": [{"type": "text", "text": {"content": duration}}]
        },
        "Has Transcript": {"checkbox": False},
    }
    if published:
        props["Published"] = {"date": {"start": published}}

    resp = notion_api(
        "POST",
        "/pages",
        {"parent": {"database_id": db_id}, "properties": props},
    )
    return resp["id"]


def append_transcript(page_id: str, transcript_text: str):
    blocks: list[dict] = []
    current_chunk = ""

    for line in transcript_text.split("\n"):
        if len(current_chunk) + len(line) + 1 > 1900:
            if current_chunk:
                blocks.append(
                    {
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": current_chunk.strip()},
                                }
                            ]
                        },
                    }
                )
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"

    if current_chunk.strip():
        blocks.append(
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": current_chunk.strip()},
                        }
                    ]
                },
            }
        )

    for i in range(0, len(blocks), 100):
        batch = blocks[i : i + 100]
        notion_api("PATCH", f"/blocks/{page_id}/children", {"children": batch})
        if i + 100 < len(blocks):
            time.sleep(0.5)


def update_has_transcript(page_id: str, value: bool):
    notion_api(
        "PATCH",
        f"/pages/{page_id}",
        {"properties": {"Has Transcript": {"checkbox": value}}},
    )


# ---------- YouTube ----------


def fetch_latest_videos(channel_url: str, max_n: int) -> list[dict]:
    cmd = [
        "yt-dlp",
        "--no-update",
        "--flat-playlist",
        "--playlist-end",
        str(max_n),
        "--dump-json",
        "--no-warnings",
        channel_url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print(f"  yt-dlp error: {result.stderr[:200]}", file=sys.stderr)
        return []

    videos = []
    for line in result.stdout.strip().split("\n"):
        if line.strip():
            try:
                videos.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return videos


def fetch_transcript(video_id: str) -> str | None:
    cmd = [
        "python3",
        str(TRANSCRIPT_SCRIPT),
        video_id,
        "--format",
        "text",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        print(
            f"  transcript failed: {result.stderr[:200]}", file=sys.stderr
        )
    except subprocess.TimeoutExpired:
        print(f"  transcript timed out for {video_id}", file=sys.stderr)
    return None


# ---------- Main ----------


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--max", type=int, default=MAX_EPISODES_PER_CHANNEL)
    ap.add_argument("--channel", help="Only check this channel name")
    ap.add_argument(
        "--skip-transcript",
        action="store_true",
        help="Create rows but skip transcript fetch",
    )
    args = ap.parse_args()

    db_id = ensure_database()
    known = fetch_existing_video_ids(db_id)
    print(f"DB {db_id}: {len(known)} existing episodes", file=sys.stderr)

    channels = CHANNELS
    if args.channel:
        channels = {
            k: v
            for k, v in CHANNELS.items()
            if k.lower() == args.channel.lower()
        }
        if not channels:
            sys.exit(
                f"unknown channel: {args.channel}. Available: {', '.join(CHANNELS)}"
            )

    total_added = 0
    total_skipped = 0
    total_transcripts = 0

    for podcast_name, channel_url in channels.items():
        print(f"\n--- {podcast_name} ---", file=sys.stderr)
        videos = fetch_latest_videos(channel_url, args.max)
        print(f"  fetched {len(videos)} recent videos", file=sys.stderr)

        for video in videos:
            vid = video.get("id", "")
            title = video.get("title", "?")

            if vid in known:
                total_skipped += 1
                if args.verbose:
                    print(f"  skip (known): {title[:60]}", file=sys.stderr)
                continue

            print(f"  + {title[:70]}", file=sys.stderr)

            if args.dry_run:
                total_added += 1
                continue

            page_id = create_page(db_id, video, podcast_name)
            total_added += 1

            if not args.skip_transcript:
                print("    fetching transcript...", file=sys.stderr)
                transcript = fetch_transcript(vid)
                if transcript:
                    append_transcript(page_id, transcript)
                    update_has_transcript(page_id, True)
                    total_transcripts += 1
                    print(
                        f"    transcript stored ({len(transcript)} chars)",
                        file=sys.stderr,
                    )
                else:
                    print("    no transcript available", file=sys.stderr)

            known.add(vid)
            time.sleep(1)

    mode = "would add" if args.dry_run else "added"
    print(
        f"\ndone. {mode} {total_added}, skipped {total_skipped}, transcripts {total_transcripts}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
