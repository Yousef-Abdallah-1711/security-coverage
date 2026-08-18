# security-coverage

Three commands that turn "we should check security" into a designed, layered, evidence-backed security audit and hardening workflow for any application repo.

```text
/security-assess      -> docs/security/SECURITY-STRATEGY.md
/security-plan        -> docs/security/SECURITY-PLAN.md + SECURITY-TASKS.md
/security-implement   -> security changes/checks + SECURITY-EVIDENCE-LOG.md
```

There is intentionally no slides command.

## Installation

### One command with Skills CLI

Install from the working GitHub repo:

```bash
npx skills add Yousef-Abdallah-1711/security-coverage --all
```

This installs three Claude Code skills, which are invoked exactly like slash commands:

```text
/security-assess
/security-plan
/security-implement
```

The Skills CLI installs these under `.claude/skills/` or `~/.claude/skills/` depending on scope. Claude Code exposes each skill by its folder name.

The repo also includes `.claude/commands/` files and `install.ps1`/`install.sh` for users who prefer classic Claude command files.

To make `/security-assess`, `/security-plan`, and `/security-implement` appear in Claude Code after using `npx skills add`, run this once in PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\commands" | Out-Null
Copy-Item "$HOME\.claude\skills\security-coverage\commands\*.md" "$HOME\.claude\commands\" -Force
```

Then restart Claude Code.

Windows PowerShell note: if `npx` fails with a script execution policy error, use:

```powershell
npx.cmd skills add Yousef-Abdallah-1711/security-coverage --all
```

Temporary PowerShell-session workaround:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
npx skills add Yousef-Abdallah-1711/security-coverage --all
```

This does not change the machine-wide policy.

If the repo has been mirrored into `rakymat-plugins`, this works too:

```bash
npx skills add rakymat-plugins/security-coverage --all
```

If an older clone has only `skills/security-coverage/SKILL.md`, add `--full-depth`:

```bash
npx skills add rakymat-plugins/security-coverage --all --full-depth
```

### Current working clone

The currently pushed copy is here:

```bash
git clone https://github.com/Yousef-Abdallah-1711/security-coverage.git
cd security-coverage
bash install.sh
```

By default this installs for both Claude and Codex.

### Org clone after mirror/push

Once `rakymat-plugins/security-coverage` has the code:

```bash
git clone https://github.com/rakymat-plugins/security-coverage.git
cd security-coverage
bash install.sh
```

### Windows manual install

```powershell
git clone https://github.com/Yousef-Abdallah-1711/security-coverage.git
cd security-coverage
.\install.ps1
```

This installs both the skill and the Claude slash commands.

After the org repo is populated, replace the clone URL with:

```text
https://github.com/rakymat-plugins/security-coverage.git
```

## Options

| Command | What it does |
|---|---|
| `./install.sh` | install globally for Claude and Codex |
| `./install.sh --claude` | install Claude commands and skill only |
| `./install.sh --codex` | install Codex commands, skill, and plugin files only |
| `./install.sh --local` | install into the current project instead of the home directory |
| `./install.sh --uninstall` | remove installed files; combine with `--local`, `--claude`, or `--codex` |
| `./install.sh --help` | show usage |

Re-run `./install.sh` any time to update. The installer replaces the previous install so deleted upstream files do not linger.

## Git Bash On Windows

Run from Git Bash:

```bash
bash install.sh
```

From PowerShell or CMD, call Git Bash directly:

```powershell
& "C:\Program Files\Git\bin\bash.exe" ./install.sh
```

## What it installs

Claude Code slash commands:

```text
~/.claude/commands/security-assess.md
~/.claude/commands/security-plan.md
~/.claude/commands/security-implement.md
```

Global Claude install:

```text
~/.claude/skills/security-coverage/
~/.claude/skills/security-assess/
~/.claude/skills/security-plan/
~/.claude/skills/security-implement/
~/.claude/commands/security-assess.md
~/.claude/commands/security-plan.md
~/.claude/commands/security-implement.md
```

Global Codex install:

```text
~/.codex/skills/security-coverage/
~/.codex/skills/security-assess/
~/.codex/skills/security-plan/
~/.codex/skills/security-implement/
~/.codex/commands/security-assess.md
~/.codex/commands/security-plan.md
~/.codex/commands/security-implement.md
~/.codex/plugins/security-coverage/
```

Local install uses `./.claude/...` and `./.codex/...` in the current project.

## Requirements

- `bash`
- Python 3.8+ is optional but recommended for `detect_security_stack.py`
- No package install and no API keys

## Usage

```bash
cd your-project

/security-assess
/security-plan
/security-implement

/security-implement --phase-only
/security-implement --dry-run
```

Plain language works too: "assess security coverage for this repo", "plan security hardening", or "implement the next security phase".

## Security layers

| Layer | Proves |
|---|---|
| S0 Inventory & attack surface | the app's exposed surfaces, assets, trust boundaries, and risky flows are known |
| S1 Secrets/config/environment | secrets are not committed or exposed; config defaults fail closed |
| S2 Authentication/sessions | identity, login, logout, session lifetime, and credential flows are protected |
| S3 Authorization/roles | every protected action enforces the right role, tenant, and ownership rules |
| S4 Input validation/API protection | untrusted inputs are validated, normalized, and rejected safely |
| S5 Database/Supabase/RLS/data access | data access is scoped and policies match the app's authorization model |
| S6 Payments/webhooks/admin money flows | payment state changes are authentic, idempotent, audited, and admin-only |
| S7 Browser security | XSS, CSRF, unsafe links, CSP, and cookie settings are handled |
| S8 Infrastructure/deploy/file permissions | deploy configuration, file permissions, and public paths are sane |
| S9 Abuse protection | rate limits, spam controls, and brute-force defenses exist where needed |
| S10 Logging/monitoring/backups/rollback | incidents can be detected, investigated, recovered, and rolled back |
| S11 Final release gate | the chosen layers have evidence and documented residual risk |

Almost no project needs every layer at full depth. Choosing `DEFER` or `SKIP` with a reason is part of the workflow.

## How it works

Each command reads what the previous command wrote. Nothing important is held only in chat.

| Command | Reads | Writes | Stops when |
|---|---|---|---|
| `/security-assess` | repo | `SECURITY-STRATEGY.md` | layer verdicts and threat model are decided |
| `/security-plan` | strategy | plan, tasks, evidence log | task list is executable phase-by-phase |
| `/security-implement` | plan and tasks | checks/fixes/evidence | one phase gate passes or a blocker appears |

## Stack detector

Standalone:

```bash
python3 skills/security-coverage/scripts/detect_security_stack.py /path/to/repo
python3 skills/security-coverage/scripts/detect_security_stack.py /path/to/repo --json
```

It uses Python standard library only and reports languages, package managers, frameworks, auth/session hints, API/admin surfaces, database/Supabase signals, payment signals, deployment files, and risk flags.

## Repo contents

```text
install.sh
.claude/commands/
security-assess/
security-plan/
security-implement/
commands/
  security-assess.md
  security-plan.md
  security-implement.md
skills/security-coverage/
  SKILL.md
  references/
  templates/
  scripts/detect_security_stack.py
.codex-plugin/plugin.json
```

## Push to GitHub

```bash
git init
git add .
git commit -m "feat: security-coverage plugin"
git branch -M main
git remote add origin https://github.com/rakymat-plugins/security-coverage.git
git push -u origin main
```
