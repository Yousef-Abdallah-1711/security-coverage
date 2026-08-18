# Browser Security

Use for S7 phases.

## Review Targets

- XSS: raw HTML insertion, template escaping, markdown rendering, rich text, query params.
- CSRF: state-changing forms, cookies, admin actions.
- CSP and security headers.
- Cookie flags.
- Links with `target="_blank"` and `rel`.
- Third-party scripts and analytics.
- Iframe/clickjacking policy.

## Checks

- Confirm output encoding at the render point.
- Prefer framework escaping over ad hoc sanitizing.
- Add CSRF tokens to cookie-authenticated state changes.
- Add CSP incrementally; do not break payment/auth providers.

## Evidence

Record headers, risky sinks reviewed, sample rejected payloads, and browser console/network checks.
