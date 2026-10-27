"""Tests for evaluation metric calculations."""

import pandas as pd

from src.baselines import metric_row


def test_metric_row_reports_mae_rmse_and_mape():
    actual = pd.Series([10.0, 20.0])
    predicted = pd.Series([8.0, 22.0])
    row = metric_row("sample", actual, predicted)
    assert row["MAE"] == 2.0
    assert row["RMSE"] == 2.0
    assert abs(row["MAPE_%"] - 15.0) < 1e-9
