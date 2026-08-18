# Infrastructure, Deploy, And File Permissions

Use for S8 phases.

## Review Targets

- Web root and public directories.
- `.git`, backups, local credentials, logs, and archives.
- Upload directories and executable permissions.
- TLS and proxy headers.
- Server config: Apache, Nginx, Vercel, Netlify, Cloudflare.
- CI/CD secrets and deployment permissions.
- Docker images and exposed ports.

## Rules

- Private config should not live under public web roots.
- Backups should not be downloadable.
- Uploaded files should not execute as code.
- CI secrets should be least-privilege and environment-scoped.

## Evidence

Record public path checks, file permission changes, server config reviewed, and rollback path.
