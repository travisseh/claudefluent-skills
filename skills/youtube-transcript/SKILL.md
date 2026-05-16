---
name: youtube-transcript
description: Pull transcripts from YouTube videos with a caption-first workflow and optional OpenAI ASR fallback. Use when Codex needs a transcript, subtitles, timestamped text, or clean text from a YouTube URL or video ID; when summarizing or analyzing a YouTube video; or when a user says "get the transcript", "pull captions", "download subtitles", "transcribe this YouTube video", or "grab the text from this video".
---

# YouTube Transcript

Use the canonical helper at:

`~/.codex/skills/youtube-transcript/scripts/fetch_youtube_transcript.py`

This repo includes `.openai-api-key-path` at the repo root, so the helper can find an OpenAI key here without exporting it in the shell.

## Quick Start

Plain text:

```bash
uv run --with youtube-transcript-api python \
  ~/.codex/skills/youtube-transcript/scripts/fetch_youtube_transcript.py \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

JSON with timestamps:

```bash
uv run --with youtube-transcript-api python \
  ~/.codex/skills/youtube-transcript/scripts/fetch_youtube_transcript.py \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  --format json
```

Force OpenAI ASR:

```bash
uv run --with youtube-transcript-api --with openai python \
  ~/.codex/skills/youtube-transcript/scripts/fetch_youtube_transcript.py \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  --force-asr
```

## Notes

- Default order is transcript API, then `yt-dlp` subtitle fallback, then OpenAI ASR if requested.
- `--fallback-asr` tries ASR only after caption paths fail.
- `--force-asr` skips caption retrieval and goes straight to audio transcription.
- `--timestamps`, `--translate-to`, `--langs`, `--text-out`, and `--json-out` are supported by the helper.
