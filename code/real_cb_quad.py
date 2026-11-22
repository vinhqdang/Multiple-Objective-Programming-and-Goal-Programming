"""Gradualism model (quadratic adjustment cost) on central banks, K=2 (inflation 4 quarters ahead realised,
GDP growth gap), quarterly; plus the official-forecast variant for GB, CA, AU. Same windows as before."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, migp_quad as Q
from inverse_interval_gp_cb import WINDOWS, ZLB
from real_cb_migp_k2 import build
from real_cb_forecast_hybrid import SPEC, forecast_series

def best_fit(X, D, seeds=(0, 1)):
    best = None
    for s in seeds:
        h = Q.fit_hybrid(X, D, seed=s)
        if best is None or h["loss"] < best["loss"]: best = h
    return best

rows = []
for cc, s, e, tgt, note in WINDOWS:
    q = build(cc); q = q[(q.index >= pd.Period(s, "M").asfreq("Q")) & (q.index <= pd.Period(e, "M").asfreq("Q")) & (q.rate_start > ZLB)]
    q["x_gap"] = q.growth - q.growth.mean(); X = q[["x_pi", "x_gap"]].values; D = q.D.values
    h = best_fit(X, D)
    rows.append(dict(input="realised", country=cc, stated=tgt, n=len(D), tau_pi=round(h["tau"][0], 2), b_pi=round(h["b"][0], 2),
                     om_p=round(h["omega_p"][0], 2), om_m=round(h["omega_m"][0], 2), loss=round(h["loss"], 3), mean_x=round(X[:, 0].mean(), 2)))
    print(rows[-1], flush=True)
for cc, var, s, e, tgt in SPEC[:3]:
    q = build(cc); q = q[(q.index >= pd.Period(s, "Q")) & (q.index <= pd.Period(e, "Q")) & (q.rate_start > ZLB)]
    q["fc"] = forecast_series(cc, var, q.index); q = q.dropna(subset=["fc"])
    q["x_gap"] = q.growth - q.growth.mean(); X = q[["fc", "x_gap"]].values; D = q.D.values
    h = best_fit(X, D)
    rows.append(dict(input="official forecast", country=cc, stated=tgt, n=len(D), tau_pi=round(h["tau"][0], 2), b_pi=round(h["b"][0], 2),
                     om_p=round(h["omega_p"][0], 2), om_m=round(h["omega_m"][0], 2), loss=round(h["loss"], 3), mean_x=round(X[:, 0].mean(), 2)))
    print(rows[-1], flush=True)
d = pd.DataFrame(rows); d.to_csv("results/real_cb_quad.csv", index=False)
for inp, g in d.groupby("input"):
    print(inp, "MAE tau", np.abs(g.tau_pi - g.stated).mean().round(2), "MAE mean", np.abs(g.mean_x - g.stated).mean().round(2))
