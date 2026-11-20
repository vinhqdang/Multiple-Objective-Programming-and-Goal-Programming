# Quadratic bound for plug-in goal programming solutions (draft proof, not yet checked by an expert)

## Setting
Work in theta = log x in R^n (the positive orthant with metric diag(1/x^2) is flat in these coordinates). True goal functions l_k(theta) = r_k - a_k' theta with r_k = ln T_k - b_k, learned ones lhat_k(theta) = rhat_k - ahat_k' theta. Objectives: F_k = max(0, l_k) for k = 1..K and F_(K+1) = c(theta) = (1/B) sum_i exp(theta_i), the relative spend, which is known exactly. Hatted versions use the learned goal functions. Write Delta a_k = ahat_k - a_k. For a box Theta = [theta_lo, theta_hi]^n, define the true gap of a point theta_hat

  g_Theta(theta_hat) = sup { t >= 0 : exists theta in Theta with F_i(theta) <= F_i(theta_hat) - t for all i = 1..K+1 }

(the largest improvement available in all true objectives at once; zero iff theta_hat is weakly Pareto optimal within Theta).

## Theorem
Let theta_hat in Theta be a weakly Pareto optimal point of the learned problem (for example the limit of the inertial proximal point algorithm of Upadhyay et al., whose Corollary 4.1 gives convergence to such a point). By Step 1 below there is a weight vector w in the simplex with theta_hat minimising the learned weighted sum. Let A = {k : lhat_k(theta_hat) > 0}. Assume

(H1) w_c := w_(K+1) > 0;
(H2) sign stability: for every k with w_k > 0, l_k(theta_hat) and lhat_k(theta_hat) are both strictly positive or both strictly negative.

Then
  g_Theta(theta_hat) <= B e^(-theta_lo) ( sum_(k in A) w_k ||Delta a_k||_2 )^2 / (2 w_c)
                     <= B e^(-theta_lo) (1 - w_c)^2 max_(k in A) ||Delta a_k||_2^2 / (2 w_c).

If theta_hat is only approximately stationary, with residual norm rho (defined in Step 2), replace the sum by (sum + rho).
(H1) holds whenever some unit has a positive learned elasticity on a goal that is unmet at theta_hat: coordinate i of the stationarity equation reads w_c e^(theta_i)/B = sum_(k in A) w_k ahat_ik.

## Proof
Step 1 (supporting weights). Fhat is convex. The set C = Fhat(R^n) + R_+^(K+1) is convex, and weak Pareto optimality means C does not meet the open set Fhat(theta_hat) - int R_+^(K+1). Separate: there is w != 0 with w'y >= w'Fhat(theta_hat) for y in C. Since C is closed under adding R_+^(K+1), w >= 0; normalise sum w = 1. Then theta_hat minimises Shat_w = w'Fhat over R^n.

Step 2 (stationarity). All terms are finite convex functions, so 0 is in the subdifferential: there are s_k in [0,1], with s_k = 1 if lhat_k(theta_hat) > 0 and s_k = 0 if < 0, such that
  0 = - sum_k w_k s_k ahat_k + w_c grad c(theta_hat).
(Approximate version: the right-hand side has norm rho.)

Step 3 (a true subgradient). By (H2), for every k with w_k > 0 the multiplier s_k equals 1[l_k(theta_hat) > 0], which is the unique subgradient coefficient of max(0, l_k) at theta_hat. Hence
  g := - sum_k w_k s_k a_k + w_c grad c(theta_hat)
belongs to the subdifferential of S_w = w'F at theta_hat, and by Step 2
  g = sum_k w_k s_k (ahat_k - a_k),   so   ||g|| <= sum_(k in A) w_k ||Delta a_k||   (plus rho in the approximate case).

Step 4 (strong convexity on Theta). The goal terms are convex. The Hessian of c is diag(e^(theta_i)/B), at least e^(theta_lo)/B times the identity on Theta, so c is mu_c-strongly convex there with mu_c = e^(theta_lo)/B. Therefore S_w is mu-strongly convex on Theta with mu = w_c e^(theta_lo)/B, and for every theta in Theta
  S_w(theta) >= S_w(theta_hat) + <g, theta - theta_hat> + (mu/2) ||theta - theta_hat||^2.

Step 5 (regret). Rearranging, S_w(theta_hat) - S_w(theta) <= <g, theta_hat - theta> - (mu/2)||theta_hat - theta||^2 <= ||g||^2 / (2 mu).

Step 6 (gap). If theta in Theta improves every true objective by at least t, then S_w(theta_hat) - S_w(theta) >= t sum_i w_i = t. By Step 5, t <= ||g||^2/(2 mu). Taking the supremum over such theta and inserting Steps 3 and 4 gives the theorem. The second inequality uses sum_(k in A) w_k <= 1 - w_c. QED.

## Remarks
1. Role of the inertial proximal algorithm: the theorem holds for any weakly Pareto point of the learned problem. The algorithm supplies such a point, and its convergence guarantee is paper 15's Corollary 4.1, which I applied but did not re-prove.
2. Why (H2) is needed. With one goal, S(theta) = w (L - a theta)_+ + (1-w) e^theta, when the goal is attained exactly at the optimum the minimiser sits at the kink theta* = L/a. Learning a_hat moves the kink to L/a_hat, and the loss of the true S is about m |theta_hat - theta*| with m = w a - (1-w) e^(theta*) > 0, which is first order in |a_hat - a|. So the quadratic rate fails when a goal is met exactly with a binding trade-off.
3. The constant e^(-theta_lo) grows if a unit receives very little budget, because the cost term then barely curves. The bound is therefore informative only when allocations stay bounded away from zero.
4. The method (strong convexity plus a sign-stable subgradient) is classical, and quadratic regret for plug-in solutions is a familiar phenomenon. I have not searched whether this exact statement for goal-weight scalarisations of weakly Pareto limits already appears in print.

## Numerical check (code/ippa_quadratic_bound.py)
Same design as docs/05 (n = 40 units, 4 goals, OLS elasticities, noise sd 0.15, 10 replications per N, box Theta = [min theta_hat - 1, max theta_hat + 1]). Supporting weights were recovered from the stationarity equations by nonnegative least squares.

| N | observed gap | bound | gap / bound | max residual rho | sign condition held | bound held |
|---|---|---|---|---|---|---|
| 200 | 0.0442 | 4.038 | 0.015 | 0.00053 | 100% | 100% |
| 800 | 0.0130 | 0.591 | 0.026 | 0.00018 | 100% | 100% |
| 3200 | 0.0036 | 0.142 | 0.026 | 0.00010 | 100% | 100% |

The bound held in all 30 runs and (H2) held in all of them. The bound is 40 to 70 times larger than the observed gap, a constant-factor looseness (the factor e^(-theta_lo) and the global strong convexity modulus), but both quantities fall by about the same factor when the sample grows four-fold (gap 0.0130 to 0.0036, bound 0.59 to 0.14), consistent with a quadratic rate in the estimation error.
