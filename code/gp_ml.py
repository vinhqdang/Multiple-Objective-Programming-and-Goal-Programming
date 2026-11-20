"""Uncertainty-aware goal programming with learned marginal effects.

Simulation study: allocate a public budget over R units to attain K social goals.
Marginal effects are unknown and predicted by ridge regression from unit features.
"""
import numpy as np, json, sys
from scipy.optimize import linprog
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import cross_val_predict

R, K, P = 60, 4, 6          # units, goals, features
BUDGET = 1.0
CAP = 0.08                  # max share per unit (equity cap)
FLOOR = 0.002               # min share per unit
RHO = 0.8

def gen_world(rng, tau):
    beta = rng.normal(0, 0.45, size=(P, K))
    def units(m):
        Z = rng.normal(size=(m, P))
        base = 1.0 + Z @ beta
        C = np.maximum(0.05, base + rng.normal(0, tau, size=(m, K)))
        return Z, C
    return units

def solve_gp(C, T, kind, w=None):
    """C: R x K effects, T: K targets. Variables x (R), d (K) underachievement shares."""
    Rn, Kn = C.shape
    w = np.ones(Kn) / Kn if w is None else w
    eps = 1e-3
    if kind == "wgp":      # min sum w_k d_k, d_k = shortfall / T_k
        c = np.concatenate([np.zeros(Rn), w])
        nv = Rn + Kn
    else:                  # Chebyshev: min lam + eps*sum d
        c = np.concatenate([np.zeros(Rn), np.full(Kn, eps), [1.0]])
        nv = Rn + Kn + 1
    A, b = [], []
    for k in range(Kn):   # -C_k x - T_k d_k <= -T_k
        row = np.zeros(nv); row[:Rn] = -C[:, k]; row[Rn + k] = -T[k]
        A.append(row); b.append(-T[k])
    if kind == "cheb":
        for k in range(Kn):   # d_k - lam <= 0
            row = np.zeros(nv); row[Rn + k] = 1; row[-1] = -1
            A.append(row); b.append(0.0)
    row = np.zeros(nv); row[:Rn] = 1; A.append(row); b.append(BUDGET)
    bounds = [(FLOOR, CAP)] * Rn + [(0, None)] * (nv - Rn)
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=bounds, method="highs")
    return res.x[:Rn]

def ideal(C):
    out = []
    for k in range(C.shape[1]):
        res = linprog(-C[:, k], A_ub=np.ones((1, C.shape[0])), b_ub=[BUDGET],
                      bounds=[(FLOOR, CAP)] * C.shape[0], method="highs")
        out.append(-res.fun)
    return np.array(out)

def devs(x, Ctrue, T):
    return np.maximum(0, T - Ctrue.T @ x) / T

def metrics(x, Ctrue, T):
    d = devs(x, Ctrue, T)
    return d.max(), d.mean()

def one_rep(seed, n_train, sigma, tau, lams, kinds=("cheb", "wgp")):
    rng = np.random.default_rng(seed)
    units = gen_world(rng, tau)
    Ztr, Ctr = units(n_train)
    Ctr_obs = Ctr + rng.normal(0, sigma, size=Ctr.shape)       # noisy historical estimates
    Z, Ctrue = units(R)                                         # decision units
    T = RHO * ideal(Ctrue)
    # learn effects, per goal
    Chat = np.zeros((R, K)); resid_sd = np.zeros(K)
    for k in range(K):
        m = RidgeCV(alphas=np.logspace(-2, 3, 12)).fit(Ztr, Ctr_obs[:, k])
        Chat[:, k] = m.predict(Z)
        oof = cross_val_predict(RidgeCV(alphas=np.logspace(-2, 3, 12)), Ztr, Ctr_obs[:, k], cv=5)
        resid_sd[k] = np.std(Ctr_obs[:, k] - oof, ddof=1)
    out = {}
    for kind in kinds:
        xo = solve_gp(Ctrue, T, kind)
        mo = metrics(xo, Ctrue, T)
        xe = np.full(R, BUDGET / R)
        me = metrics(xe, Ctrue, T)
        out[(kind, "oracle")] = mo
        out[(kind, "equal")] = me
        for lam in lams:
            Cr = np.maximum(0.0, Chat - lam * resid_sd)
            x = solve_gp(Cr, T, kind)
            m = metrics(x, Ctrue, T)
            out[(kind, f"lam{lam}")] = m
            # optimism: predicted (plug-in) vs realised deviation, lam=0 only
            if lam == 0:
                pred = devs(x, Chat, T)
                out[(kind, "pred_gap")] = ((devs(x, Ctrue, T)).max() - pred.max(),
                                           devs(x, Ctrue, T).mean() - pred.mean())
    return out

def run(n_rep=200, ns=(50, 100, 200, 500, 1000), sigma=0.3, tau=0.3,
        lams=(0, 0.25, 0.5, 1.0, 1.5), tag="main"):
    rows = []
    for n in ns:
        agg = {}
        for s in range(n_rep):
            o = one_rep(1000 * n + s, n, sigma, tau, lams)
            for key, v in o.items():
                agg.setdefault(key, []).append(v)
        for key, v in agg.items():
            v = np.array(v)
            base = np.array(agg[(key[0], "lam0")]) if key[1].startswith("lam") else None
            dd = (v - base) if base is not None else np.zeros_like(v)
            rows.append(dict(pd_cheb=dd[:, 0].mean(), pd_cheb_se=dd[:, 0].std(ddof=1) / np.sqrt(len(v)),
                             pd_wgp=dd[:, 1].mean(), pd_wgp_se=dd[:, 1].std(ddof=1) / np.sqrt(len(v)),
                             tag=tag, n=n, sigma=sigma, tau=tau, kind=key[0], method=key[1],
                             cheb_mean=v[:, 0].mean(), cheb_se=v[:, 0].std(ddof=1) / np.sqrt(len(v)),
                             wgp_mean=v[:, 1].mean(), wgp_se=v[:, 1].std(ddof=1) / np.sqrt(len(v))))
        print(tag, n, "done", flush=True)
    return rows

if __name__ == "__main__":
    rows = run(tag="main")
    for tau in (0.1, 0.6):
        rows += run(tag=f"tau{tau}", tau=tau, ns=(100, 500), n_rep=100)
    for sg in (0.1, 0.8):
        rows += run(tag=f"sigma{sg}", sigma=sg, ns=(100, 500), n_rep=100)
    json.dump(rows, open("results/results.json", "w"), indent=1)
