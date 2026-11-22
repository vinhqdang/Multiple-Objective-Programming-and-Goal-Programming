"""Build a firm-year capital-allocation panel from SEC Financial Statement Data Sets (10-K filings).
Input: financial_statements_data_us/<YYYYqN>/{sub.txt, num.txt or num.txt.001...}. Output: data/sec/firm_year_panel.csv.gz.
Rules: form 10-K, fiscal-period FY; consolidated values only (no segments, no co-registrant); USD;
value dated at the fiscal-year end (ddate == period); flows with qtrs == 4, stocks with qtrs == 0.
Several XBRL tags can carry the same concept; the first available in the listed order is used.
If a firm-year appears in several filings, the latest filing is kept."""
import glob, os, subprocess, io, pandas as pd

FLOWS = {
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
    "rnd": ["ResearchAndDevelopmentExpense", "ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost"],
    "dividends": ["PaymentsOfDividends", "PaymentsOfDividendsCommonStock", "PaymentsOfOrdinaryDividends"],
    "buybacks": ["PaymentsForRepurchaseOfCommonStock", "PaymentsForRepurchaseOfEquity"],
    "debt_repay": ["RepaymentsOfLongTermDebt", "RepaymentsOfDebt"],
    "debt_issue": ["ProceedsFromIssuanceOfLongTermDebt", "ProceedsFromIssuanceOfDebt"],
    "acquisitions": ["PaymentsToAcquireBusinessesNetOfCashAcquired"],
    "cfo": ["NetCashProvidedByUsedInOperatingActivities"],
    "revenue": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"],
    "net_income": ["NetIncomeLoss"],
}
STOCKS = {
    "assets": ["Assets"],
    "cash": ["CashAndCashEquivalentsAtCarryingValue"],
    "lt_debt": ["LongTermDebtNoncurrent", "LongTermDebt"],
    "equity": ["StockholdersEquity"],
}
TAGS = {t for v in list(FLOWS.values()) + list(STOCKS.values()) for t in v}

def read_num(qdir):
    parts = sorted(glob.glob(os.path.join(qdir, "num.txt.*")))
    src = parts if parts else [os.path.join(qdir, "num.txt")]
    proc = subprocess.Popen(["cat"] + src, stdout=subprocess.PIPE)
    out = []
    for ch in pd.read_csv(io.TextIOWrapper(proc.stdout, encoding="latin-1"), sep="\t", dtype=str, chunksize=1_000_000,
                          usecols=["adsh", "tag", "ddate", "qtrs", "uom", "segments", "coreg", "value"], quoting=3):
        ch = ch[ch.tag.isin(TAGS) & (ch.uom == "USD") & ch.segments.isna() & ch.coreg.isna()]
        out.append(ch.drop(columns=["segments", "coreg", "uom"]))
    proc.wait()
    return pd.concat(out)

rows = []
for qdir in sorted(glob.glob("financial_statements_data_us/20*q*")):
    sub = pd.read_csv(os.path.join(qdir, "sub.txt"), sep="\t", dtype=str, encoding="latin-1", quoting=3)
    sub = sub[(sub.form == "10-K") & (sub.fp == "FY")][["adsh", "cik", "name", "sic", "fy", "period", "filed"]]
    num = read_num(qdir)
    m = num.merge(sub, on="adsh")
    m = m[m.ddate == m.period]
    m["value"] = pd.to_numeric(m.value, errors="coerce")
    for var, tags in list(FLOWS.items()) + list(STOCKS.items()):
        q = "4" if var in FLOWS else "0"
        x = m[(m.tag.isin(tags)) & (m.qtrs == q)].copy()
        x["prio"] = x.tag.map({t: i for i, t in enumerate(tags)})
        x = x.sort_values("prio").drop_duplicates("adsh")
        rows.append(x[["adsh", "cik", "name", "sic", "fy", "period", "filed", "value"]].assign(var=var))
    print(qdir, len(sub), "10-K filings", flush=True)

long = pd.concat(rows)
wide = long.pivot_table(index=["adsh", "cik", "name", "sic", "fy", "period", "filed"], columns="var", values="value", aggfunc="first").reset_index()
wide = wide.sort_values("filed").drop_duplicates(["cik", "period"], keep="last")
wide.to_csv("data/sec/firm_year_panel.csv.gz", index=False)
print("firm-years:", len(wide), "firms:", wide.cik.nunique())
print(wide.notna().mean().round(2).to_dict())
