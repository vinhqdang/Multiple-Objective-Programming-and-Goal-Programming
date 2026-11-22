# Foreign-aid data for inverse goal programming

Downloaded 2026-11-22 by `code/fetch_aid.py` (run from anywhere: `python code/fetch_aid.py`, or with step names `lookups dac2a dac1 recipients_oecd worldbank`). Needs `requests`, `pandas`; about 10 minutes. All files are gzip CSV, each below 10 MB.

## Files
| file | content | rows |
|---|---|---|
| `dac2a_oda_donor_recipient_year.csv.gz` | OECD DAC2A, net ODA disbursements (measure 206), donor x recipient x year, 1960-2024. Columns: donor, recipient, year, price_base (Q = constant 2024 USD, V = current USD), oda_musd (USD million), base_year, obs_status | 1,115,302 (557,651 per price base) |
| `dac1_donor_oda_gni.csv.gz` | OECD DAC1, donor totals (SECTOR=_Z): ODA/GNI (measure 2, net-disbursement basis, 1960-2017, flow 1140, percent; measure 11002, grant-equivalent basis, 2018-2024, flow 1160, percent), ODA volumes (measure 1010 net, 11010 grant equivalent, several flow types, USD and local currency) | 49,202 |
| `recipient_oecd_gni_pop.csv.gz` | OECD DF_IND: recipient population (thousands), GNI current (USD million), GNI per capita (USD); see unit/unit_mult columns | 29,088 |
| `worldbank_recipient_indicators.csv.gz` | World Bank WDI via API v2, iso3 x year 1960-2024: GDP per capita constant 2015 USD, GDP per capita PPP constant, population, poverty headcount at 3.00 USD/day (2021 PPP), Gini, infant mortality, life expectancy, GNI per capita Atlas | 17,210 |
| `worldbank_country_meta.csv.gz` | iso3, name, region, income group, lending type (IDA/IBRD/blend) from the current WB classification. Region "Aggregates" marks non-countries | 296 |
| `oecd_area_codes.csv.gz` | names for OECD DONOR/RECIPIENT codes (CL_AREA_ORG) | 659 |
| `ldc_list_dec2024.csv` | the 44 UN least developed countries (December 2024 snapshot) with ISO3 | 44 |
| `targets.csv` | publicly stated targets usable as ground truth, with source URL and a `verification` column saying what was actually read | 15 |

## Sources, identifiers, licence
- OECD SDMX API `https://sdmx.oecd.org/public/rest/data/<flow>/<key>`; dataflows `OECD.DCD.FSD,DSD_DAC2@DF_DAC2A,1.7` (key DONOR.RECIPIENT.MEASURE.UNIT_MEASURE.PRICE_BASE, used `..206.USD.Q` and `..206.USD.V`), `OECD.DCD.FSD,DSD_DAC1@DF_DAC1,1.8` (key DONOR.SECTOR.MEASURE.TYING_STATUS.FLOW_TYPE.UNIT_MEASURE.PRICE_BASE), `OECD.DCD.FSD,DSD_GDFF@DF_IND,1.0`. Dataflow catalogue: `https://sdmx.oecd.org/public/rest/dataflow/OECD.DCD.FSD/all`. Other dataflows available but not fetched: DF_DAC3A (commitments), DF_CRS (project level, sector), DF_CPA (country programmable aid), DF_DEFL (deflators), DF_MULTI. OECD data terms: https://www.oecd.org/en/about/terms-conditions.html (page not fetched here; check before redistribution; OECD data are generally reusable with attribution).
- World Bank API `https://api.worldbank.org/v2/` (WDI source 2; last updated 2026-11-11 per API). WDI licence CC BY 4.0 per World Bank Data terms (not re-verified here).
- LDC list: https://unctad.org/topic/least-developed-countries/list (text read 2026-11-22, lists 44 LDCs, Dec 2024).

## Coverage
- DAC2A: 1960-2024; 181 donor codes, 277 recipient codes. Donor codes include 32 individual DAC-type bilateral donors (e.g. DEU, USA, GBR, JPN, FRA), aggregates (DAC, DAC_EC, G7, ALLD, ALLM, WXDAC), UN agencies (1UN...), EU institutions (4EU...), development banks (5...), vehicles (9OTH..., 9PRIV...). Recipient codes: 169 are countries/territories found in the World Bank list; the rest are aggregates (LDC, LMIC, UMIC, DPGC, regions) or multilateral/unallocated codes. Use `oecd_area_codes.csv.gz` and `worldbank_country_meta.csv.gz` to filter.
- Core panel (32 bilateral donors x country recipients, constant prices): 126,425 donor-recipient-year rows, 169 recipients, 1960-2024. Donors present each year: 14 in 1960, 20 in 1984, 27 in 2000, 32 in 2016-2024. Recipients per year about 93 in 1960, 140 in 1984, 135-156 after 1990. Donor first years differ (e.g. CZE 1998, SVN 2008, KOR 1987, ESP 1987).
- DAC1 ODA/GNI: 32 bilateral donors, 1960-2024 (full for the older members, later start for newer: e.g. SVN 2005, EST 2004, LVA/LTU 2003). Series break in 2018 (switch from net-disbursement to grant-equivalent measure); the two measures do not overlap in the file. Spot check against statute: GBR 0.70 in 2013 and 2020, 0.50 in 2021, matches the UK target history in `targets.csv`.
- LDC consistency check: DAC2A aggregate LDC for DEU in 2020 equals the sum over the 44-country list (4,039.07 USD million, constant prices).
- World Bank indicators, 1990-2023 share of non-missing rows: population 100%, life expectancy 100%, GDP per capita constant 95%, infant mortality 92%, GNI per capita Atlas 91%, PPP GDP per capita 91%, poverty headcount 30% (survey years only), Gini 25%.

## Units and conventions
- `oda_musd`: USD million (UNIT_MULT = 6). Constant prices are 2024 USD (`base_year` = 2024). Values can be negative (net of loan repayments; 4,870 negative and 206 zero rows in the core panel). A donor-recipient-year absent from the file is not reported by OECD; zero and not-reported cannot be distinguished except where an explicit 0 appears. All rows have obs_status A (normal value).
- ODA/GNI is in percent (e.g. 0.7 = 0.7%).
- Net disbursement (measure 206) is bilateral ODA by recipient; multilateral core contributions are not attributed to recipients here (use DF_MULTI for imputed shares).

## Limitations
- Bilateral net disbursements, not commitments; no sector or channel breakdown (CRS not fetched; very large).
- LDC and income classifications are current snapshots (WB) or Dec 2024 (UN list); status at each historical year is not reconstructed. OECD aggregate `LDC` in DAC2A follows the DAC list of its year.
- No political or commercial variables (UN voting, trade, colonial ties) are included; these are needed for the "alignment" and "commerce" goals and must be added from other sources (UN voting data, CEPII gravity data).
- Poverty and Gini are sparse for early years; Atlas GNI per capita begins 1962 or later for some countries.
