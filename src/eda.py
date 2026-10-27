"""Summarize and plot the generated daily sales time series."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sales.csv"
PLOT_PATH = ROOT / "reports" / "sales_overview.png"
REQUIRED_COLUMNS = {"date", "store", "item", "promo", "sales"}


def load_sales(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load sales data and fail clearly when required fields are invalid."""
    data = pd.read_csv(path, parse_dates=["date"])
    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Sales data is missing columns: {sorted(missing)}")
    if data[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError("Sales data contains missing values in required columns")
    if data.duplicated(["date", "store", "item"]).any():
        raise ValueError("Sales data contains duplicate date/store/item rows")
    if (data["sales"] < 0).any():
        raise ValueError("Sales values must be non-negative")
    return data.sort_values("date")


def create_sales_overview(data: pd.DataFrame, output_path: Path = PLOT_PATH) -> None:
    """Save daily aggregate sales, a smoothed trend, and weekday seasonality."""
    daily = data.groupby("date", as_index=False)["sales"].sum()
    weekday = data.assign(weekday=data["date"].dt.day_name()).groupby(
        "weekday", sort=False
    )["sales"].mean()
    weekday_order = [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), constrained_layout=True)
    axes[0].plot(daily["date"], daily["sales"], alpha=0.35, label="Daily total")
    axes[0].plot(
        daily["date"], daily["sales"].rolling(7).mean(),
        linewidth=2, label="7-day rolling mean"
    )
    axes[0].set(title="Daily sales over time", ylabel="Units sold")
    axes[0].legend()
    axes[0].grid(alpha=0.2)

    axes[1].bar(weekday_order, weekday.reindex(weekday_order))
    axes[1].set(title="Average sales by weekday", ylabel="Mean units sold")
    axes[1].tick_params(axis="x", rotation=20)
    axes[1].grid(axis="y", alpha=0.2)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def main() -> None:
    """Print dataset coverage and save the exploratory overview chart."""
    data = load_sales()
    daily = data.groupby("date")["sales"].sum()
    print(f"Rows: {len(data):,}")
    print(f"Date range: {data['date'].min().date()} to {data['date'].max().date()}")
    print(f"Stores: {data['store'].nunique()}, items: {data['item'].nunique()}")
    print(f"Average weekday sales: {daily.groupby(daily.index.day_name()).mean().round(1).to_dict()}")
    create_sales_overview(data)
    print(f"Saved overview chart to {PLOT_PATH}")


if __name__ == "__main__":
    main()
