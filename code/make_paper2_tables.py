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
pt = pd.read_csv("results/permutation_test.csv"); pt = pt[pt.domain == "aid"].set_index("unit").p
ax["p"] = ax.donor.map(pt); ax = ax.sort_values(["p", "tau"], ascending=[True, False])
L = [r"\begin{tabular}{lrrrrrrr}\toprule", r"Donor & $n$ & $p$ & $\hat\tau$ & Band & $\tau$ set (2\%) & Steps (down, up) & Mean\\\midrule"]
for _, r in ax.iterrows():
    star = "$^{**}$" if r.p <= 0.05 else ("$^{*}$" if r.p <= 0.10 else "")
    L.append(f"{r.donor}{star} & {int(r.n)} & {r.p:.3f} & {r.tau:.2f} & [{r.band_lo:.2f}, {r.band_hi:.2f}] & {r.set2} & {r.step_cut:.2f}, {r.step_raise:.2f} & {r.mean_level:.2f}\\\\")
L.append(r"\bottomrule\end{tabular}"); open("paper2/tab_aid.tex", "w").write("\n".join(L))
de = pd.read_csv("results/defence_exact.csv"); fi = a[a.domain.str.startswith("book")]
L = [r"\begin{tabular}{llrrrrr}\toprule", r"Domain & Unit & $n$ & Band & Step down & Step up & Mean level\\\midrule"]
for _, r in de.iterrows():
    L.append(f"Defence, NATO def. & {r.period} & {int(r.n)} & [{r.band_lo:.2f}, {r.band_hi:.2f}] & {r.step_cut:.2f} & {r.step_raise:.2f} & {r.mean_level:.2f}\\\\")
for _, r in fi.iterrows():
    L.append(f"Book leverage & {r.unit} & {int(r.n)} & [{r.tau-r.b:.2f}, {r.tau+r.b:.2f}] & {fmt(r.step_cut)} & {fmt(r.step_raise)} & {r.mean_level:.2f}\\\\")
L.append(r"\bottomrule\end{tabular}"); open("paper2/tab_def_firms.tex", "w").write("\n".join(L))

mc = pd.read_csv("results/model_comparison.csv")
L = [r"\begin{tabular}{lrrrrrrr}\toprule", r"Domain & Units & GP & PA & Hold & Median change & GP strictly best & GP worse than hold\\\midrule"]
for dom, lab in [("aid", "Aid (donors)"), ("central bank", "Central banks"), ("defence", "Defence (periods)")]:
    z = mc[mc.domain == dom]; M = z[["gp", "pa", "hold", "medchg"]].values
    strict = int(sum((M[i, 0] < np.delete(M[i], 0).min() - 1e-12) for i in range(len(z)))); worse = int((z.gp > z.hold + 1e-12).sum())
    L.append(f"{lab} & {len(z)} & {z.gp.mean():.3f} & {z.pa.mean():.3f} & {z.hold.mean():.3f} & {z.medchg.mean():.3f} & {strict}/{len(z)} & {worse}/{len(z)}\\\\")
L.append(r"\bottomrule\end{tabular}"); open("paper2/tab_mcomp.tex", "w").write("\n".join(L))
