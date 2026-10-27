# Data: Sales Prediction Project

## Sources
- Kaggle 'Store Item Demand Forecasting Challenge' (5 years, 10 stores, 50 items).
- Kaggle 'Rossmann Store Sales' (richer: promos, holidays).
- Included: `python src/generate_data.py` creates a synthetic dataset with trend, weekly and yearly seasonality so everything runs offline.

## Data handling rules
- Raw data is never edited by hand. Cleaning is done by code and written to a new file.
- Large files are not committed (see `.gitignore`); document how to download them instead.
- Respect each dataset's licence and terms of service; cite the source in the final report.
- Do not store personal or sensitive information unless it is anonymised.

## Data dictionary (fill in after loading the data)
| Column | Type | Meaning | Missing values? |
|---|---|---|---|
| date | datetime | Daily observation date | No; invalid dates are rejected |
| store | integer | Store identifier (1-3 in the synthetic data) | No; invalid IDs are rejected |
| item | integer | Product identifier (1-5 in the synthetic data) | No; invalid IDs are rejected |
| promo | integer | Whether promotion was active (0/1) | No; other values are rejected |
| sales | integer | Units sold | No; negative and invalid values are rejected |

The cleaning pipeline combines duplicate date/store/item rows by summing sales
and retaining the maximum promo flag. Missing dates inside an observed
store-item series are filled with zero sales and no promotion; this treats an
absent daily record as no recorded sales.

## Data quality checklist
- [x] Row count and column types checked
- [x] Missing values counted and a handling decision recorded
- [x] Duplicates removed
- [ ] Outliers and impossible values reviewed
- [ ] Train / test split strategy written down
