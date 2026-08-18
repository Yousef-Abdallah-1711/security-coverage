---
name: security-assess
description: Assess the current repository security posture and write docs/security/SECURITY-STRATEGY.md with attack surface, threat model, layer decisions, gaps, and assumptions.
metadata:
  short-description: Create a security strategy from repo inspection
---

# Security Assess

Assess the current repository and create or update:

```text
docs/security/SECURITY-STRATEGY.md
```

Do not assume previous chat context. Inspect the repository from its root.

## Safety

- Do not modify application code during assessment.
- Do not mutate production, databases, payment state, hosting, DNS, or live config.
- Do not expose secret values. Mention only variable names and file locations.
- Do not mark a layer safe without checking representative files.

## Workflow

1. Create `docs/security/` if it does not exist.
2. Inspect files, routes, APIs, forms, auth, sessions, roles, admin screens, database access, uploads, payments, webhooks, browser entry points, deployment files, logs, backups, and environment examples.
3. If a detector exists at `skills/security-coverage/scripts/detect_security_stack.py`, run:

   ```bash
   python3 skills/security-coverage/scripts/detect_security_stack.py . --json
   ```

   If it does not exist, continue manually.
4. Classify every security layer as `ADOPT`, `PARTIAL`, `DEFER`, or `SKIP`.
5. Write `SECURITY-STRATEGY.md` with the exact structure below.

## Security Layers

- S0 Inventory & attack surface
- S1 Secrets, config, and environment
- S2 Authentication and sessions
- S3 Authorization and roles
- S4 Input validation and API protection
- S5 Database, Supabase, RLS, and data access
- S6 Payments, webhooks, and admin money flows
- S7 Browser security: XSS, CSRF, CSP
- S8 Infrastructure, deploy, and file permissions
- S9 Abuse protection: rate limits, spam, brute force
- S10 Logging, monitoring, backups, rollback
- S11 Final production security release gate

## Output

Write:

```markdown
# Security Strategy

## Scope

## Stack And Entry Points

## Assets

## Trust Boundaries

## Attack Surface

## Layer Decisions

| Layer | Decision | Reason | Evidence | Notes |
|---|---|---|---|---|

## Threat Model

## Current Controls

## Gaps

## Assumptions And Open Questions

## Recommended Planning Order
```

Stop when the strategy is detailed enough for `/security-plan` to create executable phases without guessing.
