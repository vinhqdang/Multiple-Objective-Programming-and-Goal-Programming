"""Parametric bootstrap test of the interval goal program against linear partial adjustment (aid donors).
Null hypothesis: decisions follow linear partial adjustment, Delta_t = a + b x_t + e_t, with e_t i.i.d.
(estimated by least absolute deviations; residuals resampled). Under the null the level path is rebuilt as
x_{t+1} = x_t + Delta_t, keeping the non-decision jump at the 2018 definitional break.
Statistic: S = L_PA / L_GP, the ratio of in-sample mean absolute decision errors of the LAD partial-adjustment
fit and the exact goal-program fit. Large S means the goal-program shape (dead zone, saturation) fits better than a
linear rule by more than it would if partial adjustment were true. p = (1 + #{S* >= S}) / (B + 1), B = 199."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, exact_k1 as X
from multiprocessing import Pool
from misspec_placebo import lad
from permutation_test import rebuild
B = 199

def stat(x, d):
    a, b = lad(x, d); lpa = np.abs(d - a - b * x).mean()
    lgp = X.solve_fixed_alpha(x, -d, 1.0)["loss"]
    return lpa / max(lgp, 1e-12), a, b

def simulate(x1, a, b, res, jumps, rng):
    T = len(res); x = np.empty(T); d = np.empty(T); x[0] = x1; e = rng.choice(res, T, replace=True)
    for t in range(T):
        d[t] = a + b * x[t] + e[t]
        if t + 1 < T: x[t + 1] = x[t] + d[t] + jumps[t]
    return x, d

def job(item):
    donor, x, d = item
    s0, a, b = stat(x, d); res = d - a - b * x
    jumps = np.append(x[1:] - x[:-1] - d[:-1], 0.0)
    rng = np.random.default_rng(11); null = np.empty(B)
    for i in range(B):
        xs, ds = simulate(x[0], a, b, res, jumps, rng); null[i] = stat(xs, ds)[0]
    return dict(unit=donor, n=len(x), S=s0, null95=np.percentile(null, 95), p=(1 + (null >= s0).sum()) / (B + 1), a=a, b=b)

if __name__ == "__main__":
    import aid_profile as A
    items = [(k, g.x.values, g.delta.values) for k, g in A.data().items()]
    with Pool(2) as pool: rows = pool.map(job, items, chunksize=1)
    d = pd.DataFrame(rows).sort_values("p"); d.to_csv("results/pa_null_test.csv", index=False)
    print(d.round(3).to_string(index=False))
