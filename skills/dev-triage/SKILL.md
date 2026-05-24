---
name: dev-triage
description: >
  Triage Dev Triage Linear issues by reading the Linear board, checking
  for ENG duplicates, identifying the account/location from the request,
  investigating production production data with the v2-database skill, inspecting the
  product repo, and deciding whether each issue is a bug, feature request,
  misunderstanding, data question, duplicate, or support-solvable workaround. Use
  when asked to process, clean up, resolve, investigate, or comment on Example Company
  Dev Triage issues.
---

# Dev Triage

Use this skill to reduce Dev Triage issues to the cheapest correct
outcome. Do not assume every ticket needs engineering work. Prefer resolving
with a clear answer, duplicate link, support action, or narrowed feature request
when that is enough.

## Required Inputs And Tools

- Use the Linear app/tools to inspect the Dev Triage board and issues.
- Use the `v2-database` skill for production production account, location, contact,
  campaign, messaging, widget, tapcard, TFV, and activity evidence.
- Inspect the local product repo before claiming a bug is likely code-backed.
- Use Chrome and Computer Use only when interactive verification is needed.
- Use the `imessage` skill only when testing requires a real iMessage/SMS
  interaction, opt-in, or message receipt check.

Default DB posture is read-only. Never mutate production data unless the user
explicitly asks for a specific write.

## Board Workflow

1. List Dev Triage issues and select the requested scope: all open items, a
   subset, or a single ticket.
2. For each issue, fetch title, description, comments, attachments, status,
   labels, assignee, related issues, and project links.
3. Identify the likely account and location from the request. Look for explicit
   names, URLs, phone numbers, sender numbers, contact names, screenshots,
   campaign names, user emails, or support comments.
4. Search Linear for duplicates in the ENG project before deeper work. Search
   by customer/account name, location name, feature area, main error text, and
   normalized symptom. If a duplicate exists, comment with the duplicate link
   and recommend closing or linking the triage issue.
5. Classify the issue before investigating too deeply:
   - `Confirmed bug`
   - `Likely bug, needs repro/detail`
   - `Feature request`
   - `Data question`
   - `Misunderstanding / expected behavior`
   - `Duplicate`
   - `Needs support clarification`
6. Gather the minimum evidence needed to support the classification.
7. Add a concise Linear comment with evidence, impact, and recommended next
   action. Do not create or modify implementation tickets unless the user asks
   or the workflow clearly requires it.

## Account And Location Identification

Answer this explicitly for every issue:

```text
Account/location identified: Yes/No/Partial
```

If partial or no, state exactly what is missing and ask the support for the smallest
specific detail, such as account name, location name, customer phone/email,
campaign name, widget URL, or screenshot timestamp.

Useful production lookup patterns:

- Search accounts and locations by fuzzy name.
- Search users by email or phone.
- Search contacts by phone, email, or name within the suspected location.
- Search sender numbers, TFV records, subscribe widgets, subscribe links,
  touchpoints, or campaigns when those are the reported surface.

## Data Investigation

Use read-only SQL through `v2-database`. Keep queries narrow and include
customer/account filters whenever possible.

For bugs, determine:

- Is the condition present now or was it temporary?
- When did it start and, if applicable, stop?
- Is it isolated to the reported account/location/contact or affecting others?
- Which records prove the current state?
- Are there related errors, failed campaigns, missing sender numbers, widget
  events, opt-in states, integration statuses, or deleted records?

For data questions, answer the actual question and provide the query-backed
reasoning. If the issue can be closed with an answer, say so.

For support-solvable workarounds, name the manual action clearly. Examples:

- Move the customer from legacy webform to the production subscribe widget.
- Update a missing/misconfigured location setting.
- Ask for the exact contact phone/email or screenshot timestamp.
- Use an existing admin workflow instead of requesting a code change.

## Repo Investigation

Inspect the product repo to connect symptoms to implementation. Use `rg` first.

Look for:

- Routes, server actions, API handlers, jobs, webhooks, integrations, and
  feature flags touching the reported surface.
- Existing expected behavior, validation, guards, and error handling.
- Recently changed code if the symptom appears temporary or newly introduced.
- Nearby tests that establish intended behavior.
- Legacy/V1 vs production paths, especially subscribe links/widgets, webforms,
  tapcards, review flows, sender numbers, campaigns, and integrations.

When commenting on a bug, include code references only when they materially
clarify the cause or likely fix. Use file paths and concise descriptions rather
than large pasted snippets.

## Interactive Testing

Use interactive tools only when data and code inspection are not enough.

- Use Chrome for authenticated web app verification, reproducing UI flows,
  screenshots, and console/network inspection.
- Use Computer Use when local desktop interaction is required.
- Use `imessage` when the test requires real message receipt, opt-in, or SMS
  thread verification.

Before sending real messages, keep the test narrow: identify the account,
location, phone number, expected opt-in state, and rollback/cleanup need. Do not
spam customers or use customer phone numbers for tests unless the user has
explicitly approved that exact test.

## Outcome Comment Template

Use this shape for Linear comments. Keep it concise and evidence-led.

```markdown
Triage result: <classification>

Account/location: <identified account/location or missing detail>

Duplicate check: <none found / possible duplicate ISSUE-123 / duplicate of ISSUE-123>

Evidence:
- <production DB fact with relevant IDs/timestamps/counts>
- <repo/code fact, if useful>
- <browser/repro fact, if performed>

Impact:
- Scope: <one customer/location/contact or multiple; include who if known>
- Timing: <ongoing / temporary / unknown>

Recommended next action:
- <close with answer / link duplicate / support manual action / create feature request / engineering fix>

support follow-up needed:
- <only the smallest unanswered question, or "None">
```

## Classification Guidance

Treat it as a confirmed bug only when behavior contradicts the intended product
behavior and evidence points to code, data processing, integration, or system
failure.

Treat it as a feature request when the product does not currently support the
requested behavior, even if the customer framed it as broken.

Treat it as a misunderstanding when the system is working as designed and the
gap is expectation, setup, or training.

Treat it as a data question when the request is really asking "what happened?"
or "why does this number/state look like this?" and can be answered from production data
without code changes.

Treat it as duplicate when an existing ENG issue covers the same customer
impact or same root cause. Link the existing issue and add any new evidence
there if useful.

## Extra Things To Check

In addition to the user's requested outcomes, check these because they reduce
engineering load:

- Severity and urgency: is a customer blocked, money/message sending affected,
  or is this cosmetic/reporting confusion?
- Blast radius: same account only, same feature area globally, same integration,
  or same recent deployment window?
- Existing workaround: can support/admin resolve it today?
- Missing acceptance criteria: if it becomes a feature request, what is the
  smallest product behavior that would satisfy the request?
- Ownership: should this stay in ENG, be linked to another team/project, or be
  closed from Dev Triage?
- Repro quality: do we have enough account/location/contact/time detail for an
  engineer to act without another round trip?
