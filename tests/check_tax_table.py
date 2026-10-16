"""TaxTable behaviour."""
import pytest

from orderlab.models.tax_table import TaxTable, UnknownChannel


def test_known_channels_are_sorted():
    channels = TaxTable().known_channels()
    assert list(channels) == sorted(channels)
    assert "retail" in channels


def test_region_multiplier_scales_the_channel_rate():
    table = TaxTable()
    assert table.rate_for("retail", "US") == 0.0825
    assert table.rate_for("retail", "EU") == round(0.0825 * 1.20, 6)


def test_apply_returns_tax_and_total():
    tax, total = TaxTable().apply(100.0, "retail", "US")
    assert tax == 8.25
    assert total == 108.25


def test_unknown_channel_is_rejected():
    with pytest.raises(UnknownChannel):
        TaxTable().rate_for("barter", "US")


def test_effective_percent_is_the_rate_times_one_hundred():
    assert TaxTable().effective_percent("wholesale", "US") == 6.0


def test_auction_channel_has_a_rate():
    assert TaxTable().rate_for("auction", "US") == 0.05


def test_negative_amounts_are_rejected():
    with pytest.raises(ValueError):
        TaxTable().apply(-1.0, "retail", "US")
