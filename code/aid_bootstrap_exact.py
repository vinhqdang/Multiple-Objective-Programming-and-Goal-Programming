"""Moving-block bootstrap of the exact one-goal tau for each aid donor (alpha = 1, as in aid_exact.py).
For each donor the (x_t, delta_t) pairs are resampled in moving blocks of 5 consecutive years: a series of the
original length is built from randomly started blocks of 5 consecutive pairs (pairs are kept, levels are not rebuilt),
and the exact estimator solve_fixed_alpha is refit with D = -delta. B = 200 replications, fixed seed per donor
(1000 + index of the donor in sorted order). The 2% near-optimal set is read from results/aid_exact.csv (profile set,
truncated at 0). Writes results/aid_bootstrap_exact.csv."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, exact_k1 as X, aid_profile as A
from multiprocessing import Pool

B, BLOCK = 200, 5

def block_index(n, rng):
    """Row indices of a moving-block resample of length n (blocks of BLOCK consecutive rows, drawn with replacement)."""
    starts = rng.integers(0, n - BLOCK + 1, int(np.ceil(n / BLOCK)))
    return np.concatenate([np.arange(s, s + BLOCK) for s in starts])[:n]

def boot_job(args):
    donor, g, seed = args
    x, D = g.x.values, -g.delta.values; n = len(x); rng = np.random.default_rng(seed)
    taus = np.empty(B)
    for b in range(B):
        i = block_index(n, rng)
        taus[b] = X.solve_fixed_alpha(x[i], D[i], 1.0)["tau"]
    return donor, taus

if __name__ == "__main__":
    data = A.data(); donors = sorted(data)
    ref = pd.read_csv("results/aid_exact.csv").set_index("donor")
    assert set(ref.index) == set(donors) and len(donors) == 23, "donor set differs from aid_exact.csv"
    jobs = [(d, data[d], 1000 + i) for i, d in enumerate(donors)]
    with Pool(3) as pool: res = dict(pool.map(boot_job, jobs, chunksize=1))
    rows = []
    for d in donors:
        g = data[d]; x, D = g.x.values, -g.delta.values
        tau_hat = X.solve_fixed_alpha(x, D, 1.0)["tau"]
        lo_raw, hi_raw = [float(v) for v in ref.loc[d, "set2"].strip("[]").split(",")]
        lo, hi = max(lo_raw, 0.0), max(hi_raw, 0.0)
        q05, q50, q95 = np.quantile(res[d], [0.05, 0.5, 0.95])
        bw, sw = q95 - q05, hi - lo
        rows.append(dict(donor=d, n=len(x), tau_hat=round(tau_hat, 3), boot_q05=round(q05, 3), boot_q50=round(q50, 3),
                         boot_q95=round(q95, 3), set2_lo=round(lo, 2), set2_hi=round(hi, 2),
                         boot90_width=round(bw, 3), set2_width=round(sw, 3), width_ratio_set2_to_boot=round(sw / bw, 3),
                         set2_narrower_than_boot90=bool(sw < bw),
                         set2_inside_boot90=bool(lo >= q05 and hi <= q95),
                         set2_overlaps_boot90=bool(lo <= q95 and hi >= q05)))
        print(rows[-1], flush=True)
    out = pd.DataFrame(rows)
    out.to_csv("results/aid_bootstrap_exact.csv", index=False)
    print("donors:", len(out), " set2 narrower than boot90:", int(out.set2_narrower_than_boot90.sum()),
          " median width ratio:", round(out.width_ratio_set2_to_boot.median(), 3))
