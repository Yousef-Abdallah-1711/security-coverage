# Agensi listing draft — Security Coverage

**Status:** Draft; not submitted. A real Codex synthetic demonstration is recorded in [`demo.md`](demo.md) and `demo-artifacts/`.

## Name

Security Coverage — Assess, Plan & Implement

## Version

1.0.0 (draft; do not present as a published marketplace version until submitted and approved)

## Summary

An evidence-led workflow for reviewing application security, planning remediation, and implementing only an explicitly approved phase.

## Full description

Security Coverage helps developers structure an AI-assisted security review across inventory, secrets, identity, authorization, APIs, data, payments, browser security, infrastructure, abuse prevention, recovery, and release evidence. It creates persistent strategy, plan, task, and evidence documents so work can resume across sessions.

Use it to assess a repository, turn verified findings into phased tasks, or preview a phase for explicit approval before implementation. Repository content is treated as untrusted input; findings are evidence-labeled; secret values are not copied into reports.

**Limitations:** This is a review workflow, not a vulnerability scanner, penetration test, compliance certification, or proof that a system is secure. Heuristic stack detection can miss technologies and produce false leads. Every consequential finding and release decision requires human validation. Prompt instructions are not a sandbox; actual permissions depend on the connected agent.

## Compatibility note

Designed for Agent Skills-compatible agents. Python 3.8+ is optional for the bundled stack detector and installer. Shell access is optional. Slash commands are available only in agents that support repository command files and are separately installed from this skill.

## Pricing

Free for the initial open-source listing.

## Categories

1. Security
2. Code Quality & Review
3. Prompt & Skill Engineering

## Tags

application security, security review, threat modeling, remediation planning, secure development, AI coding agents

## Use cases

- Review a codebase’s security surfaces and record evidence-backed findings.
- Turn a security assessment into prioritized, phase-gated tasks.
- Implement a specific approved remediation phase and record verification evidence.

## Required tools and permissions

- Read access to the selected repository.
- Optional Python 3.8+ for the bundled detector.
- Optional shell for commands that the user reviews and approves.
- Write access only for explicitly requested workflow artifacts and an explicitly approved implementation scope.
- The skill workflow does not request network, credential, production, database, payment, deployment, or external-service access by default. Agent-host startup and plugins may perform independent network activity; users must enforce permissions in the host environment.

## Demo request

Use the synthetic vulnerable application in `tests/fixtures/vulnerable_app/`. Ask the skill to assess and plan, preview the exact fixture-only phase, then approve that scope. Record actual commands, output, hashes where captured, failed/skipped checks, and residual risks. See [`demo.md`](demo.md) for the executed run and limitations.

## Demo result

Codex CLI `0.166.0-alpha.5.1` completed assessment, planning, phase preview, approved synthetic remediation, and focused verification. The focused test passed (5 tests). The CLI attempted outbound plugin-catalog requests at startup and received 401 responses, so the run is not evidence of network isolation. Full details and residual risks are in [`demo.md`](demo.md).

## FAQ

**Does this prove my app is secure?** No. It structures review and evidence; it does not certify a system.

**Does assessment modify app code?** No. It may write the requested strategy report under `docs/security/` only.

**Does planning authorize implementation?** No. Every phase requires explicit approval for its exact scope.

**Does it run commands automatically?** No command should be run before its effects are reviewed; network, destructive, and production-sensitive actions need separate explicit approval.

**Does it support slash commands everywhere?** No. Natural-language skill activation is the portable path; slash commands depend on each agent.

## Documentation and screenshots

- Project guide: https://github.com/Yousef-Abdallah-1711/security-coverage
- Cover and square logo: `../assets/branding/security-coverage-cover.webp`, `../assets/branding/security-coverage-logo.png`
- Demo: [`demo.md`](demo.md); not submitted to Agensi
