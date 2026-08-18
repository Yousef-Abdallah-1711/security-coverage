---
name: security-plan
description: Convert docs/security/SECURITY-STRATEGY.md into docs/security/SECURITY-PLAN.md, SECURITY-TASKS.md, and SECURITY-EVIDENCE-LOG.md.
metadata:
  short-description: Create phased security hardening tasks
---

# Security Plan

Turn the existing security strategy into a phase-gated implementation plan.

Read:

```text
docs/security/SECURITY-STRATEGY.md
```

Create or update:

```text
docs/security/SECURITY-PLAN.md
docs/security/SECURITY-TASKS.md
docs/security/SECURITY-EVIDENCE-LOG.md
```

## Safety

- Do not implement code or config changes during planning.
- Do not invent missing architecture details. If the strategy is too thin, stop and tell the user to run `/security-assess`.
- Do not include secret values in any output.
- Do not plan destructive or live mutations without a separate explicit approval gate.

## Workflow

1. Verify `docs/security/SECURITY-STRATEGY.md` exists and includes layer decisions.
2. Convert `ADOPT` and `PARTIAL` layers into ordered phases.
3. Put payment, auth, admin, user-data, and production exposure risks early when present.
4. Give every phase a scope, task list, suggested validation commands, evidence requirement, rollback note, and green gate.
5. Create an evidence log with headings only. Do not fake evidence.

## SECURITY-PLAN.md Output

```markdown
# Security Plan

## Source Strategy

## Phase Order

| Phase | Layers | Goal | Risk Reduced | Gate |
|---|---|---|---|---|

## Phase Details

### Phase 1: <name>

Scope:

Tasks:

Validation:

Evidence:

Rollback:

Gate:

## Deferred Or Skipped Layers

## Approval Gates For Live Changes
```

## SECURITY-TASKS.md Output

```markdown
# Security Tasks

## Phase 1: <name>

- [ ] Task
- [ ] Run validation
- [ ] Record evidence
- [ ] Gate passed
```

## SECURITY-EVIDENCE-LOG.md Output

```markdown
# Security Evidence Log

No evidence recorded yet.

## Entries
```

Stop when `/security-implement` can execute the first phase without guessing.
