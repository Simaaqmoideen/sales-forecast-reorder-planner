# Risks and Ethics: Sales Prediction Project

| Risk | Mitigation |
|---|---|
| Data leakage via lag or rolling features | Shift by at least 1 day before rolling; test with a unit test. |
| Random split inflates scores | Always split by time. |
| Forecasts treated as certain | Show held-out MAE, state that no prediction interval is calculated, and let the user configure safety stock. |

## Ethics and responsible-use notes
- Be honest about limitations in the README and report; do not overstate accuracy.
- Use only data you are allowed to use; anonymise any personal information.
- Document who could be harmed by a wrong output and how the design reduces that risk.
