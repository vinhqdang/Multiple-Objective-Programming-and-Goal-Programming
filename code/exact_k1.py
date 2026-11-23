"""Exact global estimator for one-goal inverse interval goal programming with quadratic adjustment cost.

Closed form of the optimal decision (Theorem A1): with e_plus = c + d, e_minus = c - d (e_minus <= e_plus),
    D*(x) = clip(alpha x - e_plus, 0, omega_plus) + clip(alpha x - e_minus, -omega_minus, 0).
For fixed alpha the L1 loss is piecewise linear on the cells of a line arrangement; its global minimum is attained
at a vertex, whose e-coordinates lie in E = {z_t - D_s} U {z_t} (z = alpha x) and whose omega-coordinates lie in
{D_s} U {z_t - e} U {0}. The upper and lower parts separate given (e_minus, e_plus); the middle (dead-zone) cost is a
difference of prefix sums. Over alpha, the optimal loss is Lipschitz with constant mean|x|, which certifies the
global optimum of a grid search to within mean|x| * spacing / 2."""
import numpy as np

def h(x, alpha, e_p, e_m, om_p, om_m):
    z = alpha * x
    return np.clip(z - e_p, 0, om_p) + np.clip(z - e_m, -om_m, 0)

def _upper_best(z, D, E, om_max):
    """For each e in E: min over omega >= 0 of sum_{z_t > e} |D_t - min(z_t - e, omega)|, and the argmin omega."""
    best = np.full(len(E), np.inf); arg = np.zeros(len(E))
    Dpos = D[D > 0]
    for i, e in enumerate(E):
        m = z > e
        if not m.any():
            best[i], arg[i] = 0.0, 0.0; continue
        r, d = z[m] - e, D[m]
        W = np.unique(np.concatenate([[0.0, om_max], Dpos[Dpos <= om_max], r[r <= om_max]]))
        cost = np.abs(d[:, None] - np.minimum(r[:, None], W[None, :])).sum(0)
        k = cost.argmin(); best[i], arg[i] = cost[k], W[k]
    return best, arg

def solve_fixed_alpha(x, D, alpha, om_max=None):
    z = alpha * x; om_max = np.abs(D).max() * 1.0001 + 1e-12 if om_max is None else om_max
    E = np.unique(np.concatenate([(z[:, None] - D[None, :]).ravel(), z]))
    Up, Wp = _upper_best(z, D, E, om_max)                    # upper part at e_plus = E
    Lm, Wm = _upper_best(-z, -D, -E, om_max)                 # lower part at e_minus = E (mirror)
    absD = np.abs(D); order = np.argsort(z); zs, ds = z[order], absD[order]; cs = np.concatenate([[0], np.cumsum(ds)])
    A = cs[np.searchsorted(zs, E, side="right")]             # sum |D| over z <= e
    B = cs[np.searchsorted(zs, E, side="left")]              # sum |D| over z <  e
    left = Lm - B                                            # candidate e_minus values (E sorted ascending)
    run = np.minimum.accumulate(left); runarg = np.zeros(len(E), int)
    j = 0
    for i in range(len(E)):
        if left[i] <= left[j]: j = i
        runarg[i] = j
    total = run + Up + A                                     # best e_minus <= e_plus for each e_plus
    i = total.argmin(); jm = runarg[i]
    return dict(loss=total[i] / len(D), alpha=alpha, e_p=E[i], e_m=E[jm], om_p=Wp[i], om_m=Wm[jm],
                tau=(E[i] + E[jm]) / (2 * alpha), b=(E[i] - E[jm]) / (2 * alpha))

def solve(x, D, alpha_grid):
    """Certified grid search over alpha. Returns best solution and a certified lower bound on the global loss."""
    res = [solve_fixed_alpha(x, D, a) for a in alpha_grid]
    best = min(res, key=lambda r: r["loss"])
    eta = np.diff(np.sort(alpha_grid)).max() if len(alpha_grid) > 1 else 0.0
    best["lower_bound"] = best["loss"] - np.abs(x).mean() * eta / 2
    return best, res

def tau_set(x, D, alpha, rel=0.02, om_max=None):
    """Range of tau over all candidate solutions whose loss is within (1+rel) of the exact optimum."""
    z = alpha * x; om_max = np.abs(D).max() * 1.0001 + 1e-12 if om_max is None else om_max
    E = np.unique(np.concatenate([(z[:, None] - D[None, :]).ravel(), z]))
    Up, _ = _upper_best(z, D, E, om_max); Lm, _ = _upper_best(-z, -D, -E, om_max)
    absD = np.abs(D); order = np.argsort(z); zs, ds = z[order], absD[order]; cs = np.concatenate([[0], np.cumsum(ds)])
    A = cs[np.searchsorted(zs, E, side="right")]; B = cs[np.searchsorted(zs, E, side="left")]
    left, right = Lm - B, Up + A
    best = (np.minimum.accumulate(left) + right).min(); thr = best * (1 + rel)
    lo, hi = np.inf, -np.inf
    for i in range(len(E)):
        ok = np.where(left[: i + 1] + right[i] <= thr)[0]
        if len(ok):
            lo = min(lo, (E[i] + E[ok[0]]) / (2 * alpha)); hi = max(hi, (E[i] + E[ok[-1]]) / (2 * alpha))
    return lo, hi, best / len(D)

def profile_tau(x, D, alpha, taus, om_max=None):
    """Exact profile loss: for each tau, the minimum loss over (b, omega+, omega-) with tau fixed.
    With e_plus = alpha*tau + d and e_minus = alpha*tau - d (d >= 0), the objective is piecewise linear in
    (d, omega+, omega-); the optimal d lies in {+-(z_t - D_s - alpha*tau)} U {+-(z_t - alpha*tau)} U {0}."""
    z = alpha * x; om_max = np.abs(D).max() * 1.0001 + 1e-12 if om_max is None else om_max
    absD = np.abs(D); order = np.argsort(z); zs, ds = z[order], absD[order]; cs = np.concatenate([[0], np.cumsum(ds)])
    base = np.unique(np.concatenate([(z[:, None] - D[None, :]).ravel(), z]))
    out = []
    for tau in taus:
        c = alpha * tau
        dd = np.unique(np.abs(np.concatenate([base - c, [0.0]])))
        ep, em = c + dd, c - dd
        Up, _ = _upper_best(z, D, ep, om_max); Lm, _ = _upper_best(-z, -D, -em, om_max)
        mid = cs[np.searchsorted(zs, ep, side="right")] - cs[np.searchsorted(zs, em, side="left")]
        out.append((Up + Lm + mid).min() / len(D))
    return np.array(out)

def tau_set_profile(x, D, alpha, rel=0.02, step=0.005, lo=None, hi=None):
    """Near-optimal tau set from the exact profile on a grid (spacing `step`)."""
    lo = x.min() - 1 if lo is None else lo; hi = x.max() + 1 if hi is None else hi
    taus = np.arange(lo, hi + step / 2, step); prof = profile_tau(x, D, alpha, taus)
    best = prof.min(); ok = taus[prof <= best * (1 + rel) + 1e-12]
    return ok.min(), ok.max(), best, (len(ok) == ((ok.max() - ok.min()) / step + 1).round())   # last: contiguous?
