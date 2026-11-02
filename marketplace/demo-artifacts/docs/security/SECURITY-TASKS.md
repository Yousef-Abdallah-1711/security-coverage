# Security Tasks

## Task Register

| Task ID | Source finding | Phase | Layer | Scope | Acceptance criteria | Verification | Status |
|---|---|---|---|---|---|---|---|
| SEC-009 | SEC-F001, SEC-F004 (synthetic fixture subset only) | PHASE-DEMO-001 (SYNTHETIC DEMO ONLY) | S3, S4, S5 | Only `tests/fixtures/vulnerable_app/app.py` and new `tests/test_synthetic_demo.py`; only command: `python -m unittest discover -s tests -p test_synthetic_demo.py -v` | `update_note` rejects tenant mismatch; rejects non-string and >2048-character bodies; scopes SQL update by note ID and tenant ID; focused tests cover these behaviors | Run only the named unittest command if verification is performed; no implementation or verification has run | APPROVED SCOPE; NOT STARTED |
| SEC-001 | SEC-F001, SEC-F002; SEC-Q001 | PHASE-001 | S0, S3, S5, S6 | Identify actual target and registered note/invoice entry points; map each fixture example to a real counterpart or mark fixture-only | Owner confirms target, reachability, exact corresponding components, or records no real counterpart; no fixture-to-production assumption | Review target inventory and owner confirmation; no reachability check performed yet | TODO |
| SEC-002 | SEC-F001; SEC-Q002, SEC-Q003 | PHASE-001 | S2, S3, S5 | For a confirmed note flow, document actors, roles, tenant/resource ownership, data adapter, schema/policy and exact update boundary | Owner-approved allow/deny rules exist; applicable implementation requires authenticated identity and server-side authorization plus owner/tenant scope in the mutation | Review approved rules and diff; verify allowed and denied actor/resource cases, including cross-tenant denial when applicable; not run | TODO |
| SEC-003 | SEC-F002; SEC-Q004 | PHASE-001 | S3, S4, S6 | For a confirmed invoice flow, identify actor/workflow, trusted amount/currency/state source, provider/webhook or administrative path, and corresponding mutation boundary | Owner confirms flow; implementation does not trust caller-supplied financial state; manual changes require authorized role and audit evidence; provider signature/replay controls are addressed only if a webhook exists | Review flow and diff; verify amount/state tampering and authorization, plus signature/replay behavior if applicable; not run | TODO |
| SEC-004 | SEC-F003 | PHASE-002 | S2, S9 | Actual password-reset path, mailer/identity integration, and effective throttling | Scoped abuse controls and externally uniform responses are present where the flow exists | Review behavior and verify throttling and account-existence response equivalence; not run | TODO |
| SEC-005 | SEC-F004 | PHASE-002 | S4, S9 | Actual sensitive request parsing and note/invoice input boundaries | Required fields/types are validated server-side; size bounds and safe errors are enforced at applicable boundaries | Verify valid, malformed, missing, oversized, and safe-error cases against actual runtime; not run | TODO |
| SEC-006 | SEC-F005 | PHASE-003 | S2, S7 | Actual browser session configuration and cookie-authenticated state-changing flows | Runtime sets Secure, HttpOnly, and appropriate SameSite policy; applicable CSRF defenses are documented and effective | Inspect response behavior and verify cookie attributes/CSRF cases in actual runtime; not run | TODO |
| SEC-007 | SEC-F006 | PHASE-003 | S1, S7 | Actual deployment/runtime debug configuration | Debug behavior is test-only or disabled in deployed environments; diagnostics are not exposed | Review deployment configuration and verify applicable runtime behavior; not run | TODO |
| SEC-008 | S8, S10, S11; SEC-Q005 | PHASE-004 | S8, S10, S11 | Real deployment configuration, logging/monitoring, backup/recovery, rollback and release evidence | Applicable controls and owners are documented; skipped checks have reasons; residual risk ownership and recovery evidence are recorded before a release decision | Review operational evidence and execute only approved release-gate checks; not run | TODO |

Task IDs are stable plan identifiers. Source finding IDs remain those in `SECURITY-STRATEGY.md`. Tasks are conditional where the strategy does not establish a real corresponding flow. Do not implement the synthetic fixture merely because it contains the pattern.

Status values: TODO / APPROVAL PENDING / APPROVED SCOPE; NOT STARTED / IN PROGRESS / BLOCKED / DONE / DEFERRED. “APPROVED SCOPE; NOT STARTED” records the user's exact fixture-only authorization and does not claim implementation or verification.

## Phase Gates

### PHASE-001

- [ ] Phase scope previewed to user.
- [ ] Explicit approval recorded for the exact implementation scope.
- [ ] SEC-001 target mapping and applicability recorded.
- [ ] SEC-002 identity, authorization, ownership, and database rules confirmed; applicable criteria verified.
- [ ] SEC-003 trusted invoice flow and authorization documented; applicable criteria verified.
- [ ] Failed and skipped checks recorded with reasons.
- [ ] Evidence and residual risk owners recorded.
- [ ] Rollback/recovery described for approved changes.
- Gate result: NOT RUN

### PHASE-DEMO-001 — SYNTHETIC DEMO ONLY

- [x] Explicit approval recorded for the exact two-file, one-command fixture-only scope.
- [ ] Change only `tests/fixtures/vulnerable_app/app.py` to reject tenant mismatch, non-string note bodies, and bodies over 2048 characters; scope SQL update by note ID and tenant ID.
- [ ] Add only `tests/test_synthetic_demo.py` for those behaviors.
- [ ] If verifying, run only `python -m unittest discover -s tests -p test_synthetic_demo.py -v`.
- [ ] Record actual diff, command result, failures/skips, and remaining fixture limitations.
- [ ] Explicitly retain real deployment, note route reachability, roles beyond this fixture, and invoice/payment remediation as unknown/deferred.
- Gate result: APPROVED SCOPE; NOT STARTED; NOT RUN

This synthetic-demo phase does not prove a real application is secure and does not complete SEC-001 or SEC-003 for any real target.
