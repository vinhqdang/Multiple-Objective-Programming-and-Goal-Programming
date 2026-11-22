"""MI-IGP (strict-optimality margin) on central banks, quarterly, inflation goal only (K=1), vs baselines."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, time, migp
from inverse_interval_gp_cb import WINDOWS, ZLB

def quarterly(cc):
    r = pd.read_csv("data/central_banks/policy_rate_monthly.csv.gz"); c = pd.read_csv("data/central_banks/cpi_yoy_monthly.csv.gz")
    r = r[r.area == cc].set_index("period").policy_rate; c = c[c.area == cc].set_index("period").cpi_yoy
    df = pd.concat([r, c], axis=1).dropna(); df.index = pd.PeriodIndex(df.index, freq="M")
    q = df.groupby(df.index.asfreq("Q")).last()                 # end-of-quarter values
    q["D"] = q.policy_rate.diff()                                # decision during the quarter
    q["x"] = q.cpi_yoy.shift(1)                                  # inflation known at the start of the quarter
    q["rate_start"] = q.policy_rate.shift(1)
    return q.dropna()

rows = []
for cc, s, e, tgt, note in WINDOWS:
    q = quarterly(cc); q = q[(q.index >= pd.Period(s, "M").asfreq("Q")) & (q.index <= pd.Period(e, "M").asfreq("Q")) & (q.rate_start > ZLB)]
    X = q[["x"]].values; D = q.D.values
    t0 = time.time(); f = migp.fit_strict(X, D, time_limit=150); sec = time.time() - t0
    A = np.column_stack([np.ones(len(D)), X[:, 0]]); a, phi = np.linalg.lstsq(A, D, rcond=None)[0]   # difference Taylor rule
    taylor = -a / phi if phi > 0 else np.nan
    rows.append(dict(country=cc, stated=tgt, n=len(D), migp_tau=round(f["tau"][0], 2), migp_b=round(f["b"][0], 2),
                     migp_alpha=round(f["alpha"][0], 2), status=f["status"], loss=round(f["loss"], 3),
                     mean_infl=round(X[:, 0].mean(), 2), taylor_tau=round(taylor, 2), taylor_phi=round(phi, 2), seconds=round(sec)))
    print(rows[-1], flush=True)
d = pd.DataFrame(rows); d.to_csv("results/real_cb_migp.csv", index=False)
for m in ["migp_tau", "mean_infl", "taylor_tau"]:
    v = d[m]; ok = v.notna()
    print(f"{m}: MAE {np.abs(v[ok] - d.stated[ok]).mean():.2f} (n={ok.sum()}), corr {np.corrcoef(v[ok], d.stated[ok])[0,1]:.2f}")
