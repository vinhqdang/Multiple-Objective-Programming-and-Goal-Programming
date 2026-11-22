"""Fetch foreign-aid data for the inverse goal-programming project.

Writes compressed CSVs to data/aid/ (run from the repo root:  python code/fetch_aid.py).
Sources: OECD SDMX API (DAC2A, DAC1, GDFF IND) and World Bank API v2. Raw codes are kept;
no deflating or filtering of aggregates is done here (see data/aid/README.md).
"""
import io, os, sys, time, datetime
import requests, pandas as pd

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "aid")
os.makedirs(OUT, exist_ok=True)
OECD = "https://sdmx.oecd.org/public/rest"
HDR = {"Accept": "application/vnd.sdmx.data+csv"}


def get(url, params=None, headers=None, tries=4):
    for i in range(tries):
        r = requests.get(url, params=params, headers=headers, timeout=300)
        if r.status_code == 200:
            return r
        if r.status_code == 404 and ("NoResultsFound" in r.text or "NoRecordsFound" in r.text):
            return None
        time.sleep(5 * (i + 1))
    r.raise_for_status()


def oecd_csv(flow, key, start, end):
    r = get(f"{OECD}/data/{flow}/{key}", {"startPeriod": start, "endPeriod": end}, HDR)
    return None if r is None else pd.read_csv(io.StringIO(r.text), dtype=str)


def save(df, name):
    p = os.path.join(OUT, name)
    df.to_csv(p, index=False, compression="gzip")
    print(name, df.shape, round(os.path.getsize(p) / 1e6, 2), "MB")


def dac2a():
    """Net ODA disbursements (measure 206), donor x recipient x year, constant 2024 USD (Q) and current USD (V), millions."""
    parts = []
    for price in ("Q", "V"):
        for s in range(1960, 2025, 5):
            d = oecd_csv("OECD.DCD.FSD,DSD_DAC2@DF_DAC2A,1.7", f"..206.USD.{price}", s, min(s + 4, 2024))
            if d is not None:
                parts.append(d)
            print("dac2a", price, s, None if d is None else len(d), flush=True)
    df = pd.concat(parts)
    df = df[["DONOR", "RECIPIENT", "TIME_PERIOD", "PRICE_BASE", "OBS_VALUE", "BASE_PER", "UNIT_MULT", "OBS_STATUS"]]
    df.columns = ["donor", "recipient", "year", "price_base", "oda_musd", "base_year", "unit_mult", "obs_status"]
    df["oda_musd"] = df["oda_musd"].astype(float)
    assert (df.unit_mult == "6").all()
    save(df.drop(columns="unit_mult"), "dac2a_oda_donor_recipient_year.csv.gz")


def dac1():
    """Donor-level totals: ODA/GNI (measures 2 = net-disbursement basis, 11002 = grant-equivalent basis) and ODA volumes."""
    parts = []
    for m in ("2", "11002", "11010", "1010"):
        for s in range(1960, 2025, 15):
            d = oecd_csv("OECD.DCD.FSD,DSD_DAC1@DF_DAC1,1.8", f"..{m}....", s, min(s + 14, 2024))
            if d is not None:
                parts.append(d)
    df = pd.concat(parts)
    df = df[df.SECTOR == "_Z"]
    keep = ["DONOR", "MEASURE", "FLOW_TYPE", "UNIT_MEASURE", "PRICE_BASE", "TIME_PERIOD", "OBS_VALUE", "UNIT_MULT"]
    df = df[keep]
    df.columns = ["donor", "measure", "flow_type", "unit", "price_base", "year", "value", "unit_mult"]
    df["value"] = df.value.astype(float)
    save(df, "dac1_donor_oda_gni.csv.gz")


def recipients_oecd():
    """OECD recipient GNI, population, GNI per capita (DF_IND)."""
    parts = [oecd_csv("OECD.DCD.FSD,DSD_GDFF@DF_IND,1.0", "..509+559+501..", 1960, 2024)]
    df = pd.concat(parts)[["RECIPIENT", "MEASURE", "UNIT_MEASURE", "UNIT_MULT", "TIME_PERIOD", "OBS_VALUE"]]
    df.columns = ["recipient", "measure", "unit", "unit_mult", "year", "value"]
    df["measure"] = df.measure.map({"509": "population", "559": "gni_current", "501": "gni_pc"})
    save(df, "recipient_oecd_gni_pop.csv.gz")


WB = {"NY.GDP.PCAP.KD": "gdp_pc_const2015usd", "NY.GDP.PCAP.PP.KD": "gdp_pc_ppp_const", "SP.POP.TOTL": "population",
      "SI.POV.DDAY": "poverty_3usd_2021ppp", "SI.POV.GINI": "gini", "SP.DYN.IMRT.IN": "infant_mort",
      "SP.DYN.LE00.IN": "life_exp", "NY.GNP.PCAP.CD": "gni_pc_atlas_usd"}


def worldbank():
    rows = []
    for code, name in WB.items():
        page, ds = 1, []
        while True:
            r = get("https://api.worldbank.org/v2/country/all/indicator/" + code,
                    {"format": "json", "per_page": 20000, "date": "1960:2024", "page": page}).json()
            ds += r[1]
            if page >= r[0]["pages"]:
                break
            page += 1
        d = pd.DataFrame([{"iso3": x["countryiso3code"] or x["country"]["id"], "year": int(x["date"]), name: x["value"]} for x in ds])
        print("wb", name, len(d), d[name].notna().sum(), "last updated", r[0].get("lastupdated"), flush=True)
        rows.append(d.set_index(["iso3", "year"]))
    df = pd.concat(rows, axis=1).dropna(how="all").reset_index()
    save(df, "worldbank_recipient_indicators.csv.gz")
    c = get("https://api.worldbank.org/v2/country", {"format": "json", "per_page": 400}).json()[1]
    meta = pd.DataFrame([{"iso3": x["id"], "name": x["name"], "region": x["region"]["value"].strip(),
                          "income_group": x["incomeLevel"]["value"], "lending_type": x["lendingType"]["value"]} for x in c])
    save(meta, "worldbank_country_meta.csv.gz")


def lookups():
    """OECD DONOR/RECIPIENT code names (CL_AREA_ORG) so that aggregates can be filtered."""
    r = get(f"{OECD}/dataflow/OECD.DCD.FSD/DSD_DAC2@DF_DAC2A/1.7", {"references": "descendants"},
            {"Accept": "application/vnd.sdmx.structure+json"}).json()["data"]
    cl = [c for c in r["codelists"] if c["id"] == "CL_AREA_ORG"][0]["codes"]
    save(pd.DataFrame([{"code": c["id"], "name": c["name"]} for c in cl]), "oecd_area_codes.csv.gz")


if __name__ == "__main__":
    steps = sys.argv[1:] or ["lookups", "dac2a", "dac1", "recipients_oecd", "worldbank"]
    for s in steps:
        globals()[s]()
    print("done", datetime.date.today())
