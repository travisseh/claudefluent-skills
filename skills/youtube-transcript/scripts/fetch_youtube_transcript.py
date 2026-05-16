#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


@dataclass
class TranscriptResult:
    input: str
    video_id: str
    source: str
    language_code: str | None
    language: str | None
    is_generated: bool | None
    translated_to: str | None
    snippets: list[dict[str, Any]]
    text: str
    artifacts_dir: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch a YouTube transcript via captions first and ASR fallback second.",
    )
    parser.add_argument("input", help="YouTube URL or video ID")
    parser.add_argument(
        "--langs",
        default="en",
        help="Comma-separated preferred languages, in priority order. Default: en",
    )
    parser.add_argument(
        "--translate-to",
        help="Translate caption tracks to this language when supported by YouTube captions.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Default: text",
    )
    parser.add_argument(
        "--timestamps",
        action="store_true",
        help="Print timestamp-prefixed lines in text mode.",
    )
    parser.add_argument(
        "--prefer-generated",
        action="store_true",
        help="Prefer auto-generated captions before manually created captions.",
    )
    parser.add_argument(
        "--preserve-formatting",
        action="store_true",
        help="Preserve inline formatting when the transcript API supports it.",
    )
    parser.add_argument(
        "--fallback-asr",
        action="store_true",
        help="Use OpenAI speech-to-text if caption retrieval fails.",
    )
    parser.add_argument(
        "--force-asr",
        action="store_true",
        help="Skip caption retrieval and transcribe the video audio directly with OpenAI.",
    )
    parser.add_argument(
        "--asr-model",
        default="gpt-4o-mini-transcribe",
        help="OpenAI transcription model for --fallback-asr. Default: gpt-4o-mini-transcribe",
    )
    parser.add_argument(
        "--text-out",
        help="Optional path to save plain text output.",
    )
    parser.add_argument(
        "--json-out",
        help="Optional path to save JSON output.",
    )
    parser.add_argument(
        "--keep-artifacts",
        action="store_true",
        help="Keep temporary subtitle or audio artifacts for debugging.",
    )
    return parser.parse_args()


def extract_video_id(value: str) -> str:
    value = value.strip()
    if re.fullmatch(r"[\w-]{11}", value):
        return value

    parsed = urlparse(value)
    if parsed.netloc in {"youtu.be", "www.youtu.be"}:
        candidate = parsed.path.strip("/").split("/")[0]
        if re.fullmatch(r"[\w-]{11}", candidate):
            return candidate

    if "youtube.com" in parsed.netloc:
        query_video = parse_qs(parsed.query).get("v", [None])[0]
        if query_video and re.fullmatch(r"[\w-]{11}", query_video):
            return query_video

        path_parts = [part for part in parsed.path.split("/") if part]
        for marker in ("embed", "shorts", "live"):
            if marker in path_parts:
                idx = path_parts.index(marker)
                if idx + 1 < len(path_parts):
                    candidate = path_parts[idx + 1]
                    if re.fullmatch(r"[\w-]{11}", candidate):
                        return candidate

    raise ValueError(f"Could not extract a YouTube video ID from: {value}")


def split_langs(raw: str) -> list[str]:
    langs = [item.strip() for item in raw.split(",") if item.strip()]
    return langs or ["en"]


def build_text(snippets: list[dict[str, Any]]) -> str:
    return "\n".join(snippet["text"] for snippet in snippets if snippet["text"].strip())


def format_timestamp(seconds: float) -> str:
    total = int(max(seconds, 0))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def text_with_timestamps(snippets: list[dict[str, Any]]) -> str:
    return "\n".join(
        f"[{format_timestamp(float(snippet['start']))}] {snippet['text']}"
        for snippet in snippets
        if snippet["text"].strip()
    )


def ensure_parent(path_str: str) -> Path:
    path = Path(path_str).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def parse_openai_key_from_env_file(path: Path) -> str | None:
    try:
        text = path.read_text()
    except Exception:
        return None

    match = re.search(r'^OPENAI_API_KEY="?([^"\n]+)"?$', text, re.M)
    if not match:
        return None

    value = match.group(1).strip()
    if value and not value.startswith(("REPLACE_", "YOUR_", "sk-xxxxx", "sk-...")):
        return value
    return None


def find_openai_api_key_from_reference_files() -> str | None:
    reference_names = [
        ".openai-api-key-path",
        ".youtube-transcript-openai-key-path",
    ]

    for directory in [Path.cwd(), *Path.cwd().parents]:
        for name in reference_names:
            ref_path = directory / name
            if not ref_path.is_file():
                continue
            try:
                target = ref_path.read_text().strip()
            except Exception:
                continue
            if not target:
                continue

            if target.startswith("sk-"):
                os.environ["OPENAI_API_KEY"] = target
                return target

            candidate = Path(target).expanduser()
            if not candidate.is_absolute():
                candidate = (ref_path.parent / candidate).resolve()
            if candidate.is_file():
                value = parse_openai_key_from_env_file(candidate)
                if value:
                    os.environ["OPENAI_API_KEY"] = value
                    return value

    return None


def find_openai_api_key() -> str | None:
    existing = os.environ.get("OPENAI_API_KEY")
    if existing:
        return existing

    from_reference = find_openai_api_key_from_reference_files()
    if from_reference:
        return from_reference

    preferred_names = [
        ".env.vercel.production.current",
        ".env.local",
        ".env.production",
        ".env.local.prod-backup",
        ".env",
    ]
    excluded_dirs = {
        ".git",
        "node_modules",
        ".next",
        "dist",
        "build",
        ".turbo",
        ".vercel",
    }
    cwd = Path.cwd()

    candidates: list[Path] = []
    for name in preferred_names:
        candidates.extend(path for path in cwd.rglob(name) if not any(part in excluded_dirs for part in path.parts))

    seen: set[Path] = set()
    for path in candidates:
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        value = parse_openai_key_from_env_file(path)
        if value:
            os.environ["OPENAI_API_KEY"] = value
            return value

    return None


def choose_transcript(transcript_list: Any, langs: list[str], prefer_generated: bool) -> Any:
    finders = (
        [transcript_list.find_generated_transcript, transcript_list.find_manually_created_transcript]
        if prefer_generated
        else [transcript_list.find_manually_created_transcript, transcript_list.find_generated_transcript]
    )

    for finder in finders:
        try:
            return finder(langs)
        except Exception:
            continue

    try:
        return transcript_list.find_transcript(langs)
    except Exception:
        pass

    # Fall back to the first available caption track in the requested preference order.
    available = list(transcript_list)
    generated_sorted = sorted(available, key=lambda item: item.is_generated)
    if prefer_generated:
        generated_sorted = sorted(available, key=lambda item: not item.is_generated)
    if generated_sorted:
        return generated_sorted[0]

    raise RuntimeError("No transcript tracks were available for this video.")


def fetch_with_youtube_transcript_api(
    video_id: str,
    langs: list[str],
    translate_to: str | None,
    prefer_generated: bool,
    preserve_formatting: bool,
) -> TranscriptResult:
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)
    transcript = choose_transcript(transcript_list, langs, prefer_generated)

    translated_to = None
    if translate_to and transcript.language_code != translate_to:
        if not transcript.is_translatable:
            raise RuntimeError(
                f"Transcript language {transcript.language_code} is not translatable to {translate_to}.",
            )
        transcript = transcript.translate(translate_to)
        translated_to = translate_to

    fetched = transcript.fetch(preserve_formatting=preserve_formatting)
    snippets = [
        {
            "text": snippet.text.strip(),
            "start": float(snippet.start),
            "duration": float(snippet.duration),
        }
        for snippet in fetched
        if snippet.text.strip()
    ]

    return TranscriptResult(
        input=video_id,
        video_id=video_id,
        source="youtube_transcript_api",
        language_code=fetched.language_code,
        language=fetched.language,
        is_generated=fetched.is_generated,
        translated_to=translated_to,
        snippets=snippets,
        text=build_text(snippets),
    )


def yt_dlp_langs(langs: list[str], translate_to: str | None) -> str:
    targets = [translate_to] if translate_to else langs
    normalized: list[str] = []
    for lang in targets:
        if any(token in lang for token in ("*", ".", "+", "?", "[", "]", "(", ")", "{", "}", "^", "$")):
            normalized.append(lang)
        else:
            normalized.append(f"{lang}.*")
    return ",".join(normalized)


def choose_subtitle_file(files: list[Path], video_id: str, langs: list[str]) -> Path:
    def subtitle_tag(path: Path) -> str:
        match = re.match(rf"^{re.escape(video_id)}\.(.+)$", path.stem)
        return match.group(1) if match else path.stem

    def rank(path: Path) -> tuple[int, int, int, str]:
        tag = subtitle_tag(path).lower()
        for lang_index, lang in enumerate(langs):
            base = lang.lower()
            if tag == f"{base}-orig":
                return (lang_index, 0, len(tag), tag)
            if tag == base:
                return (lang_index, 1, len(tag), tag)
            if tag.startswith(f"{base}-"):
                return (lang_index, 2, len(tag), tag)
        return (len(langs), 9, len(tag), tag)

    return sorted(files, key=rank)[0]


def parse_json3_file(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text())
    snippets: list[dict[str, Any]] = []

    for event in data.get("events", []):
        segs = event.get("segs")
        if not segs:
            continue

        text = "".join(seg.get("utf8", "") for seg in segs)
        text = html.unescape(text).replace("\n", " ").strip()
        text = re.sub(r"\s+", " ", text)
        if not text:
            continue

        start_ms = event.get("tStartMs")
        if start_ms is None:
            continue

        duration_ms = event.get("dDurationMs") or 0
        snippet = {
            "text": text,
            "start": round(float(start_ms) / 1000.0, 3),
            "duration": round(float(duration_ms) / 1000.0, 3),
        }

        if snippets and snippet["text"] == snippets[-1]["text"]:
            continue

        snippets.append(snippet)

    return snippets


def parse_vtt_timestamp(value: str) -> float:
    hours, minutes, seconds = value.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def clean_vtt_text(value: str) -> str:
    value = re.sub(r"<\d{2}:\d{2}:\d{2}\.\d{3}>", "", value)
    value = re.sub(r"</?c[^>]*>", "", value)
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def parse_vtt_file(path: Path) -> list[dict[str, Any]]:
    snippets: list[dict[str, Any]] = []
    lines = path.read_text().splitlines()
    index = 0

    while index < len(lines):
        line = lines[index].strip()
        if "-->" not in line:
            index += 1
            continue

        start_raw, end_raw = line.split("-->", 1)
        start = parse_vtt_timestamp(start_raw.strip())
        end = parse_vtt_timestamp(end_raw.strip().split(" ", 1)[0])
        index += 1

        block_lines: list[str] = []
        while index < len(lines) and lines[index].strip():
            block_lines.append(lines[index])
            index += 1

        text = clean_vtt_text(" ".join(block_lines))
        if text:
            snippet = {
                "text": text,
                "start": round(start, 3),
                "duration": round(max(end - start, 0), 3),
            }
            if not snippets or snippet["text"] != snippets[-1]["text"]:
                snippets.append(snippet)

    return snippets


def infer_language_from_subtitle_tag(path: Path, video_id: str) -> str | None:
    match = re.match(rf"^{re.escape(video_id)}\.([^.]+)$", path.stem)
    if not match:
        return None
    tag = match.group(1)
    if tag.endswith("-orig"):
        return tag[:-5]
    return tag


def fetch_with_yt_dlp_subtitles(
    video_url: str,
    video_id: str,
    langs: list[str],
    translate_to: str | None,
    keep_artifacts: bool,
) -> TranscriptResult:
    with tempfile.TemporaryDirectory() as tmpdir_raw:
        tmpdir = Path(tmpdir_raw)
        lang_patterns: list[str] = [yt_dlp_langs(langs, translate_to)]
        if translate_to:
            lang_patterns.append(yt_dlp_langs(langs, None))
        lang_patterns.append("all,-live_chat")

        subtitle_files: list[Path] = []
        last_detail = "yt-dlp did not produce any subtitle files."
        for attempt_index, lang_pattern in enumerate(dict.fromkeys(lang_patterns)):
            attempt_dir = tmpdir / f"attempt_{attempt_index}"
            attempt_dir.mkdir(parents=True, exist_ok=True)
            cmd = [
                "yt-dlp",
                "--no-update",
                "--no-playlist",
                "--skip-download",
                "--write-subs",
                "--write-auto-subs",
                "--sub-format",
                "json3/vtt/best",
                "--sub-langs",
                lang_pattern,
                "-o",
                str(attempt_dir / "%(id)s.%(ext)s"),
                video_url,
            ]
            completed = subprocess.run(cmd, capture_output=True, text=True)
            subtitle_files = sorted(attempt_dir.glob("*.json3")) or sorted(attempt_dir.glob("*.vtt"))
            if subtitle_files:
                break
            stderr = completed.stderr.strip()
            stdout = completed.stdout.strip()
            last_detail = stderr or stdout or last_detail

        if not subtitle_files:
            raise RuntimeError(last_detail)

        preferred_langs = [translate_to] if translate_to else langs
        subtitle_file = choose_subtitle_file(subtitle_files, video_id, preferred_langs)
        snippets = (
            parse_json3_file(subtitle_file)
            if subtitle_file.suffix == ".json3"
            else parse_vtt_file(subtitle_file)
        )

        if not snippets:
            raise RuntimeError(f"Subtitle file {subtitle_file.name} did not contain transcript text.")

        artifacts_dir = None
        if keep_artifacts:
            persistent_dir = Path(tempfile.mkdtemp(prefix="youtube-transcript-"))
            for artifact in tmpdir.iterdir():
                artifact.rename(persistent_dir / artifact.name)
            artifacts_dir = str(persistent_dir)

        return TranscriptResult(
            input=video_url,
            video_id=video_id,
            source="yt_dlp_subtitles",
            language_code=infer_language_from_subtitle_tag(subtitle_file, video_id),
            language=None,
            is_generated=None,
            translated_to=translate_to,
            snippets=snippets,
            text=build_text(snippets),
            artifacts_dir=artifacts_dir,
        )


def fetch_with_openai_asr(
    video_url: str,
    video_id: str,
    langs: list[str],
    model: str,
    keep_artifacts: bool,
) -> TranscriptResult:
    if not find_openai_api_key():
        raise RuntimeError("OPENAI_API_KEY is not set, and no local .env file with that key was found.")

    from openai import OpenAI

    with tempfile.TemporaryDirectory() as tmpdir_raw:
        tmpdir = Path(tmpdir_raw)
        cmd = [
            "yt-dlp",
            "--no-update",
            "--no-playlist",
            "-x",
            "--audio-format",
            "mp3",
            "--audio-quality",
            "0",
            "-o",
            str(tmpdir / "%(id)s.%(ext)s"),
            video_url,
        ]
        completed = subprocess.run(cmd, capture_output=True, text=True)
        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip() or "yt-dlp audio extraction failed."
            raise RuntimeError(detail)

        audio_files = sorted(
            [
                path
                for path in tmpdir.iterdir()
                if path.is_file() and path.suffix.lower() in {".mp3", ".m4a", ".wav", ".webm", ".mp4", ".mpeg", ".mpga"}
            ],
        )
        if not audio_files:
            raise RuntimeError("yt-dlp completed but no audio file was found for transcription.")

        audio_path = audio_files[0]
        client = OpenAI()
        language_hint = langs[0].split("-", 1)[0] if langs else None
        with audio_path.open("rb") as audio_file:
            response = client.audio.transcriptions.create(
                file=audio_file,
                model=model,
                language=language_hint,
                response_format="json",
            )

        if hasattr(response, "model_dump"):
            payload = response.model_dump()
        elif isinstance(response, dict):
            payload = response
        else:
            payload = {"text": str(response)}

        segments = payload.get("segments") or []
        snippets = [
            {
                "text": segment["text"].strip(),
                "start": float(segment.get("start", 0.0)),
                "duration": round(float(segment.get("end", 0.0)) - float(segment.get("start", 0.0)), 3),
            }
            for segment in segments
            if segment.get("text", "").strip()
        ]
        if not snippets and payload.get("text"):
            snippets = [{"text": payload["text"].strip(), "start": 0.0, "duration": 0.0}]

        artifacts_dir = None
        if keep_artifacts:
            persistent_dir = Path(tempfile.mkdtemp(prefix="youtube-transcript-"))
            for artifact in tmpdir.iterdir():
                artifact.rename(persistent_dir / artifact.name)
            artifacts_dir = str(persistent_dir)

        return TranscriptResult(
            input=video_url,
            video_id=video_id,
            source="openai_asr",
            language_code=payload.get("language") or language_hint,
            language=payload.get("language"),
            is_generated=None,
            translated_to=None,
            snippets=snippets,
            text=payload.get("text", build_text(snippets)).strip(),
            artifacts_dir=artifacts_dir,
        )


def write_outputs(result: TranscriptResult, args: argparse.Namespace) -> None:
    json_text = json.dumps(result.to_dict(), indent=2, ensure_ascii=False)
    text_output = text_with_timestamps(result.snippets) if args.timestamps else result.text

    if args.json_out:
        ensure_parent(args.json_out).write_text(json_text + "\n")
    if args.text_out:
        ensure_parent(args.text_out).write_text(text_output + "\n")

    if args.format == "json":
        print(json_text)
    else:
        print(text_output)


def main() -> int:
    args = parse_args()
    if args.force_asr:
        args.fallback_asr = True
    langs = split_langs(args.langs)
    video_id = extract_video_id(args.input)
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    errors: list[str] = []
    strategies: list[tuple[str, Any]] = []

    if not args.force_asr:
        strategies.extend([
            ("youtube_transcript_api", lambda: fetch_with_youtube_transcript_api(
                video_id=video_id,
                langs=langs,
                translate_to=args.translate_to,
                prefer_generated=args.prefer_generated,
                preserve_formatting=args.preserve_formatting,
            )),
            ("yt_dlp_subtitles", lambda: fetch_with_yt_dlp_subtitles(
                video_url=video_url,
                video_id=video_id,
                langs=langs,
                translate_to=args.translate_to,
                keep_artifacts=args.keep_artifacts,
            )),
        ])

    if args.fallback_asr:
        strategies.append(
            ("openai_asr", lambda: fetch_with_openai_asr(
                video_url=video_url,
                video_id=video_id,
                langs=langs,
                model=args.asr_model,
                keep_artifacts=args.keep_artifacts,
            )),
        )

    for strategy_name, strategy in strategies:
        try:
            result = strategy()
            if strategy_name == "youtube_transcript_api" and args.keep_artifacts:
                result.artifacts_dir = None
            result.input = args.input
            write_outputs(result, args)
            return 0
        except Exception as exc:
            errors.append(f"{strategy_name}: {exc}")

    print("Failed to retrieve a transcript.\n", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    if not args.fallback_asr:
        print("\nTry rerunning with --fallback-asr if you want a billable best-effort transcription.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
