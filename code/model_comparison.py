"""Out-of-sample comparison of behavioural models on the real data.
Models: goal programming (exact one-goal for aid and defence; gradualism hybrid for central banks), linear partial
adjustment / difference Taylor rule fitted by least absolute deviations, 'hold' and median change.
Aid: per donor, train on the first 70% of years, test on the rest. Defence: 5-fold cross-validation over allies
within each period. Central banks: per bank, first 70% of quarters vs the rest. Also reports the partial-adjustment
implied target -a/b for donors with verified national goals."""
import sys, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, exact_k1 as X, migp_quad as Q
from multiprocessing import Pool
from misspec_placebo import lad
from applications_gp import panel

def aid_rows():
    import aid_profile as A
    rows = []
    for donor, g in A.data().items():
        x, d = g.x.values, g.delta.values; T = len(x); cut = int(0.7 * T)
        tr = X.solve_fixed_alpha(x[:cut], -d[:cut], 1.0)
        p_gp = -X.h(x[cut:], 1.0, tr["e_p"], tr["e_m"], tr["om_p"], tr["om_m"])
        a, b = lad(x[:cut], d[:cut]); aa, bb = lad(x, d)
        rows.append(dict(domain="aid", unit=donor, n_test=T - cut, gp=np.abs(d[cut:] - p_gp).mean(), pa=np.abs(d[cut:] - a - b * x[cut:]).mean(),
                         hold=np.abs(d[cut:]).mean(), medchg=np.abs(d[cut:] - np.median(d[:cut])).mean(),
                         tau_pa=(-aa / bb) if bb < -1e-6 else np.nan))
    return rows

def defence_rows():
    n = pd.read_csv("data/cofog/nato_defence_pc_gdp.csv.gz").rename(columns={"defence_pc_gdp": "v"})
    n = n[~n.country.str.contains("NATO|Europe|Canada and", case=False, regex=True) | (n.country == "Canada")].dropna(subset=["v"])
    p = panel(n, "country", "v"); rows = []
    for lab, (a0, a1) in {"2015-2021": (2015, 2021), "2022-2025": (2022, 2025)}.items():
        g = p[(p.year >= a0) & (p.year <= a1)]; cs = np.array(sorted(g.country.unique())); rng = np.random.default_rng(0); rng.shuffle(cs)
        err = {"gp": [], "pa": [], "hold": [], "medchg": []}
        for f in range(5):
            test = set(cs[f::5]); tr, te = g[~g.country.isin(test)], g[g.country.isin(test)]
            s = X.solve_fixed_alpha(tr.x.values, -tr.delta.values, 1.0)
            pg = -X.h(te.x.values, 1.0, s["e_p"], s["e_m"], s["om_p"], s["om_m"]); a, b = lad(tr.x.values, tr.delta.values)
            err["gp"] += list(np.abs(te.delta.values - pg)); err["pa"] += list(np.abs(te.delta.values - a - b * te.x.values))
            err["hold"] += list(np.abs(te.delta.values)); err["medchg"] += list(np.abs(te.delta.values - np.median(tr.delta.values)))
        rows.append(dict(domain="defence", unit=lab, n_test=len(err["gp"]), **{k: float(np.mean(v)) for k, v in err.items()}))
    return rows

def cb_job(args):
    import real_cb_migp_k2 as R
    from bootstrap_cb import data
    cc, q0, q1 = args
    Xc, D = data(cc, q0, q1); T = len(D); cut = int(0.7 * T)
    h = Q.fit_hybrid(Xc[:cut], D[:cut], seed=0)
    pg = Q.forward_batch(Xc[cut:], h["alpha"], h["tau"], h["b"], h["omega_p"], h["omega_m"])
    A = np.column_stack([np.ones(cut), Xc[:cut]])
    from scipy.optimize import linprog
    n = cut; c = np.r_[np.zeros(3), np.ones(2 * n)]; Aeq = np.column_stack([A, np.eye(n), -np.eye(n)])
    co = linprog(c, A_eq=Aeq, b_eq=D[:cut], bounds=[(None, None)] * 3 + [(0, None)] * (2 * n), method="highs").x[:3]
    pt = co[0] + Xc[cut:] @ co[1:]
    return dict(domain="central bank", unit=cc, n_test=T - cut, gp=np.abs(D[cut:] - pg).mean(), pa=np.abs(D[cut:] - pt).mean(),
                hold=np.abs(D[cut:]).mean(), medchg=np.abs(D[cut:] - np.median(D[:cut])).mean())

if __name__ == "__main__":
    from inverse_interval_gp_cb import WINDOWS
    from bootstrap_cb import CONF
    rows = aid_rows() + defence_rows()
    banks = [(cc, pd.Period(s, "M").asfreq("Q"), pd.Period(e, "M").asfreq("Q")) for cc, s, e, t, _ in WINDOWS]
    banks += [(cc, pd.Period(s, "Q"), pd.Period(e, "Q")) for cc, s, e, t in CONF]
    with Pool(4) as p: rows += p.map(cb_job, banks, chunksize=1)
    d = pd.DataFrame(rows); d.to_csv("results/model_comparison.csv", index=False)
    for dom, g in d.groupby("domain"):
        best = g[["gp", "pa", "hold", "medchg"]].idxmin(axis=1).value_counts().to_dict()
        print(dom, "units", len(g), "mean MAE:", g[["gp", "pa", "hold", "medchg"]].mean().round(4).to_dict(), "| best model counts:", best)
