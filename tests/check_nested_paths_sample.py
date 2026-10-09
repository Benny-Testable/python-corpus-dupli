"""route_parcels: takes the fragile and plain-heavy branches, not the express or freight ones."""
from orderlab.analysis.nested_paths_sample import route_parcels


def test_fragile_parcel_takes_the_careful_lane():
    parcels = [{"id": 1, "weight": 3, "region": "east", "fragile": True}]
    assert route_parcels(parcels, ["east"]) == [("careful", 1)]


def test_heavy_parcel_without_oversize_takes_the_heavy_lane():
    parcels = [{"id": 2, "weight": 30, "region": "east"}]
    assert route_parcels(parcels, ["east"]) == [("heavy", 2)]


def test_light_parcel_takes_the_standard_lane():
    parcels = [{"id": 3, "weight": 5, "region": "east"}]
    assert route_parcels(parcels, ["east"]) == [("standard", 3)]


def test_parcels_with_no_weight_are_skipped():
    assert route_parcels([{"id": 4, "region": "east"}], ["east"]) == []


def test_lane_counts_totals_each_lane():
    from orderlab.analysis.lane_summary import lane_counts

    parcels = [
        {"id": 1, "weight": 3, "region": "east", "fragile": True},
        {"id": 2, "weight": 5, "region": "east"},
        {"id": 3, "weight": 6, "region": "east"},
    ]
    assert lane_counts(parcels, ["east"]) == {"careful": 1, "standard": 2}
