# /security-assess

Run the Security Coverage assessment workflow for the current repository.

First, read the canonical skill instructions from the first path that exists:

- `.claude/skills/security-coverage/SKILL.md`
- `.codex/skills/security-coverage/SKILL.md`
- `skills/security-coverage/SKILL.md`
- `~/.claude/skills/security-coverage/SKILL.md`
- `~/.codex/skills/security-coverage/SKILL.md`

Then read these references from the same skill directory:

- `references/layers.md`
- `references/threat-model.md`
- `references/stack-map.md`

Use this template from the same skill directory:

- `templates/SECURITY-STRATEGY.md`

## Task

Create or update:

```text
docs/security/SECURITY-STRATEGY.md
```

## Required Workflow

1. Inspect the current repository from its root. Do not assume context from earlier chat.
2. If available, run the detector:

   ```bash
   python3 <skill-dir>/scripts/detect_security_stack.py . --json
   ```

   If Python is not available, continue by inspecting files manually.
3. Identify the real attack surface: routes, APIs, forms, auth, sessions, roles, admin screens, databases, file uploads, payments, webhooks, browser entry points, deployment files, logs, and backups.
4. Classify every layer S0-S11 as `ADOPT`, `PARTIAL`, `DEFER`, or `SKIP` with a reason.
5. Write a complete `SECURITY-STRATEGY.md` using the template.

## Stop Condition

Stop when `docs/security/SECURITY-STRATEGY.md` exists and is detailed enough for `/security-plan` to create executable phases.

Do not modify application code, production settings, databases, payment state, or secrets during assessment.
