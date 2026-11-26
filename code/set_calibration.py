"""Calibration of the 2% and 5% near-optimal tau sets under the interval goal-program DGP (true tau = 2.0).
Series come from placebo_grid.simulate("gp", T, scale, rng) with scale in {0.03, 0.1, 0.2} and T in {30, 60, 120},
100 series per cell, deterministic seeds. For each series:
  - profile sets: aid_profile.run (the function that produced set2/set5 in results/aid_exact.csv: exact profile loss on
    a 0.01 tau grid over [min x - 0.3, max x + 0.3]). Computed for T = 30 and 60 only: at T = 120 one profile
    evaluation costs about 0.6 s, i.e. about 4 min per series, which is too slow for 300 series.
  - candidate sets: exact_k1.tau_set (candidate-set version), computed for every T.
Each cell is reported with the method used in a `set_method` column. Per-series rows are appended to
results/set_calibration_series.csv as they finish; the cell summary is written to results/set_calibration.csv."""
import sys; sys.path.insert(0, "code")
import os, numpy as np, pandas as pd, exact_k1 as X, placebo_grid as PG, aid_profile as A
from multiprocessing import Pool

TRUE_TAU, SCALES, TS, REPS, PROFILE_MAX_T = 2.0, (0.03, 0.1, 0.2), (30, 60, 120), 100, 60
SERIES_CSV = "results/set_calibration_series.csv"

def parse_set(s):
    lo, hi = s.strip("[]").split(","); return float(lo), float(hi)

def job(args):
    scale, T, rep = args
    seed = 1_000_000 + 100_000 * SCALES.index(scale) + 1_000 * TS.index(T) + rep
    x, d = PG.simulate("gp", T, scale, np.random.default_rng(seed))
    row = dict(noise=scale, T=T, rep=rep, seed=seed, tau_hat=X.solve_fixed_alpha(x, -d, 1.0)["tau"])
    for rel in (0.02, 0.05):
        k = int(rel * 100); lo, hi, _ = X.tau_set(x, -d, 1.0, rel)
        row[f"cand{k}_lo"], row[f"cand{k}_hi"] = lo, hi
    if T <= PROFILE_MAX_T:
        out = A.run(("sim", pd.DataFrame({"x": x, "delta": d})))
        for k in (2, 5):
            lo, hi = parse_set(out[f"set{k}"]); row[f"prof{k}_lo"], row[f"prof{k}_hi"] = lo, hi
            row[f"prof{k}_contig"] = out[f"contig{k}"]
    print(noise_tag(row), flush=True)
    return row

def noise_tag(r):
    return f"noise={r['noise']} T={r['T']} rep={r['rep']} tau_hat={r['tau_hat']:.3f}"

def summarise(s):
    out = []
    for (scale, T), g in s.groupby(["noise", "T"]):
        for method, pre in (("profile_grid0.01", "prof"), ("candidate_tau_set", "cand")):
            if f"{pre}2_lo" not in g or g[f"{pre}2_lo"].isna().all(): continue
            z = g.dropna(subset=[f"{pre}2_lo"]); row = dict(noise=scale, T=T, set_method=method, n_series=len(z))
            for k in (2, 5):
                lo, hi = z[f"{pre}{k}_lo"], z[f"{pre}{k}_hi"]
                cov = (lo <= TRUE_TAU) & (TRUE_TAU <= hi)
                row[f"coverage{k}"] = round(cov.mean(), 3)
                row[f"median_width{k}"] = round((hi - lo).median(), 3)
                row[f"mean_width{k}"] = round((hi - lo).mean(), 3)
            row["median_tau_hat"] = round(z.tau_hat.median(), 3)
            row["median_abs_err_tau"] = round((z.tau_hat - TRUE_TAU).abs().median(), 3)
            out.append(row)
    return pd.DataFrame(out)

if __name__ == "__main__":
    import time; t0 = time.time()
    jobs = [(s, T, r) for s in SCALES for T in TS for r in range(REPS)]
    # Profile jobs (T <= 60) are the expensive ones: schedule them first.
    jobs.sort(key=lambda j: -j[1])
    if os.path.exists(SERIES_CSV): os.remove(SERIES_CSV)
    rows, header = [], True
    with Pool(3) as p:
        for row in p.imap_unordered(job, jobs, chunksize=1):
            pd.DataFrame([row]).to_csv(SERIES_CSV, mode="a", header=header, index=False); header = False
            rows.append(row)
    s = pd.DataFrame(rows).sort_values(["noise", "T", "rep"]).reset_index(drop=True)
    summ = summarise(s).sort_values(["noise", "T", "set_method"]).reset_index(drop=True)
    summ.to_csv("results/set_calibration.csv", index=False)
    print(summ.to_string(index=False))
    print(f"elapsed {time.time() - t0:.1f} s")
