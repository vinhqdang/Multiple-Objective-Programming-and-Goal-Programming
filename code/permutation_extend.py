"""Extensions of the permutation test after review.
(1) Aid donors with B = 999 permutations, raw and Benjamini-Hochberg adjusted p-values.
(2) Size under persistent but state-independent decisions, for which the permutation null (exchangeable decisions)
    is false although there is no goal: (a) AR(1) decisions, d_t = 0.7 d_{t-1} + e_t; (b) regime-switching drift,
    d_t = m_t + e_t with m_t in {-0.02, +0.02} switching with probability 0.1 per year. 100 series each, T = 60,
    B = 199; the level path is rebuilt from the decisions. Writes results/permutation_extend.csv."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd
from multiprocessing import Pool
import permutation_test as P

def bh(p):
    p = np.asarray(p); m = len(p); o = np.argsort(p); q = p[o] * m / np.arange(1, m + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]; out = np.empty(m); out[o] = np.minimum(q, 1); return out

def aid_job(item):
    donor, x, d = item; P.B = 999
    g0, p, q95 = P.ptest(x, d, 7); return dict(domain="aid", unit=donor, n=len(x), gain=g0, null95=q95, p=p)

def size_job(args):
    kind, rep = args; P.B = 199; rng = np.random.default_rng(70_000 + 1000 * (kind == "regime") + rep); T = 60
    e = rng.normal(0, 0.03, T); d = np.empty(T)
    if kind == "ar1":
        d[0] = e[0]
        for t in range(1, T): d[t] = 0.7 * d[t - 1] + e[t]
    else:
        m = 0.02 * rng.choice([-1, 1])
        for t in range(T):
            if rng.random() < 0.1: m = -m
            d[t] = m + e[t]
    x = P.rebuild(0.4, d); g0, p, q95 = P.ptest(x, d, 80_000 + rep)
    return dict(domain="size_" + kind, unit=rep, n=T, gain=g0, null95=q95, p=p)

if __name__ == "__main__":
    import aid_profile as A
    items = [(k, g.x.values, g.delta.values) for k, g in A.data().items()]
    with Pool(2) as pool:
        rows = pool.map(aid_job, items, chunksize=1)
        rows += pool.map(size_job, [(k, r) for k in ("ar1", "regime") for r in range(100)], chunksize=2)
    d = pd.DataFrame(rows); a = d.domain == "aid"; d.loc[a, "p_bh"] = bh(d.loc[a, "p"])
    d.to_csv("results/permutation_extend.csv", index=False)
    print(d[a].sort_values("p").round(3).to_string(index=False))
    for k in ("size_ar1", "size_regime"):
        z = d[d.domain == k]; print(k, "rejection at 5%:", (z.p <= .05).mean(), "at 10%:", (z.p <= .10).mean())
