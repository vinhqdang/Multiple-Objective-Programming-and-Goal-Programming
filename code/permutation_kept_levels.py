"""Size of the state-dependence permutation test when the decisions are permuted but the observed levels x_t are kept.
Design of the size study in permutation_test.py (calib_job): 200 series of 60 decisions, independent,
d = choice({-0.03, 0, 0.04}) + Laplace(0, 0.005), levels x = rebuild(0.4, d) (so x_{t+1} = x_t + d_t), data seed
50000 + rep, permutation seed 9000 + rep, B = 199.
Kept-levels variant: the null samples permute d and keep x fixed (levels are not rebuilt from the permuted
decisions). The statistic is the in-sample gain over hold of the exact fit, as in permutation_test.gain.
Because the permutation RNG draws are the same as in permutation_test.ptest, the rebuilt-levels p-values from
results/permutation_test.csv (calibration rows) are a paired reference; their observed gains are checked to match.
Writes results/permutation_kept_levels.csv (summary) and results/permutation_kept_levels_series.csv (per series)."""
import sys; sys.path.insert(0, "code")
import os, numpy as np, pandas as pd, permutation_test as P
from multiprocessing import Pool

B, N_SERIES, T = 199, 200, 60
SERIES_CSV = "results/permutation_kept_levels_series.csv"

def job(rep):
    rng = np.random.default_rng(50_000 + rep)
    d = rng.choice([-0.03, 0.0, 0.04], size=T) + rng.laplace(0, 0.005, T)
    x = P.rebuild(0.4, d)                                  # observed levels, kept fixed in the null
    prng = np.random.default_rng(9_000 + rep); g0 = P.gain(x, d)
    null = np.empty(B)
    for i in range(B):
        dp = prng.permutation(d); null[i] = P.gain(x, dp)  # permute decisions only
    p = (1 + (null >= g0).sum()) / (B + 1)
    return dict(rep=rep, gain=g0, null95=np.percentile(null, 95), p=p)

if __name__ == "__main__":
    import time; t0 = time.time()
    if os.path.exists(SERIES_CSV): os.remove(SERIES_CSV)
    rows, header = [], True
    with Pool(3) as pool:
        for r in pool.imap_unordered(job, range(N_SERIES), chunksize=1):
            pd.DataFrame([r]).to_csv(SERIES_CSV, mode="a", header=header, index=False); header = False; rows.append(r)
    s = pd.DataFrame(rows).sort_values("rep").reset_index(drop=True)
    ref = pd.read_csv("results/permutation_test.csv"); ref = ref[ref.domain == "calibration"].sort_values("unit")
    ref_match = np.allclose(ref.gain.values, s.gain.values, atol=1e-9)
    print("observed gains match permutation_test.csv calibration rows:", ref_match, flush=True)
    summ = []
    for name, p in (("kept_levels", s.p.values), ("rebuilt_levels_reference", ref.p.values)):
        summ.append(dict(variant=name, n_series=len(p), n_obs=T, B=B, reject_5=round((p <= 0.05).mean(), 3),
                         reject_10=round((p <= 0.10).mean(), 3), mean_p=round(p.mean(), 3)))
    out = pd.DataFrame(summ); out.to_csv("results/permutation_kept_levels.csv", index=False)
    print(out.to_string(index=False))
    print(f"elapsed {time.time() - t0:.1f} s")
