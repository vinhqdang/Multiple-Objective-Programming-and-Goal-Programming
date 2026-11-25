"""Exact check of the two-goal estimator on one real bank (Hungary, the shortest window, T = 33): the full MILP of
Section 3.1 (migp_quad._build, no fixed states) solved by HiGHS with a 2-hour limit. Reports the incumbent, the
proven dual bound and the gap, against the losses found by the multistart heuristic (results/cb_multiseed.csv).
Writes results/milp_check_hu.csv."""
import sys, time, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import cvxpy as cp, pandas as pd, migp_quad as Q
from bootstrap_cb import data, CONF
cc, q0, q1, t = [c for c in CONF if c[0] == "HU"][0]
X, D = data(cc, pd.Period(q0, "Q"), pd.Period(q1, "Q"))
p, V = Q._build(X, D); t0 = time.time(); p.solve(solver=cp.HIGHS, time_limit=7200)
info = p.solver_stats.extra_stats
ms = pd.read_csv("results/cb_multiseed.csv"); ms = ms[ms.country == "HU"]
row = dict(bank=cc, T=len(D), status=p.status, incumbent=p.value, dual_bound=info.mip_dual_bound, gap=info.mip_gap,
           nodes=info.mip_node_count, seconds=time.time() - t0, tau=(V["c"].value / V["al"].value)[0] if V["al"].value is not None else None,
           heuristic_best=ms.loss.min(), heuristic_worst=ms.loss.max())
pd.DataFrame([row]).to_csv("results/milp_check_hu.csv", index=False); print(row)
