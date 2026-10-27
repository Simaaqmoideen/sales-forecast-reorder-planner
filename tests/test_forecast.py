"""Tests for next-day feature construction and forecast output."""

import pandas as pd

from src.forecast import build_next_day_features, forecast_next_day


def _sales_data() -> pd.DataFrame:
    dates = pd.date_range("2023-01-01", periods=35)
    return pd.DataFrame({
        "date": dates,
        "store": 1,
        "item": 1,
        "promo": 0,
        "sales": range(10, 45),
    })


def test_next_day_features_only_use_observed_history():
    features = build_next_day_features(_sales_data(), {(1, 1): 1}).iloc[0]
    assert features["date"] == pd.Timestamp("2023-02-05")
    assert features["lag_1"] == 44
    assert features["lag_7"] == 38
    assert features["lag_28"] == 17
    assert features["roll_mean_7"] == 41
    assert features["promo"] == 1


def test_next_day_forecast_is_nonnegative():
    result = forecast_next_day(_sales_data())
    assert len(result) == 1
    assert result.iloc[0]["forecast_sales"] >= 0
