# Direction G4: inverse goal programming for public budgets. Synthesis of notes 05-07 (2026-11-22)

About 50 further papers read (per-paper notes and read scope in 05, 06, 07). Key identifiers re-checked on arxiv.org, nber.org and Crossref. The search is not systematic (OpenAlex quota exhausted; several publisher PDFs blocked), so absence claims below are provisional.

## What exists
- **Inverse optimization** is mature (Chan, Mahmood & Zhu review, Operations Research 73(2), 2025). Only the minimiser map is identified and a normalisation is required; for LP-type problems with vertex optima, weights are generically not point-identified (Ahmadi, Ganjkhanloo & Ghobadi, arXiv 2603.17033, Thm 1; their "goal-integrated" models concern an observation-constraint trade-off, not goal programming). KKT and variational-inequality estimators are inconsistent under decision noise; the decision-space loss is consistent but NP-hard (Aswani, Shen & Siddiq, Operations Research 2018, Prop. 1, Cor. 2, Thms 2-4).
- **Inverse multiobjective optimization** infers weights (Chan, Craig, Lee & Sharpe, Operations Research 2014, cancer therapy, DOI 10.1287/opre.2014.1267; Chan & Lee 2018; Dong & Zeng 2018 onward; Carrizosa, Gomez-Vargas & Piccialli, Omega 2026, DOI 10.1016/j.omega.2026.103675, abstract only). Weights are unique only when the observed point lies in the relative interior of a facet (Chan et al. 2014, Cor. 2).
- **Inverse goal programming** in name: one paper (Saif & Weber, "Inverse Linear Goal Programming Problem", Thamar Univ. J. Nat. Appl. Sci., DOI 10.59167/tujnas.v3i3.1284; Crossref date 2023) adjusts deviation weights for a single noiseless solution with targets fixed. No joint inference of weights and aspiration levels from noisy data was found.
- **Economics already infers priorities from allocations.** Inverse-optimum welfare weights from tax schedules (Bourguignon & Spadaro 2012; Hendren 2020, NBER w20351; Lockwood & Weinzierl, NBER w21927; Saez & Stantcheva, NBER w18835). Behrman & Craig (AER 1987) estimate inequality aversion of a city from police allocation using an outcome production function and IV, the direct precedent. Authors' own warnings: weights depend on assumed behavioural elasticities, are not structural, and are confounded with political-economy distortions. No school-finance paper read inverts state-aid decisions into weights; school-finance work measures progressivity (Baker et al.; Chingos & Blagg 2017) or estimates causal effects.
- **Closest applied precedent:** Karami-Fard 2026, "Need, Alignment, or Commerce? Recovering the Revealed Priorities of Foreign Aid Donors through Inverse Optimization", SSRN, DOI 10.2139/ssrn.7302189 (title only; must be read).

## What an inverse goal-programming approach could add (candidate contributions, not yet established)
1. Joint inference of goal weights and aspiration levels (targets), which a smooth welfare function cannot represent. Inferred so far only by reasoning, to be proved: with under-achievement deviations only, targets drop out; targets become informative through kinks (goals met or exceeded); under Chebyshev GP, weights and targets are confounded through w_i (b_i - f_i(x)); variation in the budget envelope across years can restore identification.
2. Set-valued output: the cone of weights and targets consistent with an allocation, rather than a point estimate.
3. Several outcomes plus legal and fiscal constraints, with production-side effects taken from credible causal estimates and their error propagated.
4. Application: revealed priorities of US states in allocating state aid across districts, 2010-2019 (state aid is the controllable layer; local revenue offsets it, Chingos & Blagg), compared with formula weights and with the Great Recession period.

## Main risks
- Economics may regard the idea as known (inverse optimum, Behrman & Craig); the OR contribution must be the GP structure, identification theory and set-valued inference.
- Identification may fail in the data (vertex optima, few kinks).
- The outcome production function is not identified from the panel; credible effects must come from quasi-experimental literature (notes 04).
- Political economy confounds preferences.

## To read next (paywalled or blocked)
Karami-Fard 2026 (SSRN 10.2139/ssrn.7302189); Carrizosa et al. 2026 (Omega 10.1016/j.omega.2026.103675); Chan et al. 2014 (10.1287/opre.2014.1267); Roland et al. 2016 (C&OR 10.1016/j.cor.2015.07.006); Ahuja & Orlin 2001 (10.1287/opre.49.5.771.10607).
