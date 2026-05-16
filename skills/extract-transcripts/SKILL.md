---
name: extract-transcripts
description: Extract AskElephant transcripts with custom filters (time range, participants, duration, etc.). Use when needing to pull meeting transcripts from AskElephant.ai for analysis. Trigger with '/extract-transcripts' followed by filter criteria.
---

# Extract AskElephant Transcripts

Extract meeting transcripts from AskElephant.ai with custom filtering criteria.

## What it does

1. Checks if AUTH_TOKEN is valid (refreshes if needed)
2. Creates/modifies the extraction script based on your filters
3. Runs the extraction to generate markdown transcript files
4. Saves transcripts to `./transcripts/` directory

## How to use

Invoke with specific instructions about what transcripts to extract:

```
/extract-transcripts last 30 days with external participants
```

```
/extract-transcripts Jackson Call meetings over 20 minutes from January
```

```
/extract-transcripts Kole Minnoch sales calls with duration > 15 minutes
```

```
/extract-transcripts all meetings with "launch prep" in the title
```

## Supported Filters

**Time Range:**
- "last X days/weeks/months"
- "from [date] to [date]"
- "in January", "this week", etc.

**Participants:**
- Name search: "Jackson Call", "Kole Minnoch", etc.
- "with external participants" (non-exampleco.com)
- "internal only" (exampleco.com only)

**Duration:**
- "over X minutes"
- "duration > X"
- "longer than X minutes"

**Keywords:**
- "with 'keyword' in title"
- "containing 'phrase'"

**Meeting Type:**
- "sales calls"
- "launch prep"
- "marketing meetings"

## Output

Transcripts are saved as markdown files in:
`./transcripts/[date]-[sanitized-title].md`

Each file includes:
- Meeting title and date
- Duration and participants with emails
- Full conversation transcript with timestamps
- Engagement ID for reference

## Examples

**Extract recent sales calls with external customers:**
```
/extract-transcripts last 2 weeks, external participants, Jackson or Kole, over 10 minutes
```

**Extract all onboarding calls:**
```
/extract-transcripts "launch prep" in title, last 30 days
```

**Extract long strategy meetings:**
```
/extract-transcripts over 45 minutes, last month
```

**Extract specific person's calls:**
```
/extract-transcripts Kole Minnoch meetings, external participants, last week
```

## Requirements

- Valid AUTH_TOKEN in `.env` file
- Use `/get-askelephant-token` if token is expired
- Node.js and TypeScript must be installed

## Tips

- Token expires after ~1 hour - refresh with `/get-askelephant-token` if extraction fails
- Transcripts are saved as markdown for easy reading and analysis
- Use these transcripts to analyze:
  - Common customer objections
  - Successful sales patterns
  - Feature requests and feedback
  - Competitor mentions
  - Pricing discussions
- Feed transcripts into Claude or other AI tools for deeper analysis

## Implementation

The skill will:
1. Parse your natural language instructions into filter criteria
2. Modify the `extract-filtered.ts` script or generate a new one
3. Run the extraction with appropriate GraphQL queries
4. Handle pagination and API errors gracefully
5. Format output as clean markdown files
