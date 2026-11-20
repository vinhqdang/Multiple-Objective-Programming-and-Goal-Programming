"""Inertial proximal point algorithm (IPPA) for Cobb-Douglas goal programming on the positive orthant.

Allocation x in R^n_{++}, theta = log x. The positive orthant with metric diag(1/x^2) is the Hadamard manifold of
Example 6.1 in Upadhyay, Poddar, Caristi, Barilla (Ann. Oper. Res., 2025); in theta coordinates it is flat.
Goal k has outcome y_k(x) = exp(b_k + a_k' theta) (Cobb-Douglas). Objectives (all >= 0, Lipschitz, convex in theta):
  Psi_k = max(0, ln T_k - b_k - a_k' theta)   (log shortfall of goal k), k = 1..K
  Psi_{K+1} = sum_i exp(theta_i) / B           (relative spend)
"""
import numpy as np, cvxpy as cp

def make_world(rng, n=40, K=4):
    A = np.zeros((K, n))
    for k in range(K):
        mask = rng.random(n) < 0.5
        A[k, mask] = rng.uniform(0.5, 1.5, mask.sum())
    for i in range(n):                       # every unit matters for at least one goal
        if A[:, i].sum() == 0: A[rng.integers(K), i] = 1.0
    A = A / A.sum(1, keepdims=True) * 0.6     # decreasing returns: elasticities sum to 0.6 per goal
    b = rng.normal(0, 0.3, K)
    th_eq = np.full(n, np.log(1.0 / n))       # equal split of budget B = 1
    lnT = b + A @ th_eq + np.log(1.5)         # target: 50% above equal-split outcome
    return A, b, lnT

def psi(theta, A, b, lnT):
    d = np.maximum(0.0, lnT - b - A @ theta)
    return np.append(d, np.exp(theta).sum())

def prox_step(y, th_k, u, eta, A, b, lnT):
    n = len(y); th = cp.Variable(n)
    dev = cp.pos(lnT - b - A @ th)
    cost = cp.sum(cp.exp(th))
    cur = psi(th_k, A, b, lnT)
    cons = [dev <= cur[:-1] + 1e-9, cost <= cur[-1] + 1e-9]
    obj = u[:-1] @ dev + u[-1] * cost + (eta / 2) * cp.sum_squares(th - y)
    cp.Problem(cp.Minimize(obj), cons).solve(solver=cp.CLARABEL)
    return th.value

def ippa(A, b, lnT, u, tau=0.3, eta=1.0, iters=60, theta0=None, tol=1e-7):
    n = A.shape[1]
    th_prev = th = np.full(n, np.log(1.0 / n)) if theta0 is None else theta0.copy()
    hist = [psi(th, A, b, lnT)]
    for _ in range(iters):
        y = th + tau * (th - th_prev)                  # inertial extrapolation (flat in log coordinates)
        new = prox_step(y, th, u, eta, A, b, lnT)
        if np.linalg.norm(new - th) < tol: th_prev, th = th, new; break
        th_prev, th = th, new
        hist.append(psi(th, A, b, lnT))
    return th, np.array(hist)

def pareto_gap(theta_hat, A, b, lnT, return_point=False, lo=None, hi=None):
    """Largest simultaneous improvement t >= 0 available in every objective of the (true) problem.
    t = 0 iff theta_hat is weakly Pareto optimal (convex case)."""
    n = len(theta_hat); th = cp.Variable(n); t = cp.Variable()
    ref = psi(theta_hat, A, b, lnT)
    cons = [cp.pos(lnT - b - A @ th) <= ref[:-1] - t, cp.sum(cp.exp(th)) <= ref[-1] - t]
    if lo is not None: cons += [th >= lo]
    if hi is not None: cons += [th <= hi]
    p = cp.Problem(cp.Maximize(t), cons); p.solve(solver=cp.CLARABEL)
    g = max(0.0, p.value) if p.value is not None else np.nan
    return (g, th.value) if return_point else g
