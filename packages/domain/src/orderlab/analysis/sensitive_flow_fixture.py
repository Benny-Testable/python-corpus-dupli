"""Sensitive-data flow fixture.

Planted for Opengrep taint mode and Semgrep. Four functions read a secret from
the process environment. Three send it to an output sink (a log line, stdout,
a file handle) and are planted CWE-200 leaks. The fourth passes it through
`redact` first and must NOT be reported.

  leaks    : log_api_token, print_db_password, write_signing_secret
  control  : log_redacted_token
"""
import logging
import os

log = logging.getLogger(__name__)


def redact(value):
    """Return a non-reversible marker in place of the secret."""
    return "***" if value else ""


def log_api_token():
    """PLANTED CWE-200: the token reaches a log line."""
    token = os.environ.get("ORDERLAB_API_TOKEN", "")
    log.info("using token %s", token)
    return bool(token)


def print_db_password():
    """PLANTED CWE-200: the password reaches stdout."""
    password = os.environ["ORDERLAB_DB_PASSWORD"]
    print("connecting with " + password)


def write_signing_secret(handle):
    """PLANTED CWE-200: the secret reaches a file handle."""
    secret = os.getenv("ORDERLAB_SIGNING_SECRET", "")
    handle.write(secret)


def log_redacted_token():
    """Negative control: the same shape, redacted before the log call."""
    token = os.environ.get("ORDERLAB_API_TOKEN", "")
    log.info("using token %s", redact(token))
