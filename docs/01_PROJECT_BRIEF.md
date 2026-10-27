# Project Brief: Sales Prediction Project

## One-line summary
Use past sales data to predict future sales and support inventory decisions.

## Problem statement
Stocking too much ties up cash; too little loses sales. Forecasting demand lets a business plan inventory.

## Learning goals
Time-series forecasting: lag and rolling features, time-based train/test splits, baselines, MAE / RMSE / MAPE, and how forecasts feed inventory planning.

## Target users
- Store or operations managers
- Analysts studying demand forecasting

## In scope
- Load and clean historical sales data
- Feature engineering: calendar features, lags, rolling means
- Time-based split (never random)
- Compare a naive baseline against at least one ML model
- Report MAE, RMSE and MAPE; plot forecast versus actual

## Out of scope (for v1)
- Production-scale infrastructure, authentication and payments
- Anything under "Could have" in `02_REQUIREMENTS.md` unless time remains

## Success criteria
- ML model beats seasonal-naive on MAE
- MAPE under ~15% on the synthetic data (real data varies)
- No leakage: features use only data available before the forecast date

## Owner / timeline
- Owner: _your name_
- Start date: ____  Target finish: ____ (see `05_ROADMAP.md`)
