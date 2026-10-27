"""Turn a demand forecast into an inventory reorder suggestion."""

from collections.abc import Iterable
import math


def reorder_quantity(
    forecast_next_days: Iterable[float], on_hand: float, safety_factor: float = 0.2
) -> int:
    """Return demand plus safety stock less on-hand units, floored at zero."""
    if on_hand < 0:
        raise ValueError("On-hand inventory must be non-negative")
    if safety_factor < 0:
        raise ValueError("Safety factor must be non-negative")
    demand = sum(forecast_next_days)
    safety = math.ceil(demand * safety_factor)
    return max(0, math.ceil(demand + safety - on_hand))
