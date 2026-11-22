#!/usr/bin/env python3
"""Fetch published central-bank inflation forecasts (vintage = publication date) and
write one tidy file: data/central_banks/forecasts.csv.gz

Columns: bank, country (ISO2), vintage_date, target_period (YYYY-Qn), horizon_q,
         variable, value, source_url

Banks: Riksbank (SE), Norges Bank (NO), Bank of England (GB), Federal Reserve (US),
       Bank of Canada (CA), Reserve Bank of Australia (AU).
RBNZ (NZ) blocks automated access (HTTP 403) and is NOT fetched.

Raw downloads go to RAW (default /tmp/cbfc/<bank>/); a manifest with download
dates is written to RAW/manifest.csv. Re-running re-uses cached raw files unless
--refresh is given.

Usage:  python3 code/fetch_cb_forecasts.py [--refresh] [--only se,no,gb,us,ca,au]
Needs: pandas, requests, openpyxl, xlrd (for the legacy .xls files of Norges Bank/RBA).
"""
import argparse, datetime as dt, html, io, json, os, re, sys, time
from pathlib import Path
import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = Path(os.environ.get("CBFC_RAW", "/tmp/cbfc"))
OUT = ROOT / "data" / "central_banks" / "forecasts.csv.gz"
TODAY = dt.date.today().isoformat()
UA = {"User-Agent": "research-data-fetch/1.0"}
SESSION = requests.Session()
SESSION.headers.update(UA)
MANIFEST = []          # (bank, file, url, status, download_date)
LOG = []               # warnings


def log(msg):
    LOG.append(msg)
    print("  [note]", msg, file=sys.stderr)


def fetch(url, path, refresh=False, bank=""):
    """Download url to path (cached). Returns Path or None if blocked/failed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0 and not refresh:
        MANIFEST.append((bank, path.name, url, "ok(cached)", dt.date.fromtimestamp(path.stat().st_mtime).isoformat()))
        return path
    for attempt in range(3):
        try:
            r = SESSION.get(url, timeout=90)
        except requests.RequestException as e:
            time.sleep(2)
            continue
        if r.status_code == 200:
            path.write_bytes(r.content)
            MANIFEST.append((bank, path.name, url, "ok", TODAY))
            return path
        if r.status_code in (403, 404):
            MANIFEST.append((bank, path.name, url, f"HTTP {r.status_code}", TODAY))
            return None
        time.sleep(2)
    MANIFEST.append((bank, path.name, url, "failed", TODAY))
    return None


def qlabel(y, q):
    return f"{y}-Q{q}"


def qidx(y, q):
    return y * 4 + (q - 1)


def qidx_date(d):
    return qidx(d.year, (d.month - 1) // 3 + 1)


def lab_from_idx(i):
    return qlabel(i // 4, i % 4 + 1)


def make_rows(bank, cc, vint, tgt_idx, var, val, url):
    """one record; horizon_q = target quarter - quarter of vintage (0 = current quarter)."""
    v = pd.Timestamp(vint)
    return dict(bank=bank, country=cc, vintage_date=v.strftime("%Y-%m-%d"),
                target_period=lab_from_idx(tgt_idx),
                horizon_q=int(tgt_idx - qidx_date(v)), variable=var,
                value=float(val), source_url=url)


def norm(x):
    if x is None:
        return ""
    return re.sub(r"\s+", " ", str(x).replace("\xad", "-").replace("–", "-")).strip()


def read_grid(path, max_rows=700, max_cols=60):
    """Return {sheet: list of row lists} for .xlsx (openpyxl) or .xls (xlrd); dates as datetime."""
    path = Path(path)
    out = {}
    if path.suffix.lower() == ".xls":
        import xlrd
        wb = xlrd.open_workbook(str(path))
        for sh in wb.sheets():
            rows = []
            for r in range(min(sh.nrows, max_rows)):
                row = []
                for c in range(min(sh.ncols, max_cols)):
                    cell = sh.cell(r, c)
                    if cell.ctype == xlrd.XL_CELL_DATE:
                        try:
                            row.append(xlrd.xldate.xldate_as_datetime(cell.value, wb.datemode))
                        except Exception:
                            row.append(None)
                    elif cell.ctype in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK, xlrd.XL_CELL_ERROR):
                        row.append(None)
                    else:
                        row.append(cell.value)
                rows.append(row)
            out[sh.name] = rows
    else:
        import openpyxl
        wb = openpyxl.load_workbook(str(path), data_only=True, read_only=True)
        for ws in wb.worksheets:
            rows = [list(r[:max_cols]) for r in ws.iter_rows(max_row=max_rows, values_only=True)]
            out[ws.title] = rows
    return out


def num(x):
    if isinstance(x, bool):
        return None
    if isinstance(x, (int, float, np.floating)):
        return None if (isinstance(x, float) and np.isnan(x)) else float(x)
    if isinstance(x, str):
        s = x.strip().replace(",", ".")
        try:
            return float(s)
        except ValueError:
            return None
    return None


# ----------------------------------------------------------------------------------------
# Norges Bank (NO): CPI and CPI-ATE, four-quarter change, quarterly, from the data files that
# accompany each Monetary Policy Report. Vintage = publication date printed on the report page.
# Projection quarters = quarters >= the quarter of publication (Norges Bank's projections start in
# the current quarter; checked against the 'Projections/Anslag' markers in the 2021-2024 tables).
# ----------------------------------------------------------------------------------------
NB_BASE = "https://www.norges-bank.no"
NB_VAR = {"CPI": "CPI_4q", "CPI-ATE": "CPI-ATE_4q"}
HDR_RE = re.compile(r"^(CPI-ATE|CPI|KPI-JAE|KPI)\.?\s?\d?\)?(, four-quarter change)?$")
ROW_RE = re.compile(r"^(CPI-ATE|CPI|KPI-JAE|KPI)\s*(\((four-quarter|firekvartal)[^)]*\))?$", re.I)
QLAB_RE = [re.compile(r"^Q(\d)\s*(\d{4})$"), re.compile(r"^(\d)\.?\s?kv\.?\s?(\d{4})$")]


def nb_pages(refresh):
    cache = RAW / "norgesbank" / "pages.json"
    found = json.loads(cache.read_text()) if cache.exists() and not refresh else {}
    pages = []
    for y in range(2007, 2027):
        yy = str(y)[2:]
        for n in range(1, 5):
            key = f"{y}_{n}"
            slugs = [found[key]] if key in found else [
                f"{n}{yy}-monetary-policy-report", f"mpr-{n}{y}", f"mpr-{n}{yy}", f"{n}{yy}"]
            for slug in slugs:
                url = f"{NB_BASE}/en/news-events/publications/Monetary-Policy-Report/{y}/{slug}/"
                p = fetch(url, RAW / "norgesbank" / "pages" / f"p_{n}_{y}.html", refresh, "NO")
                if p is None:
                    continue
                s = p.read_text(errors="ignore")
                t = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)))
                t = re.sub(r"\s+", " ", t)
                m = re.search(r"Published:? (\d{1,2} [A-Z][a-z]+ 20\d\d)", t)
                ti = re.search(r"<title>([^<]*)", s)
                title = html.unescape(ti.group(1)) if ti else ""
                if not m or not re.search(rf"{n}/(?:{yy}|{y})\b", re.sub(r"\s+", " ", title)):
                    p.unlink()
                    continue
                pub = dt.datetime.strptime(m.group(1), "%d %B %Y").date()
                links = sorted(set(re.findall(r'href="([^"]*\.xlsx?)[^"]*"', s)))
                found[key] = slug
                pages.append(dict(y=y, n=n, pub=pub, url=url, links=links))
                break
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(found))
    return pages


def _qparse(c):
    if isinstance(c, (dt.datetime, dt.date)):
        return qidx_date(c), True
    s = norm(c)
    for rx in QLAB_RE:
        m = rx.match(s)
        if m:
            q, y = int(m.group(1)), int(m.group(2))
            return qidx(y, q), False
    m = re.match(r"^(\d{4})\s*-?Q(\d)$", s)
    if m:
        return qidx(int(m.group(1)), int(m.group(2))), False
    return None, False


NB_EXCL = re.compile(r"sweden|sverige|euro|trading partner|handelspartner|abroad|foreign|conditional|betinget|new information|ny informasjon", re.I)


def nb_chart_candidates(grid):
    """Quarterly series in chart sheets: header cell is exactly CPI / CPI-ATE (current vintage),
    sheet title mentions four-quarter growth (firekvartalersvekst) and is not about other countries."""
    for sh, rows in grid.items():
        title = " ".join(norm(c) for r in rows[:12] for c in r[:1] if c)
        hdrtxt = " ".join(norm(c) for r in rows[:12] for c in r[:20] if c)
        if not re.search(r"four-quarter|firekvartal", hdrtxt, re.I) or NB_EXCL.search(title):
            continue
        seen = set()
        for h in range(min(16, len(rows))):
            for c in range(1, min(len(rows[h]), 20)):
                m = HDR_RE.match(re.sub(r"[\u00b9\u00b2\u00b3\u2070-\u209f]", "", norm(rows[h][c])))
                if not m or c in seen:
                    continue
                seen.add(c)
                var = "CPI-ATE" if m.group(1) in ("CPI-ATE", "KPI-JAE") else "CPI"
                pts = []
                for r in range(h + 1, len(rows)):
                    row = rows[r]
                    d = None
                    for dc in (0, 1):
                        if dc < len(row) and isinstance(row[dc], (dt.datetime, dt.date)):
                            d = row[dc]
                            break
                    v = num(row[c]) if c < len(row) else None
                    if d is not None and v is not None:
                        pts.append((d, v))
                if len(pts) < 8:
                    continue
                gaps = np.diff([pd.Timestamp(p[0]).value for p in pts]) / 86400e9
                if not (80 <= np.median(gaps) <= 100):
                    continue          # monthly (12-month) or annual series
                yield sh, var, {qidx_date(d): v for d, v in pts}, "chart"


def nb_table_candidates(grid):
    """Tables with quarterly column headers (Q1 2023 / 1 kv. 2023) and rows 'CPI (four-quarter change)'."""
    for sh, rows in grid.items():
        for h in range(min(14, len(rows))):
            labs = {}
            for c, cell in enumerate(rows[h][:60]):
                i, isdate = _qparse(cell)
                if i is not None and not isdate:
                    labs[c] = i
            if len(labs) < 6:
                continue
            for r in range(h + 1, min(h + 40, len(rows))):
                lab = norm(rows[r][0]) if rows[r] else ""
                m = ROW_RE.match(lab)
                if not m:
                    continue
                var = "CPI-ATE" if m.group(1) in ("CPI-ATE", "KPI-JAE") else "CPI"
                ser = {i: num(rows[r][c]) for c, i in labs.items() if c < len(rows[r]) and num(rows[r][c]) is not None}
                if len(ser) >= 6:
                    yield sh, var, ser, "table"
            break


def nb_extract(pg, refresh):
    pub = pd.Timestamp(pg["pub"])
    pub_idx = qidx_date(pub)
    cands = {}
    srcurl = {}
    for ln in pg["links"]:
        url = NB_BASE + ln
        fn = RAW / "norgesbank" / "raw" / f"{pg['y']}_{pg['n']}__{os.path.basename(ln)}"
        p = fetch(url, fn, refresh, "NO")
        if p is None:
            continue
        try:
            grid = read_grid(p)
        except Exception as e:
            log(f"NO {pg['y']}/{pg['n']} cannot read {fn.name}: {e}")
            continue
        for gen in (nb_table_candidates(grid), nb_chart_candidates(grid)):
            for sh, var, ser, kind in gen:
                fut = {i: v for i, v in ser.items() if i >= pub_idx}
                if not fut:
                    continue
                cands.setdefault(var, []).append((kind, fn.name, sh, fut, url))
    recs = []
    for var, lst in cands.items():
        lst.sort(key=lambda t: (0 if t[0] == "table" else 1, -len(t[3])))
        kind, fname, sh, fut, url = lst[0]
        for kind2, f2, sh2, fut2, _ in lst[1:]:
            common = set(fut) & set(fut2)
            bad = [i for i in common if abs(fut[i] - fut2[i]) > 0.051]
            if common and bad:
                log(f"NO {pg['y']}/{pg['n']} {var}: {len(bad)}/{len(common)} values differ between {fname}:{sh} and {f2}:{sh2}; used first")
        for i, v in sorted(fut.items()):
            recs.append(make_rows("Norges Bank", "NO", pub, i, NB_VAR[var], v, url))
    if not recs:
        log(f"NO {pg['y']}/{pg['n']}: no CPI projections found in {len(pg['links'])} data file(s)")
    # drop (vintage, variable) blocks with fewer than 6 projected quarters (partial / mis-parsed)
    df = pd.DataFrame(recs)
    if len(df):
        cnt = df.groupby("variable").value.transform("size")
        small = df.groupby("variable").value.size()
        for var, k in small.items():
            if k < 6:
                log(f"NO {pg['y']}/{pg['n']} {var}: only {k} projected quarters, dropped")
                df = df[df.variable != var]
    return df.to_dict("records") if len(df) else []


def get_norges(refresh):
    out = []
    for pg in nb_pages(refresh):
        out += nb_extract(pg, refresh)
    return out


# ----------------------------------------------------------------------------------------
# Sveriges Riksbank (SE): 'Forecasts and outcomes' Excel files (all Monetary Policy Reports).
# Sheets SEMCPINAYNA (CPI) and SEMCPIFNAYNA (CPIF): annual % change, MONTHLY, one column per MPR,
# header rows give 'Publication date' and 'Last outcome date'. Forecast months = months after the
# last outcome. Converted to quarters as the mean of the 3 monthly y/y rates (a quarter is kept
# only if all 3 months are available and at least one of them is a forecast month).
# ----------------------------------------------------------------------------------------
RB_URLS = [
    "https://www.riksbank.se/globalassets/media/statistik/makro/eng/outcome-and-forecasts.xlsx",
    "https://www.riksbank.se/globalassets/media/statistik/makro/eng/forecasts-and-outcomes-2007-2014.xlsx",
]
RB_SHEETS = {"SEMCPINAYNA": "CPI_yoy_qavg", "SEMCPIFNAYNA": "CPIF_yoy_qavg"}


def get_riksbank(refresh):
    recs, seen = [], set()
    for url in RB_URLS:
        fn = RAW / "riksbank" / os.path.basename(url)
        p = fetch(url, fn, refresh, "SE")
        if p is None:
            log(f"SE: could not download {url}")
            continue
        grid = read_grid(p, max_rows=800, max_cols=120)
        for sh, var in RB_SHEETS.items():
            rows = grid.get(sh)
            if not rows:
                continue
            hdr = {norm(r[0]): r for r in rows[:14] if r and r[0]}
            mpr, pubs, last = hdr["MPR"], hdr["Publication date"], hdr["Last outcome date"]
            data = [(r[0], r) for r in rows if r and r[0] is not None and re.match(r"^\d{4}-\d{2}-\d{2}", str(r[0]))]
            for c in range(1, len(mpr)):
                lab = norm(mpr[c])
                if not lab or not isinstance(pubs[c], (dt.datetime, dt.date)):
                    continue
                key = (lab, var)
                if key in seen:
                    continue
                seen.add(key)
                pub, lo = pd.Timestamp(pubs[c]), pd.Timestamp(last[c])
                m = {}
                for d, r in data:
                    v = num(r[c]) if c < len(r) else None
                    if v is not None:
                        m[pd.Timestamp(d)] = v
                qs = {}
                for d, v in m.items():
                    qs.setdefault(qidx_date(d), []).append((d, v))
                for qi, lst in sorted(qs.items()):
                    if len(lst) != 3 or not any(d > lo for d, _ in lst) or qi < qidx_date(pub):
                        continue
                    recs.append(make_rows("Sveriges Riksbank", "SE", pub, qi, var, np.mean([v for _, v in lst]), url))
    return recs


# ----------------------------------------------------------------------------------------
# Bank of England (GB): 'Projections Databank CSV' inside the 'charts, slides and data' zip of the
# latest Monetary Policy Report. It holds the central projection of every Inflation Report / MPR
# since Feb 2004. 'CPI inflation, Per cent' = four-quarter CPI inflation by quarter. Report date is
# month-level only (e.g. 'Feb-04'); vintage_date is set to the first day of that month.
# Rows before the vintage quarter are outcomes and are dropped.
# ----------------------------------------------------------------------------------------
BOE_ZIPS = [
    "https://www.bankofengland.co.uk/-/media/boe/files/monetary-policy-report/2026/november/mpr-november-2026-charts-slides-and-data.zip",
    "https://www.bankofengland.co.uk/-/media/boe/files/monetary-policy-report/2026/july/mpr-july-2026-charts-slides-and-data.zip",
    "https://www.bankofengland.co.uk/-/media/boe/files/monetary-policy-report/2026/february/mpr-february-2026-charts-slides-and-data.zip",
    "https://www.bankofengland.co.uk/-/media/boe/files/monetary-policy-report/2025/november/mpr-november-2025-charts-slides-and-data.zip",
]


def get_boe(refresh):
    import zipfile
    for url in BOE_ZIPS:
        fn = RAW / "boe" / os.path.basename(url)
        if fetch(url, fn, refresh, "GB") is None:
            continue
        with zipfile.ZipFile(fn) as z:
            names = [n for n in z.namelist() if n.lower().endswith(".csv")]
            if not names:
                continue
            df = pd.read_csv(io.BytesIO(z.read(names[0])))
        break
    else:
        log("GB: no Projections Databank CSV could be downloaded")
        return []
    df = df[(df["Variable"] == "CPI inflation") & (df["Units"] == "Per cent")]
    recs = []
    for r in df.itertuples(index=False):
        rep = dt.datetime.strptime(r[0], "%b-%y")
        m = re.match(r"(\d{4}) Q(\d)", r[1])
        if not m:
            continue
        ti = qidx(int(m.group(1)), int(m.group(2)))
        if ti < qidx_date(rep):
            continue
        recs.append(make_rows("Bank of England", "GB", rep, ti, "CPI_yoy_q", r[4], url))
    return recs


# ----------------------------------------------------------------------------------------
# Federal Reserve (US): Summary of Economic Projections, MEDIAN projections of PCE and core PCE
# inflation (Q4/Q4 per cent) parsed from the official 'Projection Materials' tables of each FOMC
# meeting with an SEP. Median first appears in the table from the Sep 2015 SEP (earlier tables show
# only central tendency/range and are skipped). Target = Q4 of the projected year.
# ----------------------------------------------------------------------------------------
FED = "https://www.federalreserve.gov/monetarypolicy/"


def fed_dates(refresh):
    dates = set()
    pages = [FED + "fomccalendars.htm"] + [FED + f"fomchistorical{y}.htm" for y in range(2015, 2021)]
    for u in pages:
        p = fetch(u, RAW / "fed" / "cal" / os.path.basename(u), refresh, "US")
        if p:
            dates |= set(re.findall(r"(?:fomcminutes|fomcpresconf|monetary|fomcprojtabl[e]?)(20\d{6})", p.read_text(errors="ignore")))
    return sorted(d for d in dates if d >= "20150101")


def fed_parse(text, kind):
    t = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", "", text, flags=re.S)))
    t = re.sub(r"\s+", " ", t.replace(" ", " ").replace("–", "-"))
    hdr = re.search(r"(?:Median|Variable)[^.]{0,80}?((?:20\d\d\s+){2,5})Longer", t)
    if not hdr:
        return None
    years = [int(x) for x in hdr.group(1).split()]
    i0 = t.find("Unemployment rate")
    lab = "Core PCE inflation" if kind == "core" else "PCE inflation"
    i = t.find(lab, i0)
    if i < 0:
        return None
    toks = t[i + len(lab): i + len(lab) + 120].split()
    if kind == "core" and toks and re.fullmatch(r"\d", toks[0]):
        toks = toks[1:]                      # footnote marker
    vals = []
    for tk in toks[: len(years)]:
        if not re.fullmatch(r"-?\d+\.\d", tk) and not re.fullmatch(r"-?\d+", tk):
            return None                      # central-tendency format ('1.3 to 1.7') -> skip
        vals.append(float(tk))
    if len(vals) != len(years) or len(toks) <= len(years) or toks[len(years)] in ("to", "-"):
        return None
    return dict(zip(years, vals))


def get_fed(refresh):
    recs = []
    for d in fed_dates(refresh):
        txt = None
        for nm in ("fomcprojtabl", "fomcprojtable"):
            url = f"{FED}{nm}{d}.htm"
            p = fetch(url, RAW / "fed" / f"{nm}{d}.htm", refresh, "US")
            if p:
                txt = p.read_text(errors="ignore")
                break
        if txt is None:
            continue
        vint = pd.Timestamp(d)
        for kind, var in (("pce", "PCE_median_Q4Q4"), ("core", "corePCE_median_Q4Q4")):
            res = fed_parse(txt, kind)
            if not res:
                if kind == "pce":
                    log(f"US {d}: median not parsed (older central-tendency format?)")
                continue
            for y, v in res.items():
                recs.append(make_rows("Federal Reserve", "US", vint, qidx(y, 4), var, v, url))
    return recs


# ----------------------------------------------------------------------------------------
# Bank of Canada (CA): Staff Economic Projections database (Valet API groups SWP-PCPI = CPI and
# SWP-PCPIX = core CPI). One series per projection round (named by quarter, e.g. SWP-PCPI2015Q1);
# each holds the CPI INDEX LEVEL (real-time history plus projections). Released with a five-year lag
# (last round 2019Q4). Four-quarter growth 100*(L_t/L_{t-4}-1) is computed within the same round.
# Projection quarters = quarters >= the round's quarter. The exact date inside the quarter is not
# published: vintage_date is set to the last day of the round's quarter.
# ----------------------------------------------------------------------------------------
BOC = "https://www.bankofcanada.ca/valet/observations/group/{g}/csv"


def get_boc(refresh):
    recs = []
    for g, var in (("SWP-PCPI", "CPI_yoy_q"), ("SWP-PCPIX", "CPIX_core_yoy_q")):
        url = BOC.format(g=g)
        p = fetch(url, RAW / "boc" / f"{g}.csv", refresh, "CA")
        if p is None:
            log(f"CA: could not download {url}")
            continue
        t = p.read_text(encoding="utf-8-sig")
        d = pd.read_csv(io.StringIO(t[t.find('"OBSERVATIONS"') + len('"OBSERVATIONS"'):].strip()))
        d.index = [qidx(int(s[:4]), int(s[5])) for s in d["date"]]
        d = d.drop(columns="date").sort_index()
        for c in d.columns:
            m = re.fullmatch(rf"{g}(\d{{4}})Q(\d)", c)
            if not m or int(m.group(1)) < 1990:
                continue
            y, q = int(m.group(1)), int(m.group(2))
            vi = qidx(y, q)
            lvl = d[c].dropna()
            vint = pd.Timestamp(y, q * 3, 1) + pd.offsets.MonthEnd(0)
            for ti in lvl.index:
                if ti >= vi and (ti - 4) in lvl.index:
                    recs.append(make_rows("Bank of Canada", "CA", vint, ti, var, 100 * (lvl[ti] / lvl[ti - 4] - 1), url))
    return recs


# ----------------------------------------------------------------------------------------
# Reserve Bank of Australia (AU)
#  (a) 'Historical forecasts' (forecast date x event date), since 1990, published with ~1 year lag:
#      forecast-date-by-event-date.xls: sheets 'CPI - 4 quarter change' and 'Underlying - 4 quarter change'
#      (underlying = changing measure, see row 'Measure'). Forecast date is month-level (1st of month).
#  (b) 'Forecast archive' smp-forecast-archive.xlsx: Statement on Monetary Policy forecasts since
#      Nov 2018, year-ended CPI / trimmed mean at June and December only. Used only for SMP rounds
#      after the last round in (a).
# ----------------------------------------------------------------------------------------
RBA_HIST = "https://www.rba.gov.au/statistics/xls/forecast-date-by-event-date.xls"
RBA_SMP = "https://www.rba.gov.au/statistics/xls/smp-forecast-archive.xlsx"


def get_rba(refresh):
    import xlrd
    recs = []
    last_hist = pd.Timestamp("1900-01-01")
    p = fetch(RBA_HIST, RAW / "rba" / "forecast-date-by-event-date.xls", refresh, "AU")
    if p is not None:
        wb = xlrd.open_workbook(str(p))
        for sn, base in (("CPI - 4 quarter change", "CPI_yoy_q"), ("Underlying - 4 quarter change", "underlying_yoy_q")):
            sh = wb.sheet_by_name(sn)
            fd = sh.row_values(0)
            measure = sh.row_values(1) if sn.startswith("Underlying") else None
            for c in range(1, sh.ncols):
                if not isinstance(fd[c], float):
                    continue
                vint = pd.Timestamp(xlrd.xldate.xldate_as_datetime(fd[c], wb.datemode))
                vi = qidx_date(vint)
                var = base
                if measure is not None and str(measure[c]).strip():
                    var = base + "[" + re.sub(r"[^A-Za-z0-9]+", "_", str(measure[c]).strip()).strip("_") + "]"
                got = False
                for r in range(3, sh.nrows):
                    lab, v = str(sh.cell_value(r, 0)), sh.cell_value(r, c)
                    m = re.fullmatch(r"(\d{4})Q(\d)", lab)
                    if m and isinstance(v, float) and qidx(int(m.group(1)), int(m.group(2))) >= vi:
                        recs.append(make_rows("Reserve Bank of Australia", "AU", vint, qidx(int(m.group(1)), int(m.group(2))), var, v, RBA_HIST))
                        got = True
                if got:
                    last_hist = max(last_hist, vint)
    else:
        log("AU: historical forecast file not downloadable")
    p = fetch(RBA_SMP, RAW / "rba" / "smp-forecast-archive.xlsx", refresh, "AU")
    if p is not None:
        grid = read_grid(p, max_rows=60, max_cols=80)
        for sh, var in (("CPI", "CPI_yoy_q"), ("TMI", "trimmed_mean_yoy_q")):
            rows = grid.get(sh)
            if not rows:
                continue
            hdr = next(r for r in rows if r and norm(r[0]).startswith("Publication date"))
            for c in range(1, len(hdr)):
                if not hdr[c]:
                    continue
                vint = pd.to_datetime(str(hdr[c]), format="%b-%Y") if not isinstance(hdr[c], (dt.datetime, dt.date)) else pd.Timestamp(hdr[c])
                if vint <= last_hist:
                    continue
                for r in rows:
                    m = re.fullmatch(r"(\w{3})-(\d{4})", norm(r[0])) if r and r[0] else None
                    v = num(r[c]) if m and c < len(r) else None
                    if v is None:
                        continue
                    tm = pd.to_datetime(norm(r[0]), format="%b-%Y")
                    ti = qidx_date(tm)
                    if ti >= qidx_date(vint):
                        recs.append(make_rows("Reserve Bank of Australia", "AU", vint, ti, var, v, RBA_SMP))
    return recs


# ----------------------------------------------------------------------------------------
# Reserve Bank of New Zealand (NZ): rbnz.govt.nz answers automated requests with HTTP 403. This is
# only a probe that records the block; no workaround is attempted and no NZ data are produced.
# ----------------------------------------------------------------------------------------
def get_rbnz(refresh):
    url = "https://www.rbnz.govt.nz/monetary-policy/monetary-policy-statement"
    if fetch(url, RAW / "rbnz" / "mps.html", True, "NZ") is None:
        log("NZ: rbnz.govt.nz blocks automated access (HTTP 403); RBNZ forecasts not collected")
    return []


BANKS = {"se": get_riksbank, "no": get_norges, "gb": get_boe, "us": get_fed, "ca": get_boc, "au": get_rba, "nz": get_rbnz}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="re-download raw files")
    ap.add_argument("--only", default=",".join(BANKS), help="comma list of: " + ",".join(BANKS))
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    if set(a.only.split(",")) != set(BANKS) and a.out == str(OUT):
        a.out = str(RAW / "forecasts_partial.csv.gz")      # never overwrite the full file with a partial run
        print("partial run -> writing", a.out, file=sys.stderr)
    recs = []
    for k in a.only.split(","):
        print("== fetching", k, file=sys.stderr)
        r = BANKS[k](a.refresh)
        print(f"   {k}: {len(r)} records", file=sys.stderr)
        recs += r
    cols = ["bank", "country", "vintage_date", "target_period", "horizon_q", "variable", "value", "source_url"]
    df = pd.DataFrame(recs, columns=cols)
    df = df.drop_duplicates(["bank", "vintage_date", "target_period", "variable"], keep="first")
    assert (df.horizon_q >= 0).all()
    df["value"] = df["value"].round(4)
    df = df.sort_values(["bank", "variable", "vintage_date", "horizon_q"]).reset_index(drop=True)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(a.out, index=False, compression="gzip")
    RAW.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(MANIFEST, columns=["bank", "file", "url", "status", "download_date"]).drop_duplicates().to_csv(RAW / "manifest.csv", index=False)
    (RAW / "run_notes.txt").write_text("\n".join(LOG))
    g = df.groupby(["bank", "variable"]).agg(rows=("value", "size"), vintages=("vintage_date", "nunique"),
                                            first=("vintage_date", "min"), last=("vintage_date", "max"),
                                            hmax=("horizon_q", "max"))
    print(g.to_string())
    print("wrote", a.out, os.path.getsize(a.out) // 1024, "KB,", len(df), "rows")


if __name__ == "__main__":
    main()
