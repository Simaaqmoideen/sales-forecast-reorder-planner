# Testing and Evaluation: Sales Prediction Project

## Success metrics
- ML model beats seasonal-naive on MAE
- MAPE under ~15% on the synthetic data (real data varies)
- No leakage: features use only data available before the forecast date

## Test plan
- [x] Unit: lag features at row t equal the target at t-lag
- [x] Unit: rolling features never include the current day
- [x] Evaluation: metrics for baseline and model in one table
- [x] Manual: plot forecast versus actuals and inspect the biggest misses

## How to run tests
```bash
python -m pytest -q
```

## Results log
| Date | Experiment / test | Result | Conclusion |
|---|---|---|---|
| 2026-10-27 | `python src/generate_data.py`; `python src/eda.py` | Generated 27,390 rows from 2019-01-01 to 2023-12-31 (3 stores, 5 items); chart saved to `reports/sales_overview.png`. Friday mean sales: 682.5; Monday: 544.4. Pytest was initially unavailable; it was installed later. | Synthetic data generation and EDA completed; weekday pattern is visible. The full suite was later verified. |
| 2026-10-27 | `python src/baselines.py` on the 2023-07-01–2023-12-31 time holdout | Yesterday: MAE 9.79, RMSE 13.37, MAPE 22.88%. Last week: MAE 8.83, RMSE 12.06, MAPE 21.03%. Metrics saved in `reports/baseline_metrics.csv`. | Seasonal naive is the stronger baseline so far; the final model must beat MAE 8.83 to meet the project success criterion. |
| 2026-10-27 | `python src/train.py` | Fitted HistGradientBoosting on 24,210 feature rows from 2019-01-29 through 2023-06-30 and saved `models/sales_model.joblib`. No holdout metrics were used for fitting. | Training artifact was fit only on the training dates; the full suite was later verified. |
| 2026-10-27 | Clean Python 3.14 environment `python src/evaluate.py` on the 2023-07-01–2023-12-31 holdout; visual review of forecast and largest absolute errors | Yesterday baseline: 9.79 / 13.37 / 22.88%; seasonal naive: 8.83 / 12.06 / 21.03%; HistGradientBoosting: 5.49 / 7.12 / 13.60% (MAE / RMSE / MAPE). Weekday model MAE ranges from 5.01 (Monday) to 5.92 (Sunday). Largest miss was 42.84 units (store 3/item 5, 2023-10-26, promo day); other large misses include stochastic non-promo peaks. | Model beats the strongest baseline on MAE and meets the synthetic MAPE target. It smooths isolated spikes; one-step rolling evaluation uses prior observed sales. |
| 2026-10-27 | `python src/recommend_reorder.py --store 1 --item 1 --on-hand 20`; dashboard browser smoke check | Clean-environment CLI forecast 42.4 units for 2024-01-01 and suggested ordering 32 units with the default 20% safety factor. Dashboard rendered forecasts, held-out metrics, weekday errors, and updated the recommendation to 0 units when on-hand stock was set to 100. Clean-environment `python -m pytest -q`: 10 passed. | Reorder and dashboard flows work. Holiday labels are unavailable in the selected synthetic data; the point forecast is not a confidence interval. |
| 2026-10-27 | Fresh detached worktree at `fea84e0`, isolated Python 3.14 virtual environment, and README commands | Installed all requirements; generation, EDA, baselines, training, evaluation, reorder CLI, and dashboard launch completed. `python -m pytest -q`: 10 passed. | Clean checkout setup works. Metric differences across supported library versions are small; README values match this isolated environment. |
