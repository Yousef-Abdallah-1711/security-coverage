# API Validation

Use for S4 phases.

## Review Targets

- Allowed methods and content types.
- Required fields and types.
- Maximum body size and file size.
- Server-side normalization.
- Output encoding.
- Error response shape.
- External HTTP calls and SSRF risk.
- Shell commands and file paths.

## Rules

- Validate on the server even when the frontend validates.
- Reject unknown or dangerous fields when they can change behavior.
- Keep validation errors helpful but not revealing.
- Do not trust payment amount, role, ownership, or status from the client.

## Evidence

Record accepted and rejected examples for each sensitive endpoint.
