---
name: claude
description: >
  Use when the user says /claude, $claude, "check with Claude", "ask Claude",
  "call Claude Code", or wants a second opinion, critique, feedback, sanity
  check, debugging perspective, architectural review, copy review, or product
  strategy critique using the local `claude -p` command. Helps Codex call
  Claude Code as an external reviewer and integrate the result.
---

# Claude

Use this skill to ask Claude Code for focused feedback via the local CLI:

```bash
claude -p "<prompt>"
```

This is useful when the user explicitly says `/claude`, `check with /claude`,
"ask Claude", "call Claude Code", "get Claude's feedback", "second opinion",
or when you are stuck and need a fast independent critique.

## Default Workflow

1. Define the exact question Claude should answer.
2. Gather only the relevant context: user goal, constraints, current plan, key files,
   error output, or draft text.
3. Call `claude -p` with a concise, structured prompt.
4. Treat Claude's response as input, not authority.
5. Synthesize the feedback into your own recommendation or implementation plan.
6. Tell the user what Claude added that changed, confirmed, or challenged your view.

## When To Use

- The user explicitly asks for Claude Code feedback.
- You are stuck on an error, config issue, build failure, or ambiguous design choice.
- You want a critique of strategy, positioning, copy, architecture, or implementation.
- A second model might catch missing risks before you edit files or ship a decision.

## When Not To Use

- Simple factual questions, trivial code edits, or tasks you can solve directly.
- Sensitive secrets, tokens, credentials, private keys, or raw customer data.
- Huge repo dumps. Summarize context and include narrow snippets instead.
- Anything requiring Claude to mutate files directly unless the user explicitly asks.

## Prompt Pattern

Use this shape:

```text
You are reviewing my work as a blunt, senior second-opinion reviewer.

Goal:
<what we are trying to accomplish>

Context:
<short relevant background>

Current thinking or artifact:
<plan, code excerpt, copy, error, or decision>

Constraints:
<repo rules, business constraints, deadlines, user preferences>

Please respond with:
1. Biggest risks or flaws
2. What you would change
3. Anything I am overthinking
4. A concise recommended next step
```

## Shell Usage

Prefer a here-doc when the prompt is more than one sentence:

```bash
claude -p "$(cat <<'EOF'
<prompt>
EOF
)"
```

Run from the relevant project directory when file paths or repo context matter.
Use `timeout` if available for long-running calls:

```bash
timeout 120 claude -p "$(cat <<'EOF'
<prompt>
EOF
)"
```

On macOS, `timeout` may not exist; if it fails, rerun without it.

## Output Handling

- Do not paste Claude's entire response unless the user asks.
- Summarize the useful feedback and note disagreements.
- If Claude's feedback is wrong or mismatched to the repo, say so and proceed with
  the stronger local judgment.
- If Claude identifies a credible issue, incorporate it before finalizing.

## Safety

Before calling `claude -p`, strip:

- API keys, auth tokens, cookies, and passwords
- Personal/customer data not needed for the review
- Large proprietary files unrelated to the question

For codebase questions, prefer file paths, short snippets, and command output over
bulk file contents.
