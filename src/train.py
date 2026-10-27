"""Fit a sales forecasting model using data before the temporal test cutoff."""

from pathlib import Path
import sys

import joblib
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

# Support both ``python src/train.py`` and ``python -m src.train``.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data import load_sales
from src.features import FEATURES, add_features


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "sales_model.joblib"
TEST_START = pd.Timestamp("2023-07-01")


def train_model(
    data: pd.DataFrame, test_start: pd.Timestamp = TEST_START
) -> tuple[HistGradientBoostingRegressor, pd.DataFrame]:
    """Fit and return a model using only rows before the test start date."""
    featured = add_features(data)
    train = featured[featured["date"] < test_start]
    if train.empty:
        raise ValueError("No training rows exist before the test start date")
    model = HistGradientBoostingRegressor(
        max_iter=300, learning_rate=0.05, random_state=0
    )
    model.fit(train[FEATURES], train["sales"])
    return model, train


def main() -> None:
    """Fit on the training period and save the trained model artifact."""
    model, train = train_model(load_sales())
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Training period: {train['date'].min().date()} to {train['date'].max().date()}")
    print(f"Training rows: {len(train):,}")
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
