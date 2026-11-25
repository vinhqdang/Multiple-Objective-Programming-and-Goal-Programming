"""Consistency Monte Carlo for the exact one-goal estimator (alpha = 1, Laplace decision noise), under three designs.
Same true parameters, estimator (exact_k1.solve_fixed_alpha), sample sizes and error metrics as consistency_mc.py.
  exo  : exogenous AR(1) state (as in consistency_mc.py), D_t = D*(x_t) + Laplace(0, 0.1)
  ctrl : controlled state x_{t+1} = x_t - D_t + u_t, u_t = 0.5 u_{t-1} + N(0, 0.3), D_t = D*(x_t) + Laplace(0, 0.1)
         (sign: D > 0 reduces the goal variable, as in exact_k1.h; the shock scale 0.3 keeps the state stable and
         visits both outer regimes, x < 1.5 and x > 2.5, in roughly 30% and 24% of periods)
  disc : exogenous state as in consistency_mc.py, observed decision rounded to a 0.25 grid (25 bp moves); the latent
         Laplace scale is proportional to the grid (0.4 * 0.25 = 0.1, the scale used in consistency_mc.py)
  both : controlled state (ctrl) with the rounded decision (disc); the state moves by the observed, rounded decision.
Output: one row per replication with the estimates, absolute errors, the within-0.1 indicator for tau, and the share
of periods in the lower (x < 1.5) and upper (x > 2.5) outer regimes."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, exact_k1 as X
from multiprocessing import Pool
TRUE = dict(tau=2.0, b=0.5, om_p=0.4, om_m=0.3)
EP, EM = TRUE["tau"] + TRUE["b"], TRUE["tau"] - TRUE["b"]
DESIGNS = ("exo", "ctrl", "disc", "both")
GRID, NOISE, CTRL_SD, REPS, TS = 0.25, 0.1, 0.3, 100, (50, 100, 200)

def h1(s):
    return X.h(np.array([s]), 1.0, EP, EM, TRUE["om_p"], TRUE["om_m"])[0]

def one(args):
    design, T, rep = args
    rng = np.random.default_rng(1_000_000 * DESIGNS.index(design) + 10_000 * T + rep)
    x = np.empty(T); D = np.empty(T)
    if design in ("exo", "disc"):
        s = 2.0
        for t in range(T):
            s = 2.0 + 0.7 * (s - 2.0) + rng.normal(0, 0.9); x[t] = s
            D[t] = h1(s) + rng.laplace(0, NOISE)
    else:  # controlled state
        s, u = 2.0, 0.0
        for t in range(T):
            x[t] = s
            D[t] = h1(s) + rng.laplace(0, NOISE)
            if design == "both": D[t] = np.round(D[t] / GRID) * GRID
            u = 0.5 * u + rng.normal(0, CTRL_SD)
            s = s - D[t] + u
    if design in ("disc", "both"):
        D = np.round(D / GRID) * GRID
    r = X.solve_fixed_alpha(x, D, 1.0)
    row = dict(design=design, T=T, rep=rep, tau=r["tau"], b=r["b"], om_p=r["om_p"], om_m=r["om_m"],
               share_lo=(x < 1.5).mean(), share_hi=(x > 2.5).mean())
    for k, v in TRUE.items(): row[k + "_err"] = abs(row[k] - v)
    row["tau_within_0.1"] = abs(row["tau"] - TRUE["tau"]) <= 0.1 + 1e-12
    return row

if __name__ == "__main__":
    import time; t0 = time.time()
    jobs = [(d, T, r) for d in DESIGNS for T in TS for r in range(REPS)]
    with Pool(2) as p: out = pd.DataFrame(p.map(one, jobs, chunksize=4))
    out.to_csv("results/consistency_mc_closed.csv", index=False)
    g = out.groupby(["design", "T"])
    s = pd.DataFrame({k + "_mae": g[k + "_err"].mean() for k in TRUE})
    s["share_tau_within_0.1"] = g["tau_within_0.1"].mean(); s["n"] = g.size()
    s["share_lo"] = g.share_lo.mean(); s["share_hi"] = g.share_hi.mean()
    print(s.round(4).to_string())
    print(f"elapsed {time.time() - t0:.1f} s")
