# /security-plan

Turn the security strategy into a phase-gated implementation plan for the current repository.

First, read the canonical skill instructions from the first path that exists:

- `.claude/skills/security-coverage/SKILL.md`
- `.codex/skills/security-coverage/SKILL.md`
- `skills/security-coverage/SKILL.md`
- `~/.claude/skills/security-coverage/SKILL.md`
- `~/.codex/skills/security-coverage/SKILL.md`

Then read these references from the same skill directory:

- `references/layers.md`
- `references/gates.md`
- any domain reference needed by layers marked `ADOPT` or `PARTIAL`

Use these templates from the same skill directory:

- `templates/SECURITY-PLAN.md`
- `templates/SECURITY-TASKS.md`
- `templates/SECURITY-EVIDENCE-LOG.md`

## Task

Read:

```text
docs/security/SECURITY-STRATEGY.md
```

Create or update:

```text
docs/security/SECURITY-PLAN.md
docs/security/SECURITY-TASKS.md
docs/security/SECURITY-EVIDENCE-LOG.md
```

## Required Workflow

1. Refuse to invent a plan if `SECURITY-STRATEGY.md` is missing or too thin. Tell the user to run `/security-assess` first.
2. Convert adopted and partial layers into ordered implementation phases.
3. Put the highest-risk business flows as early as dependencies allow.
4. Give every phase: scope, exact tasks, suggested commands, expected evidence, rollback note, and green gate.
5. Create `SECURITY-EVIDENCE-LOG.md` as an empty log with headings ready for `/security-implement`.

## Stop Condition

Stop when the plan and tasks are complete enough that `/security-implement` can execute one safe phase without guessing.

Do not implement security changes during planning.
