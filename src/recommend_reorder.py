"""CLI for a next-day sales forecast and inventory reorder suggestion."""

import argparse
from pathlib import Path
import sys

# Support ``python src/recommend_reorder.py`` from the project root.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data import load_sales
from src.forecast import forecast_next_day
from src.reorder import reorder_quantity


DEFAULT_SAFETY_FACTOR = 0.2


def main() -> None:
    """Parse inventory inputs and print the selected reorder recommendation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", type=int, required=True)
    parser.add_argument("--item", type=int, required=True)
    parser.add_argument("--on-hand", type=int, required=True)
    parser.add_argument("--promo", action="store_true", help="mark a promotion for this item")
    parser.add_argument("--safety-factor", type=float, default=DEFAULT_SAFETY_FACTOR)
    args = parser.parse_args()

    flags = {(args.store, args.item): int(args.promo)}
    predictions = forecast_next_day(load_sales(), flags)
    selected = predictions[
        (predictions["store"] == args.store) & (predictions["item"] == args.item)
    ]
    if selected.empty:
        parser.error("Store or item is not present in the sales history")
    row = selected.iloc[0]
    quantity = reorder_quantity(
        [row["forecast_sales"]], args.on_hand, args.safety_factor
    )
    print(f"Forecast date: {row['date'].date()}")
    print(f"Forecast demand: {row['forecast_sales']:.1f} units")
    print(f"Suggested reorder: {quantity} units")


if __name__ == "__main__":
    main()
