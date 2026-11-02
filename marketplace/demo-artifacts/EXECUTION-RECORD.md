# Demo execution record

## Run identity

- Date: 2026-11-02 (Africa/Cairo)
- Agent: Codex CLI `0.166.0-alpha.5.1`
- Skill: `security-coverage`, installed through Skills CLI into a disposable Codex project
- Disposable workspace: `C:\Users\yosea\AppData\Local\Temp\security-coverage-demo-20261102`
- Product repository was not the target of this demonstration.

## Stages and files

1. `security-assess` wrote only `docs/security/SECURITY-STRATEGY.md`.
2. `security-plan` wrote `SECURITY-PLAN.md`, `SECURITY-TASKS.md`, and `SECURITY-EVIDENCE-LOG.md`; after approval, a planning-only update isolated `PHASE-DEMO-001`.
3. `security-implement` presented the recorded scope and preview, then changed only `tests/fixtures/vulnerable_app/app.py` and `tests/test_synthetic_demo.py` in the disposable workspace.
4. The agent left the task/evidence files unchanged because those documents were excluded from the exact approved two-file scope. This record supplements, but does not alter, the actual pre-implementation evidence log.

## Approval

The human reply was: “Approve this exact test-only scope”. The approved phase was limited to actor/tenant matching, string and 2,048-character body validation, tenant-scoped SQL, one test file, and the single test command below. No database or production effects were authorized.

## Exact verification

```text
python -m unittest discover -s tests -p test_synthetic_demo.py -v
```

Observed output: **5 tests passed; 0 failed; 0 skipped; exit code 0**. The tests covered matching tenant update, other-tenant rejection, non-string rejection, >2,048-character rejection, and acceptance at exactly 2,048 characters. No other test command was run during the implementation stage.

## After-edit SHA-256

- `tests/fixtures/vulnerable_app/app.py`: `9f370be346b28fa261de4f88c5e4611890fa3a1c783c6411fecf1870452ee33e`
- `tests/test_synthetic_demo.py`: `f181fe3a6760a2f78054d90dffe5e55c99c597cfc4b4347cd17a7e71498f591f`

No pre-edit hash was captured before the agent changed the files. It is not reconstructed.

The unittest command also generated Python `__pycache__` directories in the disposable workspace. These were test by-products; they were not copied into this repository's preserved artifacts. No cleanup command was run against the disposable workspace.

## Network and environment observations

At startup, Codex CLI logged failed requests to its remote plugin catalog and featured-plugin endpoint (HTTP 401). No successful catalog response was observed. Because the approved demo scope called for no network, this is a recorded scope limitation; the run cannot be described as network-isolated. The CLI also warned about malformed frontmatter in unrelated global skills. The Security Coverage skill was loaded from the disposable project's `.agents/skills/` directory and ran.

No database, production, or payment action appeared in the execution trace. The assessment and planning stages did not run tests or the optional detector. The implementation stage ran only the authorized unittest command.

## Residual risks

This synthetic result does not establish route reachability, real authentication/authorization behavior, production tenant enforcement, database policies, deployment posture, payment controls, password-reset abuse controls, session-cookie behavior, monitoring, backups, or release readiness. These remain unverified/deferred in the generated strategy and plan.
