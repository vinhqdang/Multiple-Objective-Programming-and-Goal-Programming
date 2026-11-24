"""Evaluation of the two-goal heuristic (migp_quad.fit_hybrid, default settings) after review.
(1) Parameter recovery: 20 synthetic instances per noise level, K = 2, T = 60 (the size of the bank samples), state
    1 AR(1) around 3 (coefficient 0.8, sd 0.8), state 2 AR(1) around 0 (0.7, 1.0); true alpha = (0.5, 1.0),
    tau = (2.5, 0.0), b = (0.5, 1.0), omega+ = (0.5, 0.25), omega- = (0.5, 0.25); Laplace decision noise 0.05, 0.1.
    Reports fitted loss relative to the loss at the true parameters and absolute errors of tau_1, b_1, alpha_1.
(2) Multi-seed stability of the 14 central-bank fits: five seeds per bank (the reported fit uses the best of seeds 0, 1).
Writes results/k2_recovery.csv and results/cb_multiseed.csv."""
import sys, warnings; sys.path.insert(0, "code"); warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from multiprocessing import Pool
import migp_quad as Q
TRUE = dict(alpha=np.array([0.5, 1.0]), tau=np.array([2.5, 0.0]), b=np.array([0.5, 1.0]),
            op=np.array([0.5, 0.25]), om=np.array([0.5, 0.25]))

def instance(seed, noise, T=60):
    r = np.random.default_rng(seed); X = np.zeros((T, 2)); s = np.array([3.0, 0.0])
    for t in range(T):
        s = np.array([3.0, 0.0]) + np.array([0.8, 0.7]) * (s - np.array([3.0, 0.0])) + r.normal(0, [0.8, 1.0]); X[t] = s
    D0 = Q.forward_batch(X, TRUE["alpha"], TRUE["tau"], TRUE["b"], TRUE["op"], TRUE["om"])
    return X, D0 + r.laplace(0, noise, T), D0

def rec_job(args):
    noise, rep = args; X, D, D0 = instance(1000 + rep, noise)
    h = Q.fit_hybrid(X, D, seed=rep)
    return dict(noise=noise, rep=rep, loss=h["loss"], loss_true=np.abs(D - D0).mean(),
                err_tau1=abs(h["tau"][0] - 2.5), err_b1=abs(h["b"][0] - 0.5), err_alpha1=abs(h["alpha"][0] - 0.5),
                err_tau2=abs(h["tau"][1] - 0.0))

def seed_job(args):
    from bootstrap_cb import data
    cc, q0, q1, s = args; X, D = data(cc, q0, q1); h = Q.fit_hybrid(X, D, seed=s)
    return dict(country=cc, seed=s, loss=h["loss"], tau=h["tau"][0], alpha=h["alpha"][0])

if __name__ == "__main__":
    from bootstrap_cb import CONF
    from inverse_interval_gp_cb import WINDOWS
    with Pool(2) as p:
        rec = pd.DataFrame(p.map(rec_job, [(n, r) for n in (0.05, 0.1) for r in range(20)], chunksize=1))
        rec.to_csv("results/k2_recovery.csv", index=False)
        print(rec.groupby("noise").agg(rel_loss=("loss", lambda z: 0), ).to_string())
        rec["rel"] = rec.loss / rec.loss_true
        print(rec.groupby("noise")[["rel", "err_tau1", "err_b1", "err_alpha1", "err_tau2"]].median().round(3).to_string(), flush=True)
        banks = [(cc, pd.Period(s, "M").asfreq("Q"), pd.Period(e, "M").asfreq("Q")) for cc, s, e, t, _ in WINDOWS]
        banks += [(cc, pd.Period(s, "Q"), pd.Period(e, "Q")) for cc, s, e, t in CONF]
        ms = pd.DataFrame(p.map(seed_job, [(cc, a, b, s) for cc, a, b in banks for s in range(5)], chunksize=1))
    ms.to_csv("results/cb_multiseed.csv", index=False)
    print(ms.groupby("country").agg(tau_min=("tau", "min"), tau_max=("tau", "max"), loss_min=("loss", "min"), loss_max=("loss", "max")).round(3).to_string())
