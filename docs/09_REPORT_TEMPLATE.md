# Sales Prediction: Forecasting and Reorder Guidance

**Author:** Project owner
**Date:** 2026-10-27

## Abstract

This project forecasts daily sales for individual store and product pairs to support inventory planning. It uses a reproducible synthetic dataset with calendar, promotion, lag, and rolling-mean features in a time-series pipeline. A HistGradientBoosting model was trained before 2023-07-01 and evaluated on the later 2023-07-01 through 2023-12-31 period using one-step rolling forecasts. The model achieved MAE 5.49, RMSE 7.12, and MAPE 13.58%, improving on the seasonal-naive MAE of 8.83. A Streamlit dashboard and command-line tool turn next-day forecasts into reorder suggestions with configurable safety stock.

## Introduction

Retailers need enough stock to meet demand while avoiding excessive inventory. A daily sales forecast can help set replenishment quantities, but forecasts should be compared with simple baselines and treated as estimates. This project provides a small, reproducible example of that workflow.

## Data

The included generator creates 27,390 daily observations from 2019-01-01 through 2023-12-31 for 3 stores and 5 items. It includes trend, weekly and yearly seasonality, Poisson sales variation, and synthetic promotion flags. The cleaning pipeline validates fields and values, sums duplicate date/store/item rows, and fills missing dates within a series with zero sales and no promotion. These zero fills assume an absent daily record means no recorded sales. The data is synthetic and does not include region-specific holidays or real retail effects.

## Method

Calendar features include weekday, month, and day of year. Lag features use the previous day, previous week, and previous 28 days; rolling means are shifted so they include only earlier observations. The 2023-07-01 time cutoff separates training from evaluation; no random split is used. Yesterday and last-week seasonal-naive forecasts provide baselines. HistGradientBoosting uses the same temporal split. Test evaluation is one-step rolling: each test date may use observed sales from earlier dates in the test period. For the next-day recommendation, a separate final model is fitted on all available history.

## Results

| Model | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| Naive: yesterday | 9.79 | 13.37 | 22.88% |
| Seasonal naive: last week | 8.83 | 12.06 | 21.03% |
| HistGradientBoosting | 5.49 | 7.12 | 13.58% |

The model's weekday MAE ranges from 5.03 units on Monday to 5.91 on Sunday. The forecast-versus-actual chart is in `reports/forecast.png`; the EDA trend and weekday chart is in `reports/sales_overview.png`.

## Discussion and error analysis

The model beats both baselines on MAE and stays below the synthetic-data MAPE target of about 15%. The largest absolute miss was 41.36 units for store 3/item 5 on 2023-10-26, a promotion day with an observed spike. Other large misses were stochastic non-promotion peaks. Lag and rolling features smooth such spikes, so the model can under-forecast abrupt demand changes.

## Limitations and ethics

The results describe only synthetic data; performance on real stores and products may differ. The test simulates one-step replenishment where recent actual sales become available each day; it does not measure a long open-loop forecast horizon. The forecast is a point estimate, not a probability interval. The reorder rule adds a user-selected safety stock but does not account for lead time, supplier constraints, perishability, or service-level targets. Users should review the suggestion against operational context.

## Future work

- Add licensed holiday-labelled data and compare holiday effects.
- Evaluate against Store Item Demand or Rossmann data with documented splits and licences.
- Add lead-time and service-level settings to reorder logic.
- Measure performance over multi-day horizons and report uncertainty.

## References

- Synthetic data generator: `src/generate_data.py` (project implementation).
- pandas for data handling: https://pandas.pydata.org/
- scikit-learn HistGradientBoostingRegressor: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html
- Streamlit: https://docs.streamlit.io/

## Appendix: reproduction

Follow the commands in the project README to create the synthetic data, generate reports, evaluate the model, run the reorder CLI, and launch the dashboard. Run automated tests with `python -m pytest -q`.
