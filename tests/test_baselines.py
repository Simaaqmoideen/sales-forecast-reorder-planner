"""Tests for one-step sales baseline construction and time holdout scoring."""

import pandas as pd

from src.baselines import add_baseline_predictions, evaluate_baselines


def _sales_data() -> pd.DataFrame:
    dates = pd.date_range("2023-01-01", periods=12)
    return pd.DataFrame({"date": dates, "store": 1, "item": 1, "sales": range(10, 22)})


def test_baselines_use_only_previous_observations() -> None:
    result = add_baseline_predictions(_sales_data())
    assert pd.isna(result.iloc[0]["naive_yesterday"])
    assert result.iloc[1]["naive_yesterday"] == 10
    assert result.iloc[7]["seasonal_naive_7d"] == 10


def test_baseline_metrics_use_temporal_test_period() -> None:
    result = evaluate_baselines(_sales_data(), pd.Timestamp("2023-01-09"))
    assert list(result["model"]) == ["Naive: yesterday", "Seasonal naive: last week"]
    assert len(result) == 2
    assert result["MAE"].ge(0).all()
