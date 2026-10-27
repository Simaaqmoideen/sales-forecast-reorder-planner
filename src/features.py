import pandas as pd

from src.data import clean_sales


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calendar + lag + rolling features. Every lag/rolling value uses only PAST days."""
    df = clean_sales(df)
    df["dow"] = df["date"].dt.day_of_week
    df["month"] = df["date"].dt.month
    df["dayofyear"] = df["date"].dt.day_of_year
    g = df.groupby(["store", "item"])["sales"]
    df["lag_1"] = g.shift(1)
    df["lag_7"] = g.shift(7)
    df["lag_28"] = g.shift(28)
    # shift(1) first so the current day is never inside its own rolling window
    df["roll_mean_7"] = g.transform(lambda s: s.shift(1).rolling(7).mean())
    df["roll_mean_28"] = g.transform(lambda s: s.shift(1).rolling(28).mean())
    return df.dropna().reset_index(drop=True)


FEATURES = ["store", "item", "promo", "dow", "month", "dayofyear", "lag_1", "lag_7", "lag_28", "roll_mean_7", "roll_mean_28"]
