# Security Layers

Use these layers to decide scope and phase order. Every layer receives one verdict:

- `ADOPT`: implement and gate now.
- `PARTIAL`: implement the most important subset now and document the gap.
- `DEFER`: intentionally postpone with owner/date/trigger.
- `SKIP`: not relevant to this repo or deployment model.

## S0 Inventory & Attack Surface

Proves the team knows what can be attacked.

Look for routes, API endpoints, admin panels, cron jobs, webhooks, background workers, storage buckets, uploaded files, public directories, auth providers, databases, third-party services, and deployment boundaries.

Skip only for non-runnable docs/templates with no deployed surface.

## S1 Secrets, Config, And Environment

Proves secrets are not committed or exposed and defaults fail closed.

Check `.env*`, local config, committed keys, service-role tokens, debug flags, sample config, secret loading, and public build variables.

Do not print secret values. Record names and file paths only.

## S2 Authentication And Sessions

Proves identity flows are protected.

Check login, logout, session rotation, expiry, cookies, password reset, OAuth callbacks, admin login, rate limiting, and account recovery.

## S3 Authorization And Roles

Proves protected actions enforce role, tenant, ownership, and revocation rules.

Check anonymous access, ordinary users, admins, inactive users, cross-tenant access, direct object access, and backend enforcement.

## S4 Input Validation And API Protection

Proves untrusted input is validated and rejected safely.

Check request methods, content types, body size, schema validation, normalization, output encoding, command/file path handling, and error responses.

## S5 Database, Supabase, RLS, And Data Access

Proves data access rules match authorization.

Check migrations, policies, service-role usage, client-side queries, backups, indexes for policy predicates, and sensitive columns.

## S6 Payments, Webhooks, And Admin Money Flows

Proves money state changes are authentic, idempotent, audited, and admin-only.

Check webhook signatures, replay handling, manual payment marking, idempotency keys, amount/currency trust, admin access, and audit logs.

## S7 Browser Security

Proves the browser cannot become a privilege escalation path.

Check XSS, CSRF, CSP, cookie flags, unsafe links, iframe policy, mixed content, third-party scripts, and DOM injection.

## S8 Infrastructure, Deploy, And File Permissions

Proves deploy configuration does not expose private files or unsafe services.

Check web roots, `.git` exposure, backups, local credentials, logs, upload dirs, chmod, server config, TLS, cron, containers, and CI variables.

## S9 Abuse Protection

Proves expensive or sensitive actions resist brute force and spam.

Check rate limits, CAPTCHA alternatives, lockouts, email abuse, payment retries, signup abuse, password reset abuse, and resource exhaustion.

## S10 Logging, Monitoring, Backups, Rollback

Proves incidents can be detected and recovered.

Check security events, redaction, alerting, backup freshness, restore test, rollback path, retention, and incident contact.

## S11 Final Release Gate

Proves selected layers have evidence and accepted residual risk.

Require all adopted phase gates, unresolved-risk table, deployment checklist, owner signoff, and rollback plan.
