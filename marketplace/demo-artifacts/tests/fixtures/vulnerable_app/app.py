"""Synthetic intentionally vulnerable example. Do not deploy."""

DEBUG = True
SESSION_COOKIE_SECURE = False
NOTE_ROUTE = "/api/v1/notes"


def update_note(actor, tenant_id, note_id, request_body, database):
    if actor.tenant_id != tenant_id:
        raise PermissionError("actor tenant does not match note tenant")

    body = request_body.get("body")
    if not isinstance(body, str) or len(body) > 2048:
        raise ValueError("note body must be a string of at most 2048 characters")

    query = "UPDATE notes SET body = %s WHERE id = %s AND tenant_id = %s"
    database.execute(query, (body, note_id, tenant_id))
    return {"updated": note_id, "tenant": tenant_id}


def request_password_reset(email, mailer):
    # Intentionally missing rate limiting and account enumeration controls.
    mailer.send_reset(email)
    return {"sent": True, "email": email}


def mark_invoice_paid(invoice_id, amount, database):
    # Intentionally trusts the caller-provided amount and has no role check.
    database.execute("UPDATE invoices SET paid = 1, amount = %s WHERE id = %s", (amount, invoice_id))
    return True


def set_session_cookie(response, session_id):
    # Synthetic framework adapter: deliberately omits Secure/HttpOnly/SameSite flags.
    response.setcookie("session", session_id)
    return response
