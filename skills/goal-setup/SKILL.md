---
name: goal-setup
description: Draft, refine, activate, and manage explicit Codex Goals. Use only when the user asks for the goal-setup skill, asks to write or improve a /goal command, or explicitly wants to create or manage a persistent Codex Goal lifecycle.
---

# Goal

Use this skill to help users turn uncertain multi-step work into a strong Codex Goal: a thread-scoped completion contract with a measurable outcome, evidence-based verification, constraints, and a clear stop condition.

Source pattern: OpenAI cookbook, "Using Goals in Codex" (May 9, 2026): https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex

## Core judgment

Use a Goal when the task has a clear finish line but the path is uncertain. Good fits include performance optimization, flaky test investigation, bug hunts requiring reproduction, benchmark-driven tuning, dependency migrations, multi-step refactors, and research that must end in an evidence-backed artifact.

Do not use a Goal for one-line edits, simple explanations, short code reviews, or vague asks like "make this better" unless you first tighten the finish line and verification surface.

## Goal formula

When drafting a Goal, include these six elements when relevant:

- Outcome: what must be true when done.
- Verification surface: tests, benchmark, command output, generated artifact, source material, or other concrete evidence.
- Constraints: what must not regress.
- Boundaries: allowed files, repos, data sources, tools, or resources.
- Iteration policy: how Codex should choose the next useful action after each attempt.
- Blocked stop condition: when to stop and what to report if no defensible path remains.

Preferred template:

```text
/goal <desired end state> verified by <specific evidence> while preserving <constraints>. Use <allowed inputs, tools, or boundaries>. Between iterations, <how Codex should choose the next best action>. If blocked or no valid paths remain, <what Codex should report and what would unlock progress>.
```

## Drafting workflow

1. Decide whether a Goal is warranted. If a normal prompt is better, say so briefly and handle the task normally.
2. If the user's task is clear enough, draft a paste-ready `/goal ...` command.
3. If the finish line is ambiguous, ask for the one missing detail that determines verification, or provide a conservative draft with explicit assumptions.
4. Prefer measurable language over vibes. Name the artifact, command, test suite, benchmark, report, source inventory, or acceptance criteria.
5. Preserve uncertainty. If data, credentials, benchmarks, or source material may be missing, include how to label blocked or approximate results.

## Activation and lifecycle

When the user wants to activate a Goal, use the available goal tools if present in the current environment. Otherwise provide the paste-ready `/goal` command.

Useful command surface:

```text
/goal <objective>   Start a Goal
/goal               View the current Goal
/goal pause         Pause an active Goal
/goal resume        Resume a paused Goal
/goal clear         Remove the current Goal
```

Goals are thread-scoped, not global memory and not project instructions. They should be marked complete only after checking the objective against concrete evidence such as files changed, commands run, tests passed, benchmark output, generated artifacts, logs, or research sources.

Budget limits and blockers are not completion. If the Goal cannot be completed under the current constraints, report progress, evidence gathered, attempted paths, blocker, and the next input needed.

## Examples

Weak:

```text
/goal Improve performance
```

Strong:

```text
/goal Reduce p95 checkout latency below 120 ms, verified by the checkout benchmark, while keeping the correctness suite green. Use only the checkout service, benchmark fixtures, and related tests. Between iterations, record what changed, what the benchmark showed, and the next best experiment to try. If the benchmark cannot run or no valid paths remain, stop with the attempted paths, evidence gathered, blocker, and next input needed.
```

Weak:

```text
/goal Reproduce this paper
```

Strong:

```text
/goal Produce the strongest evidence-backed reproduction of the paper using the available materials and local resources. Attempt the headline results where feasible, verify outputs where possible, and end with a report that separates confirmed findings, approximate reconstructions, blocked claims, and remaining uncertainty.
```

Weak:

```text
/goal Write docs for this feature
```

Strong:

```text
/goal Produce a docs page for this feature that explains the lifecycle, command surface, and two examples. Verify that the page builds locally and that all referenced commands match current CLI behavior.
```
