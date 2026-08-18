# CLAUDE.md

This repository is the `security-coverage` plugin/skill repo.

## Important Git Context

Primary target repo:

```text
https://github.com/Yousef-Abdallah-1711/security-coverage
```

Org mirror target, if access is later fixed:

```text
https://github.com/rakymat-plugins/security-coverage
```

This server previously had Git credentials for a different GitHub account, which caused:

```text
Permission to Yousef-Abdallah-1711/security-coverage.git denied to yousefabdallah171
```

If that happens again, do not hardcode tokens in files. Store a new token with:

```bash
read -p "GitHub username: " GH_USER
read -s -p "GitHub token: " GH_TOKEN
echo
printf "protocol=https\nhost=github.com\nusername=%s\npassword=%s\n\n" "$GH_USER" "$GH_TOKEN" | git credential approve
unset GH_TOKEN
```

Then verify:

```bash
GIT_TERMINAL_PROMPT=0 git ls-remote https://github.com/Yousef-Abdallah-1711/security-coverage.git refs/heads/main
```

## Branches

- `main`: local working branch tracking the personal HTTPS remote.
- `push-yousef-official`: branch based on `Yousef-Abdallah-1711/main` with server updates prepared.

When pushing to the personal repo:

```bash
git push yousef-official push-yousef-official:main
```

## Validation Before Push

Run:

```bash
bash -n install.sh
python3 -m json.tool package.json >/dev/null
python3 -m py_compile skills/security-coverage/scripts/detect_security_stack.py
python3 /root/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/security-coverage
```

Do not commit `.claude/`, `.codex/`, credentials, tokens, caches, or generated local install test folders.
