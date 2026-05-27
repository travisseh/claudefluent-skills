# Current Example Company PR Rules

Use this as a quick reminder. Re-read the repo files if accuracy matters.

## Source Files

- `/Users/you/Programming/example-company/CONTRIBUTING.md`
- `/Users/you/Programming/example-company/.github/pull_request_template.md`
- `/Users/you/Programming/example-company/.github/CODEOWNERS`

## Current Expectations

- Tie every change to one Linear issue.
- Use branch format `{LINEAR_ISSUE_ID}-short-description`.
- Keep one issue per PR.
- Use descriptive commit messages that explain what changed and why.
- Run:
  - `npm run lint`
  - `npm run typecheck`
  - `npm run test:run`
  - `npm run build`
- Fill out the PR template completely.
- Link the Linear issue in the PR.
- Include screenshots for UI changes.
- Call out migrations or breaking changes.
- Request CODEOWNERS review.
- Do not force-push during review.
- Expect squash merge after approval.

## Current CODEOWNERS Highlights

- Default reviewer group: `@example-company/core`
- Backend review required for:
  - `prisma/schema.prisma`
  - `prisma/migrations/`
  - `*.sql`
