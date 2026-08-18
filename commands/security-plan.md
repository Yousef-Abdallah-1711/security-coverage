# /security-plan

Use the `security-coverage` skill to turn the strategy into a decision-complete security plan.

## Reads

- `docs/security/SECURITY-STRATEGY.md`
- References:
  - `references/layers.md`
  - `references/gates.md`
  - relevant domain references for selected layers

## Writes

- `docs/security/SECURITY-PLAN.md`
- `docs/security/SECURITY-TASKS.md`
- `docs/security/SECURITY-EVIDENCE-LOG.md`

Use these templates:

- `templates/SECURITY-PLAN.md`
- `templates/SECURITY-TASKS.md`
- `templates/SECURITY-EVIDENCE-LOG.md`

## Workflow

1. Refuse to plan if `SECURITY-STRATEGY.md` is missing or too thin; ask the user to run `/security-assess`.
2. Convert adopted and partial layers into ordered phases.
3. Put the highest business risk as early as its dependencies allow.
4. Give each phase a command, task list, evidence requirement, rollback note, and green gate.
5. Mark parallel-safe tasks with `[P]` only when they touch independent files or checks.

## Stop When

The plan and task list are reviewable, phase-gated, and safe to execute one phase at a time.

Do not implement security changes during planning.
