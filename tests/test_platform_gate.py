"""Minimal pytest module so wb-cpu-worker discovers tests (test_*.py).

Real suite modules use check_*.py (see pytest.ini) so pymcdc stays in static mode.
This file must not import sandbox-only paths or add MC/DC unittest coupling.
"""


def test_platform_pytest_discovery_gate() -> None:
    assert True
