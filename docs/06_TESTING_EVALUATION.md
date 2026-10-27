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
