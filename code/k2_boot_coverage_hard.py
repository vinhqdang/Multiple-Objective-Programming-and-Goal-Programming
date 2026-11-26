"""Coverage of the moving-block bootstrap for the two-goal model in a weakly identified, bank-like design:
T = 33, transmission of goal 1 low (alpha_1 = 0.2), wide band for goal 1 (b_1 = 1.5), Laplace noise 0.1 and
decisions rounded to multiples of 0.25 (as policy-rate changes are). True tau_1 = 2.5. 20 instances, each fitted
with the lighter search (as for the bank replicates) and bootstrapped with B = 50 replicates (blocks of 8).
The 90% percentile interval for tau_1 is computed over all replicates, with degenerate replicates (alpha_1 at its
lower bound) placed at +/- infinity on the side of the bounded median on which they fall, as in
summarise_bootstrap_cb_100.py. Writes results/k2_boot_coverage_hard_reps.csv (resumable) and
results/k2_boot_coverage_hard.csv. Usage: python code/k2_boot_coverage_hard.py [n_workers]"""
import sys, os, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from multiprocessing import Pool
import migp_quad as Q
N, B, BLOCK, T, OUT = 20, 50, 8, 33, "results/k2_boot_coverage_hard_reps.csv"
TRUE = dict(alpha=np.array([0.2, 1.0]), tau=np.array([2.5, 0.0]), b=np.array([1.5, 1.0]),
            op=np.array([0.5, 0.25]), om=np.array([0.5, 0.25]))

def instance(seed):
    r = np.random.default_rng(seed); X = np.zeros((T, 2)); s = np.array([3.0, 0.0])
    for t in range(T):
        s = np.array([3.0, 0.0]) + np.array([0.8, 0.7]) * (s - np.array([3.0, 0.0])) + r.normal(0, [1.2, 1.0]); X[t] = s
    D0 = Q.forward_batch(X, TRUE["alpha"], TRUE["tau"], TRUE["b"], TRUE["op"], TRUE["om"])
    return X, np.round((D0 + r.laplace(0, 0.1, T)) / 0.25) * 0.25

def job(a):
    i, b = a; X, D = instance(7000 + i)
    if b < 0: idx = np.arange(T)
    else:
        rng = np.random.default_rng(9000 * i + b); nb = int(np.ceil(T / BLOCK))
        idx = np.concatenate([np.arange(s, s + BLOCK) for s in rng.integers(0, T - BLOCK + 1, nb)])[:T]
    h = Q.fit_hybrid(X[idx], D[idx], de_iter=800, de_pop=40, lns_iters=0, seed=max(b, 0))
    with open(OUT, "a") as f: f.write(f"{i},{b},{h['tau'][0]:.6f},{h['alpha'][0]:.6f},{h['loss']:.6f}\n")

if __name__ == "__main__":
    nw = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    done = set()
    if os.path.exists(OUT): d = pd.read_csv(OUT, header=None); done = set(zip(d[0], d[1]))
    jobs = [(i, b) for b in range(-1, B) for i in range(N) if (i, b) not in done]
    with Pool(nw) as p:
        for _ in p.imap_unordered(job, jobs): pass
    d = pd.read_csv(OUT, header=None, names=["inst", "rep", "tau", "alpha", "loss"]).drop_duplicates(["inst", "rep"]); rows = []
    for i, g in d.groupby("inst"):
        r = g[g.rep >= 0]; deg = r.alpha <= 0.05 * 1.002
        m = r.tau[~deg].median() if (~deg).any() else 0.0
        t = r.tau.where(~deg, np.where(r.tau >= m, np.inf, -np.inf))
        lo, hi = np.quantile(t, [0.05, 0.95], method="inverted_cdf")
        rows.append(dict(inst=i, point=g[g.rep < 0].tau.iloc[0], point_alpha=g[g.rep < 0].alpha.iloc[0], lo=lo, hi=hi,
                         covers=lo <= 2.5 <= hi, degenerate=int(deg.sum()), n_rep=len(r)))
    s = pd.DataFrame(rows); s.to_csv("results/k2_boot_coverage_hard.csv", index=False)
    print(s.round(3).to_string(index=False)); print("coverage:", s.covers.mean())
