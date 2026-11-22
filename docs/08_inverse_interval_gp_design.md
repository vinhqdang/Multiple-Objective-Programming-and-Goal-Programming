# Inverse interval goal programming for sequential policy decisions: formulation, identification, exact estimator

Draft, 2026-11-22. Proofs are sketches written by us and have not been checked by an independent expert.

## 1. Forward model
At decision time t the decision maker (a central bank) observes a forecast vector x_t in R^K of goal variables if policy is unchanged (inflation, activity gap) and chooses a policy change D (percentage points). Goal k responds linearly, y_k(D) = x_kt + beta_k D with beta_k < 0 (tightening lowers inflation and activity). Each goal is an interval goal [tau_k - b_k, tau_k + b_k] with asymmetric weights, and changing policy has unit cost (normalisation lambda = 1):

  F_t(D) = sum_k [ w_k^+ (y_k(D) - tau_k - b_k)_+ + w_k^- (tau_k - b_k - y_k(D))_+ ] + |D|.

Change of variables. Let alpha_k = 1/|beta_k| (policy change needed to move goal k by one unit), c_k = alpha_k tau_k, d_k = alpha_k b_k, omega_k^pm = w_k^pm / alpha_k, and g_kt(D) = alpha_k x_kt - D - c_k (= alpha_k (y_k(D) - tau_k)). Then

  F_t(D) = sum_k [ omega_k^+ (g_kt(D) - d_k)_+ + omega_k^- (-g_kt(D) - d_k)_+ ] + |D|,

which is linear in all parameters (alpha, c, d) inside the kinks and in omega outside them.

## 2. Structural results
**Proposition 1 (breakpoint property).** F_t is convex, piecewise linear and coercive in D, so its minimum is attained, and some minimiser lies in the finite set C_t = {0} union {alpha_k x_kt - c_k - d_k, alpha_k x_kt - c_k + d_k : k = 1..K}.
Sketch: each term is convex piecewise linear in D; the slope tends to 1 + sum_k omega_k^- > 0 as D -> +inf and to -(1 + sum_k omega_k^+) < 0 as D -> -inf; a convex piecewise-linear coercive function attains its minimum at a breakpoint.

**Proposition 2 (observational equivalence).** Decisions depend on (w, beta, tau, b) only through (alpha, tau, b, omega). In particular, raw weights w_k and transmission beta_k are not separately identified; the effective weight omega_k = w_k |beta_k| (marginal goal gain per unit of policy) is the identifiable object. Sketch: the substitution in Section 1 is exact.

**Proposition 3 (edge revelation of aspiration levels).** If at an optimum goal k sits on its upper (lower) band edge, then D* = alpha_k x_kt - c_k - d_k (respectively + d_k), equivalently tau_k + b_k = x_kt - D*/alpha_k (respectively tau_k - b_k). With noiseless decisions, two upper-edge observations with distinct x_kt and two lower-edge observations with distinct x_kt determine alpha_k, tau_k and b_k uniquely. Sketch: each edge observation is a linear equation in (alpha_k, c_k + d_k) or (alpha_k, c_k - d_k).

**Proposition 4 (weights are set-identified, generically never point-identified).** Fix (alpha, c, d). Optimality of D* is 0 in the subdifferential of F_t at D*: sigma = sum_k (p_k - q_k), with sigma in the subdifferential of |D| at D*, p_k in [0, omega_k^+] (= omega_k^+ if goal k is strictly above its band, = 0 if strictly below its upper edge) and similarly q_k. By Proposition 1, D* is a breakpoint, so at least one of sigma, p_k, q_k ranges over an interval. The stationarity condition therefore restricts omega only through inequalities, and the set of omega consistent with any sample is a polyhedron that is generically full-dimensional. Point identification of omega can only arise from coincident breakpoints (degenerate data). Consequence: priorities are reported as sets (bounds per weight), aspiration levels as points.

These results contrast with quadratic-loss inverse models (Taylor-rule type), where weights and targets enter a smooth policy rule and are point-identified only jointly with the neutral rate.

## 3. Exact estimator: mixed-integer inverse goal programming (MI-IGP)
Observed decisions D_t^obs = D*_t + noise. Decision-space L1 estimator:

  min over (alpha, c, d, omega) and (D*_t)  sum_t |D_t^obs - D*_t|   subject to D*_t optimal for F_t.

Optimality is written exactly with the subgradient conditions of Proposition 4 and binary state variables per goal and period (upper-active, upper-full, lower-active, lower-full) plus up/down variables for |D|. Every constraint is linear because of the change of variables: g_kt = alpha_k x_kt - D*_t - c_k is linear in the unknowns, and p_k >= omega_k^+ - Omega (1 - s_kt) links multipliers to weights. The result is a mixed-integer linear program solved to global optimality (or with a certified gap) by branch and bound. Recovery: tau_k = c_k/alpha_k, b_k = d_k/alpha_k, beta_k = -1/alpha_k. A second stage computes the identified set of omega by solving, for each weight, min and max linear programs over the stationarity constraints with the estimated states fixed.

Known results this builds on: decision-space losses are statistically consistent but NP-hard in general (Aswani, Shen & Siddiq 2018); here the goal-programming structure makes the exact estimator a MILP of size O(TK).

## 4. Evaluation plan
1. Synthetic data from the forward model with known parameters: recovery of tau, b, alpha; coverage of the omega identified set.
2. Central banks with stated targets (ground truth). Baselines: mean inflation; a difference Taylor rule D_t = a + phi x_pi,t + gamma x_gap,t with implied target -a/phi; the sign-only pilot (docs/07).
3. Then defence and aid budgets, and firms, where targets are not known.

## 5. Refinement: strict-optimality margin (implemented as migp.fit_strict)
The plain estimator (migp.fit) is ill-posed under noise: when an effective weight equals the unit adjustment cost (omega = 1), or a sum of slopes cancels, F_t is flat on a segment, every point of the segment is optimal, and the fitted decisions can absorb the noise. We therefore require strict optimality with margin eps > 0 at each fitted decision:

  right derivative of F_t at D*_t >= eps,   left derivative <= -eps.

With the state binaries (upper active a, strictly above s, lower active l, strictly below z, up/down for |D|), the one-sided derivatives are linear in products omega x binary, linearised exactly by McCormick constraints:

  right = - sum_k omega_k^+ s_k + sum_k omega_k^- l_k + 1 - 2 dn,   left = - sum_k omega_k^+ a_k + sum_k omega_k^- z_k + 2 up - 1.

Strict optimality implies optimality, so the stationarity equality is no longer needed. Interpretation: observed decisions are not knife-edge; the decision maker strictly prefers the chosen change. The identified set for omega becomes {omega : margins hold}, still a polyhedron (Proposition 4).

## 6. Synthetic check (K = 1, T = 80 quarters, true tau = 2.5, b = 0.5, alpha = 0.8; Laplace decision noise)
| noise scale | tau_hat | b_hat | alpha_hat | solver |
|---|---|---|---|---|
| 0 | 2.50 | 0.50 | 0.80 | optimal |
| 0.05 | 2.50 | 0.45 | 0.77 | optimal (70 s) |
| 0.15 | 2.53 | 0.42 | 0.77 | time limit 120 s |
| 0.30 | 2.66 | 0.59 | 0.75 | time limit 120 s |
The plain estimator on the same data gave tau_hat = 2.64 and 2.07 with b_hat near 0 at noise 0.05 and 0.15 (flat-optimum overfitting). Weights are returned at the boundary of their identified set (about 1.05 = 1 + eps), as Proposition 4 predicts.

With K = 2 (inflation and activity, T = 80, noiseless), the plain estimator fitted the decisions exactly but recovered only the upper edge of the inflation band (tau + b = 3.0), because no period had the lower inflation edge binding: an instance of Proposition 3's coverage condition. Aspiration levels must therefore be reported as identified sets when an edge never binds.
