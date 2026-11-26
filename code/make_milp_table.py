"""Table of MILP closure on small synthetic two-goal instances (results/milp_small.csv) -> paper2/tab_milp.tex."""
import pandas as pd
d = pd.read_csv("results/milp_small.csv")
L = [r"\begin{tabular}{rcrrrr}\toprule",
     r"$T$ & \hd{Solved to\\optimality} & \hd{Run time (s),\\median} & \hd{Relative gap,\\median} & \hd{Fitted loss,\\median} & \hd{Loss at\\true $\theta$, median}\\\midrule"]
for T, g in d.groupby("T"):
    L.append(f"{T} & {int(g.closed.sum())} of {len(g)} & {g.seconds.median():.0f} & {g.gap_rel.clip(lower=0).median():.2f} & {g.incumbent.median():.3f} & {g.loss_true.median():.3f}\\\\")
L.append(r"\bottomrule\end{tabular}"); open("paper2/tab_milp.tex", "w").write("\n".join(L)); print("\n".join(L))
