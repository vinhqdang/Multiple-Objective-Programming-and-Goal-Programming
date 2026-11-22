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
if os.path.exists("results/bootstrap_cb_summary.csv"):
    b = pd.read_csv("results/bootstrap_cb_summary.csv")
    L = [r"\begin{tabular}{lrrrrc}\toprule", r"Bank & Stated & 5\% & Median & 95\% & Covers stated \\\midrule"]
    for _, r in b.iterrows():
        L.append(f"{r.country} & {r.stated:.1f} & {r.lo:.2f} & {r.med:.2f} & {r.hi:.2f} & {'yes' if r.covers_stated else 'no'}\\\\")
    L.append(r"\bottomrule\end{tabular}"); open("paper2/tab_cb_bootstrap.tex", "w").write("\n".join(L))
print("ok")

a = pd.read_csv("results/applications_gp_aid_defence_firms.csv")
def fmt(v): return "--" if pd.isna(v) else f"{v:.2f}"
aid = a[a.domain == "ODA % GNI"].sort_values("tau", ascending=False)
L = [r"\begin{tabular}{lrrrrrr}\toprule", r"Donor & $n$ & $\hat\tau$ & Band & Step down & Step up & Mean level\\\midrule"]
for _, r in aid.iterrows():
    L.append(f"{r.unit} & {int(r.n)} & {r.tau:.2f} & [{r.tau-r.b:.2f}, {r.tau+r.b:.2f}] & {fmt(r.step_cut)} & {fmt(r.step_raise)} & {r.mean_level:.2f}\\\\")
L.append(r"\bottomrule\end{tabular}"); open("paper2/tab_aid.tex", "w").write("\n".join(L))
oth = a[a.domain != "ODA % GNI"]
L = [r"\begin{tabular}{llrrrrr}\toprule", r"Domain & Unit & $n$ & Band & Step down & Step up & Mean level\\\midrule"]
for _, r in oth.iterrows():
    dom = "Defence, NATO def." if r.domain.startswith("defence") else "Book leverage"
    unit = r.unit.replace("NATO def., ", "")
    L.append(f"{dom} & {unit} & {int(r.n)} & [{r.tau-r.b:.2f}, {r.tau+r.b:.2f}] & {fmt(r.step_cut)} & {fmt(r.step_raise)} & {r.mean_level:.2f}\\\\")
L.append(r"\bottomrule\end{tabular}"); open("paper2/tab_def_firms.tex", "w").write("\n".join(L))
