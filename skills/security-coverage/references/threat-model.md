# Threat Model Guide

Use this during `/security-assess`.

## Minimum Model

Capture:

- Assets: data, money, accounts, admin powers, files, secrets, reputation.
- Actors: anonymous visitor, customer, admin, support, service worker, third-party provider, attacker.
- Entry points: public pages, forms, APIs, webhooks, admin pages, uploads, scheduled jobs, deployment access.
- Trust boundaries: browser/server, app/database, app/payment provider, admin/public, tenant/tenant, CI/production.
- Abuse stories: concrete attacker goals in plain language.

## Questions Worth Asking

Ask only when the repo cannot reveal the answer:

- Which data would be worst to leak?
- Which users or customers require separation?
- Which money-flow changes are legally or financially sensitive?
- Which systems are production today?
- Who can approve live security mutations?

## Output Shape

Prefer short, concrete bullets:

```text
Asset: payment status
Actor: public visitor with a copied request
Boundary: browser -> /api/payment_intent.php -> database
Threat: forged payment state or duplicated payment record
Control: server-side payment status remains pending; admin marking requires login
Gap: no webhook signature verification found
Layer: S6 PARTIAL
```
