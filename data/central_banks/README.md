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

## Official forecasts
Published central-bank inflation forecasts, collected 2026-11-22 by `code/fetch_cb_forecasts.py` (raw downloads cached in `/tmp/cbfc/<bank>/`, manifest with URLs and download dates in `/tmp/cbfc/manifest.csv`; needs `pandas`, `requests`, `openpyxl`, `xlrd`). Output: `forecasts.csv.gz` (about 10,600 rows, 74 KB) with columns `bank, country (ISO2), vintage_date, target_period (YYYY-Qn), horizon_q, variable, value, source_url`. `vintage_date` is the publication date of the forecast round; `horizon_q` = target quarter minus quarter of `vintage_date` (0 = current-quarter projection/nowcast). Values are per cent. All sources are the banks' own files; no third-party compilation was used.

| bank | variable(s) in file | what it is | vintages (rounds) | horizons | source |
|---|---|---|---|---|---|
| Sveriges Riksbank (SE) | `CPI_yoy_qavg`, `CPIF_yoy_qavg` | CPI / CPIF annual % change; the Riksbank publishes MONTHLY paths, converted here to quarters as the mean of the 3 monthly y/y rates (quarter kept only if all 3 months exist and at least one is a forecast month) | CPI 2007-02-15 to 2026-09-24 (106 rounds); CPIF 2008-07-03 to 2026-09-24 (100). 2020:2 is absent (the Riksbank published scenarios, not a forecast) | 0-12 | riksbank.se `/globalassets/media/statistik/makro/eng/outcome-and-forecasts.xlsx` (2015:1 on) and `forecasts-and-outcomes-2007-2014.xlsx`; layout in `forecasts-and-outcomes-description-of-datasheet.pdf` |
| Norges Bank (NO) | `CPI_4q`, `CPI-ATE_4q` | CPI and CPI-ATE (CPI adjusted for tax changes, excluding energy) four-quarter change, central (baseline) projection | 2013-09-19 to 2026-09-24, every MPR (53 rounds) | 0-15 | per-report data files linked from `norges-bank.no/en/news-events/publications/Monetary-Policy-Report/<year>/<slug>/` (xlsx; table 'Projections for main economic aggregates' where present, else the fan-chart/Data A sheet). Vintage = 'Published' date on the report page |
| Bank of England (GB) | `CPI_yoy_q` | four-quarter CPI inflation, central projection | Feb 2004 to Nov 2026, 91 Inflation Reports / MPRs | 0-12 | 'Projections Databank CSV' inside `mpr-november-2026-charts-slides-and-data.zip` on the BoE MPR page |
| Federal Reserve (US) | `PCE_median_Q4Q4`, `corePCE_median_Q4Q4` | SEP MEDIAN projection of PCE and core PCE inflation, Q4/Q4; target period is Q4 of each projected year | 2015-09-17 to 2026-09-16, 44 SEPs (none in 2020 Q1) | 2-13 (annual points only) | `federalreserve.gov/monetarypolicy/fomcprojtabl<yyyymmdd>.htm` (HTML tables, parsed) |
| Bank of Canada (CA) | `CPI_yoy_q`, `CPIX_core_yoy_q` | four-quarter growth of staff projection of CPI and core CPI (computed from the index levels in the Staff Economic Projections database) | quarterly rounds 1990Q1-2019Q4 (120); database is released with a 5-year lag | 0-11 (fewer in early rounds) | Valet API groups `SWP-PCPI`, `SWP-PCPIX` (`bankofcanada.ca/valet/observations/group/<g>/csv`) |
| Reserve Bank of Australia (AU) | `CPI_yoy_q` (year-ended CPI); `underlying_yoy_q[<measure>]`, `trimmed_mean_yoy_q` | year-ended CPI and the RBA's underlying measure (the measure changed over time; its name is in the brackets) | 1990-03 to 2026-11, 146 rounds | 0-10 | `rba.gov.au/statistics/xls/forecast-date-by-event-date.xls` (1990 to Feb 2025) and `smp-forecast-archive.xlsx` (SMP rounds after that, June and December targets only) |

Not collected: **Reserve Bank of New Zealand** - rbnz.govt.nz returns HTTP 403 to automated requests (page and file URLs); recorded and not circumvented. Norges Bank rounds before Sep 2013 (data files expose only fan-chart bands, not a labelled central path, or no file), Riksbank before 2007 and CPIX, BoE before 2004 and Bank of Canada after 2019 (published only as PDF tables) are not in the file. No openly available, citable cross-country compilation of central-bank forecast vintages was found (searched; the closest items are academic papers that build their own panels from the banks' files without public replication archives), so none is used.

Caveats for use:
- Variable vs target index: the Riksbank's target variable is CPIF since 2017 (CPI before; both are in the file, CPIF forecasts only from 2008-07); Norges Bank targets CPI; BoE targets CPI; Fed targets PCE (headline, Q4/Q4 medians, annual only); BoC targets total CPI (core CPIX is also given); RBA targets CPI (year-ended). RBA underlying measures are not comparable across measure labels.
- Precision of `vintage_date`: exact publication dates for Riksbank, Norges Bank and Fed. BoE and RBA give only month (set to the 1st of the month); BoC gives only the projection quarter (set to the last day of that quarter). Joins to policy decisions within the same month/quarter need care.
- `horizon_q = 0` is a current-quarter projection and can partly consist of known outcomes (e.g. Riksbank months already published, RBA 'nowcast' - the RBA notes that its t-point is not a clean one-step-ahead forecast). RBA historical data were released with a lag and spliced from internal papers (JEFG, PDG, board papers, SMP; see the workbook notes and Tulip and Wallace 2012).
- Conditioning differs: Riksbank/Norges Bank/BoE/BoC projections are conditional on the bank's own or market interest-rate path (BoE: market curve in recent years, constant rate earlier); Fed SEP is conditioned on each participant's own appropriate policy. Distinct from private-sector forecasts.
- Bank of Canada projection quarters far out (roughly beyond 8 quarters) often sit at about 2.0 mechanically (target-consistent), so long-horizon BoC values carry little information about the bank's own view; treat with care when inferring the target.
- Riksbank quarterly values are means of monthly y/y rates, which differ slightly from a published quarterly y/y.
- Norges Bank projection quarters are those from the quarter of publication on (checked against the 'Projections' marker in the 2021-2024 tables). Where several sheets contained a series, the table was preferred over chart sheets, and sheets about alternative/conditional paths were excluded; the choice is logged by the script in `/tmp/cbfc/run_notes.txt`.
- Fed SEP medians for Mar and Jun 2015 and earlier are not parsed (those tables show central tendency/range only); 2012-2014 SEPs likewise.
- Licence/terms of each source were not reviewed in detail; cite the banks (links above) when redistributing.
