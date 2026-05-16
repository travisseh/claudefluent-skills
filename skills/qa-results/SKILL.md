---
name: qa-results
description: Query the Supabase solv-mock database to analyze QA booking outcomes, pass/fail rates, failure patterns, and per-student progress. Use when checking test results, QA outcomes, failures, or booking data.
---

# QA Results

Query the Supabase database to analyze booking outcomes from QA automation runs. Surfaces pass/fail rates, failure patterns, and per-student progress.

## When to Use

When the user says "check results", "show QA outcomes", "how did the tests go", "what failed", "show me the data", or wants to analyze booking data across students.

## Connection

Use the Supabase MCP to query the solv-mock database.

Project ID: `ncqpcjoignqxmkgiiiiq`
Tables: `students`, `patients`, `bookings`

## Schema

**students:** id (uuid), name (text), cookie_token (text), created_at (timestamptz)

**patients:** id (uuid), student_id (FK→students), first_name, last_name, date_of_birth, phone, email, insurance_plan, member_id, group_number, insurance_card_uploaded (bool), created_at

**bookings:** id (uuid), patient_id (FK→patients), student_id (FK→students), booking_ref (text), slot_time, reason, appointment_type, status, eligibility_status, eligibility_reason, ehr_sync_status, ehr_sync_reason, intake_complete (bool), created_at

## Reports

### 1. Summary Report (default)

When the user just says "check results" or "how did it go", run this:

```sql
SELECT
  s.name AS student,
  COUNT(*) AS total_bookings,
  COUNT(*) FILTER (WHERE b.status = 'checked_in') AS passed,
  COUNT(*) FILTER (WHERE b.status != 'checked_in') AS failed,
  ROUND(100.0 * COUNT(*) FILTER (WHERE b.status = 'checked_in') / COUNT(*), 1) AS pass_rate
FROM students s
JOIN bookings b ON b.student_id = s.id
GROUP BY s.name
ORDER BY total_bookings DESC
```

### 2. Failure Breakdown

When the user asks "what failed" or "show failures":

```sql
SELECT
  p.first_name || ' ' || p.last_name AS patient,
  b.booking_ref,
  b.eligibility_status,
  b.eligibility_reason,
  b.ehr_sync_status,
  b.ehr_sync_reason,
  s.name AS student
FROM bookings b
JOIN patients p ON p.id = b.patient_id
JOIN students s ON s.id = b.student_id
WHERE b.eligibility_status = 'failed' OR b.ehr_sync_status = 'failed'
ORDER BY b.created_at DESC
```

### 3. Expected vs Actual

When the user asks "did everything match" or "validate results", compare against expected outcomes:

```sql
SELECT
  p.first_name || ' ' || p.last_name AS patient,
  p.insurance_plan,
  p.member_id,
  p.date_of_birth,
  b.slot_time,
  b.eligibility_status,
  b.eligibility_reason,
  b.ehr_sync_status,
  b.ehr_sync_reason,
  b.status
FROM bookings b
JOIN patients p ON p.id = b.patient_id
ORDER BY b.created_at DESC
```

Then compare each row against these expected failures:
- insurance_plan ILIKE '%expired%' or '%lapsed%' → eligibility should be 'failed'
- insurance_plan ILIKE '%unknown%' → eligibility should be 'failed'
- LENGTH(member_id) < 5 → eligibility should be 'failed'
- date_of_birth not matching YYYY-MM-DD pattern → ehr_sync should be 'failed'
- first_name or last_name contains non-ASCII or apostrophes → ehr_sync should be 'failed'
- slot_time contains '13:00' → ehr_sync should be 'failed'
- All others → both should pass, status should be 'checked_in'

Flag any mismatches as potential bugs.

### 4. Per-Student Detail

When the user asks about a specific student:

```sql
SELECT
  p.first_name || ' ' || p.last_name AS patient,
  b.booking_ref,
  b.status,
  b.eligibility_status,
  b.ehr_sync_status,
  b.intake_complete,
  b.created_at
FROM bookings b
JOIN patients p ON p.id = b.patient_id
JOIN students s ON s.id = b.student_id
WHERE s.name ILIKE '%STUDENT_NAME%'
ORDER BY b.created_at
```

## Behavior

1. Default to the summary report unless the user asks for something specific.
2. After showing results, highlight anything unexpected — mismatches between expected and actual outcomes, students with 0 bookings, or missing failure types.
3. If no data exists yet, say so and suggest running the booking-qa skill first.
4. Format output as clean markdown tables when possible.
