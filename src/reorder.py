"""Turn a forecast into a reorder suggestion."""
import math


def reorder_quantity(forecast_next_days, on_hand, safety_factor=0.2):
    """Units to order = forecast demand + safety stock - stock on hand (never negative)."""
    demand = sum(forecast_next_days)
    safety = math.ceil(demand * safety_factor)
    return max(0, math.ceil(demand + safety - on_hand))
