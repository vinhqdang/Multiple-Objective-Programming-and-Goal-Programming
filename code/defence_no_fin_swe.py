"""Defence spending (NATO definition, % of GDP): point fits of defence_exact.py with Finland and Sweden excluded.
Same panel construction (defence_exact.load), same two periods, same exact one-goal estimator (alpha = 1,
D = -Delta) and same output columns as results/defence_exact.csv. Before the excluded fit, the full-sample fit is
recomputed and checked against results/defence_exact.csv. Writes results/defence_no_fin_swe.csv."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd
import defence_exact as DE

EXCLUDE = ["Finland", "Sweden"]

def rows_for(q, label):
    out = []
    for a0, a1 in DE.PERIODS:
        g = q[(q.year >= a0) & (q.year <= a1)]; r = DE.fit(g); x = g.x.values
        out.append(dict(period=f"{a0}-{a1}", n=len(g), loss=round(r["loss"], 4), tau=round(r["tau"], 3), b=round(r["b"], 3),
                        band_lo=round(r["e_m"], 2), band_hi=round(r["e_p"], 2), step_cut=round(r["om_p"], 2),
                        step_raise=round(r["om_m"], 2), mean_level=round(x.mean(), 3),
                        share_above_hi=round((x > r["e_p"]).mean(), 3), share_below_lo=round((x < r["e_m"]).mean(), 3)))
    return pd.DataFrame(out)

if __name__ == "__main__":
    q = DE.load()
    full = rows_for(q, "full")
    ref = pd.read_csv("results/defence_exact.csv")
    same = full.drop(columns=[]).astype(str).values.tolist() == ref.astype(str).values.tolist()
    print("full-sample recomputation matches results/defence_exact.csv:", same, flush=True)
    print(full.to_string(index=False))
    sub = q[~q.country.isin(EXCLUDE)]
    print("excluded:", sorted(set(q.country) & set(EXCLUDE)), " countries kept:", sub.country.nunique(), flush=True)
    out = rows_for(sub, "no_fin_swe")
    out.to_csv("results/defence_no_fin_swe.csv", index=False)
    print(out.to_string(index=False))
