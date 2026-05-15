#!/usr/bin/env python3
import argparse
from pathlib import Path


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def command_name(value: str) -> str:
    value = value.strip()
    return value if value.startswith("/") else f"/{value}"


def unique(values: list[str]) -> list[str]:
    seen: list[str] = []
    for value in values:
        value = value.strip()
        if value and value not in seen:
            seen.append(value)
    return seen


def parse_prompts(values: list[str] | None) -> list[tuple[str, str]]:
    if not values:
        return [("Status", "status"), ("What needs attention?", "What needs attention today?")]

    prompts: list[tuple[str, str]] = []
    for value in values:
        if "|" not in value:
            raise SystemExit(
                f"Invalid --prompt {value!r}. Use 'Title|message', for example 'Status|status'."
            )
        title, message = value.split("|", 1)
        title = title.strip()
        message = message.strip()
        if not title or not message:
            raise SystemExit(
                f"Invalid --prompt {value!r}. Both title and message are required."
            )
        prompts.append((title, message))
    return prompts


def build_suggested_prompts(prompts: list[tuple[str, str]]) -> str:
    lines: list[str] = []
    for title, message in prompts:
        lines.extend(
            [
                "      - title: " + yaml_quote(title),
                "        message: " + yaml_quote(message),
            ]
        )
    return "\n".join(lines)


def build_manifest(args: argparse.Namespace) -> str:
    bot_display_name = args.bot_display_name or args.name
    agent_description = args.agent_description or args.description
    long_description = args.long_description or (
        f"{args.name} is an internal Slack AI agent configured with Socket Mode. "
        "It supports Slack's agent panel, app Chat and History tabs, suggested prompts, "
        "and long-running TypeScript/Node workers without a public request URL."
    )

    prompts = parse_prompts(args.prompt)
    scopes = ["assistant:write", "chat:write", "im:history"]
    events = ["assistant_thread_started", "assistant_thread_context_changed", "message.im"]

    slash_command_block = ""
    if args.command:
        command = command_name(args.command)
        usage = args.usage or "status | ask <question>"
        slash_command_block = f"""  slash_commands:
    - command: {command}
      description: {yaml_quote(args.description)}
      usage_hint: {yaml_quote(usage)}
      should_escape: false
      url: {yaml_quote(args.request_url)}
"""
        scopes.append("commands")

    if args.app_mentions:
        scopes.append("app_mentions:read")
        events.append("app_mention")

    scopes.extend(args.extra_scope or [])
    bot_scope_lines = "\n".join(f"      - {scope}" for scope in unique(scopes))
    event_lines = "\n".join(f"      - {event}" for event in unique(events))

    return f"""_metadata:
  major_version: 2
  minor_version: 1

display_information:
  name: {yaml_quote(args.name)}
  description: {yaml_quote(args.description)}
  long_description: {yaml_quote(long_description)}
  background_color: {yaml_quote(args.background_color)}

features:
  agent_view:
    agent_description: {yaml_quote(agent_description)}
    suggested_prompts:
{build_suggested_prompts(prompts)}
  app_home:
    home_tab_enabled: false
    messages_tab_enabled: true
    messages_tab_read_only_enabled: false
  bot_user:
    display_name: {yaml_quote(bot_display_name)}
    always_online: true
{slash_command_block}
oauth_config:
  scopes:
    bot:
{bot_scope_lines}

settings:
  socket_mode_enabled: true
  token_rotation_enabled: false
  org_deploy_enabled: false
  is_hosted: false
  interactivity:
    is_enabled: true
  event_subscriptions:
    bot_events:
{event_lines}
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a paste-ready Slack manifest for a Socket Mode AI agent."
    )
    parser.add_argument("--name", required=True, help="Slack app display name")
    parser.add_argument("--description", required=True, help="Short Slack app description")
    parser.add_argument(
        "--agent-description",
        help="Description shown in Slack's agent experience. Defaults to --description.",
    )
    parser.add_argument(
        "--prompt",
        action="append",
        help="Suggested prompt as 'Title|message'. Repeat for multiple prompts.",
    )
    parser.add_argument("--bot-display-name", help="Bot user display name. Defaults to --name")
    parser.add_argument(
        "--long-description",
        help="Long Slack app description. Defaults to a concise generated description.",
    )
    parser.add_argument(
        "--background-color",
        default="#4A154B",
        help="Slack app background color",
    )
    parser.add_argument(
        "--command",
        help="Optional slash command, with or without leading slash. Not included by default.",
    )
    parser.add_argument("--usage", help="Slash command usage hint, only used with --command")
    parser.add_argument(
        "--request-url",
        default="https://example.com/slack/commands",
        help="Placeholder HTTPS URL for optional slash command config. Socket Mode carries the actual payload.",
    )
    parser.add_argument(
        "--app-mentions",
        action="store_true",
        help="Include app mention event support. Useful for channel mentions, not required for agent UX.",
    )
    parser.add_argument(
        "--extra-scope",
        action="append",
        help="Additional bot OAuth scope. Repeat for multiple scopes.",
    )
    parser.add_argument("--output", help="Optional path to write the manifest")
    args = parser.parse_args()

    manifest = build_manifest(args)
    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.write_text(manifest)
        print(str(output_path))
    else:
        print(manifest)


if __name__ == "__main__":
    main()
