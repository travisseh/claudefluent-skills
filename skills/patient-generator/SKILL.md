---
name: patient-generator
description: Generate realistic test patient data for the Baby Solv mock booking system. Use when creating patients, test data, insurance scenarios, booking payloads, or failure cases for the mock booking API.
---

# Patient Generator

Generate realistic test patient data for the Baby Solv mock booking system. Output JSON ready to POST to the booking API.

## When to Use

When the user says "generate a patient", "create test data", "patient with expired insurance", or describes a failure scenario they want to test.

## API Endpoint

POST https://solv-mock.vercel.app/api/bookings

Required fields: `location_id`, `first_name`, `last_name`, `phone`, `reason`, `slot_time`

## Output Format

```json
{
  "location_id": "gLXje2",
  "first_name": "...",
  "last_name": "...",
  "date_of_birth": "YYYY-MM-DD",
  "phone": "...",
  "email": "...",
  "insurance_plan": "...",
  "member_id": "...",
  "group_number": "...",
  "reason": "...",
  "slot_time": "2026-04-23T09:00:00",
  "appointment_type": "urgent_care"
}
```

## Failure Triggers

The mock system uses deterministic rules. To trigger a specific failure, use these data patterns:

**Eligibility failures:**
- Insurance plan containing "expired" or "lapsed" → "Insurance plan is expired or lapsed"
- Insurance plan containing "unknown" or empty string → "Insurance plan not recognized"
- Member ID shorter than 5 characters (e.g. "AET") → "Member ID is too short — likely invalid"

**EHR sync failures:**
- Patient name with special characters: apostrophes (O'Brien), accents (Muñoz), or non-ASCII → "EHR sync failed: special characters in patient name"
- Invalid date_of_birth (not matching YYYY-MM-DD, e.g. "not-a-date" or "") → "EHR sync failed: invalid date of birth format"

**System errors:**
- Slot time containing "13:00" (1:00 PM) → "Booking failed: 1:00 PM slot is blocked for system maintenance"

**Passing bookings:**
- Use a recognized plan (Aetna PPO, Cigna HMO, United Healthcare, Anthem Blue Cross, Kaiser Permanente, Medicare Part B)
- Member ID 5+ characters
- Valid YYYY-MM-DD date of birth
- ASCII-only name with no apostrophes or quotes
- Any slot except 1:00 PM

## Available Time Slots

All on 2026-04-23: 09:00, 09:30, 10:00, 10:30, 11:00, 13:00, 13:30, 14:00, 14:30, 15:00

## Behavior

1. If the user specifies a scenario (e.g. "expired insurance"), generate a patient that triggers that specific failure while keeping all other fields realistic.
2. If the user asks for a batch (e.g. "generate 5 patients"), create a mix of passing and failing patients across different failure types. Use different time slots for each.
3. If the user asks for a "passing" or "clean" patient, ensure no failure triggers are present.
4. Always use realistic American names, valid phone numbers (415555XXXX format), and plausible email addresses.
5. After generating, offer to POST the data to the API. If the user has a student_token cookie, include it in the request.
