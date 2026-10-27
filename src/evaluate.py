"""Evaluate sales forecasts on a held-out time period and save reports."""

from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

# Support both ``python src/evaluate.py`` and ``python -m src.evaluate``.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.baselines import TEST_START, add_baseline_predictions, metric_row
from src.data import load_sales
from src.features import FEATURES, add_features
from src.train import train_model


ROOT = Path(__file__).resolve().parents[1]
METRICS_PATH = ROOT / "reports" / "metrics.csv"
WEEKDAY_PATH = ROOT / "reports" / "weekday_error.csv"
FORECAST_PATH = ROOT / "reports" / "forecast.png"
MODEL_COMPARISON_PATH = ROOT / "reports" / "model_comparison.png"


def evaluate_model(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Return model/baseline scores, weekday errors, and row-level forecasts."""
    model, _ = train_model(data)
    featured = add_features(data)
    test = featured[featured["date"] >= TEST_START].copy()
    if test.empty:
        raise ValueError("No feature rows exist in the configured test period")
    test["model_prediction"] = model.predict(test[FEATURES]).clip(min=0)

    baseline_rows = add_baseline_predictions(data)
    baseline_test = baseline_rows[baseline_rows["date"] >= TEST_START]
    results = []
    for column, label in [
        ("naive_yesterday", "Naive: yesterday"),
        ("seasonal_naive_7d", "Seasonal naive: last week"),
    ]:
        scored = baseline_test.dropna(subset=[column])
        results.append(metric_row(label, scored["sales"], scored[column]))
    results.append(metric_row("HistGradientBoosting", test["sales"], test["model_prediction"]))
    metrics = pd.DataFrame(results)

    test["weekday"] = test["date"].dt.day_name()
    test["absolute_error"] = (test["sales"] - test["model_prediction"]).abs()
    weekday_order = [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]
    weekday_errors = (
        test.groupby("weekday")["absolute_error"].mean()
        .reindex(weekday_order)
        .rename("MAE")
        .reset_index()
    )
    return metrics, weekday_errors, test


def save_reports(
    metrics: pd.DataFrame, weekday_errors: pd.DataFrame, forecasts: pd.DataFrame
) -> None:
    """Write metric tables and a representative forecast-versus-actual plot."""
    ROOT.joinpath("reports").mkdir(exist_ok=True)
    metrics.to_csv(METRICS_PATH, index=False)
    weekday_errors.to_csv(WEEKDAY_PATH, index=False)

    comparison, axis = plt.subplots(figsize=(9, 4.5))
    bars = axis.bar(metrics["model"], metrics["MAE"], color=["#94a3b8", "#64748b", "#2563eb"])
    axis.set(title="Held-out mean absolute error", ylabel="MAE (units)")
    axis.grid(axis="y", alpha=0.2)
    axis.bar_label(bars, fmt="%.2f", padding=3)
    axis.set_ylim(0, max(metrics["MAE"]) * 1.18)
    axis.tick_params(axis="x", rotation=12)
    comparison.tight_layout()
    comparison.savefig(MODEL_COMPARISON_PATH, dpi=150)
    plt.close(comparison)

    series = forecasts[(forecasts["store"] == 1) & (forecasts["item"] == 1)]
    fig, axis = plt.subplots(figsize=(11, 4))
    axis.plot(series["date"], series["sales"], label="Actual", linewidth=1.5)
    axis.plot(series["date"], series["model_prediction"], label="Forecast", linewidth=1.5)
    axis.set(title="Store 1 / Item 1: holdout forecast", ylabel="Units sold")
    axis.legend()
    axis.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(FORECAST_PATH, dpi=150)
    plt.close(fig)


def main() -> None:
    """Run the temporal evaluation and print its measured results."""
    metrics, weekday_errors, forecasts = evaluate_model(load_sales())
    save_reports(metrics, weekday_errors, forecasts)
    print(f"Test period: {TEST_START.date()} to {forecasts['date'].max().date()}")
    print(metrics.round(2).to_string(index=False))
    print("\nModel MAE by weekday:")
    print(weekday_errors.round(2).to_string(index=False))
    print(f"Saved forecast chart to {FORECAST_PATH}")
    print(f"Saved model comparison chart to {MODEL_COMPARISON_PATH}")


if __name__ == "__main__":
    main()
