"""Sensitivity of the exact MILPs to their constants, on the smallest synthetic instance (K = 2, T = 10, seed 2001,
decision noise 0.05; the same generator as milp_small.py).
(a) Quadratic cost (migp_quad._build): M in {20, 30, 50} at Omega = 5, and Omega in {3, 5, 10} at M = 30.
(b) Linear cost with strict-optimality margin (migp._build_strict): eps in {0.02, 0.05, 0.1} at M = 30, Omega = 5,
    delta = 1e-3, on T = 10 and T = 15 (seed 2001). Data for (b) are generated with migp.forward_batch at the same
    true parameters (linear cost) plus Laplace noise 0.05.
HiGHS, one thread, time limit per run given below. Writes results/milp_sensitivity.csv."""
import sys, time, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, cvxpy as cp
import migp, migp_quad as Q
from k2_study import instance, TRUE
from milp_small import solve as solve_quad

TL = 600
SEED = 2001
rows = []

def save():
    pd.DataFrame(rows).to_csv("results/milp_sensitivity.csv", index=False)

def solve_lin(X, D, eps, time_limit=300, M=30.0, Omega=5.0, delta=1e-3):
    p, V = migp._build_strict(X, D, eps, delta, Omega, M, 8.0, (0.05, 3.0))
    t0 = time.time(); p.solve(solver=cp.HIGHS, time_limit=time_limit, threads=1); sec = time.time() - t0
    st = p.solver_stats.extra_stats if p.solver_stats is not None else None
    inc = p.value; bound = getattr(st, "mip_dual_bound", np.nan) if st is not None else np.nan
    gap_rel = (inc - bound) / max(abs(inc), 1e-12) if inc is not None and np.isfinite(bound) else np.nan
    out = dict(status=p.status, incumbent=inc, dual_bound=bound, gap_rel=gap_rel, seconds=sec,
               closed=bool(p.status == "optimal" and np.isfinite(gap_rel) and gap_rel <= 1e-4))
    al = V["al"].value
    if al is not None:
        out.update(alpha1=al[0], alpha2=al[1], tau1=(V["c"].value / al)[0], tau2=(V["c"].value / al)[1])
    return out

if __name__ == "__main__":
    X, D, D0 = instance(SEED, 0.05, T=10)
    for name, M, Om in [("baseline", 30, 5), ("M=20", 20, 5), ("M=50", 50, 5), ("Omega=3", 30, 3), ("Omega=10", 30, 10)]:
        r = solve_quad(X, D, float(np.abs(D - D0).mean()), time_limit=TL, M=float(M), Omega=float(Om))
        rows.append(dict(model="quadratic", T=10, seed=SEED, setting=name, M=M, Omega=Om, eps=np.nan, time_limit=TL, **r))
        save(); print(rows[-1], flush=True)
    for T in (10, 15):
        X = instance(SEED, 0.05, T=T)[0]
        rng = np.random.default_rng(SEED + 77)
        Dlin0 = migp.forward_batch(X, TRUE["alpha"], TRUE["tau"], TRUE["b"], TRUE["op"], TRUE["om"])
        D = Dlin0 + rng.laplace(0, 0.05, T)
        for eps in (0.02, 0.05, 0.1):
            r = solve_lin(X, D, eps, time_limit=300)
            rows.append(dict(model="linear", T=T, seed=SEED, setting=f"eps={eps}", M=30, Omega=5, eps=eps,
                             time_limit=300, loss_true=float(np.abs(D - Dlin0).mean()), **r))
            save(); print(rows[-1], flush=True)
