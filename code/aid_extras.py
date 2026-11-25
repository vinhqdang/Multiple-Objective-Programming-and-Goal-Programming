"""Additional aid analyses after the second review.
(1) Heuristic vs exact: the multistart fits in results/applications_gp_aid_defence_firms.csv against the exact fits in
    results/aid_exact.csv -> results/aid_heuristic_vs_exact.csv.
(2) GNI-growth drift: the state x_t = ODA_{t-1}/GNI_{t-1} moves mechanically when GNI grows. Alternative state
    x'_t = ODA_{t-1}/GNI_t = share_{t-1} * GNI_{t-1}/GNI_t, decision share_t - x'_t. GNI in national currency is
    recovered as ODA (national currency, current prices) / share; net ODA (flow 1140) to 2017, grant equivalent
    (flow 1160) from 2018; the 2017-2018 change is dropped as in the main analysis. Years with ODA below 5 million
    units of national currency are dropped (rounding makes the implied GNI unreliable).
    Refit with the exact estimator -> results/aid_gni_drift.csv.
(3) Near-optimal tau sets (2%) restricted to tau >= 0, and target minus mean level -> results/aid_sets_truncated.csv."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, exact_k1 as X
import aid_profile as A

def heuristic_vs_exact():
    h = pd.read_csv("results/applications_gp_aid_defence_firms.csv")
    h = h[h.domain == "ODA % GNI"][["unit", "loss", "tau"]].rename(columns={"unit": "donor"})
    e = pd.read_csv("results/aid_exact.csv")[["donor", "loss", "tau"]]
    m = h.merge(e, on="donor", suffixes=("_heur", "_exact")); m["rel_gap"] = m.loss_heur / m.loss_exact - 1
    m.to_csv("results/aid_heuristic_vs_exact.csv", index=False)
    print("heuristic within 0.1% of exact:", (m.rel_gap < 1e-3).sum(), "of", len(m), "; max gap", round(m.rel_gap.max(), 4))

def gni_drift():
    a = pd.read_csv("data/aid/dac1_donor_oda_gni.csv.gz")
    sh = a[((a.measure.astype(str) == "2") & (a.year <= 2017)) | ((a.measure.astype(str) == "11002") & (a.year >= 2018))]
    sh = sh[sh.unit == "PT_B5G"].groupby(["donor", "year"]).value.first().rename("share")
    od = a[(a.unit == "XDC") & (a.price_base == "V") & (((a.measure.astype(str) == "1010") & (a.flow_type == 1140) & (a.year <= 2017)) |
            ((a.measure.astype(str) == "11010") & (a.flow_type == 1160) & (a.year >= 2018)))]
    od = od.groupby(["donor", "year"]).value.first().rename("oda")
    d = pd.concat([sh, od], axis=1).dropna().reset_index().sort_values(["donor", "year"])
    d = d[d.oda >= 5]   # values are rounded to 0.01 million; very small early amounts give unreliable GNI
    d["gni"] = d.oda / (d.share / 100)
    d["share_prev"] = d.groupby("donor").share.shift(1); d["gni_prev"] = d.groupby("donor").gni.shift(1)
    d["ygap"] = d.year - d.groupby("donor").year.shift(1)
    d = d[(d.ygap == 1) & (d.year != 2018)].dropna()
    d["growth"] = d.gni / d.gni_prev
    rows = []
    base = pd.read_csv("results/aid_exact.csv").set_index("donor")
    for donor in A.data().keys():
        g = d[d.donor == donor]
        if len(g) < 30: continue
        x = (g.share_prev / g.growth).values; delta = g.share.values - x
        s = X.solve_fixed_alpha(x, -delta, 1.0); lo, hi, _ = X.tau_set(x, -delta, 1.0, 0.02)
        rows.append(dict(donor=donor, n=len(g), tau=s["tau"], band_lo=s["tau"] - s["b"], band_hi=s["tau"] + s["b"],
                         set_lo=lo, set_hi=hi, tau_base=base.loc[donor, "tau"], max_growth=g.growth.max(), min_growth=g.growth.min()))
    r = pd.DataFrame(rows); r.to_csv("results/aid_gni_drift.csv", index=False)
    print(r.round(3).to_string(index=False))
    print("median |tau - tau_base|:", round((r.tau - r.tau_base).abs().median(), 3), "max:", round((r.tau - r.tau_base).abs().max(), 3))

def truncated():
    e = pd.read_csv("results/aid_exact.csv")
    def tr(s):
        lo, hi = [float(v) for v in s.strip("[]").split(",")]; return max(lo, 0.0), hi
    e["set2_lo"], e["set2_hi"] = zip(*e.set2.map(tr))
    e["tau_minus_mean"] = e.tau - e.mean_level
    e[["donor", "tau", "mean_level", "tau_minus_mean", "set2_lo", "set2_hi"]].to_csv("results/aid_sets_truncated.csv", index=False)
    print(e[["donor", "tau", "mean_level", "tau_minus_mean", "set2_lo", "set2_hi"]].round(3).to_string(index=False))

if __name__ == "__main__":
    heuristic_vs_exact(); gni_drift(); truncated()
