# Central-bank domain data (baseline / ground-truth domain)

Downloaded 2026-11-22 by `code/fetch_central_banks.py` (re-run to refresh; needs `pandas`, `requests`). All files gzip CSV, each well under 1 MB.

| file | content | source / id | coverage | unit |
|---|---|---|---|---|
| `policy_rate_monthly.csv.gz` | central-bank policy rate, end of month (`period, area, policy_rate, source_ref`) | BIS SDMX dataflow `BIS:WS_CBPOL(1.0)`, key `M` | 49 areas (ISO2, `XM` = euro area), 1945-01..2026-10 (US from 1954-07, euro area from 1999-01); many euro-area members stop in 1998/2000 | per cent per annum |
| `cpi_yoy_monthly.csv.gz` | CPI inflation y/y (`period, area, cpi_yoy`) | BIS `WS_LONG_CPI(1.0)`, key `M`, `UNIT_MEASURE=771` | 63 areas, 1914-01..2026-09 | per cent y/y (checked: equals y/y change of the index series `UNIT_MEASURE=628`) |
| `gdp_growth_yoy_quarterly.csv.gz` | real GDP growth y/y (`period, area_iso3, gdp_growth_yoy`) | OECD `OECD.SDD.NAD:DSD_NAMAIN1@DF_QNA_EXPENDITURE_GROWTH_OECD(1.1)`, key `Q.Y..S1.S1.B1GQ._Z._Z._Z.PC.L.GY.T0102` | 53 areas (incl. aggregates EA, EU, G7, G20, OECD), 1948-Q1..2026-Q3 | per cent y/y, volume |
| `output_gap_annual.csv.gz` | output gap (`year, area_iso3, output_gap_pct`) | OECD Economic Outlook `OECD.ECO.MAD:DSD_EO@DF_EO(1.5)`, measure `GAP`, freq `A` | 41 areas, 1985..2027 (includes OECD projections for recent years) | per cent of potential GDP |
| `worldbank_annual.csv.gz` | annual GDP growth, unemployment (`year, area_iso3, gdp_growth, unemployment_rate`) | World Bank API indicators `NY.GDP.MKTP.KD.ZG`, `SL.UEM.TOTL.ZS` | 259 economies/aggregates, 1961..2025 | per cent |
| `country_crosswalk.csv.gz` | ISO2 (BIS) to ISO3 (OECD/WB) | World Bank country API, plus `XM`->`EA` | | |
| `targets.csv` | explicit inflation targets (see below) | see per-row `source_url` | 15 banks incl. 6 emerging-market, 24 rows | |
| `download_date.txt` | date of last run | | | |

## Notes and caveats
- BIS API quirk: the `all` key returns "No results"; an explicit frequency key (`M`) is required. Policy-rate definitions differ across countries (see `source_ref`; the BIS series carries per-country footnotes in the raw `COMPILATION`/`SUPP_INFO_BREAKS` fields, not kept here - re-fetch if needed).
- Euro-area members before 1999 are national rates (Bundesbank, Banque de France ...); use `XM` from 1999-01.
- The activity measures are annual (output gap, World Bank) or quarterly (GDP growth); the output gap is an OECD estimate, so recent values are projections, not real-time data. No unemployment or output-gap series is monthly. Real-time vintages are not included, which matters for estimating decision rules (see docs/lit/13).
- Inflation index differs from the targeted index (e.g. Fed targets PCE, Riksbank CPIF, ECB HICP); BIS CPI is headline CPI. Matching the targeted index is a task for the analysis step.
- Licence/terms: not reviewed in detail at download time. BIS statistics: https://www.bis.org/terms_conditions.htm ; OECD data: https://www.oecd.org/en/about/terms-conditions.html ; World Bank open data: https://www.worldbank.org/en/about/legal/terms-of-use-for-datasets . Cite the sources above if redistributing.

## targets.csv
Columns: `bank, country (ISO2; EA = euro area), target_value, band_low, band_high, from_date, to_date, source_url`, plus `index` (targeted price index), `note`, `verification`. Empty `to_date` = still in force at 2026-11-22; empty `from_date` = start date not retrieved.
`verification` states how each row was checked in this session:
- "page fetched": text of the cited page read (Fed 2012 statement, ECB 2003 press release and strategy page, Bank of England inflation page, Bank of Canada ICT page, RBA, BoJ).
- "search result summary": values taken from a web-search result summary that cites the listed URL, but the page body was not itself read (RBNZ, Riksbank, Norges Bank, Brazil, Mexico, Chile, India, South Africa, Poland, BoE 1997-2003). These rows should be re-checked against the primary page before publication; central-bank sites often blocked automated fetching (HTTP 403/404).
- Several start dates are approximate and marked as such in `note`. Rows not retrievable (e.g. earlier RBNZ remits, Bank of Canada pre-2001 levels, RBA adoption date, Brazil before 2025) are deliberately omitted rather than filled from memory.
- Treat ECB `to_date`/`from_date` around mid-2021 as month-level.
