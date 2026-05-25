#!/usr/bin/env python3
"""Send full text to the user's own iMessage, chunking long bodies."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PHONE = "+18014337874"
IMESSAGE = str(Path.home() / ".config/imessage-tools/imessage.js")
CHUNK_LIMIT = 2800


def read_body(arg: str) -> str:
    if arg == "-":
        return sys.stdin.read()
    if arg.startswith("@"):
        return Path(arg[1:]).read_text()
    return arg


def split_chunks(text: str, limit: int = CHUNK_LIMIT) -> list[str]:
    if len(text) <= limit:
        return [text]

    chunks: list[str] = []
    remaining = text
    while remaining:
        if len(remaining) <= limit:
            chunks.append(remaining)
            break

        split_at = remaining.rfind("\n\n", 0, limit)
        if split_at < limit // 2:
            split_at = remaining.rfind("\n", 0, limit)
        if split_at < limit // 2:
            split_at = remaining.rfind(" ", 0, limit)
        if split_at < limit // 2:
            split_at = limit

        chunk = remaining[:split_at].strip()
        if chunk:
            chunks.append(chunk)
        remaining = remaining[split_at:].lstrip()

    return chunks


def send(chunk: str) -> None:
    subprocess.run(
        ["node", IMESSAGE, "send", PHONE, chunk],
        check=True,
    )


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: message_me.py <text|@file|->", file=sys.stderr)
        return 2

    body = read_body(sys.argv[1]).strip()
    if not body:
        print("No message body provided.", file=sys.stderr)
        return 2

    chunks = split_chunks(body)
    total = len(chunks)
    for index, chunk in enumerate(chunks, start=1):
        if total > 1:
            chunk = f"({index}/{total})\n{chunk}"
        send(chunk)

    print(f"Sent {total} iMessage chunk(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
