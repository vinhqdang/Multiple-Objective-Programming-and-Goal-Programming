"""Level-form Taylor rule with partial adjustment as a benchmark for the implied inflation target, on the same
14 central-bank windows and quarters as the gradualism fit (9 exploratory, 5 confirmatory).

Model: i_t = rho * i_{t-1} + (1 - rho) * (c + phi * pi_t + gamma * y_t) + e_t, with pi_t the inflation input of our
model (inflation 4 quarters ahead, x_pi) and y_t the growth gap. Estimated by NLS (scipy least_squares, several
starts, best cost kept) and by LAD (Nelder-Mead started from the NLS solution, restarted until stable).
Neutral real rate r* = window mean of (i_t - pi_t); implied target pi* = (c - r*) / (1 - phi), undefined if
|1 - phi| < 0.1 or rho >= 0.99.

Also: MAE tables against stated targets (14 banks and 13 without Turkey), and a comparison of the official
tolerance band half-width with our fitted inflation band half-width b (stored as b_pi in results/real_cb_quad.csv
and results/confirmatory_cb.csv; already in inflation units, since b = d/alpha in migp_quad).
Writes results/cb_level_taylor.csv (one row per bank).
"""
import sys, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from scipy.optimize import least_squares, minimize
from scipy.stats import spearmanr
from bootstrap_cb import data, CONF
from inverse_interval_gp_cb import WINDOWS, ZLB
import real_cb_migp_k2 as R

OUT = "results/cb_level_taylor.csv"
BOUNDS = ([-1.0, -30.0, -10.0, -10.0], [1.2, 40.0, 10.0, 10.0])   # rho, c, phi, gamma


def sample(cc, q0, q1):
    """Same filter as bootstrap_cb.data (window, ZLB), keeping the policy-rate level and its lag."""
    q = R.build(cc); q = q[(q.index >= q0) & (q.index <= q1) & (q.rate_start > ZLB)].copy()
    q["x_gap"] = q.growth - q.growth.mean()
    X, D = data(cc, q0, q1)
    assert np.allclose(X[:, 0], q.x_pi.values) and np.allclose(X[:, 1], q.x_gap.values) and np.allclose(D, q.D.values)
    assert np.allclose(q.D.values, (q.policy_rate - q.rate_start).values)
    return q


def resid(p, i, il, pi, y):
    rho, c, phi, gam = p
    return i - (rho * il + (1 - rho) * (c + phi * pi + gam * y))


def fit_nls(i, il, pi, y):
    best = None
    for rho0 in (0.2, 0.6, 0.9):
        for phi0 in (0.5, 1.5, 2.5):
            p0 = np.array([rho0, np.mean(i) - phi0 * np.mean(pi), phi0, 0.1])
            r = least_squares(resid, p0, args=(i, il, pi, y), bounds=BOUNDS)
            if best is None or r.cost < best.cost:
                best = r
    return best.x, 2 * best.cost                       # sum of squared residuals


def fit_lad(p0, i, il, pi, y):
    obj = lambda p: np.abs(resid(p, i, il, pi, y)).sum()
    p = np.asarray(p0, float); val = obj(p)
    for _ in range(5):
        r = minimize(obj, p, method="Nelder-Mead",
                     options=dict(maxiter=40000, maxfev=40000, xatol=1e-9, fatol=1e-12, adaptive=True))
        if r.fun < val - 1e-12:
            p, val = r.x, r.fun
        else:
            break
    return p, val                                      # sum of absolute residuals


def target(p, rstar):
    rho, c, phi, gam = p
    reasons = []
    if abs(1 - phi) < 0.1: reasons.append("|1-phi|<0.1")
    if rho >= 0.99: reasons.append("rho>=0.99")
    raw = (c - rstar) / (1 - phi) if abs(1 - phi) > 1e-12 else np.nan
    ok = not reasons
    return (raw if ok else np.nan), ok, ("defined" if ok else "; ".join(reasons)), raw


def band_for(cc, start, end, bands):
    """Band (low, high) with the largest overlap with the window (bands with the same limits are pooled)."""
    d = bands[(bands.country == cc) & bands.band_low.notna() & bands.band_high.notna()]
    W = (end - start).total_seconds(); best = None
    for (lo, hi), g in d.groupby(["band_low", "band_high"]):
        ov = 0.0
        for _, r in g.iterrows():
            fr = pd.to_datetime(r.from_date, errors="coerce"); to = pd.to_datetime(r.to_date, errors="coerce")
            fr = fr if pd.notna(fr) else pd.Timestamp.min; to = to if pd.notna(to) else pd.Timestamp.max
            ov += max(0.0, (min(end, to) - max(start, fr)).total_seconds())
        cov = min(ov, W) / W
        if best is None or cov > best[3]:
            best = (lo, hi, (hi - lo) / 2, cov)
    return best  # None if no band rows


# ---------------------------------------------------------------- windows and our fit
ex = pd.read_csv("results/real_cb_quad.csv"); ex = ex[ex.input == "realised"].set_index("country")
cf = pd.read_csv("results/confirmatory_cb.csv"); cf = cf[cf.status == "included"].set_index("country")
bm = pd.read_csv("results/cb_benchmarks.csv").set_index("country")
tg_ex = pd.read_csv("data/central_banks/targets.csv"); tg_cf = pd.read_csv("data/central_banks/targets_confirmatory.csv")

jobs = []
for cc, s, e, tgt, _ in WINDOWS:
    q0, q1 = pd.Period(s, "M").asfreq("Q"), pd.Period(e, "M").asfreq("Q")
    jobs.append(("exploratory", cc, q0, q1, tgt, pd.Period(s, "M").start_time, pd.Period(e, "M").end_time,
                 ex.loc[cc, "tau_pi"], ex.loc[cc, "b_pi"], tg_ex))
for cc, q0s, q1s, tgt in CONF:
    q0, q1 = pd.Period(q0s, "Q"), pd.Period(q1s, "Q")
    jobs.append(("confirmatory", cc, q0, q1, tgt, q0.start_time, q1.end_time,
                 cf.loc[cc, "tau_pi"], cf.loc[cc, "b_pi"], tg_cf))

rows = []
for sname, cc, q0, q1, tgt, wstart, wend, implied, b_ours, tg in jobs:
    q = sample(cc, q0, q1)
    i, il, pi, y = q.policy_rate.values, q.rate_start.values, q.x_pi.values, q.x_gap.values
    rstar = float(np.mean(i - pi)); mean_infl = float(np.mean(pi))
    p_nls, ssr = fit_nls(i, il, pi, y)
    p_lad, sae = fit_lad(p_nls, i, il, pi, y)
    pn, okn, rn, rawn = target(p_nls, rstar)
    pl, okl, rl, rawl = target(p_lad, rstar)
    dt = bm.loc[cc, "taylor"] if bm.loc[cc, "b_pi"] > 1e-6 else np.nan   # cb_benchmarks.csv difference-Taylor rule
    band = band_for(cc, wstart, wend, tg)
    row = dict(sample=sname, country=cc, stated=tgt, window=f"{q0}-{q1}", n=len(q), implied_ours=implied,
               mean_infl=round(mean_infl, 3), rstar=round(rstar, 3),
               nls_rho=p_nls[0], nls_c=p_nls[1], nls_phi=p_nls[2], nls_gamma=p_nls[3], nls_ssr=ssr,
               nls_pi_star=pn, nls_defined=okn, nls_reason=rn, nls_pi_star_raw=rawn,
               lad_rho=p_lad[0], lad_c=p_lad[1], lad_phi=p_lad[2], lad_gamma=p_lad[3], lad_sae=sae,
               lad_pi_star=pl, lad_defined=okl, lad_reason=rl, lad_pi_star_raw=rawl,
               diff_taylor=dt)
    row["taylor_or_mean"] = pn if okn else mean_infl                   # level NLS, mean where undefined
    row["taylor_or_mean_lad"] = pl if okl else mean_infl               # level LAD
    row["taylor_or_mean_diff"] = dt if not np.isnan(dt) else mean_infl # difference Taylor (cb_benchmarks.csv)
    row["official_band_low"] = band[0] if band else np.nan
    row["official_band_high"] = band[1] if band else np.nan
    row["official_coverage"] = round(band[3], 3) if band else np.nan
    hw = band[2] if (band and band[3] >= 0.5) else np.nan            # band must cover most of the window
    row["official_halfwidth"] = hw
    row["our_b"] = b_ours
    row["hw_over_our_b"] = hw / b_ours if (not np.isnan(hw) and b_ours > 0) else np.nan
    row["hw_in_0.5b_2b"] = (0.5 * b_ours <= hw <= 2 * b_ours) if not np.isnan(hw) else np.nan
    rows.append(row)

d = pd.DataFrame(rows)
d.round(4).to_csv(OUT, index=False)

# ---------------------------------------------------------------- printed tables
pd.set_option("display.width", 250)
print("== Per bank: stated, implied (ours), level-Taylor NLS and LAD ==")
t1 = d[["sample", "country", "stated", "implied_ours", "mean_infl", "rstar", "nls_pi_star", "nls_phi", "nls_rho",
        "nls_defined", "lad_pi_star", "lad_phi", "lad_rho", "lad_defined", "diff_taylor"]].copy()
print(t1.round(3).to_string(index=False))
print("\nReasons (NLS | LAD):")
for _, r in d.iterrows():
    print(f"  {r.country}: NLS {r.nls_reason} | LAD {r.lad_reason}")

E = lambda v, s: float(np.mean(np.abs(v - s)))
methods = {
    "our implied target": d.implied_ours,
    "mean inflation": d.mean_infl,
    "constant 2.5": pd.Series(2.5, index=d.index),
    "difference-Taylor-or-mean": d.taylor_or_mean_diff,
    "level-Taylor-or-mean (NLS)": d.taylor_or_mean,
    "level-Taylor-or-mean (LAD)": d.taylor_or_mean_lad,
}
print("\n== MAE vs stated target ==")
mask13 = d.country != "TR"
out = []
for name, v in methods.items():
    out.append(dict(method=name, MAE_14=round(E(v, d.stated), 3), MAE_13_excl_TR=round(E(v[mask13], d.stated[mask13]), 3)))
mae = pd.DataFrame(out); print(mae.to_string(index=False))
print(f"Taylor defined (NLS) {int(d.nls_defined.sum())}/14, (LAD) {int(d.lad_defined.sum())}/14, "
      f"(difference rule) {int(d.diff_taylor.notna().sum())}/14")

print("\n== Official tolerance band vs our fitted inflation band half-width b ==")
bt = d[["country", "window", "official_band_low", "official_band_high", "official_coverage", "official_halfwidth",
        "our_b", "hw_over_our_b", "hw_in_0.5b_2b"]]
print(bt.round(3).to_string(index=False))
ok = d.official_halfwidth.notna()
print(f"banks with official band covering >=50% of window: {int(ok.sum())} of 14")
print("in [0.5b, 2b]:", int((d.loc[ok, 'hw_in_0.5b_2b'] == True).sum()), "of", int(ok.sum()),
      "| excluded (no band covering most of window):", list(d.country[~ok]))
both = d[ok & d.our_b.notna()]
rho_s, p_s = spearmanr(both.official_halfwidth, both.our_b)
print(f"Spearman(official half-width, our b) n={len(both)}: rho={rho_s:.3f}, p={p_s:.3f}")
