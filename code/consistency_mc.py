"""Monte Carlo for Theorem B: exact one-goal estimator (alpha = 1) with Laplace decision noise; error of
(tau, b, omega+, omega-) as T grows. x_t: a stationary AR(1) process (the state the decision maker faces)."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, exact_k1 as X
from multiprocessing import Pool
TRUE = dict(tau=2.0, b=0.5, om_p=0.4, om_m=0.3)

def one(args):
    T, rep = args; rng = np.random.default_rng(10_000 * T + rep)
    ep, em = TRUE["tau"] + TRUE["b"], TRUE["tau"] - TRUE["b"]
    x = np.empty(T); s = 2.0
    for t in range(T):
        s = 2.0 + 0.7 * (s - 2.0) + rng.normal(0, 0.9); x[t] = s
    D = X.h(x, 1.0, ep, em, TRUE["om_p"], TRUE["om_m"]) + rng.laplace(0, 0.1, T)
    r = X.solve_fixed_alpha(x, D, 1.0)
    return dict(T=T, rep=rep, tau=r["tau"], b=r["b"], om_p=r["om_p"], om_m=r["om_m"])

if __name__ == "__main__":
    jobs = [(T, r) for T in (50, 100, 200) for r in range(30)]
    with Pool(4) as p: out = pd.DataFrame(p.map(one, jobs, chunksize=1))
    out.to_csv("results/consistency_mc.csv", index=False)
    for k, v in TRUE.items(): out[k + "_err"] = (out[k] - v).abs()
    print(out.groupby("T")[[k + "_err" for k in TRUE]].median().round(4))
