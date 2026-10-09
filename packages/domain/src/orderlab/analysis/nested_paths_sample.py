"""Nested-decision fixture.

Planted for the coverage tools' nested-condition-path measure: a decision counts
as deeply nested when it sits more than three control structures down, and no other
file here goes that deep. ``route_parcels`` has decisions at depth four and five.
The test in ``tests/check_nested_paths_sample.py`` takes some of those branches and
leaves others, so a working tool reports a share between 0 and 100.
"""


def route_parcels(parcels, regions, express_only=False):
    """Pick a lane per parcel. Deliberately nested rather than flattened.

    Returns a list of ``(lane, parcel id)`` pairs, in parcel order.
    """
    lanes = []
    for parcel in parcels:                                  # depth 1
        if parcel.get("weight", 0) > 0:                     # depth 2
            for region in regions:                          # depth 2
                if parcel.get("region") == region:          # depth 3
                    if parcel.get("fragile"):               # depth 4
                        if express_only:                    # depth 5
                            lanes.append(("express-fragile", parcel["id"]))
                        else:
                            lanes.append(("careful", parcel["id"]))
                    elif parcel.get("weight", 0) > 20:      # depth 4
                        if parcel.get("oversize"):          # depth 5
                            lanes.append(("freight", parcel["id"]))
                        else:
                            lanes.append(("heavy", parcel["id"]))
                    else:
                        lanes.append(("standard", parcel["id"]))
    return lanes
