"""Build and evaluate simple time-series sales forecasting baselines."""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sales.csv"
OUTPUT_PATH = ROOT / "reports" / "baseline_metrics.csv"
TEST_START = pd.Timestamp("2023-07-01")


def add_baseline_predictions(data: pd.DataFrame) -> pd.DataFrame:
    """Add yesterday and same-weekday-last-week predictions per series."""
    result = data.copy()
    result["date"] = pd.to_datetime(result["date"])
    result = result.sort_values(["store", "item", "date"])
    grouped_sales = result.groupby(["store", "item"], sort=False)["sales"]
    result["naive_yesterday"] = grouped_sales.shift(1)
    result["seasonal_naive_7d"] = grouped_sales.shift(7)
    return result


def metric_row(name: str, actual: pd.Series, predicted: pd.Series) -> dict[str, float | str]:
    """Calculate MAE, RMSE, and nonzero-target MAPE for a forecast."""
    actual_values = actual.to_numpy(dtype=float)
    predicted_values = predicted.to_numpy(dtype=float)
    nonzero = actual_values != 0
    mape = (
        float(
            np.mean(
                np.abs(actual_values[nonzero] - predicted_values[nonzero])
                / np.abs(actual_values[nonzero])
            ) * 100
        )
        if nonzero.any()
        else float("nan")
    )
    return {
        "model": name,
        "MAE": float(mean_absolute_error(actual_values, predicted_values)),
        "RMSE": float(mean_squared_error(actual_values, predicted_values) ** 0.5),
        "MAPE_%": mape,
    }


def evaluate_baselines(data: pd.DataFrame, test_start: pd.Timestamp = TEST_START) -> pd.DataFrame:
    """Score both baselines only on dates at or after the temporal cutoff."""
    with_predictions = add_baseline_predictions(data)
    test = with_predictions[with_predictions["date"] >= test_start].copy()
    rows = []
    for column, label in [
        ("naive_yesterday", "Naive: yesterday"),
        ("seasonal_naive_7d", "Seasonal naive: last week"),
    ]:
        scored = test.dropna(subset=[column])
        rows.append(metric_row(label, scored["sales"], scored[column]))
    return pd.DataFrame(rows)


def main() -> None:
    """Evaluate baselines on the held-out synthetic sales period."""
    data = pd.read_csv(DATA_PATH, parse_dates=["date"])
    metrics = evaluate_baselines(data)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(OUTPUT_PATH, index=False)
    print(f"Test dates: {TEST_START.date()} through {data['date'].max().date()}")
    print(metrics.round(2).to_string(index=False))
    print(f"Saved baseline metrics to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
