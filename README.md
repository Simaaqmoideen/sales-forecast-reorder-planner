# Project 4: Sales Prediction Project

> Use past sales data to predict future sales and support inventory decisions.

**What you will learn:** Time-series forecasting: lag and rolling features, time-based train/test splits, baselines, MAE / RMSE / MAPE, and how forecasts feed inventory planning.

```mermaid
flowchart LR
    A[Daily sales CSV] --> B[Validate and clean]
    B --> C[Calendar, lag, rolling features]
    C --> D[Time-based split]
    D --> E[Naive baselines]
    D --> F[HistGradientBoosting]
    E --> G[MAE / RMSE / MAPE]
    F --> G
    G --> H[Forecast dashboard]
    H --> I[Reorder suggestion + safety stock]
```

## Quick start
```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS / Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/generate_data.py
python src/eda.py
python src/baselines.py
python src/train.py
python src/evaluate.py
python src/recommend_reorder.py --store 1 --item 1 --on-hand 20
streamlit run app.py
```
Run the tests with `python -m pytest -q` from this folder.

The EDA command validates the generated CSV, prints its coverage and average
sales by weekday, and writes `reports/sales_overview.png` with the daily sales
trend and weekday pattern.
The baseline command compares a one-day naive forecast with the same weekday
from the previous week, using dates from 2023-07-01 onward as the held-out test
period. It writes `reports/baseline_metrics.csv`.
The training command fits a reproducible HistGradientBoosting model on data
strictly before that cutoff and saves `models/sales_model.joblib`.
The shared cleaning step rejects invalid values, combines duplicate
date/store/item records, and fills missing dates within each series with zero
sales and no promotion.
The evaluation command measures MAE, RMSE, and MAPE for both baselines and the
ML model on the same 2023-07-01 onward holdout, and writes a forecast chart and
weekday error table under `reports/`.
The reorder CLI trains on all available history for a next-day forecast and
calculates suggested units from on-hand inventory and a configurable safety
factor. Add `--promo` when promotion is planned; use `--safety-factor 0.3` to
set safety stock to 30% of forecast demand. The dashboard provides the same
controls in a browser.

### Held-out results

These results use the synthetic data from 2023-07-01 through 2023-12-31.
Forecasting is one-step rolling: each test day can use actual observations
from earlier test days as lag features.

| Model | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| Naive: yesterday | 9.79 | 13.37 | 22.88% |
| Seasonal naive: last week | 8.83 | 12.06 | 21.03% |
| HistGradientBoosting | 5.49 | 7.12 | 13.60% |

![Store 1, item 1 held-out forecast compared with actual sales](reports/forecast.png)

The largest model error was 42.84 units on a synthetic promo-day spike; other
large errors were stochastic non-promo peaks. Lag and rolling features smooth
some of these peaks. Exact scores can vary slightly across supported
scikit-learn versions.

## Folder map
| Path | Purpose |
|---|---|
| `docs/01_PROJECT_BRIEF.md` | Problem, users, scope, success criteria |
| `docs/02_REQUIREMENTS.md` | Must / should / could requirements and non-functional needs |
| `docs/03_ARCHITECTURE.md` | Design, components, tech stack |
| `docs/04_DATA.md` | Data sources, schema and data rules |
| `docs/05_ROADMAP.md` | Phase-by-phase build plan with checklists |
| `docs/06_TESTING_EVALUATION.md` | Test plan and evaluation metrics |
| `docs/07_RISKS_ETHICS.md` | Risks, mitigations, ethics notes |
| `docs/08_DELIVERABLES_CHECKLIST.md` | Definition of done |
| `docs/09_REPORT_TEMPLATE.md` | Final report / presentation outline |
| `src/` | Starter source code |
| `app.py` | Thin Streamlit dashboard |
| `tests/` | Automated tests |
| `data/` | Datasets (git-ignored except samples) |
| `notebooks/` | Exploration notebooks |
| `reports/` | Generated charts and metrics |

### Sales trend and weekday pattern

![Synthetic daily total sales with a seven-day rolling mean and average sales by weekday](reports/sales_overview.png)

## Tech stack
- Python 3.10+
- pandas, numpy
- scikit-learn (GradientBoosting / RandomForest)
- matplotlib
- statsmodels or prophet (optional)
- pytest
