---
name: commit-and-push
description: >
  Commit and push a completed local change set, then monitor the resulting
  Vercel or Railway deployment until it succeeds or clearly fails. Use when the
  user asks to commit, push, ship, deploy, publish changes, or "commit and push"
  work that has just been discussed or implemented. Emphasizes staging only the
  relevant files from the current conversation, avoiding unrelated dirty
  worktree changes, running required checks before committing, and reporting the
  deployment result.
---

# Commit And Push

Use this skill to package a finished change safely and verify that the pushed
commit actually builds in the hosting provider.

## Workflow

1. Identify the intended change set.
   - Use the recent conversation, `git diff`, `git status --short`, and changed
     file paths to infer which files belong to the requested work.
   - Stage only files clearly tied to the change being committed.
   - If a changed file contains mixed unrelated edits, stop and ask before
     staging it.
   - Do not include skill edits, local notes, generated artifacts, or unrelated
     dirty files unless the user explicitly includes them.

2. Show the commit scope before committing.
   - Report the exact files that would be committed.
   - If the user has already explicitly asked to commit, proceed after checking
     scope; do not ask for redundant confirmation unless the scope is ambiguous.
   - Respect repo-specific instructions such as "do not commit automatically"
     when the current user request is not an explicit commit request.

3. Pull remote changes first when pushing `main` or `master`.
   - If the current branch is `main` or `master`, fetch and integrate upstream
     changes before staging/committing/pushing.
   - Prefer a non-destructive pull that preserves local work, such as
     `git pull --rebase --autostash`, after confirming the dirty files are the
     intended change set.
   - If the pull creates conflicts, stop and resolve them before validation.
     Never force-push or discard local/remote changes to get unstuck.
   - If the current branch has no upstream, fetch the matching origin branch and
     integrate it when it exists before pushing.

4. Run required validation.
   - Read local repo instructions first: `AGENTS.md`, `CLAUDE.md`,
     `CONTRIBUTING.md`, package scripts, or project skills referenced by the
     current task.
   - For TypeScript projects, run the required typecheck before commit. Common
     defaults are `npx tsc --noEmit`, `npm run typecheck`, or the repo-specific
     command.
   - For frontend changes, run the smallest meaningful browser or build check
     that matches the risk. Use the repo's stated requirements when present.
   - If validation fails, do not commit unless the user explicitly accepts the
     risk after seeing the failure.

5. Commit.
   - Use a concise descriptive message explaining what changed.
   - Avoid vague messages such as `fix`, `updates`, or `wip`.
   - After committing, capture the short commit hash.

6. Push.
   - Push the current branch to its upstream when configured.
   - If no upstream exists, push with `git push -u origin <branch>`.
   - Never force-push unless the user explicitly asks.

7. Merge to main unless this is the Example Company repo.
   - Default behavior after a successful feature-branch push is to merge the
     current branch into `main` and push `main`, so completed work actually
     ships instead of stopping at a branch.
   - Exception: if the repo is Example Company / `boostly`, do not merge to `main`;
     follow the Example Company PR/review process instead.
   - Before merging, confirm the branch has no unstaged or staged changes that
     belong to the requested commit. Unrelated dirty files may exist in the
     worktree; do not stage, revert, or include them.
   - Use a normal non-force merge. Prefer fast-forward when available; otherwise
     create a merge commit only when that is the repo's normal workflow.
   - Push `main` after the merge succeeds.

8. Monitor deployment.
   - Detect likely hosting from repo files:
     - Vercel: `.vercel/project.json`, `vercel.json`, Vercel app structure, or
       existing Vercel CLI usage.
     - Railway: `railway.json`, `railway.toml`, Railway service files, or
       existing Railway CLI usage.
   - Prefer provider CLI/API checks over guessing from git push output.
   - For Vercel:
     - Use `vercel ls` / `vercel inspect` if authenticated and linked.
     - If available, identify the deployment for the pushed commit or branch and
       poll until `READY` or an error state.
     - If CLI access is unavailable, report that monitoring could not be
       completed and provide the best deployment URL or dashboard path found.
   - For Railway:
     - Use `railway status`, `railway deployments`, or the current Railway CLI
       commands available in the repo/environment.
     - Poll the deployment for the pushed commit or latest service deployment
       until success or failure.
     - If CLI access is unavailable, report the limitation and provide the
       relevant project/service context found locally.
   - If both Vercel and Railway are present, infer the correct one from project
     config, recent deploy commands, or user context. If unclear, check both
     read-only.
   - Stop monitoring when the deployment succeeds, fails, or times out with a
     clear status.

## Safety Rules

- Never use `git add .` unless every dirty file has already been confirmed as
  part of the requested change.
- Never revert unrelated user changes.
- Never run destructive git commands such as `git reset --hard` or
  `git checkout --` unless the user explicitly asks.
- Never print secrets from deployment config or provider output.
- If the repo has untracked generated artifacts, ignore them unless they are
  clearly required for the change.
- If the current branch is protected or the repo expects PR branches, follow the
  repo-specific workflow instead of pushing directly to `main`.

## Final Report

Include:

- Files committed
- Validation run and result
- Commit hash and branch
- Push result
- Main merge and main push result, unless skipped for Example Company or a repo-specific
  PR workflow
- Deployment provider checked
- Deployment status and URL when available
- Any unrelated dirty files left untouched

If the push succeeded but deployment monitoring could not be completed, say so
plainly and state why.
