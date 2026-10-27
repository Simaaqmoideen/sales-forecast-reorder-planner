import pandas as pd
from src.features import add_features
from src.reorder import reorder_quantity
from src.data import clean_sales


def _df():
    d = pd.date_range("2023-01-01", periods=60)
    return pd.DataFrame({"date": d, "store": 1, "item": 1, "promo": 0, "sales": range(60)})


def test_lag_equals_past_value():
    out = add_features(_df())
    row = out.iloc[0]
    assert row["lag_7"] == row["sales"] - 7


def test_rolling_excludes_today():
    out = add_features(_df())
    row = out.iloc[0]  # sales = k, previous 7 days = k-7..k-1, mean = k-4
    assert row["roll_mean_7"] == row["sales"] - 4


def test_reorder_never_negative():
    assert reorder_quantity([10, 10], on_hand=100) == 0
    assert reorder_quantity([10, 10], on_hand=0) == 24


def test_clean_sales_combines_duplicates_and_fills_missing_days():
    data = _df().iloc[:3].copy()
    data = data.drop(index=1)
    duplicate = _df().iloc[[0]].copy()
    duplicate["sales"] = 5
    cleaned = clean_sales(pd.concat([data, duplicate], ignore_index=True))
    assert len(cleaned) == 3
    assert cleaned.iloc[0]["sales"] == 5
    assert cleaned.iloc[1]["sales"] == 0


def test_lag_one_uses_previous_day():
    out = add_features(_df())
    assert out.iloc[0]["lag_1"] == out.iloc[0]["sales"] - 1
