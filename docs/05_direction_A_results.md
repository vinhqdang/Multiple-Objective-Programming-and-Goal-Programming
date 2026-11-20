# Direction A: IPPA on a Cobb-Douglas goal program with learned elasticities

## Model (code/ippa_cd.py)
Allocation x > 0 on the positive orthant with metric diag(1/x^2), the Hadamard manifold of Example 6.1 in paper 15 (flat in theta = log x). Goal k has outcome exp(b_k + a_k' theta). Objectives: log shortfall of each goal, max(0, ln T_k - b_k - a_k' theta), and relative spend sum(x)/B. All are nonnegative, locally Lipschitz and geodesically convex, so assumptions A1-A3 of paper 15 hold. A4 (completeness) holds by a boundedness argument (spend caps theta above; a positive elasticity for every unit then bounds theta below); this is my sketch and not a checked proof.

## What is established
1. Application of paper 15, Corollary 4.1: IPPA converges to a weakly Pareto optimal point of the learned problem. Not new. Numerically: all objectives decrease monotonically, and the weak-Pareto gap falls to 0 within about 300 iterations (n = 40 units, 4 goals).
2. Elementary stability proposition (proved here, simple): if w_hat is weakly Pareto optimal for the learned objectives and the goal objectives differ from the true ones by at most eps(w) at a point w, then the improvement t available in all true objectives satisfies t <= eps(w_hat) + eps(w*), where w* is the improving point. Spend is known exactly so it carries no error.
3. Numerical check (code/ippa_stability.py, 15 replications per N, noise sd 0.15, OLS on log-log data):

| N | mean abs. error of elasticities | gap, IPPA on learned model | gap, equal split | proposition bound | gap / error^2 |
|---|---|---|---|---|---|
| 100 | 0.833 | 0.0662 (se 0.0049) | 0.0410 | 4.08 | 0.095 |
| 200 | 0.561 | 0.0439 (se 0.0027) | 0.0399 | 2.07 | 0.140 |
| 400 | 0.374 | 0.0232 (se 0.0014) | 0.0405 | 1.38 | 0.167 |
| 800 | 0.273 | 0.0128 (se 0.0007) | 0.0373 | 0.97 | 0.172 |
| 1600 | 0.198 | 0.0077 (se 0.0006) | 0.0383 | 0.69 | 0.196 |
| 3200 | 0.136 | 0.0036 (se 0.0002) | 0.0397 | 0.58 | 0.194 |

The proposition held in all 90 runs but is far too loose to be useful (bound 0.58 to 4.1 against gaps of 0.004 to 0.066).

## Observations
- Below roughly N = 300 historical observations, the learned solution leaves more improvement on the table than equal split (0.066 and 0.044 against 0.040 at N = 100 and 200). The learned model only pays off with enough data.
- The gap behaves like c times error squared with c about 0.19 for N >= 800 (last column). A quadratic rate would be the natural second-order regret result for a plug-in solution. This is a numerical pattern in one design, not a theorem.

## Assessment
Items 1 and 2 are an application and an elementary corollary. The model is a reasonable fit for paper 15's framework, but there is no new theorem yet. A sharp bound (quadratic in the estimation error, with explicit constants and regularity conditions) would be genuine content; it is unproven and may need conditions I have not identified. Not yet tried: real data, other weight sequences u_k, constraints such as caps.
