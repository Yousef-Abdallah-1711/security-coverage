# AGENTS.md

Guidance for AI coding agents working on this repo.

## What This Repo Contains

`security-coverage` is a plugin/skill repo that provides:

- `/security-assess`
- `/security-plan`
- `/security-implement`
- `skills/security-coverage/SKILL.md`
- references, templates, installer scripts, and a stdlib-only detector script

There is intentionally no slides command.

## Credential Safety

Never write GitHub tokens, PATs, deploy keys, passwords, API keys, or service keys into:

- source files
- README files
- `CLAUDE.md`
- `AGENTS.md`
- evidence logs
- command output summaries

If GitHub auth breaks, store credentials through Git credential helper only:

```bash
printf "protocol=https\nhost=github.com\nusername=USERNAME\npassword=TOKEN\n\n" | git credential approve
```

Prefer interactive `read -s` for token entry when a human is at the terminal.

## Common Push Issue

If push fails with:

```text
Permission denied to yousefabdallah171
```

the server is authenticated as the wrong account. Replace the GitHub credential with a token for `Yousef-Abdallah-1711` that has `Contents: Read and write` on `Yousef-Abdallah-1711/security-coverage`.

## Remotes

Expected useful remotes:

```text
yousef-official  https://github.com/Yousef-Abdallah-1711/security-coverage.git
personal-https   https://github.com/yousefabdallah171/security-coverage.git
origin           https://github.com/rakymat-plugins/security-coverage.git
```

Push the prepared official update with:

```bash
git push yousef-official push-yousef-official:main
```

## Checks

Before final response, run the validation checks listed in `CLAUDE.md`.
