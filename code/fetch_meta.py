import json, re, requests
dois = """s10479-026-07356-x s10479-026-07364-x s10479-026-07355-y s10479-026-07272-0 s10479-026-07270-2 s10479-026-07265-z s10479-026-07173-2 s10479-026-07223-9 s10479-026-07192-z s10479-026-07229-3 s10479-026-07143-8 s10479-026-07177-y s10479-025-06954-5 s10479-025-06918-9 s10479-025-06912-1 s10479-025-06763-w s10479-024-06413-7 s10479-024-06330-9 s10479-024-06325-6""".split()
out = []
for i, s in enumerate(dois, 1):
    d = "10.1007/" + s
    row = dict(n=i, doi=d)
    try:
        m = requests.get(f"https://api.crossref.org/works/{d}", timeout=30).json()["message"]
        row["title"] = m["title"][0]
        row["abstract_crossref"] = re.sub(r"<[^>]+>", " ", m.get("abstract", "")).strip()
        row["cc_license"] = any("creativecommons" in l["URL"] for l in m.get("license", []))
    except Exception as e:
        row["crossref_error"] = str(e)
    try:
        o = requests.get(f"https://api.openalex.org/works/doi:{d}", timeout=30).json()
        row["is_oa"] = o["open_access"]["is_oa"]; row["oa_url"] = o["open_access"]["oa_url"]
        idx = o.get("abstract_inverted_index")
        if idx:
            pos = sorted((p, w) for w, ps in idx.items() for p in ps)
            row["abstract_openalex"] = " ".join(w for _, w in pos)
    except Exception as e:
        row["openalex_error"] = str(e)
    out.append(row)
json.dump(out, open("results/paper_metadata.json", "w"), indent=1)
for r in out:
    print(r["n"], "OA" if r.get("is_oa") else "CLOSED", "| abs:", bool(r.get("abstract_crossref") or r.get("abstract_openalex")), "|", r.get("title","?")[:70])
