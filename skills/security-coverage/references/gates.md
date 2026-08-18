# Security Gates

Use for `/security-plan` and every `/security-implement` phase.

## Five Gate Conditions

A phase is complete only when all five are true:

1. The phase command(s) run from the repo root and exit zero, or a manual check is recorded with exact steps and result.
2. Every task in the phase is checked off.
3. Evidence includes real output: counts, findings, durations, HTTP status, screenshots path, or scanner IDs.
4. Zero unexplained skips. Every skip has a non-failure reason.
5. Residual risk is documented with owner, severity, and follow-up.

## Forbidden Routes To Green

Never:

- delete or comment out a failing security check to pass
- disable auth, CSRF, RLS, CSP, or validation without a documented replacement
- broaden CORS to `*` for credentialed/private APIs
- print or commit secrets
- mark a scanner false-positive without reading the code
- use filtered command output as full evidence
- mutate live production systems without explicit approval

## Vulnerability Handling

If a real vulnerability is found:

1. Record the finding without exploit instructions beyond what is needed to reproduce safely.
2. Classify impact and affected surface.
3. Fix only if the current phase authorizes that type of change.
4. If the fix needs live migration, credential rotation, or user-data mutation, stop and ask.

## Phase Closeout

Append to `SECURITY-EVIDENCE-LOG.md`:

```text
Phase:
Date:
Commands:
Evidence:
Findings:
Changes:
Residual risk:
Rollback:
Gate result:
```
