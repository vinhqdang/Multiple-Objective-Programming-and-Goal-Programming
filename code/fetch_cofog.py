#!/usr/bin/env python3
"""Reproducible fetch of COFOG / fiscal / NATO data. Writes data/cofog/*.csv.gz.

Usage: python3 code/fetch_cofog.py [--no-nato]
Sources: Eurostat SDMX 2.1 SDMX-CSV bulk API (no key); NATO press-release PDF
(Table 3, defence expenditure as share of GDP; needs `pdftotext`).
targets.csv is hand-curated (see data/cofog/README.md) and is not written here.
"""
import gzip, io, os, re, subprocess, sys, datetime, urllib.request
import pandas as pd

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "cofog")
B = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"
# dataset -> SDMX key (dimension order of each dataflow)
EUROSTAT = {
    "gov_10a_exp":   "A.PC_GDP+PC_TOT+MIO_EUR.S13..TE.",   # freq.unit.sector.cofog99.na_item.geo
    "gov_10dd_edpt1": "A.PC_GDP+MIO_EUR.S13.B9+GD.",        # freq.unit.sector.na_item.geo
    "nama_10_gdp":   "A.CP_MEUR.B1GQ.",                     # freq.unit.na_item.geo
    "demo_pjan":     "A.NR.TOTAL.T.",                       # freq.unit.age.sex.geo (1 Jan population)
}
NATO_URL = "https://www.nato.int/content/dam/nato/webready/documents/finance/def-exp-2025-en.pdf"

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "research-fetch/1.0"}), timeout=300) as r:
        return r.read()

def fetch_eurostat():
    for ds, key in EUROSTAT.items():
        raw = get(f"{B}/{ds}/{key}?format=SDMX-CSV")
        df = pd.read_csv(io.BytesIO(raw), dtype=str)
        df = df.drop(columns=["DATAFLOW", "CONF_STATUS"], errors="ignore")
        df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")
        p = os.path.join(OUT, f"{ds}.csv.gz")
        df.to_csv(p, index=False, compression="gzip")
        print(ds, df.shape, os.path.getsize(p) // 1024, "kB")

def fetch_nato():
    pdf = os.path.join(OUT, "_nato.pdf"); txt = os.path.join(OUT, "_nato.txt")
    open(pdf, "wb").write(get(NATO_URL))
    subprocess.check_call(["pdftotext", "-layout", pdf, txt])
    lines = open(txt, encoding="utf-8").read().splitlines()
    i0 = next(i for i, l in enumerate(lines) if "Table 3: Defence expenditure as a share of GDP" in l)
    i1 = next(i for i in range(i0, len(lines)) if lines[i].strip().startswith("Annual real change"))
    years, rows = None, []
    for l in lines[i0:i1]:
        if years is None and re.search(r"2014\s+2015", l):
            years = re.findall(r"20\d\d", l); est = [("e" in t) for t in re.findall(r"20\d\d\w?", l)]
            continue
        m = re.match(r"^(\S.*?)\s{2,}((?:[-\d.]+|\.\.)(?:\s+(?:[-\d.]+|\.\.))+)\s*$", l)
        if years and m:
            vals = m.group(2).split()
            if len(vals) != len(years): continue
            c = m.group(1).replace("*", "").strip()
            for y, v, e in zip(years, vals, est):
                rows.append((c, int(y), None if v == ".." else float(v), "estimate" if e else "reported"))
    df = pd.DataFrame(rows, columns=["country", "year", "defence_pc_gdp", "status"])
    df["source"] = NATO_URL
    df.to_csv(os.path.join(OUT, "nato_defence_pc_gdp.csv.gz"), index=False, compression="gzip")
    print("nato", df.shape)
    os.remove(pdf); os.remove(txt)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fetch_eurostat()
    if "--no-nato" not in sys.argv: fetch_nato()
    open(os.path.join(OUT, "DOWNLOAD_DATE.txt"), "w").write(datetime.date.today().isoformat() + "\n")
