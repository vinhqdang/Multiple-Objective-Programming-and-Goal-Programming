"""Inverse interval goal programming with QUADRATIC adjustment cost (gradualism).

Forward model per period: F_t(D) = sum_k [omega_k^+ (g_k - d_k)_+ + omega_k^- (-g_k - d_k)_+] + D^2 / 2,
with g_k = alpha_k x_kt - D - c_k (same change of variables as migp.py; tau = c/alpha, b = d/alpha).
F_t is strictly convex, so the optimum is unique. Optimality: D = sum_k (p_k - q_k), p_k in [0, omega_k^+]
(= omega_k^+ strictly above the band, 0 strictly inside), q_k likewise. While goal k is strictly outside its band
and the edge is not reached, the step is D = omega_k (constant steps: gradualism)."""
import numpy as np, cvxpy as cp
from itertools import product

def forward_batch(X, alpha, tau, b, op, om):
    T, K = X.shape
    c, d = alpha * tau, alpha * b
    base = alpha * X - c
    bps = np.concatenate([base - d, base + d], axis=1)                      # breakpoints (T, 2K)
    sums = np.array([sum(v) for v in product(*[(op[k], 0.0, -om[k]) for k in range(K)])])   # possible slope sums
    cand = np.concatenate([bps, np.tile(sums, (T, 1))], axis=1)            # (T, J)
    g = base[:, :, None] - cand[:, None, :]
    F = (op[None, :, None] * np.maximum(0, g - d[None, :, None]) + om[None, :, None] * np.maximum(0, -g - d[None, :, None])).sum(1) + 0.5 * cand ** 2
    return cand[np.arange(T), F.argmin(1)]

def _build(X, D_obs, Omega=5.0, M=30.0, Dmax=8.0, alpha_bounds=(0.05, 3.0), delta=1e-3, fix=None, free=None):
    T, K = X.shape
    V = dict(al=cp.Variable(K), c=cp.Variable(K), d=cp.Variable(K, nonneg=True), op=cp.Variable(K, nonneg=True),
             om=cp.Variable(K, nonneg=True), D=cp.Variable(T), r=cp.Variable(T, nonneg=True),
             p=cp.Variable((T, K), nonneg=True), q=cp.Variable((T, K), nonneg=True),
             a=cp.Variable((T, K), boolean=True), s=cp.Variable((T, K), boolean=True),
             l=cp.Variable((T, K), boolean=True), z=cp.Variable((T, K), boolean=True))
    al, c, d, op, om, D, r, p, q, a, s, l, z = (V[k] for k in ["al", "c", "d", "op", "om", "D", "r", "p", "q", "a", "s", "l", "z"])
    one = np.ones((T, 1)); row = lambda v: one @ cp.reshape(v, (1, K), order="C")
    G = cp.multiply(X, row(al)) - cp.reshape(D, (T, 1), order="C") @ np.ones((1, K)) - row(c)
    Dd, OP, OM = row(d), row(op), row(om)
    cons = [al >= alpha_bounds[0], al <= alpha_bounds[1], op <= Omega, om <= Omega, cp.abs(c) <= M, d <= M,
            r >= D_obs - D, r >= D - D_obs, cp.abs(D) <= Dmax,
            G - Dd <= M * a, G - Dd >= -M * (1 - a), s <= a, G - Dd <= M * s, G - Dd >= delta - M * (1 - s),
            p <= Omega * a, p <= OP, p >= OP - Omega * (1 - s),
            -G - Dd <= M * l, -G - Dd >= -M * (1 - l), z <= l, -G - Dd <= M * z, -G - Dd >= delta - M * (1 - z),
            q <= Omega * l, q <= OM, q >= OM - Omega * (1 - z),
            D == cp.sum(p - q, axis=1)]                                     # stationarity of the strictly convex F_t
    if fix is not None:
        idx = np.where(~free)[0]
        if len(idx):
            for k in ["a", "s", "l", "z"]:
                cons.append(V[k][idx, :] == fix[k][idx, :])
    return cp.Problem(cp.Minimize(cp.sum(r) / T), cons), V

def _res(p, V):
    al = V["al"].value
    return dict(status=p.status, loss=p.value, alpha=al, tau=V["c"].value / al, b=V["d"].value / al,
                omega_p=V["op"].value, omega_m=V["om"].value, D=V["D"].value)

def states_from(X, D, alpha, tau, b, delta=1e-3):
    g = alpha * X - D[:, None] - alpha * tau; d = alpha * b
    return dict(a=(g - d >= -1e-9).astype(float), s=(g - d > delta).astype(float),
                l=(-g - d >= -1e-9).astype(float), z=(-g - d > delta).astype(float))

def fit_hybrid(X, D_obs, de_iter=3000, de_pop=80, lns_iters=20, sub_size=12, sub_time=10, seed=0, **kw):
    from scipy.optimize import differential_evolution
    T, K = X.shape
    bounds = [(0.05, 3.0)] * K + [(-3.0, 10.0)] * K + [(0.0, 4.0)] * K + [(0.0, 5.0)] * (2 * K)
    unpack = lambda v: (v[:K], v[K:2 * K], v[2 * K:3 * K], v[3 * K:4 * K], v[4 * K:])
    f = lambda v: np.abs(D_obs - forward_batch(X, *unpack(v))).mean()
    de = differential_evolution(f, bounds, maxiter=de_iter, popsize=de_pop, seed=seed, tol=1e-10, polish=False,
                                strategy="currenttobest1bin", mutation=(0.5, 1.0), recombination=0.9)
    th = unpack(de.x); Dde = forward_batch(X, *th)
    fix = states_from(X, Dde, th[0], th[1], th[2])
    p, V = _build(X, D_obs, fix=fix, free=np.zeros(T, bool), **kw); p.solve(solver=cp.HIGHS)
    best = _res(p, V) if V["al"].value is not None else dict(loss=de.fun, alpha=th[0], tau=th[1], b=th[2], omega_p=th[3], omega_m=th[4], D=Dde)
    if V["al"].value is not None: fix = {k: np.round(V[k].value) for k in ["a", "s", "l", "z"]}
    rng = np.random.default_rng(seed)
    for it in range(lns_iters):
        res = np.abs(D_obs - best["D"]); k1 = sub_size // 2
        worst = np.argsort(-res)[:k1]; rand = rng.choice(np.setdiff1d(np.arange(T), worst), sub_size - k1, replace=False)
        free = np.zeros(T, bool); free[np.r_[worst, rand]] = True
        p2, V2 = _build(X, D_obs, fix=fix, free=free, **kw); p2.solve(solver=cp.HIGHS, time_limit=sub_time)
        if p2.value is not None and V2["al"].value is not None and p2.value < best["loss"] - 1e-9:
            best = _res(p2, V2); fix = {k: np.round(V2[k].value) for k in ["a", "s", "l", "z"]}
    best["de_loss"] = de.fun
    return best

# ---------------------------------------------------------------------------
# Multistart local search (parallel Powell on the continuous decision loss) + exact LP/LNS polishing.
_G = {}
def _ms_init(X, D_obs, lo, hi):
    _G.update(X=X, D=D_obs, lo=lo, hi=hi)

def _ms_loss(v):
    lo, hi, K = _G["lo"], _G["hi"], _G["X"].shape[1]
    v = np.clip(v, lo, hi)
    return np.abs(_G["D"] - forward_batch(_G["X"], v[:K], v[K:2*K], v[2*K:3*K], v[3*K:4*K], v[4*K:])).mean()

def _ms_run(seed):
    from scipy.optimize import minimize
    lo, hi = _G["lo"], _G["hi"]
    v0 = lo + np.random.default_rng(seed).random(len(lo)) * (hi - lo)
    r = minimize(_ms_loss, v0, method="Powell", bounds=list(zip(lo, hi)), options={"maxiter": 20000, "xtol": 1e-6, "ftol": 1e-9})
    return r.fun, np.clip(r.x, lo, hi)

def polish(X, D_obs, v, lns_iters=15, sub_size=12, sub_time=10, seed=0, **kw):
    T, K = X.shape
    th = (v[:K], v[K:2*K], v[2*K:3*K], v[3*K:4*K], v[4*K:])
    D0 = forward_batch(X, *th); fix = states_from(X, D0, th[0], th[1], th[2])
    best = dict(loss=np.abs(D_obs - D0).mean(), alpha=th[0], tau=th[1], b=th[2], omega_p=th[3], omega_m=th[4], D=D0)
    p, V = _build(X, D_obs, fix=fix, free=np.zeros(T, bool), **kw)
    try: p.solve(solver=cp.HIGHS)
    except cp.error.SolverError: pass
    if V["al"].value is not None and p.value is not None and p.value < best["loss"]:
        best = _res(p, V); fix = {k: np.round(V[k].value) for k in ["a", "s", "l", "z"]}
    rng = np.random.default_rng(seed)
    for it in range(lns_iters):
        res = np.abs(D_obs - best["D"]); k1 = sub_size // 2
        worst = np.argsort(-res)[:k1]; rand = rng.choice(np.setdiff1d(np.arange(T), worst), sub_size - k1, replace=False)
        free = np.zeros(T, bool); free[np.r_[worst, rand]] = True
        p2, V2 = _build(X, D_obs, fix=fix, free=free, **kw)
        try: p2.solve(solver=cp.HIGHS, time_limit=sub_time)
        except cp.error.SolverError: continue
        if p2.value is not None and V2["al"].value is not None and p2.value < best["loss"] - 1e-9:
            best = _res(p2, V2); fix = {k: np.round(V2[k].value) for k in ["a", "s", "l", "z"]}
    return best

def fit_ms(X, D_obs, n_starts=800, top=5, procs=4, seed=0, lo=None, hi=None, **kw):
    from multiprocessing import Pool
    T, K = X.shape
    lo = np.array([0.05]*K + [-3.0]*K + [0.0]*K + [0.0]*(2*K)) if lo is None else lo
    hi = np.array([3.0]*K + [10.0]*K + [4.0]*K + [5.0]*(2*K)) if hi is None else hi
    with Pool(procs, initializer=_ms_init, initargs=(X, D_obs, lo, hi)) as pool:
        res = pool.map(_ms_run, range(seed * 100000, seed * 100000 + n_starts))
    res.sort(key=lambda z: z[0])
    best = None
    for f0, v in res[:top]:
        h = polish(X, D_obs, v, **kw)
        if best is None or h["loss"] < best["loss"]: best = h
    best["ms_loss"] = res[0][0]
    return best
