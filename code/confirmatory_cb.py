"""Confirmatory run exactly as pre-registered in docs/09_preregistration_confirmatory_cb.md."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, migp_quad as Q
from inverse_interval_gp_cb import ZLB
import real_cb_migp_k2 as R
R.ISO3.update({"CZ": "CZE", "HU": "HUN", "KR": "KOR", "IL": "ISR", "CO": "COL", "ID": "IDN", "TR": "TUR", "IS": "ISL", "NZ": "NZL"})
W = pd.read_csv("results/confirmatory_windows.csv")
rows = []
for _, w in W.iterrows():
    cc, tgt = w.country, float(w.tgt)
    q = R.build(cc); q = q[(q.index >= pd.Period(w.q0, "Q")) & (q.index <= pd.Period(w.q1, "Q")) & (q.rate_start > ZLB)]
    if len(q) < 30:
        rows.append(dict(country=cc, stated=tgt, n=len(q), status="excluded (<30 quarters)")); print(rows[-1], flush=True); continue
    q["x_gap"] = q.growth - q.growth.mean(); X = q[["x_pi", "x_gap"]].values; D = q.D.values
    best = None
    for s in (0, 1, 2):
        h = Q.fit_hybrid(X, D, seed=s)
        if best is None or h["loss"] < best["loss"]: best = h
    rows.append(dict(country=cc, stated=tgt, n=len(q), status="included", window=f"{w.q0}-{w.q1}", tau_pi=round(best["tau"][0], 2),
                     b_pi=round(best["b"][0], 2), loss=round(best["loss"], 3), mean_infl=round(X[:, 0].mean(), 2)))
    print(rows[-1], flush=True)
d = pd.DataFrame(rows); d.to_csv("results/confirmatory_cb.csv", index=False)
i = d[d.status == "included"]
print("Outcome 1: MAE implied", np.abs(i.tau_pi - i.stated).mean().round(3), "MAE mean", np.abs(i.mean_infl - i.stated).mean().round(3), "n", len(i))
o = i[np.abs(i.mean_infl - i.stated) > 0.5]
closer = (np.abs(o.tau_pi - o.stated) < np.abs(o.mean_infl - o.stated))
print("Outcome 2: n", len(o), "implied closer in", int(closer.sum()), "MAE implied", np.abs(o.tau_pi - o.stated).mean().round(3), "MAE mean", np.abs(o.mean_infl - o.stated).mean().round(3))
