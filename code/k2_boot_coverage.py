"""Coverage check of the moving-block bootstrap for the two-goal model: 20 synthetic instances (the K = 2 design of
k2_study.py, noise 0.05, T = 60), each fitted with the lighter search and bootstrapped with B = 50 replicates
(blocks of 8). The 90% percentile interval for tau_1 is computed over all replicates (degenerate ones included);
we record whether it covers the true value 2.5. Writes results/k2_boot_coverage.csv (resumable)."""
import sys, os, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from multiprocessing import Pool
import migp_quad as Q
from k2_study import instance
N, B, BLOCK, OUT = 20, 50, 8, "results/k2_boot_coverage_reps.csv"

def job(a):
    i, b = a; X, D, _ = instance(1000 + i, 0.05); T = len(D)
    if b < 0: idx = np.arange(T)
    else:
        rng = np.random.default_rng(5000 * i + b); nb = int(np.ceil(T / BLOCK))
        idx = np.concatenate([np.arange(s, s + BLOCK) for s in rng.integers(0, T - BLOCK + 1, nb)])[:T]
    h = Q.fit_hybrid(X[idx], D[idx], de_iter=800, de_pop=40, lns_iters=0, seed=max(b, 0))
    line = f"{i},{b},{h['tau'][0]:.6f},{h['alpha'][0]:.6f},{h['loss']:.6f}\n"
    with open(OUT, "a") as f: f.write(line)

if __name__ == "__main__":
    done = set()
    if os.path.exists(OUT): d = pd.read_csv(OUT, header=None); done = set(zip(d[0], d[1]))
    jobs = [(i, b) for b in range(-1, B) for i in range(N) if (i, b) not in done]
    with Pool(4) as p:
        for _ in p.imap_unordered(job, jobs): pass
    d = pd.read_csv(OUT, header=None, names=["inst", "rep", "tau", "alpha", "loss"]); rows = []
    for i, g in d.groupby("inst"):
        r = g[g.rep >= 0]; lo, hi = r.tau.quantile([0.05, 0.95])
        pt = g[g.rep < 0].tau.iloc[0]
        rows.append(dict(inst=i, point=pt, lo=lo, hi=hi, covers=lo <= 2.5 <= hi, degenerate=int((r.alpha < 0.0501).sum())))
    s = pd.DataFrame(rows); s.to_csv("results/k2_boot_coverage.csv", index=False)
    print(s.round(3).to_string(index=False)); print("coverage:", s.covers.mean())
