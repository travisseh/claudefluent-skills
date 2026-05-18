#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

AE_REST_BASE = "https://app.askelephant.ai/api/v2"
AE_GRAPHQL_URL = "https://app.askelephant.ai/graphql"
DEFAULT_PERSON = "user.com"
DEFAULT_WORKSPACE_ID = "wrks_01JNKRAD8B3QJVT7CZPPPNMTRZ"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def load_default_env() -> None:
    for path in [
        Path.cwd() / ".env",
        Path.cwd() / ".env.local",
        Path("/Users/you/Programming/boostly-reporting/apps/dashboard/.env.local"),
        Path("/Users/you/.config/render/product-analytics.env"),
    ]:
        load_env_file(path)


def parse_date_range(args: argparse.Namespace) -> tuple[dt.datetime, dt.datetime]:
    now = dt.datetime.now(dt.timezone.utc)
    local_tz = dt.datetime.now().astimezone().tzinfo

    if args.date:
        if args.date == "yesterday":
            local_day = dt.datetime.now(local_tz).date() - dt.timedelta(days=1)
        elif args.date == "today":
            local_day = dt.datetime.now(local_tz).date()
        else:
            local_day = dt.date.fromisoformat(args.date)
        start_local = dt.datetime.combine(local_day, dt.time.min, tzinfo=local_tz)
        end_local = start_local + dt.timedelta(days=1)
        return start_local.astimezone(dt.timezone.utc), end_local.astimezone(dt.timezone.utc)

    if args.since:
        start = dt.datetime.fromisoformat(args.since)
        if start.tzinfo is None:
            start = start.replace(tzinfo=local_tz)
        start = start.astimezone(dt.timezone.utc)
    else:
        start = now - dt.timedelta(days=args.days)

    if args.until:
        end = dt.datetime.fromisoformat(args.until)
        if end.tzinfo is None:
            end = end.replace(tzinfo=local_tz)
        end = end.astimezone(dt.timezone.utc)
    else:
        end = now

    return start, end


def request_json(url: str, headers: dict[str, str], data: dict | None = None) -> dict:
    body = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "accept": "application/json",
            **({"content-type": "application/json"} if data is not None else {}),
            **headers,
        },
        method="POST" if data is not None else "GET",
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode())


def firebase_id_token() -> str | None:
    refresh_token = os.getenv("ASKELEPHANT_REFRESH_TOKEN")
    api_key = os.getenv("ASKELEPHANT_FIREBASE_API_KEY")
    if not refresh_token or not api_key:
        return None
    url = f"https://securetoken.googleapis.com/v1/token?key={urllib.parse.quote(api_key)}"
    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"content-type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        payload = json.loads(response.read().decode())
    return payload.get("id_token")


def rest_headers() -> dict[str, str] | None:
    api_key = os.getenv("ASKELEPHANT_API_KEY")
    if api_key:
        return {"authorization": api_key}
    return None


def fetch_rest_engagements(start: dt.datetime, end: dt.datetime, limit: int) -> list[dict]:
    headers = rest_headers()
    if not headers:
        return []

    engagements: list[dict] = []
    cursor = None
    while len(engagements) < limit:
        params = urllib.parse.urlencode({
            "limit": min(100, limit - len(engagements)),
            "expand": "tags,companies,contacts,owner,transcript",
            "order_by": "start_at:desc",
            "filter[start_at][gte]": start.isoformat().replace("+00:00", "Z"),
            "filter[start_at][lte]": end.isoformat().replace("+00:00", "Z"),
            **({"cursor": cursor} if cursor else {}),
        })
        page = request_json(f"{AE_REST_BASE}/engagements?{params}", headers)
        engagements.extend(page.get("data") or [])
        cursor = page.get("next_cursor")
        if not page.get("has_more") or not cursor:
            break
    return engagements


def fetch_graphql_engagements(start: dt.datetime, end: dt.datetime, limit: int) -> list[dict]:
    token = firebase_id_token()
    if not token:
        return []

    query = """
    query SkillSearchEngagements($first: Int!, $after: String, $filter: EngagementFilter, $sort: [EngagementSort!]) {
      viewer {
        currentWorkspace {
          engagements(first: $first, after: $after, filter: $filter, sort: $sort) {
            edges {
              cursor
              node {
                id
                title
                startAt
                endAt
                duration
                isRecorded
                hasTranscript
                transcriptText
                tags { id name }
                companies { id displayName primaryDomain }
                allParticipants {
                  edges {
                    node { id __typename displayName primaryEmail isUser }
                  }
                }
              }
            }
            pageInfo { hasNextPage endCursor }
          }
        }
      }
    }
    """
    variables = {
        "first": min(100, limit),
        "after": None,
        "filter": {
            "isRecorded": True,
            "startAt": start.isoformat().replace("+00:00", "Z"),
        },
        "sort": ["DATE_DESC"],
    }
    headers = {"authorization": f"Bearer {token}"}
    engagements: list[dict] = []
    while len(engagements) < limit:
        variables["first"] = min(100, limit - len(engagements))
        payload = request_json(AE_GRAPHQL_URL, headers, {"query": query, "variables": variables})
        if payload.get("errors"):
            raise RuntimeError(json.dumps(payload["errors"]))
        connection = payload["data"]["viewer"]["currentWorkspace"]["engagements"]
        for edge in connection.get("edges") or []:
            node = edge["node"]
            normalized = normalize_graphql_engagement(node)
            started = parse_iso(normalized.get("start_at"))
            if started and started < start:
                return engagements
            if started and started <= end:
                engagements.append(normalized)
        page_info = connection.get("pageInfo") or {}
        if not page_info.get("hasNextPage"):
            break
        variables["after"] = page_info.get("endCursor")
    return engagements


def normalize_graphql_engagement(node: dict) -> dict:
    participants = [
        edge.get("node") for edge in ((node.get("allParticipants") or {}).get("edges") or [])
        if isinstance(edge, dict) and isinstance(edge.get("node"), dict)
    ]
    return {
        "id": node.get("id"),
        "title": node.get("title"),
        "start_at": node.get("startAt"),
        "end_at": node.get("endAt"),
        "duration_seconds": parse_duration_seconds(node.get("duration")),
        "owner": None,
        "host": None,
        "tags": node.get("tags") or [],
        "companies": [
            {
                "id": company.get("id"),
                "name": company.get("displayName"),
                "domains": [company.get("primaryDomain")] if company.get("primaryDomain") else [],
            }
            for company in (node.get("companies") or [])
            if isinstance(company, dict)
        ],
        "contacts": node.get("contacts") or [],
        "participants": participants,
        "transcript": node.get("transcriptText"),
    }


def parse_iso(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def parse_duration_seconds(value: str | None) -> int | None:
    if not value:
        return None
    total = 0
    for amount, unit in re.findall(r"(\d+)\s*(h|hr|hrs|hour|hours|m|min|mins|minute|minutes|s|sec|secs|second|seconds)", value.lower()):
        n = int(amount)
        if unit.startswith("h"):
            total += n * 3600
        elif unit.startswith("m"):
            total += n * 60
        else:
            total += n
    return total or None


def emails_from_obj(value) -> list[str]:
    emails = []
    if isinstance(value, dict):
        for item in value.get("emails") or []:
            if isinstance(item, dict) and item.get("email"):
                emails.append(item["email"].lower())
            elif isinstance(item, str):
                emails.append(item.lower())
    return emails


def all_emails(engagement: dict) -> set[str]:
    emails: set[str] = set()
    for key in ["owner", "host"]:
        emails.update(emails_from_obj(engagement.get(key)))
    for key in ["contacts", "participants"]:
        for item in engagement.get(key) or []:
            emails.update(emails_from_obj(item))
            if isinstance(item, dict) and item.get("email"):
                emails.add(item["email"].lower())
            if isinstance(item, dict) and item.get("primaryEmail"):
                emails.add(item["primaryEmail"].lower())
    return emails


def matches_person(engagement: dict, person: str) -> bool:
    person = person.lower()
    if not person:
        return True
    if person in all_emails(engagement):
        return True
    localpart = person.split("@", 1)[0]
    text = json.dumps({
        "owner": engagement.get("owner"),
        "host": engagement.get("host"),
        "participants": engagement.get("participants"),
        "transcript": engagement.get("transcript"),
    }, default=str).lower()
    return person in text or (localpart and localpart in text)


def keyword_snippets(text: str, terms: list[str], max_snippets: int = 5) -> list[str]:
    if not text:
        return []
    clean = re.sub(r"\s+", " ", text)
    if not terms:
        return [clean[:900]]
    snippets = []
    lowered = clean.lower()
    for term in terms:
        idx = lowered.find(term.lower())
        if idx == -1:
            continue
        start = max(0, idx - 250)
        end = min(len(clean), idx + len(term) + 450)
        snippets.append(clean[start:end].strip())
        if len(snippets) >= max_snippets:
            break
    return snippets


def main() -> int:
    load_default_env()
    parser = argparse.ArgumentParser(description="Search AskElephant meetings/transcripts.")
    parser.add_argument("--person", default=DEFAULT_PERSON)
    parser.add_argument("--date", help="today, yesterday, or YYYY-MM-DD")
    parser.add_argument("--since")
    parser.add_argument("--until")
    parser.add_argument("--days", type=int, default=1)
    parser.add_argument("--query", default="", help="Space-separated keyword terms.")
    parser.add_argument("--limit", type=int, default=20, help="Maximum matching meetings to return.")
    parser.add_argument("--fetch-limit", type=int, default=500, help="Maximum recent engagements to scan before local filtering.")
    parser.add_argument("--include-transcript", action="store_true")
    args = parser.parse_args()

    start, end = parse_date_range(args)
    terms = [term for term in re.split(r"\s+", args.query.strip()) if term]

    engagements = fetch_rest_engagements(start, end, args.fetch_limit)
    auth_mode = "rest_api_key" if engagements else "graphql_refresh_token"
    if not engagements:
        engagements = fetch_graphql_engagements(start, end, args.fetch_limit)

    filtered = [eng for eng in engagements if matches_person(eng, args.person)]
    if terms:
        filtered = [
            eng for eng in filtered
            if any(term.lower() in (eng.get("transcript") or "").lower() or term.lower() in (eng.get("title") or "").lower() for term in terms)
        ]

    output = {
        "auth_mode": auth_mode,
        "person": args.person,
        "window_start": start.isoformat(),
        "window_end": end.isoformat(),
        "scanned": len(engagements),
        "count": len(filtered),
        "meetings": [],
    }

    for eng in filtered[: args.limit]:
        transcript = eng.get("transcript") or ""
        item = {
            "id": eng.get("id"),
            "url": f"https://app.askelephant.ai/workspaces/{DEFAULT_WORKSPACE_ID}/engagements/{eng.get('id')}",
            "title": eng.get("title"),
            "start_at": eng.get("start_at"),
            "duration_seconds": eng.get("duration_seconds"),
            "owner": eng.get("owner"),
            "host": eng.get("host"),
            "tags": [tag.get("name") for tag in (eng.get("tags") or []) if isinstance(tag, dict)],
            "companies": [company.get("name") for company in (eng.get("companies") or []) if isinstance(company, dict)],
            "participants": [
                {
                    "name": participant.get("displayName") or participant.get("name"),
                    "email": participant.get("primaryEmail") or participant.get("email"),
                    "is_user": participant.get("isUser"),
                }
                for participant in (eng.get("participants") or [])
                if isinstance(participant, dict)
            ],
            "contacts": [
                {
                    "name": " ".join(filter(None, [contact.get("first_name") or contact.get("firstName"), contact.get("last_name") or contact.get("lastName")])).strip(),
                    "emails": sorted(emails_from_obj(contact)),
                }
                for contact in (eng.get("contacts") or [])
                if isinstance(contact, dict)
            ],
            "snippets": keyword_snippets(transcript, terms),
        }
        if args.include_transcript:
            item["transcript"] = transcript
        output["meetings"].append(item)

    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"AskElephant search failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
