"""Exact quadratic-cost K = 2 MILP (migp_quad._build, no fixed states, default M = 30, Omega = 5, delta = 1e-3) on
synthetic instances from k2_study.instance: T in {10, 15, 20, 30}, three fixed seeds each, decision noise 0.05,
HiGHS with one thread and a 600 s limit per run. Records status, incumbent (objective = mean absolute decision
error), dual bound, relative gap, run time, fitted parameters and the loss at the true parameters.
Writes results/milp_small.csv (rewritten after every run)."""
import sys, time, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, cvxpy as cp
import migp_quad as Q
from k2_study import instance, TRUE

TL = 600
SEEDS = [2001, 2002, 2003]

def solve(X, D, D0_loss, time_limit=TL, **kw):
    p, V = Q._build(X, D, **kw)
    t0 = time.time()
    p.solve(solver=cp.HIGHS, time_limit=time_limit, threads=1)
    sec = time.time() - t0
    st = p.solver_stats.extra_stats if p.solver_stats is not None else None
    inc = p.value
    bound = getattr(st, "mip_dual_bound", np.nan) if st is not None else np.nan
    gap_h = getattr(st, "mip_gap", np.nan) if st is not None else np.nan
    gap_rel = (inc - bound) / max(abs(inc), 1e-12) if inc is not None and np.isfinite(bound) else np.nan
    al = V["al"].value
    out = dict(status=p.status, incumbent=inc, dual_bound=bound, gap_rel=gap_rel, gap_highs=gap_h,
               nodes=getattr(st, "mip_node_count", np.nan) if st is not None else np.nan, seconds=sec,
               closed=bool(p.status == "optimal" and np.isfinite(gap_rel) and gap_rel <= 1e-4),
               loss_true=D0_loss)
    if al is not None:
        out.update(alpha1=al[0], alpha2=al[1], tau1=(V["c"].value / al)[0], tau2=(V["c"].value / al)[1],
                   b1=(V["d"].value / al)[0], b2=(V["d"].value / al)[1])
    return out

if __name__ == "__main__":
    rows = []
    for T in (10, 15, 20, 30):
        for seed in SEEDS:
            X, D, D0 = instance(seed, 0.05, T=T)
            loss_true = float(np.abs(D - D0).mean())
            r = solve(X, D, loss_true)
            rows.append(dict(T=T, seed=seed, noise=0.05, time_limit=TL, **r))
            pd.DataFrame(rows).to_csv("results/milp_small.csv", index=False)
            print({k: (round(v, 5) if isinstance(v, float) else v) for k, v in rows[-1].items()}, flush=True)
