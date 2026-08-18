# Stack Map

Use the repo's existing stack. Do not migrate frameworks as a side effect of security work.

## JavaScript / TypeScript

Signals: `package.json`, `vite.config.*`, `next.config.*`, `tsconfig.json`, `src/`, `app/`, `pages/`.

Useful checks: package audit, typecheck, lint, route review, cookie/session config, server actions/API routes, CSP headers.

## PHP

Signals: `composer.json`, `*.php`, `public/`, `api/`, `admin/`, `.htaccess`.

Useful checks: session handling, CSRF tokens, `htmlspecialchars`, prepared statements, upload handling, local config exposure, web root boundaries.

## Python

Signals: `pyproject.toml`, `requirements.txt`, `manage.py`, `app.py`, `fastapi`, `flask`, `django`.

Useful checks: debug flags, dependency audit, auth decorators, serializer validation, CSRF middleware, migrations.

## Ruby

Signals: `Gemfile`, `config/routes.rb`, Rails directories.

Useful checks: strong params, CSRF, auth filters, mass assignment, secrets credentials, migrations.

## Go

Signals: `go.mod`, `cmd/`, `internal/`.

Useful checks: context timeouts, auth middleware, JSON decoding limits, SQL parameterization, TLS/proxy settings.

## Supabase

Signals: `supabase/`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, RLS policy SQL, client queries.

Useful checks: RLS enabled, service key server-only, anon key limited, policies tested per role, storage bucket policies.

## Payments

Signals: Stripe, Paymob, Paddle, Lemon Squeezy, webhook routes, payment status fields, admin payment pages.

Useful checks: webhook signature, idempotency, amount/currency source of truth, replay handling, manual admin audit.

## Infrastructure

Signals: Dockerfile, compose files, GitHub Actions, Vercel/Netlify configs, Nginx/Apache, `.htaccess`, cron, backup files.

Useful checks: public file exposure, CI secrets, TLS headers, build artifacts, source maps, backup/restore.
