# Architecture: Sales Prediction Project

## Overview
```
Raw sales CSV -> src/data.py (clean, parse dates, fill gaps)
                       |
                       v
        src/features.py: calendar, lag_7, lag_28, rolling_mean_7
                       |
              time split: train | validation | test
                       |
        +--------------+--------------+
        v                             v
  Baseline (last week)      ML model (src/train.py)
        \                             /
         +--------> src/evaluate.py (MAE, RMSE, MAPE, plots)
                       |
                       v
          reports/forecast.png + reorder suggestion
```

## Tech stack
- Python 3.10+
- pandas, numpy
- scikit-learn (GradientBoosting / RandomForest)
- matplotlib
- statsmodels or prophet (optional)
- pytest

## Design decisions (fill in as you go)
| Decision | Options considered | Choice | Why |
|---|---|---|---|
| | | | |

## Module responsibilities
See the files in `src/`. Keep logic (testable functions) separate from UI and scripts.
