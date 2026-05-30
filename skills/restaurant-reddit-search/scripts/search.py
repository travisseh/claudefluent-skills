#!/usr/bin/env python3
"""Search Reddit for a phrase/topic via Apify trudax/reddit-scraper-lite.

Example Company variant: artifacts land under the product2 repo, defaults tuned
for business-marketing / competitive-intel research.

Writes a markdown report and raw JSON to artifacts/reddit-search/<slug>/.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ACTOR = "trudax~reddit-scraper-lite"
APIFY_ENDPOINT = (
    f"https://api.apify.com/v2/acts/{ACTOR}/run-sync-get-dataset-items"
)
ENV_FILE = Path(
    "/Users/you/Programming/personal-master/personal/"
    "claude_course/website/.env.local"
)
WORKSPACE_ROOT = Path("/Users/you/Programming/product2")


def load_token() -> str:
    env = os.environ.get("APIFY_API_TOKEN")
    if env:
        return env
    if not ENV_FILE.exists():
        sys.exit(f"APIFY_API_TOKEN not in env and {ENV_FILE} missing")
    for line in ENV_FILE.read_text().splitlines():
        if line.startswith("APIFY_API_TOKEN"):
            _, _, val = line.partition("=")
            return val.strip().strip('"').strip("'")
    sys.exit(f"APIFY_API_TOKEN not found in {ENV_FILE}")


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:60] or "query"


def run_actor(token: str, payload: dict, timeout_secs: int) -> list[dict]:
    url = f"{APIFY_ENDPOINT}?token={token}&timeout={timeout_secs}"
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_secs + 30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        sys.exit(f"Apify HTTP {e.code}: {body[:500]}")
    except urllib.error.URLError as e:
        sys.exit(f"Apify request failed: {e}")


def group_items(items: list[dict]) -> tuple[list[dict], dict[str, list[dict]]]:
    """Split dataset items into posts and comments-by-postId."""
    posts: list[dict] = []
    comments: dict[str, list[dict]] = {}
    for it in items:
        kind = it.get("dataType") or it.get("type") or ""
        if "comment" in kind.lower():
            pid = it.get("postId") or it.get("parentId") or ""
            comments.setdefault(str(pid), []).append(it)
        else:
            posts.append(it)
    return posts, comments


def fmt_ts(value) -> str:
    if value is None:
        return ""
    try:
        ts = float(value)
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
    except (TypeError, ValueError):
        pass
    if isinstance(value, str):
        return value.split("T")[0]
    return ""


def build_report(
    query: str,
    args: argparse.Namespace,
    posts: list[dict],
    comments: dict[str, list[dict]],
) -> str:
    lines: list[str] = []
    lines.append(f"# Reddit search: {query}")
    lines.append("")
    meta = [
        f"**Run**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Sort**: {args.sort}",
        f"**Time**: {args.time}",
        f"**Subreddit**: {args.subreddit or '(all)'}",
        f"**Posts**: {len(posts)}",
    ]
    lines.append(" · ".join(meta))
    lines.append("")

    if not posts:
        lines.append("_No posts returned. Try a broader query, longer time window, or different sort._")
        return "\n".join(lines)

    posts_sorted = sorted(
        posts,
        key=lambda p: (p.get("numberOfupvotes") or p.get("upVotes") or p.get("score") or 0),
        reverse=True,
    )

    for i, p in enumerate(posts_sorted, 1):
        title = p.get("title") or "(no title)"
        url = p.get("url") or p.get("postUrl") or ""
        subreddit = (
            p.get("communityName")
            or p.get("subreddit")
            or p.get("parsedCommunityName")
            or ""
        )
        author = p.get("username") or p.get("author") or ""
        score = (
            p.get("numberOfupvotes")
            or p.get("upVotes")
            or p.get("score")
            or 0
        )
        num_comments = (
            p.get("numberOfComments") or p.get("numComments") or 0
        )
        created = fmt_ts(p.get("createdAt") or p.get("created"))
        body = (p.get("body") or p.get("text") or "").strip()
        if len(body) > 600:
            body = body[:600].rstrip() + "…"

        lines.append(f"## {i}. {title}")
        lines.append("")
        bits = []
        if subreddit:
            bits.append(f"r/{subreddit}" if not str(subreddit).startswith("r/") else subreddit)
        if author:
            bits.append(f"u/{author}")
        bits.append(f"⬆ {score}")
        bits.append(f"💬 {num_comments}")
        if created:
            bits.append(created)
        lines.append(" · ".join(bits))
        lines.append("")
        if url:
            lines.append(f"<{url}>")
            lines.append("")
        if body:
            lines.append("> " + body.replace("\n", "\n> "))
            lines.append("")

        pid = str(p.get("id") or p.get("postId") or "")
        post_comments = comments.get(pid, [])
        if post_comments:
            post_comments.sort(
                key=lambda c: (
                    c.get("numberOfupvotes") or c.get("upVotes") or c.get("score") or 0
                ),
                reverse=True,
            )
            lines.append("**Top comments:**")
            lines.append("")
            for c in post_comments[: args.max_comments_shown]:
                cbody = (c.get("body") or c.get("text") or "").strip()
                if not cbody:
                    continue
                if len(cbody) > 400:
                    cbody = cbody[:400].rstrip() + "…"
                cauthor = c.get("username") or c.get("author") or "?"
                cscore = (
                    c.get("numberOfupvotes") or c.get("upVotes") or c.get("score") or 0
                )
                lines.append(f"- **u/{cauthor}** (⬆ {cscore}): {cbody}")
            lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Search Reddit via Apify and write a markdown report (Example Company variant)."
    )
    parser.add_argument("query", help="Search phrase or topic")
    parser.add_argument(
        "--subreddit",
        default="",
        help="Restrict to one subreddit (name only, no r/ prefix)",
    )
    parser.add_argument(
        "--sort",
        default="relevance",
        choices=["relevance", "hot", "top", "new", "rising", "comments"],
    )
    parser.add_argument(
        "--time",
        default="year",
        choices=["all", "hour", "day", "week", "month", "year"],
    )
    parser.add_argument(
        "--posts",
        type=int,
        default=10,
        help="Posts to return (default 10)",
    )
    parser.add_argument(
        "--comments-per-post",
        type=int,
        default=5,
        help="Comments scraped per post (default 5)",
    )
    parser.add_argument(
        "--max-comments-shown",
        type=int,
        default=3,
        help="Top comments shown in report per post (default 3)",
    )
    parser.add_argument(
        "--no-comments",
        action="store_true",
        help="Skip comments entirely (cheaper/faster)",
    )
    parser.add_argument(
        "--include-nsfw",
        action="store_true",
        help="Include NSFW results (default: off)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=240,
        help="Actor timeout seconds (default 240)",
    )
    parser.add_argument(
        "--out",
        default="",
        help="Output dir (default: artifacts/reddit-search/<slug> under product2)",
    )
    args = parser.parse_args()

    token = load_token()

    max_comments = 0 if args.no_comments else args.comments_per_post
    max_items = args.posts + (args.posts * max_comments) + 5

    payload = {
        "searches": [args.query],
        "searchPosts": True,
        "searchComments": False,
        "searchCommunities": False,
        "searchUsers": False,
        "skipComments": args.no_comments,
        "skipUserPosts": True,
        "skipCommunity": True,
        "sort": args.sort,
        "time": args.time,
        "includeNSFW": args.include_nsfw,
        "maxItems": max_items,
        "maxPostCount": args.posts,
        "maxComments": max_comments,
        "proxy": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]},
    }
    if args.subreddit:
        payload["searchCommunityName"] = args.subreddit.lstrip("r/").rstrip("/")

    slug = slugify(args.query)
    if args.out:
        out_dir = Path(args.out)
    else:
        out_dir = WORKSPACE_ROOT / "artifacts" / "reddit-search" / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[business-reddit-search] querying Apify for: {args.query!r}", file=sys.stderr)
    print(f"[business-reddit-search] sort={args.sort} time={args.time} posts={args.posts} max_items={max_items}", file=sys.stderr)
    started = time.time()
    items = run_actor(token, payload, args.timeout)
    elapsed = time.time() - started
    print(f"[business-reddit-search] got {len(items)} dataset items in {elapsed:.1f}s", file=sys.stderr)

    raw_path = out_dir / "raw.json"
    raw_path.write_text(json.dumps(items, indent=2))

    posts, comments = group_items(items)
    print(f"[business-reddit-search] parsed {len(posts)} posts, {sum(len(v) for v in comments.values())} comments", file=sys.stderr)

    report = build_report(args.query, args, posts, comments)
    report_path = out_dir / "report.md"
    report_path.write_text(report)

    est_cost = len(items) * 0.004 + 0.02 * 2
    print(f"[business-reddit-search] wrote {report_path}", file=sys.stderr)
    print(f"[business-reddit-search] estimated cost: ${est_cost:.3f}", file=sys.stderr)

    print(str(report_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
