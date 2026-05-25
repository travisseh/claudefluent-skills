---
name: message-me
description: "Send the assistant's output, a provided text body, or a file's full contents to the user's own iMessage. Use whenever the user says 'message me', 'send to my iMessage', 'text me this', 'send this to my phone', or asks for an automation result to be delivered by iMessage. Sends long content in chunks instead of summarizing or truncating."
---

# Message Me

Send content to the user's own iMessage using the local iMessage tool.

## Default Behavior

- Send the content in full.
- Do not summarize just to fit a text message.
- If the content is long, split it into numbered chunks and send all chunks.
- Use the user's self iMessage number: `+18014337874`.
- Prefer this skill over `cron/lib/imessage-self.sh` because that helper truncates long messages.

## Command

Use the helper script:

```bash
python3 /Users/you/.codex/skills/message-me/scripts/message_me.py @/path/to/body.txt
```

Or pipe content:

```bash
printf '%s' "$BODY" | python3 /Users/you/.codex/skills/message-me/scripts/message_me.py -
```

The script calls:

```bash
node ~/.config/imessage-tools/imessage.js send +18014337874 "<chunk>"
```

## Workflow

1. Put the exact message body in a temp file, preserving useful structure.
2. Run `scripts/message_me.py @/tmp/file`.
3. Confirm success briefly.

## Style

For generated summaries, keep the message concise if that is what the underlying task calls for, but never omit content solely because iMessage is long. When the user specifically says not to summarize, send the full content.
