# COFOG government budgets, fiscal aggregates and published targets

Downloaded 2026-11-22 with `code/fetch_cofog.py` (rerun to refresh: `python3 code/fetch_cofog.py`; NATO part needs `pdftotext`, skip with `--no-nato`).

## Files (all < 1 MB)
| file | source / dataset | content |
|---|---|---|
| `gov_10a_exp.csv.gz` | Eurostat `gov_10a_exp`, SDMX-CSV bulk API, key `A.PC_GDP+PC_TOT+MIO_EUR.S13..TE.` | General government (S13) total expenditure (TE) by COFOG: 10 divisions GF01..GF10, all groups (GF0101..GF1009) and TOTAL; units % of GDP, % of total expenditure, million EUR. Last update stamp in source 2026-10-21. |
| `gov_10dd_edpt1.csv.gz` | Eurostat `gov_10dd_edpt1`, key `A.PC_GDP+MIO_EUR.S13.B9+GD.` | B9 net lending/borrowing and GD gross debt (Maastricht), S13, % of GDP and million EUR |
| `nama_10_gdp.csv.gz` | Eurostat `nama_10_gdp`, key `A.CP_MEUR.B1GQ.` | GDP at current market prices, million EUR |
| `demo_pjan.csv.gz` | Eurostat `demo_pjan`, key `A.NR.TOTAL.T.` | Population on 1 January, total |
| `nato_defence_pc_gdp.csv.gz` | NATO, "Defence Expenditure of NATO Countries (2014-2025)", press-release PDF, Table 3 (share of real GDP, 2021 prices), cut-off 3 June 2025; parsed from the PDF text | 31 allies listed plus two NATO aggregates, 2014-2025 (2024-2025 flagged `estimate`) |
| `targets.csv` | hand-curated, columns `target,value,unit,applies_to,from_year,source_url` | published targets, see below |

Columns of the Eurostat files are the SDMX-CSV ones (`freq, unit, sector, cofog99, na_item, geo, TIME_PERIOD, OBS_VALUE, OBS_FLAG`; dataflow and confidentiality columns dropped). Flags: `p` provisional, `b` break in series, `m` missing (OBS_VALUE empty); consult Eurostat flag list for exact wording. `geo` uses Eurostat codes (EL = Greece, aggregates EA19/EA20/EA21/EU27_2020 are included and must be dropped for country panels).

## Coverage (checked after download)
- `gov_10a_exp`: 212,024 rows; years 1990-2025. 34 geo codes = 30 countries (all 27 EU members plus CH, IS, NO) + 4 aggregates. Per country the span is 1995-2024 (30 years) for most; FI starts 1990, IS 1998, LU runs to 2025; SK, and the EA/EU aggregates, only 2010-2024. GF01..GF10 in % of GDP are complete (no gaps) for 948 geo-year cells, 888 of them for individual countries. Subdivisions are sparser: 1,580 rows with flag `m` (empty value), all in LT, BG, PT.
- `gov_10dd_edpt1`: 31 geo codes (27 EU members + 4 aggregates), 1995-2025; essentially complete, 2 flagged `b`.
- `nama_10_gdp`: 46 geo codes, 1975-2025. `demo_pjan`: 59 geo codes, 1960-2025.
- NATO table: one missing value (Germany 2025e, `..` in source). The NATO PDF of 2026 (`def-exp-2026-en.pdf`) is an image-only print-to-PDF without a text layer; it was not parsed (no OCR done). NATO's open Excel file was not found linked on the topic page, so the PDF table is the series used.
- Eurostat values for COFOG in % of GDP are published with one decimal; this limits precision for small functions.

## Definitions caution
Eurostat COFOG division GF02 (defence, general government) and NATO's defence expenditure follow different definitions and GDP bases. 2023 examples (Eurostat GF02 % GDP vs NATO Table 3): PL 2.2 vs 3.27, DE 1.2 vs 1.61, LU 0.5 vs 1.06, EE 3.1 vs 3.0. Do not mix the two without modelling the gap; the 2% guideline is defined on NATO's definition.

## Licence
Eurostat data: free reuse with attribution under the Eurostat/Commission reuse policy (terms not re-fetched for this README; check the Eurostat copyright notice before redistribution). NATO table: published by NATO press service, used here for research with source attribution; check NATO terms before redistribution.

## Targets table (`targets.csv`)
Each row comes from a page fetched during preparation (verbatim figures confirmed on the page):
- NATO Wales Summit Declaration, 5 Sep 2014, para 14: 2% of GDP guideline (Allies below to move towards it within a decade), 20% of defence budgets on major equipment incl. R&D.
- NATO Vilnius Summit Communiqué, 11 Jul 2023, paras 27-28: "at least 2%" as enduring commitment; at least 20% on major equipment.
- NATO Hague Summit Declaration, 25 Jun 2025: 5% of GDP annually (3.5% core defence by the NATO definition plus up to 1.5% related spending) by 2035; annual plans; review in 2029.
- Protocol No 12 on the excessive deficit procedure, Art. 1 (EUR-Lex consolidated text): 3% deficit and 60% debt reference values. `from_year` left empty because the entry-into-force date was not retrieved.
- Barcelona European Council 15-16 Mar 2002: approach 3% of GDP R&D by 2010 (CORDIS news item, secondary source; the Presidency Conclusions were not retrieved). Europe 2020 (COM(2010) 2020): 3% R&D, early school leavers below 10%, tertiary attainment at least 40%. These are EU-level targets, to be translated into national ones.
Not found/retrieved (gaps): national Europe 2020 R&D targets by country (only fragments seen in search snippets, not used), any EU or national targets for health or education spending as % of GDP, the reformed SGP (2024) expenditure-path rules. The Europe 2020 education items are outcome targets, not budget shares.
