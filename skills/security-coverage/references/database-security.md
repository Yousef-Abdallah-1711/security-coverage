# Database, Supabase, RLS, And Data Access

Use for S5 phases.

## Review Targets

- Connection strings and service credentials.
- SQL parameterization or query builder safety.
- Migrations and schema drift.
- Sensitive columns.
- Row Level Security policies.
- Storage bucket policies.
- Admin/service-role boundaries.

## Supabase Notes

- Service-role keys must stay server-side.
- RLS should be enabled on tables accessed from clients.
- Policy predicates need tests for anonymous, owner, non-owner, admin, and revoked users where relevant.
- Keep anon keys out of privileged server operations.

## Evidence

Record table/policy list, sensitive fields, role checks, and any policy test outputs.
