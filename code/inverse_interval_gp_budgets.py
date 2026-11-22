"""Pilot: inverse interval goal programming on budget shares (defence % GDP, ODA % GNI).

Forward model (per actor-year): keep the share s inside [T - b, T + b] at minimum adjustment cost.
Optimum: increase when s < T - b, decrease when s > T + b, hold otherwise. Only the direction of the
year-on-year change is used. Inverse problem: (T, b) minimising total hinge violation, profiled over a grid
of T to give a set estimate; if the set touches the grid edge, T is only bounded on one side.
Benchmarks: the stated target and the mean share in the same window.
"""
import numpy as np, pandas as pd

HOLD = {"defence": 0.03, "oda": 0.01}     # changes smaller than this (pp) count as hold

def hinge(x, dec, T, b):
    hi, lo = T + b, T - b
    return np.where(dec == 1, np.maximum(0, x - lo),            # increase requires x <= T - b
           np.where(dec == -1, np.maximum(0, hi - x),           # decrease requires x >= T + b
                    np.maximum(0, x - hi) + np.maximum(0, lo - x))).mean()

def estimate(x, dec, grid, bgrid):
    prof = np.array([min(hinge(x, dec, T, b) for b in bgrid) for T in grid])
    k = prof.argmin(); s = grid[prof <= prof.min() + 0.01]
    return grid[k], (s.min(), s.max()), prof.min()

def panel(df, key, val, hold):
    df = df.sort_values([key, "year"]).copy()
    df["d"] = df.groupby(key)[val].diff()
    df = df.dropna(subset=["d"])
    df["dec"] = np.where(df.d > hold, 1, np.where(df.d < -hold, -1, 0))
    df["x"] = df.groupby(key)[val].shift(0) - df.d          # level before the decision (previous year)
    return df

def report(name, df, periods, stated, grid, bgrid):
    rows = []
    for lab, (a, b_) in periods.items():
        g = df[(df.year >= a) & (df.year <= b_)]
        T, s, loss = estimate(g.x.values, g.dec.values, grid, bgrid)
        edge = " (upper end at grid edge: only a lower bound)" if s[1] >= grid.max() - 1e-9 else ""
        rows.append(dict(domain=name, period=lab, n=len(g), up=int((g.dec == 1).sum()), down=int((g.dec == -1).sum()),
                         T_hat=round(T, 2), set_T=f"[{s[0]:.2f}, {s[1]:.2f}]{edge}", mean_level=round(g.x.mean(), 2), stated=stated[lab]))
    return pd.DataFrame(rows)

if __name__ == "__main__":
    out = []
    # Defence: Eurostat COFOG GF02 (% GDP), EU members that were NATO members throughout 1995-2024
    nato_eu = ["BE","BG","HR","CZ","DK","EE","FR","DE","GR","HU","IT","LV","LT","LU","NL","PL","PT","RO","SK","SI","ES"]
    c = pd.read_csv("data/cofog/gov_10a_exp.csv.gz")
    d = c[(c.unit == "PC_GDP") & (c.cofog99 == "GF02") & (c.geo.isin(nato_eu))].rename(columns={"TIME_PERIOD": "year", "OBS_VALUE": "v"})
    d = panel(d[["geo", "year", "v"]], "geo", "v", HOLD["defence"])
    out.append(report("defence, COFOG GF02 % GDP (21 EU NATO members)", d,
                      {"1996-2013 (before Wales)": (1996, 2013), "2015-2021 (after Wales 2014)": (2015, 2021), "2022-2024 (after 2022 invasion)": (2022, 2024)},
                      {"1996-2013 (before Wales)": "none", "2015-2021 (after Wales 2014)": "2.0 (NATO def.)", "2022-2024 (after 2022 invasion)": "2.0 floor (NATO def.)"},
                      np.arange(0.0, 6.001, 0.02), np.linspace(0, 2, 41)))
    # Defence: NATO definition, all allies 2015-2025
    n = pd.read_csv("data/cofog/nato_defence_pc_gdp.csv.gz").rename(columns={"defence_pc_gdp": "v"})
    n = n[~n.country.str.contains("NATO|Europe|Canada and", case=False, regex=True) | (n.country == "Canada")]
    n = panel(n[["country", "year", "v"]].dropna(), "country", "v", HOLD["defence"])
    out.append(report("defence, NATO definition % GDP (allies)", n,
                      {"2015-2021": (2015, 2021), "2022-2025": (2022, 2025)}, {"2015-2021": "2.0", "2022-2025": "2.0 floor; 3.5 core by 2035"},
                      np.arange(0.0, 6.001, 0.02), np.linspace(0, 2, 41)))
    # ODA/GNI: DAC1, net-disbursement basis to 2017, grant-equivalent from 2018 (series break)
    a = pd.read_csv("data/aid/dac1_donor_oda_gni.csv.gz")
    a = a[((a.measure.astype(str) == "2") & (a.year <= 2017)) | ((a.measure.astype(str) == "11002") & (a.year >= 2018))]
    a = a[a.unit == "PT_B5G"].groupby(["donor", "year"], as_index=False).value.first().rename(columns={"value": "v"})
    a = panel(a, "donor", "v", HOLD["oda"]); a = a[~((a.year == 2018))]   # drop the change across the series break
    out.append(report("ODA % GNI (DAC donors)", a,
                      {"1971-2004": (1971, 2004), "2006-2015 (EU 2005 commitments)": (2006, 2015), "2016-2024": (2016, 2024)},
                      {"1971-2004": "0.7 (UN)", "2006-2015 (EU 2005 commitments)": "0.7 by 2015 (EU-15); 0.33 (new members)", "2016-2024": "0.7 (UN, SDG 17.2)"},
                      np.arange(0.0, 1.5001, 0.005), np.linspace(0, 0.8, 41)))
    res = pd.concat(out); pd.set_option("display.width", 250)
    print(res.to_string(index=False)); res.to_csv("results/inverse_interval_gp_budgets.csv", index=False)
