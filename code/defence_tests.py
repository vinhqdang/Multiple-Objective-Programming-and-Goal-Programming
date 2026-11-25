"""Defence spending (NATO, % of GDP): panel tests for the two pooled periods of code/defence_exact.py.
(1) State-dependence permutation test: decisions permuted within each ally, level paths rebuilt from each ally's
    first observed level (x_{t+1} = x_t + delta_t), pooled, refit with the exact one-goal estimator; statistic
    gain = 1 - L_GP / mean|D|; B = 999.
(2) Partial-adjustment (PA) null test: pooled LAD fit delta = a + b x; each ally's path simulated from its first level
    with residuals resampled (i) i.i.d. from the pooled residuals and (ii) by whole-ally residual vectors (cluster);
    statistic S = L_PA / L_GP, refit on each simulated panel; B = 999.
(3) Leave-one-ally-out refits: lower edge e_m, upper edge e_p, step up om_m, step down om_p.
(4) Full-sample shares outside the band and within-ally lag-1 autocorrelation of decisions (printed).
Writes results/defence_tests.csv and results/defence_loo.csv."""
import sys; sys.path.insert(0, "code")
import time
import numpy as np, pandas as pd, exact_k1 as X
from multiprocessing import Pool
from defence_exact import load, fit, PERIODS
from permutation_test import gain, rebuild
from misspec_placebo import lad

B = 999; BPA = 499          # PA replicates reduced from 999 to 499 (runtime, ~2.8 s per PA replicate on 2 cores)
G, ALLY, PA = {}, {}, {}          # filled in __main__ before the pool forks

def allies(g):
    return [(s.x.values[0], s.delta.values) for _, s in g.groupby("country", sort=True)]

def pa_stat(x, d):
    a, b = lad(x, d); res = d - a - b * x
    lgp = X.solve_fixed_alpha(x, -d, 1.0)["loss"]
    return np.abs(res).mean() / max(lgp, 1e-12), a, b, res

def perm_job(args):
    pi, rep = args
    rng = np.random.default_rng(1_000_000 * (pi + 1) + rep); xs, ds = [], []
    for x0, d in ALLY[pi]:
        dp = rng.permutation(d); xs.append(rebuild(x0, dp)); ds.append(dp)
    return gain(np.concatenate(xs), np.concatenate(ds))

def pa_job(args):
    pi, mode, rep = args
    rng = np.random.default_rng(2_000_000 + 1_000_000 * pi + 100_000 * (mode == "cluster") + rep)
    _, a, b, res_pool, res_ally = PA[pi]; xs, ds = [], []
    for x0, d in ALLY[pi]:
        n = len(d)
        if mode == "iid":
            e = rng.choice(res_pool, n, replace=True)
        else:                                    # whole-ally residual vector, cyclically resized to this ally's length
            e = np.resize(res_ally[rng.integers(len(res_ally))], n)
        x = np.empty(n); dd = np.empty(n); x[0] = x0
        for t in range(n):
            dd[t] = a + b * x[t] + e[t]
            if t + 1 < n: x[t + 1] = x[t] + dd[t]
        xs.append(x); ds.append(dd)
    return pa_stat(np.concatenate(xs), np.concatenate(ds))[0]

def loo_job(args):
    pi, ally = args                              # ally None = full sample
    g = G[pi] if ally is None else G[pi][G[pi].country != ally]
    r = fit(g)
    return dict(period=PERIODS_LBL[pi], dropped_ally=ally or "none", n=len(g), lower_edge=r["e_m"], upper_edge=r["e_p"],
                step_up=r["om_m"], step_down=r["om_p"], loss=r["loss"])

PERIODS_LBL = [f"{a0}-{a1}" for a0, a1 in PERIODS]

def pvalue(null, obs):
    return (1 + (np.asarray(null) >= obs).sum()) / (len(null) + 1)

if __name__ == "__main__":
    t0 = time.time(); q = load(); rows = []; diag = []; loo_jobs = []
    quick = len(sys.argv) > 1 and sys.argv[1] == "quick"
    for pi, (a0, a1) in enumerate(PERIODS):
        g = q[(q.year >= a0) & (q.year <= a1)].sort_values(["country", "year"]); G[pi] = g; ALLY[pi] = allies(g)
        x, d = g.x.values, g.delta.values; D = -d
        full = fit(g)
        a, b = lad(x, d); res = d - a - b * x
        res_ally = [s.delta.values - a - b * s.x.values for _, s in g.groupby("country", sort=True)]
        PA[pi] = (None, a, b, res, res_ally)
        obs_gain = gain(x, d)
        obs_pa = pa_stat(x, d)[0]
        print(f"[{PERIODS_LBL[pi]}] n={len(g)} allies={len(ALLY[pi])} gain={obs_gain:.4f} S={obs_pa:.4f} "
              f"PA a={a:.4f} b={b:.4f}", flush=True)
        lo, hi = full["e_m"], full["e_p"]
        below = (x < lo).mean(); above = (x > hi).mean()
        pairs = [(s.delta.values[:-1], s.delta.values[1:]) for _, s in g.groupby("country", sort=True) if len(s) > 1]
        p0 = np.concatenate([p[0] for p in pairs]); p1 = np.concatenate([p[1] for p in pairs])
        ac_raw = np.corrcoef(p0, p1)[0, 1]
        dm = g.assign(dd=g.delta - g.groupby("country").delta.transform("mean"))
        pairs_dm = [(s.dd.values[:-1], s.dd.values[1:]) for _, s in dm.groupby("country", sort=True) if len(s) > 1]
        ac_dm = np.corrcoef(np.concatenate([p[0] for p in pairs_dm]), np.concatenate([p[1] for p in pairs_dm]))[0, 1]
        diag.append(dict(period=PERIODS_LBL[pi], band_lo=round(lo, 3), band_hi=round(hi, 3), share_below_lo=round(below, 3),
                         share_above_hi=round(above, 3), ac1_within_ally=round(ac_raw, 3), ac1_within_ally_demeaned=round(ac_dm, 3),
                         ac1_pairs=len(p0)))
        rows.append(dict(period=PERIODS_LBL[pi], test="perm", stat=obs_gain, null95=None, p=None, B=B, _obs=obs_gain))
        rows.append(dict(period=PERIODS_LBL[pi], test="pa_iid", stat=obs_pa, null95=None, p=None, B=BPA, _obs=obs_pa))
        rows.append(dict(period=PERIODS_LBL[pi], test="pa_cluster", stat=obs_pa, null95=None, p=None, B=BPA, _obs=obs_pa))
        loo_jobs.append((pi, None))
        loo_jobs += [(pi, c) for c in sorted(g.country.unique())]
    if quick:
        t1 = time.time()
        with Pool(2) as pool:
            p_ = pool.map(perm_job, [(0, r) for r in range(4)], chunksize=1)
            t2 = time.time(); _ = pool.map(pa_job, [(0, "iid", r) for r in range(4)], chunksize=1)
            t3 = time.time(); _ = pool.map(pa_job, [(0, "cluster", r) for r in range(4)], chunksize=1)
            t4 = time.time()
        print(f"timing: perm {(t2-t1)/4:.2f}s/rep, pa_iid {(t3-t2)/4:.2f}s/rep, pa_cluster {(t4-t3)/4:.2f}s/rep (Pool(2), per-core approx x2)", flush=True)
        print("quick perm sample", np.round(p_, 4)); sys.exit(0)

    jobs_perm = [(pi, r) for pi in range(len(PERIODS)) for r in range(B)]
    jobs_pa = [(pi, m, r) for pi in range(len(PERIODS)) for m in ("iid", "cluster") for r in range(BPA)]
    with Pool(2) as pool:
        t = time.time(); null_perm = pool.map(perm_job, jobs_perm, chunksize=8); print(f"perm done {time.time()-t:.0f}s", flush=True)
        t = time.time(); null_pa = pool.map(pa_job, jobs_pa, chunksize=8); print(f"pa done {time.time()-t:.0f}s", flush=True)
        t = time.time(); loo = pool.map(loo_job, loo_jobs, chunksize=2); print(f"loo done {time.time()-t:.0f}s", flush=True)
    np_ = np.array(null_perm).reshape(len(PERIODS), B); npa = np.array(null_pa).reshape(len(PERIODS), 2, BPA)
    out = []
    for pi, lbl in enumerate(PERIODS_LBL):
        for r in rows:
            if r["period"] != lbl: continue
            if r["test"] == "perm": null = np_[pi]
            else: null = npa[pi, 0 if r["test"] == "pa_iid" else 1]
            r["null95"] = np.percentile(null, 95); r["p"] = pvalue(null, r["_obs"]); out.append({k: v for k, v in r.items() if k != "_obs"})
    T = pd.DataFrame(out).round({"stat": 4, "null95": 4, "p": 4}); T.to_csv("results/defence_tests.csv", index=False)
    LOO = pd.DataFrame(loo); LOO.to_csv("results/defence_loo.csv", index=False)
    print(T.to_string(index=False)); print(pd.DataFrame(diag).to_string(index=False))
    for lbl in PERIODS_LBL:
        z = LOO[LOO.period == lbl]; full_row = z[z.dropped_ally == "none"].iloc[0]; zz = z[z.dropped_ally != "none"].copy()
        zz["shift"] = (zz.lower_edge - full_row.lower_edge).abs(); top = zz.loc[zz["shift"].idxmax()]
        print(f"LOO {lbl}: full e_m={full_row.lower_edge:.3f}; e_m range over {len(zz)} drops = [{zz.lower_edge.min():.3f}, {zz.lower_edge.max():.3f}]; "
              f"largest move: drop {top.dropped_ally} -> e_m={top.lower_edge:.3f} (shift {top['shift']:.3f}); "
              f"upper edge range [{zz.upper_edge.min():.3f}, {zz.upper_edge.max():.3f}]")
    print(f"total run time {time.time()-t0:.0f}s", flush=True)
