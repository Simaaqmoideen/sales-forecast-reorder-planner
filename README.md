# Project 4: Sales Prediction Project

> Use past sales data to predict future sales and support inventory decisions.

**What you will learn:** Time-series forecasting: lag and rolling features, time-based train/test splits, baselines, MAE / RMSE / MAPE, and how forecasts feed inventory planning.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/generate_data.py
python src/eda.py
python src/baselines.py
python src/train.py
```
Run the tests with `python -m pytest -q` from this folder.

The EDA command validates the generated CSV, prints its coverage and average
sales by weekday, and writes `reports/sales_overview.png` with the daily sales
trend and weekday pattern.
The baseline command compares a one-day naive forecast with the same weekday
from the previous week, using dates from 2023-07-01 onward as the held-out test
period. It writes `reports/baseline_metrics.csv`.

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
| `tests/` | Automated tests |
| `data/` | Datasets (git-ignored except samples) |
| `notebooks/` | Exploration notebooks |
| `reports/` | Generated charts and metrics |

## Tech stack
- Python 3.10+
- pandas, numpy
- scikit-learn (GradientBoosting / RandomForest)
- matplotlib
- statsmodels or prophet (optional)
- pytest
