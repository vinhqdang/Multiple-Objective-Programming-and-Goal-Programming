"""Placebo grid: interval goal program (gp) and random 'coin flip' behaviour (coin) over noise scale x T.
DGP mirrors misspec_placebo.simulate (AR(1) state, mean 2, coefficient 0.7, sd 0.6; gp band [1.5, 2.5] with steps
down 0.3 / up 0.4; coin Delta in {-0.3, 0, +0.4} at random), with the Laplace noise scale as a grid variable
(misspec_placebo uses 0.03 throughout; for coin the same Laplace noise is added to the random step).
Per-series diagnostics follow misspec_placebo.evaluate (in-sample gain over holding, out-of-sample comparison with
holding on the last 30% of the series, tau of the exact estimator), with one change for speed: the width of the
near-optimal tau set is the candidate-set version exact_k1.tau_set (2% tolerance) instead of the tau-grid profile
exact_k1.tau_set_profile (step 0.01), which costs about 25 s per T = 60 series. The two were compared on a small
validation sample (see the report). Pool(2)."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, exact_k1 as X, misspec_placebo as M
from multiprocessing import Pool

BEHAV, NOISE, TS, REPS, TRUE_TAU = ("gp", "coin"), (0.03, 0.1, 0.2), (30, 60, 120), 100, 2.0

def simulate(kind, T, scale, rng):
    xs, ds = [], []; s = 2.0
    for t in range(T):
        s = 2.0 + 0.7 * (s - 2.0) + rng.normal(0, 0.6)
        if kind == "gp": d = -X.h(np.array([s]), 1.0, 2.5, 1.5, 0.3, 0.4)[0] + rng.laplace(0, scale)
        else: d = rng.choice([-0.3, 0.0, 0.4]) + rng.laplace(0, scale)
        xs.append(s); ds.append(d); s = s + d
    return np.array(xs), np.array(ds)

def evaluate(x, d):
    """As misspec_placebo.evaluate, with the candidate-set width of the near-optimal tau set."""
    T = len(x); cut = int(0.7 * T)
    full = X.solve_fixed_alpha(x, -d, 1.0)
    tr = X.solve_fixed_alpha(x[:cut], -d[:cut], 1.0)
    pred_gp = -X.h(x[cut:], 1.0, tr["e_p"], tr["e_m"], tr["om_p"], tr["om_m"])
    lo, hi, _ = X.tau_set(x, -d, 1.0, 0.02)
    return dict(tau_gp=full["tau"], gain_vs_hold=1 - full["loss"] / np.abs(d).mean(), set_width=hi - lo,
                oos_gp=np.abs(d[cut:] - pred_gp).mean(), oos_hold=np.abs(d[cut:]).mean())

def job(args):
    kind, scale, T, rep = args
    seed = ((BEHAV.index(kind) * len(NOISE) + NOISE.index(scale)) * len(TS) + TS.index(T)) * 1000 + rep
    x, d = simulate(kind, T, scale, np.random.default_rng(seed))
    r = evaluate(x, d); r.update(kind=kind, noise=scale, T=T, rep=rep); return r

if __name__ == "__main__":
    import time; t0 = time.time()
    jobs = [(k, s, T, r) for k in BEHAV for s in NOISE for T in TS for r in range(REPS)]
    with Pool(2) as p: out = pd.DataFrame(p.map(job, jobs, chunksize=2))
    out["gp_beats_hold"] = out.oos_gp < out.oos_hold
    out["abs_err_tau"] = np.where(out.kind == "gp", (out.tau_gp - TRUE_TAU).abs(), np.nan)
    g = out.groupby(["kind", "noise", "T"])
    s = pd.DataFrame({"n_series": g.size(), "mean_gain_vs_hold": g.gain_vs_hold.mean(),
                      "median_set_width": g.set_width.median(), "share_width_lt_1": g.set_width.apply(lambda z: (z < 1).mean()),
                      "share_gp_beats_hold_oos": g.gp_beats_hold.mean(),
                      "median_abs_err_tau": g.abs_err_tau.median(), "median_tau_gp": g.tau_gp.median()}).reset_index()
    s.to_csv("results/placebo_grid.csv", index=False)
    print(s.round(4).to_string(index=False))
    print(f"elapsed {time.time() - t0:.1f} s")
