"""Exact near-optimal tau sets for the aid application from the exact profile loss (grid spacing 0.01)."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, exact_k1 as X
from multiprocessing import Pool
from applications_gp import panel

def data():
    a = pd.read_csv("data/aid/dac1_donor_oda_gni.csv.gz")
    a = a[((a.measure.astype(str) == "2") & (a.year <= 2017)) | ((a.measure.astype(str) == "11002") & (a.year >= 2018))]
    a = a[a.unit == "PT_B5G"].groupby(["donor", "year"], as_index=False).value.first()
    p = panel(a, "donor", "value"); p = p[p.year != 2018]
    meta = pd.read_csv("data/aid/worldbank_country_meta.csv.gz")
    iso = set(meta[(meta.region != "Aggregates") & (meta.income_group != "Aggregates")].iso3)
    return {d: g for d, g in p[p.donor.isin(iso)].groupby("donor") if len(g) >= 30}

def run(item):
    donor, g = item; x, D = g.x.values, -g.delta.values
    taus = np.arange(round(x.min() - 0.3, 2), round(x.max() + 0.3, 2) + 1e-9, 0.01)
    prof = X.profile_tau(x, D, 1.0, taus); best = prof.min()
    out = dict(donor=donor, best=best)
    for rel in (0.02, 0.05):
        ok = taus[prof <= best * (1 + rel) + 1e-12]
        out[f"set{int(rel*100)}"] = f"[{ok.min():.2f}, {ok.max():.2f}]"
        out[f"contig{int(rel*100)}"] = bool(len(ok) == int(round((ok.max() - ok.min()) / 0.01)) + 1)
    return out

if __name__ == "__main__":
    with Pool(4) as p: rows = p.map(run, list(data().items()), chunksize=1)
    d = pd.DataFrame(rows); old = pd.read_csv("results/aid_exact.csv")
    m = old.merge(d, on="donor"); m.to_csv("results/aid_exact.csv", index=False)
    print(m[["donor", "tau", "tau_set2", "set2", "contig2", "tau_set5", "set5", "contig5", "loss", "best"]].to_string(index=False))
