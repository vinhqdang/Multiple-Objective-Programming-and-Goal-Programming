"""Computational study for the one-goal case: runtime of the exact algorithm versus T, and the optimality gap of
the multistart heuristic (migp_quad.fit_ms, 200 starts) relative to the exact optimum, on synthetic instances.
Parameters drawn at random; alpha = 1 (direct control); Laplace noise 0.1."""
import sys, time, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, exact_k1 as X, migp_quad as Q

def instance(T, rng):
    tau, b, op, om = rng.uniform(1, 3), rng.uniform(0.1, 0.8), rng.uniform(0.1, 0.6), rng.uniform(0.1, 0.6)
    x = np.empty(T); s = tau
    for t in range(T): s = tau + 0.7 * (s - tau) + rng.normal(0, 1.0); x[t] = s
    D = X.h(x, 1.0, tau + b, tau - b, op, om) + rng.laplace(0, 0.1, T)
    return x, D

rows = []
for T in (25, 50, 100, 200):
    for i in range(10):
        rng = np.random.default_rng(1000 * T + i); x, D = instance(T, rng)
        t0 = time.time(); ex = X.solve_fixed_alpha(x, D, 1.0); t_ex = time.time() - t0
        row = dict(T=T, inst=i, exact_loss=ex["loss"], exact_sec=t_ex)
        if T <= 100:
            span = np.abs(D).max()
            lo = np.array([0.9999, x.min(), 0, 0, 0]); hi = np.array([1.0001, x.max(), (x.max() - x.min()) / 2, 2 * span, 2 * span])
            t0 = time.time(); hh = Q.fit_ms(x[:, None], D, n_starts=200, top=3, lo=lo, hi=hi, lns_iters=5, alpha_bounds=(0.9999, 1.0001))
            row.update(heur_loss=hh["loss"], heur_sec=time.time() - t0, gap_pct=100 * (hh["loss"] - ex["loss"]) / ex["loss"])
        rows.append(row); print(row, flush=True)
pd.DataFrame(rows).to_csv("results/comp_study.csv", index=False)
