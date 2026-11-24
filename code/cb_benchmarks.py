"""Benchmarks for the implied inflation target (after review): (i) average inflation; (ii) a constant 2.5%;
(iii) the median stated target of the other banks in the same sample; (iv) the target implied by a difference
Taylor rule, Delta i = a + b_pi pi + b_y gap, fitted by least absolute deviations on the same window, with
implied target -a/b_pi (the gap has mean zero); undefined when b_pi <= 0. Writes results/cb_benchmarks.csv."""
import sys, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from scipy.optimize import linprog
from bootstrap_cb import data, CONF
from inverse_interval_gp_cb import WINDOWS

def lad(Z, y):
    n, k = Z.shape; c = np.r_[np.zeros(k), np.ones(2 * n)]
    A = np.column_stack([Z, np.eye(n), -np.eye(n)])
    r = linprog(c, A_eq=A, b_eq=y, bounds=[(None, None)] * k + [(0, None)] * (2 * n), method="highs"); return r.x[:k]

ex = pd.read_csv("results/real_cb_quad.csv"); ex = ex[ex.input == "realised"]
cf = pd.read_csv("results/confirmatory_cb.csv"); cf = cf[cf.status == "included"]
rows = []
for sample, lst in [("exploratory", [(cc, pd.Period(s, "M").asfreq("Q"), pd.Period(e, "M").asfreq("Q"), t) for cc, s, e, t, _ in WINDOWS]),
                    ("confirmatory", [(cc, pd.Period(s, "Q"), pd.Period(e, "Q"), t) for cc, s, e, t in CONF])]:
    for cc, q0, q1, tgt in lst:
        X, D = data(cc, q0, q1); a, bp, by = lad(np.column_stack([np.ones(len(D)), X]), D)
        imp = (ex[ex.country == cc].tau_pi.values if sample == "exploratory" else cf[cf.country == cc].tau_pi.values)[0]
        rows.append(dict(sample=sample, country=cc, stated=tgt, implied=imp, mean_infl=X[:, 0].mean(),
                         taylor=(-a / bp) if bp > 1e-6 else np.nan, b_pi=bp))
d = pd.DataFrame(rows)
for s in d["sample"].unique():
    m = d["sample"] == s; d.loc[m, "median_other"] = [d.loc[m & (d.country != c), "stated"].median() for c in d.loc[m, "country"]]
d["const25"] = 2.5
d.to_csv("results/cb_benchmarks.csv", index=False)
E = lambda z, col: np.abs(z[col] - z.stated)
for lab, z in [("exploratory", d[d["sample"] == "exploratory"]), ("confirmatory", d[d["sample"] == "confirmatory"]),
               ("confirmatory excl. TR", d[(d["sample"] == "confirmatory") & (d.country != "TR")]),
               ("all 14", d), ("all excl. TR", d[d.country != "TR"])]:
    tz = z.dropna(subset=["taylor"])
    print(f"{lab:24s} n={len(z):2d} implied {E(z,'implied').mean():.2f} mean {E(z,'mean_infl').mean():.2f} const2.5 {E(z,'const25').mean():.2f} "
          f"median-other {E(z,'median_other').mean():.2f} | Taylor defined n={len(tz)}: taylor {E(tz,'taylor').mean():.2f} implied {E(tz,'implied').mean():.2f}")
print(d.round(2).to_string(index=False))
