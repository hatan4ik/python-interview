# Senior DevOps Git Interview Guide

This guide is a practical answer bank for senior DevOps/SRE interviews. It focuses on
safe workflows, incident recovery, release hygiene, and GitOps alignment.

## What interviewers care about

- Safety on shared branches (no history rewrites on main).
- Fast recovery (bisect, reflog, revert).
- Release discipline (tags, hotfixes, rollback paths).
- Collaboration (reviews, conflict resolution, clear commit messages).
- GitOps mindset (Git as source of truth, reconcilers pull state).

## Mental model (short)

- A commit is an immutable snapshot; branches are just pointers to commits.
- The index (staging area) is separate from the working tree.
- History is a DAG; you can move pointers but you should not rewrite shared history.

## Command quick reference

- Inspect: `git status`, `git log --oneline --graph --decorate --all`, `git show`, `git diff`
- Undo local: `git restore`, `git reset --soft|--mixed|--hard`
- Undo shared: `git revert <sha>`, `git revert -m 1 <merge_sha>`
- Recover: `git reflog`, `git checkout <old_sha>`
- Debug: `git bisect start`, `git bisect good <sha>`, `git bisect bad <sha>`
- Review: `git blame`, `git range-diff <old> <new>`
- Collaboration: `git fetch`, `git rebase`, `git merge`, `git cherry-pick`

## Senior-level Q and A (with discussion points)

### Merge vs rebase
Answer:
- I rebase my local feature branch to keep a clean story, then merge into main
  (or squash-merge) to preserve an audit trail. I never rebase shared branches.
Discussion:
- Rebase rewrites history; merge preserves history. Senior engineers choose based
  on safety and traceability.

### Reset vs revert
Answer:
- `reset` is for local cleanup before pushing. `revert` creates a new commit to
  undo changes on shared branches. On main, I use `revert` so history stays intact.
Discussion:
- This shows respect for shared history and incident audit requirements.

### Force push policy
Answer:
- Only on personal branches and always with `--force-with-lease`. Never on main
  or protected branches.
Discussion:
- `--force-with-lease` prevents clobbering teammates.

### Squash vs merge commits
Answer:
- Squash for noisy branches to keep main readable. Merge commits when the
  multi-commit history is valuable for debugging or compliance.
Discussion:
- Emphasize the trade-off between readability and forensic context.

### Cherry-pick
Answer:
- Use it for targeted hotfixes across branches, then reconcile the divergence
  later with a merge to avoid long-term drift.

### Conflict resolution
Answer:
- I identify intent on both sides, keep the smallest correct change, and rerun
  tests. I prefer smaller PRs to reduce conflict surface.

### Bisect for regressions
Answer:
- I use `git bisect` between known good/bad commits, ideally automated with
  `git bisect run <test>` so it is fast and objective.

### Reflog for recovery
Answer:
- If a commit "disappears," I check `git reflog`, then cherry-pick or reset to
  the old HEAD. Reflog is my safety net.

### Release strategy
Answer:
- Trunk-based with short-lived branches. Tags for immutable releases.
  Release branches only for long-lived support lines.
Discussion:
- This enables faster delivery and predictable rollbacks.

### Hotfix in production
Answer:
- Cut a hotfix branch from the release tag or production SHA, ship the fix,
  tag a new release, then merge back to main to avoid divergence.

### GitOps rollback
Answer:
- Revert the Git commit or move the release tag. The controller reconciles the
  cluster back to the desired state. This is a safe, auditable rollback path.

### Monorepo trade-offs
Answer:
- Pros: atomic changes and consistent tooling. Cons: CI scale and ownership
  boundaries. Mitigate with CODEOWNERS, path-based CI, and caching.

### Submodules
Answer:
- Avoid unless there is a strong reason. They are operationally brittle.
  Prefer subtrees or proper package management.

### Secret leak response
Answer:
- Rotate the secret immediately. Remove it from history using `git filter-repo`
  or BFG if required, invalidate caches, and add scanning and hooks to prevent
  recurrence.

### Signed commits/tags
Answer:
- In regulated environments, I sign commits and tags and enforce verification
  on protected branches to ensure provenance.

## Scenario drills (practice answers)

1. "You merged a bad commit to main."
   - Revert the commit on main, open a follow-up PR with the real fix, and add
     a regression test. Avoid rewriting history.

2. "CI failed after merge and prod is broken."
   - If impact is high, revert first to stabilize, then fix forward. Use tags
     and GitOps to roll back safely.

3. "A teammate force-pushed and broke your branch."
   - Use `git reflog` to recover the old SHA, then recreate your branch.

4. "How do you keep long-lived branches in sync?"
   - Prefer short-lived branches. If long-lived are required, rebase regularly
     and use `range-diff` to review changes post-rebase.

## Red flags to avoid saying

- "I just reset main to fix it."
- "Force push is fine on shared branches."
- "I do not know what reflog is."

## 30-second senior pitch

"I optimize for safety on shared branches, clarity of history, and reliable
rollback paths. I rebase locally, merge or squash into main, and use revert for
shared fixes. For incidents, I use bisect and reflog to recover quickly, and in
GitOps I roll back by reverting Git so the system converges safely."
