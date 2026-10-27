# Testing and Evaluation: Sales Prediction Project

## Success metrics
- ML model beats seasonal-naive on MAE
- MAPE under ~15% on the synthetic data (real data varies)
- No leakage: features use only data available before the forecast date

## Test plan
- [ ] Unit: lag features at row t equal the target at t-lag
- [ ] Unit: rolling features never include the current day
- [ ] Evaluation: metrics for baseline and model in one table
- [ ] Manual: plot forecast versus actuals and inspect the biggest misses

## How to run tests
```bash
python -m pytest -q
```

## Results log
| Date | Experiment / test | Result | Conclusion |
|---|---|---|---|
| 2026-10-27 | `python src/generate_data.py`; `python src/eda.py` | Generated 27,390 rows from 2019-01-01 to 2023-12-31 (3 stores, 5 items); chart saved to `reports/sales_overview.png`. Friday mean sales: 682.5; Monday: 544.4. `python -m pytest -q` could not run: pytest is not installed, and pip could not reach its package index (DNS failure). | Synthetic data generation and EDA completed; weekday pattern is visible. Automated tests remain unverified in this environment. |
| 2026-10-27 | `python src/baselines.py` on the 2023-07-01–2023-12-31 time holdout | Yesterday: MAE 9.79, RMSE 13.37, MAPE 22.88%. Last week: MAE 8.83, RMSE 12.06, MAPE 21.03%. Metrics saved in `reports/baseline_metrics.csv`. Pytest could not run (`No module named pytest`). | Seasonal naive is the stronger baseline so far; the later ML model must beat MAE 8.83 to meet the project success criterion. |
| 2026-10-27 | `python src/train.py` | Fitted HistGradientBoosting on 24,210 feature rows from 2019-01-29 through 2023-06-30 and saved `models/sales_model.joblib`. No holdout metrics were used for fitting. `python -m pytest -q` could not run (`No module named pytest`). | Training artifact is ready for the separate temporal evaluation phase; automated tests remain unverified. |
