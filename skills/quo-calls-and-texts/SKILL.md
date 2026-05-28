---
name: quo-calls-and-texts
description: >
  This skill should be used when the user asks to search, sync, fetch, or query
  Quo/OpenPhone calls, texts, customer messages, conversations, call recordings,
  call transcripts, call summaries, or OpenPhone API endpoints.
---

# Quo Calls and Texts Skill

Provide knowledge about the Quo (formerly OpenPhone) REST API and local data access patterns for querying, syncing, and exploring customer texts, conversations, call recordings, transcripts, and summaries.

## API Fundamentals

- **Base URL:** `https://api.openphone.com/v1`
- **Auth:** API key in `Authorization` header (raw key, no Bearer prefix)
- **Rate limit:** 10 requests/second per key; HTTP 429 on excess
- **Pagination:** Cursor-based via `pageToken`/`nextPageToken`; max 100 per page
- **Known bug:** `totalItems` field is inaccurate — always paginate until `nextPageToken` is null

## Core Data Model

### Conversations and Texts
Conversations are the entry point for day-to-day customer text messages. They include `phoneNumberId` and `participants`, and message bundles include text bodies, timestamps, sender/recipient context, and conversation metadata. Use messages when the user asks about customer texts, support conversations, quick support interactions, or ongoing follow-up threads.

### Calls
Identify calls by `AC`-prefixed IDs. Key fields: `id`, `phoneNumberId`, `userId`, `direction` (incoming/outgoing), `status`, `participants` (E.164 array), `duration` (seconds), `createdAt`, `answeredAt`, `completedAt`.

### Recordings
Fetch per call via `GET /v1/call-recordings/{callId}`. Returns array of segments with `id`, `duration`, `startTime`, `status`, `type` (audio/mpeg), `url` (download link). Download promptly — URLs may be signed and time-limited. The `url` field may be null if recording is not yet processed or has been deleted.

### Transcripts (Business/Scale plans)
Fetch via `GET /v1/call-transcripts/{callId}`. Returns `dialogue[]` with `content`, `start`, `end`, `identifier` (phone number), `userId`. Speaker-labeled and time-coded.

### Summaries (Business/Scale plans)
Fetch via `GET /v1/call-summaries/{callId}`. Returns AI-generated call summary.

## Enumeration Pattern

Use conversations as the entry point for both texts and calls. The `/v1/calls` endpoint requires a `participants` filter (E.164 array, limited to 1), so conversations are also how to discover call participants without knowing them upfront:

1. List conversations (`GET /v1/conversations`) — returns `phoneNumberId` and `participants` for each
2. For text searches, fetch messages for matching conversations
3. For call searches, list calls (`GET /v1/calls?phoneNumberId=PNxxx&participants[]=+1...`)
4. Fetch per-call data (recordings, transcript, summary)

Conversations support `updatedAfter`/`updatedBefore` filters for incremental sync.

**Important:** A `User-Agent` header is required — Cloudflare blocks Python's default urllib agent.

## Library Interface

`QuoClient` in `/Users/you/Programming/product2/quo/scripts/lib/quo_client.py` exposes high-level iterators that encapsulate the conversation→participant→calls/messages discovery pattern:

- **`iter_calls(since, until, phone_number_id, skip_ids, enrich)`** — Yields enriched call records (call + recordings + transcript + summary + synced_at). Handles pagination, dedup, and rate limiting.
- **`iter_messages(since, until, phone_number_id, skip_conversation_ids)`** — Yields conversation message bundles.
- **`enrich_call(call)`** — Fetch recordings, transcript, and summary for a single call.

Callers decide where to store data. The quo plugin does not store user data internally.

## Available Scripts

The Quo plugin root is `/Users/you/Programming/product2/quo`. Run scripts from that directory:

- **`python3 scripts/fetch-calls.py`** — Fetch calls via iterators; outputs JSONL to stdout or `--output-dir`
- **`python3 scripts/fetch-messages.py`** — Fetch messages via iterators; outputs JSONL to stdout or `--output-dir`
- **`python3 scripts/query-calls.py`** — Search and filter call data from a `--data-dir`
- **`python3 scripts/explore-api.py`** — Direct API queries (phone numbers, users, contacts, calls, transcripts)

For broad customer-intel questions, fetch both calls and messages for the requested time range, then search both output directories before synthesizing evidence.

## Additional Resources

### Reference Files
- **`references/api-endpoints.md`** — Complete endpoint reference with request/response schemas, status enumerations, error codes, and API version history

### Expertise File
- **`expertise/quo-api.yaml`** — Structured YAML domain knowledge: ID prefixes, plan restrictions, enumeration order, recording format details. Updated via `/quo:self-improve`.
