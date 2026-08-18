# /security-implement

Use the `security-coverage` skill to execute the next security phase safely.

## Reads

- `docs/security/SECURITY-PLAN.md`
- `docs/security/SECURITY-TASKS.md`
- `docs/security/SECURITY-EVIDENCE-LOG.md`
- References:
  - `references/gates.md`
  - domain references for the current phase

## Writes

- Security checks, tests, config, documentation, or code changes required by the current phase.
- Updated `docs/security/SECURITY-TASKS.md`
- Updated `docs/security/SECURITY-EVIDENCE-LOG.md`

## Options

- `--phase-only`: complete at most one phase, then stop.
- `--dry-run`: report the next phase and commands without changing files.

## Workflow

1. Find the first unticked phase in `SECURITY-TASKS.md`.
2. Complete tasks in order, running the smallest meaningful validation after each material change.
3. Never weaken a security control, expose secrets, delete evidence, skip a failing check, or mutate production/live systems without explicit approval.
4. If a real vulnerability is found, record it clearly. Fix only when the task authorizes that class of change.
5. Close the phase only when every gate in `references/gates.md` passes.

## Stop When

One phase gate passes, `--phase-only` is reached, or a blocker/vulnerability requires user decision.
