"""Paired tests of out-of-sample decision errors across units (results/model_comparison.csv): for aid donors and
central banks, the goal program (GP) against partial adjustment / Taylor rule (PA), always holding and the median
change. Exact two-sided sign test on the number of units where GP has the lower error (ties dropped) and the
Wilcoxon signed-rank test on the paired differences. Writes results/paired_tests.csv."""
import pandas as pd, numpy as np
from scipy.stats import binomtest, wilcoxon
m = pd.read_csv("results/model_comparison.csv"); rows = []
for dom in ("aid", "central bank"):
    g = m[m.domain == dom]
    for other in ("pa", "hold", "medchg"):
        d = (g.gp - g[other]).values; nz = d[np.abs(d) > 1e-12]
        wins = int((nz < 0).sum()); n = len(nz)
        rows.append(dict(domain=dom, versus=other, units=len(d), gp_better=wins, nonties=n,
                         sign_p=binomtest(wins, n, 0.5).pvalue if n else np.nan,
                         wilcoxon_p=wilcoxon(nz).pvalue if n > 5 else np.nan, median_diff=np.median(d)))
r = pd.DataFrame(rows); r.to_csv("results/paired_tests.csv", index=False); print(r.round(3).to_string(index=False))
