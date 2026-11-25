"""Summarise the moving-block bootstrap of the central-bank fits (results/bootstrap_cb_100_reps.csv; 500 replicates
per bank after the second revision). Replicates with alpha at its lower bound (0.05) are degenerate: tau = c/alpha
is then unbounded. Quantiles of tau are taken over ALL replicates, with each degenerate replicate set to +inf or
-inf according to the side of the bounded median on which its tau lies; an interval end that falls on a degenerate
replicate is reported as unbounded (inf). Writes results/bootstrap_cb_100_summary.csv."""
import pandas as pd, numpy as np
ALPHA_MIN = 0.05
STATED = dict(AU=2.5, CA=2.0, CL=3.0, CO=3.0, GB=2.0, HU=3.0, IL=2.0, IN=4.0, MX=3.0, NO=2.5, NZ=2.0, PL=2.5, SE=2.0, TR=5.0)
d = pd.read_csv("results/bootstrap_cb_100_reps.csv", header=None, names=["cc", "b", "tau", "alpha", "e_minus", "e_plus", "loss"])
d = d.drop_duplicates(["cc", "b"])
lp = pd.read_csv("results/cb_light_point.csv").set_index("country")
rows = []
for cc, z in d.groupby("cc"):
    deg = z.alpha <= ALPHA_MIN * 1.002
    m = z.tau[~deg].median() if (~deg).any() else 0.0
    t = z.tau.where(~deg, np.where(z.tau >= m, np.inf, -np.inf))
    lo, med, hi = np.quantile(t, [0.05, 0.5, 0.95], method="inverted_cdf")
    s = STATED[cc]
    rows.append(dict(country=cc, point_light=lp.tau.get(cc, np.nan), lo=lo, med=med, hi=hi, stated=s,
                     covers_stated=lo <= s <= hi, width=hi - lo, n_rep=len(z), n_degenerate=int(deg.sum())))
pd.DataFrame(rows).to_csv("results/bootstrap_cb_100_summary.csv", index=False)
print(pd.DataFrame(rows).round(2).to_string(index=False))
