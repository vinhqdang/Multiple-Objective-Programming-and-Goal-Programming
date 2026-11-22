"""Gradualism inverse goal programming (K=1, direct control) on three application domains.
The decision directly changes the controlled share (transmission 1): y = x + Delta, so in migp_quad's
parametrisation alpha = 1 and D = -Delta. Each unit-year is one decision; units are pooled with common
parameters where per-unit series are short. Estimator: migp_quad.fit_ms (parallel multistart + LP/LNS polish).
Outputs: implied target tau, half-band b, step sizes (omega+ = step when above the band, i.e. a cut;
omega- = step when below, i.e. an increase), compared with stated targets and with mean levels."""
import sys, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, migp_quad as Q

def fit_k1(x, delta, n_starts=200):
    X = x.reshape(-1, 1); D = -delta
    lo = np.array([0.9999, np.percentile(x, 1), 0.0, 0.0, 0.0]); span = np.abs(delta).max()
    hi = np.array([1.0001, np.percentile(x, 99), (x.max() - x.min()) / 2, 2 * span, 2 * span])
    h = Q.fit_ms(X, D, n_starts=n_starts, top=3, lo=lo, hi=hi, lns_iters=5, alpha_bounds=(0.9999, 1.0001))
    # a step at its upper bound means no period was strictly outside the band on that side: not identified
    sc, sr = float(h["omega_p"][0]), float(h["omega_m"][0])
    sc = sc if sc < hi[3] * 0.999 and sc < 4.999 else np.nan; sr = sr if sr < hi[4] * 0.999 and sr < 4.999 else np.nan
    return dict(tau=float(h["tau"][0]), b=float(h["b"][0]), step_cut=sc, step_raise=sr,
                loss=float(h["loss"]), n=len(x), mean_level=float(x.mean()))

def panel(df, unit, val):
    df = df.sort_values([unit, "year"]).copy()
    df["prev"] = df.groupby(unit)[val].shift(1); df["prev_year"] = df.groupby(unit).year.shift(1)
    df = df[(df.year - df.prev_year) == 1].dropna(subset=["prev", val])
    return df.assign(x=df.prev, delta=df[val] - df.prev)

def aid():
    a = pd.read_csv("data/aid/dac1_donor_oda_gni.csv.gz")
    a = a[((a.measure.astype(str) == "2") & (a.year <= 2017)) | ((a.measure.astype(str) == "11002") & (a.year >= 2018))]
    a = a[a.unit == "PT_B5G"].groupby(["donor", "year"], as_index=False).value.first()
    p = panel(a, "donor", "value"); p = p[p.year != 2018]
    countries = pd.read_csv("data/aid/worldbank_country_meta.csv.gz")
    iso = set(countries[(countries.region != "Aggregates") & (countries.income_group != "Aggregates")].iso3)
    p = p[p.donor.isin(iso)]                                     # bilateral country donors only (drop DAC, G7, EU aggregates)
    rows = []
    for donor, g in p.groupby("donor"):
        if len(g) < 30: continue
        r = fit_k1(g.x.values, g.delta.values); r.update(domain="ODA % GNI", unit=donor, stated=0.7); rows.append(r); print(r, flush=True)
    return rows

def defence():
    rows = []
    n = pd.read_csv("data/cofog/nato_defence_pc_gdp.csv.gz").rename(columns={"defence_pc_gdp": "v"})
    n = n[~n.country.str.contains("NATO|Europe|Canada and", case=False, regex=True) | (n.country == "Canada")].dropna(subset=["v"])
    p = panel(n, "country", "v")
    for lab, (a, b) in {"NATO def., 2015-2021": (2015, 2021), "NATO def., 2022-2025": (2022, 2025)}.items():
        g = p[(p.year >= a) & (p.year <= b)]
        r = fit_k1(g.x.values, g.delta.values); r.update(domain="defence % GDP (pooled allies)", unit=lab, stated=2.0); rows.append(r); print(r, flush=True)
    return rows

def firms():
    f = pd.read_csv("data/sec/firm_year_panel.csv.gz")
    f = f[(f.assets > 1e7) & f.equity.notna()].copy()
    f["lev"] = 1 - f.equity / f.assets; f = f[(f.lev > 0) & (f.lev < 1)]
    f["year"] = f.period.astype(str).str[:4].astype(int); f["sic2"] = (pd.to_numeric(f.sic, errors="coerce") // 100)
    f = f.dropna(subset=["sic2"]).drop_duplicates(["cik", "year"], keep="last")
    p = panel(f, "cik", "lev")
    rows = []
    for sic2, g in p.groupby("sic2"):
        if len(g) < 1500: continue
        g = g.sample(n=min(len(g), 3000), random_state=0)
        r = fit_k1(g.x.values, g.delta.values); r.update(domain="book leverage (pooled firms)", unit=f"SIC {int(sic2):02d}", stated=np.nan,
                                                         median_level=float(g.x.median())); rows.append(r); print(r, flush=True)
    return rows

if __name__ == "__main__":
    which = sys.argv[1:] or ["aid", "defence", "firms"]
    out = []
    for w in which: out += globals()[w]()
    pd.DataFrame(out).to_csv(f"results/applications_gp_{'_'.join(which)}.csv", index=False)
