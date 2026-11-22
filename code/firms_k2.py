"""Two-goal gradualism model for firms: decision = change in book leverage; goals = leverage (moved one-for-one)
and cash-to-assets (transmission estimated: alpha_cash = 1/theta where a leverage increase of 1 raises the cash
ratio by theta). Compared with the one-goal fit on the same sample by decision loss."""
import sys, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, migp_quad as Q
from applications_gp import panel

f = pd.read_csv("data/sec/firm_year_panel.csv.gz")
f = f[(f.assets > 1e7) & f.equity.notna() & f.cash.notna()].copy()
f["lev"] = 1 - f.equity / f.assets; f["cashr"] = f.cash / f.assets
f = f[(f.lev > 0) & (f.lev < 1) & (f.cashr >= 0) & (f.cashr < 1)]
f["year"] = f.period.astype(str).str[:4].astype(int); f["sic2"] = pd.to_numeric(f.sic, errors="coerce") // 100
f = f.dropna(subset=["sic2"]).drop_duplicates(["cik", "year"], keep="last").sort_values(["cik", "year"])
f["prev_cash"] = f.groupby("cik").cashr.shift(1)
p = panel(f, "cik", "lev").dropna(subset=["prev_cash"])
rows = []
for sic2 in (28, 36, 73):
    g = p[p.sic2 == sic2].sample(n=2000, random_state=0)
    X = np.column_stack([g.x.values, g.prev_cash.values]); D = -(g.delta.values); span = np.abs(D).max()
    lo = np.array([0.9999, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    hi = np.array([1.0001, 5.0, 1.0, 0.8, 0.5, 0.4, 2 * span, 2 * span, 2 * span, 2 * span])
    h2 = Q.fit_ms(X, D, n_starts=200, top=3, lo=lo, hi=hi, lns_iters=5, alpha_bounds=(0.05, 5.0))
    h1 = Q.fit_ms(X[:, :1], D, n_starts=200, top=3, lo=lo[[0, 2, 4, 6, 8]], hi=hi[[0, 2, 4, 6, 8]], lns_iters=5, alpha_bounds=(0.9999, 1.0001))
    r = dict(sic2=sic2, n=len(D), loss_k1=round(h1["loss"], 4), loss_k2=round(h2["loss"], 4), loss_hold=round(np.abs(D).mean(), 4),
             tau_lev=round(h2["tau"][0], 3), b_lev=round(h2["b"][0], 3), tau_cash=round(h2["tau"][1], 3), b_cash=round(h2["b"][1], 3),
             alpha_cash=round(h2["alpha"][1], 3), om_p=np.round(h2["omega_p"], 3).tolist(), om_m=np.round(h2["omega_m"], 3).tolist(),
             median_lev=round(g.x.median(), 3), median_cash=round(g.prev_cash.median(), 3))
    rows.append(r); print(r, flush=True)
pd.DataFrame(rows).to_csv("results/firms_k2.csv", index=False)
