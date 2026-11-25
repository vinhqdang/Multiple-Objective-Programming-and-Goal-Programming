import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, exact_k1 as X
from applications_gp import panel
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
# 1. policy shape
x = np.linspace(-1, 6, 600); fig, ax = plt.subplots(figsize=(5, 2.6))
ax.plot(x, X.h(x, 1.0, 3.0, 1.0, 0.5, 0.4), color="C0", lw=2)
for v, lab in [(0, ""), (1, r"$\tau-b$"), (3, r"$\tau+b$")]:
    if lab: ax.axvline(v, color="0.6", ls=":", lw=1); ax.text(v, 0.55, lab, ha="center", fontsize=8)
ax.axhline(0, color="0.3", lw=0.6)
ax.annotate("dead zone (hold)", (2, 0.03), ha="center", fontsize=8)
ax.annotate(r"step $\omega^+$", (5, 0.45), ha="center", fontsize=8); ax.annotate(r"step $-\omega^-$", (-0.4, -0.36), ha="center", fontsize=8)
ax.annotate("stop at band edge", (3.3, 0.2), fontsize=8)
ax.set_xlabel(r"goal variable if policy unchanged, $x$ (with $\alpha=1$)"); ax.set_ylabel(r"optimal change $D^*$")
fig.tight_layout(); fig.savefig("paper2/fig_policy.pdf"); plt.close(fig)
# 2. aid profiles
a = pd.read_csv("data/aid/dac1_donor_oda_gni.csv.gz")
a = a[((a.measure.astype(str) == "2") & (a.year <= 2017)) | ((a.measure.astype(str) == "11002") & (a.year >= 2018))]
a = a[a.unit == "PT_B5G"].groupby(["donor", "year"], as_index=False).value.first()
p = panel(a, "donor", "value"); p = p[p.year != 2018]
fig, axs = plt.subplots(2, 3, figsize=(7, 4), sharex=True)
goals = {"LUX": 1.0, "NOR": 1.0, "SWE": 1.0, "DNK": 0.8, "NLD": 0.7, "GBR": 0.7}
taus = np.arange(0.0, 1.41, 0.01)
for ax, (d, gl) in zip(axs.ravel(), goals.items()):
    g = p[p.donor == d]; prof = X.profile_tau(g.x.values, -g.delta.values, 1.0, taus)
    ax.plot(taus, prof / prof.min(), color="C0"); ax.axhline(1.02, color="0.6", ls=":", lw=1)
    ax.axvline(gl, color="C3", ls="--", lw=1); ax.axvline(g.x.mean(), color="C2", ls="-.", lw=1)
    ax.set_title(d, fontsize=9); ax.set_ylim(0.98, 1.25)
for ax in axs[1]: ax.set_xlabel(r"aspiration level $\tau$ (% of GNI)")
for ax in axs[:, 0]: ax.set_ylabel("profile loss / minimum")
fig.legend(["profile loss", "2% tolerance", "stated goal", "mean level"], loc="lower center", ncol=4, frameon=False, fontsize=8)
fig.tight_layout(rect=(0, 0.06, 1, 1)); fig.savefig("paper2/fig_aid_profiles.pdf"); plt.close(fig)
# 3. central banks: implied vs stated
e = pd.read_csv("results/real_cb_quad.csv"); e = e[e.input == "realised"].rename(columns={"tau_pi": "tau", "mean_x": "mean"})
c = pd.read_csv("results/confirmatory_cb.csv"); c = c[c.status == "included"].rename(columns={"tau_pi": "tau", "mean_infl": "mean"})
b = pd.read_csv("results/bootstrap_cb_100_summary.csv").set_index("country")
fig, ax = plt.subplots(figsize=(4.2, 3.6))
for df, col, lab in [(e, "C0", "exploratory"), (c, "C1", "confirmatory")]:
    for _, r in df.iterrows():
        lo, hi, nd = b.loc[r.country, "lo"], b.loc[r.country, "hi"], int(b.loc[r.country, "n_degenerate"])
        x0 = r.stated + (0.08 if r.country in ("IL", "MX", "CO") else 0.0)
        ax.plot([x0, x0], [max(lo, 0.05), min(hi, 10.9)], color=col, alpha=0.35, lw=3)
        if lo < 0.05: ax.annotate("", (x0, 0.0), (x0, 0.6), arrowprops=dict(arrowstyle="->", color=col, alpha=0.6))
        if hi > 10.9: ax.annotate("", (x0, 11.0), (x0, 10.4), arrowprops=dict(arrowstyle="->", color=col, alpha=0.6))
        if nd > 0: ax.annotate(f"{nd}", (x0 + 0.04, 0.25), fontsize=6, color=col)
    ax.scatter(df.stated, df.tau, color=col, label=f"implied, {lab}", zorder=3)
    ax.scatter(df.stated, df["mean"], facecolors="none", edgecolors=col, marker="s", label=f"mean inflation, {lab}", zorder=3)
    for _, r in df.iterrows(): ax.annotate(r.country, (r.stated + 0.05, r.tau), fontsize=7)
ax.plot([1, 6], [1, 6], color="0.5", ls=":"); ax.set_xlim(1.5, 5.5); ax.set_ylim(0, 11)
ax.set_xlabel("stated inflation target (%)"); ax.set_ylabel("estimate (%)"); ax.legend(fontsize=7, frameon=False)
fig.tight_layout(); fig.savefig("paper2/fig_cb.pdf"); plt.close(fig)
# 4. defence
n = pd.read_csv("data/cofog/nato_defence_pc_gdp.csv.gz").rename(columns={"defence_pc_gdp": "v"})
n = n[~n.country.str.contains("NATO|Europe|Canada and", case=False, regex=True) | (n.country == "Canada")].dropna(subset=["v"])
q = panel(n, "country", "v"); de = pd.read_csv("results/defence_exact.csv")
fig, axs = plt.subplots(1, 2, figsize=(7, 2.8), sharey=True)
for ax, (_, r) in zip(axs, de.iterrows()):
    a0, a1 = map(int, r.period.split("-")); g = q[(q.year >= a0) & (q.year <= a1)]
    ax.scatter(g.x, g.delta, s=8, alpha=0.5, color="0.4")
    xx = np.linspace(g.x.min(), g.x.max(), 400); ep, em = r.tau + r.b, r.tau - r.b
    ax.plot(xx, -X.h(xx, 1.0, ep, em, r.step_cut, r.step_raise), color="C0", lw=2)
    ax.axvline(r.band_lo, color="C3", ls="--", lw=1); ax.set_title(f"{r.period}: lower edge {r.band_lo:.2f}%", fontsize=9)
    ax.set_xlabel("defence spending, previous year (% of GDP)")
axs[0].set_ylabel("change (pp of GDP)")
fig.tight_layout(); fig.savefig("paper2/fig_defence.pdf"); plt.close(fig)
print("ok")
