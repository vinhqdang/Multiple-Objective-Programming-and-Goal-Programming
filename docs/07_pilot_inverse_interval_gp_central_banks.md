# Pilot: inverse interval goal programming on central banks (2026-11-22)

Code: code/inverse_interval_gp_cb.py. Results: results/inverse_interval_gp_cb.csv.

## Design
- Forward model per month: minimise w_pi * dist(x, [T - b, T + b]) + w_s * |rate change|. Its optimum is a three-way rule (hold inside the band, raise above it, cut below it), so only the direction of each decision is used and the transmission strength need not be known.
- Inverse problem: choose (T, b) minimising the total hinge (suboptimality) violation of observed hike/hold/cut decisions. This is a linear program. Set estimate of T: all T whose profile loss is within 0.02 of the minimum. 90% interval: moving-block bootstrap (12-month blocks, 200 draws).
- Data: BIS policy rates and CPI y/y, monthly; months with the rate at or below 0.25% dropped. Nine banks with distinct stated targets (2, 2.5, 3, 4%); windows with a stable target. Inflation measured as current CPI y/y, or CPI y/y 12 months ahead as a perfect-foresight proxy for the forecast.
- Ground truth: stated targets (data/central_banks/targets.csv; several rows still need re-verification, see its README). The Fed, ECB and BoJ are excluded (zero lower bound for much of the period; the Fed targets PCE, not CPI).

## Result
| measure | MAE of T_hat vs stated target | corr(T_hat, stated) | MAE of mean inflation vs stated | corr(mean inflation, stated) |
|---|---|---|---|---|
| current CPI | 0.46 pp | 0.93 | 0.48 pp | 0.92 |
| CPI 12 months ahead | 0.44 pp | 0.91 | 0.47 pp | 0.93 |

T_hat tracks the stated targets across countries (correlation above 0.9), but a trivial benchmark, the mean inflation rate over the window, does just as well. Where inflation averaged away from target (Sweden 1.3% vs 2%, Mexico 4.2% vs 3%, India 5.0% vs 4%), T_hat follows mean inflation, not the stated target.

## Interpretation
- With a symmetric band and sign-only data, the estimator essentially centres T on the bulk of the inflation distribution. The pilot therefore does not show that inverse goal programming recovers targets better than the naive average.
- Two readings cannot be separated yet: the method is too weak, or the revealed target genuinely differs from the stated one (for example, the Riksbank was criticised for keeping policy tight while inflation was below target).

## What would make the test discriminating
1. Use magnitudes of rate changes (needs transmission, which can be calibrated from the literature or estimated from identified shocks).
2. Use the central banks' own published inflation forecasts instead of realised inflation.
3. Add the activity goal (output gap) and asymmetric weights, so supply-shock periods that the bank "looked through" do not pull T towards realised inflation.
4. Evaluate on windows where mean inflation and the stated target diverge, which is where the method must beat the benchmark.
