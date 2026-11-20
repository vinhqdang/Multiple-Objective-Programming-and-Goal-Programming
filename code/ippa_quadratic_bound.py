"""Numerical check of the quadratic gap bound (docs/06_quadratic_bound_proof.md)."""
import sys, json; sys.path.insert(0, "code")
import numpy as np, ippa_cd as M
from ippa_stability import learn
from scipy.optimize import nnls

def supporting_weights(theta, Ah, bh, lnT, B=1.0):
    """w >= 0, sum w = 1 with  -sum_{k in A} w_k a_hat_k + w_c e^theta / B ~ 0 (stationarity of the learned scalarisation)."""
    K, n = Ah.shape
    act = (lnT - bh - Ah @ theta) > 0
    cols = [-Ah[k] if act[k] else np.zeros(n) for k in range(K)] + [np.exp(theta) / B]
    G = np.column_stack(cols); lam = 1e3                      # soft sum-to-one constraint
    G2 = np.vstack([G, lam * np.ones(K + 1)]); rhs = np.concatenate([np.zeros(n), [lam]])
    w, _ = nnls(G2, rhs); res = np.linalg.norm(G @ w)
    return w / w.sum(), act, res / w.sum()

def run(Ns=(200, 800, 3200), reps=10, sigma=0.15, n=40, K=4, iters=300, margin=1.0):
    u = np.array([1, 1, 1, 1, 0.2]); u = u / np.linalg.norm(u); out = []
    for N in Ns:
        for r in range(reps):
            rng = np.random.default_rng(10_000 * N + r)
            A, b, lnT = M.make_world(rng, n, K)
            Ah, bh = learn(rng, A, b, n, N, sigma)
            th, _ = M.ippa(Ah, bh, lnT, u, iters=iters, tol=1e-10)
            w, act, rho = supporting_weights(th, Ah, bh, lnT)
            lo, hi = th.min() - margin, th.max() + margin
            gap = M.pareto_gap(th, A, b, lnT, lo=lo, hi=hi)
            dA = np.linalg.norm(Ah - A, axis=1)
            l_hat = lnT - bh - Ah @ th; l_true = lnT - b - A @ th
            margin_ok = bool(all(np.sign(l_hat[k]) == np.sign(l_true[k]) and abs(l_hat[k]) > 0 for k in range(K) if w[k] > 1e-9))
            wc = w[-1]
            core = (w[:K] * act * dA).sum() + rho                      # dist(0, subdifferential of the true scalarisation)
            bound = np.exp(-lo) * core ** 2 / (2 * wc)
            out.append(dict(N=N, gap=gap, bound=float(bound), rho=float(rho), wc=float(wc), margin_ok=margin_ok, holds=bool(gap <= bound + 1e-8)))
        print(N, "done", flush=True)
    return out

if __name__ == "__main__":
    rows = run(); json.dump(rows, open("results/ippa_quadratic_bound.json", "w"), indent=1)
    import pandas as pd; d = pd.DataFrame(rows)
    d["ratio"] = d.gap / d.bound
    print(d.groupby("N").agg(gap=("gap", "mean"), bound=("bound", "mean"), ratio=("ratio", "mean"), rho=("rho", "max"),
                             wc=("wc", "mean"), margin_ok=("margin_ok", "mean"), holds=("holds", "mean")).round(5))
