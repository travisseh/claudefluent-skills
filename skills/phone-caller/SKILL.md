---
name: phone-caller
description: "Make outbound AI phone calls via Bland.ai to schedule appointments, get quotes, or handle business calls on Travisse's behalf. Use when he asks to 'call this place', 'schedule an appointment', 'get a quote from', 'phone call', or wants to contact a business by phone. Also trigger when texting a business didn't get a response and a call is needed."
---

# Phone Caller

Make outbound AI phone calls using Bland.ai. The AI agent calls the business, has a natural conversation, and returns a summary + transcript.

## Prerequisites

- `BLAND_API_KEY` in `.env` (get one at https://app.bland.ai)
- `jq` and `curl` installed

## How to Use

### 1. Build the task prompt

Write a natural language task that tells the AI caller:
- Who it's calling on behalf of ("Travisse Hansen")
- What it needs (appointment, quote, availability check)
- Key details (property address, what's broken, preferred times)
- What info to collect (cost, availability, next steps)

### 2. Make the call

```bash
bash .claude/skills/phone-caller/scripts/call.sh \
  "+18012850268" \
  "You are calling on behalf of Travisse Hansen. He has a rental property at 1313 S 1540 E, Provo UT 84606 and needs a garage door repair. The garage door needs to be looked at. Ask about their availability this week or next, get a cost estimate for a service call, and confirm what information they need from the homeowner." \
  "josh" \
  10
```

**Parameters:**
1. Phone number (E.164 format with +1)
2. Task/instructions for the AI caller
3. Voice (optional, default "josh") - options: josh, florian, derek, june, nat, paige
4. Max duration in minutes (optional, default 10)

### 3. Read results

The script polls until the call completes and returns:
- **status**: completed, failed, no-answer, busy
- **summary**: AI-generated summary of what happened
- **concatenated_transcript**: Full conversation text
- **call_length**: Duration in minutes
- **price**: Cost of the call
- **recording_url**: Link to the audio recording

## Common Use Cases

### Schedule a repair
```bash
bash .claude/skills/phone-caller/scripts/call.sh "+18015551234" \
  "You are calling on behalf of Travisse Hansen to schedule a garage door repair at 1313 S 1540 E, Provo UT. Ask about availability this week, cost for a service call, and what they need from the homeowner."
```

### Get a cleaning quote
```bash
bash .claude/skills/phone-caller/scripts/call.sh "+18015551234" \
  "You are calling on behalf of Travisse Hansen to get a quote for carpet cleaning at a 4 bedroom house at 1313 S 1540 E, Provo UT 84606. Ask about pricing, availability, and how long the job typically takes."
```

### General inquiry
```bash
bash .claude/skills/phone-caller/scripts/call.sh "+18015551234" \
  "You are calling on behalf of Travisse Hansen. [describe what you need]. Be polite and professional. Get their availability and pricing."
```

## Pricing

Bland.ai free tier: $0.14/min, 100 calls/day. A typical 3-5 minute business call costs ~$0.42-$0.70.

## After the call

- Present the summary and transcript to Travisse
- If an appointment was scheduled, add it to the appropriate calendar
- If a follow-up is needed, note the next steps
- Send Travisse an iMessage summary if he's not actively in the conversation
