"""Tier and volume discount rules.

The nesting here is deliberate: it gives cyclomatic and cognitive complexity
tools something with real branch structure to score, without being artificial
enough to look like a fixture.
"""
from typing import Optional

TIER_DISCOUNT = dict([("standard", 0.00), ("silver", 0.05), ("gold", 0.10)])

VOLUME_STEPS = ((500, 0.08), (100, 0.05), (25, 0.02))

PROMO_CODES = dict([("SPRING10", 0.10), ("VOLUME5", 0.05), ("LOYAL15", 0.15), ("WELCOME5", 0.05)])


class PricingRules(object):
    """Computes the combined discount rate for an order.

    The tier, volume and promo components are additive and the sum is capped
    at ``max_combined``.
    """

    MAX_COMBINED = 0.20

    def __init__(self, max_combined: float = None) -> None:
        self.max_combined = self.MAX_COMBINED if max_combined is None else max_combined

    def tier_discount(self, tier: str) -> float:
        return TIER_DISCOUNT.get(tier, 0.0)

    def volume_bonus(self, units: int) -> float:
        for threshold, bonus in VOLUME_STEPS:
            if units >= threshold:
                return bonus
        return 0.0

    def volume_tier(self, units: int) -> str:
        """Name of the volume band an order falls in."""
        if units >= 500:
            return "gold"
        if units >= 100:
            return "silver"
        if units >= 25:
            return "bronze"
        return "none"

    def promo_discount(self, promo_code: Optional[str]) -> float:
        if not promo_code:
            return 0.0
        return PROMO_CODES.get(promo_code.strip().upper(), 0.0)

    def _raw_rate(self, tier: str, units: int, promo_code: Optional[str] = None) -> float:
        raw = self.tier_discount(tier) + self.volume_bonus(units)
        return raw + self.promo_discount(promo_code)

    def combined(self, tier: str, units: int, promo_code: Optional[str] = None) -> float:
        combined = self._raw_rate(tier, units, promo_code)
        return round(combined if combined <= self.max_combined else self.max_combined, 4)

    def is_capped(self, tier: str, units: int, promo_code: Optional[str] = None) -> bool:
        """True when the uncapped discount would exceed the combined cap."""
        raw = self._raw_rate(tier, units, promo_code)
        return raw > self.max_combined

    def cap_headroom(self, tier: str, units: int, promo_code: Optional[str] = None) -> float:
        """How much further the combined rate could grow before it reaches the cap."""
        raw = self._raw_rate(tier, units, promo_code)
        return round(max(self.max_combined - raw, 0.0), 4)

    def describe(self, tier: str, units: int, promo_code: Optional[str] = None) -> str:
        parts = ["tier={0:.2%}".format(self.tier_discount(tier)),
                 "volume={0:.2%}".format(self.volume_bonus(units))]
        promo = self.promo_discount(promo_code)
        if promo:
            parts.append("promo={0:.2%}".format(promo))
        return " + ".join(parts)
