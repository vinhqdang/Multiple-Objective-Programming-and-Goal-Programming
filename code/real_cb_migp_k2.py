"""MI-IGP (strict margin) on central banks, quarterly, K=2: inflation 4 quarters ahead (realised, proxy for the
forecast) and the GDP growth gap (y/y growth minus its window mean). Specification fixed before seeing results."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, time, migp
from inverse_interval_gp_cb import WINDOWS, ZLB
ISO3 = {"GB": "GBR", "CA": "CAN", "NO": "NOR", "SE": "SWE", "AU": "AUS", "MX": "MEX", "CL": "CHL", "IN": "IND", "PL": "POL"}
r_all = pd.read_csv("data/central_banks/policy_rate_monthly.csv.gz"); c_all = pd.read_csv("data/central_banks/cpi_yoy_monthly.csv.gz")
g_all = pd.read_csv("data/central_banks/gdp_growth_yoy_quarterly.csv.gz")

def build(cc):
    r = r_all[r_all.area == cc].set_index("period").policy_rate; c = c_all[c_all.area == cc].set_index("period").cpi_yoy
    df = pd.concat([r, c], axis=1).dropna(); df.index = pd.PeriodIndex(df.index, freq="M")
    q = df.groupby(df.index.asfreq("Q")).last()
    q["D"] = q.policy_rate.diff(); q["rate_start"] = q.policy_rate.shift(1)
    q["x_pi"] = q.cpi_yoy.shift(-3)                       # inflation at the end of quarter t+3 (4 quarters after decision start)
    g = g_all[g_all.area_iso3 == ISO3[cc]].copy(); g.index = pd.PeriodIndex(g.period.str.replace("-", ""), freq="Q")
    q["growth"] = g.gdp_growth_yoy
    return q.dropna()

rows = []
for cc, s, e, tgt, note in WINDOWS:
    q = build(cc); q = q[(q.index >= pd.Period(s, "M").asfreq("Q")) & (q.index <= pd.Period(e, "M").asfreq("Q")) & (q.rate_start > ZLB)]
    q["x_gap"] = q.growth - q.growth.mean()
    X = q[["x_pi", "x_gap"]].values; D = q.D.values
    t0 = time.time(); f = migp.fit_strict(X, D, time_limit=300); sec = time.time() - t0
    A = np.column_stack([np.ones(len(D)), X]); a, phi, gam = np.linalg.lstsq(A, D, rcond=None)[0]
    rows.append(dict(country=cc, stated=tgt, n=len(D), migp_tau_pi=round(f["tau"][0], 2), migp_b_pi=round(f["b"][0], 2),
                     migp_alpha_pi=round(f["alpha"][0], 2), migp_tau_gap=round(f["tau"][1], 2), migp_alpha_gap=round(f["alpha"][1], 2),
                     status=f["status"], loss=round(f["loss"], 3), mean_infl=round(X[:, 0].mean(), 2),
                     taylor_tau=round(-a / phi, 2) if phi > 0 else np.nan, taylor_phi=round(phi, 2), taylor_gamma=round(gam, 2), seconds=round(sec)))
    print(rows[-1], flush=True)
d = pd.DataFrame(rows); d.to_csv("results/real_cb_migp_k2.csv", index=False)
for m in ["migp_tau_pi", "mean_infl", "taylor_tau"]:
    v = d[m]; ok = v.notna()
    print(f"{m}: MAE {np.abs(v[ok] - d.stated[ok]).mean():.2f} (n={ok.sum()}), corr {np.corrcoef(v[ok], d.stated[ok])[0,1]:.2f}")
