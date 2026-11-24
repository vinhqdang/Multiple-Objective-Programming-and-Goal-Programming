"""Summarise the 100-replicate moving-block bootstrap of the central-bank fits (results/bootstrap_cb_100_reps.csv).
Replicates with alpha at its lower bound (0.05) are degenerate: tau = c/alpha is then unbounded. Quantiles of tau
are taken over the non-degenerate replicates; the number of degenerate replicates is reported separately.
Writes results/bootstrap_cb_100_summary.csv."""
import pandas as pd, numpy as np
ALPHA_MIN = 0.05
STATED = dict(AU=2.5, CA=2.0, CL=3.0, CO=3.0, GB=2.0, HU=3.0, IL=2.0, IN=4.0, MX=3.0, NO=2.5, NZ=2.0, PL=2.5, SE=2.0, TR=5.0)
d = pd.read_csv("results/bootstrap_cb_100_reps.csv", header=None, names=["cc", "b", "tau", "alpha", "e_minus", "e_plus", "loss"])
rows = []
for cc, z in d.groupby("cc"):
    ok = z[z.alpha > ALPHA_MIN * 1.002]
    lo, med, hi = ok.tau.quantile([0.05, 0.5, 0.95])
    s = STATED[cc]
    rows.append(dict(country=cc, lo=lo, med=med, hi=hi, stated=s, covers_stated=lo <= s <= hi, width=hi - lo,
                     n_rep=len(z), n_degenerate=len(z) - len(ok)))
pd.DataFrame(rows).to_csv("results/bootstrap_cb_100_summary.csv", index=False)
print(pd.DataFrame(rows).round(2).to_string(index=False))
