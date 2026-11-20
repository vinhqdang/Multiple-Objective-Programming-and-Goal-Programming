import json, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
rows = json.load(open("results/results.json"))
def get(tag, kind, method, n, f): 
    return [r for r in rows if r["tag"]==tag and r["kind"]==kind and r["method"]==method and r["n"]==n][0][f]
ns = [50,100,200,500,1000]
fig, axs = plt.subplots(1,2, figsize=(8,3.2), sharey=False)
for ax, kind, ttl in zip(axs, ["cheb","wgp"], ["Chebyshev GP","Weighted GP"]):
    for m, lab, st in [("equal","Equal split","k:"),("lam0","Plug-in (λ=0)","C0-o"),("lam0.5","Shrunk (λ=0.5)","C1-s"),("oracle","Oracle","k--")]:
        y=[get("main",kind,m,n,"cheb_mean") for n in ns]
        e=[get("main",kind,m,n,"cheb_se") for n in ns]
        ax.errorbar(ns,y,yerr=[1.96*x for x in e],fmt=st,label=lab,capsize=2,ms=4)
    ax.set_xscale("log"); ax.set_xlabel("training units n"); ax.set_title(ttl,fontsize=10)
axs[0].set_ylabel("worst-goal shortfall (realised)"); axs[0].legend(fontsize=7)
plt.tight_layout(); plt.savefig("paper/fig_main.pdf")
def f(x): return f"{x:.3f}"
T=[r"\begin{tabular}{rlcccc}\toprule",r"$n$ & Model & Equal & Plug-in & Shrunk ($\lambda{=}0.5$) & Oracle\\\midrule"]
for kind,nm in [("cheb","Chebyshev"),("wgp","Weighted")]:
    for n in ns:
        T.append(f"{n} & {nm} & "+" & ".join(f(get("main",kind,m,n,"cheb_mean")) for m in ["equal","lam0","lam0.5","oracle"])+r"\\")
T.append(r"\bottomrule\end{tabular}")
open("paper/tab_main.tex","w").write("\n".join(T))
T=[r"\begin{tabular}{rlccc}\toprule",r"$n$ & Model & $\lambda{=}0.25$ & $\lambda{=}0.5$ & $\lambda{=}1$\\\midrule"]
for kind,nm in [("cheb","Chebyshev"),("wgp","Weighted")]:
    for n in (50,200,1000):
        T.append(f"{n} & {nm} & "+" & ".join(f"{get('main',kind,m,n,'pd_cheb'):+.4f} ({get('main',kind,m,n,'pd_cheb_se'):.4f})" for m in ["lam0.25","lam0.5","lam1.0"])+r"\\")
T.append(r"\bottomrule\end{tabular}")
open("paper/tab_paired.tex","w").write("\n".join(T))
T=[r"\begin{tabular}{llrcccc}\toprule",r"Scenario & Model & $n$ & Equal & Plug-in & Shrunk & Oracle\\\midrule"]
for tag,lab in [("tau0.1","$\\tau{=}0.1$"),("tau0.6","$\\tau{=}0.6$"),("sigma0.1","$\\sigma{=}0.1$"),("sigma0.8","$\\sigma{=}0.8$")]:
    for n in (100,500):
        T.append(f"{lab} & Chebyshev & {n} & "+" & ".join(f(get(tag,"cheb",m,n,"cheb_mean")) for m in ["equal","lam0","lam0.5","oracle"])+r"\\")
T.append(r"\bottomrule\end{tabular}")
open("paper/tab_sens.tex","w").write("\n".join(T))
