# Authentication And Sessions

Use for S2 phases.

## Review Targets

- Login, logout, registration, password reset, OAuth callbacks, magic links.
- Admin login and session gate.
- Cookie flags: `HttpOnly`, `Secure`, `SameSite`.
- Session rotation on privilege changes.
- Expiry and idle timeout.
- Rate limits on credential attempts.
- Error messages that reveal account existence.

## Evidence

Record the auth surfaces found, current controls, commands/tests run, and any manual flows checked.

## Common Fixes

- Add explicit session checks to every admin route.
- Regenerate sessions after login.
- Set cookie flags through framework config.
- Add CSRF protection to state-changing forms.
- Make logout destroy server state and redirect safely.
