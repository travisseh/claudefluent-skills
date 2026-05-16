#!/usr/bin/env python3
"""X API v2 CLI wrapper (pay-per-use tier).

Auth: bearer token from $X_BEARER_TOKEN or ~/.x-api-bearer
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import secrets
import sys
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError

API = "https://api.x.com/2"
OAUTH_CLIENT_FILE = Path.home() / ".x-api-oauth-client.json"
OAUTH_TOKEN_FILE = Path.home() / ".x-api-oauth-token.json"

TWEET_FIELDS = "created_at,public_metrics,author_id,conversation_id,lang,entities"
USER_FIELDS = "username,name,description,public_metrics,verified"
EXPANSIONS = "author_id"


def bearer() -> str:
    tok = os.environ.get("X_BEARER_TOKEN")
    if tok:
        return tok.strip()
    p = Path.home() / ".x-api-bearer"
    if p.exists():
        return p.read_text().strip()
    sys.exit("error: set X_BEARER_TOKEN env var or write token to ~/.x-api-bearer")


def get(path: str, params: dict, token: str | None = None) -> dict:
    url = f"{API}{path}?{urlencode({k: v for k, v in params.items() if v is not None})}"
    req = Request(url, headers={"Authorization": f"Bearer {token or bearer()}"})
    try:
        with urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode(errors='replace')}")


# ---------- OAuth2 PKCE (for bookmarks + other user-context endpoints) ----------

def _b64url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def _load_client() -> dict:
    if not OAUTH_CLIENT_FILE.exists():
        sys.exit(f"error: missing {OAUTH_CLIENT_FILE}")
    return json.loads(OAUTH_CLIENT_FILE.read_text())


def _save_token(tok: dict):
    tok["obtained_at"] = int(time.time())
    OAUTH_TOKEN_FILE.write_text(json.dumps(tok, indent=2))
    os.chmod(OAUTH_TOKEN_FILE, 0o600)


def _post_token(data: dict, client: dict) -> dict:
    body = urlencode(data).encode()
    auth = base64.b64encode(
        f"{client['client_id']}:{client['client_secret']}".encode()
    ).decode()
    req = Request(
        "https://api.x.com/2/oauth2/token",
        data=body,
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    try:
        with urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except HTTPError as e:
        sys.exit(f"token exchange failed: HTTP {e.code}: {e.read().decode(errors='replace')}")


def _do_pkce_flow() -> dict:
    client = _load_client()
    verifier = _b64url(secrets.token_bytes(64))
    challenge = _b64url(hashlib.sha256(verifier.encode()).digest())
    state = secrets.token_urlsafe(16)

    auth_url = "https://x.com/i/oauth2/authorize?" + urlencode({
        "response_type": "code",
        "client_id": client["client_id"],
        "redirect_uri": client["redirect_uri"],
        "scope": "tweet.read users.read bookmark.read offline.access",
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    })

    received = {}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a, **k): pass
        def do_GET(self):
            qs = parse_qs(urlparse(self.path).query)
            received.update({k: v[0] for k, v in qs.items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>OK - you can close this tab.</h1>")

    port = int(urlparse(client["redirect_uri"]).port or 8765)
    server = HTTPServer(("localhost", port), Handler)
    print(f"opening browser for X authorization...\nif it doesn't open, visit:\n{auth_url}\n", file=sys.stderr)
    webbrowser.open(auth_url)
    while "code" not in received:
        server.handle_request()
    if received.get("state") != state:
        sys.exit("state mismatch — possible CSRF, aborting")

    tok = _post_token({
        "grant_type": "authorization_code",
        "code": received["code"],
        "redirect_uri": client["redirect_uri"],
        "code_verifier": verifier,
        "client_id": client["client_id"],
    }, client)
    _save_token(tok)
    return tok


def _refresh(tok: dict) -> dict | None:
    """Try to refresh. Returns new token dict, or None if the refresh token was
    already consumed (e.g. by the Vercel cron using the same credentials)."""
    client = _load_client()
    body = urlencode({
        "grant_type": "refresh_token",
        "refresh_token": tok["refresh_token"],
        "client_id": client["client_id"],
    }).encode()
    auth = base64.b64encode(
        f"{client['client_id']}:{client['client_secret']}".encode()
    ).decode()
    req = Request(
        "https://api.x.com/2/oauth2/token",
        data=body,
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    try:
        with urlopen(req, timeout=30) as r:
            new = json.loads(r.read())
    except HTTPError as e:
        if e.code == 400:
            print("refresh token was already consumed, re-authenticating...", file=sys.stderr)
            return None
        raise
    _save_token(new)
    return new


def user_token() -> str:
    if not OAUTH_TOKEN_FILE.exists():
        tok = _do_pkce_flow()
    else:
        tok = json.loads(OAUTH_TOKEN_FILE.read_text())
        if tok["obtained_at"] + tok.get("expires_in", 7200) - 60 < time.time():
            refreshed = _refresh(tok) if "refresh_token" in tok else None
            if refreshed:
                tok = refreshed
            else:
                tok = _do_pkce_flow()
    return tok["access_token"]


def attach_authors(payload: dict) -> dict:
    users = {u["id"]: u for u in payload.get("includes", {}).get("users", [])}
    for t in payload.get("data", []) or []:
        u = users.get(t.get("author_id"))
        if u:
            t["author"] = {"username": u["username"], "name": u["name"]}
    return payload


def to_md(payload: dict) -> str:
    posts = payload.get("data", []) or []
    if not posts:
        return "_No results._"
    out = []
    for t in posts:
        a = t.get("author", {})
        m = t.get("public_metrics", {})
        handle = a.get("username", "?")
        url = f"https://x.com/{handle}/status/{t['id']}"
        out.append(
            f"### @{handle} — {t.get('created_at','')}\n"
            f"{t.get('text','').strip()}\n\n"
            f"♥ {m.get('like_count',0)} · 🔁 {m.get('retweet_count',0)} · "
            f"💬 {m.get('reply_count',0)} · [link]({url})\n"
        )
    return "\n---\n\n".join(out)


def emit(payload: dict, fmt: str):
    if fmt == "md":
        print(to_md(payload))
    else:
        print(json.dumps(payload, indent=2))


def cmd_search(args):
    q = args.query
    if args.no_retweets:
        q += " -is:retweet"
    if args.lang:
        q += f" lang:{args.lang}"
    if args.min_likes:
        q += f" min_faves:{args.min_likes}"
    payload = get(
        "/tweets/search/recent",
        {
            "query": q,
            "max_results": min(max(args.max, 10), 100),
            "tweet.fields": TWEET_FIELDS,
            "user.fields": USER_FIELDS,
            "expansions": EXPANSIONS,
            "sort_order": "relevancy" if args.relevancy else "recency",
        },
    )
    emit(attach_authors(payload), args.format)


def cmd_user(args):
    payload = get(
        f"/users/by/username/{args.username}",
        {"user.fields": USER_FIELDS},
    )
    emit(payload, args.format)


def cmd_user_tweets(args):
    u = get(f"/users/by/username/{args.username}", {})
    uid = u["data"]["id"]
    payload = get(
        f"/users/{uid}/tweets",
        {
            "max_results": min(max(args.max, 5), 100),
            "tweet.fields": TWEET_FIELDS,
            "user.fields": USER_FIELDS,
            "expansions": EXPANSIONS,
            "exclude": "retweets,replies" if args.no_retweets else None,
        },
    )
    emit(attach_authors(payload), args.format)


def parse_tweet_id(s: str) -> str:
    m = re.search(r"status/(\d+)", s)
    return m.group(1) if m else s


def cmd_tweet(args):
    tid = parse_tweet_id(args.id_or_url)
    payload = get(
        f"/tweets/{tid}",
        {
            "tweet.fields": TWEET_FIELDS,
            "user.fields": USER_FIELDS,
            "expansions": EXPANSIONS,
        },
    )
    # Normalize so to_md works
    if "data" in payload and isinstance(payload["data"], dict):
        payload["data"] = [payload["data"]]
    emit(attach_authors(payload), args.format)


def cmd_bookmarks(args):
    tok = user_token()
    me = get("/users/me", {}, token=tok)
    uid = me["data"]["id"]
    remaining = args.max
    all_tweets, all_users, next_token = [], {}, None
    while remaining > 0:
        page = get(
            f"/users/{uid}/bookmarks",
            {
                "max_results": min(max(remaining, 10), 100),
                "tweet.fields": TWEET_FIELDS,
                "user.fields": USER_FIELDS,
                "expansions": EXPANSIONS,
                "pagination_token": next_token,
            },
            token=tok,
        )
        data = page.get("data") or []
        if not data:
            break
        all_tweets.extend(data)
        for u in page.get("includes", {}).get("users", []):
            all_users[u["id"]] = u
        remaining -= len(data)
        next_token = page.get("meta", {}).get("next_token")
        if not next_token:
            break
    payload = {
        "data": all_tweets[: args.max],
        "includes": {"users": list(all_users.values())},
        "meta": {"result_count": min(len(all_tweets), args.max)},
    }
    emit(attach_authors(payload), args.format)


def cmd_thread(args):
    tid = parse_tweet_id(args.id_or_url)
    payload = get(
        "/tweets/search/recent",
        {
            "query": f"conversation_id:{tid}",
            "max_results": min(max(args.max, 10), 100),
            "tweet.fields": TWEET_FIELDS,
            "user.fields": USER_FIELDS,
            "expansions": EXPANSIONS,
        },
    )
    emit(attach_authors(payload), args.format)


def main():
    p = argparse.ArgumentParser(prog="x")
    p.add_argument("--format", choices=["json", "md"], default="json")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--max", type=int, default=25)
    s.add_argument("--lang")
    s.add_argument("--no-retweets", action="store_true")
    s.add_argument("--min-likes", type=int)
    s.add_argument("--relevancy", action="store_true")
    s.set_defaults(func=cmd_search)

    s = sub.add_parser("user")
    s.add_argument("username")
    s.set_defaults(func=cmd_user)

    s = sub.add_parser("user-tweets")
    s.add_argument("username")
    s.add_argument("--max", type=int, default=20)
    s.add_argument("--no-retweets", action="store_true")
    s.set_defaults(func=cmd_user_tweets)

    s = sub.add_parser("tweet")
    s.add_argument("id_or_url")
    s.set_defaults(func=cmd_tweet)

    s = sub.add_parser("thread")
    s.add_argument("id_or_url")
    s.add_argument("--max", type=int, default=50)
    s.set_defaults(func=cmd_thread)

    s = sub.add_parser("bookmarks")
    s.add_argument("--max", type=int, default=10)
    s.set_defaults(func=cmd_bookmarks)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
