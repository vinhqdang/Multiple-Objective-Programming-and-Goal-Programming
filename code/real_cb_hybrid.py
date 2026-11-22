"""Hybrid MI-IGP on central banks (K=2: inflation 4 quarters ahead, GDP growth gap), quarterly.
(i) Full-window fit: implied inflation target vs stated target, against mean inflation and a difference Taylor rule.
(ii) Out-of-sample decisions: fit on the first 70% of quarters, predict rate changes in the last 30%;
     compare with a difference Taylor rule and with 'always hold'. Specification fixed before results."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, time, migp
from inverse_interval_gp_cb import WINDOWS, ZLB
from real_cb_migp_k2 import build

def taylor_fit(X, D):
    A = np.column_stack([np.ones(len(D)), X]); return np.linalg.lstsq(A, D, rcond=None)[0]

rows = []
for cc, s, e, tgt, note in WINDOWS:
    q = build(cc); q = q[(q.index >= pd.Period(s, "M").asfreq("Q")) & (q.index <= pd.Period(e, "M").asfreq("Q")) & (q.rate_start > ZLB)]
    q["x_gap"] = q.growth - q.growth.mean(); X = q[["x_pi", "x_gap"]].values; D = q.D.values; T = len(D)
    best = None
    for seed in range(3):                                         # restarts
        h = migp.fit_hybrid(X, D, seed=seed)
        if best is None or h["loss"] < best["loss"]: best = h
    a, phi, gam = taylor_fit(X, D)
    cut = int(0.7 * T); Xtr, Dtr, Xte, Dte = X[:cut], D[:cut], X[cut:], D[cut:]
    htr = None
    for seed in range(3):
        h = migp.fit_hybrid(Xtr, Dtr, seed=seed)
        if htr is None or h["loss"] < htr["loss"]: htr = h
    pred = migp.forward_batch(Xte, htr["alpha"], htr["tau"], htr["b"], htr["omega_p"], htr["omega_m"])
    ta = taylor_fit(Xtr, Dtr); pt = ta[0] + Xte @ ta[1:]
    rows.append(dict(country=cc, stated=tgt, n=T, tau_pi=round(best["tau"][0], 2), b_pi=round(best["b"][0], 2), alpha_pi=round(best["alpha"][0], 2),
                     tau_gap=round(best["tau"][1], 2), loss=round(best["loss"], 3), mean_infl=round(X[:, 0].mean(), 2),
                     taylor_tau=round(-a / phi, 2) if phi > 0 else np.nan,
                     oos_mae_gp=round(np.abs(Dte - pred).mean(), 3), oos_mae_taylor=round(np.abs(Dte - pt).mean(), 3),
                     oos_mae_hold=round(np.abs(Dte).mean(), 3),
                     oos_dir_gp=round((np.sign(np.round(pred, 2)) == np.sign(np.round(Dte, 2))).mean(), 2),
                     oos_dir_taylor=round((np.sign(np.round(pt, 2)) == np.sign(np.round(Dte, 2))).mean(), 2)))
    print(rows[-1], flush=True)
d = pd.DataFrame(rows); d.to_csv("results/real_cb_hybrid.csv", index=False)
for m in ["tau_pi", "mean_infl", "taylor_tau"]:
    v = d[m]; ok = v.notna(); print(f"{m}: MAE {np.abs(v[ok]-d.stated[ok]).mean():.2f} (n={ok.sum()}), corr {np.corrcoef(v[ok], d.stated[ok])[0,1]:.2f}")
print("out-of-sample MAE of decisions: GP", d.oos_mae_gp.mean().round(3), "Taylor", d.oos_mae_taylor.mean().round(3), "hold", d.oos_mae_hold.mean().round(3))
print("out-of-sample direction accuracy: GP", d.oos_dir_gp.mean().round(2), "Taylor", d.oos_dir_taylor.mean().round(2))
