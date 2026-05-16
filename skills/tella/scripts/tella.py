#!/usr/bin/env python3
"""Tella API CLI — list videos, get details, pull transcripts and chapters."""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE_URL = "https://api.tella.com/v1"


def load_env():
    """Walk up from script and CWD looking for an .env that defines TELLA_API_KEY."""
    seen = set()
    starts = [Path(__file__).resolve().parent, Path.cwd().resolve()]
    for start in starts:
        for parent in [start, *start.parents]:
            env_path = parent / ".env"
            if env_path in seen:
                continue
            seen.add(env_path)
            if env_path.exists():
                for line in env_path.read_text().splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, val = line.partition("=")
                        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))
                if os.environ.get("TELLA_API_KEY"):
                    return


def get_token():
    load_env()
    token = os.environ.get("TELLA_API_KEY")
    if not token:
        sys.exit("No Tella API key. Set TELLA_API_KEY in .env (workspace root).")
    return token


def api_request(method, path, params=None, body=None):
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urlencode({k: v for k, v in params.items() if v is not None})
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode() if body else None
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=60) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else {}
    except HTTPError as e:
        sys.exit(f"Tella API error {e.code}: {e.read().decode()}")
    except URLError as e:
        sys.exit(f"Network error: {e.reason}")


# ----- Helpers -----

VIDEO_ID_RE = re.compile(r"vid_[a-z0-9]+")


def resolve_video_id(value):
    """Accept a vid_..., a tella.tv URL, or a slug suffix; return the canonical id."""
    if not value:
        return value
    m = VIDEO_ID_RE.search(value)
    if m:
        return m.group(0)
    # tella.tv slug like 'become-an-ai-builder-ai-stack-2blf' — last hyphen segment is suffix
    suffix = value.rsplit("/", 1)[-1].split("?")[0].rstrip("/")
    if "-" in suffix:
        suffix = suffix.rsplit("-", 1)[-1]
    if suffix and len(suffix) >= 4:
        # Need to look it up via list — but cheaper to ask user to provide the ID directly.
        # Fall back to scanning the first few pages.
        cursor = None
        for _ in range(5):
            params = {"limit": 100}
            if cursor:
                params["cursor"] = cursor
            page = api_request("GET", "/videos", params=params)
            for v in page.get("videos", []):
                if v["id"].endswith(suffix):
                    return v["id"]
            pag = page.get("pagination", {})
            if not pag.get("hasMore"):
                break
            cursor = pag.get("nextCursor")
    return value


# ----- Commands -----

def cmd_list(args):
    params = {"limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    if args.playlist:
        params["playlistId"] = args.playlist
    data = api_request("GET", "/videos", params=params)
    videos = data.get("videos", [])
    if args.search:
        q = args.search.lower()
        videos = [v for v in videos if q in v.get("name", "").lower() or q in v.get("description", "").lower()]
    if args.format == "json":
        print(json.dumps({"videos": videos, "pagination": data.get("pagination", {})}, indent=2))
        return
    for v in videos:
        print(f"{v['id']}  {v.get('name', '')}")
        if v.get("description") and args.format == "md":
            print(f"  {v['description']}")
            print(f"  {v['links']['viewPage']}")
            print(f"  views: {v.get('views', 0)}  created: {v.get('createdAt', '')[:10]}")
            print()
    if data.get("pagination", {}).get("hasMore"):
        print(f"\n# more available: --cursor {data['pagination']['nextCursor']}", file=sys.stderr)


def cmd_get(args):
    vid = resolve_video_id(args.id)
    data = api_request("GET", f"/videos/{vid}")
    if args.format == "json":
        print(json.dumps(data, indent=2))
        return
    v = data.get("video", data)
    print(f"# {v.get('name', vid)}")
    if v.get("description"):
        print(f"\n{v['description']}\n")
    for k in ("id", "createdAt", "updatedAt", "views", "aspectRatio"):
        if v.get(k):
            print(f"- **{k}:** {v[k]}")
    if v.get("links"):
        print(f"- **viewPage:** {v['links'].get('viewPage', '')}")
    chapters = v.get("chapters") or []
    if chapters:
        print("\n## Chapters")
        for c in chapters:
            ts = c.get("startSeconds", 0)
            mm, ss = divmod(int(ts), 60)
            print(f"- {mm:02d}:{ss:02d}  {c.get('title', c.get('name', ''))}")
    t = v.get("transcript") or {}
    if t:
        print(f"\n## Transcript ({t.get('status', 'unknown')}, {t.get('language', '')})")
        if t.get("text"):
            print()
            print(t["text"])


def cmd_transcript(args):
    vid = resolve_video_id(args.id)
    data = api_request("GET", f"/videos/{vid}")
    v = data.get("video", data)
    t = v.get("transcript") or {}
    if not t or t.get("status") != "ready":
        sys.exit(f"Transcript not ready (status: {t.get('status', 'missing')})")
    if args.format == "json":
        print(json.dumps(t, indent=2))
        return
    if args.format == "vtt":
        print("WEBVTT\n")
        for s in t.get("sentences") or []:
            start = s.get("startSeconds", 0)
            end = s.get("endSeconds", start + 2)
            print(f"{_secs(start)} --> {_secs(end)}\n{s.get('text', '')}\n")
        return
    if args.timestamps:
        for s in t.get("sentences") or []:
            mm, ss = divmod(int(s.get("startSeconds", 0)), 60)
            print(f"[{mm:02d}:{ss:02d}] {s.get('text', '')}")
        return
    # Plain text fallback
    if t.get("text"):
        print(t["text"])
    else:
        for s in t.get("sentences") or []:
            print(s.get("text", ""))


def _secs(s):
    h, rem = divmod(int(s), 3600)
    m, sec = divmod(rem, 60)
    ms = int((s - int(s)) * 1000)
    return f"{h:02d}:{m:02d}:{sec:02d}.{ms:03d}"


def cmd_chapters(args):
    vid = resolve_video_id(args.id)
    data = api_request("GET", f"/videos/{vid}")
    v = data.get("video", data)
    chapters = v.get("chapters") or []
    if args.format == "json":
        print(json.dumps(chapters, indent=2))
        return
    for c in chapters:
        ts = c.get("startSeconds", 0)
        mm, ss = divmod(int(ts), 60)
        print(f"{mm:02d}:{ss:02d}  {c.get('title', c.get('name', ''))}")


def cmd_playlists(args):
    data = api_request("GET", "/playlists", params={"limit": args.limit})
    if args.format == "json":
        print(json.dumps(data, indent=2))
        return
    for p in data.get("playlists", []):
        print(f"{p.get('id', '')}  {p.get('name', '')}")


def main():
    ap = argparse.ArgumentParser(description="Tella API CLI")
    ap.add_argument("--format", choices=["txt", "md", "json", "vtt"], default="md")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="List videos")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--cursor")
    p.add_argument("--playlist")
    p.add_argument("--search", help="Substring filter on name or description")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("get", help="Get a video (incl. transcript + chapters)")
    p.add_argument("id", help="vid_..., tella.tv URL, or slug")
    p.set_defaults(func=cmd_get)

    p = sub.add_parser("transcript", help="Pull just the transcript")
    p.add_argument("id")
    p.add_argument("--timestamps", action="store_true", help="Per-sentence timestamps")
    p.set_defaults(func=cmd_transcript)

    p = sub.add_parser("chapters", help="List chapters")
    p.add_argument("id")
    p.set_defaults(func=cmd_chapters)

    p = sub.add_parser("playlists", help="List playlists")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_playlists)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
