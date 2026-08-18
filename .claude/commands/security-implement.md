# /security-implement

Execute the next safe phase from the Security Coverage task list for the current repository.

First, read the canonical skill instructions from the first path that exists:

- `.claude/skills/security-coverage/SKILL.md`
- `.codex/skills/security-coverage/SKILL.md`
- `skills/security-coverage/SKILL.md`
- `~/.claude/skills/security-coverage/SKILL.md`
- `~/.codex/skills/security-coverage/SKILL.md`

Then read:

- `references/gates.md`
- the domain reference for the current phase

## Task

Read:

```text
docs/security/SECURITY-PLAN.md
docs/security/SECURITY-TASKS.md
docs/security/SECURITY-EVIDENCE-LOG.md
```

Update as needed:

```text
docs/security/SECURITY-TASKS.md
docs/security/SECURITY-EVIDENCE-LOG.md
```

You may also update code, config, tests, docs, or scripts required by the current approved phase.

## Options

- `--phase-only`: complete at most one phase, then stop.
- `--dry-run`: report the next phase and commands without changing files.

## Required Workflow

1. Refuse to continue if `SECURITY-PLAN.md` or `SECURITY-TASKS.md` is missing. Tell the user to run `/security-plan`.
2. Find the first incomplete phase or task in `SECURITY-TASKS.md`.
3. If `--dry-run` is present, report the selected phase, intended edits, validation commands, and risks without changing files.
4. Otherwise, implement only that phase. Keep changes narrowly scoped.
5. Run the smallest meaningful validation after each material change.
6. Record evidence in `SECURITY-EVIDENCE-LOG.md`: commands run, output summary, files changed, security result, residual risk, and rollback note.
7. Mark tasks complete only when the matching gate passes.

## Stop Condition

Stop when one phase gate passes, `--phase-only` is reached, validation fails, or a live/production/security-sensitive mutation needs explicit user approval.

Never expose secrets, weaken security controls, delete evidence, skip failing checks, or mutate production/live systems without explicit approval.
