---
name: record-demo
description: Record a real step-by-step product walkthrough in Tella and return the final clip URL. Use when the user asks for a demo video, screen recording, Tella link, feature walkthrough recording, or when a task explicitly needs a product demo after implementation.
---

# Record Demo

Use Tella to record the actual flow, not a fake wrapper flow.

## When To Use

Use this skill when:
- the user asks for a demo video or screen recording
- a task says to record a walkthrough after making a change
- you need a Tella link to attach back to Notion or elsewhere

Do not use this for static screenshots or when no walkthrough is needed.

## Tooling

Use the shared Tella helper script:

```bash
npx tsx ~/Programming/personal-master/personal/scripts/tella-demo.ts start
npx tsx ~/Programming/personal-master/personal/scripts/tella-demo.ts stop
```

`stop` returns the final Tella clip URL.

## Required Flow

1. Get the product into the state you want to demonstrate.
2. Start Tella immediately before the walkthrough:

```bash
npx tsx ~/Programming/personal-master/personal/scripts/tella-demo.ts start
```

3. Perform the real walkthrough step by step using normal tools:
- browser automation
- local app testing
- clicking through the actual UI
- whatever you would normally do to verify the feature

4. Stop Tella immediately after the walkthrough:

```bash
npx tsx ~/Programming/personal-master/personal/scripts/tella-demo.ts stop
```

5. Capture and return the Tella URL.

## Rules

- Record the real flow, not a synthetic one-line command unless the task truly is one command.
- Keep the walkthrough tight and intentional.
- If the walkthrough needs setup time, do the setup before starting Tella when possible.
- If the flow fails mid-demo, stop recording, fix the issue, and record again.
- If Tella returns a URL, treat that as the source of truth.

## Output

Always include:
- the Tella URL
- one sentence saying what the demo shows

If the recording fails:
- say exactly where it failed
- do not pretend a demo exists
