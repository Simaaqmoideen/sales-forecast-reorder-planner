"""Create synthetic daily sales for 3 stores x 5 items (2019-2023) -> data/sales.csv"""
import pathlib
import numpy as np, pandas as pd

rng = np.random.default_rng(42)
dates = pd.date_range("2019-01-01", "2023-12-31", freq="D")
rows = []
for store in range(1, 4):
    for item in range(1, 6):
        base = rng.uniform(15, 45)
        t = np.arange(len(dates))
        trend = 1 + 0.0003 * t
        weekly = 1 + 0.25 * np.isin(dates.day_of_week, [4, 5, 6])
        yearly = 1 + 0.2 * np.sin(2 * np.pi * (dates.day_of_year - 80) / 365)
        promo = rng.random(len(dates)) < 0.08
        mu = base * trend * weekly * yearly * (1 + 0.35 * promo) * (1 + 0.1 * (store - 2))
        sales = rng.poisson(mu)
        rows.append(pd.DataFrame({"date": dates, "store": store, "item": item, "promo": promo.astype(int), "sales": sales}))
out = pathlib.Path(__file__).resolve().parents[1] / "data"
out.mkdir(exist_ok=True)
pd.concat(rows).to_csv(out / "sales.csv", index=False)
print("wrote", out / "sales.csv")
