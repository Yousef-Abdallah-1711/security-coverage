# /security-assess

Use the `security-coverage` skill to assess this repository's security coverage.

## Reads

- The current repository.
- Existing security docs under `docs/security/`, if present.
- The stack detector at `skills/security-coverage/scripts/detect_security_stack.py`, when available.
- References:
  - `references/layers.md`
  - `references/threat-model.md`
  - `references/stack-map.md`

## Writes

- `docs/security/SECURITY-STRATEGY.md`

Use `templates/SECURITY-STRATEGY.md` as the output shape.

## Workflow

1. Detect the stack and attack surface from files, routes, APIs, admin tools, auth, database, payments, and deployment signals.
2. Inspect a representative sample before trusting path heuristics.
3. Decide every security layer as `ADOPT`, `PARTIAL`, `DEFER`, or `SKIP`.
4. Record assumptions, assets, trust boundaries, likely threats, current controls, and gaps.
5. Ask only for business/security intent that cannot be discovered from the repo.

## Stop When

`docs/security/SECURITY-STRATEGY.md` is complete enough for `/security-plan` to produce phased tasks without inventing scope.

Do not modify application code during assessment.
