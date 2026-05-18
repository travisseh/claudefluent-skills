# Gather Issue Context

## Context
Collect enough information to file a useful issue. Two paths: proactive (conversation context already exists) and explicit (may need interactive gathering). The goal is to pre-fill as much as possible from what the agent already knows, then confirm with the user.

## Input
- **Trigger mode**: proactive (agent detected failure) or explicit (user ran `/aos-issue`)
- **Argument**: optional description text from `/aos-issue [description]`

## Steps

### 1. Check Prerequisites

```bash
command -v gh >/dev/null 2>&1
```
If missing: "gh CLI is required. Install: `brew install gh`" — stop.

```bash
gh auth status 2>/dev/null
```
If not authenticated: "GitHub auth required. Run: `gh auth login`" — stop.

### 2. Identify the Component

Read the library catalog:
```bash
cat ~/.claude/skills/aos-library/library.yaml
```

Search for the component across all type lists:
- `library.skills` — match by name
- `library.agents` — match by name
- `library.prompts` — match by name
- `library.hooks` — match by name
- `library.plugins` — match by name
- `library.mcp_servers` — match by name

Also check if it's an aos-internal skill: `aos`, `aos-library`, `aos-issue`.

Extract and record:
- **name**: component name
- **type**: skill / agent / prompt / hook / plugin / mcp_server / aos-internal
- **source**: GitHub URL from the `source` field in library.yaml, or `https://github.com/Example Company/aos` for aos-internal skills

If the component cannot be identified by exact name:
1. **Fuzzy match** — scan catalog names and descriptions for partial matches. If plausible matches exist, ask the user: "Did you mean one of these?" and list them.
2. **No match at all** — ask the user to clarify which component they mean. If it's not a library component, it may still be a general aos issue — proceed with type `general` and source `https://github.com/Example Company/aos`.

### 3. Gather Context (path depends on trigger mode)

#### Proactive Path

The conversation already contains context about the failure. Extract:

- **Problem**: what went wrong — the error, unexpected output, or incorrect behavior
- **Expected behavior**: what the user expected to happen
- **Actual behavior**: what actually happened (include error messages, wrong output)
- **Context**: what the user was trying to accomplish
- **Reproduction**: any steps or conditions that led to the failure (if discernible)

Also form an **Agent Assessment**: your analysis of the suspected root cause — which part of the skill/agent/hook might be responsible, your confidence level (low/medium/high), and any specific files or sections you suspect.

#### Explicit Path

If the user provided an argument with `/aos-issue [description]`, use it as starting context.

If there is relevant conversation context about a component failure, extract from it (same as proactive path).

If there is no prior context, ask the user via AskUserQuestion:

**Question 1** (if component not already identified):
"Which library component had the issue?" — provide a list of installed components if helpful.

**Question 2** (if problem not clear from context):
"What happened? Include any error messages or unexpected output."

**Question 3** (if expected behavior not clear):
"What did you expect to happen instead?"

**Filing threshold**: If you can fill Problem, Expected Behavior, and Actual Behavior with distinct, specific content, you have enough to file without further questions. Minimize questions — skip any already answered by the argument or conversation context. One well-targeted question is better than three redundant ones.

Form an Agent Assessment even on the explicit path if you have enough context to analyze the problem.

### 4. Build Issue Draft

Assemble the following fields:

| Field | Source |
| --- | --- |
| Component name | Step 2 |
| Component type | Step 2 |
| Source URL | Step 2 |
| Problem | Step 3 |
| Expected behavior | Step 3 |
| Actual behavior | Step 3 |
| Context | Step 3 |
| Reproduction | Step 3 (or "Not captured") |
| Agent Assessment | Step 3 |

### 5. Confirm with User

Present the draft summary to the user via AskUserQuestion:

```
I've drafted an issue for [component name]:

Title: [Verb] [component] [specific problem]

Problem: [summary]
Expected: [expected behavior]
Actual: [actual behavior]
Assessment: [brief agent assessment]

File this issue, or adjust anything first?
```

Options:
- "File it" — proceed to the file cookbook
- "Let me adjust" — incorporate changes, re-confirm

When confirmed, proceed to [cookbook/file.md](file.md) with the finalized draft.
