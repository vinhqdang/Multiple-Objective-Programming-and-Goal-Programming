"""Aid tables for paper2 (second revision): test results with B = 999 PA test (i.i.d. and block residuals),
combined Benjamini-Hochberg rule over max(p_state, p_PA), sets truncated at 0, and the goal table over all
donors with a documented goal (national goals and the EU-15 0.7% by 2015 commitment)."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd
from permutation_extend import bh
ax = pd.read_csv("results/aid_exact.csv").set_index("donor")
tr = pd.read_csv("results/aid_sets_truncated.csv").set_index("donor")
pe = pd.read_csv("results/permutation_extend.csv"); pe = pe[pe.domain == "aid"].set_index("unit")
pn = pd.read_csv("results/pa_null_extend.csv"); pn = pn[pn.domain == "aid"].set_index("unit")
gd = pd.read_csv("results/aid_gni_drift.csv").set_index("donor")
bs = pd.read_csv("results/aid_bootstrap_exact.csv").set_index("donor")
d = pd.DataFrame({"p_state": pe.p, "p_pa_iid": pn.p_iid, "p_pa_block": pn.p_block})
d["q_state"] = bh(d.p_state.values); d["q_pa_iid"] = bh(d.p_pa_iid.values); d["q_pa_block"] = bh(d.p_pa_block.values)
d["q_comb_iid"] = bh(d[["p_state", "p_pa_iid"]].max(axis=1).values)
d["q_comb_block"] = bh(d[["p_state", "p_pa_block"]].max(axis=1).values)
d = d.join(ax[["n", "tau", "band_lo", "band_hi", "step_cut", "step_raise", "mean_level"]]).join(tr[["set2_lo", "set2_hi", "tau_minus_mean"]])
d.round(4).to_csv("results/aid_combined_tests.csv", index_label="donor")
d = d.sort_values(["q_comb_iid", "q_comb_block", "q_pa_iid"])
L = [r"\begin{tabular}{lrccccrcccc}\toprule",
     r"Donor & $n$ & \hd{State\\dep.} & \hd{PA\\i.i.d.} & \hd{PA\\block} & \hd{Both\\(i.i.d.; block)} & $\hat\tau$ & Band & \hd{$\tau$ set\\(2\%)} & \hd{Steps\\(down, up)} & \hd{$\hat\tau-{}$\\mean}\\\midrule"]
for k, r in d.iterrows():
    star = r"$^{\dagger}$" if r.q_comb_iid <= 0.10 else ""
    L.append(f"{k}{star} & {int(r.n)} & {r.q_state:.2f} & {r.q_pa_iid:.2f} & {r.q_pa_block:.2f} & {r.q_comb_iid:.2f}; {r.q_comb_block:.2f} & {r.tau:.2f} & "
             f"[{r.band_lo:.2f}, {r.band_hi:.2f}] & ({r.set2_lo:.2f}, {r.set2_hi:.2f}) & {r.step_cut:.2f}, {r.step_raise:.2f} & {(round(r.tau_minus_mean, 2) + 0.0):+.2f}\\\\")
L.append(r"\bottomrule\end{tabular}"); open("paper2/tab_aid.tex", "w").write("\n".join(L))
goals = [("SWE", 1.0, "1.0 (N, to 2022)"), ("NOR", 1.0, "1.0 (N, 2005)"), ("LUX", 1.0, "1.0 (N, 1999)"),
         ("DNK", 0.8, "0.8 (N, 2011)"), ("NLD", 0.7, "0.7 (N, 2012)"), ("GBR", 0.7, "0.7 (S, 2015)")]
for c in ["AUT", "BEL", "DEU", "ESP", "FIN", "FRA", "IRL", "ITA", "PRT"]: goals.append((c, 0.7, "0.7 (EU, 2015)"))
L = [r"\begin{tabular}{llcccccc}\toprule",
     r"Donor & Goal & \hd{Revealed\\band} & \hd{$\tau$ set\\(2\%)} & \hd{Bootstrap\\90\%} & \hd{Goal in\\band; set; boot.} & \hd{GNI-adjusted\\$\hat\tau$ (set)} & \hd{Both tests\\(BH)}\\\midrule"]
rows = []
for c, g, lab in goals:
    r = d.loc[c]; inb = r.band_lo <= g <= r.band_hi; ins = r.set2_lo <= g <= r.set2_hi
    gr = gd.loc[c] if c in gd.index else None
    gs = f"{gr.tau:.2f} ({gr.set_lo:.2f}, {gr.set_hi:.2f})" if gr is not None else "--"
    ging = (gr.set_lo <= g <= gr.set_hi) if gr is not None else np.nan
    bb = bs.loc[c]; inbo = bb.boot_q05 <= g <= bb.boot_q95
    rows.append(dict(donor=c, goal=g, in_band=inb, in_set=ins, in_boot=inbo, in_set_gni=ging, q_comb_iid=r.q_comb_iid))
    L.append(f"{c} & {lab} & [{r.band_lo:.2f}, {r.band_hi:.2f}] & ({r.set2_lo:.2f}, {r.set2_hi:.2f}) & ({bb.boot_q05:.2f}, {bb.boot_q95:.2f}) & {'yes' if inb else 'no'}; {'yes' if ins else 'no'}; {'yes' if inbo else 'no'} & {gs} & {r.q_comb_iid:.2f}\\\\")
L.append(r"\bottomrule\end{tabular}"); open("paper2/tab_aid_goals.tex", "w").write("\n".join(L))
pd.DataFrame(rows).to_csv("results/aid_goal_comparison.csv", index=False)
print(pd.DataFrame(rows).to_string(index=False))
