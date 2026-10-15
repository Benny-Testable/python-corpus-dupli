"""Entry-point fixture.

Planted for Opengrep taint mode and Semgrep. A minimal router (no framework)
registers three GET handlers. Each reads a query parameter from the request.

  /orders/lookup : parameter -> SQL string          PLANTED CWE-89, unsanitised
  /orders/safe   : int() cast, then parameterised   negative control
  /orders/export : authorize() first, then writes   access-controlled entry point

Importing this module registers the three routes in a dict and does nothing
else: no I/O, no network, no database.
"""
from .access_control_fixture import authorize


class Router(object):
    """A dict of path -> handler, filled by decorators."""

    def __init__(self):
        self.routes = {}

    def get(self, path):
        def register(func):
            self.routes[path] = func
            return func
        return register


app = Router()


@app.get("/orders/lookup")
def lookup_handler(request, cursor):
    """PLANTED CWE-89: the query parameter reaches an SQL string."""
    order_id = request.args["order_id"]
    cursor.execute("SELECT * FROM orders WHERE order_id = '" + order_id + "'")
    return cursor.fetchall()


@app.get("/orders/safe")
def safe_lookup_handler(request, cursor):
    """Negative control: cast to int, then parameterised. Must NOT be reported."""
    order_id = int(request.args["order_id"])
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    return cursor.fetchall()


@app.get("/orders/export")
def export_handler(request, user, path):
    """Access-controlled: authorizes before the file write."""
    authorize(user, "orders:export")
    with open(path, "w") as handle:
        handle.write(request.args.get("format", "csv"))
