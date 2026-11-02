# Concise Verification Examples

Use only examples that match an adopted layer and the repository's actual framework. These are review patterns, not claims that every application needs every control.

| Layer | Example positive check | Example negative/failure check |
|---|---|---|
| S0 inventory | Route inventory is compared with deployed route configuration; each owner and trust boundary is named | A production route absent from the reviewed inventory blocks release |
| S1 secrets/config | Secret scanner sees only variable names and locations; a rotation runbook is reviewed without displaying values | A committed live credential or debug default blocks release and triggers out-of-band rotation |
| S2 authentication | Login establishes a session with expected expiry and rotation | Expired/revoked session cannot access a protected route; reset token is single-use and expires |
| S3 authorization | Table-driven role × action × resource cases allow the intended owner/admin action | Anonymous, non-owner, and different-tenant reads/writes are denied server-side |
| S4 API/input | Valid request schema reaches the handler; size and content-type limits are enforced | Oversized, malformed, wrong-type, or disallowed URL inputs fail before side effects |
| S5 database | Runtime role has only required table/operation grants; parameterized query is reviewed | Cross-tenant query and RLS policy tests return no other tenant's rows |
| S6 payments | Valid signed webhook changes one intended state and records its event ID | Bad signature, replayed event, duplicate delivery, client-set amount/status, and unauthorized refund do not mutate state |
| S7 browser | Response headers contain intended cookie flags and CSP; rendered text is escaped | CSRF token absence and XSS payload fixtures are rejected/escaped at the actual sink |
| S8 infrastructure | Non-production secrets and least-privilege deploy permissions are checked in configuration | Backup/config file is publicly served or a CI token can deploy outside its environment |
| S9 abuse | Rate-limit test records threshold, key scope, window, and retry response | Repeated login/reset or oversized expensive request is throttled without unbounded work |
| S10 monitoring/recovery | Redacted security event reaches the expected alert; a restore drill records duration and owner | Secret-bearing log sample or untested claimed backup restoration fails the gate |
| S11 release | Every adopted phase has evidence, risk owner, expiry/revisit trigger, and rollback | Failed required check, unexplained skip, or missing risk owner keeps release `NOT READY` |

For each adopted example, record the exact test or manual procedure, command/result, environment, and what the evidence does not establish. Never run payment, production, or destructive examples against live systems as part of repository review.
