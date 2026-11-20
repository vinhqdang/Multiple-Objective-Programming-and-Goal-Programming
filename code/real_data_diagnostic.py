"""Diagnostic: can World Bank country data support learning goal-programming coefficients?
Country-specific slopes of each outcome on social spending (health + education, % GDP) are computed
for 2000-2009 and 2010-2019. We report how stable they are and how well features predict them.
These slopes are associations, not causal effects."""
import numpy as np, pandas as pd
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import cross_val_predict
GOALS = ["life_exp", "child_surv", "sec_enrol", "prim_compl"]
df = pd.read_csv("data/worldbank_countries_2000_2023.csv")
df["child_surv"] = 1000 - df["u5_mort"]; df["social"] = df["edu_exp_gdp"] + df["health_exp_gdp"]
def slopes(a, b):
    out = {}
    for iso, g in df[(df.year >= a) & (df.year <= b)].groupby("iso3"):
        row = {}
        for k in GOALS:
            h = g[["social", k]].dropna()
            row[k] = np.polyfit(h.social, h[k], 1)[0] if len(h) >= 6 and h.social.std() > 1e-6 else np.nan
        out[iso] = row
    return pd.DataFrame(out).T
tr, te = slopes(2000, 2009), slopes(2010, 2019)
f = df[df.year == 2009].set_index("iso3")
feat = pd.DataFrame({"lgdp": np.log(f.gdp_pc_ppp), "lpop": np.log(f["pop"]), "urban": f.urban, "dep": f.dependency,
                     "social": f.social, **{k: f[k] for k in GOALS}})
base = pd.concat([feat, tr.add_suffix("_tr"), te.add_suffix("_te")], axis=1)
fc = ["lgdp", "lpop", "urban", "dep", "social"]
print("countries with all goals and both windows:", len(base.dropna()))
for k in GOALS:
    d = base[fc + [k + "_tr", k + "_te", k]].dropna()
    X = ((d[fc + [k]] - d[fc + [k]].mean()) / d[fc + [k]].std()).values
    ytr, yte = d[k + "_tr"].clip(lower=0).values, d[k + "_te"].clip(lower=0).values
    p = cross_val_predict(RidgeCV(alphas=np.logspace(-1, 3, 12)), X, ytr, cv=5)
    print(f"{k}: n={len(d)} CV corr(pred, train slope)={np.corrcoef(p, ytr)[0,1]:.2f} | "
          f"pred vs test slope={np.corrcoef(p, yte)[0,1]:.2f} | raw train vs test slope={np.corrcoef(ytr, yte)[0,1]:.2f}")
