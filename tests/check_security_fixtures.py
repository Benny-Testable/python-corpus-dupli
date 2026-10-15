"""The access-control and entry-point fixtures behave as their docstrings say."""
import pytest

from orderlab.analysis.access_control_fixture import (
    PermissionDenied, authorize, delete_order, export_orders, purge_archive,
    refund_order)
from orderlab.analysis.entry_points_fixture import app
from orderlab.analysis.sensitive_flow_fixture import redact


class FakeCursor(object):
    def __init__(self):
        self.calls = []

    def execute(self, sql, params=()):
        self.calls.append((sql, params))


def test_authorize_raises_without_the_permission():
    with pytest.raises(PermissionDenied):
        authorize({"permissions": ["orders:read"]}, "orders:delete")


def test_protected_delete_does_nothing_when_denied():
    cursor = FakeCursor()
    with pytest.raises(PermissionDenied):
        delete_order(cursor, {"permissions": []}, 7)
    assert cursor.calls == []


def test_protected_delete_runs_when_allowed():
    cursor = FakeCursor()
    delete_order(cursor, {"permissions": ["orders:delete"]}, 7)
    assert len(cursor.calls) == 1


def test_protected_export_writes_when_allowed(tmp_path):
    target = tmp_path / "orders.txt"
    export_orders({"permissions": ["orders:export"]}, str(target), [1, 2])
    assert target.read_text() == "1\n2\n"


def test_unprotected_functions_have_no_check(tmp_path):
    target = tmp_path / "old.tgz"
    target.write_text("x")
    purge_archive(str(target))
    assert not target.exists()
    cursor = FakeCursor()
    refund_order(cursor, 7, 5.0)
    assert len(cursor.calls) == 1


def test_three_routes_are_registered():
    assert sorted(app.routes) == ["/orders/export", "/orders/lookup", "/orders/safe"]


def test_redact_hides_the_value():
    assert redact("hunter2") == "***"
    assert redact("") == ""
