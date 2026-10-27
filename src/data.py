"""Load and clean daily store-item sales observations."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sales.csv"
REQUIRED_COLUMNS = {"date", "store", "item", "promo", "sales"}
SERIES_KEYS = ["store", "item"]


def clean_sales(data: pd.DataFrame) -> pd.DataFrame:
    """Validate records, aggregate duplicate keys, and fill missing days with zero sales.

    Duplicate date/store/item records are combined by summing sales and retaining
    the maximum promo flag. A missing date within an existing series is treated
    as a day with zero recorded sales and no promotion.
    """
    missing_columns = REQUIRED_COLUMNS - set(data.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    cleaned = data[list(REQUIRED_COLUMNS)].copy()
    cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")
    for column in ["store", "item", "promo", "sales"]:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
    if cleaned.isna().any().any():
        raise ValueError("Sales data contains missing or invalid required values")
    if (cleaned[["store", "item"]] < 1).any().any():
        raise ValueError("Store and item identifiers must be positive")
    if not cleaned["promo"].isin([0, 1]).all():
        raise ValueError("Promo values must be 0 or 1")
    if (cleaned["sales"] < 0).any():
        raise ValueError("Sales values must be non-negative")

    cleaned = cleaned.groupby(
        ["date", "store", "item"], as_index=False, sort=True
    ).agg(sales=("sales", "sum"), promo=("promo", "max"))

    complete_series = []
    for (store, item), group in cleaned.groupby(SERIES_KEYS, sort=True):
        group = group.set_index("date").sort_index()
        full_dates = pd.date_range(group.index.min(), group.index.max(), freq="D")
        group = group.reindex(full_dates)
        group.index.name = "date"
        group["store"] = store
        group["item"] = item
        group["sales"] = group["sales"].fillna(0)
        group["promo"] = group["promo"].fillna(0)
        complete_series.append(group.reset_index())

    return pd.concat(complete_series, ignore_index=True)[
        ["date", "store", "item", "promo", "sales"]
    ].sort_values(["store", "item", "date"]).reset_index(drop=True)


def load_sales(path: Path = DATA_PATH) -> pd.DataFrame:
    """Read a CSV and return validated, gap-filled daily observations."""
    return clean_sales(pd.read_csv(path))
