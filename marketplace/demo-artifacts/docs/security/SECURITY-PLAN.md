# Security Plan

## Record

- Schema version: 1
- Source strategy: `docs/security/SECURITY-STRATEGY.md` (assessment date 2026-11-02)
- Plan date: 2026-11-02
- Phase count: 5 (one synthetic-demo-only phase approved for implementation; real-target phases remain conditional)
- Highest risk: HIGH, conditional on corresponding code being reachable in a real application
- Scope: Plan only. Findings are source patterns in a synthetic, non-production fixture; do not infer reachability or deployment.

## Phases

| Phase | Goal | Source findings | Risk reduced | Dependencies | Gate |
|---|---|---|---|---|---|
| PHASE-DEMO-001 (SYNTHETIC DEMO ONLY) | Harden the isolated note fixture and add focused fixture tests under the exact user-approved scope | SEC-F001, SEC-F004 (fixture-only subset) | Fixture-level cross-tenant note update and invalid/oversized body acceptance | Explicit approval recorded in the current conversation; no real-target assumptions | Exact fixture files and single local test command only; results remain unverified until separately run |
| PHASE-001 | Establish the real target and determine whether note and invoice mutations have real counterparts | SEC-F001, SEC-F002 | Potential unauthorized or cross-tenant note changes; false invoice paid state or amount manipulation | Identify the real application, registered entry points, ownership/role rules, database behavior, and payment flow; answers to SEC-Q001–SEC-Q004 | Deferred; do not implement real application changes until target and business rules are confirmed |
| PHASE-002 | Bound and protect reset and sensitive input flows | SEC-F003, SEC-F004 | Reset abuse/account enumeration; malformed or excessive inputs | Confirm actual reset and request handling paths, effective infrastructure limits, and identity/mailer behavior | Verify uniform external reset responses, effective throttles, validation, limits, and safe errors |
| PHASE-003 | Review session and debug behavior in the actual runtime | SEC-F005, SEC-F006 | Session exposure/CSRF risk; debug diagnostics exposure | Identify actual browser-facing runtime, session lifecycle, CSRF controls, and deployment configuration | Verify runtime cookie policy and debug configuration; assess CSRF for cookie-authenticated mutations |
| PHASE-004 | Close deployment and operational evidence gaps and apply release gate | S8, S10, S11; SEC-Q005 | Unassessed deployment, monitoring, backup/recovery, and release risks | Real deployment and operational evidence | Record verified controls, skips, residual-risk owners, rollback/recovery, and release decision |

## Phase Details

### PHASE-001: Confirm target and protect high-impact mutations

- Objective: Resolve whether the synthetic note and invoice examples correspond to reachable flows in a real target. Real route reachability and any real remediation remain unknown and deferred; this phase does not inherit the synthetic-demo approval.
- Source evidence: `SEC-F001` (`tests/fixtures/vulnerable_app/app.py:8-13`) shows an update query by note ID without shown authentication, authorization, or tenant predicate. `SEC-F002` (`tests/fixtures/vulnerable_app/app.py:22-25`) shows invoice state mutation from caller-supplied amount with no shown role check. The strategy states reachability is unverified and the fixture README describes it as non-production.
- Scope (files/components): Establish the real application and its registered note/invoice entry points, identity and ownership model, database adapter/schema/policies, and payment or administrative workflow. Any real remediation requires a later, separate exact approval. The approval for PHASE-DEMO-001 applies only to the synthetic fixture scope stated there.
- Out of scope: Assuming the fixture is deployed; inventing routes, roles, tenant rules, payment provider/webhook, database policies, or schema; unrelated application changes; production changes; network, database, or external-service operations.
- Task IDs: SEC-001, SEC-002, SEC-003.
- Proposed commands and safety classes: No implementation commands are authorized by this plan. Before an approved implementation, inspect exact project-specific commands and scripts; classify any read-only inventory as `SAFE_READ_ONLY`, local checks as `LOCAL_VALIDATION`, and file edits as `FILESYSTEM_MUTATION`. No network, database, or production operation is proposed in this phase.
- Approval required: yes, separately for any implementation in a real target, after target and exact file scope are previewed.
- Side effects and network/database/production impact: Planning has none. Any future implementation is limited to approved local files and checks; no production, database, network, or provider side effects are in scope without separate exact authorization.
- Acceptance criteria:
  1. The owner identifies the actual target, registered entry points, and whether each fixture flow maps to it; if no real counterpart exists, record the findings as fixture-only and defer code remediation.
  2. The product/application owner documents allowed actors, roles, tenant/resource ownership rules, and denied cases for note updates.
  3. The data owner documents the actual query/adapter and effective tenant/data policy relevant to note updates.
  4. The payment owner documents whether invoice changes come from provider events, an administrative action, or another flow, and identifies trusted amount/currency/state sources and any signature/replay controls if a webhook exists.
  5. For a confirmed corresponding flow, implementation acceptance requires authorization before mutation, server-derived tenant/ownership scope for note updates, and server-trusted invoice amount/state with appropriate authorization and audit evidence for manual actions.
  6. Verification evidence covers permitted and denied actors/resources, cross-tenant denial where tenants exist, and invoice amount/state tampering or replay cases where applicable. Each case is marked unverified if no runnable target or test mechanism is supplied.
- Verification and expected evidence: Target/route mapping and owner-approved business rules; reviewed implementation diff; actual results from focused authorization and mutation checks; database-policy evidence if applicable; payment-flow evidence if applicable. No such checks have run. Record commands and results only after an approved implementation.
- Rollback/recovery: For a future approved code change, revert only the approved phase diff using the repository's reviewed recovery procedure; preserve database/payment state and do not attempt data rollback absent an approved migration/recovery plan. No runtime or production rollback is defined by current evidence.
- Residual risks (severity, owner, revisit date/trigger): HIGH, application owner — SEC-F001 remains unresolved until real target/reachability and ownership rules are established and applicable cases verified. HIGH, payment owner — SEC-F002 remains unresolved until the payment/admin flow and trusted state source are established and applicable cases verified. Revisit before implementation approval and before any release of a corresponding system.
- Status: PLANNED; implementation and verification NOT RUN.

### PHASE-DEMO-001: SYNTHETIC DEMO ONLY — approved fixture scope

- Objective: Apply the explicitly approved local fixture hardening and define a focused test for that fixture only. This is a test-only demonstration of specified behavior; it does not establish that any real application is secure.
- Approval: The human explicitly approved this exact test-only scope in the current conversation: modify only `tests/fixtures/vulnerable_app/app.py` so `update_note` rejects actors whose `tenant_id` does not match, rejects non-string or over-2048-character note bodies, and scopes the SQL update by both note ID and tenant ID; add `tests/test_synthetic_demo.py`; run only `python -m unittest discover -s tests -p test_synthetic_demo.py -v`. This planning update does not perform any of those actions.
- Source evidence: SEC-F001 identifies the fixture update without tenant scope (`tests/fixtures/vulnerable_app/app.py:8-13`); SEC-F004 identifies absent request/body bounds at this function. Both are source-pattern findings in a non-production synthetic fixture.
- Scope (files/components): If/when implementation proceeds, only `tests/fixtures/vulnerable_app/app.py` and `tests/test_synthetic_demo.py`. Only the exact unittest command above is in the approved verification scope.
- Out of scope: All other files and commands; real deployment; whether `/api/v1/notes` is a registered or reachable route; roles or authorization rules beyond the tenant-mismatch behavior in this fixture; invoice/payment remediation; network, database, or production effects. These remain unknown or deferred.
- Task IDs: SEC-009.
- Proposed command and safety class: `python -m unittest discover -s tests -p test_synthetic_demo.py -v` (`LOCAL_VALIDATION`), authorized as the sole check for this phase, but not run in this planning-only update.
- Side effects and network/database/production impact: The approved scope is local fixture source and test files plus the named local test command. No network, DB, or production effects are authorized or expected.
- Acceptance criteria: (1) `update_note` rejects an actor when `actor.tenant_id` does not match the note tenant; (2) it rejects a body that is not a string or exceeds 2048 characters; (3) its SQL update is constrained by both note ID and tenant ID; (4) `tests/test_synthetic_demo.py` covers these specified behaviors; (5) only the named test command is run if verification occurs. No criterion establishes route reachability or real-application security.
- Verification and expected evidence: The only authorized check is the named unittest command. No code changes or checks have occurred; all behavior remains UNVERIFIED.
- Rollback/recovery: Revert only the two approved local fixture/test file changes if they are later made; this plan defines no database or runtime recovery action.
- Residual risks (severity, owner, revisit date/trigger): SEC-F001 remains HIGH for any corresponding real application until route reachability, real authorization, tenant/resource model, and data access controls are established and verified. SEC-F002 remains HIGH and invoice/payment remediation is deferred. SEC-F003 and SEC-F005–SEC-F006 remain as previously recorded. SEC-F004 is only partially addressed by this fixture scope; real request parsing, API bounds, and runtime enforcement remain unknown. Deployment, route reachability, and roles beyond this fixture remain unknown/deferred.
- Status: APPROVED SCOPE; NOT STARTED; implementation and verification NOT RUN.

## Deferred and Skipped Risks

| Finding/layer | Reason | Severity | Owner | Revisit trigger |
|---|---|---|---|---|
| SEC-F003 / SEC-F004 | Planned after high-impact mutation flows; actual reset/request paths, mailer behavior, parsing, and infrastructure limits are unknown | MEDIUM | Identity owner / API owner | PHASE-002, after actual paths and controls are identified |
| SEC-F005 / SEC-F006 | Runtime, cookie use, session lifecycle, and deployment config are unknown | MEDIUM | Application owner / deployment owner | PHASE-003, when the actual runtime/configuration is in scope |
| S8 / S10 | No deployment or operational evidence in the synthetic fixture | Unknown | Operations owner | PHASE-004, when a real deployment is identified |
| S6 provider/webhook specifics | No provider, webhook, state machine, or route is supplied | Conditional | Payment owner | Establish whether such a flow exists in PHASE-001 |
| S11 release readiness | No runtime/deployment evidence and no checks run | Not assessed | Release owner | Before release of a real corresponding system |

The approval for PHASE-DEMO-001 is fixture-only. It does not close SEC-F001 or SEC-F004 for a real system, validate the nominal note route, establish roles beyond the fixture tenant check, or authorize SEC-F002 invoice/payment changes.

## Final Release Gate

- Adopted phases verified: None; no implementation or verification has run.
- Failed or skipped checks explained: No checks were run; runtime/deployment checks remain unavailable on current evidence.
- Residual risks accepted by: Not assigned; owners above must validate applicable findings.
- Decision: NOT READY (release readiness of any real corresponding system is unassessed; this is not a release assessment of the synthetic fixture).
