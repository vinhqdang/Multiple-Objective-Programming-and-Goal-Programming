"""Mixed-integer inverse interval goal programming (MI-IGP). See docs/08_inverse_interval_gp_design.md."""
import numpy as np, cvxpy as cp

def forward(x, alpha, c, d, om_p, om_m):
    """Optimal policy change for one period (Proposition 1: enumerate breakpoints)."""
    cand = [0.0] + [alpha[k] * x[k] - c[k] - d[k] for k in range(len(x))] + [alpha[k] * x[k] - c[k] + d[k] for k in range(len(x))]
    def F(D):
        g = alpha * x - D - c
        return (om_p * np.maximum(0, g - d) + om_m * np.maximum(0, -g - d)).sum() + abs(D)
    vals = np.array([F(D) for D in cand]); best = vals.min()
    ties = [D for D, v in zip(cand, vals) if v <= best + 1e-9]
    return min(ties, key=abs)

def to_scaled(tau, b, beta, w_p, w_m):
    alpha = 1 / np.abs(beta)
    return alpha, alpha * tau, alpha * b, w_p / alpha, w_m / alpha

def fit(X, D_obs, Omega=10.0, M=60.0, Dmax=8.0, alpha_bounds=(0.05, 10.0), time_limit=300, verbose=False):
    T, K = X.shape
    al = cp.Variable(K); c = cp.Variable(K); d = cp.Variable(K, nonneg=True)
    op = cp.Variable(K, nonneg=True); om = cp.Variable(K, nonneg=True)
    D = cp.Variable(T); r = cp.Variable(T, nonneg=True); sig = cp.Variable(T)
    p = cp.Variable((T, K), nonneg=True); q = cp.Variable((T, K), nonneg=True)
    a = cp.Variable((T, K), boolean=True); s = cp.Variable((T, K), boolean=True)
    l = cp.Variable((T, K), boolean=True); z = cp.Variable((T, K), boolean=True)
    up = cp.Variable(T, boolean=True); dn = cp.Variable(T, boolean=True)
    G = cp.multiply(X, np.ones((T, 1)) @ cp.reshape(al, (1, K), order="C")) - cp.reshape(D, (T, 1), order="C") @ np.ones((1, K)) \
        - np.ones((T, 1)) @ cp.reshape(c, (1, K), order="C")
    Dd = np.ones((T, 1)) @ cp.reshape(d, (1, K), order="C")
    OP = np.ones((T, 1)) @ cp.reshape(op, (1, K), order="C"); OM = np.ones((T, 1)) @ cp.reshape(om, (1, K), order="C")
    cons = [al >= alpha_bounds[0], al <= alpha_bounds[1], op <= Omega, om <= Omega, cp.abs(c) <= M, d <= M,
            r >= D_obs - D, r >= D - D_obs, cp.abs(D) <= Dmax,
            # upper side: a = active (G >= d), s = full (p = omega+)
            G - Dd <= M * a, G - Dd >= -M * (1 - a), p <= Omega * a, p <= OP, p >= OP - Omega * (1 - s), s <= a, G - Dd <= M * s,
            # lower side: l = active (-G >= d), z = full (q = omega-)
            -G - Dd <= M * l, -G - Dd >= -M * (1 - l), q <= Omega * l, q <= OM, q >= OM - Omega * (1 - z), z <= l, -G - Dd <= M * z,
            # |D| subgradient
            D <= Dmax * up, D >= -Dmax * dn, up + dn <= 1, sig >= 2 * up - 1, sig <= 1 - 2 * dn, sig >= -1, sig <= 1,
            # stationarity: sigma = sum_k (p_k - q_k)
            sig == cp.sum(p - q, axis=1)]
    prob = cp.Problem(cp.Minimize(cp.sum(r) / T), cons)
    prob.solve(solver=cp.HIGHS, time_limit=time_limit, verbose=verbose)
    alpha = al.value
    return dict(status=prob.status, loss=prob.value, alpha=alpha, tau=c.value / alpha, b=d.value / alpha,
                beta=-1 / alpha, omega_p=op.value, omega_m=om.value, D=D.value)

def fit_strict(X, D_obs, eps=0.05, delta=1e-3, Omega=5.0, M=30.0, Dmax=8.0, alpha_bounds=(0.05, 3.0), time_limit=300, verbose=False):
    """MI-IGP with a strict-optimality margin: at the fitted decision the right slope of F_t is >= eps and the
    left slope <= -eps. This excludes flat (knife-edge) optima that otherwise let the model absorb noise."""
    T, K = X.shape
    al = cp.Variable(K); c = cp.Variable(K); d = cp.Variable(K, nonneg=True)
    op = cp.Variable(K, nonneg=True); om = cp.Variable(K, nonneg=True)
    D = cp.Variable(T); r = cp.Variable(T, nonneg=True)
    a = cp.Variable((T, K), boolean=True); s = cp.Variable((T, K), boolean=True)   # upper: active (g>=d), strictly above (g>d)
    l = cp.Variable((T, K), boolean=True); z = cp.Variable((T, K), boolean=True)   # lower: active (-g>=d), strictly below
    up = cp.Variable(T, boolean=True); dn = cp.Variable(T, boolean=True)
    # McCormick products omega * binary (exact for binaries)
    Ps = cp.Variable((T, K), nonneg=True); Pa = cp.Variable((T, K), nonneg=True)
    Ql = cp.Variable((T, K), nonneg=True); Qz = cp.Variable((T, K), nonneg=True)
    one = np.ones((T, 1))
    row = lambda v: one @ cp.reshape(v, (1, K), order="C")
    G = cp.multiply(X, row(al)) - cp.reshape(D, (T, 1), order="C") @ np.ones((1, K)) - row(c)
    Dd, OP, OM = row(d), row(op), row(om)
    def prod(P, w, bvar):
        return [P <= Omega * bvar, P <= w, P >= w - Omega * (1 - bvar)]
    cons = [al >= alpha_bounds[0], al <= alpha_bounds[1], op <= Omega, om <= Omega, cp.abs(c) <= M, d <= M,
            r >= D_obs - D, r >= D - D_obs, cp.abs(D) <= Dmax,
            G - Dd <= M * a, G - Dd >= -M * (1 - a), s <= a, G - Dd <= M * s, G - Dd >= delta - M * (1 - s),
            -G - Dd <= M * l, -G - Dd >= -M * (1 - l), z <= l, -G - Dd <= M * z, -G - Dd >= delta - M * (1 - z),
            up + dn <= 1, D <= Dmax * up, D >= -Dmax * dn, D >= delta - Dmax * (1 - up), D <= -delta + Dmax * (1 - dn)]
    cons += prod(Ps, OP, s) + prod(Pa, OP, a) + prod(Ql, OM, l) + prod(Qz, OM, z)
    right = -cp.sum(Ps, axis=1) + cp.sum(Ql, axis=1) + 1 - 2 * dn     # right derivative of F_t at D
    left = -cp.sum(Pa, axis=1) + cp.sum(Qz, axis=1) + 2 * up - 1      # left derivative of F_t at D
    cons += [right >= eps, left <= -eps]
    prob = cp.Problem(cp.Minimize(cp.sum(r) / T), cons)
    prob.solve(solver=cp.HIGHS, time_limit=time_limit, verbose=verbose)
    alpha = al.value
    return dict(status=prob.status, loss=prob.value, alpha=alpha, tau=c.value / alpha, b=d.value / alpha,
                beta=-1 / alpha, omega_p=op.value, omega_m=om.value, D=D.value)
