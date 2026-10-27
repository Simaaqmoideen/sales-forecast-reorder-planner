# Roadmap: Sales Prediction Project

Suggested pace: one phase every 2-4 days (about 2-3 weeks in total).

## Phase 1: Setup and data
Generate or download data. Plot total daily sales; identify trend and seasonality.

- [x] Task completed
- [x] Notes written in the project log
- [x] Changes committed

## Phase 2: Baselines
Naive (yesterday), seasonal naive (same weekday last week). These are the numbers to beat.

- [x] Task completed
- [x] Notes written in the project log
- [x] Changes committed

## Phase 3: Features and model
Add lags and rolling means (computed only from the past). Train GradientBoosting.

- [x] Task completed
- [x] Notes written in the project log
- [x] Changes committed

## Phase 4: Evaluate
Time-based test set, metrics table, forecast plot, error analysis by weekday.

- [x] Task completed
- [x] Notes written in the project log
- [x] Changes committed

## Phase 5: Decision layer
Convert forecast into a suggested reorder quantity with a safety stock. Dashboard and README.

- [ ] Task completed
- [ ] Notes written in the project log
- [ ] Changes committed

## Project log
| Date | What I did | Blockers | Next |
|---|---|---|---|
| 2026-10-27 | Generated the documented synthetic sales data and added a validating EDA script with a daily trend and weekday seasonality chart. Data covers 2019-01-01 through 2023-12-31 across 3 stores and 5 items; Friday averaged 682.5 units versus Monday's 544.4. | Pytest was initially unavailable; it was later installed from cache and the full suite passed. | Phase 2: compare yesterday and last-week baselines on a time-based holdout. |
| 2026-10-27 | Added prior-day and prior-week baseline forecasts, temporal holdout scoring, and unit tests. On 2023-07-01 through 2023-12-31, yesterday MAE/RMSE/MAPE were 9.79/13.37/22.88%; last-week values were 8.83/12.06/21.03%. | Pytest was initially unavailable; it was later installed from cache and the full suite passed. | Phase 3: engineer leakage-safe features and train the ML model against these baselines. |
| 2026-10-27 | Added shared sales cleaning (invalid values rejected, duplicate keys aggregated, missing dates filled), a prior-day model feature, and training-only HistGradientBoosting fitting. The model trained on 24,210 rows through 2023-06-30. | Pytest was initially unavailable; it was later installed from cache and the full suite passed. | Phase 4: evaluate the saved model on the held-out dates and compare with both baselines. |
| 2026-10-27 | Evaluated the baselines and HistGradientBoosting on held-out 2023-07-01–2023-12-31 dates, saved metrics and forecast plots, and reviewed weekday errors and largest misses. ML MAE/RMSE/MAPE were 5.49/7.12/13.58%; all 8 tests passed. | None. | Phase 5: add reorder recommendations and the Streamlit dashboard after the Must-have pipeline passed tests. |
