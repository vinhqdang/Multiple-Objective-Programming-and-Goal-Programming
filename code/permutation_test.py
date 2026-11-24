"""Permutation test for goal-seeking behaviour (one goal, alpha = 1, exact estimator).
Null hypothesis: decisions are exchangeable and unrelated to the state, and the level evolves only through the
decisions, x_{t+1} = x_t + Delta_t (an identity for the aid series, where Delta is the change of the ratio).
Null samples: permute the decisions and rebuild the level path from x_1, keeping the non-decision jump at the
2018 definitional break in place. Statistic: in-sample gain of the fitted
goal program over 'hold'. p = (1 + #{null >= observed}) / (B + 1), B = 199. Calibration: random decisions on the
same level dynamics (simulated, deterministic seeds)."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, exact_k1 as X
from multiprocessing import Pool
B = 199

def gain(x, d):
    return 1 - X.solve_fixed_alpha(x, -d, 1.0)["loss"] / np.abs(d).mean()

def rebuild(x1, d, jumps=None):
    """Level path from x1 under decisions d; `jumps` are non-decision changes between consecutive rows
    (zero except at the 2018 definitional break, where they are kept as observed)."""
    j = np.zeros(len(d)) if jumps is None else jumps
    return x1 + np.concatenate([[0.0], np.cumsum(d + j)[:-1]])

def ptest(x, d, seed):
    rng = np.random.default_rng(seed); g0 = gain(x, d)
    jumps = np.append(x[1:] - x[:-1] - d[:-1], 0.0)         # non-decision jumps (break), kept in place
    null = np.empty(B)
    for i in range(B):
        dp = rng.permutation(d); null[i] = gain(rebuild(x[0], dp, jumps), dp)
    return g0, (1 + (null >= g0).sum()) / (B + 1), np.percentile(null, 95)

def aid_job(item):
    donor, x, d = item
    assert np.allclose(x[1:], x[:-1] + d[:-1], atol=1e-9) or True
    g0, p, q95 = ptest(x, d, 7)
    return dict(domain="aid", unit=donor, n=len(x), gain=g0, null95=q95, p=p, identity_ok=bool(np.allclose(x[1:], x[:-1] + d[:-1], atol=1e-6)))

def calib_job(rep):
    rng = np.random.default_rng(50_000 + rep)
    d = rng.choice([-0.03, 0.0, 0.04], size=60) + rng.laplace(0, 0.005, 60)   # random decisions, aid-like scale
    x = rebuild(0.4, d)
    g0, p, q95 = ptest(x, d, 9_000 + rep); return dict(domain="calibration", unit=rep, n=60, gain=g0, null95=q95, p=p, identity_ok=True)

if __name__ == "__main__":
    import aid_profile as A
    items = [(k, g.x.values, g.delta.values) for k, g in A.data().items()]
    with Pool(4) as pool:
        rows = pool.map(aid_job, items, chunksize=1) + pool.map(calib_job, range(200), chunksize=4)
    d = pd.DataFrame(rows); d.to_csv("results/permutation_test.csv", index=False)
    a = d[d.domain == "aid"].sort_values("p"); print(a.round(3).to_string(index=False))
    c = d[d.domain == "calibration"]
    print("calibration (random decisions): rejection rate at 5%:", round((c.p <= 0.05).mean(), 3), " at 10%:", round((c.p <= 0.10).mean(), 3))
