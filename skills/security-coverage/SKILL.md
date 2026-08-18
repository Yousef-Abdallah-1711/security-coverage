---
name: security-coverage
description: Assess, plan, and implement layered security coverage for an application repo, producing strategy, plan, tasks, and evidence artifacts. Use when the user asks for security audit, hardening, appsec coverage, production security readiness, or the /security-* commands.
metadata:
  short-description: Layered security audit and hardening workflow
---

# Security Coverage

Security Coverage turns "is this safe enough to ship?" into a layered, evidence-backed workflow.

Use this skill for:

- `/security-assess`: decide which security layers apply and write `docs/security/SECURITY-STRATEGY.md`.
- `/security-plan`: convert the strategy into `SECURITY-PLAN.md`, `SECURITY-TASKS.md`, and an empty evidence log.
- `/security-implement`: execute one safe phase at a time and record evidence.

Do not create or use a slides command. Slide/session material can be derived later from the docs, but it is not part of this plugin's command surface.

## Non-Negotiables

- Do not expose secrets in chat, docs, logs, screenshots, or evidence. Redact values and keep only the variable/key name plus location.
- Do not mutate live production systems, payment state, user data, DNS, hosting, or databases without explicit user approval for that exact mutation.
- Do not silently weaken security controls to reach green: no disabling auth, skipping checks, broadening CORS, turning off RLS, adding `--no-verify`, or swallowing failures.
- Do not treat scanner output as truth without reading representative code. Heuristics point to surfaces; humans/agents still verify behavior.
- Do not mix unrelated product fixes into a security phase. If a real application bug blocks security validation, record it and ask before broadening scope.

## Layers

Security work is organized into these layers:

| Layer | Name |
|---|---|
| S0 | Inventory & attack surface |
| S1 | Secrets, config, and environment |
| S2 | Authentication and sessions |
| S3 | Authorization and roles |
| S4 | Input validation and API protection |
| S5 | Database, Supabase, RLS, and data access |
| S6 | Payments, webhooks, and admin money flows |
| S7 | Browser security: XSS, CSRF, CSP |
| S8 | Infrastructure, deploy, and file permissions |
| S9 | Abuse protection: rate limits, spam, brute force |
| S10 | Logging, monitoring, backups, rollback |
| S11 | Final production security release gate |

A layer can be `ADOPT`, `PARTIAL`, `DEFER`, or `SKIP`. A documented skip is acceptable; a silent gap is not.

## Command Routing

For `/security-assess`:

- Run `scripts/detect_security_stack.py <repo>` when Python is available.
- Read `references/layers.md`, `references/threat-model.md`, and `references/stack-map.md`.
- Use `templates/SECURITY-STRATEGY.md`.

For `/security-plan`:

- Require `docs/security/SECURITY-STRATEGY.md`.
- Read `references/layers.md` and `references/gates.md`.
- Read specific domain references only for adopted or partial layers.
- Use `templates/SECURITY-PLAN.md`, `templates/SECURITY-TASKS.md`, and `templates/SECURITY-EVIDENCE-LOG.md`.

For `/security-implement`:

- Require `SECURITY-PLAN.md` and `SECURITY-TASKS.md`.
- Read `references/gates.md` and the domain reference for the current phase.
- Update `SECURITY-EVIDENCE-LOG.md` with actual command output, findings, decisions, and residual risk.

## Evidence Standard

Every completed phase needs:

- The exact command(s) run from the repo root.
- Real output summary: counts, status, duration, or scanner finding IDs.
- Security result: what is now protected or what remains exposed.
- Zero unexplained skips.
- A rollback or recovery note when configuration/code changed.

## Default Phase Order

1. S0 Inventory
2. S1 Secrets/config
3. S4 API/input validation
4. S2 Authentication
5. S3 Authorization
6. S5 Data access
7. S6 Payments/admin money flows
8. S7 Browser security
9. S9 Abuse protection
10. S8 Infrastructure
11. S10 Monitoring/backups
12. S11 Final release gate

Move the highest-risk area earlier when dependencies allow. For example, payment/webhook security can move before browser security once API/data prerequisites are ready.
