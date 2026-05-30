#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

API_BASE = "https://api.render.com/v1"
REPORTING_REPO = "https://github.com/example-org/example-company-reporting"
REPORTING_OWNER_ID = os.environ.get("RENDER_REPORTING_OWNER_ID", "tea-cbfgtpl0malclpe38gu0")


def api_key():
    key = os.environ.get("RENDER_API_KEY")
    if not key:
        raise SystemExit(
            "Missing RENDER_API_KEY. Create one at https://dashboard.render.com/account/api-keys "
            "and export it in your shell."
        )
    return key


def get(path, params=None):
    query = urllib.parse.urlencode(params or {}, doseq=True)
    url = f"{API_BASE}{path}"
    if query:
        url = f"{url}?{query}"

    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key()}",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else None
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = body
        raise SystemExit(
            f"Render API returned {error.code} {error.reason}:\n"
            f"{json.dumps(parsed, indent=2) if not isinstance(parsed, str) else parsed}"
        ) from error


def request_json(method, path, payload=None):
    url = f"{API_BASE}{path}"
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key()}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            response_body = response.read().decode("utf-8")
            return json.loads(response_body) if response_body else None
    except urllib.error.HTTPError as error:
        response_body = error.read().decode("utf-8")
        try:
            parsed = json.loads(response_body)
        except json.JSONDecodeError:
            parsed = response_body
        raise SystemExit(
            f"Render API returned {error.code} {error.reason}:\n"
            f"{json.dumps(parsed, indent=2) if not isinstance(parsed, str) else parsed}"
        ) from error


def assert_reporting_service(service_id):
    service_payload = get(f"/services/{service_id}")
    service = service_payload.get("service", service_payload) if isinstance(service_payload, dict) else {}
    repo = service.get("repo")
    owner_id = service.get("ownerId")
    root_dir = service.get("rootDir")
    name = service.get("name", "")

    if repo != REPORTING_REPO or owner_id != REPORTING_OWNER_ID or root_dir != "apps/dashboard":
        raise SystemExit(
            "Refusing Render write: target is not the Example Company Reporting service. "
            f"service_id={service_id} name={name!r} repo={repo!r} owner_id={owner_id!r} root_dir={root_dir!r}"
        )

    return service


def redact_env_vars(payload):
    redacted = []
    for item in payload or []:
        env_var = item.get("envVar", {})
        key = env_var.get("key")
        value = env_var.get("value")
        redacted.append({
            **item,
            "envVar": {
                "key": key,
                "value": "" if value == "" else "[redacted]",
            },
        })
    return redacted


def redact_env_var_response(payload):
    if not isinstance(payload, dict):
        return payload
    if "envVar" in payload:
        return redact_env_vars([payload])[0]
    if "key" in payload and "value" in payload:
        return {
            **payload,
            "value": "" if payload.get("value") == "" else "[redacted]",
        }
    return payload


def split_csv(value):
    if not value:
        return None
    return [item.strip() for item in value.split(",") if item.strip()]


def print_json(payload):
    print(json.dumps(payload, indent=2, sort_keys=True))


def add_common_list_args(parser):
    parser.add_argument("--limit", type=int)
    parser.add_argument("--cursor")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Reporting-scoped Render API helper."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    owners = subparsers.add_parser("owners", help="List Render workspaces/owners")
    owners.add_argument("--name")
    owners.add_argument("--email")
    add_common_list_args(owners)

    services = subparsers.add_parser("services", help="List services")
    services.add_argument("--name")
    services.add_argument("--type")
    services.add_argument("--region")
    services.add_argument("--owner")
    add_common_list_args(services)

    service = subparsers.add_parser("service", help="Get one service")
    service.add_argument("service_id")

    env_vars = subparsers.add_parser("env-vars", help="List service env vars with values redacted")
    env_vars.add_argument("service_id")

    set_env_var = subparsers.add_parser("set-env-var", help="Add or update one env var on a Reporting service")
    set_env_var.add_argument("service_id")
    set_env_var.add_argument("key")
    set_env_var.add_argument("--value", required=True)

    deploys = subparsers.add_parser("deploys", help="List deploys for a service")
    deploys.add_argument("service_id")
    deploys.add_argument("--status")
    add_common_list_args(deploys)

    deploy = subparsers.add_parser("deploy", help="Get one deploy")
    deploy.add_argument("service_id")
    deploy.add_argument("deploy_id")

    logs = subparsers.add_parser("logs", help="List logs for a resource")
    logs.add_argument("--owner", default=os.environ.get("RENDER_OWNER_ID"))
    logs.add_argument("--resource", required=True, help="Usually the service ID, e.g. srv-...")
    logs.add_argument("--minutes", type=int, default=60)
    logs.add_argument("--start")
    logs.add_argument("--end")
    logs.add_argument("--direction", default="backorganization", choices=["backorganization", "fororganization"])
    logs.add_argument("--level")
    logs.add_argument("--type")
    logs.add_argument("--status")
    logs.add_argument("--path")
    logs.add_argument("--text")
    logs.add_argument("--limit", type=int)

    return parser.parse_args()


def main():
    args = parse_args()

    if args.command == "owners":
        params = {
            "name": split_csv(args.name),
            "email": split_csv(args.email),
            "limit": args.limit,
            "cursor": args.cursor,
        }
        print_json(get("/owners", clean(params)))
        return

    if args.command == "services":
        params = {
            "name": split_csv(args.name),
            "type": split_csv(args.type),
            "region": split_csv(args.region),
            "ownerId": args.owner,
            "limit": args.limit,
            "cursor": args.cursor,
        }
        print_json(get("/services", clean(params)))
        return

    if args.command == "service":
        print_json(get(f"/services/{args.service_id}"))
        return

    if args.command == "env-vars":
        assert_reporting_service(args.service_id)
        print_json(redact_env_vars(get(f"/services/{args.service_id}/env-vars")))
        return

    if args.command == "set-env-var":
        service = assert_reporting_service(args.service_id)
        result = request_json(
            "PUT",
            f"/services/{args.service_id}/env-vars/{urllib.parse.quote(args.key, safe='')}",
            {"value": args.value},
        )
        print_json({
            "updated": True,
            "serviceId": args.service_id,
            "serviceName": service.get("name"),
            "key": args.key,
            "value": "[redacted]" if args.value else "",
            "renderResponse": redact_env_var_response(result),
        })
        return

    if args.command == "deploys":
        params = {
            "status": split_csv(args.status),
            "limit": args.limit,
            "cursor": args.cursor,
        }
        print_json(get(f"/services/{args.service_id}/deploys", clean(params)))
        return

    if args.command == "deploy":
        print_json(get(f"/services/{args.service_id}/deploys/{args.deploy_id}"))
        return

    if args.command == "logs":
        if not args.owner:
            raise SystemExit("Logs require --owner <ownerId> or RENDER_OWNER_ID.")
        end = datetime.now(timezone.utc)
        start = end - timedelta(minutes=args.minutes)
        params = {
            "ownerId": args.owner,
            "resource": split_csv(args.resource),
            "startTime": args.start or start.isoformat().replace("+00:00", "Z"),
            "endTime": args.end or end.isoformat().replace("+00:00", "Z"),
            "direction": args.direction,
            "level": split_csv(args.level),
            "type": split_csv(args.type),
            "statusCode": split_csv(args.status),
            "path": split_csv(args.path),
            "text": split_csv(args.text),
            "limit": args.limit,
        }
        print_json(get("/logs", clean(params)))
        return


def clean(params):
    return {key: value for key, value in params.items() if value not in (None, [], "")}


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
