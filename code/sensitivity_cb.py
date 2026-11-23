"""Sensitivity of the implied inflation targets (gradualism model, realised inputs, 9 exploratory + 5 confirmatory
banks) to: inflation horizon (2 or 6 quarters ahead instead of 4) and sample end (2015Q4 instead of 2019Q4).
One seed per fit (the main results used three)."""
import sys, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, migp_quad as Q
from multiprocessing import Pool
import real_cb_migp_k2 as R
from inverse_interval_gp_cb import WINDOWS, ZLB
from bootstrap_cb import CONF
R.ISO3.update({"IL": "ISR", "NZ": "NZL", "CO": "COL", "HU": "HUN", "TR": "TUR"})

def build_h(cc, h):
    q = R.build(cc)
    r = R.r_all[R.r_all.area == cc].set_index("period").policy_rate; c = R.c_all[R.c_all.area == cc].set_index("period").cpi_yoy
    df = pd.concat([r, c], axis=1).dropna(); df.index = pd.PeriodIndex(df.index, freq="M")
    qq = df.groupby(df.index.asfreq("Q")).last()
    q["x_pi"] = qq.cpi_yoy.shift(-(h - 1)).reindex(q.index)
    return q.dropna(subset=["x_pi"])

def task(a):
    spec, cc, q0, q1, tgt = a
    h = {"h2": 2, "h6": 6}.get(spec, 4)
    q = build_h(cc, h) if spec in ("h2", "h6") else R.build(cc)
    end = min(q1, pd.Period("2015Q4", "Q")) if spec == "end2015" else q1
    q = q[(q.index >= q0) & (q.index <= end) & (q.rate_start > ZLB)]
    if len(q) < 20: return dict(spec=spec, country=cc, stated=tgt, n=len(q), tau=np.nan, mean=np.nan)
    q = q.copy(); q["x_gap"] = q.growth - q.growth.mean()
    hh = Q.fit_hybrid(q[["x_pi", "x_gap"]].values, q.D.values, seed=0)
    return dict(spec=spec, country=cc, stated=tgt, n=len(q), tau=float(hh["tau"][0]), mean=float(q.x_pi.mean()))

if __name__ == "__main__":
    banks = [(cc, pd.Period(s, "M").asfreq("Q"), pd.Period(e, "M").asfreq("Q"), t) for cc, s, e, t, _ in WINDOWS]
    banks += [(cc, pd.Period(s, "Q"), pd.Period(e, "Q"), t) for cc, s, e, t in CONF]
    jobs = [(sp, cc, q0, q1, t) for sp in ("h2", "h6", "end2015") for cc, q0, q1, t in banks]
    with Pool(4) as p: out = pd.DataFrame(p.map(task, jobs, chunksize=1))
    out.to_csv("results/sensitivity_cb.csv", index=False)
    for sp, g in out.groupby("spec"):
        g = g.dropna(); off = g[(g["mean"] - g.stated).abs() > 0.5]
        print(sp, "n", len(g), "MAE tau", round((g.tau - g.stated).abs().mean(), 2), "MAE mean", round((g["mean"] - g.stated).abs().mean(), 2),
              "| off-target n", len(off), "closer", int(((off.tau - off.stated).abs() < (off["mean"] - off.stated).abs()).sum()))
