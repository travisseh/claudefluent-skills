---
name: grain-testimonials
description: "Extract potential testimonials from Grain recording pages and save them to ClaudeFluent participant records in Convex. Use when Travisse wants to pull testimonials, extract Grain feedback, or save participant quotes after a ClaudeFluent session."
---

# Grain Testimonials Extractor

Extract potential testimonials from Grain recording pages and save them to ClaudeFluent participant records in Convex.

## When to use
- After a ClaudeFluent course session, when Grain recording links are available
- When Travisse says "pull testimonials" or "extract testimonials"

## Prerequisites
- Grain share URL(s) for the session
- The session's `sessionId` in Convex (e.g., `saturday5`)

## Workflow

### Step 1: Get the Grain page content

Use `$dev-browser` to open the Grain share URL. The page is fully client-side rendered, so do not rely on plain HTTP fetches for the content.

1. Navigate to the Grain share URL
2. Wait for content to load
3. Click the **Summary** tab if visible (it has structured, speaker-attributed notes)
4. Extract the relevant page text using locators, `textContent`, or `snapshotForAI`

Focus on the **"Course Feedback and Next Steps"** section — this is where participants share what they found most useful (Travisse asks this at the end of every session).

### Step 2: Identify participants for the session

```bash
curl -s "https://polite-toad-76.convex.cloud/api/query" \
  -H "Content-Type: application/json" \
  -d '{"path":"participants:getBySessionId","args":{"sessionId":"SESSION_ID"}}' \
  | python3 -c "import json,sys; [print(f\"{p['_id']} | {p['name']} | {p['email']}\") for p in json.load(sys.stdin).get('value',[])]"
```

### Step 3: Extract testimonial quotes

From the Grain page text, identify quotes or paraphrased statements from **participants only** (NOT Travisse Hansen, the instructor). Focus on:
- What they found most useful or valuable
- Positive feedback about the course, exercises, or teaching
- Specific outcomes or "aha moments"
- Statements about recommending the course

For each testimonial, note:
- **quote**: Exact quote or close paraphrase using their actual words
- **speaker**: Participant's full name
- **context**: Brief context like "end-of-session feedback"

### Step 4: Save to Convex

For each participant who has testimonials, call the `updateTestimonials` mutation:

```bash
curl -s -X POST "https://polite-toad-76.convex.cloud/api/mutation" \
  -H "Content-Type: application/json" \
  -d '{
    "path":"participants:updateTestimonials",
    "args":{
      "participantId":"PARTICIPANT_CONVEX_ID",
      "testimonials":[
        {
          "quote":"The exact quote here",
          "speaker":"Participant Name",
          "context":"end-of-session feedback",
          "extractedAt":TIMESTAMP_MS
        }
      ]
    }
  }'
```

Use `Date.now()` equivalent for `extractedAt` (current timestamp in milliseconds).

### Step 5: Report results

Tell Travisse how many testimonials were found and saved, grouped by participant.

## Schema reference

The `potentialTestimonials` field on participants:
```
potentialTestimonials: optional array of {
  quote: string,
  speaker: string,
  context: optional string,
  extractedAt: number (timestamp ms)
}
```

## Tips
- The last Grain link for a session is typically the second/final class — this has the best feedback content
- If there are 2 Grain links (Part 1 and Part 2), focus on Part 2
- The Summary tab is usually sufficient — you rarely need the full Transcript tab
- Skip anything Travisse says — only extract participant quotes
