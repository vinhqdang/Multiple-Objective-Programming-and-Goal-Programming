# Pre-registration: confirmatory test of the gradualism inverse goal-programming model on new central banks

Written and committed on 2026-11-22, before the confirmatory target table exists and before any estimation on these banks.

## Hypothesis
The implied inflation target from the gradualism model (code/migp_quad.py) is closer to the stated target than average inflation over the same window, in particular for banks whose average inflation deviated from target. This pattern was found in exploratory work on GB, CA, NO, SE, AU, MX, CL, IN, PL (docs/08, Section 10); those nine banks are excluded here.

## Sample (fixed rule)
Candidate banks: inflation targeters with BIS policy rates, BIS CPI and OECD quarterly GDP growth in data/central_banks, not among the nine exploratory banks: CZ, HU, KR, IL, CO, ID, TR, IS, NZ. A bank enters if a numeric target (point, or the midpoint of a band) and its validity dates are verified from a fetched source (data/central_banks/targets_confirmatory.csv, to be compiled after this file is committed). Switzerland is excluded in advance (its definition is a range "below 2%" without a point). PE, PH, TH, RO are excluded because quarterly GDP growth is not in the dataset.

## Window rule
For each bank, take the longest period with an unchanged numeric target that ends no later than 2019Q4; drop quarters whose policy rate at the start of the quarter is at or below 0.25%; require at least 30 remaining quarters, otherwise the bank is reported as excluded.

## Specification (identical to code/real_cb_quad.py, realised input)
Quarterly data; decision D = change in the end-of-quarter policy rate; inflation input = CPI y/y at the end of quarter q+3; activity input = GDP growth y/y in quarter q minus its window mean; K = 2; estimator migp_quad.fit_hybrid with default settings and seeds 0, 1, 2, keeping the lowest-loss fit. No other specification will be reported as the confirmatory result.

## Outcomes and success criteria
1. MAE of (implied target - stated target) versus MAE of (mean inflation - stated target) over all included banks.
2. Among included banks with |mean inflation - stated| > 0.5 pp: the share in which the implied target is closer to the stated target than mean inflation, and the MAE of each.
The test is counted as supportive if, in outcome 2, the implied target is closer in more than half of the banks and has the lower MAE. All results will be reported whether supportive or not.

## Result (run 2026-11-22, results/confirmatory_cb.csv)
Included banks (at least 30 quarters after the window rule): IL, NZ, CO, HU, TR. Excluded: CZ (20 quarters above the 0.25% rate floor), KR (12), IS (4).

| bank | stated | implied target | mean inflation |
|---|---|---|---|
| IL | 2.0 | 3.49 | 1.77 |
| NZ | 2.0 | 1.66 | 2.54 |
| CO | 3.0 | 3.02 | 3.79 |
| HU | 3.0 | 4.97 | 3.33 |
| TR | 5.0 | 6.14 | 10.70 |

- Outcome 1: MAE implied 0.99 pp vs mean inflation 1.52 pp (n = 5).
- Outcome 2: three banks had |mean - stated| > 0.5 (NZ, CO, TR); the implied target was closer in all three; MAE 0.50 vs 2.34. By the pre-registered criterion the test is supportive.
- Not supportive elsewhere: for the two banks whose average inflation was close to target (IL, HU) the implied target was much further from the stated target than average inflation (errors 1.49 and 1.97 pp). The overall MAE advantage depends heavily on Turkey.
- The sample is small (five banks; three in outcome 2). Combined with the exploratory banks, the implied target was closer than mean inflation in all seven off-target cases, and less reliable when inflation was on target.
