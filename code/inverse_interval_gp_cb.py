"""Pilot: inverse interval goal programming on central-bank decisions (ground-truth test).

Forward model (per month): the bank chooses a rate change d to minimise
    w_pi * dist(x(d), [T - b, T + b]) + w_s * |d|,   x(d) = x_t - gamma * d,
where x_t is the inflation measure. If w_pi * gamma > w_s the optimum is: hold when x_t is inside the band,
raise when x_t > T + b, cut when x_t < T - b (move to the band edge). Only the direction of decisions is used,
so gamma does not need to be known.
Inverse problem: choose (T, b >= 0) minimising the total hinge (suboptimality) violation of observed directions.
This is a linear program. Ground truth: published inflation targets.
"""
import numpy as np, pandas as pd, json
from scipy.optimize import linprog

WINDOWS = [  # country, start, end, stated target (CPI-based or midpoint of band), note
    ("GB", "2004-01", "2019-12", 2.0, "BoE CPI 2%"),
    ("CA", "1996-01", "2019-12", 2.0, "BoC 2% midpoint of 1-3%"),
    ("NO", "2001-04", "2017-12", 2.5, "Norges Bank 2.5%"),
    ("SE", "1995-01", "2010-12", 2.0, "Riksbank 2%"),
    ("AU", "1994-01", "2019-12", 2.5, "RBA 2-3% (midpoint)"),
    ("MX", "2003-01", "2019-12", 3.0, "Banxico 3%"),
    ("CL", "2001-01", "2019-12", 3.0, "BCCh 3%"),
    ("IN", "2016-09", "2024-12", 4.0, "RBI 4%"),
    ("PL", "2004-01", "2019-12", 2.5, "NBP 2.5%"),
]
ZLB = 0.25          # months with the policy rate at or below this are dropped (cuts infeasible)
EPS = 0.01          # rate changes below this (pp) count as hold

def load():
    r = pd.read_csv("data/central_banks/policy_rate_monthly.csv.gz")
    c = pd.read_csv("data/central_banks/cpi_yoy_monthly.csv.gz")
    r = r.sort_values(["area", "period"]); r["d"] = r.groupby("area").policy_rate.diff()
    return r.merge(c, on=["period", "area"], how="inner")

def fit(x, dec, b_max=None):
    """x: inflation measure; dec in {-1,0,1}. Variables [T, b, xi_1..xi_n]; minimise sum xi."""
    n = len(x); A, ub = [], []
    def row(cT, cb, i, rhs):
        a = np.zeros(2 + n); a[0], a[1], a[2 + i] = cT, cb, -1.0; A.append(a); ub.append(rhs)
    for i, (xi, d) in enumerate(zip(x, dec)):
        if d == 1:   row(1, 1, i, xi)       # need x >= T + b   ->  T + b - x <= xi
        elif d == -1: row(-1, 1, i, -xi)    # need x <= T - b   ->  x - T + b <= xi
        else:
            row(-1, -1, i, -xi)             # need x <= T + b   ->  x - T - b <= xi
            row(1, -1, i, xi)               # need x >= T - b   ->  T - b - x <= xi
    c = np.r_[0, 0, np.ones(n)]
    bounds = [(-5, 15), (0, b_max)] + [(0, None)] * n
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(ub), bounds=bounds, method="highs")
    return res.x[0], res.x[1], res.fun / n

def profile_T(x, dec, grid):
    """Objective as a function of T (b re-optimised): gives a set estimate of T."""
    out = []
    for T in grid:
        best = np.inf
        for b in np.linspace(0, 4, 81):
            hi, lo = T + b, T - b
            v = np.where(dec == 1, np.maximum(0, hi - x), np.where(dec == -1, np.maximum(0, x - lo),
                         np.maximum(0, x - hi) + np.maximum(0, lo - x)))
            best = min(best, v.mean())
        out.append(best)
    return np.array(out)

def run(horizon=0, block=12, B=200, seed=0):
    df = load(); rng = np.random.default_rng(seed); rows = []
    for cc, s, e, tgt, note in WINDOWS:
        g = df[df.area == cc].sort_values("period").reset_index(drop=True)
        g["x"] = g.cpi_yoy.shift(-horizon) if horizon else g.cpi_yoy
        g = g[(g.period >= s) & (g.period <= e) & (g.policy_rate > ZLB)].dropna(subset=["x", "d"])
        dec = np.where(g.d > EPS, 1, np.where(g.d < -EPS, -1, 0)); x = g.x.values
        T, b, loss = fit(x, dec)
        grid = np.arange(-1, 8.001, 0.05); prof = profile_T(x, dec, grid)
        setT = grid[prof <= prof.min() + 0.02]                  # T values within 0.02 of the best loss
        bs = []                                                  # moving-block bootstrap
        n = len(x); nb = int(np.ceil(n / block))
        for _ in range(B):
            idx = np.concatenate([np.arange(k, k + block) for k in rng.integers(0, n - block, nb)])[:n]
            bs.append(fit(x[idx], dec[idx])[0])
        lo, hi = np.percentile(bs, [5, 95])
        rows.append(dict(country=cc, window=f"{s}..{e}", stated=tgt, T_hat=round(T, 2), b_hat=round(b, 2),
                         ci90=(round(lo, 2), round(hi, 2)), set_T=(round(setT.min(), 2), round(setT.max(), 2)),
                         n=n, hikes=int((dec == 1).sum()), cuts=int((dec == -1).sum()), mean_infl=round(x.mean(), 2),
                         loss=round(loss, 3), note=note))
    return pd.DataFrame(rows)

if __name__ == "__main__":
    res = {}
    for h in (0, 12):
        d = run(horizon=h); res[h] = d
        print(f"\n=== inflation measure: CPI y/y {'current' if h == 0 else f'{h} months ahead (perfect-foresight proxy)'} ===")
        print(d[["country", "stated", "T_hat", "ci90", "set_T", "b_hat", "mean_infl", "n", "hikes", "cuts"]].to_string(index=False))
        err = (d.T_hat - d.stated); naive = (d.mean_infl - d.stated)
        print(f"MAE(T_hat - stated) = {err.abs().mean():.2f};  MAE(mean inflation - stated) = {naive.abs().mean():.2f};  "
              f"corr(T_hat, stated) = {np.corrcoef(d.T_hat, d.stated)[0,1]:.2f}; corr(mean infl, stated) = {np.corrcoef(d.mean_infl, d.stated)[0,1]:.2f}")
    pd.concat([res[0].assign(horizon=0), res[12].assign(horizon=12)]).to_csv("results/inverse_interval_gp_cb.csv", index=False)
