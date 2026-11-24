"""Placebo and misspecification experiments (one goal, direct control alpha = 1, exact estimator).
Data-generating processes (T = 60 decisions, AR(1) state with mean 2):
  gp      : interval goal program, band [1.5, 2.5], steps down 0.3 / up 0.4, Laplace noise 0.03
  coin    : Delta in {-0.3, 0, +0.4} at random, independent of x
  partial : partial adjustment Delta = 0.3 (2 - x) + noise
  qp      : a quadratic program solved per period, min (x + Delta - 2)^2 + 2 Delta^2 s.t. |Delta| <= 0.35
            (closed form: clip((2 - x)/3, -0.35, 0.35)) + noise
Diagnostics: in-sample gain over 'hold'; out-of-sample (last 30%) MAE of GP, linear partial adjustment (L1),
hold and mean change; width of the 2% near-optimal tau set from the exact profile; tau_hat vs the reference 2."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, exact_k1 as X
from multiprocessing import Pool
from scipy.optimize import linprog

def lad(x, y):
    """L1 regression y = a + b x (least absolute deviations) by linear programming."""
    n = len(x); c = np.r_[0, 0, np.ones(2 * n)]
    A = np.column_stack([np.ones(n), x, np.eye(n), -np.eye(n)])
    r = linprog(c, A_eq=A, b_eq=y, bounds=[(None, None)] * 2 + [(0, None)] * (2 * n), method="highs")
    return r.x[0], r.x[1]

def simulate(kind, T, rng):
    xs, ds = [], []; s = 2.0
    for t in range(T):
        s = 2.0 + 0.7 * (s - 2.0) + rng.normal(0, 0.6)
        if kind == "gp": d = -X.h(np.array([s]), 1.0, 2.5, 1.5, 0.3, 0.4)[0] + rng.laplace(0, 0.03)
        elif kind == "coin": d = rng.choice([-0.3, 0.0, 0.4])
        elif kind == "partial": d = 0.3 * (2.0 - s) + rng.laplace(0, 0.03)
        else: d = float(np.clip((2.0 - s) / 3.0, -0.35, 0.35)) + rng.laplace(0, 0.03)
        xs.append(s); ds.append(d); s = s + d
    return np.array(xs), np.array(ds)

def evaluate(x, d):
    """GP (exact) and alternatives on one series. Decisions are Delta; GP uses D = -Delta."""
    T = len(x); cut = int(0.7 * T)
    full = X.solve_fixed_alpha(x, -d, 1.0)
    tr = X.solve_fixed_alpha(x[:cut], -d[:cut], 1.0)
    pred_gp = -X.h(x[cut:], 1.0, tr["e_p"], tr["e_m"], tr["om_p"], tr["om_m"])
    a, b = lad(x[:cut], d[:cut]); pred_pa = a + b * x[cut:]
    aa, bb = lad(x, d)
    lo, hi, best, _ = X.tau_set_profile(x, -d, 1.0, 0.02, 0.01, x.min() - 0.3, x.max() + 0.3)
    return dict(tau_gp=full["tau"], b_gp=full["b"], tau_pa=(-aa / bb) if bb < -1e-6 else np.nan,
                gain_vs_hold=1 - full["loss"] / np.abs(d).mean(), set_width=hi - lo,
                oos_gp=np.abs(d[cut:] - pred_gp).mean(), oos_pa=np.abs(d[cut:] - pred_pa).mean(),
                oos_hold=np.abs(d[cut:]).mean(), oos_meanchg=np.abs(d[cut:] - np.median(d[:cut])).mean())

def job(args):
    kind, rep = args; rng = np.random.default_rng(10_000 * ["gp", "coin", "partial", "qp"].index(kind) + rep)
    x, d = simulate(kind, 60, rng); r = evaluate(x, d); r.update(kind=kind, rep=rep); return r

if __name__ == "__main__":
    jobs = [(k, r) for k in ("gp", "coin", "partial", "qp") for r in range(100)]
    with Pool(4) as p: out = pd.DataFrame(p.map(job, jobs, chunksize=2))
    out.to_csv("results/misspec_placebo.csv", index=False)
    g = out.groupby("kind")
    s = pd.DataFrame({"tau_gp_median": g.tau_gp.median(), "tau_gp_iqr": g.tau_gp.quantile(.75) - g.tau_gp.quantile(.25),
                      "tau_pa_median": g.tau_pa.median(), "gain_vs_hold": g.gain_vs_hold.median(), "set_width": g.set_width.median(),
                      "oos_gp": g.oos_gp.median(), "oos_pa": g.oos_pa.median(), "oos_hold": g.oos_hold.median(),
                      "gp_beats_pa": g.apply(lambda z: (z.oos_gp < z.oos_pa).mean()), "gp_beats_hold": g.apply(lambda z: (z.oos_gp < z.oos_hold).mean())})
    print(s.round(3).to_string())
