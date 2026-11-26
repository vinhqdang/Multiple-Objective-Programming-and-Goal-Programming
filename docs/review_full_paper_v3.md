# Referee report (third round): "Revealed Aspiration Levels: Inverse Interval Goal Programming for Recovering the Targets Behind Public Decisions"

Annals of Operations Research, special issue "Multiple Objective Programming and Goal Programming: Artificial Intelligence for Decision Making in Economic and Social Sciences".

Material read: paper2/main.tex (line numbers below refer to it; 29 pages), the tab_*.tex files, the compiled main.pdf and springer/main_sn.pdf (34 pages), cover_letter.md, refs.bib, results/*.csv, data/aid, and the previous reports (docs/review_full_paper.md, docs/review_full_paper_v2.md). I formed my own judgement from the manuscript first and then checked the v2 items. Numbers were recomputed with scratch scripts outside the repository. Where I ran the repository's exact one-goal solver (code/exact_k1.py), I did so read-only. On Swedish aid it reproduced the reported loss 0.0667, and a 200,000-draw random search did not beat it. The shares of donor-years above and below the band (22% and 44%) also reproduce.

---

## 1. Summary and recommendation

**What the paper does.** It treats the recovery of aspiration bands, transmission and step sizes of an interval goal program from sequential decisions. The forward model has asymmetric deviation weights and a linear or quadratic adjustment cost.

- Theory: breakpoint optimality; effective weights; edge revelation; non-identification of weights under linear cost; a rank condition under quadratic cost; a closed-form clip policy for one goal; an exact O(T^4) estimator for one goal and fixed alpha; a Lipschitz certificate over alpha; a consistency theorem (point identification for K=1 only); a pseudo-true-parameter result.
- For K>=2: an MILP that does not close, and a multistart heuristic.
- Applications: 14 central banks (K=2), 23 aid donors, NATO defence spending, and corporate leverage (all K=1).
- Adequacy study: placebos, paired tests, out-of-sample comparisons.

**Overall assessment.** The second revision is a real improvement. Almost every v2 item has been dealt with, usually honestly. Examples:

- degenerate bootstrap replicates are now kept at plus or minus infinity;
- the PA test has a size study, and a max-p BH rule combines the two tests;
- all donors with a documented goal are scored;
- a GNI-drift sensitivity analysis and a mean-level column were added;
- defence now has permutation and PA tests plus a leave-one-out check;
- there is a Monte Carlo with a controlled state and discrete decisions;
- level-form Taylor benchmarks and an official-band comparison were added;
- paired tests were added;
- the title and the abstract were toned down.

The core K=1 contribution (closed-form policy, exact estimator, consistency) is correct and publishable in ANOR. The empirical sections are now largely candid about weak validation.

What remains falls into four groups.

1. **Surviving K>=2 gap.** There is still no identification theory and no reliable optimiser for the multiple-objective part, which is what the special issue is about.
2. **Claims that the evidence does not support or that contradict the paper's own tables.** The main ones:
   - the statement that the GNI-adjusted estimates move donors "towards their national goals" (l.285);
   - the defence out-of-sample statement (l.298);
   - the abstract's "near their national 1% goals" for Sweden;
   - the abstract's "one to three donors", which hides an unusual FDR threshold.
3. **Inference for the central banks, still not valid.** The bootstrap uses a different optimiser from the point estimates, runs B=200 with a percentile interval for a boundary-affected estimator, and its coverage check uses a design with no degenerate replicates. The only positive central-bank evidence (Turkey) is a boundary fit (alpha at its lower bound 0.05, band width zero).
4. **Proof and presentation defects:**
   - the domain reduction in the proof of Theorem 2 is incorrect (the theorem itself is probably true);
   - the Springer file still carries the old title with "Priorities";
   - cross-reference and ordering errors;
   - several 300-word paragraphs;
   - a stale "Draft, date" line.

**Recommendation: Major revision, but a short, targeted one.** I would not need a further full round if items N1 to N6 below are handled. The contribution is narrower than the special-issue framing suggests ("multiple objective", "AI"): the proved, exact part is one-goal, and the K=2 application is the weakest result. The paper is a reasonable fit as a goal-programming methodology paper with public-sector illustrations, and a weak fit as multi-objective or AI work.

---

## 2. Status of v2 items

### Major items

| Item | Status | Evidence |
|---|---|---|
| M1. K>=2 content under-developed | **Partly addressed** | The abstract now says the rank condition holds "given ... the other parameters" (l.22). The title no longer says "Priorities" in main.tex (but see N5: the Springer file still does). The intro (l.32) says the guarantees are strongest for one goal. The cover letter no longer calls the MILP an "exact estimator". An MILP run on Hungary (T=33, 2 h) was added: gap 26.5%, so not certified (l.143; milp_check_hu.csv: incumbent 0.2546, bound 0.1871, gap 0.265). Still missing: no identification result for K>=2 (the Remark at l.110 says "remains open"); no K=2 application that interprets weights; the cover letter's "solves small instances" is not supported by any reported solved instance (see N3). |
| M2. Central-bank bootstrap not valid | **Partly addressed** | (b), (c): degenerate replicates are kept and placed at plus or minus infinity, quantiles are over all replicates (UK, TR, IN, NO now unbounded below), and "twelve of fourteen" is withdrawn (l.261). (d): B raised from 100 to 200, still below the requested 500. (e): a coverage check was added (k2_boot_coverage.csv: 20 of 20 covered, median width 0.459). Still open: (a) replicates still use the lighter optimiser, and the median is far from the point estimate for several banks (IL 1.45 vs 3.49; SE 0.88 vs 1.36; HU 4.10 vs 4.97; NZ 2.77 vs 1.66, with NZ's 5% limit equal to the point estimate); the coverage design has 0 degenerate replicates in all 20 instances, so it says nothing about the bank-like regime (see N2). |
| M3. CB benchmark and second ground truth | **Largely addressed** | Level-form Taylor/partial-adjustment benchmarks (NLS defined for 11 banks, LAD for 6), a completion rule that covers all 14 banks (1.26, 1.10, 1.21 pp), and a band comparison with official ranges (12 banks; 6 within a factor of two; rank correlation 0.02) were added and match cb_level_taylor.csv. Remaining: "right magnitude" is still in the abstract (l.22), at l.253 and l.327, although a constant 2.5% does as well (0.61 vs 0.64). The claim "informative where inflation and target diverge" rests on one boundary fit (Turkey; see N2). |
| M4. Aid inference chain | **Largely addressed, with new defects** | (a) A PA-test size study was added (60 series, B=199; 0-7% at 5%), but the aid test uses B=999 while the size study uses B=199, and the study covers four null behaviours with no regime-switching or trend null. (b) The abstract now says "nonlinear state dependence inconsistent with partial adjustment". (c) BH on max(p_state, p_PA) gives a single multiplicity rule. (d) Fixed (l.271), but the conclusion (l.327) still says "actors that share a commitment". (e) All 15 donors with a documented goal are scored, but the abstract still says "near" for Sweden although the goal is outside both band and set (Table 9). (f) The mean-level column was added (Table 10). (g) Sets are truncated at 0; step sizes are discussed (l.281; I verified: Sweden's largest cut above the band 0.46 and next 0.23, Portugal 0.42 and next 0.09, from 12 and 6 observations above the band respectively). (h) A GNI-adjusted sensitivity was added, but it is misdescribed (N1). (i) Autocorrelation is reported (median -0.179; > 0.3 only for FRA, TUR); no block permutation. |
| M5. Defence | **Largely addressed** | (a) Permutation and PA tests were run (defence_tests.csv: p between 0.080 and 0.818, none rejects). The paper concludes that defence evidence is descriptive. (b) Both uncertainty measures are now in the abstract and discussion. (c) The "lower limit = point estimate" is acknowledged (l.296). (d) The invasion confound is acknowledged, but the share of observations below the band in 2022-25 (92.7%) is not discussed. (e) Not addressed: Table 11 still prints step-down 0.20 and 0.21, although l.296 calls the upper edge and steps down "not interpretable". (f) The "superseded estimator" reference was removed. Leave-one-out added (defence_loo.csv: 1.73 without Romania to 2.00 for 2015-21; 3.80 without the US in 2022-25). New error: l.298 vs Table 14 (N1). |
| M6. Theory precision | **Addressed, but a new proof gap** | (a) The Remark (l.110) now describes the ramp. (b) The half-line statement is in the proof of Proposition 4. (c) The O(T^3 log T) refinement now has a sketch (l.193) and the exponents are consistent (T^2.3 to T^2.9; recomputed slopes 2.32, 2.41, 2.90). (d) A controlled-state and discretised Monte Carlo was added (l.228; consistency_mc_closed.csv reproduces: tau mean abs error 0.015/0.032/0.022 at T=200; within 0.1 in 89/81/73% at T=50; omega+ error about 0.10 under rounding). (e) The support condition is linked to the applications (l.323). (f) The Proposition 5 qualifier was added. New: the restriction e in [min z, max z] in the proof of Theorem 2 is not without loss (N6). |
| M7. Adequacy diagnostics | **Partly addressed** | (a) A noise x T grid was added (placebo_grid.csv), but only for the "coin" and goal-program behaviours, and for the coin at (noise 0.03, T=60) it disagrees with Table 12 (see Number checks and N4). (b) Sign and Wilcoxon tests were added (paired_tests.csv; reproduce). (c) The five-donor comparison is now labelled an illustration; the phrase "compares favourably" is gone. |
| M8. Fit and structure | **Partly addressed** | The firms paragraph is shorter, and Appendix B was added. No online supplement. The intro states that guarantees are one-goal. The "AI" dimension is still thin (see Fit, section 6). |

### Minor items (v2 numbering)

| # | Status | Evidence |
|---|---|---|
| 1 | Addressed | Table 15 header now ends `\\\midrule`; the compiled PDF (p.28) prints correctly. |
| 2 | Addressed | MILP uses \hat D_t for fitted and D_t for observed (l.117). |
| 3 | Partly | PA parameters are now mu, kappa, and the Taylor ones kappa_pi, kappa_y. Remaining clashes: L is the Lipschitz constant (Theorem 3), the loss \hat L in the permutation statistic (l.275) and L_PA/L_GP (l.277); pi_{kt} (multipliers, Proposition 5) vs pi_t (inflation, l.245); c is the transformed aspiration level and the Taylor intercept (l.253); epsilon is both noise and the MILP margin; B is the number of draws and, implicitly, the band parameter b. |
| 4 | Addressed | l.247 now states 0.72-1.55 vs 0.47, 1.83 vs 0.22, and the sign-only 0.46 vs 0.48. |
| 5 | Addressed | The Remark cites the rate-limited placebo. |
| 6 | Addressed | l.275 now says 12% and gives the MC standard error. |
| 7 | Addressed | The 2018 break handling is stated once in Section 4.3. |
| 8 | Addressed in substance | Goals moved to Table 9; Table 10 now carries tau-minus-mean. Table 10 still has 11 columns. |
| 9 | Addressed | Table 2 caption mentions the 3,000-per-industry cap. |
| 10 | Addressed | India's window is 2016Q3-2024Q4 (l.245). Indonesia is explained in the text only (not in confirmatory_windows.csv, which has eight rows, not nine; see Number checks). |
| 11 | Addressed | l.294 explains Finland/Sweden. |
| 12 | Addressed | Fig. 2 caption gives degenerate counts out of 200. |
| 13 | Addressed | l.142 says the table reports losses only. |
| 14 | Addressed | The discussion no longer groups Japan and the US with the passing donors. |
| 15 | Mostly addressed | The cover letter is toned down. Remaining: "solves small instances", "Eurostat" (not mentioned in main.tex), and "code that reproduces every table" (Table 3 has no results file). |
| 16 | Mostly addressed | Afriat, Varian, Ng-Russell, Ziebart, Taylor, CGG, Svensson, Simon, Charnes-Cooper, Olson-Zeckhauser, Sandler-Hartley, Clemens-Moss added. Still missing: Samuelson; the interval/aspiration-level goal programming literature (e.g. Ignizio, Jones-Tamiz practical GP); Dunne-Smith. |
| 17 | Not addressed | Nine paragraphs exceed 250 words (l.180, 245, 253, 261, 277, 313, 317; the abstract and l.45 as well). |
| 18 | Partly | The caption now cites "supplementary material", but results/*.csv paths still appear in running text (l.143, 253, 268, 277, 279, 285, 317). |
| 19 | Addressed | "serve as a check". |

---

## 3. New major issues

### N1. Two statements contradict the paper's own tables

- **l.285 (GNI-adjusted estimates).** The text says the adjustment "moves the high-aid donors towards their national goals". Using Table 9:
  - Sweden moves towards its goal (distance to 1.0 falls from 0.10 to 0.02).
  - Norway moves away (0.02 to 0.05); the goal 1.0 is outside the adjusted set (1.02, 1.25).
  - Luxembourg is at 1.00 and moves to 1.01.
  - Denmark moves strongly away from its 0.8 goal (0.06 to 0.23; set 0.98-1.13).
  - The Netherlands also moves away (0.15 to 0.17).
  - Counting goals inside the 2% set: six under the main measure (NOR, LUX, DNK, NLD, GBR, DEU) against four under the adjusted measure (SWE, GBR, DEU, FRA; aid_goal_comparison.csv `in_set_gni`).

  So the headline "near the national goals" depends on which measure is used, and the paper should say so. The abstract's claim for Sweden and Norway is accurate only for Norway on the main measure and for Sweden on the adjusted one.
- **l.298 (defence out-of-sample).** The text says "partial adjustment, holding and the median change all predict at least as well as the goal program (Table 14)". In Table 14 the goal program (0.183) beats holding (0.191), and in model_comparison.csv the 2022-25 goal program (0.228) beats both partial adjustment (0.236) and holding (0.262). Only the median change (0.170 on average) beats it on average. The statement should be restated per period.

### N2. Central-bank inference remains weak and the headline success case is degenerate

- **Turkey.** The only case supporting "informative where inflation and target diverge strongly" is Turkey. Its fit sits on a boundary (cb_light_point.csv: alpha = 0.05, b = 0). 62 of 200 bootstrap replicates are degenerate. The interval is unbounded below. The two-quarter horizon gives the same number, the six-quarter horizon is degenerate. The benchmark comparison with average inflation is carried by this one bank (0.64 vs 0.85 overall; 0.61 vs 0.47 without Turkey).
- **Bootstrap.** The replicates use a different (lighter) optimiser from the point estimate. Medians are systematically displaced from the point estimates (IL, SE, HU, NZ, IN), so a percentile interval is not centred on the reported number. For NZ the lower limit equals the point estimate (1.66). B=200 with 8-quarter blocks on windows of 32-104 quarters is small.
- **Coverage check.** k2_boot_coverage.csv has 0 degenerate replicates in all 20 instances, so it validates the bootstrap only in the well-identified case. The bank series (T=32-104, bands up to 5 pp wide, up to 37% degenerate replicates) are outside it. The claim "if anything conservative" (l.261) is not supported for banks.
- **Reporting.** The main tables report single-seed fits that are not the best of five for Hungary (3.90 vs 4.97, 2% lower loss) and Australia (2.76 vs 2.63). Best-of-five should be the primary estimate. The paper also notes that six banks have seed-dependent targets (cb_multiseed.csv). Taken with the horizon sensitivity (SE: 1.36, 0.98, 0.10; CL: 3.96, 3.91, 1.38), the central-bank estimates are not reliable enough for the label "check".
- **Requested.** (i) Use the same search for the point estimate and the replicates, or include the full search for a subset of replicates. (ii) Report the degenerate share as part of the result (e.g. "tau unbounded with probability 0.37 for GB"). (iii) Raise B (>=500) and run the coverage check on a design with degenerate replicates (T=33, wide band, low alpha). (iv) Present Turkey as a boundary fit.

### N3. The multiple-objective part has no certified result, and the K=1 certificate is never used

- The MILP is not shown to solve any instance to optimality (Table 3: gap not closed at T=80; Hungary T=33 after two hours: 26.5%). Yet l.117 says it is "solved to optimality only for small instances" and the cover letter says it "solves small instances". Either report a case that closes (e.g. T=15-20) or remove the claim.
- The multistart search misses the true-parameter loss in 8/20 and 5/20 instances (k2_recovery.csv: reproduces; max 1.31 and 1.20).
- Theorem 3 (certified search over alpha) and the alpha-identification part of Theorem 4 are used in no application (aid, defence and firms fix alpha = 1; the Monte Carlo fixes alpha = 1; central banks are K=2). The K=1 results that matter empirically are Theorem 1 and Theorem 2 with alpha = 1.
- A K=2 identification result (e.g. disjoint state supports so that the problem separates) is still missing.

### N4. Calibration of the diagnostics and the uncertainty sets

- **Placebo numbers disagree across tables.** The same design (coin flip, noise 0.03, T=60, 100 series) gives median set width 3.54, 17% out-of-sample wins over holding, 10% of sets narrower than one unit, and mean gain 0.037 in misspec_placebo.csv (Table 12), but 2.44, 25%, 11% and 0.047 in placebo_grid.csv. A factor of 1.4 in the median width is large for 100 series, and it indicates substantial run-to-run variation or different seeds, although l.313 says "seeds are fixed". Report one set of numbers with Monte Carlo standard errors.
- **The 2% profile-loss sets are not calibrated.** The tolerance of 2% (and 5%) is arbitrary and is used as an uncertainty measure for aid and defence. It disagrees with the bootstrap in defence (overlapping sets vs disjoint intervals). Since the exact estimator is fast (0.1-0.5 s at T=50-100), a bootstrap or subsampling calibration of the sets is cheap, and it was requested in v2.
- **FDR threshold hidden in the abstract.** "One to three donors" corresponds to a 10% FDR (3 donors with independent residuals, 1 with block residuals). At 5% it is one donor (Sweden, adjusted 0.023) for independent residuals and none for block residuals (Sweden 0.069). The abstract should state the level. The PA test has 12-16% power against a goal program with small steps (l.277), so non-rejections for the other 20 donors are uninformative, and the step estimates of two of the three combined-test discoveries rest on very few observations above the band (Sweden 12, Portugal 6).
- **State-dependence test.** Because x_{t+1} = x_t + Delta_t for aid and defence, the permutation null rebuilds a random-walk level. Any mean-reverting or regime-shifting level path will reject (the paper's own regime-switching size of 8-13% is a weak check). The test is a mean-reversion test, not a goal-seeking test, as l.275 admits. Combined with the specification search (six central-bank specifications, a post-hoc goal comparison, a combined rule chosen after the single tests) the multiplicity control covers only part of the forking paths.

### N5. Submission files are inconsistent

- springer/main_sn.tex line 10 and main_sn.pdf p.1 carry the title "... Recovering the Targets **and Priorities** Behind Public Decisions". main.tex and the cover letter say "Targets Behind Public Decisions". This undoes the v2 M1 fix in the file that would be submitted. The keywords also differ (Springer file: "Public budgets" only; main.tex adds "central banks").
- main.tex prints "Draft, \today" (l.13) and has no declarations; the Springer file has them.
- The cover letter lists "Eurostat" among the data sources; main.tex does not mention it (the Springer declarations do).

### N6. Proof of Theorem 2: the box restriction on the band edges is not without loss

At l.180 the proof says "we may take e^+- in [min z_t, max z_t]". This is correct for e^+ > max z (set e^+ = max z) and for e^- < min z (set e^- = min z), but it does not follow for e^+ < min z or e^- > max z. Counter-example: z = (5, 6, 7), D = (4.7, 5.7, 6.7). The parameters e^+ = e^- = 0.3 with omega^+ >= 6.7 fit exactly (all points on the upper ramp). With e^+ >= e^- >= min z = 5 the best loss is positive (the residual equals e^+ - 0.3 >= 4.7 at every point). Raising e^- to min z also violates e^- <= e^+. The statement of the theorem is probably still true, because the candidate set E contains z_t - D_s and the argument can be repaired by bounding e^+ below by min z - bar-omega^+ (below that every point is saturated and the objective is constant in e^+), and the code enumerates all of E. But the proof as written is wrong, and the domain in Theorem 3 (|e^+-| <= alpha_max max|x_t|) needs the same repair, since z_t - D_s can lie below -alpha_max max|x_t|.

---

## 4. Minor issues

1. **l.13** `\date{Draft, \today}` prints "Draft, November 25, 2026" on the title page; remove for submission.
2. **l.261 and l.268, order of paragraphs.** "Uncertainty" (l.261) says the light-search point estimate "differs from the full one for Israel, India and Norway (above)", but the seed paragraph that explains this comes after it (l.268). "Search seeds" says "the bootstrap below", but the bootstrap is above. Swap "above" and "below", or reorder.
3. **l.253 and Table 7, "right magnitude".** Replace it in the abstract (l.22), l.253, l.322 and l.327 by the quantitative statement "within about 0.6 pp on average, as a constant 2.5% is".
4. **l.327 (conclusion)** "differ across actors that share a commitment": l.271 and Table 9 show that donors do not share one commitment (US, national goals). Reword.
5. **l.281.** "Portugal's [other cuts] 0.23 pp or less" is true but loose: Portugal's other cuts are 0.09 or less (Sweden's are 0.23 or less). State both.
6. **Table 11 (defence)** prints step-down 0.20 and 0.21 although l.296 says upper edges and steps down "are not interpretable" (2.3% and 2.4% of observations; 5 and 3 observations). Use a dash or flag them.
7. **l.294.** Finland and Sweden are pooled for all years although they were not NATO allies before 2023/24; pre-accession spending did not respond to the NATO guideline, which affects the pre-2022 band. A robustness run without them would settle this.
8. **l.251.** "Of nine candidate banks, five qualified": confirmatory_windows.csv and confirmatory_cb.csv list eight banks (IL, NZ, CZ, CO, HU, TR, KR, IS); Indonesia appears only in the text.
9. **Section 4.1.** The Taylor-rule benchmark remains partly undefined (the "taylor_or_mean" completion mixes two different estimators). State how many of the 14 banks use the Taylor target and how many fall back to the mean in each column of Table 7.
10. **Fig. 2** (fig_cb.pdf): labels at the 2.0 and 2.5 stated targets overlap (GB, CA, SE, NZ, AU, NO, PL); the unbounded arrows and degenerate counts are small and unreadable at print size. Consider a dot plot with one row per bank and a separate degenerate column.
11. **Table 10** has 11 columns with two-line cells and two lists of p-values (iid; block). Consider moving the PA columns to an online table and keeping tau, band, set, steps, mean-minus-tau, combined q.
12. **Table 3** (synthetic evidence) has no results file in results/ (I could not trace 0.205/0.089/0.189/0.101/0.093/0.052/0.111). The cover letter promises code that reproduces every table; add the file or remove the claim.
13. **Algorithm 1, line 3-4.** The candidate sets are written inside `min over omega in (...) cap [0, bar omega] cup {0}` where the cup/cap precedence is ambiguous; add parentheses.
14. **l.117.** Give a sensitivity of the MILP results to epsilon (0.05) and M (30), requested in the first-round review (minor 4) and still absent.
15. **l.143.** The MILP incumbent on Hungary (0.2546, tau 3.91) equals the best of five seeds, not the reported single-seed fit (4.97). Say that the reported Hungary estimate is not the optimum found.
16. **l.193.** The O(T^3 log T) sketch should say how many candidate e values are enumerated (O(T^2)) and that the second sweep also needs the lower part; a two-line proof would do.
17. **Remark (l.110) and Proposition 5.** The statement "with two goals outside their bands only the sum of their weights is revealed" is correct but is the only comment on K>=2 weights. Add the corresponding rank statement for the central-bank design (is the incidence matrix of the two-goal central-bank sample full rank?).
18. **l.45.** The "Revealed preferences" paragraph is 254 words with 30 citations; split it or move the central-bank list to the benchmarks section.
19. **Bibliography.** `rao1962` is in refs.bib and never cited (the uniform-convergence citation is Newey-McFadden only). `karamifard2026` has a single-token author "Karami-Fard" with no initial, and `saif2023` carries a note about the journal header date (2010) that should be resolved or removed. `ahmadi2026` and `karamifard2026` are preprints (arXiv 2603.17033; SSRN); check status before submission. Ireland (2007) lacks a DOI.
20. **Notation** (continuation of v2 minor 3): c (transformed level vs Taylor intercept); pi_{kt} vs pi_t; L (Lipschitz, loss, loss ratio); epsilon (noise vs margin); E (expectation vs candidate set \mathcal E); consider renaming.
21. **l.263 / Table 8 caption.** State the number of replicates (200) in the figure caption of Fig. 2 as well as in Table 8, and say that the bootstrap in the main text is over bank series of different lengths.
22. **l.317.** "always holding has the lowest average error for aid and central banks" is a tie with the median change for banks (0.380 each; the median change is zero for most banks). Say so.
23. **Abstract** (253 words) lists 12 distinct findings. Shorten to the three or four that carry the paper (K=1 theory, the aid and defence findings with their caveats, the central-bank check).
24. **l.271.** The 0.7% target "adopted by the UN General Assembly in 1970 and accepted by most donors" is cited to Clemens-Moss; the national goals in Table 9 (years 1999-2015) are said to be verified in the "supplementary material", which was not available to me. Include the source table in the submission.
25. **Appendix A.** The "specifications tried" table is helpful; add the number of specifications that were run and discarded without being listed (if any), and state whether the order shown is chronological.

---

## 5. Number checks

"Yes" means the text value equals the file value after rounding. "n/a" means no file in results/ or no way to recompute it.

| Location | Claim | File value | Match |
|---|---|---|---|
| l.253, Table 7 | MAE implied 0.64, mean inflation 0.85 (14 banks) | cb_benchmarks.csv: 0.644 / 0.846 | yes |
| l.253 | without Turkey 0.61 vs 0.47; constant 2.5%: 0.61 (0.46 w/o TR); median of others 0.68 (0.54) | 0.606 / 0.473; 0.607 / 0.462; 0.679 / 0.538 | yes |
| Table 7 | exploratory 0.45/0.47/0.44/0.44; confirmatory 0.99/1.52/0.90/1.10; confirmatory w/o TR 0.96/0.47/0.50/0.75 | 0.451/0.472/0.444/0.444; 0.992/1.52/0.90/1.10; 0.955/0.474/0.50/0.75 | yes |
| Table 7, l.253 | Taylor target defined for 7 banks, 1.29 vs 0.81 (confirm. 1.65/0.96, n=4; expl. 0.81/0.62, n=3) | 1.286 / 0.813; 1.646 / 0.955; 0.806 / 0.623 | yes |
| l.253 | Taylor-or-mean 1.21 (0.86 w/o TR); NLS level rule defined for 11, 1.26 (0.92); LAD defined for 6, 1.10 (0.75) | 1.206 / 0.859; 11, 1.261 / 0.919; 6, 1.099 / 0.745 | yes |
| l.253 | 12 banks with official range; 6 within factor 2; rank correlation 0.02 | 12; 6; Spearman 0.023 | yes |
| l.251 | NZ passes the 0.5 pp filter by 0.04 pp; sign test 0.125 | |2.543-2.0| = 0.543; 1/8 | yes |
| l.251 | Of nine candidate banks, five qualified | confirmatory_windows.csv / confirmatory_cb.csv list 8 banks (no Indonesia) | no (8 vs 9) |
| Table 8 / l.261 | degenerate replicates GB 74, TR 62, IN 49, NO 17, PL 16, IL 11; widths AU 0.96, MX 0.74; CA 1.4, CO 2.2, HU 2.1, NZ 1.8, SE 1.8; CL 4.5, IL 5.4 | bootstrap_cb_100_summary.csv: 74, 62, 49, 17, 16, 11; 0.956, 0.744; 1.41, 2.15, 2.11, 1.78, 1.85; 4.52, 5.40 | yes |
| l.261 | MX (3.15-3.90) and HU (3.18-5.30) exclude the stated target; PL reaches -15 | 3.153-3.897; 3.181-5.296; -15.20 | yes |
| l.261 | 20 K=2 instances, all 90% intervals cover, median width 0.46 | k2_boot_coverage.csv: 20/20, 0.459; 0 degenerate in every instance | yes (but see N2) |
| l.268 | best of five gives the reported target for twelve banks; HU 3.90 vs 4.97 (2% lower loss); AU 2.76 vs 2.63; MAE 0.58 (0.53 w/o TR) | cb_multiseed.csv: 0.577 / 0.534; HU 3.901, 0.2546; AU 2.756 | yes |
| l.268 | light search gives the same target within 0.03 for eleven banks; IL 3.37; IN 2.38; NO 2.48 | cb_light_point.csv: 11 banks within 0.026; 3.369; 2.375; 2.475 | yes |
| l.266, Table 16 | horizon 2 / 6 quarters: 3 / 2 degenerate; MAE 0.80 / 0.93 vs 1.02 / 0.42; 4 of 7 and 2 of 4; end 2015: 0.75 vs 0.48, 4 of 5 | sensitivity_cb.csv recomputed: 3 / 2; 0.80 / 0.93 vs 1.02 / 0.42; 4 of 7 and 2 of 4; 0.75 vs 0.48, 4 of 5 | yes |
| l.143 | K=2 recovery: median loss 5% below true; stops above in 8/20 and 5/20; at most 31% above | k2_recovery.csv: 0.946 / 0.953; 8 and 5; max 1.315 | yes |
| l.143 | median errors tau1 0.02/0.09, b1 0.04/0.11, alpha1 0.03/0.14, tau2 0.17/0.56 | 0.021/0.088, 0.037/0.111, 0.031/0.141, 0.175/0.557 | yes |
| l.143 | MILP on Hungary: loss 0.2546, bound 0.187, gap 26.5% | milp_check_hu.csv: 0.2546, 0.1871, 0.265 | yes |
| Table 4 / l.193 | exact 0.02/0.10/0.53/3.97 s (max 0.03/0.14/0.64/4.55); heuristic 4.1/4.1/5.3 s; 10/10, 9/10, 10/10; one case 0.06% above | comp_study.csv: 0.020/0.100/0.532/3.974; max 0.028/0.143/0.640/4.549; 4.07/4.13/5.35; 29 of 30 at optimum; 0.058% | yes |
| l.193 | exponent T^2.3 to T^2.9; heuristic 10-200 times slower | slopes 2.32, 2.41, 2.90; ratios 10 and 203 | yes |
| l.190 | multistart matched the exact loss (within 0.1%) for 10 donors, up to 6% above for 13; NLD 0.55 vs 0.73; UK 0.49 vs 0.27 | aid_heuristic_vs_exact.csv: 10 within 0.1% (max other 5.95%); NLD tau_heur 0.73, tau_exact 0.55; GBR 0.485 / 0.27 | yes |
| l.221 | MC errors T=50/100/200: 0.040/0.039/0.020/0.024; 0.023/0.022/0.013/0.014; 0.021/0.017/0.013/0.009 | consistency_mc.csv: 0.040/0.038/0.020/0.023; 0.023/0.022/0.013/0.014; 0.021/0.017/0.012/0.009 | yes (rounding) |
| l.228 | controlled / discrete / both: tau error at T=200 0.015, 0.032, 0.022; within 0.1 at T=50 89/81/73%; omega+ error about 0.10 | consistency_mc_closed.csv: 0.015, 0.032, 0.022; 0.89, 0.81, 0.73; 0.106 / 0.101 | yes |
| l.275 | state-dependence test size 2% at 5%, 7% at 10% (200 series) | permutation_test.csv: 0.02 / 0.07 | yes |
| l.275 | AR(1) decisions 9% (12%); regime switching 8% (13%) | permutation_extend.csv: 0.09 / 0.12; 0.08 / 0.13 | yes |
| l.275 | 9% when levels are kept at observed values | no file | n/a |
| l.275 | seven donors at 10% (SWE, BEL, PRT, FRA, NOR, TUR, NZL), four at 5% | q_state: 0.023, 0.038, 0.038, 0.040, 0.060, 0.084, 0.085 | yes |
| l.277 | PA size 0-7% at 5%, 0-17% at 10%; power 16%/12% (goal program), 59%/62% (quadratic program) | pa_null_extend.csv: 0.00-0.067, 0.00-0.167; 0.16/0.12; 0.59/0.62 | yes |
| l.277 | PA rejected at 10% for SWE, NOR, PRT, TUR, JPN, LUX (iid), same except LUX (block) | q_pa_iid: 0.0115, 0.0115, 0.0153, 0.0173, 0.0537, 0.0537; q_pa_block LUX 0.165 | yes |
| l.279 | combined q (iid) SWE 0.02, PRT 0.06, NOR 0.10; block SWE 0.07, others 0.13 | aid_combined_tests.csv: 0.023, 0.0575, 0.0997; 0.069; 0.1265 | yes |
| l.279 | acf1 median -0.18; above 0.3 only for FRA, TUR | aid_autocorr.csv: -0.179; FRA 0.319, TUR 0.481 (FIN 0.236) | yes |
| l.281, Table 10 | SWE 0.90 (mean 0.77), NOR 0.98 (0.80), PRT 0.27 (0.21), JPN 0.28 (0.25), USA 0.21 (0.25) | 0.90 (0.766), 0.98 (0.797), 0.265 (0.212), 0.285 (0.254), 0.215 (0.246) | yes |
| l.281 | Sweden's largest cut above band 0.46, others 0.23 or less; Portugal 0.42 | recomputed from data: 0.46, 0.23; 0.42, 0.09 | yes |
| l.283 | goal in band for 4 of 15, in set for 6; eight of nine EU donors below 0.7 (0.14 Italy to 0.59 Finland) | aid_goal_comparison.csv: 4, 6; | yes |
| l.285 | GNI adjustment moves the target by a median of 0.05 across 22 donors, up to 0.43 (UK 0.27 to 0.70); SWE 0.98 (0.96-1.03), NOR 1.05, LUX 1.01, DNK 1.03 | aid_gni_drift.csv: 0.046, 22, 0.43 (GBR); 0.984, 1.053, 1.015, 1.03 | yes (numbers) |
| l.285 | the adjustment "moves the high-aid donors towards their national goals" | Distance to goal: SWE 0.10 to 0.02; NOR 0.02 to 0.05; LUX 0.00 to 0.01; DNK 0.06 to 0.23; NLD 0.15 to 0.17 | no (only Sweden moves towards) |
| l.323 | 22% of donor-years above and 44% below the aid band | recomputed from data/aid and aid_exact.csv: 0.224, 0.444 (1313 donor-years) | yes |
| l.296, Table 11 | 2015-21: n 217, band [1.99, 3.48], 85% below band, step up 0.03, bootstrap 1.37-2.10, set 1.12-3.61; 2022-25: band [3.21, 3.66], up 0.12 (0.11-0.20), bootstrap 3.21-3.95, set 2.75-3.87 | defence_exact.csv, defence_uncertainty.csv | yes |
| l.296 | dropping one ally: 1.73 (Romania) to 2.00; US removal gives 3.80 | defence_loo.csv: 1.73 (Romania) to 2.000 (France, Norway); 3.80 (US) | yes |
| l.298 | defence tests: p between 0.08 and 0.82, B = 999 / 499 | defence_tests.csv: 0.080-0.818 | yes |
| l.298 / Table 14 | "partial adjustment, holding and the median change all predict at least as well as the goal program" | Table 14: GP 0.183 < Hold 0.191; per period 2022-25 GP 0.228 < PA 0.236, < Hold 0.262 | no |
| Table 14 | aid 23 units: 0.056/0.052/0.049/0.050; 5/23 best; 12/23 worse than hold; banks 0.481/0.413/0.380/0.380; 1/14; 11/14; defence 0.183/0.176/0.191/0.170 | model_comparison.csv recomputed: identical; defence mean 0.183, 0.176, 0.191, 0.170 | yes |
| l.317 | paired tests: aid smallest p = 0.06; banks vs hold sign p = 0.006, Wilcoxon 0.003; vs Taylor 0.34 | paired_tests.csv: 0.0619; 0.00635, 0.00342; 0.3396 | yes |
| l.317 | PA target undefined for five donors (CHE, DEU, FIN, GBR, KOR); LUX 1.87, SWE 0.75, DNK 1.41, NOR 1.01, NLD 0.75 | model_comparison.csv: 5 NaN; 1.87, 0.746, 1.41, 1.01, 0.746 | yes |
| Table 12 | coin: tau 2.05, IQR 0.83, gain 3%, set width 3.54, GP beats hold 17%, GP beats PA 25%; GP: 2.00/0.01/78%/0.02/100/100; PA: 1.99/0.10/66%/0.06/100/0; QP: 1.99/0.07/71%/0.06/100/5 | misspec_placebo.csv: 2.049, 0.83, median gain 0.028 (mean 0.037), 3.54, 0.17, 0.25; others identical | yes |
| l.313 | coin at noise 0.03, T=60 (same design as Table 12): 10% of sets narrower than one unit | placebo_grid.csv (coin, 0.03, 60): share_width_lt_1 0.11, median width 2.44, GP beats hold 0.25, mean gain 0.047 | no (internal inconsistency with Table 12, see N4) |
| l.313 | narrow sets 31-45% (T=30), 10-14% (T=60), 1-5% (T=120); goal-program sets narrow in at least 96% of cells; target error 0.01-0.13 at T=30 and 0.004-0.03 at T=120 | placebo_grid.csv: 0.31-0.45; 0.10-0.14; 0.01-0.05; min 0.96; 0.012-0.133; 0.0044-0.0255 | yes |
| Table 3 | synthetic losses 0.205/0.089, 0.189, 0.101, 0.000, 0.093/0.055, 0.052, 0.111/0.106 | no file in results/ | n/a |
| Table 10 / Table 9 | all entries (n, tau, band, set, steps, mean-minus-tau, q-values, GNI-adjusted) | aid_combined_tests.csv, aid_gni_drift.csv, aid_goal_comparison.csv | yes |
| Table 8, Table 6, Table 5 | bootstrap, confirmatory and exploratory entries | bootstrap_cb_100_summary.csv, cb_benchmarks.csv, confirmatory_cb.csv | yes |
| l.22 abstract | "one to three donors" | combined q <= 0.10: 3 (iid), 1 (block); at 0.05: 1 (iid), 0 (block) | yes at 10% only (level not stated) |

---

## 6. Other assessment points

### Correctness of the main results

- **Theorem 1 (closed form):** correct as stated. I rechecked the derivative cases (u >= omega^+, 0 <= u < omega^+, u < 0 < l, symmetric lower cases) and the b = 0 edge case.
- **Propositions 1-5:** correct for the stated generic (strict-optimality) case. The MILP derivative constraints (right and left derivatives with the binaries a, s, l, z, u, v) are correct. Proposition 5 correctly assumes known (alpha, c, d) and observable sets.
- **Theorem 2:** the statement and the vertex argument are plausible and the algorithm agrees with a random-search check on Swedish aid. The proof has the domain gap described in N6.
- **Theorem 3:** the Lipschitz argument is correct; the domain needs the repair in N6.
- **Theorem 4:** the argument (median condition, continuity via strong convexity, ergodic uniform law, kink count) is correct. The kink count (four for b > 0, two for b = 0, because the slope alpha is continuous across the dead zone when b = 0) is right. Its assumptions do not hold for any of the applications; the scope paragraph and the closed-loop Monte Carlo say so.
- **Overclaiming that remains:** "right magnitude" (central banks); "near their national 1% goals" (Sweden); "a combined test ... one to three donors" without the FDR level; "solves small instances" (MILP). Item N1 contains two statements that contradict the paper's own tables.

### Substantive points not yet discussed in the paper

- ODA "decisions" include in-donor refugee costs and debt-relief spikes (Iraq 2005-06, the 2015-16 refugee peaks). These produce large single-year changes unrelated to the donor's aid goal and could be responsible for the large Sweden and Portugal steps. A sensitivity analysis that excludes debt relief (or uses the grant-equivalent measure throughout) would help.
- The aid sample pools 1960-2024 under a constant target while the paper itself says goals changed (Sweden 2022, the Netherlands 2012). A sub-period fit for the donors with a documented change would be a more direct test than the pooled comparison.
- The "goal in band" comparison is not independent of the estimates: the five national goals were compiled after the estimates existed (l.283 admits it).

### Fit to the special issue

- **Goal programming:** a good fit (interval goals, aspiration levels, identification).
- **Multiple objective:** thin. The exact and proved results are one-goal, and the K=2 application is the weakest result.
- **AI for decision making:** the link is "learning a goal program from data". There is no machine-learning component beyond a multistart search. The connection to inverse reinforcement learning and decision-focused learning is only in the literature review.
- **Economic and social sciences:** four applications, one of them a null result (firms) and one descriptive (defence). The aid application is the strongest, but only for one to three donors.

### Presentation

- Long paragraphs (list in minor 17 of section 2 and minor 18 of section 4) with ten or more numbers each, particularly l.253, 261, 277, 313, 317. Move the numbers to tables.
- Reading order: tables 9 and 10 are referenced before they appear (Table 10 first at l.190), and the tables float to the next page.
- The compiled PDF has no unresolved references or literal "midrule". The v2 LaTeX bug is gone.

---

## 7. What I would require for acceptance

1. N1: correct the two statements (l.285 and l.298); restate the abstract's claim about Sweden and Norway with both measures.
2. N2: align optimisers for the bootstrap, add a coverage check with degenerate replicates, report best-of-five as primary, and present Turkey as a boundary fit.
3. N3: either report an MILP instance that closes or delete "solves small instances"; state that Theorem 3 and the alpha-identification are not used empirically.
4. N4: reconcile Tables 12 and the grid; report the FDR level in the abstract; calibrate the 2% sets (or call them descriptive).
5. N5: fix the Springer title, keywords and the date line.
6. N6: repair the domain argument in Theorem 2 and Theorem 3.
7. Presentation: shorten the abstract, split the 300-word paragraphs, fix minor items 2, 6, 7, 8, 19 of section 4.
