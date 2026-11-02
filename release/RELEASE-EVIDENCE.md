# Release evidence

## State

- Baseline: `d003f4805dea8686a00205c6bf1efb03399a3ba5`
- Branch: `main`
- Worktree: isolated temporary clone; initial tree was clean
- Push: NOT ATTEMPTED — GitHub CI is unverified and the Codex host attempted outbound catalog requests despite the demo's no-network scope
- Agensi: not submitted
- Final commit: none

## Local checks

| Check | Command/action | Result |
|---|---|---|
| Python tests | `python -m unittest discover -s tests -v` | PASS: final post-change run 35 tests; one symlink test skipped because Windows symlink creation is unavailable |
| Approved synthetic tests | `python -m unittest discover -s tests -p test_synthetic_demo.py -v` | PASS in product worktree: 5 tests, 0 failures, 0 skips; also PASS in the separate Codex demo workspace: 5 tests, exit code 0 |
| Skill/package source validation | `python scripts/build_agensi_package.py --check` | PASS: one skill, valid name/frontmatter, 20 package files including license |
| Archive | `python scripts/build_agensi_package.py` | PASS: `dist/security-coverage-agensi.zip`, 23,526 bytes, SHA-256 `ef5466600fe819f5885666cbcb1ac91893f130a7e6f974a991cbf0df5b237f34`; archive integrity and one SKILL.md verified |
| Bash syntax | `C:\Program Files\Git\bin\bash.exe -n install.sh` | PASS |
| PowerShell parse | PowerShell AST parser on `install.ps1` | PASS |
| Claude repository commands | SHA-256 compare for `.claude/commands/` and shared `commands/` adapters | PASS: all three match |
| Installer smoke | PowerShell Claude local install/uninstall and Git Bash Codex local install/uninstall in disposable Unicode/space path | PASS; no real user home touched |
| Skills CLI discovery | `npx.cmd --yes skills add . --list` with Skills CLI 1.7.4 | PASS: Skills CLI identified Codex and found exactly one `security-coverage` skill |
| Skills CLI installation | `npx.cmd --yes skills add <local repo> --skill security-coverage --agent codex --copy --yes` from disposable project | PASS: copied canonical skill and references under `.agents/skills/security-coverage` |
| JSON | Python JSON parsing of package and plugin metadata | PASS |
| Git whitespace | `git diff --check` | PASS after template cleanup |
| Python 3.8 syntax | Parse all repository `.py` files with `ast.parse(..., feature_version=(3, 8))` | PASS: 7 Python files |
| Branding | Generated cover/logo opened and dimensions checked | PASS: cover 2172×724 (PNG source plus 2172×724 WebP); logo 512×512 PNG |

The detector test suite covers empty/multi-stack fixtures, comments, large files, binary files, unreadable files, file/depth caps, exit codes, JSON, synthetic input, and symlink escape (the latter was skipped locally). GitHub Ubuntu CI is configured to run the symlink test; no GitHub Actions result is claimed.

After the local checks, `git fetch origin main` confirmed `origin/main` remained at `d003f4805dea8686a00205c6bf1efb03399a3ba5`, matching the isolated clone HEAD. The first shell-quoted Python 3.8 syntax check was malformed; it was corrected and passed as recorded above.

## Agent runtime and demo

A real end-to-end workflow was completed in a disposable synthetic workspace with Codex CLI `0.166.0-alpha.5.1`. Skills CLI installed the single `security-coverage` skill into `.agents/skills/security-coverage/`. The agent produced an assessment strategy and planning artifacts, handled the hostile imported note as untrusted, presented a preview for `PHASE-DEMO-001`, and made only the explicitly approved source/test changes in the disposable target. The approved focused test passed: 5 tests, exit code 0. The same focused command also passed in the product worktree after its approved test file was expanded to cover the exact 2,048-character boundary: 5 tests, exit code 0. The complete product-worktree suite was then rerun: 35 tests, 1 Windows symlink skip, 0 failures.

The implementing agent left its task/evidence documents unchanged because those were excluded from the exact two-file approval. The original pre-implementation documents are preserved in `marketplace/demo-artifacts/`; `POSTRUN-EVIDENCE.md` is a separate, reviewer-curated result record. Before/after hashes were not both captured; only post-edit hashes are recorded. Python generated ignored `__pycache__` directories in the disposable demo workspace as a test by-product.

**Network limitation:** Codex startup attempted remote plugin-catalog and featured-plugin requests; both logged HTTP 401. No successful catalog response was observed, but this run is not network-isolated and does not satisfy the phase's no-network expectation. No database or production action appeared in the trace. Codex also emitted unrelated malformed-frontmatter warnings from globally installed skills. The prior Codex CLI `0.155.0-alpha.16.3` attempt had stalled; the newer CLI run completed. No Claude workflow run was attempted.

The real assessment, plan, preview, approved remediation, focused verification, and untrusted-content scenario are preserved. No decline/refusal scenario or resume scenario was run. No GitHub Actions result is claimed. Do not claim production readiness or marketplace approval.

## Marketplace package

- Artifact: `dist/security-coverage-agensi.zip` (ignored build output; not committed)
- Exactly one SKILL.md; complete relative references/templates/script; no installers, Git internals, executables, or dependency directories
- Size: 23,526 bytes (well under the specified 50 MB upload limit)
- SHA-256: `ef5466600fe819f5885666cbcb1ac91893f130a7e6f974a991cbf0df5b237f34`
- ZIP extracted and integrity checked by the package builder test
- Listing draft: `marketplace/listing.md`; actual demo artifacts and post-run record are in `marketplace/demo-artifacts/`; listing not submitted

## Gate decision

- A Repository integrity: NOT VERIFIED for final release until Git diff and remote synchronization are rechecked
- B Architecture: PASS locally
- C Security: FAIL — Codex host attempted outbound catalog requests during the explicitly no-network demo phase; the skill did not request these, but the runtime was not network-isolated
- D Testing: PARTIAL — post-change full local suite passed (35 tests, one platform skip); GitHub Actions remains unverified
- E Distribution: PARTIAL — Skills CLI and ZIP locally verified; other agents and Agensi delivery unverified
- F Documentation: PASS locally, with supported-agent runtime claims explicitly limited
- G Demonstration: PARTIAL — actual assess/plan/preview/approved fix/verify run completed and evidence is preserved; no refusal scenario, pre-edit hashes, or network-isolated run
- H Git release: BLOCKED — conditional push authorization requires all mandatory release gates; no commit or push made
