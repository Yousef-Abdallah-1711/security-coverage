# Resume and Schema Migration

## Persistent state after interruption

Treat the repository state and the four persistent artifacts as the source of truth, not prior conversation memory:

- `docs/security/SECURITY-STRATEGY.md`
- `docs/security/SECURITY-PLAN.md`
- `docs/security/SECURITY-TASKS.md`
- `docs/security/SECURITY-EVIDENCE-LOG.md`

At the start of a resumed stage:

1. Confirm repository root, branch, working-tree changes, and relevant file hashes.
2. Read the strategy, plan, task register, and full append-only evidence log that exist.
3. Reconcile task status with actual files and recorded commands. Mark discrepancies `BLOCKED` or `UNVERIFIED`; do not assume a prior agent completed work.
4. Identify completed, partial, failed, deferred, and pending tasks. Do not repeat migrations, deployments, data changes, or other side effects blindly.
5. Revalidate the exact approval reference. Continue only if the approved phase, files, commands, network requirements, and side effects still match. Otherwise stop and request fresh approval.
6. Keep failed verification incomplete, append its actual failure, and resume from the observed state after scope is re-approved.

## Schema versions

- Schema v1 is supported as read-only legacy input. It may be summarized with missing fields explicitly marked `UNVERIFIED`.
- New artifacts use schema v2 and include stable record/finding/task IDs, layer, severity, evidence, verification state, risk owner, approval scope, phase status, test results, skips, and timestamps where applicable.
- Never silently rewrite a v1 file or claim missing v2 fields are verified.
- If a v1 file must be updated, preview the migration separately. Require approval for both the unchanged archival copy (for example `SECURITY-STRATEGY.schema-v1.md`) and the v2 destination. Do not move, delete, or overwrite the source.
- Preserve original text and all findings/evidence in the archived copy. In the v2 output, map only facts that can be traced to the source; use `UNVERIFIED` for absent ownership, severity, approval, or test details. Record the source hash and migration mapping in an evidence entry.
- If an existing v1 record cannot be migrated without guessing, retain it and ask for missing information. A migration preview is not migration approval.

## Approval and evidence scope

Every implementation preview separately names:

1. Application code/configuration/tests/migrations.
2. Workflow documents (strategy, plan, task list, evidence log).
3. Exact verification commands, safety class, expected effects, and network needs.

If the user approves application files and the evidence log, update the task status and append actual outcomes, failed/skipped checks, residual risk owner, and gate result. If evidence files are excluded, leave them byte-identical and return the execution summary in the response; say persistent workflow state was not updated.
