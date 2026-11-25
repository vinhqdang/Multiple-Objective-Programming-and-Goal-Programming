"""Moving-block bootstrap with 100 replicates per bank (500 when run with BOOT_B=500) (after review; the 20-replicate version with the full
estimator is in bootstrap_cb_full.py). Blocks of 8 quarters; the same resampling seeds as bootstrap_cb.py for the
first 20 replicates. Each replicate uses the lighter search of bootstrap_cb.py (differential evolution, population
40, 800 generations, LP polishing, no LNS). Besides tau we record alpha and the inflation band edges in the
transformed scale, e = alpha*(tau -/+ b), which stay bounded when alpha reaches its lower bound and tau does not.
Resumable: results/bootstrap_cb_100_reps.csv."""
import sys, os, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from multiprocessing import Pool
import migp_quad as Q
from bootstrap_cb import data, CONF, BLOCK
from inverse_interval_gp_cb import WINDOWS
B = int(os.environ.get('BOOT_B', 100)); OUT = "results/bootstrap_cb_100_reps.csv"

def task(args):
    cc, q0, q1, b = args
    X, D = data(cc, q0, q1); T = len(D); rng = np.random.default_rng(1000 * b + 7)
    nb = int(np.ceil(T / BLOCK))
    idx = np.concatenate([np.arange(s, s + BLOCK) for s in rng.integers(0, T - BLOCK + 1, nb)])[:T]
    h = Q.fit_hybrid(X[idx], D[idx], de_iter=800, de_pop=40, lns_iters=0, seed=b)
    a, t, bb = h["alpha"][0], h["tau"][0], h["b"][0]
    line = f"{cc},{b},{t:.6f},{a:.6f},{a*(t-bb):.6f},{a*(t+bb):.6f},{h['loss']:.6f}\n"
    with open(OUT, "a") as f: f.write(line)
    return line

if __name__ == "__main__":
    banks = [(cc, pd.Period(s, "M").asfreq("Q"), pd.Period(e, "M").asfreq("Q"), t) for cc, s, e, t, _ in WINDOWS]
    banks += [(cc, pd.Period(s, "Q"), pd.Period(e, "Q"), t) for cc, s, e, t in CONF]
    done = set()
    if os.path.exists(OUT):
        d = pd.read_csv(OUT, header=None); done = set(zip(d[0], d[1]))
    jobs = [(cc, q0, q1, b) for b in range(B) for cc, q0, q1, t in banks if (cc, b) not in done]
    print("jobs remaining:", len(jobs), flush=True)
    with Pool(4) as p:
        for _ in p.imap_unordered(task, jobs): pass
    print("done", flush=True)
