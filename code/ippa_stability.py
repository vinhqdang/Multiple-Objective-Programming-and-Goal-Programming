"""Stability of IPPA solutions when the Cobb-Douglas coefficients are learned from data."""
import sys, json; sys.path.insert(0, "code")
import numpy as np, ippa_cd as M

def learn(rng, A, b, n, N, sigma):
    Th = np.log(1.0 / n) + rng.normal(0, 0.5, size=(N, n))        # historical allocations (log scale)
    Y = Th @ A.T + b + rng.normal(0, sigma, size=(N, A.shape[0]))  # log outcomes with noise
    X = np.column_stack([np.ones(N), Th])
    coef = np.linalg.lstsq(X, Y, rcond=None)[0]                    # OLS on log-log data
    bh, Ah = coef[0], np.maximum(coef[1:].T, 1e-3)                 # elasticities kept positive (nonnegativity, A4)
    return Ah, bh

def eps_at(theta, Ah, bh, A, b, lnT):
    return np.abs(M.psi(theta, Ah, bh, lnT)[:-1] - M.psi(theta, A, b, lnT)[:-1]).max()

def run(Ns=(100, 200, 400, 800, 1600, 3200), reps=15, sigma=0.15, n=40, K=4, iters=250):
    u = np.array([1, 1, 1, 1, 0.2]); u = u / np.linalg.norm(u); rows = []
    for N in Ns:
        for r in range(reps):
            rng = np.random.default_rng(10_000 * N + r)
            A, b, lnT = M.make_world(rng, n, K)
            Ah, bh = learn(rng, A, b, n, N, sigma)
            th, h = M.ippa(Ah, bh, lnT, u, iters=iters, tol=1e-10)
            gap_hat = M.pareto_gap(th, Ah, bh, lnT)                 # optimality for the learned problem
            gap, th_star = M.pareto_gap(th, A, b, lnT, return_point=True)   # improvement left in the TRUE problem
            bound = eps_at(th, Ah, bh, A, b, lnT) + eps_at(th_star, Ah, bh, A, b, lnT)
            th_eq = np.full(n, np.log(1.0 / n))
            rows.append(dict(N=N, rep=r, err_A=float(np.abs(Ah - A).sum(1).mean()), gap_hat=float(gap_hat), gap=float(gap),
                             bound=float(bound), gap_equal=float(M.pareto_gap(th_eq, A, b, lnT)),
                             holds=bool(gap <= bound + 1e-6)))
        print(N, "done", flush=True)
    return rows

if __name__ == "__main__":
    rows = run(); json.dump(rows, open("results/ippa_stability.json", "w"), indent=1)
    import pandas as pd
    d = pd.DataFrame(rows)
    print(d.groupby("N").agg(err_A=("err_A", "mean"), gap_hat=("gap_hat", "max"), gap=("gap", "mean"), gap_se=("gap", lambda x: x.std()/len(x)**.5),
                             bound=("bound", "mean"), equal=("gap_equal", "mean"), holds=("holds", "mean")).round(5))
