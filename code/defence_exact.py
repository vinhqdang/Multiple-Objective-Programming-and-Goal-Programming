"""Defence spending (NATO definition, % of GDP), allies pooled with common parameters in two periods.
Exact one-goal estimator (Theorem 2, alpha = 1, decision D = -Delta). Adds, for the lower band edge e_minus:
(i) the exact profile loss over a grid of e_minus values and its near-optimal set (2% and 5% tolerance), and
(ii) a cluster bootstrap that resamples allies with replacement (B = 200).
Writes results/defence_exact.csv (point estimates) and results/defence_uncertainty.csv."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, exact_k1 as X
from multiprocessing import Pool
from applications_gp import panel
PERIODS = [(2015, 2021), (2022, 2025)]; BOOT = 200

def load():
    n = pd.read_csv("data/cofog/nato_defence_pc_gdp.csv.gz").rename(columns={"defence_pc_gdp": "v"})
    n = n[~n.country.str.contains("NATO|Europe|Canada and", case=False, regex=True) | (n.country == "Canada")].dropna(subset=["v"])
    return panel(n, "country", "v")

def profile_lower(x, D, grid):
    """Exact profile loss over the lower edge e_minus (alpha = 1): for each e_minus, minimise over e_plus >= e_minus
    and both steps. Candidates for e_plus are E U {e_minus} (the coupling vertex)."""
    z = x; om = np.abs(D).max() * 1.0001 + 1e-12
    E = np.unique(np.concatenate([(z[:, None] - D[None, :]).ravel(), z]))
    absD = np.abs(D); o = np.argsort(z); zs, cs = z[o], np.concatenate([[0], np.cumsum(absD[o])])
    out = []
    for em in grid:
        Ep = np.unique(np.concatenate([E[E >= em], [em]]))
        Up, _ = X._upper_best(z, D, Ep, om); A = cs[np.searchsorted(zs, Ep, side="right")]
        Lm, _ = X._upper_best(-z, -D, np.array([-em]), om); B = cs[np.searchsorted(zs, em, side="left")]
        out.append((Lm[0] - B + (Up + A).min()) / len(D))
    return np.array(out)

def fit(g):
    x, D = g.x.values, -g.delta.values
    return X.solve_fixed_alpha(x, D, 1.0)

def boot_job(args):
    a0, a1, b = args; q = load(); g = q[(q.year >= a0) & (q.year <= a1)]
    rng = np.random.default_rng(100 + b); allies = g.country.unique()
    pick = rng.choice(allies, len(allies), replace=True)
    gb = pd.concat([g[g.country == c] for c in pick]); r = fit(gb)
    return dict(period=f"{a0}-{a1}", rep=b, band_lo=r["e_m"], band_hi=r["e_p"], step_raise=r["om_m"], step_cut=r["om_p"])

if __name__ == "__main__":
    q = load(); rows, unc = [], []
    for a0, a1 in PERIODS:
        g = q[(q.year >= a0) & (q.year <= a1)]; r = fit(g); x, D = g.x.values, -g.delta.values
        rows.append(dict(period=f"{a0}-{a1}", n=len(g), loss=round(r["loss"], 4), tau=round(r["tau"], 3), b=round(r["b"], 3),
                         band_lo=round(r["e_m"], 2), band_hi=round(r["e_p"], 2), step_cut=round(r["om_p"], 2), step_raise=round(r["om_m"], 2),
                         mean_level=round(x.mean(), 3), share_above_hi=round((x > r["e_p"]).mean(), 3),
                         share_below_lo=round((x < r["e_m"]).mean(), 3)))
        grid = np.round(np.arange(max(0.5, x.min()), x.max() + 0.005, 0.01), 3); prof = profile_lower(x, D, grid); best = prof.min()
        s2 = grid[prof <= best * 1.02 + 1e-12]; s5 = grid[prof <= best * 1.05 + 1e-12]
        unc.append(dict(period=f"{a0}-{a1}", band_lo=r["e_m"], prof_best=best, set2_lo=s2.min(), set2_hi=s2.max(), set5_lo=s5.min(), set5_hi=s5.max()))
        print(rows[-1], unc[-1], flush=True)
    jobs = [(a0, a1, b) for a0, a1 in PERIODS for b in range(BOOT)]
    with Pool(2) as p: bt = pd.DataFrame(p.map(boot_job, jobs, chunksize=4))
    bt.to_csv("results/defence_boot_reps.csv", index=False)
    for u in unc:
        z = bt[bt.period == u["period"]]
        u.update(boot_lo5=z.band_lo.quantile(.05), boot_lo95=z.band_lo.quantile(.95),
                 boot_raise5=z.step_raise.quantile(.05), boot_raise95=z.step_raise.quantile(.95))
    pd.DataFrame(rows).to_csv("results/defence_exact.csv", index=False)
    pd.DataFrame(unc).to_csv("results/defence_uncertainty.csv", index=False); print(pd.DataFrame(unc).round(3).to_string())
