# Requirements: Sales Prediction Project

## Functional requirements (MoSCoW)

### Must have
- [ ] Load and clean historical sales data
- [ ] Feature engineering: calendar features, lags, rolling means
- [ ] Time-based split (never random)
- [ ] Compare a naive baseline against at least one ML model
- [ ] Report MAE, RMSE and MAPE; plot forecast versus actual

### Should have
- [ ] Per-store / per-product models or store as a feature
- [ ] Holiday and promotion features
- [ ] Simple reorder-quantity suggestion from the forecast
- [ ] Dashboard in Streamlit

### Could have (stretch)
- [ ] Prophet or SARIMA comparison
- [ ] Prediction intervals
- [ ] Automated retraining script
- [ ] Scenario what-if (price change)

## Non-functional requirements
- **Reproducible:** a fresh clone runs end to end with the commands in README.md.
- **Secure:** secrets only in `.env`; no keys, tokens or personal data in Git.
- **Readable:** type hints on public functions, docstrings on modules, PEP 8 formatting.
- **Tested:** automated tests for core logic; they pass before every merge.
- **Documented:** README and docs updated whenever behaviour changes.

## Assumptions
- Python 3.10 or newer; internet access to install packages and fetch data.
- Free-tier / free-dataset resources are used wherever possible.

## Constraints
- Solo or small-team student project; target is a working demo, not production.
