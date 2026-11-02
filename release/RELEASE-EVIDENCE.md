# Release evidence

## State

- Baseline: `d003f4805dea8686a00205c6bf1efb03399a3ba5`
- Branch: `main`
- Worktree: isolated temporary clone; initial tree was clean
- Push: pushed to `origin/main`; final implementation commit at evidence collection: `3078023b7a507fcd3fe91a969699c910247f06c2`
- GitHub CI: PASS — run [41389407946](https://github.com/Yousef-Abdallah-1711/security-coverage/actions/runs/41389407946), all 9 jobs successful
- Agensi: not submitted
- Final code commit: `3078023b7a507fcd3fe91a969699c910247f06c2`; this evidence update is committed separately

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

The detector test suite covers empty/multi-stack fixtures, comments, large files, binary files, unreadable files, file/depth caps, exit codes, JSON, synthetic input, and symlink escape. The symlink test was skipped locally because this Windows host lacks symlink creation permission and passed on GitHub runners. GitHub Actions run 41389407946 passed all 9 jobs across Python 3.8, 3.11, and 3.13 on Ubuntu and Windows, plus Bash and PowerShell syntax checks. The prior Windows failures in run 41388990184 were addressed by mocking `Path.open` and matching the unique fixture basename to tolerate Windows 8.3 temp-path aliases.

The final code commit was pushed to `origin/main`; local HEAD and `origin/main` both resolved to `3078023b7a507fcd3fe91a969699c910247f06c2` after the successful CI run. Release-evidence and remediation-status updates are being committed after that code commit and do not change application or test code.

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

- A Repository integrity: PASS for code commit `3078023`; evidence-doc follow-up is pushed and remote synchronization rechecked
- B Architecture: PASS locally
- C Security: FAIL — Codex host attempted outbound catalog requests during the explicitly no-network demo phase; the skill did not request these, but the runtime was not network-isolated
- D Testing: PASS — 35 local tests passed (one platform-specific skip); all 9 GitHub Actions jobs passed on run 41389407946
- E Distribution: PARTIAL — Skills CLI and ZIP locally verified; other agents and Agensi delivery unverified
- F Documentation: PASS locally, with supported-agent runtime claims explicitly limited
- G Demonstration: PARTIAL — actual assess/plan/preview/approved fix/verify run completed and evidence is preserved; no refusal scenario, pre-edit hashes, or network-isolated run
- H Git release: PASS — implementation pushed to `main` and CI passed; no marketplace submission made

## 2026-11-02 release candidate continuation

Candidate work is on `release/security-coverage-v1-readiness`, based on `7f982bf6f36da35dfa20d2d19cb2755a9f3c27a7`. The local suite now contains 40 tests: all pass, with one Windows symlink capability skip. Docker `--network none` verification passed for detector/package only; image setup ran before isolation. Local Skills CLI v1.7.4 candidate discovery and disposable install passed. Candidate package is 22 files / 28,743 bytes / SHA-256 `c7ed79700fbe2bf7764c8132cdc8bc1a31582fc5ce924f4aebf9b7377bc11bfb`.

Mandatory release gates remain open: strict host-level no-network-attempt evidence; actual runtime refusal, ambiguous approval, scope expansion, evidence scope, and resume/recovery cases; hosted candidate CI and Linux symlink run; fresh secret scan and full installer matrix. Therefore no merge/push to `main` and no Agensi submission. See `FINAL-PRODUCTION-RELEASE-REPORT.md` for details and any later candidate CI evidence.

## Candidate hosted CI and remote distribution result (2026-11-02)

Candidate code commit `2c58ae308a887082976c9456e11a394fbbb97f36` passed all 9 jobs in PR run [41391053531](https://github.com/Yousef-Abdallah-1711/security-coverage/actions/runs/41391053531), including Python 3.8/3.11/3.13 on Ubuntu and Windows, Linux symlink coverage, offline detector/package isolation, Bash syntax, and PowerShell syntax. The first run failed the offline script with exit 126 because it lacked the executable bit; the mode was corrected and the subsequent complete run passed.

Skills CLI 1.7.4 installed the remote candidate from a temporary no-slash branch ref at the same candidate SHA; one skill, 21 files and 14 references were installed, and the installed `SKILL.md` hash matched the candidate. A slash-delimited branch URL was misparsed by the CLI as ref `release`; remote-main installation has not occurred because the candidate remains unmerged.

This CI/distribution evidence does not clear the mandatory agent-host no-network-attempt, approval refusal, evidence/resume, or runtime compatibility gates. PR #1 remains draft and must not be merged. `main` remains at `7f982bf6f36da35dfa20d2d19cb2755a9f3c27a7`.

The no-slash helper ref was deleted after its install verification; only the release candidate branch remains pushed.

Final report/evidence candidate HEAD `961fd1490baaf6704f3e03ea004562efc8e1462c` passed all 9 jobs in Actions run [41391292195](https://github.com/Yousef-Abdallah-1711/security-coverage/actions/runs/41391292195). That run covers all Python versions on Windows and Ubuntu, Linux symlink handling, shell/PowerShell syntax, and offline detector/package isolation. The release branch remains draft PR #1; no main merge or Agensi submission occurred.
