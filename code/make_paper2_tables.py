"""Generate LaTeX tables for paper2 from result files."""
import pandas as pd, numpy as np, os
os.makedirs("paper2", exist_ok=True)
e = pd.read_csv("results/real_cb_quad.csv"); e = e[e.input == "realised"]
c = pd.read_csv("results/confirmatory_cb.csv"); c = c[c.status == "included"]
def tab(df, tcol, mcol, cap_rows):
    L = [r"\begin{tabular}{lrrrrr}\toprule", r"Bank & $n$ & Stated & Implied $\hat\tau$ & Mean inflation & Closer \\\midrule"]
    for _, r in df.iterrows():
        closer = "implied" if abs(r[tcol] - r.stated) < abs(r[mcol] - r.stated) else "mean"
        L.append(f"{r.country} & {int(r.n)} & {r.stated:.1f} & {r[tcol]:.2f} & {r[mcol]:.2f} & {closer}\\\\")
    m1, m2 = np.abs(df[tcol] - df.stated).mean(), np.abs(df[mcol] - df.stated).mean()
    L += [r"\midrule", f"MAE & & & {m1:.2f} & {m2:.2f} & \\\\", r"\bottomrule\end{tabular}"]
    return "\n".join(L)
open("paper2/tab_cb_exploratory.tex", "w").write(tab(e, "tau_pi", "mean_x", None))
open("paper2/tab_cb_confirmatory.tex", "w").write(tab(c, "tau_pi", "mean_infl", None))
if os.path.exists("results/bootstrap_cb_full_summary.csv"):
    b = pd.read_csv("results/bootstrap_cb_full_summary.csv")
    L = [r"\begin{tabular}{lrrrrc}\toprule", r"Bank & Stated & 5\% & Median & 95\% & Covers stated \\\midrule"]
    for _, r in b.iterrows():
        L.append(f"{r.country} & {r.stated:.1f} & {r.lo:.2f} & {r.med:.2f} & {r.hi:.2f} & {'yes' if r.covers_stated else 'no'}\\\\")
    L.append(r"\bottomrule\end{tabular}"); open("paper2/tab_cb_bootstrap.tex", "w").write("\n".join(L))
print("ok")

a = pd.read_csv("results/applications_gp_aid_defence_firms.csv")
def fmt(v): return "--" if pd.isna(v) else f"{v:.2f}"
ax = pd.read_csv("results/aid_exact.csv").sort_values("tau", ascending=False)
import os
from permutation_extend import bh
pe = pd.read_csv("results/permutation_extend.csv") if os.path.exists("results/permutation_extend.csv") else None
pt = (pe[pe.domain == "aid"] if pe is not None else pd.read_csv("results/permutation_test.csv").query("domain == 'aid'")).set_index("unit")
pt["p_bh"] = bh(pt.p.values)
pn = pd.read_csv("results/pa_null_test.csv").set_index("unit"); pn["p_bh"] = bh(pn.p.values)
ax["p1"] = ax.donor.map(pt.p); ax["q1"] = ax.donor.map(pt.p_bh); ax["p2"] = ax.donor.map(pn.p); ax["q2"] = ax.donor.map(pn.p_bh)
ax = ax.sort_values(["q2", "q1", "tau"], ascending=[True, True, False])
L = [r"\begin{tabular}{lrcccccc}\toprule",
     r"Donor & $n$ & \hd{State dependence\\$p$ (BH)} & \hd{GP vs PA\\$p$ (BH)} & $\hat\tau$ & \hd{Band\\($\tau$ set, 2\%)} & \hd{Steps\\(down, up)} & Mean\\\midrule"]
for _, r in ax.iterrows():
    star = r"$^{\dagger}$" if (r.q1 <= 0.10 and r.q2 <= 0.10) else ""
    L.append(f"{r.donor}{star} & {int(r.n)} & {r.p1:.3f} ({r.q1:.2f}) & {r.p2:.3f} ({r.q2:.2f}) & {r.tau:.2f} & \\hd{{[{r.band_lo:.2f}, {r.band_hi:.2f}]\\\\({r.set2[1:-1]})}} & {r.step_cut:.2f}, {r.step_raise:.2f} & {r.mean_level:.2f}\\\\")
L.append(r"\bottomrule\end{tabular}"); open("paper2/tab_aid.tex", "w").write("\n".join(L))
de = pd.read_csv("results/defence_exact.csv"); fi = a[a.domain.str.startswith("book")]
H = r"$n$ & Band & Step down & Step up & Mean level\\\midrule"
du = pd.read_csv("results/defence_uncertainty.csv").set_index("period")
L = [r"\begin{tabular}{lrcrrrcc}\toprule", r"Period & $n$ & Band & \hd{Step\\down} & \hd{Step\\up} & \hd{Mean\\level} & \hd{Lower edge:\\2\% set} & \hd{Lower edge:\\bootstrap 90\%}\\\midrule"]
for _, r in de.iterrows():
    u = du.loc[r.period]
    L.append(f"{r.period} & {int(r.n)} & [{r.band_lo:.2f}, {r.band_hi:.2f}] & {r.step_cut:.2f} & {r.step_raise:.2f} & {r.mean_level:.2f} & [{u.set2_lo:.2f}, {u.set2_hi:.2f}] & [{u.boot_lo5:.2f}, {u.boot_lo95:.2f}]\\\\")
L.append(r"\bottomrule\end{tabular}"); open("paper2/tab_defence.tex", "w").write("\n".join(L))
L = [r"\begin{tabular}{lrcrrr}\toprule", "Industry & " + H]
for _, r in fi.iterrows():
    L.append(f"{r.unit} & {int(r.n)} & [{r.tau-r.b:.2f}, {r.tau+r.b:.2f}] & {fmt(r.step_cut)} & {fmt(r.step_raise)} & {r.mean_level:.2f}\\\\")
L.append(r"\bottomrule\end{tabular}"); open("paper2/tab_firms.tex", "w").write("\n".join(L))

mc = pd.read_csv("results/model_comparison.csv")
L = [r"\begin{tabular}{lrrrrrrr}\toprule", r"Domain & Units & GP & PA & Hold & \hd{Median\\change} & \hd{GP strictly\\best} & \hd{GP worse\\than hold}\\\midrule"]
for dom, lab in [("aid", "Aid (donors)"), ("central bank", "Central banks"), ("defence", "Defence (periods)")]:
    z = mc[mc.domain == dom]; M = z[["gp", "pa", "hold", "medchg"]].values
    strict = int(sum((M[i, 0] < np.delete(M[i], 0).min() - 1e-12) for i in range(len(z)))); worse = int((z.gp > z.hold + 1e-12).sum())
    L.append(f"{lab} & {len(z)} & {z.gp.mean():.3f} & {z.pa.mean():.3f} & {z.hold.mean():.3f} & {z.medchg.mean():.3f} & {strict}/{len(z)} & {worse}/{len(z)}\\\\")
L.append(r"\bottomrule\end{tabular}"); open("paper2/tab_mcomp.tex", "w").write("\n".join(L))

pl = pd.read_csv("results/misspec_placebo.csv"); g = pl.groupby("kind")
L = [r"\begin{tabular}{lrrrrrr}\toprule", r"True behaviour & \hd{$\hat\tau$\\median} & \hd{$\hat\tau$\\IQR} & \hd{Gain over\\hold} & \hd{$\tau$-set\\width} & \hd{GP beats\\hold} & \hd{GP beats\\PA}\\\midrule"]
for k, lab in [("gp", "Interval goal program"), ("coin", "Random (coin flip)"), ("partial", "Partial adjustment"), ("qp", "Quadratic program")]:
    z = pl[pl.kind == k]; t = z.tau_gp
    L.append(f"{lab} & {t.median():.2f} & {t.quantile(.75)-t.quantile(.25):.2f} & {100*z.gain_vs_hold.median():.0f}\\% & {z.set_width.median():.2f} & "
             f"{100*(z.oos_gp < z.oos_hold).mean():.0f}\\% & {100*(z.oos_gp < z.oos_pa).mean():.0f}\\%\\\\")
L.append(r"\bottomrule\end{tabular}"); open("paper2/tab_placebo.tex", "w").write("\n".join(L))

bm = pd.read_csv("results/cb_benchmarks.csv")
L = [r"\begin{tabular}{lrccccc}\toprule",
     r"Sample & $n$ & \hd{Implied\\target} & \hd{Mean\\inflation} & \hd{Constant\\2.5\%} & \hd{Median of\\other banks} & \hd{Taylor rule\\(implied / ours)}\\\midrule"]
for lab, z in [("Exploratory", bm[bm["sample"] == "exploratory"]), ("Confirmatory", bm[bm["sample"] == "confirmatory"]),
               (r"\hd{Confirmatory\\without Turkey}", bm[(bm["sample"] == "confirmatory") & (bm.country != "TR")]),
               ("All 14 banks", bm), (r"\hd{All without\\Turkey}", bm[bm.country != "TR"])]:
    e = lambda c, zz=z: np.abs(zz[c] - zz.stated).mean(); tz = z.dropna(subset=["taylor"])
    tay = r"\hd{" + f"{np.abs(tz.taylor - tz.stated).mean():.2f} / {np.abs(tz.implied - tz.stated).mean():.2f}" + r"\\" + f"($n={len(tz)}$)" + "}" if len(tz) else "--"
    L.append(f"{lab} & {len(z)} & {e('implied'):.2f} & {e('mean_infl'):.2f} & {e('const25'):.2f} & {e('median_other'):.2f} & {tay}\\\\")
L.append(r"\bottomrule\end{tabular}"); open("paper2/tab_cb_bench.tex", "w").write("\n".join(L))
