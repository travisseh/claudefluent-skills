#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


DEFAULT_ACCOUNT_ID = "act_2766538970268735"


def env(name: str, default: str | None = None) -> str:
    value = os.environ.get(name, default)
    if not value:
        raise SystemExit(f"Missing required env var: {name}")
    return value


def graph_get(path: str, params: dict[str, str]) -> dict:
    version = os.environ.get("META_API_VERSION", "v25.0")
    token = env("META_ACCESS_TOKEN")
    query = urllib.parse.urlencode({**params, "access_token": token})
    url = f"https://graph.facebook.com/{version}/{path}?{query}"
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode("utf-8"))


def print_json(data: dict) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def insights(args: argparse.Namespace) -> None:
    account_id = os.environ.get("META_AD_ACCOUNT_ID", DEFAULT_ACCOUNT_ID)
    data = graph_get(
        f"{account_id}/insights",
        {
            "date_preset": args.date_preset,
            "level": "ad",
            "fields": "ad_id,campaign_name,adset_name,ad_name,spend,impressions,clicks,ctr,cpc,reach,actions",
            "limit": str(args.limit),
        },
    )
    if data.get("paging", {}).get("next"):
        data["paging"]["next"] = "[redacted: contains access token]"
    print_json(data)


def ads(args: argparse.Namespace) -> None:
    account_id = os.environ.get("META_AD_ACCOUNT_ID", DEFAULT_ACCOUNT_ID)
    data = graph_get(
        f"{account_id}/ads",
        {
            "fields": "id,name,effective_status,campaign{name},adset{name},creative{id,name,title,body,object_story_spec,asset_feed_spec}",
            "limit": str(args.limit),
        },
    )
    if data.get("paging", {}).get("next"):
        data["paging"]["next"] = "[redacted: contains access token]"
    print_json(data)


def preview(args: argparse.Namespace) -> None:
    data = graph_get(
        f"{args.ad_id}/previews",
        {
            "ad_format": args.ad_format,
            "limit": "1",
        },
    )
    print_json(data)


def video(args: argparse.Namespace) -> None:
    data = graph_get(
        args.video_id,
        {
            "fields": "id,source,embed_html,permalink_url,picture,thumbnails",
        },
    )
    print_json(data)


def main() -> int:
    parser = argparse.ArgumentParser(description="Query ExampleCo Meta Ads via Graph API.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    insights_parser = subparsers.add_parser("insights")
    insights_parser.add_argument("--date-preset", default="last_30d")
    insights_parser.add_argument("--limit", type=int, default=100)
    insights_parser.set_defaults(func=insights)

    ads_parser = subparsers.add_parser("ads")
    ads_parser.add_argument("--limit", type=int, default=25)
    ads_parser.set_defaults(func=ads)

    preview_parser = subparsers.add_parser("preview")
    preview_parser.add_argument("ad_id")
    preview_parser.add_argument("--ad-format", default="DESKTOP_FEED_STANDARD")
    preview_parser.set_defaults(func=preview)

    video_parser = subparsers.add_parser("video")
    video_parser.add_argument("video_id")
    video_parser.set_defaults(func=video)

    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
