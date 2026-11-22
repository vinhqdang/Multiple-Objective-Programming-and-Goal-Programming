"""Hybrid MI-IGP with the banks' OWN inflation forecasts (4 quarters ahead) as the inflation input, K=2 with the
GDP growth gap. Specification fixed before results: for each decision quarter q, take the latest forecast vintage
published on or before the first day of q and its forecast for quarter q+4. Banks with forecast vintages covering
the window and positive rates: GB, CA, AU, SE, NO. Caveat: published forecasts are conditional on a policy path,
so at long horizons they tend towards the target by construction; the 4-quarter horizon limits but does not remove this."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, migp
from inverse_interval_gp_cb import ZLB
from real_cb_migp_k2 import build

SPEC = [  # country, variable, start, end, stated target
    ("GB", "CPI_yoy_q", "2004Q2", "2019Q4", 2.0), ("CA", "CPI_yoy_q", "1996Q1", "2019Q4", 2.0),
    ("AU", "CPI_yoy_q", "1994Q1", "2019Q4", 2.5), ("SE", "CPI_yoy_qavg", "2007Q2", "2017Q2", 2.0),
    ("NO", "CPI_4q", "2013Q4", "2018Q1", 2.5)]
F = pd.read_csv("data/central_banks/forecasts.csv.gz", parse_dates=["vintage_date"])

def forecast_series(cc, var, quarters):
    f = F[(F.country == cc) & (F.variable == var)].copy()
    out = {}
    for q in quarters:
        start = q.start_time; tgt = str(q + 4).replace("Q", "-Q")
        v = f[f.vintage_date <= start]
        if v.empty: continue
        last = v[v.vintage_date == v.vintage_date.max()]
        row = last[last.target_period == tgt]
        if len(row): out[q] = row.value.iloc[0]
    return pd.Series(out)

rows = []
for cc, var, s, e, tgt in SPEC:
    q = build(cc); q = q[(q.index >= pd.Period(s, "Q")) & (q.index <= pd.Period(e, "Q")) & (q.rate_start > ZLB)]
    q["fc"] = forecast_series(cc, var, q.index); q = q.dropna(subset=["fc"])
    q["x_gap"] = q.growth - q.growth.mean(); X = q[["fc", "x_gap"]].values; D = q.D.values
    best = None
    for seed in range(3):
        h = migp.fit_hybrid(X, D, seed=seed)
        if best is None or h["loss"] < best["loss"]: best = h
    A = np.column_stack([np.ones(len(D)), X]); a, phi, gam = np.linalg.lstsq(A, D, rcond=None)[0]
    rows.append(dict(country=cc, stated=tgt, n=len(D), tau_pi=round(best["tau"][0], 2), b_pi=round(best["b"][0], 2),
                     alpha_pi=round(best["alpha"][0], 2), loss=round(best["loss"], 3), mean_forecast=round(X[:, 0].mean(), 2),
                     mean_realised=round(q.x_pi.mean(), 2), taylor_tau=round(-a / phi, 2) if phi > 0 else np.nan))
    print(rows[-1], flush=True)
d = pd.DataFrame(rows); d.to_csv("results/real_cb_forecast_hybrid.csv", index=False)
for m in ["tau_pi", "mean_forecast", "mean_realised", "taylor_tau"]:
    v = d[m]; ok = v.notna(); print(f"{m}: MAE {np.abs(v[ok]-d.stated[ok]).mean():.2f} (n={ok.sum()})")
