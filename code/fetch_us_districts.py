"""Download US school-district finance, enrollment and graduation rates from the Urban Institute
Education Data Portal (https://educationdata.urban.org/documentation/). Public, no key."""
import requests, pandas as pd, time, sys
B = "https://educationdata.urban.org/api/v1/school-districts/"
def get_all(path, params=None):
    url, rows, p = B + path, [], dict(params or {})
    while url:
        for k in range(6):
            try:
                r = requests.get(url, params=p, timeout=180); r.raise_for_status(); j = r.json(); break
            except Exception as e:
                time.sleep(3 * (k + 1))
        else:
            raise RuntimeError(f"failed {url}")
        rows += j["results"]; url = j["next"]; p = None
    return pd.DataFrame(rows)
FIN = ["year","leaid","fips","enrollment_fall_responsible","rev_total","rev_fed_total","rev_state_total","rev_local_total",
       "exp_total","exp_current_elsec_total","exp_current_instruction_total","exp_current_supp_serv_total",
       "salaries_total","salaries_instruction"]
fin, enr, grad = [], [], []
for y in range(2010, 2020):
    f = get_all(f"ccd/finance/{y}/"); fin.append(f[[c for c in FIN if c in f.columns]]); print("fin", y, len(f), flush=True)
    e = get_all(f"ccd/enrollment/{y}/grade-99/", {"race": 99, "sex": 99}); enr.append(e[["year","leaid","enrollment"]]); print("enr", y, len(e), flush=True)
    if y >= 2011:
        g = get_all(f"edfacts/grad-rates/{y}/", dict(race=99, disability=99, lep=99, econ_disadvantaged=99, homeless=99, foster_care=99))
        grad.append(g[["year","leaid","cohort_num","grad_rate_low","grad_rate_high","grad_rate_midpt"]]); print("grad", y, len(g), flush=True)
pd.concat(fin).to_csv("data/us_districts/finance.csv.gz", index=False)
pd.concat(enr).to_csv("data/us_districts/enrollment.csv.gz", index=False)
pd.concat(grad).to_csv("data/us_districts/grad_rates.csv.gz", index=False)
