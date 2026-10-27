"""Build features for the next day and generate store-item forecasts."""

from collections.abc import Mapping

import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

from src.data import clean_sales
from src.features import FEATURES, add_features


def build_next_day_features(
    data: pd.DataFrame,
    promo_flags: Mapping[tuple[int, int], int] | None = None,
) -> pd.DataFrame:
    """Create next-day calendar, lag, and rolling features for each series.

    Promotion defaults to zero unless an explicit (store, item) flag is given.
    """
    clean = clean_sales(data)
    promo_flags = promo_flags or {}
    rows = []
    for (store, item), group in clean.groupby(["store", "item"], sort=True):
        group = group.sort_values("date")
        if len(group) < 28:
            raise ValueError(f"Store {store}, item {item} needs at least 28 days of history")
        next_date = group["date"].iloc[-1] + pd.Timedelta(days=1)
        promo = int(promo_flags.get((int(store), int(item)), 0))
        if promo not in (0, 1):
            raise ValueError("Promo flags must be 0 or 1")
        sales = group["sales"]
        rows.append({
            "date": next_date,
            "store": store,
            "item": item,
            "promo": promo,
            "dow": next_date.dayofweek,
            "month": next_date.month,
            "dayofyear": next_date.dayofyear,
            "lag_1": sales.iloc[-1],
            "lag_7": sales.iloc[-7],
            "lag_28": sales.iloc[-28],
            "roll_mean_7": sales.tail(7).mean(),
            "roll_mean_28": sales.tail(28).mean(),
        })
    return pd.DataFrame(rows)


def fit_full_history_model(data: pd.DataFrame) -> HistGradientBoostingRegressor:
    """Fit the forecast model on every cleaned historical feature row."""
    clean = clean_sales(data)
    train = add_features(clean)
    if train.empty:
        raise ValueError("At least 29 daily observations are needed to train the model")
    model = HistGradientBoostingRegressor(
        max_iter=300, learning_rate=0.05, random_state=0
    )
    model.fit(train[FEATURES], train["sales"])
    return model


def forecast_next_day(
    data: pd.DataFrame,
    promo_flags: Mapping[tuple[int, int], int] | None = None,
    model: HistGradientBoostingRegressor | None = None,
) -> pd.DataFrame:
    """Forecast the next day per store-item using all available history."""
    clean = clean_sales(data)
    model = model or fit_full_history_model(clean)
    next_features = build_next_day_features(clean, promo_flags)
    next_features["forecast_sales"] = model.predict(next_features[FEATURES]).clip(min=0)
    return next_features
