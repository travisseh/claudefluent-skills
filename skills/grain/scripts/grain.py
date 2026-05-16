#!/usr/bin/env python3
"""Grain API CLI — query recordings, transcripts, summaries, and more."""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE_URL = "https://api.grain.com/_/public-api/v2"
API_VERSION = "2025-10-31"


def load_env():
    for env_path in [Path(__file__).resolve().parents[3] / ".env", Path.cwd() / ".env"]:
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, val = line.partition("=")
                    os.environ.setdefault(key.strip(), val.strip())
            break


def get_token():
    load_env()
    token = os.environ.get("GRAIN_PAT")
    if not token:
        token_file = os.path.expanduser("~/.grain-pat")
        if os.path.exists(token_file):
            with open(token_file) as f:
                token = f.read().strip()
    if not token:
        sys.exit("No Grain token found. Set GRAIN_PAT env var, add to .env, or save to ~/.grain-pat")
    return token


def api_request(method, path, body=None):
    token = get_token()
    url = f"{BASE_URL}{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Public-Api-Version": API_VERSION,
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode() if body else None
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=30) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else {}
    except HTTPError as e:
        body_text = e.read().decode()
        sys.exit(f"API error {e.code}: {body_text}")
    except URLError as e:
        sys.exit(f"Network error: {e.reason}")
    except (OSError, TimeoutError) as e:
        sys.exit(f"Connection error: {e}")


def cmd_list(args):
    body = {}
    filt = {}
    if args.after:
        filt["after_datetime"] = args.after
    if args.before:
        filt["before_datetime"] = args.before
    if args.search:
        filt["title_search"] = args.search
    if args.team:
        filt["team"] = args.team
    if args.meeting_type:
        filt["meeting_type"] = args.meeting_type
    if filt:
        body["filter"] = filt

    include = {}
    if args.summaries:
        include["ai_summary"] = True
    if args.action_items:
        include["ai_action_items"] = True
    if args.participants:
        include["participants"] = True
    if args.highlights:
        include["highlights"] = True
    if include:
        body["include"] = include
    if args.cursor:
        body["cursor"] = args.cursor

    result = api_request("POST", "/recordings", body or None)
    recordings = result.get("recordings", result) if isinstance(result, dict) else result

    if args.format == "md":
        print_recordings_md(result)
    else:
        print(json.dumps(result, indent=2))


def cmd_get(args):
    include = {}
    if args.summary:
        include["ai_summary"] = True
    if args.action_items:
        include["ai_action_items"] = True
    if args.participants:
        include["participants"] = True
    if args.highlights:
        include["highlights"] = True
    if args.notes:
        include["private_notes"] = True
    if args.calendar:
        include["calendar_event"] = True
    if args.sections:
        include["ai_template_sections"] = True

    body = {"include": include} if include else None
    result = api_request("POST", f"/recordings/{args.recording_id}", body)

    if args.format == "md":
        print_recording_detail_md(result)
    else:
        print(json.dumps(result, indent=2))


def cmd_transcript(args):
    fmt = args.transcript_format or "json"
    if fmt == "json":
        result = api_request("GET", f"/recordings/{args.recording_id}/transcript")
        if args.format == "md":
            print_transcript_md(result)
        else:
            print(json.dumps(result, indent=2))
    else:
        token = get_token()
        url = f"{BASE_URL}/recordings/{args.recording_id}/transcript.{fmt}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Public-Api-Version": API_VERSION,
        }
        req = Request(url, headers=headers, method="GET")
        try:
            with urlopen(req) as resp:
                print(resp.read().decode())
        except HTTPError as e:
            sys.exit(f"API error {e.code}: {e.read().decode()}")


def cmd_users(args):
    result = api_request("POST", "/users", None)
    if args.format == "md":
        for u in result if isinstance(result, list) else result.get("users", []):
            print(f"- **{u.get('name')}** ({u.get('email')}) — `{u.get('id')}`")
    else:
        print(json.dumps(result, indent=2))


def cmd_teams(args):
    result = api_request("POST", "/teams", None)
    if args.format == "md":
        for t in result if isinstance(result, list) else result.get("teams", []):
            print(f"- **{t.get('name')}** — `{t.get('id')}`")
    else:
        print(json.dumps(result, indent=2))


def cmd_meeting_types(args):
    result = api_request("POST", "/meeting_types", None)
    if args.format == "md":
        for mt in result if isinstance(result, list) else result.get("meeting_types", []):
            print(f"- **{mt.get('name')}** ({mt.get('scope')}) — `{mt.get('id')}`")
    else:
        print(json.dumps(result, indent=2))


def cmd_tag(args):
    if args.remove:
        api_request("DELETE", f"/recordings/{args.recording_id}/tags/{args.tag}")
        print(f"Removed tag '{args.tag}'")
    else:
        api_request("PUT", f"/recordings/{args.recording_id}/tags", {"tag": args.tag})
        print(f"Added tag '{args.tag}'")


def cmd_update(args):
    body = {}
    if args.title:
        body["title"] = args.title
    if not body:
        sys.exit("Nothing to update. Use --title.")
    api_request("PATCH", f"/recordings/{args.recording_id}", body)
    print("Updated.")


def cmd_upload(args):
    import mimetypes
    file_path = Path(args.file).resolve()
    if not file_path.exists():
        sys.exit(f"File not found: {file_path}")
    filename = args.filename or file_path.name
    result = api_request("POST", "/recordings/upload", {"filename": filename})
    upload_url = result.get("url")
    uuid = result.get("uuid")
    max_bytes = result.get("max_upload_bytes", 0)
    file_size = file_path.stat().st_size
    if max_bytes and file_size > max_bytes:
        sys.exit(f"File too large: {file_size} bytes (max {max_bytes})")
    content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
    with open(file_path, "rb") as f:
        file_data = f.read()
    req = Request(upload_url, data=file_data, method="PUT")
    req.add_header("Content-Type", content_type)
    try:
        with urlopen(req, timeout=300) as resp:
            pass
    except (HTTPError, URLError, OSError) as e:
        sys.exit(f"Upload failed: {e}")
    print(f"Uploaded '{filename}' — recording UUID: {uuid}")
    print("Grain will process the recording shortly.")


def cmd_share(args):
    if args.user:
        api_request("PUT", f"/recordings/{args.recording_id}/users", {"user_id": args.user})
        print(f"Shared with user {args.user}")
    elif args.team:
        api_request("PUT", f"/recordings/{args.recording_id}/teams/{args.team}", None)
        print(f"Shared with team {args.team}")
    else:
        sys.exit("Specify --user <user_id> or --team <team_id>")


def cmd_unshare(args):
    if args.user:
        api_request("DELETE", f"/recordings/{args.recording_id}/users/{args.user}")
        print(f"Unshared from user {args.user}")
    elif args.team:
        api_request("DELETE", f"/recordings/{args.recording_id}/teams/{args.team}")
        print(f"Unshared from team {args.team}")
    else:
        sys.exit("Specify --user <user_id> or --team <team_id>")


# --- Markdown formatters ---

def extract_text(field):
    if isinstance(field, str):
        return field
    if isinstance(field, dict):
        return field.get("text", str(field))
    return str(field)


def print_recordings_md(result):
    recordings = result.get("recordings", []) if isinstance(result, dict) else result
    cursor = result.get("cursor") if isinstance(result, dict) else None
    if not recordings:
        print("No recordings found.")
        return
    for r in recordings:
        title = r.get("title", "Untitled")
        rid = r.get("id", "")
        date = r.get("start_datetime", r.get("created_at", ""))[:10]
        duration_ms = r.get("duration_ms")
        duration_sec = r.get("duration_sec") or r.get("duration")
        mins = duration_ms // 60000 if duration_ms else (duration_sec // 60 if duration_sec else "?")
        print(f"### {title}")
        print(f"- **Date:** {date} | **Duration:** {mins} min | **ID:** `{rid}`")
        if r.get("ai_summary"):
            summary = extract_text(r["ai_summary"])
            first_line = summary.split("\n")[0][:200]
            print(f"- **Summary:** {first_line}")
        if r.get("ai_action_items"):
            items = r["ai_action_items"]
            if isinstance(items, dict):
                items = items.get("items", items.get("text", []))
            if isinstance(items, str):
                print(f"- **Action items:** {items[:200]}")
            elif isinstance(items, list):
                print("- **Action items:**")
                for item in items[:5]:
                    text = item if isinstance(item, str) else item.get("text", str(item))
                    print(f"  - {text}")
        if r.get("participants"):
            names = [p.get("name", p.get("email", "?")) for p in r["participants"]]
            print(f"- **Participants:** {', '.join(names)}")
        print()
    if cursor:
        print(f"---\n*More results available. Cursor:* `{cursor}`")


def print_recording_detail_md(r):
    title = r.get("title", "Untitled")
    rid = r.get("id", "")
    date = r.get("start_datetime", r.get("created_at", ""))[:10]
    duration = r.get("duration_sec") or r.get("duration")
    mins = duration // 60 if duration else "?"
    print(f"# {title}")
    print(f"**Date:** {date} | **Duration:** {mins} min | **ID:** `{rid}`")
    if r.get("participants"):
        names = [p.get("name", p.get("email", "?")) for p in r["participants"]]
        print(f"\n**Participants:** {', '.join(names)}")
    if r.get("ai_summary"):
        print(f"\n## Summary\n{extract_text(r['ai_summary'])}")
    if r.get("ai_action_items"):
        print("\n## Action Items")
        items = r["ai_action_items"]
        if isinstance(items, dict):
            items = items.get("items", [extract_text(items)])
        if isinstance(items, str):
            print(items)
        elif isinstance(items, list):
            for item in items:
                text = item if isinstance(item, str) else item.get("text", str(item))
                print(f"- {text}")
    if r.get("highlights"):
        print("\n## Highlights")
        for h in r["highlights"][:10]:
            text = h.get("text", h.get("title", str(h)))
            print(f"- {text}")
    if r.get("ai_template_sections"):
        print("\n## Meeting Notes")
        sections = r["ai_template_sections"]
        if isinstance(sections, dict):
            sections = sections.get("sections", [sections])
        for sec in sections:
            if isinstance(sec, dict):
                print(f"\n### {sec.get('title', 'Section')}")
                print(extract_text(sec.get("content", "")))
            else:
                print(str(sec))
    if r.get("private_notes"):
        print(f"\n## Private Notes\n{extract_text(r['private_notes'])}")


def print_transcript_md(segments):
    if isinstance(segments, dict):
        segments = segments.get("transcript", segments.get("segments", []))
    for seg in segments:
        speaker = seg.get("speaker", "Unknown")
        text = seg.get("text", "")
        ts = seg.get("start", seg.get("start_time", seg.get("timestamp", "")))
        print(f"**{speaker}** [{ts}]: {text}")


def main():
    parser = argparse.ArgumentParser(description="Grain API CLI")
    parser.add_argument("--format", choices=["json", "md"], default="json",
                        help="Output format (default: json)")
    sub = parser.add_subparsers(dest="command")

    # list recordings
    p_list = sub.add_parser("list", help="List/search recordings")
    p_list.add_argument("--after", help="Filter: after datetime (ISO 8601)")
    p_list.add_argument("--before", help="Filter: before datetime (ISO 8601)")
    p_list.add_argument("--search", help="Filter: title search")
    p_list.add_argument("--team", help="Filter: team ID")
    p_list.add_argument("--meeting-type", help="Filter: meeting type ID")
    p_list.add_argument("--summaries", action="store_true", help="Include AI summaries")
    p_list.add_argument("--action-items", action="store_true", help="Include AI action items")
    p_list.add_argument("--participants", action="store_true", help="Include participants")
    p_list.add_argument("--highlights", action="store_true", help="Include highlights")
    p_list.add_argument("--cursor", help="Pagination cursor")
    p_list.set_defaults(func=cmd_list)

    # get recording
    p_get = sub.add_parser("get", help="Get a single recording with details")
    p_get.add_argument("recording_id", help="Recording ID")
    p_get.add_argument("--summary", action="store_true", help="Include AI summary")
    p_get.add_argument("--action-items", action="store_true", help="Include action items")
    p_get.add_argument("--participants", action="store_true", help="Include participants")
    p_get.add_argument("--highlights", action="store_true", help="Include highlights")
    p_get.add_argument("--notes", action="store_true", help="Include private notes")
    p_get.add_argument("--calendar", action="store_true", help="Include calendar event")
    p_get.add_argument("--sections", action="store_true", help="Include AI template sections")
    p_get.set_defaults(func=cmd_get)

    # transcript
    p_tx = sub.add_parser("transcript", help="Get recording transcript")
    p_tx.add_argument("recording_id", help="Recording ID")
    p_tx.add_argument("--transcript-format", choices=["json", "txt", "vtt", "srt"],
                      default="json", help="Transcript format")
    p_tx.set_defaults(func=cmd_transcript)

    # users
    p_users = sub.add_parser("users", help="List workspace users")
    p_users.set_defaults(func=cmd_users)

    # teams
    p_teams = sub.add_parser("teams", help="List workspace teams")
    p_teams.set_defaults(func=cmd_teams)

    # meeting types
    p_mt = sub.add_parser("meeting-types", help="List meeting types")
    p_mt.set_defaults(func=cmd_meeting_types)

    # tag
    p_tag = sub.add_parser("tag", help="Add or remove a tag from a recording")
    p_tag.add_argument("recording_id", help="Recording ID")
    p_tag.add_argument("tag", help="Tag name (alphanumeric + dashes)")
    p_tag.add_argument("--remove", action="store_true", help="Remove the tag")
    p_tag.set_defaults(func=cmd_tag)

    # update
    p_upd = sub.add_parser("update", help="Update a recording")
    p_upd.add_argument("recording_id", help="Recording ID")
    p_upd.add_argument("--title", help="New title")
    p_upd.set_defaults(func=cmd_update)

    # upload
    p_upload = sub.add_parser("upload", help="Upload a recording file")
    p_upload.add_argument("file", help="Path to audio/video file")
    p_upload.add_argument("--filename", help="Override filename sent to Grain")
    p_upload.set_defaults(func=cmd_upload)

    # share
    p_share = sub.add_parser("share", help="Share a recording with a user or team")
    p_share.add_argument("recording_id", help="Recording ID")
    p_share.add_argument("--user", help="User ID to share with")
    p_share.add_argument("--team", help="Team ID to share with")
    p_share.set_defaults(func=cmd_share)

    # unshare
    p_unshare = sub.add_parser("unshare", help="Unshare a recording from a user or team")
    p_unshare.add_argument("recording_id", help="Recording ID")
    p_unshare.add_argument("--user", help="User ID to unshare from")
    p_unshare.add_argument("--team", help="Team ID to unshare from")
    p_unshare.set_defaults(func=cmd_unshare)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
