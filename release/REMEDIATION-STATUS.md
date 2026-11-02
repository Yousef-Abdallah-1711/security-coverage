# Audit remediation status

Baseline: `d003f4805dea8686a00205c6bf1efb03399a3ba5` (2026-11-01 audit). Implementation is pushed to `main` at `3078023b7a507fcd3fe91a969699c910247f06c2`; GitHub Actions run 41389407946 passed all 9 jobs. No marketplace submission was made.

| Finding | Change | Verification | Status |
|---|---|---|---|
| F-01 phase approval | Canonical skill and command adapter require explicit approval for exact scope; preview details defined | Adapter contract test passes; Codex presented and applied one specifically approved demo phase; refusal behavior remains untested | PARTIAL — one approved flow observed; refusal path remains untested |
| F-02 Claude copy path | README rewritten; installer copies commands from the canonical source | README link check and temporary PowerShell install/uninstall smoke pass | FIXED locally |
| F-03 standalone skills | Removed three duplicate workflow SKILL.md files; one canonical skill covers all stages | Skills CLI 1.7.4 lists one skill and installs it in a disposable project | FIXED locally |
| F-04 installer deletion | Shared installer uses per-file ownership manifest, collision checks, hash-aware uninstall, backups and rollback | 35-test post-change suite (one Windows symlink skip); PowerShell and Bash local install/uninstall smoke in disposable Unicode/space path | FIXED locally; production agents not tested |
| F-05 tests/compatibility | Added unit/contract/packaging/installer tests and CI matrix; fixed Windows unreadable-file mock portability | 35 local tests pass with one Windows symlink skip; GitHub Actions run 41389407946 passes all 9 jobs across Python 3.8/3.11/3.13 on Windows and Ubuntu plus shell syntax checks | FIXED |
| F-06 output schemas | Reworked strategy/plan/tasks/evidence templates and gates around stable IDs and consistent fields | Template contract test passes | FIXED locally |
| F-07 detector completeness | Bounded traversal, warnings, symlink handling, binary skip, status schema v2, Swift/Dart support, clearer patterns | Synthetic detector tests pass; symlink case skipped on local Windows host and passes on GitHub runners | FIXED LOCALLY AND IN CI |
| F-08 prompt injection | Canonical skill states repository input is untrusted and cannot override trusted instructions | Codex assessment ignored the hostile imported note and did not reproduce secrets or false test claims; broader agent behavior remains unverified | PARTIAL — agent behavior unverified |
| F-09 repository docs | Replaced owner-specific credential/remotes guidance; added SECURITY.md and concise contributor guidance | README local-link test passes | FIXED locally |
| F-10 Agensi listing/demo | Listing draft, brand assets and one-skill package built | ZIP validation and actual Codex synthetic demo pass locally; startup attempted remote catalog requests, no Agensi submission | PARTIAL — demo executed; network isolation and marketplace submission remain unverified |
| F-11 coverage claims | Added explicit limitations and evidence statuses | README/skill language reviewed; no certification claims | FIXED locally |

| Task | Status | Evidence/limitation |
|---|---|---|
| SEC-001 skill/package boundaries | DONE | Single Skills CLI skill; ZIP includes one SKILL.md and supporting relative resources |
| SEC-002 mandatory phase approval | PARTIAL | One Codex approved-phase preview and implementation observed; refusal path and other agents untested |
| SEC-003 Claude installation docs | DONE | Corrected README and successful disposable installer smoke |
| SEC-004 Agensi package validation | PARTIAL | ZIP created and validated; actual demo recorded; listing is not submitted and host network isolation is unverified |
| SEC-005 installer safety | DONE | Ownership-aware implementation and unit/smoke tests; Windows and Ubuntu CI passed |
| SEC-006 output contract alignment | DONE | Templates, references, and instruction text aligned; validator tests pass |
| SEC-007 tests and agent verification | DONE FOR REPOSITORY CI | Full suite (35 tests, one platform skip), focused Codex demo, and all 9 jobs in GitHub Actions run 41389407946 passed; other agent runtimes remain unverified |
| SEC-008 prompt-injection boundary | PARTIAL | Explicit policy added; one hostile-note runtime case passed; broad semantic coverage remains unverified |
| SEC-009 detector reliability | DONE | Synthetic edge cases pass; Windows symlink case passed on GitHub runners |
| SEC-010 detector false positives | PARTIAL | Broad generic terms narrowed; heuristics remain approximate |
| SEC-011 layer examples | PARTIAL | Layer applicability/evidence/failure criteria expanded; no per-framework executable examples |
| SEC-012 doc separation | DONE | End-user and contributor docs separated; sensitive Git token examples removed |
| SEC-013 framework profiles | DEFERRED | No evidence supports adding profiles for v1 |
| SEC-014 schema version/migration | PARTIAL | Schema version fields added; migration guidance for historic user reports remains unimplemented |
