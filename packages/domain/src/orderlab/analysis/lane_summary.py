"""Lane totals built on ``route_parcels``.

Gives the nested-decision fixture a downstream module, so a change to
``nested_paths_sample.py`` has something whose tests the change-impact measure can check.
"""
from collections import Counter

from .nested_paths_sample import route_parcels


def lane_counts(parcels, regions, express_only=False):
    """Count parcels per lane, e.g. ``{"careful": 2, "standard": 1}``."""
    return dict(Counter(lane for lane, _ in route_parcels(parcels, regions, express_only)))
