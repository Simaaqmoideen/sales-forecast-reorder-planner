"""Streamlit dashboard for sales forecasts and inventory reorder guidance."""

from pathlib import Path

import pandas as pd
import streamlit as st
from sklearn.ensemble import HistGradientBoostingRegressor

from src.data import DATA_PATH, load_sales
from src.forecast import fit_full_history_model, forecast_next_day
from src.reorder import reorder_quantity


ROOT = Path(__file__).resolve().parent
METRICS_PATH = ROOT / "reports" / "metrics.csv"
WEEKDAY_PATH = ROOT / "reports" / "weekday_error.csv"
FORECAST_PLOT = ROOT / "reports" / "forecast.png"


@st.cache_data(show_spinner="Loading sales history…")
def get_sales_data() -> pd.DataFrame:
    """Load and clean sales history for the dashboard."""
    return load_sales(DATA_PATH)


@st.cache_resource(show_spinner="Training the forecasting model on history…")
def get_model() -> HistGradientBoostingRegressor:
    """Train once per dashboard process; reuse the model across UI changes."""
    return fit_full_history_model(get_sales_data())


@st.cache_data(show_spinner="Generating next-day forecasts…")
def get_forecast(promo_flags: dict[tuple[int, int], int]) -> pd.DataFrame:
    """Create next-day predictions using the selected promotion plan."""
    return forecast_next_day(get_sales_data(), promo_flags, get_model())


def main() -> None:
    """Render forecast, historical model results, and reorder controls."""
    st.set_page_config(page_title="Sales Forecast & Reorder", page_icon="📦", layout="wide")
    st.title("Sales Forecast & Reorder Planner")
    st.caption(
        "Synthetic daily sales forecast. Use the suggested reorder as a planning aid; "
        "actual demand can differ from the point forecast."
    )

    try:
        data = get_sales_data()
        first, second = st.columns(2)
        with first:
            store = int(st.selectbox("Store", sorted(data["store"].unique())))
        with second:
            item = int(st.selectbox("Item", sorted(data["item"].unique())))

        promo_active = st.checkbox("Promotion planned for this store and item")
        safety_percent = st.slider("Safety stock (%)", min_value=0, max_value=100, value=20)
        promo_flags = {(store, item): int(promo_active)}
        forecasts = get_forecast(promo_flags)
        selected = forecasts[
            (forecasts["store"] == store) & (forecasts["item"] == item)
        ].iloc[0]

        stock = st.number_input("Units currently on hand", min_value=0, value=0, step=1)
        recommendation = reorder_quantity(
            [float(selected["forecast_sales"])],
            on_hand=stock,
            safety_factor=safety_percent / 100,
        )

        forecast_card, reorder_card, date_card = st.columns(3)
        forecast_card.metric("Next-day demand forecast", f"{selected['forecast_sales']:.1f} units")
        reorder_card.metric("Suggested reorder", f"{recommendation} units")
        date_card.metric("Forecast date", selected["date"].strftime("%Y-%m-%d"))
        st.caption(
            f"Forecast assumes promotion is {'active' if promo_active else 'off'}; "
            f"safety stock is {safety_percent}% of forecast demand."
        )

        st.subheader("Next-day forecasts by store and item")
        st.dataframe(
            forecasts[["store", "item", "date", "promo", "forecast_sales"]]
            .rename(columns={"forecast_sales": "forecast_units"})
            .round({"forecast_units": 1}),
            width="stretch",
            hide_index=True,
        )

        left, right = st.columns(2)
        with left:
            st.subheader("Held-out model results")
            if METRICS_PATH.exists():
                st.dataframe(pd.read_csv(METRICS_PATH).round(2), hide_index=True)
                st.caption("Historical rolling holdout; these are not next-day confidence intervals.")
        with right:
            st.subheader("Model MAE by weekday")
            if WEEKDAY_PATH.exists():
                errors = pd.read_csv(WEEKDAY_PATH).set_index("weekday")
                st.bar_chart(errors)
        if FORECAST_PLOT.exists():
            st.subheader("Held-out forecast versus actual")
            st.image(str(FORECAST_PLOT), width="stretch")
    except (ValueError, FileNotFoundError) as exc:
        st.error(str(exc))


if __name__ == "__main__":
    main()
