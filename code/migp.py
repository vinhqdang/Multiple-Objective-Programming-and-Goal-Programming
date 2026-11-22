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

# ---------------------------------------------------------------------------
# Large-neighbourhood search (LNS) for MI-IGP with exact sub-MILPs and a certified lower bound.

def _build_strict(X, D_obs, eps, delta, Omega, M, Dmax, alpha_bounds, fix=None, free=None):
    """Strict-margin MI-IGP model. If fix is given (dict of arrays a,s,l,z,up,dn), binaries of periods
    with free[t] == False are fixed to those values (the problem then has binaries only for free periods)."""
    T, K = X.shape
    V = dict(al=cp.Variable(K), c=cp.Variable(K), d=cp.Variable(K, nonneg=True), op=cp.Variable(K, nonneg=True),
             om=cp.Variable(K, nonneg=True), D=cp.Variable(T), r=cp.Variable(T, nonneg=True),
             a=cp.Variable((T, K), boolean=True), s=cp.Variable((T, K), boolean=True), l=cp.Variable((T, K), boolean=True),
             z=cp.Variable((T, K), boolean=True), up=cp.Variable(T, boolean=True), dn=cp.Variable(T, boolean=True),
             Ps=cp.Variable((T, K), nonneg=True), Pa=cp.Variable((T, K), nonneg=True),
             Ql=cp.Variable((T, K), nonneg=True), Qz=cp.Variable((T, K), nonneg=True))
    al, c, d, op, om, D, r = (V[k] for k in ["al", "c", "d", "op", "om", "D", "r"])
    a, s, l, z, up, dn, Ps, Pa, Ql, Qz = (V[k] for k in ["a", "s", "l", "z", "up", "dn", "Ps", "Pa", "Ql", "Qz"])
    one = np.ones((T, 1)); row = lambda v: one @ cp.reshape(v, (1, K), order="C")
    G = cp.multiply(X, row(al)) - cp.reshape(D, (T, 1), order="C") @ np.ones((1, K)) - row(c)
    Dd, OP, OM = row(d), row(op), row(om)
    prod = lambda P, w, b: [P <= Omega * b, P <= w, P >= w - Omega * (1 - b)]
    cons = [al >= alpha_bounds[0], al <= alpha_bounds[1], op <= Omega, om <= Omega, cp.abs(c) <= M, d <= M,
            r >= D_obs - D, r >= D - D_obs, cp.abs(D) <= Dmax,
            G - Dd <= M * a, G - Dd >= -M * (1 - a), s <= a, G - Dd <= M * s, G - Dd >= delta - M * (1 - s),
            -G - Dd <= M * l, -G - Dd >= -M * (1 - l), z <= l, -G - Dd <= M * z, -G - Dd >= delta - M * (1 - z),
            up + dn <= 1, D <= Dmax * up, D >= -Dmax * dn, D >= delta - Dmax * (1 - up), D <= -delta + Dmax * (1 - dn)]
    cons += prod(Ps, OP, s) + prod(Pa, OP, a) + prod(Ql, OM, l) + prod(Qz, OM, z)
    right = -cp.sum(Ps, axis=1) + cp.sum(Ql, axis=1) + 1 - 2 * dn
    left = -cp.sum(Pa, axis=1) + cp.sum(Qz, axis=1) + 2 * up - 1
    cons += [right >= eps, left <= -eps]
    if fix is not None:
        idx = np.where(~free)[0]
        if len(idx):
            for k in ["a", "s", "l", "z"]:
                cons.append(V[k][idx, :] == fix[k][idx, :])
            for k in ["up", "dn"]:
                cons.append(V[k][idx] == fix[k][idx])
    return cp.Problem(cp.Minimize(cp.sum(r) / T), cons), V

def _states(V):
    return {k: np.round(V[k].value).astype(float) for k in ["a", "s", "l", "z", "up", "dn"]}

def _result(prob, V):
    alpha = V["al"].value
    return dict(status=prob.status, loss=prob.value, alpha=alpha, tau=V["c"].value / alpha, b=V["d"].value / alpha,
                beta=-1 / alpha, omega_p=V["op"].value, omega_m=V["om"].value, D=V["D"].value)

def fit_lns(X, D_obs, eps=0.05, delta=1e-3, Omega=5.0, M=30.0, Dmax=8.0, alpha_bounds=(0.05, 3.0),
            init_time=30, sub_size=12, iters=40, sub_time=20, cert_time=0, seed=0, log=None):
    """1) short full MILP for an incumbent; 2) LNS: free the binaries of a neighbourhood of periods (largest
    residuals plus random periods), fix the rest, solve the sub-MILP exactly, accept improvements;
    3) optional full MILP run to obtain a certified lower bound (reported as the MIP bound)."""
    rng = np.random.default_rng(seed); T, K = X.shape
    args = (eps, delta, Omega, M, Dmax, alpha_bounds)
    prob, V = _build_strict(X, D_obs, *args); prob.solve(solver=cp.HIGHS, time_limit=init_time)
    best, fix = _result(prob, V), _states(V); hist = [best["loss"]]
    for it in range(iters):
        res = np.abs(D_obs - best["D"])
        k1 = sub_size // 2
        worst = np.argsort(-res)[:k1]
        rand = rng.choice(np.setdiff1d(np.arange(T), worst), sub_size - k1, replace=False)
        free = np.zeros(T, bool); free[np.r_[worst, rand]] = True
        p2, V2 = _build_strict(X, D_obs, *args, fix=fix, free=free)
        p2.solve(solver=cp.HIGHS, time_limit=sub_time)
        if p2.value is not None and V2["al"].value is not None and p2.value < best["loss"] - 1e-9:
            best, fix = _result(p2, V2), _states(V2)
        hist.append(best["loss"])
        if log: log(it, best["loss"])
    best["history"] = hist
    if cert_time:
        p3, V3 = _build_strict(X, D_obs, *args)
        p3.solve(solver=cp.HIGHS, time_limit=cert_time)
        best["lower_bound"] = p3.solver_stats.extra_stats.mip_dual_bound if hasattr(p3.solver_stats.extra_stats, "mip_dual_bound") else None
        best["full_milp_loss"] = p3.value
    return best

# ---------------------------------------------------------------------------
# Hybrid algorithm: global search in parameter space (breakpoint enumeration makes each evaluation O(TK)),
# LP polishing with the states of the incumbent fixed, then LNS over states.

def forward_batch(X, alpha, tau, b, op, om):
    """Optimal decisions for all periods (Proposition 1), vectorised."""
    c, d = alpha * tau, alpha * b
    base = alpha * X - c                                       # (T, K)
    cand = np.concatenate([np.zeros((X.shape[0], 1)), base - d, base + d], axis=1)   # (T, 2K+1)
    g = base[:, :, None] - cand[:, None, :]                    # (T, K, J)
    F = (op[None, :, None] * np.maximum(0, g - d[None, :, None]) + om[None, :, None] * np.maximum(0, -g - d[None, :, None])).sum(1) + np.abs(cand)
    j = F.argmin(1)
    return cand[np.arange(X.shape[0]), j]

def global_search(X, D_obs, bounds=None, maxiter=300, popsize=30, seed=0):
    from scipy.optimize import differential_evolution
    K = X.shape[1]
    if bounds is None:
        bounds = [(0.05, 3.0)] * K + [(-3.0, 10.0)] * K + [(0.0, 4.0)] * K + [(0.0, 5.0)] * (2 * K)
    def unpack(v):
        return v[:K], v[K:2 * K], v[2 * K:3 * K], v[3 * K:4 * K], v[4 * K:5 * K]
    f = lambda v: np.abs(D_obs - forward_batch(X, *unpack(v))).mean()
    res = differential_evolution(f, bounds, maxiter=maxiter, popsize=popsize, seed=seed, tol=1e-8, polish=False)
    return unpack(res.x), res.fun

def states_from(X, D, alpha, tau, b, delta=1e-3):
    c, d = alpha * tau, alpha * b
    g = alpha * X - D[:, None] - c
    return dict(a=(g - d >= -1e-9).astype(float), s=(g - d > delta).astype(float), l=(-g - d >= -1e-9).astype(float),
                z=(-g - d > delta).astype(float), up=(D > delta).astype(float), dn=(D < -delta).astype(float))

def fit_hybrid(X, D_obs, eps=0.05, delta=1e-3, Omega=5.0, M=30.0, Dmax=8.0, alpha_bounds=(0.05, 3.0),
               de_iter=300, de_pop=30, lns_iters=20, sub_size=12, sub_time=10, seed=0):
    T, K = X.shape
    (alpha, tau, b, op, om), de_loss = global_search(X, D_obs, maxiter=de_iter, popsize=de_pop, seed=seed)
    D = forward_batch(X, alpha, tau, b, op, om)
    fix = states_from(X, D, alpha, tau, b, delta)
    args = (eps, delta, Omega, M, Dmax, alpha_bounds)
    p, V = _build_strict(X, D_obs, *args, fix=fix, free=np.zeros(T, bool))       # LP polish (all states fixed)
    p.solve(solver=cp.HIGHS)
    if V["al"].value is None:                                                     # margin infeasible at the DE point: free worst periods
        free = np.zeros(T, bool); free[np.argsort(-np.abs(D_obs - D))[:sub_size]] = True
        p, V = _build_strict(X, D_obs, *args, fix=fix, free=free); p.solve(solver=cp.HIGHS, time_limit=60)
    best = _result(p, V); best["de_loss"] = de_loss
    fix = _states(V); rng = np.random.default_rng(seed); hist = [best["loss"]]
    for it in range(lns_iters):
        res = np.abs(D_obs - best["D"]); k1 = sub_size // 2
        worst = np.argsort(-res)[:k1]; rand = rng.choice(np.setdiff1d(np.arange(T), worst), sub_size - k1, replace=False)
        free = np.zeros(T, bool); free[np.r_[worst, rand]] = True
        p2, V2 = _build_strict(X, D_obs, *args, fix=fix, free=free); p2.solve(solver=cp.HIGHS, time_limit=sub_time)
        if p2.value is not None and V2["al"].value is not None and p2.value < best["loss"] - 1e-9:
            best, fix = _result(p2, V2), _states(V2)
        hist.append(best["loss"])
    best["history"] = hist; best["de_loss"] = de_loss
    return best
