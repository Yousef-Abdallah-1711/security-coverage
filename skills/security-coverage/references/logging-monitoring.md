# Logging, Monitoring, Backups, Rollback

Use for S10 phases.

## Security Events

Log these when relevant:

- Admin login success/failure.
- Payment state changes.
- Permission denials.
- Webhook signature failures.
- Rate-limit triggers.
- Backup/restore actions.
- Secret/config load failures.

## Redaction

Logs must not include passwords, tokens, full payment data, private keys, or complete session IDs.

## Recovery

Document:

- Backup location and cadence.
- Restore command or procedure.
- Last restore test.
- Rollback command or procedure.
- Incident owner/contact.

## Evidence

Record sample redacted log lines, backup metadata, restore/rollback proof, and remaining gaps.
