---
name: security-coverage
description: Assess, plan, and implement layered security coverage for an application repo, producing strategy, plan, tasks, and evidence artifacts. Use when the user asks for security audit, hardening, appsec coverage, production security readiness, or the /security-* commands.
metadata:
  short-description: Layered security audit and hardening workflow
---

# Security Coverage

This root `SKILL.md` exists so tools such as `npx skills add owner/security-coverage --all` can discover the skill directly from the repository root.

The canonical skill implementation lives at:

```text
skills/security-coverage/SKILL.md
```

When using this skill, read that canonical file first and follow its command routing, safety rules, references, templates, and evidence standards.

Important resources:

- `commands/security-assess.md`
- `commands/security-plan.md`
- `commands/security-implement.md`
- `skills/security-coverage/references/`
- `skills/security-coverage/templates/`
- `skills/security-coverage/scripts/detect_security_stack.py`

Do not create or use a `/security-slides` command. This repository provides only `/security-assess`, `/security-plan`, and `/security-implement`.
