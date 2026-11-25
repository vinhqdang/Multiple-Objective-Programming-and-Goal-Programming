"""Parametric bootstrap test of the interval goal program against linear partial adjustment, extended.
Null hypothesis: decisions follow linear partial adjustment, Delta_t = a + b x_t + e_t, estimated by LAD
(misspec_placebo.lad). The statistic is S = L_PA / L_GP, the ratio of in-sample mean absolute decision errors of
the LAD partial-adjustment fit and the exact goal-program fit (pa_null_test.stat). Under a bootstrap draw the level
path is rebuilt as x_{t+1} = x_t + Delta_t + jump_t, where jump_t is the non-decision change (kept at the 2018
definitional break for the aid series, zero for simulated series). Two residual resamplers are compared:
  iid   : residuals drawn i.i.d. with replacement (as in pa_null_test),
  block : residuals resampled in moving blocks of length 3 (blocks drawn with replacement, concatenated, cut to T),
          so that persistent residuals are kept.
p = (1 + #{S* >= S}) / (B + 1). Output: results/pa_null_extend.csv with one row per unit.

Parts:
 (1) aid: the 23 donors of aid_profile.data(), B = 999, seed 11 (same seed as pa_null_test). Benjamini-Hochberg
     adjusted p-values (permutation_extend.bh) over the 23 donors for each variant.
 (2) size: the PA test applied to series generated under a null, B = 199 per series, 60 series per design
     (reduced from 100 because the full run would take about 4 hours on Pool(2)),
     T = 60, start level 0.4, decision innovations N(0, 0.03):
       size_a_pa_iid : Delta = 0.04 - 0.1 x + e, e i.i.d. (mean-reverting PA, null true)
       size_b_pa_ar1 : Delta = 0.04 - 0.1 x + e, e AR(1) with coefficient 0.5 (innovations N(0, 0.03))
       size_c_iid    : Delta i.i.d. N(0, 0.03), independent of the state (PA with b near 0)
       size_d_ar1    : Delta AR(1) with coefficient 0.7, independent of the state
     Level path rebuilt as x_{t+1} = x_t + Delta_t.
 (3) power: 100 series per design, B = 199 each.
       power_gp : decisions from the exact interval goal program (exact_k1.h, alpha = 1, upper edge e_p = 0.6,
                  lower edge e_m = 0.3, om_p = om_m = 0.05): Delta_t = -h(x_t) + Laplace(0, 0.01), x_{t+1} = x_t + Delta_t,
                  x_1 = 0.4.
       power_qp : the quadratic-programme DGP of misspec_placebo.simulate("qp") reused unchanged (its level scale is
                  around 2, not 0.4).
Rejection rates at 5% and 10% are printed; the rows are written to the CSV with the same columns for all domains.
Run from the repository root: python code/pa_null_extend.py [n_size n_power B_aid B_sim out_csv]
(defaults 60 100 999 199 results/pa_null_extend.csv)."""
import sys; sys.path.insert(0, "code")
import os, time
import numpy as np, pandas as pd, exact_k1 as X
from multiprocessing import Pool
from misspec_placebo import lad, simulate as qp_simulate
from pa_null_test import stat
from permutation_extend import bh
from permutation_test import rebuild

BLOCK = 3; SEED = 11; T_SIM = 60; X1 = 0.4
SIZE_DESIGNS = ["size_a_pa_iid", "size_b_pa_ar1", "size_c_iid", "size_d_ar1"]
POWER_DESIGNS = ["power_gp", "power_qp"]
B_AID = 999; B_SIM = 199

def jumps_of(x, d):
    return np.append(x[1:] - x[:-1] - d[:-1], 0.0)

def draw_errors(res, T, rng, block):
    if not block:
        return rng.choice(res, T, replace=True)
    starts = rng.integers(0, T - BLOCK + 1, -(-T // BLOCK))
    return np.concatenate([res[s:s + BLOCK] for s in starts])[:T]

def rebuild_pa(x1, a, b, e, jumps):
    T = len(e); x = np.empty(T); d = np.empty(T); x[0] = x1
    for t in range(T):
        d[t] = a + b * x[t] + e[t]
        if t + 1 < T:
            x[t + 1] = x[t] + d[t] + jumps[t]
    return x, d

def pa_pvalues(x, d, B, seed):
    """Returns S, p_iid, p_block for one series (same statistic and LAD fit for both resamplers)."""
    s0, a, b = stat(x, d); res = d - a - b * x; jumps = jumps_of(x, d)
    rng = np.random.default_rng(seed); p = {}
    for name, block in (("iid", False), ("block", True)):
        null = np.empty(B)
        for i in range(B):
            xs, ds = rebuild_pa(x[0], a, b, draw_errors(res, len(x), rng, block), jumps)
            null[i] = stat(xs, ds)[0]
        p[name] = (1 + (null >= s0).sum()) / (B + 1)
    return s0, p["iid"], p["block"]

def aid_job(item):
    donor, x, d = item
    s0, p_iid, p_block = pa_pvalues(x, d, B_AID, SEED)
    return dict(domain="aid", unit=donor, n=len(x), S=s0, p_iid=p_iid, p_block=p_block)

def size_series(design, rng, T=T_SIM):
    e = rng.normal(0, 0.03, T)
    if design in ("size_a_pa_iid", "size_b_pa_ar1"):
        if design == "size_b_pa_ar1":
            u = e.copy(); e[0] = u[0]
            for t in range(1, T): e[t] = 0.5 * e[t - 1] + u[t]
        x = np.empty(T); d = np.empty(T); x[0] = X1
        for t in range(T):
            d[t] = 0.04 - 0.1 * x[t] + e[t]
            if t + 1 < T: x[t + 1] = x[t] + d[t]
        return x, d
    if design == "size_c_iid":
        d = e
    else:                                   # size_d_ar1
        d = np.empty(T); d[0] = e[0]
        for t in range(1, T): d[t] = 0.7 * d[t - 1] + e[t]
    return rebuild(X1, d), d

def power_series(design, rng, T=T_SIM):
    if design == "power_qp":
        return qp_simulate("qp", T, rng)
    x = np.empty(T); d = np.empty(T); x[0] = X1
    for t in range(T):
        d[t] = -X.h(np.array([x[t]]), 1.0, 0.6, 0.3, 0.05, 0.05)[0] + rng.laplace(0, 0.01)
        if t + 1 < T: x[t + 1] = x[t] + d[t]
    return x, d

def sim_job(args):
    design, idx, rep, B = args
    rng = np.random.default_rng(100_000 * (idx + 1) + rep)
    x, d = size_series(design, rng) if design.startswith("size") else power_series(design, rng)
    s0, p_iid, p_block = pa_pvalues(x, d, B, 1_000_000 * (idx + 1) + rep)
    return dict(domain=design, unit=rep, n=len(x), S=s0, p_iid=p_iid, p_block=p_block)

def rate(z, col, level):
    return (z[col] <= level).mean()

if __name__ == "__main__":
    n_size = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    n_power = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    B_AID = int(sys.argv[3]) if len(sys.argv) > 3 else 999
    B_SIM = int(sys.argv[4]) if len(sys.argv) > 4 else 199
    out = sys.argv[5] if len(sys.argv) > 5 else "results/pa_null_extend.csv"
    import aid_profile as A
    items = [(k, g.x.values, g.delta.values) for k, g in A.data().items()]
    sims = [(dz, i, r, B_SIM) for i, dz in enumerate(SIZE_DESIGNS) for r in range(n_size)]
    sims += [(dz, 10 + i, r, B_SIM) for i, dz in enumerate(POWER_DESIGNS) for r in range(n_power)]
    t0 = time.time()
    with Pool(2) as pool:
        rows = pool.map(aid_job, items, chunksize=1)
        t1 = time.time(); print(f"aid done in {t1 - t0:.0f}s", flush=True)
        for k, r in enumerate(pool.imap(sim_job, sims, chunksize=2), 1):
            rows.append(r)
            if k % 40 == 0: print(f"simulated series {k}/{len(sims)} at {time.time() - t0:.0f}s", flush=True)
    d = pd.DataFrame(rows)
    d["p_iid_bh"] = np.nan; d["p_block_bh"] = np.nan
    a = d.domain == "aid"
    d.loc[a, "p_iid_bh"] = bh(d.loc[a, "p_iid"].values); d.loc[a, "p_block_bh"] = bh(d.loc[a, "p_block"].values)
    d = d[["domain", "unit", "n", "S", "p_iid", "p_block", "p_iid_bh", "p_block_bh"]]
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True); d.to_csv(out, index=False)
    print(f"total run time {time.time() - t0:.0f}s; wrote {out}")
    ad = d[a].sort_values("p_iid")
    print(ad.round(3).to_string(index=False))
    print(f"\nrejection rates (B_aid={B_AID}, B_sim={B_SIM}; iid / block)")
    for dz in SIZE_DESIGNS + POWER_DESIGNS:
        z = d[d.domain == dz]
        if len(z) == 0: continue
        print(f"{dz:15s} n={len(z):3d}  5%: {rate(z, 'p_iid', .05):.3f} / {rate(z, 'p_block', .05):.3f}   "
              f"10%: {rate(z, 'p_iid', .10):.3f} / {rate(z, 'p_block', .10):.3f}")
