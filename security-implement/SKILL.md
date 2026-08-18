---
name: security-implement
description: Execute the next safe phase from docs/security/SECURITY-TASKS.md and record real validation evidence in docs/security/SECURITY-EVIDENCE-LOG.md.
metadata:
  short-description: Implement one security phase with evidence
---

# Security Implement

Execute the next safe phase from the security plan.

Read:

```text
docs/security/SECURITY-PLAN.md
docs/security/SECURITY-TASKS.md
docs/security/SECURITY-EVIDENCE-LOG.md
```

Update:

```text
docs/security/SECURITY-TASKS.md
docs/security/SECURITY-EVIDENCE-LOG.md
```

You may also update code, config, tests, docs, or scripts required by the current approved phase.

## Arguments

- `--phase-only`: complete at most one phase, then stop.
- `--dry-run`: report the next phase and commands without changing files.

## Safety

- Refuse to continue if `SECURITY-PLAN.md` or `SECURITY-TASKS.md` is missing.
- Never expose secrets.
- Never weaken security controls to pass validation.
- Never delete evidence or mark a task complete without real verification.
- Never mutate production, databases, payment state, hosting, DNS, or live settings without explicit approval for that exact action.

## Workflow

1. Find the first incomplete phase or task in `SECURITY-TASKS.md`.
2. If `--dry-run` is present, report the selected phase, intended edits, validation commands, risks, and stop.
3. Implement only the selected phase. Keep changes narrowly scoped.
4. Run the smallest meaningful validation after each material change.
5. Append real evidence to `SECURITY-EVIDENCE-LOG.md`.
6. Mark tasks complete only when the matching gate passes.

## Evidence Entry

Append entries like:

```markdown
## YYYY-MM-DD HH:MM UTC - Phase <n>: <name>

Files changed:

Commands run:

Output summary:

Security result:

Residual risk:

Rollback note:
```

Stop when one phase gate passes, `--phase-only` is reached, validation fails, or a sensitive live mutation needs user approval.
