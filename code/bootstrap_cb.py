"""Moving-block bootstrap (blocks of 8 quarters, 20 replicates) of the implied inflation target in the gradualism
model, for the 9 exploratory and 5 confirmatory central banks. Each replicate uses a lighter search
(differential evolution, population 40, 800 generations, LP polishing, no LNS) to keep the cost manageable."""
import sys, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from multiprocessing import Pool
import migp_quad as Q, real_cb_migp_k2 as R
from inverse_interval_gp_cb import WINDOWS, ZLB
R.ISO3.update({"IL": "ISR", "NZ": "NZL", "CO": "COL", "HU": "HUN", "TR": "TUR"})
CONF = [("IL", "2003Q1", "2019Q4", 2.0), ("NZ", "2002Q3", "2012Q3", 2.0), ("CO", "2010Q1", "2019Q4", 3.0),
        ("HU", "2007Q1", "2015Q1", 3.0), ("TR", "2012Q1", "2019Q4", 5.0)]
B, BLOCK = 20, 8

def data(cc, q0, q1):
    q = R.build(cc); q = q[(q.index >= q0) & (q.index <= q1) & (q.rate_start > ZLB)]
    q["x_gap"] = q.growth - q.growth.mean()
    return q[["x_pi", "x_gap"]].values, q.D.values

def task(args):
    cc, q0, q1, b = args
    X, D = data(cc, q0, q1); T = len(D); rng = np.random.default_rng(1000 * b + 7)
    nb = int(np.ceil(T / BLOCK))
    idx = np.concatenate([np.arange(s, s + BLOCK) for s in rng.integers(0, T - BLOCK + 1, nb)])[:T]
    h = Q.fit_hybrid(X[idx], D[idx], de_iter=800, de_pop=40, lns_iters=0, seed=b)
    return cc, b, float(h["tau"][0])

if __name__ == "__main__":
    banks = [(cc, pd.Period(s, "M").asfreq("Q"), pd.Period(e, "M").asfreq("Q"), t) for cc, s, e, t, _ in WINDOWS]
    banks += [(cc, pd.Period(s, "Q"), pd.Period(e, "Q"), t) for cc, s, e, t in CONF]
    jobs = [(cc, q0, q1, b) for cc, q0, q1, t in banks for b in range(B)]
    with Pool(4) as p:
        out = p.map(task, jobs, chunksize=1)
    df = pd.DataFrame(out, columns=["country", "rep", "tau_pi"]); df.to_csv("results/bootstrap_cb_reps.csv", index=False)
    stated = {cc: t for cc, _, _, t in banks}
    s = df.groupby("country").tau_pi.agg(lo=lambda x: np.percentile(x, 5), med="median", hi=lambda x: np.percentile(x, 95)).round(2)
    s["stated"] = s.index.map(stated); s["covers_stated"] = (s.lo <= s.stated) & (s.stated <= s.hi); s["width"] = (s.hi - s.lo).round(2)
    s.to_csv("results/bootstrap_cb_summary.csv"); print(s.to_string())
