# Payments, Webhooks, And Admin Money Flows

Use for S6 phases.

## Review Targets

- Payment intent creation.
- Redirect/callback flows.
- Webhook signature verification.
- Idempotency keys and replay handling.
- Amount and currency source of truth.
- Manual admin marking.
- Audit trail and reporting.

## Rules

- Client redirects are not proof of payment.
- Do not trust client-submitted amount, status, role, or paid timestamp.
- Webhooks must verify provider signatures before changing state.
- Manual changes need admin auth and durable evidence.

## Evidence

Record provider, endpoints, state transitions, duplicate handling, failed signature behavior, and admin audit path.
