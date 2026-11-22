#!/usr/bin/env python3
"""Fetch central-bank policy-rate, inflation and activity data (reproducible).

Writes gzip CSVs to data/central_banks/. Sources: BIS SDMX (WS_CBPOL, WS_LONG_CPI),
OECD SDMX (QNA y/y GDP growth, Economic Outlook output gap), World Bank API.
Usage: python3 code/fetch_central_banks.py
"""
import io, json, os, datetime
import pandas as pd
import requests

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "central_banks")
os.makedirs(OUT, exist_ok=True)
BIS = "https://stats.bis.org/api/v2/data/dataflow/BIS"
OECD = "https://sdmx.oecd.org/public/rest/data"
WB = "https://api.worldbank.org/v2"


def get(url, **kw):
    r = requests.get(url, timeout=300, **kw)
    r.raise_for_status()
    return r


def save(df, name):
    p = os.path.join(OUT, name)
    df.to_csv(p, index=False, compression="gzip")
    print(name, df.shape, df.iloc[:, 1].nunique() if df.shape[1] > 1 else "")


def bis(flow, key):
    # NB: an explicit frequency key ("M") is required; "all" returns "No results".
    return pd.read_csv(io.StringIO(get(f"{BIS}/{flow}/1.0/{key}?format=csvfile").text))


# 1. policy rates, monthly end of period, per cent per annum
d = bis("WS_CBPOL", "M")
d = d.rename(columns={"REF_AREA": "area", "TIME_PERIOD": "period", "OBS_VALUE": "policy_rate"})
d["source_ref"] = d["SOURCE_REF"]
save(d[["period", "area", "policy_rate", "source_ref"]].sort_values(["area", "period"]),
     "policy_rate_monthly.csv.gz")

# 2. CPI y/y per cent (UNIT_MEASURE 771), monthly, long history
d = bis("WS_LONG_CPI", "M")
d = d[d["UNIT_MEASURE"].astype(str) == "771"]
d = d.rename(columns={"REF_AREA": "area", "TIME_PERIOD": "period", "OBS_VALUE": "cpi_yoy"})
save(d[["period", "area", "cpi_yoy"]].sort_values(["area", "period"]), "cpi_yoy_monthly.csv.gz")

# 3. OECD quarterly GDP volume growth y/y (seasonally adj. flag Y), all areas
u = (f"{OECD}/OECD.SDD.NAD,DSD_NAMAIN1@DF_QNA_EXPENDITURE_GROWTH_OECD,1.1/"
     "Q.Y..S1.S1.B1GQ._Z._Z._Z.PC.L.GY.T0102?format=csvfile")
d = pd.read_csv(io.StringIO(get(u).text))
d = d.rename(columns={"REF_AREA": "area_iso3", "TIME_PERIOD": "period", "OBS_VALUE": "gdp_growth_yoy"})
save(d[["period", "area_iso3", "gdp_growth_yoy"]].sort_values(["area_iso3", "period"]),
     "gdp_growth_yoy_quarterly.csv.gz")

# 4. OECD Economic Outlook output gap (% of potential GDP), annual
u = f"{OECD}/OECD.ECO.MAD,DSD_EO@DF_EO,1.5/.GAP.A?format=csvfile"
d = pd.read_csv(io.StringIO(get(u).text))
d = d.rename(columns={"REF_AREA": "area_iso3", "TIME_PERIOD": "year", "OBS_VALUE": "output_gap_pct"})
save(d[["year", "area_iso3", "output_gap_pct"]].sort_values(["area_iso3", "year"]),
     "output_gap_annual.csv.gz")

# 5. World Bank annual GDP growth and unemployment (covers emerging markets)
rows = []
for ind, col in [("NY.GDP.MKTP.KD.ZG", "gdp_growth"), ("SL.UEM.TOTL.ZS", "unemployment_rate")]:
    j = get(f"{WB}/country/all/indicator/{ind}?format=json&per_page=20000&date=1960:2026").json()[1]
    rows.append(pd.DataFrame([{"year": int(x["date"]), "area_iso3": x["countryiso3code"], col: x["value"]}
                              for x in j if x["value"] is not None and x["countryiso3code"]]))
save(rows[0].merge(rows[1], on=["year", "area_iso3"], how="outer").sort_values(["area_iso3", "year"]),
     "worldbank_annual.csv.gz")

# 6. crosswalk ISO2 (BIS) <-> ISO3 (OECD/WB); BIS uses XM for the euro area (OECD: EA)
j = get(f"{WB}/country?format=json&per_page=400").json()[1]
cw = pd.DataFrame([{"iso2": c["iso2Code"], "iso3": c["id"], "name": c["name"]} for c in j])
cw = pd.concat([cw, pd.DataFrame([{"iso2": "XM", "iso3": "EA", "name": "Euro area (BIS XM / OECD EA)"}])])
save(cw, "country_crosswalk.csv.gz")

with open(os.path.join(OUT, "download_date.txt"), "w") as f:
    f.write(datetime.date.today().isoformat() + "\n")
