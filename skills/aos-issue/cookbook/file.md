# File the Issue

## Context
Issue context has been gathered and confirmed by the user. Execute the filing pipeline: version check, component freshness, environment metadata, dedup search, compose, file, report.

## Input
Finalized issue draft from the gather cookbook:
- Component: name, type, source URL
- Problem, expected behavior, actual behavior, context, reproduction
- Agent assessment

## Steps

### 1. Version Check

Check if the local aos installation is current:

```bash
git -C ~/.claude/aos fetch origin main --quiet 2>/dev/null
LOCAL=$(git -C ~/.claude/aos rev-parse HEAD)
REMOTE=$(git -C ~/.claude/aos rev-parse origin/main 2>/dev/null)
```

If LOCAL != REMOTE:
- Tell the user: "Your aos installation is behind the latest version. The issue may already be fixed."
- Ask whether to update first (re-run install script or `git -C ~/.claude/aos pull`) or continue filing
- If user wants to update: stop and suggest the update command
- If user wants to continue: proceed, noting the version gap in the issue

Get the aos version:
```bash
jq -r '.version' ~/.claude/aos/.claude-plugin/plugin.json
```

### 2. Component Freshness Check

For source-based components (skills, agents, prompts, hooks), check when the installed copy was last updated.

Determine the installed path based on component type:
- Skills: `~/.claude/skills/<name>/SKILL.md` or `.claude/skills/<name>/SKILL.md`
- Agents: `~/.claude/agents/<name>.md` or `.claude/agents/<name>.md`
- Prompts: `~/.claude/commands/<name>.md` or `.claude/commands/<name>.md`
- Hooks: `~/.claude/hooks/<name>.sh` or `.claude/hooks/<name>.sh`

Check both global and local paths. Use whichever exists:
```bash
ls -l <installed_path> 2>/dev/null
```

Record the file modification date. If the component was last modified more than 7 days ago:
- Suggest: "This component was last installed/synced on [date]. Consider running `/aos-library sync` to get the latest version before filing."
- Ask whether to sync first or continue filing

For config-based components (plugins, MCP servers) or aos-internal skills: skip this step.

### 3. Collect Environment Metadata

```bash
gh api user --jq '.login' 2>/dev/null
```

```bash
uname -srm
```

```bash
claude --version 2>/dev/null
```

Record:
- **GitHub username**: from `gh api user`
- **OS**: from `uname -srm`
- **Claude Code version**: from `claude --version`
- **aos version**: from Step 1
- **Installed date**: from Step 2 (file modification date, or "N/A" for config-based)

### 4. Dedup Search

Search for existing open issues. Include problem keywords alongside the component name for better relevance:

```bash
gh issue list -R ExampleCo/aos --search "<component_name> <key_problem_words>" --state open --limit 10 --json number,title,url
```

For example, if the component is `slack` and the problem is about channel resolution, search `"slack channel"` not just `"slack"`.

If matching open issues are found:
- Compare each issue's title against the gathered problem description
- Recommend the best match (if any) — don't just dump the list
- Present to user: "Found N open issues. #42 'Fix slack channel lookup with spaces' looks related. Want to add your context there, or file a new issue?"
- If comment on existing: compose a comment using this template and post it:
  ```bash
  gh issue comment <number> -R ExampleCo/aos --body "$(cat <<'COMMENT_EOF'
  ## Additional Report

  **Filed by**: @<github_username>
  **aos version**: <aos_version>

  ### Problem
  <problem_description>

  ### Actual Behavior
  <actual_behavior>

  ### Environment
  - **OS**: <os_info>
  - **Claude Code version**: <claude_version>
  - **Installed**: <mod_date>

  ### Agent Assessment
  <agent_analysis_with_confidence_level>
  COMMENT_EOF
  )"
  ```
  Then skip to Step 7 (report the commented issue URL).
- If file new: proceed to Step 5

If no matching issues: proceed to Step 5.

### 5. Compose the Issue

**Title**: `[Verb] [component] [specific problem]`

Rules:
- Start with an action verb: Fix, Improve, Add, Update, Investigate
- Include the component name
- Be specific enough to distinguish from other issues
- Keep under 70 characters

Examples:
- `Fix hubspot skill returning empty results for contacts`
- `Improve slack skill rate limiting handling`
- `Investigate quo batch extraction timeout`

**Body**: Use this exact template structure:

```markdown
## Component
- **Name**: `<name>`
- **Type**: <type>
- **Source**: <source_url>
- **aos version**: <aos_version>
- **Installed**: <mod_date> (file modification date)

## Problem
<problem_description>

## Expected Behavior
<expected_behavior>

## Actual Behavior
<actual_behavior>

## Context
<user_context>

## Reproduction
<reproduction_steps>

## Environment
- **Filed by**: @<github_username>
- **OS**: <os_info>
- **Claude Code version**: <claude_version>

## Agent Assessment
<agent_analysis_with_confidence_level>
```

Notes:
- If reproduction steps are unknown, write "Not captured — issue observed during normal use"
- Agent Assessment should include: suspected root cause, which file/section of the component may be involved, confidence level (low/medium/high)
- Keep sections concise — enough for a triaging agent to act, not a novel

### 6. File the Issue

Use a heredoc to handle markdown formatting and special characters:

```bash
gh issue create -R ExampleCo/aos \
  --title "<title>" \
  --label "aos-issue" \
  --body "$(cat <<'ISSUE_EOF'
<body>
ISSUE_EOF
)"
```

If the command fails because the `aos-issue` label doesn't exist, create it first:
```bash
gh label create "aos-issue" -R ExampleCo/aos --description "Filed by aos-issue skill" --color "c2e0c6"
```
Then retry the issue creation.

### 7. Report

Extract the issue URL from the `gh issue create` output (it prints the URL on success).

Report to the user:

```
Issue filed: <url>

In the meantime, you can try:
- /aos-library sync — refresh installed components to latest
- Re-run install script or `git -C ~/.claude/aos pull` — update aos itself
```

If the user commented on an existing issue instead of filing new:

```
Comment added to <url>
```
