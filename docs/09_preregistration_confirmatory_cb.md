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
