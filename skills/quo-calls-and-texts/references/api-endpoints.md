# Quo API Endpoint Reference

Base URL: `https://api.openphone.com/v1`

## Phone Numbers

### GET /v1/phone-numbers
List all phone numbers in the workspace.

**Response:** `{ "data": [{ "id": "PNxxx", ... }] }`

Phone number IDs (`PN`-prefixed) are required for listing calls.

## Calls

### GET /v1/calls
List calls for a phone number.

**Required params:**
- `phoneNumberId` (string, `^PN(.*)$`)
- `participants` (E.164 array, **required**, currently limited to 1 item) — the external phone number(s). Encode as `participants[]=+1...`
- `maxResults` (1-100, default 10)

**Optional params:**
- `createdAfter` (ISO 8601 datetime — must include time, e.g. `2025-01-01T00:00:00Z`)
- `createdBefore` (ISO 8601 datetime)
- `userId` (string, `^US(.*)$`)
- `pageToken` (string)

**Important:** `participants` is required. To discover participants, use the conversations endpoint first.

**Response:**
```json
{
  "data": [{
    "id": "AC123abc",
    "phoneNumberId": "PN123abc",
    "userId": "US123abc",
    "direction": "incoming",
    "status": "completed",
    "participants": ["+15555555555"],
    "duration": 60,
    "createdAt": "2022-01-01T00:00:00Z",
    "answeredAt": "2022-01-01T00:00:00Z",
    "completedAt": "2022-01-01T00:00:00Z"
  }],
  "totalItems": 100,
  "nextPageToken": "..."
}
```

**Note:** `totalItems` is known to be inaccurate. Paginate until `nextPageToken` is null.

### GET /v1/calls/{id}
Get a single call by ID.

## Recordings

### GET /v1/call-recordings/{callId}
Get recording segments for a call. Sorted chronologically (oldest first).

**Response:**
```json
{
  "data": [{
    "id": "CRwRVK2qBq",
    "duration": 60,
    "startTime": "2022-01-01T00:00:00Z",
    "status": "completed",
    "type": "audio/mpeg",
    "url": "https://storage.example.com/recording.mp3"
  }]
}
```

**Recording status values:** `absent`, `completed`, `deleted`, `failed`, `in-progress`, `paused`, `processing`, `stopped`, `stopping`

**Important:** The `url` field may be null (recording not ready or deleted) and may be time-limited (signed URL). Download promptly.

## Transcripts

### GET /v1/call-transcripts/{callId}
Get the transcript for a call. **Requires Business or Scale plan.**

**Response:**
```json
{
  "data": {
    "callId": "ACxxx",
    "createdAt": "2022-01-01T00:00:00Z",
    "dialogue": [{
      "content": "Hello, world!",
      "start": 5.123,
      "end": 10.123,
      "identifier": "+19876543210",
      "userId": "US123abc"
    }],
    "duration": 100,
    "status": "completed"
  }
}
```

**Transcript status values:** `absent`, `in-progress`, `completed`, `failed`

## Summaries

### GET /v1/call-summaries/{callId}
Get the AI-generated summary for a call. **Requires Business or Scale plan.**

## Conversations

### GET /v1/conversations
List conversations. Key entry point for discovering call participants.

**Required params:**
- `maxResults` (1-100, default 10)

**Optional params:**
- `phoneNumbers` (array of E.164 or PN IDs, 1-100 items)
- `userId` (string)
- `createdAfter` / `createdBefore` (ISO 8601 datetime)
- `updatedAfter` / `updatedBefore` (ISO 8601 datetime)
- `excludeInactive` (boolean)
- `pageToken` (string)

**Response:**
```json
{
  "data": [{
    "id": "CNxxx",
    "phoneNumberId": "PNxxx",
    "participants": ["+15555555555"],
    "lastActivityAt": "2022-01-01T00:00:00Z",
    "lastActivityId": "ACxxx",
    "createdAt": "2022-01-01T00:00:00Z",
    "updatedAt": "2022-01-01T00:00:00Z"
  }],
  "totalItems": 50,
  "nextPageToken": "..."
}
```

**Note:** Defaults to all conversations in the workspace, ordered newest first. Use `updatedAfter` for incremental sync.

## Users

### GET /v1/users
List workspace users.

## Contacts

### GET /v1/contacts
List contacts (added in v1.2.0, January 2025).

## Webhooks

### POST /v1/webhooks
Create a webhook subscription.

### GET /v1/webhooks
List webhook subscriptions.

### DELETE /v1/webhooks/{id}
Delete a webhook.

**Webhook event types:**
- `call.ringing` — Call begins ringing
- `call.completed` — Call ends
- `call.recording.completed` — Recording finishes processing
- `call.transcript.completed` — Transcript ready
- `call.summary.completed` — Summary ready
- `message.received` — Inbound message
- `message.delivered` — Outbound message delivered

## Error Codes

| HTTP | Meaning |
|------|---------|
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized (missing/invalid API key) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Resource not found |
| 429 | Rate limited (10 req/s exceeded) |
| 500 | Server error |

## API Version History

- **v1.0.0** (Oct 21, 2024): Public API launch
- **v1.0.2** (Nov 4, 2024): Fixed recordings endpoint returning empty arrays
- **v1.1.2** (Dec 6, 2024): Fixed nextPageToken; totalItems known inaccurate
- **v1.2.0** (Jan 22, 2025): Added contacts endpoint, externalId on contacts
