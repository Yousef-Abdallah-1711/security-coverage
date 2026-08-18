# Authorization And Roles

Use for S3 phases.

## Matrix

Build a role-action-resource matrix:

```text
Role | Action | Resource | Expected | Enforcement point | Evidence
anonymous | view admin dashboard | dashboard | deny | server route | 302 to login
user | update another tenant record | record | deny | policy/controller | 403
admin | mark payment paid | payment intent | allow | admin route | audit row
```

## Checks

- Backend enforcement, not only hidden UI.
- Direct object references.
- Tenant or owner scope.
- Revoked, inactive, or deleted users.
- Admin-only routes and APIs.
- Service-role usage.

## Gate

A phase is not green until every adopted protected action has at least one allow and one deny check, or a documented reason.
