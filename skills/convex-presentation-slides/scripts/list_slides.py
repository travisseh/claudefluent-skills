#!/usr/bin/env python3
"""List slide order, id, and inferred title from slidesV3:getByPresentation JSON."""

import json
import sys
from pathlib import Path


def infer_title(slide):
    content_json = slide.get("contentJson") or {}
    nodes = content_json.get("content") or []

    for node in nodes:
        if node.get("type") not in ("heading", "paragraph"):
            continue
        for text_node in node.get("content") or []:
            text = (text_node.get("text") or "").strip()
            if text:
                return text[:50]
    return "(no title)"


def load_slides():
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    return json.load(sys.stdin)


def main():
    slides = load_slides()
    slides.sort(key=lambda slide: slide["order"])

    for index, slide in enumerate(slides, start=1):
        title = infer_title(slide)
        print(f"  {index:3d}. [{slide['order']:3d}] {slide['_id']} | {title}")


if __name__ == "__main__":
    main()
