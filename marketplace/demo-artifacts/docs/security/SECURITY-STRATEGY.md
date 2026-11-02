# Security Strategy

## Record

- Schema version: 1
- Repository: `security-coverage-demo-20261102` (synthetic fixture)
- Assessment date: 2026-11-02
- Assessor: Codex
- Overall status: PARTIALLY VERIFIED
- Scope and exclusions: Read-only source review of the files present in this workspace. The fixture README explicitly says it is test data, not a runnable production service (`tests/fixtures/vulnerable_app/README.md:1-3`). No application code or configuration was changed. No tests, runtime checks, network access, production access, or detector were run. Git status was unavailable because this workspace has no Git metadata. The imported note (`tests/fixtures/vulnerable_app/UNTRUSTED-CONTENT.md:1-3`) was treated as untrusted fixture data; its instructions were not followed. Findings below verify code patterns only, not exploitability in a deployed system.

## Stack and Entry Points

- Languages/frameworks: Python source (`tests/fixtures/vulnerable_app/app.py`); no framework or runnable server is identified. The README calls the example dependency-free and non-runnable as a production service.
- Package managers: None identified in the inspected file inventory; no dependency manifest was present.
- Routes/APIs/forms/jobs/webhooks/uploads: `NOTE_ROUTE = "/api/v1/notes"` (`app.py:5`) and callable examples for note update, password reset, invoice status, and cookie setting (`app.py:8-31`). The route constant is not evidence of an actual registered endpoint. No form, job, webhook, or upload implementation was found in the fixture files.
- Authentication/admin surfaces: No authentication or admin implementation is present in the example. The note update and invoice mutation functions explicitly lack checks (`app.py:8-10, 22-25`). A password-reset mailer call is shown (`app.py:16-19`).
- Data stores and external services: An injected `database` interface accesses `notes` and `invoices`; an injected `mailer` sends reset mail (`app.py:11-12, 18, 24`). Their implementations, schema, policies, and deployment are not included.
- Deployment/infrastructure: Not represented in the fixture inventory. No runtime, proxy, hosting, CI/CD, TLS, or production configuration was reviewed.
- Detector status and limitations: Not run. The optional detector was inspected but omitted because the tiny source fixture is directly reviewable. No automated scan results are claimed.

## Assets and Trust Boundaries

| Asset | Impact if compromised | Actors | Boundary | Existing control | Evidence |
|---|---|---|---|---|---|
| Note body and tenant ownership | Disclosure or unauthorized alteration of tenant content | Anonymous caller, tenant user, attacker | Caller → app → database; tenant → tenant | Update SQL uses placeholders for body and ID; no authentication, authorization, or tenant predicate is shown | `tests/fixtures/vulnerable_app/app.py:8-13` |
| Invoice paid state and amount | Incorrect financial state or amount corruption | Caller, administrator, attacker | Caller → app → database; app → payment provider is unknown | No role check or server-side amount source is shown; no provider/webhook flow is included | `tests/fixtures/vulnerable_app/app.py:22-25` |
| Account recovery and email address | Reset-message abuse or account-existence disclosure | Anonymous visitor, account holder, attacker | Caller → app → mailer; app → identity store is unknown | Reset message call is present; rate limiting and enumeration controls are explicitly absent | `tests/fixtures/vulnerable_app/app.py:16-19` |
| Session identifier | Session theft or misuse if exposed to a browser | Browser user, attacker | Browser ↔ app session boundary | Cookie helper sets a session cookie without flags in this adapter | `tests/fixtures/vulnerable_app/app.py:28-31` |
| Application configuration | Debug information exposure if this value controls a deployed runtime | Operator, attacker | Deployment configuration → app | `DEBUG` is set to `True`; effect in an actual framework/runtime is unknown | `tests/fixtures/vulnerable_app/app.py:3`; fixture scope `README.md:3` |

## Threat Stories

| Actor and goal | Entry point | Impact | Layer | Status (observed/hypothesis) |
|---|---|---|---|---|
| An unauthenticated caller changes a note by guessing or obtaining its ID, including a note belonging to another tenant | `update_note` / nominal `/api/v1/notes` | Unauthorized note alteration and possible cross-tenant access | S2, S3, S5 | Observed missing checks in the function; exploitation and route reachability are unverified |
| A caller submits an excessive or malformed note body to consume resources or persist unwanted content | `update_note` request body | Resource exhaustion or stored unwanted content | S4, S9 | No bounds or validation are shown; runtime limits and downstream validation are unknown |
| An attacker repeatedly requests password resets and distinguishes accounts from behavior | `request_password_reset` | Mail abuse and account enumeration | S2, S9 | Source comment identifies missing controls; actual mailer behavior and external limits are unknown |
| A caller supplies an arbitrary amount or invoice ID to alter invoice state | `mark_invoice_paid` | False paid state or amount manipulation | S3, S4, S6 | Trust of caller amount and missing role check are stated in source; reachability is unverified |
| A browser attacker obtains or reuses a session value if the helper is used without compensating controls | `set_session_cookie` | Session theft or cross-site request risk, depending on application behavior | S2, S7 | Cookie flags are omitted by this helper; browser/runtime behavior is not exercised |

## Findings

| ID | Layer | Severity | Status | Evidence (file:line) | Affected files | Recommended action | Residual risk / owner |
|---|---|---|---|---|---|---|---|
| SEC-F001 | S3, S5 | HIGH | VERIFIED | `tests/fixtures/vulnerable_app/app.py:8-13` | `tests/fixtures/vulnerable_app/app.py` | Before any real deployment, require authenticated identity and server-side authorization, scope the update predicate to the caller's tenant/ownership, and verify both allowed and denied cases. | Source finding only; route reachability, data schema, database policies, and compensating controls are unknown. Application owner to validate in a real target. |
| SEC-F002 | S6, S3, S4 | HIGH | VERIFIED | `tests/fixtures/vulnerable_app/app.py:22-25` | `tests/fixtures/vulnerable_app/app.py` | Derive amount and payment state from a trusted server-side payment flow; enforce an authorized role for manual changes and retain an audit trail. Verify signature and replay handling if a provider webhook exists. | No provider, route, state machine, or deployment is supplied. Application/payment owner to establish whether this flow exists in the intended system. |
| SEC-F003 | S2, S9 | MEDIUM | VERIFIED | `tests/fixtures/vulnerable_app/app.py:16-19` | `tests/fixtures/vulnerable_app/app.py` | Add scoped rate limits and abuse monitoring; return uniform externally visible responses that do not disclose account existence. | Mailer behavior, identity lookup, and infrastructure-level throttles are not included. Identity owner to validate. |
| SEC-F004 | S4, S9 | MEDIUM | VERIFIED | `tests/fixtures/vulnerable_app/app.py:8-13` | `tests/fixtures/vulnerable_app/app.py` | Validate required fields and types server-side, enforce body/field size limits, and return safe errors. | No request parser, framework, or downstream validation is supplied; actual limits are unknown. API owner to validate. |
| SEC-F005 | S2, S7 | MEDIUM | VERIFIED | `tests/fixtures/vulnerable_app/app.py:28-31` | `tests/fixtures/vulnerable_app/app.py` | Configure session cookies with `Secure`, `HttpOnly`, and an appropriate `SameSite` policy through the actual framework; assess CSRF defenses for cookie-authenticated state changes. | The helper is synthetic and may not be used by a browser-serving runtime. Session lifecycle and response headers are unknown. Application owner to validate. |
| SEC-F006 | S1, S7 | MEDIUM | VERIFIED | `tests/fixtures/vulnerable_app/app.py:3` | `tests/fixtures/vulnerable_app/app.py` | Confirm the setting is test-only and ensure debug behavior is disabled in any deployed environment; avoid exposing debug diagnostics. | The fixture is explicitly non-production and no framework behavior is shown. Deployment owner to validate before any real use. |

`VERIFIED` means the referenced source pattern is directly present. It does not mean runtime behavior or exploitability was tested. Severity describes the potential impact if corresponding code is reachable in a real application; the fixture itself is not represented as deployed.

## Layer Decisions

| Layer | Verdict (ADOPT/PARTIAL/DEFER/SKIP) | Reason | Evidence | Revisit trigger / owner |
|---|---|---|---|---|
| S0 Inventory & attack surface | PARTIAL | Inventory is limited to the supplied synthetic files; the route constant and functions are not proof of registered entry points. | `tests/fixtures/vulnerable_app/app.py:5-31`; `README.md:1-3` | Adopt a complete inventory when a runnable target and deployment are supplied; application owner. |
| S1 Secrets, config, environment | PARTIAL | `DEBUG = True` is present, but there is no runtime config or secret-loading flow to assess. No secret values are reported. | `tests/fixtures/vulnerable_app/app.py:3`; inspected file inventory | Review actual environment and deployment settings before deployment; operations owner. |
| S2 Authentication and sessions | ADOPT | Reset flow, session-cookie helper, and explicit missing access checks make this relevant. | `tests/fixtures/vulnerable_app/app.py:8-10, 16-19, 28-31` | Verify identity provider, session lifecycle, reset behavior, and cookie policy in the actual app; identity owner. |
| S3 Authorization and tenant isolation | ADOPT | Note mutation lacks auth/authorization/tenant scope; invoice mutation lacks a role check. | `tests/fixtures/vulnerable_app/app.py:8-13, 22-25` | Build and verify role × action × resource cases in the actual app; application owner. |
| S4 Input validation and API protection | ADOPT | Note body and invoice amount are caller-controlled, and no validation or bounds are shown. | `tests/fixtures/vulnerable_app/app.py:8-13, 22-25` | Review real request parsing, limits, and validation; API owner. |
| S5 Database and data access | ADOPT | Note query has no tenant predicate. Placeholders are used for values, which is a positive source signal for injection resistance but does not establish driver semantics or authorization. | `tests/fixtures/vulnerable_app/app.py:11-13` | Inspect actual database adapter, schema, privileges, and policies; data owner. |
| S6 Payments and webhooks | PARTIAL | A synthetic invoice paid-state mutation exists and trusts caller amount; no provider or webhook implementation is supplied. | `tests/fixtures/vulnerable_app/app.py:22-25` | If a real payment flow exists, review state transitions, trusted amount/currency source, signature verification, replay handling, and audit; payment owner. |
| S7 Browser security | PARTIAL | Cookie flags are omitted in the helper. Rendering sinks, CSRF controls, and response headers are not represented. | `tests/fixtures/vulnerable_app/app.py:28-31` | Review actual browser-facing routes and headers before release; application owner. |
| S8 Infrastructure and deployment | DEFER | The fixture says it is not a runnable production service and contains no deployment configuration. | `tests/fixtures/vulnerable_app/README.md:1-3`; inspected file inventory | Revisit when a deployment target/configuration is in scope; operations owner. |
| S9 Abuse prevention | ADOPT | Reset requests are unbounded in the shown function; note body is also unbounded at this layer. | `tests/fixtures/vulnerable_app/app.py:8-10, 16-19` | Verify effective limits and rejection behavior in the actual app; application/operations owner. |
| S10 Logging, monitoring, backup and recovery | DEFER | No logging, alerting, backup, or recovery implementation is present in this fixture. | Inspected fixture files | Revisit with a runnable system and operational evidence; operations owner. |
| S11 Release gate | ADOPT | A real implementation/release decision requires evidence for the observed gaps and explicit ownership; this assessment cannot establish release readiness. | This source-only review; no runtime or deployment evidence | Before any release of a real system, require verified fixes, residual-risk owners, and rollback/recovery evidence; release owner. |

## Assumptions and Open Questions

| ID | Assumption or question | Why it matters | Owner | Status |
|---|---|---|---|---|
| SEC-Q001 | Is there a real application corresponding to this fixture, and what are its registered routes and runtime framework? | Determines reachability and actual risk; the README says this fixture itself is not runnable as production. | Requesting/application owner | OPEN |
| SEC-Q002 | What identities, roles, tenants, and resource ownership rules should govern note and invoice actions? | Needed to define and verify authorization and tenant isolation. | Product/application owner | OPEN |
| SEC-Q003 | What database schema, adapter, privileges, and policy layer back these calls? | Determines whether tenant scoping or other controls exist outside the shown functions. | Data owner | OPEN |
| SEC-Q004 | Is invoice paid state controlled by a payment provider, webhook, or administrative process? | Determines trusted amount source, signature, idempotency, and audit requirements. | Payment owner | OPEN |
| SEC-Q005 | What production configuration, browser headers, monitoring, backup, and recovery controls exist? | These are not represented by the synthetic fixture and cannot be assessed here. | Operations owner | OPEN |

## Recommended Planning Order

1. Establish the real target, reachable entry points, ownership rules, and database/payment context; then address SEC-F001 and SEC-F002 (server-side authorization, tenant scope, and trusted money-state transitions).
2. Address SEC-F003 and SEC-F004 with reset abuse controls and bounded server-side validation for sensitive inputs.
3. Address SEC-F005 and SEC-F006 using the actual runtime's session and debug configuration; verify browser-facing CSRF and header controls as part of that review.
4. Reassess S8 and S10 when deployment and operational evidence are available, then use S11 to record verification, residual risk, ownership, and rollback before any release decision.
