"""Regime incidence of the two-goal central-bank fits (rank condition of Proposition 5): for each bank, refit with
the lighter search at the seed of results/cb_light_point.csv and count the periods in which, at the fitted decision,
only goal 1 (inflation), only goal 2 (growth gap) or both goals lie outside their bands. The weights of goal k are
point-identified (given the other parameters) only if some period has goal k alone outside its band.
Writes results/cb_regimes.csv."""
import sys, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import migp_quad as Q
from bootstrap_cb import data, CONF
from inverse_interval_gp_cb import WINDOWS
banks = [(cc, pd.Period(s, "M").asfreq("Q"), pd.Period(e, "M").asfreq("Q")) for cc, s, e, t, _ in WINDOWS]
banks += [(cc, pd.Period(s, "Q"), pd.Period(e, "Q")) for cc, s, e, t in CONF]
lp = pd.read_csv("results/cb_light_point.csv").set_index("country")
rows = []
for cc, q0, q1 in banks:
    X, D = data(cc, q0, q1)
    h = Q.fit_hybrid(X, D, de_iter=800, de_pop=40, lns_iters=0, seed=int(lp.loc[cc, "seed"]))
    al, tau, b = np.asarray(h["alpha"]), np.asarray(h["tau"]), np.asarray(h["b"])
    Dh = Q.forward_batch(X, al, tau, b, np.asarray(h["omega_p"]), np.asarray(h["omega_m"]))
    g = al * X - Dh[:, None] - al * tau            # position of each goal relative to its target after the decision
    out = np.abs(g) > al * b + 1e-9
    rows.append(dict(country=cc, T=len(D), tau1=tau[0], alpha1=al[0], alpha2=al[1], only1=int((out[:, 0] & ~out[:, 1]).sum()),
                     only2=int((~out[:, 0] & out[:, 1]).sum()), both=int(out.all(1).sum()), none=int((~out).all(1).sum())))
    print(rows[-1], flush=True)
pd.DataFrame(rows).round(3).to_csv("results/cb_regimes.csv", index=False)
