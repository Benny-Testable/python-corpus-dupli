"""Access-control fixture.

Planted for Opengrep / Semgrep (missing-authorization rule, CWE-862). Four
functions each perform a sensitive operation (a database write, a file write
or a file delete). Two call `authorize` first. Two do not. A tool that reports
all four, or none, is not reading the call order.

  protected   : delete_order, export_orders
  unprotected : purge_archive, refund_order   <- planted CWE-862

`authorize` raises PermissionDenied when the user lacks the permission, so the
protected functions never reach their operation for an unauthorised user.
"""
import os


class PermissionDenied(Exception):
    """The user does not hold the permission the operation needs."""


def authorize(user, permission):
    """Raise PermissionDenied unless the user holds the permission."""
    if permission not in user.get("permissions", ()):
        raise PermissionDenied(permission)


def delete_order(cursor, user, order_id):
    """Protected: the authorization call precedes the sensitive operation."""
    authorize(user, "orders:delete")
    cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))


def export_orders(user, path, rows):
    """Protected: the authorization call precedes the file write."""
    authorize(user, "orders:export")
    with open(path, "w") as handle:
        for row in rows:
            handle.write(str(row) + "\n")


def purge_archive(path):
    """PLANTED CWE-862: deletes a file with no authorization check."""
    os.remove(path)


def refund_order(cursor, order_id, amount):
    """PLANTED CWE-862: writes a refund with no authorization check."""
    cursor.execute(
        "UPDATE orders SET refunded = ? WHERE order_id = ?", (amount, order_id))
