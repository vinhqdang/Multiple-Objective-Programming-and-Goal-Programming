"""Point estimates of the 14 central-bank fits with the same lighter search as the bootstrap replicates
(differential evolution, population 40, 800 generations, LP polishing, no LNS), best of seeds 0-4, so that the
bootstrap distribution and the point estimate come from the same optimiser. Writes results/cb_light_point.csv."""
import sys, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import pandas as pd
from multiprocessing import Pool
import migp_quad as Q
from bootstrap_cb import data, CONF
from inverse_interval_gp_cb import WINDOWS

def job(a):
    cc, q0, q1, t, s = a; X, D = data(cc, q0, q1)
    h = Q.fit_hybrid(X, D, de_iter=800, de_pop=40, lns_iters=0, seed=s)
    return dict(country=cc, seed=s, loss=h["loss"], tau=h["tau"][0], alpha=h["alpha"][0], b=h["b"][0], stated=t)

if __name__ == "__main__":
    banks = [(cc, pd.Period(s, "M").asfreq("Q"), pd.Period(e, "M").asfreq("Q"), t) for cc, s, e, t, _ in WINDOWS]
    banks += [(cc, pd.Period(s, "Q"), pd.Period(e, "Q"), t) for cc, s, e, t in CONF]
    with Pool(4) as p: rows = p.map(job, [b + (s,) for b in banks for s in range(5)], chunksize=1)
    d = pd.DataFrame(rows); d.to_csv("results/cb_light_point_all.csv", index=False)
    best = d.loc[d.groupby("country").loss.idxmin()]; best.to_csv("results/cb_light_point.csv", index=False)
    print(best.round(3).to_string(index=False))
