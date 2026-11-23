"""Aid application with the exact one-goal estimator (alpha = 1, direct control) and near-optimal tau sets."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, exact_k1 as X
from applications_gp import panel
a = pd.read_csv("data/aid/dac1_donor_oda_gni.csv.gz")
a = a[((a.measure.astype(str) == "2") & (a.year <= 2017)) | ((a.measure.astype(str) == "11002") & (a.year >= 2018))]
a = a[a.unit == "PT_B5G"].groupby(["donor", "year"], as_index=False).value.first()
p = panel(a, "donor", "value"); p = p[p.year != 2018]
meta = pd.read_csv("data/aid/worldbank_country_meta.csv.gz")
iso = set(meta[(meta.region != "Aggregates") & (meta.income_group != "Aggregates")].iso3)
rows = []
for donor, g in p[p.donor.isin(iso)].groupby("donor"):
    if len(g) < 30: continue
    x, D = g.x.values, -g.delta.values
    s = X.solve_fixed_alpha(x, D, 1.0); lo2, hi2, _ = X.tau_set(x, D, 1.0, 0.02); lo5, hi5, _ = X.tau_set(x, D, 1.0, 0.05)
    rows.append(dict(donor=donor, n=len(x), loss=round(s["loss"], 5), tau=round(s["tau"], 3), b=round(s["b"], 3),
                     band_lo=round(s["tau"] - s["b"], 3), band_hi=round(s["tau"] + s["b"], 3),
                     step_cut=round(s["om_p"], 3), step_raise=round(s["om_m"], 3), tau_set2=f"[{lo2:.2f}, {hi2:.2f}]",
                     tau_set5=f"[{lo5:.2f}, {hi5:.2f}]", mean_level=round(x.mean(), 3)))
    print(rows[-1], flush=True)
pd.DataFrame(rows).to_csv("results/aid_exact.csv", index=False)
