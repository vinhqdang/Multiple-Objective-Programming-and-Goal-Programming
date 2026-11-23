"""Moving-block bootstrap of the implied inflation target with the FULL estimator used for the point estimates
(migp_quad.fit_hybrid, default settings: differential evolution with population 80 and 3000 generations, LP
polishing and LNS). Blocks of 8 quarters, 20 replicates per bank, one seed per replicate. Resumable: finished
replicates are appended to results/bootstrap_cb_full_reps.csv and skipped on restart."""
import sys, os, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from multiprocessing import Pool
import migp_quad as Q
from bootstrap_cb import data, CONF, B, BLOCK
from inverse_interval_gp_cb import WINDOWS
OUT = "results/bootstrap_cb_full_reps.csv"

def task(args):
    cc, q0, q1, b = args
    X, D = data(cc, q0, q1); T = len(D); rng = np.random.default_rng(1000 * b + 7)   # same resamples as before
    nb = int(np.ceil(T / BLOCK))
    idx = np.concatenate([np.arange(s, s + BLOCK) for s in rng.integers(0, T - BLOCK + 1, nb)])[:T]
    h = Q.fit_hybrid(X[idx], D[idx], seed=b)
    line = f"{cc},{b},{h['tau'][0]:.6f},{h['alpha'][0]:.6f},{h['loss']:.6f}\n"
    with open(OUT, "a") as f: f.write(line)
    return line

if __name__ == "__main__":
    banks = [(cc, pd.Period(s, "M").asfreq("Q"), pd.Period(e, "M").asfreq("Q"), t) for cc, s, e, t, _ in WINDOWS]
    banks += [(cc, pd.Period(s, "Q"), pd.Period(e, "Q"), t) for cc, s, e, t in CONF]
    done = set()
    if os.path.exists(OUT):
        d = pd.read_csv(OUT, header=None, names=["country", "rep", "tau_pi", "alpha_pi", "loss"]); done = set(zip(d.country, d.rep))
    jobs = [(cc, q0, q1, b) for cc, q0, q1, t in banks for b in range(B) if (cc, b) not in done]
    print("jobs remaining:", len(jobs), flush=True)
    with Pool(4) as p:
        for _ in p.imap_unordered(task, jobs): pass
    print("done", flush=True)
