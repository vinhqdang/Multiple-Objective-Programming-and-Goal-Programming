# Referee report (second round): "Revealed Aspiration Levels: Inverse Interval Goal Programming for Recovering the Targets and Priorities Behind Public Decisions"

Annals of Operations Research, special issue "Multiple Objective Programming and Goal Programming: AI for Decision Making in Economic and Social Sciences".
Material read: paper2/main.tex (line numbers below refer to it), the tab_*.tex files, the compiled Springer PDF (31 pages), cover_letter.md, results/*.csv, and docs/review_full_paper.md (first-round report).

---

## 1. Summary

The paper formulates the recovery of aspiration bands, transmission coefficients and deviation weights of an interval goal program from sequential decisions. The forward model is a one-period interval goal program with asymmetric weights and a linear or quadratic adjustment cost. A change of variables ((alpha, c, d, omega)) linearises the optimality conditions for given discrete states. Theory:

- Proposition 1: breakpoint optimality.
- Proposition 2: normalisation and effective weights.
- Proposition 3: edge revelation.
- Proposition 4: weights are not point-identified under linear cost.
- Proposition 5: a rank condition for the weights under quadratic cost.
- Theorem 1: closed-form clip policy for one goal.
- Theorem 2: exact O(T^4) estimator for one goal and fixed alpha.
- Theorem 3: Lipschitz grid certificate over alpha.
- Theorem 4: consistency, with point identification for K=1 only.
- Theorem 5: pseudo-true-parameter result under misspecification.

For K>=2 the paper gives an exact MILP, which stalls, and a multistart heuristic with LP/LNS polishing.

Applications:

- 14 central banks (K=2, heuristic). The implied targets are no closer to the stated targets than a constant 2.5%.
- 23 aid donors (K=1, exact). Two BH-adjusted tests are used, and a minority of donors pass both.
- Defence spending, pooled over allies, before and after 2022.
- Corporate leverage (largely uninformative).

A model-adequacy section reports placebo experiments and out-of-sample comparisons. The goal program does not out-predict simple rules.

The revision is a substantial improvement on the first round. Benchmarks, multiplicity adjustment, persistent-decision size checks, defence uncertainty, a recovery study for K=2, multi-seed stability, a scope paragraph for the theorems and a wider literature review have been added. The abstract and discussion now report the weak validation honestly. I verified almost all numbers in the text against the CSVs and found two small mismatches (Section 5). The mathematics for K=1 is correct, with a few presentation-level imprecisions. The remaining problems are:

- (a) the K>=2 part, which is the "multiple objective" part, has neither identification theory nor a reliable optimiser;
- (b) the uncertainty quantification for central banks and defence is not valid as described;
- (c) the aid inference chain has gaps in test calibration;
- (d) the title and abstract still promise "priorities";
- (e) fit to the special issue is only partial;
- (f) presentation defects, including one visible LaTeX bug.

## 2. Recommendation: **Major revision**

Reasons:

- (i) The contribution that is exact and proved (a closed-form policy, an exact estimator and certified grid for one goal, consistency for K=1) is real and publishable in ANOR. It is narrower than the title ("priorities") and the multiple-objective framing of the special issue suggest.
- (ii) For K>=2 nothing is proved or reliably computed. The only K=2 application (central banks) is the weakest result in the paper, and its uncertainty statements are not valid as described (Major 2 and 3).
- (iii) The substantive findings for aid and defence rest on tests whose calibration is incomplete (Major 4 and 5). Defence has no goal-seeking or partial-adjustment test at all, and its headline contrast depends on one of two uncertainty measures.
- (iv) The paper is honest about negative results. That is a strength. With the revisions below I would expect to recommend acceptance. The trajectory is good, and I would not require a third full round if Major 1-5 are handled.

---

## 3. Major issues

### M1. The multiple-objective content (K>=2) is the least developed part, yet it carries the framing and one of four applications
- Locations: abstract (l.21), contributions (l.31), Remark (l.107), Section 3.1 (l.114-117, 139-140), Theorem 4 (l.203), scope paragraph (l.214), cover letter ("exact mixed-integer linear estimator").
- Problem.
  - All identification results beyond Proposition 5 and all exactness, certificate and consistency-with-identification results are for K=1. Proposition 5 for K>=2 assumes (alpha, c, d) known and the state sets A_t, B_t observable.
  - Joint identification for K>=2 is explicitly "open" (l.107).
  - The MILP "did not close the gap" (l.114, Table 3: 0.205 vs 0.089 at the true parameters).
  - The heuristic stops above the true-parameter loss in 8/20 (noise 0.05) and 5/20 (noise 0.10) instances at K=2, T=60 (l.140; I reproduce this from k2_recovery.csv), with errors for the second goal of 0.17-0.56 in tau.
  - Six of fourteen bank fits are seed-dependent (l.263).
  - Yet the abstract says priority weights "are [point-identified] under a quadratic one, given a rank condition". The rank condition presupposes known (alpha, c, d) and known states (Remark, l.107). The cover letter says the method "yields an exact mixed-integer linear estimator", which contradicts l.114.
  - The only multi-goal empirical case, the central banks, has two goals (inflation and growth gap), and no result in the paper interprets the weights or priorities across goals. "Priorities" in the title is therefore not supported by any application, and in the goal-programming literature "priorities" usually denotes lexicographic levels, which are not modelled.
- Fix.
  1. State in the abstract that the weight rank condition is conditional on known aspiration levels, and that joint identification is proved for one goal only.
  2. Either prove at least one K=2 identification result (for example K=2 with disjoint support of the states, reducing to two K=1 problems), or move all K>=2 statements into an explicit "negative/limited" paragraph.
  3. Remove "exact estimator" for the MILP from the cover letter. Say "exact formulation, solved to optimality only for small instances".
  4. Rename or define "priorities" (suggest "deviation weights/step sizes"), or add an application where cross-goal weights are estimated and checked.
  5. Add an exact check for K=2 on at least one real bank, for example by running the MILP on the shortest bank (Hungary, n=33) with a warm start and reporting the proven gap.

### M2. Central-bank uncertainty (bootstrap) is not a valid inference procedure as described
- Locations: l.258-260, Table `tab:boot`, Fig. `fig:cb`, abstract/cover letter statements about intervals; discussion l.320.
- Problems.
  - (a) The replicates use a lighter optimiser (DE, no LNS) than the point estimates, so the bootstrap distribution mixes sampling variability with optimiser differences. Bootstrap medians differ strongly from the point estimates: IL 1.45 vs 3.49, SE 0.88 vs 1.36, NZ 2.84 vs 1.66 (the point estimate sits at the 5% limit, 1.65), HU 4.10 vs 4.97 (from bootstrap_cb_100_summary.csv and Table 8). That indicates bias or optimiser mismatch, not just spread.
  - (b) Quantiles are computed only over non-degenerate replicates. This conditions on an event that is itself informative. The UK has 42 of 100 degenerate replicates and Turkey 39, but the text still says the UK interval is "about 1 pp wide" (l.258) and presents it as a reliable one. The reported 1.79-2.77 describes only 58 replicates, and the table does not show the UK as uninformative.
  - (c) "Twelve of fourteen intervals contain the stated target" is not a coverage statement. A confidence interval for the pseudo-true parameter has no reason to contain the stated target. The statistic confuses validation with inference, and Section 4.1 itself shows that the model recovers the stated target no better than 2.5%.
  - (d) B=100, with 8-quarter blocks on windows of 33-104 quarters. The 5%/95% limits are the 5th and 95th of ~100 draws, and the first round's request for >=500 was not met.
  - (e) Percentile bootstrap for a non-regular, boundary-affected estimator is not justified. No coverage simulation is given, although the K=2 simulator already exists (k2_recovery).
- Fix.
  1. Use the same optimiser for point estimate and replicates, or add the point estimate's optimiser as one of the replicate fits.
  2. Report intervals for bounded quantities (band edges e+/-, c, alpha, or the profile set of tau) and treat a degenerate replicate as "tau unbounded", i.e. report the probability of that event and use it as a part of the interval (conservative: any interval for a bank with >10% degenerate replicates should be shown as one-sided or unbounded).
  3. Drop "twelve of fourteen contain the stated target" or relabel it as a descriptive statistic.
  4. Calibrate coverage in the K=2 simulation (20 instances x B=100 is enough for a rough check).
  5. Raise B to at least 500 for the main table.

### M3. The comparative benchmark for central banks is still weak, and the planned second ground truth is missing
- Locations: l.242, 250, Table `tab:cbbench`.
- Problems.
  - (a) The "Taylor-rule implied target" is a difference rule fitted by LAD on rate changes. For 7 of 14 banks the fitted slope on inflation is zero or negative (b_pi = 0 for GB, NO, AU, IN, PL, TR and -0.02 for CA in cb_benchmarks.csv), largely because most quarterly changes are zero. The "undefined" outcome is therefore an artefact of the benchmark, not of the economics. The comparison "0.81 vs 1.29" is over the 7 banks where the benchmark happened to be defined, which is itself a selected set.
  - (b) The literature the paper cites (Dennis; Favero-Rovelli; Ozlale; Ireland) uses level rules with partial adjustment and estimates the implicit inflation target from the intercept. That is the natural benchmark with the same data, and it is not reported.
  - (c) The first report asked for a comparison of the estimated band half-width b with official tolerance bands (Israel and NZ 1-3%, Mexico +-1, etc.), a free second validation. It is absent.
  - (d) The statement "implied targets have the right magnitude" (abstract) carries little information, given that a constant 2.5% does as well (0.61 vs 0.64 overall).
- Fix.
  1. Add a level-form Taylor/partial-adjustment benchmark on the same windows, with an implied target from the intercept under a stated neutral-rate assumption (or with r* estimated).
  2. Report all 14 banks for each benchmark, with an explicit rule for undefined cases rather than dropping them.
  3. Add the estimated vs official band comparison, or explain why it is not feasible.
  4. Qualify "right magnitude" in the abstract (for example "within about 0.6 pp on average, as a constant 2.5% is").

### M4. Aid: the inference chain from "tests passed" to "revealed target" is incompletely calibrated, and some framing statements are false or inconsistent
- Locations: l.266-276, Tables `tab:aid`, `tab:aidgt`, abstract, discussion l.319.
- Problems.
  - (a) Size of the PA test is never checked. Only the state-dependence test has a size study (l.270). The PA test resamples LAD residuals as i.i.d., although the paper itself documents that decisions are persistent, and that persistence alone raised the rejection rate of the first test to 9% at the 5% level (13%/12% at 10%, 100 series). The second test has B=199, so its smallest attainable p is 0.005. Five donors are "rejected at 5%" with BH-adjusted values of 0.038-0.046 (reproduced from pa_null_test.csv), which sit at the resolution limit. Run the same size experiments (i.i.d., AR(1), regime-switching non-goal-seeking decisions, and a partial-adjustment DGP with autocorrelated errors) for the PA test and increase B to 999.
  - (b) A rejection of partial adjustment is not evidence for the goal program. Any nonlinearity, asymmetric response, structural break (Sweden's 2023 change, the Netherlands' 2012 change, as the paper itself says) or heteroskedasticity rejects it. The placebo (Table 12) shows that the quadratic-programme DGP, which is not a goal programme, is also fitted with tau = 1.99 and rejects PA 95% of the time. The sentence "find goal-program behaviour for a minority" (abstract) should read "find state dependence and non-linearity inconsistent with linear partial adjustment".
  - (c) "Four donors pass both tests" combines two BH procedures per test. The conjunction has no error-rate control, and a total of 46 tests is carried out. Either use a single combined procedure (for example BH over max(p1, p2), which is valid under the intersection-union structure), or say clearly that the "pass both" list is descriptive.
  - (d) l.266: "Every donor has the same stated commitment, 0.7% of GNI" is not accurate. The US has not accepted the 0.7% target, Korea and Spain joined at other dates and with other targets, and the paper itself then lists national goals that differ (1.0, 0.8). This affects the stated contrast "under the same 0.7% commitment" (discussion).
  - (e) Weak national-goal comparison. The rule is now fixed ("goal in band / in set"), which is an improvement, but the donor set is still the five donors for which a goal was found after the estimates existed. EU-15 donors with documented 0.7% timetables (BEL 0.48, FRA 0.56, DEU 0.57, FIN 0.59) have revealed targets clearly below 0.7. These are only mentioned in one sentence for PRT and FIN (l.274) and are not scored by the rule. The Netherlands' goal (0.7) is outside the band, Sweden's (1.0) outside both band and set, yet the abstract says Sweden "reveals targets near" the goal. State the full table over all donors with a documented goal, including misses, and apply the same rule to the abstract.
  - (f) Targets near the mean level. For the four "passing" donors with low levels (PRT 0.27, JPN 0.28, USA 0.21), the revealed target is within 0.05 of the average level (0.21/0.25/0.25). A target that equals the sample mean is exactly what a fit of a drift-with-noise model produces. Discuss this explicitly, and report the revealed target minus mean level for all donors.
  - (g) Near-optimal sets contain negative values (TUR -0.27, AUS -0.11, DEU -0.04, GBR -0.06): sets for a non-negative share should be truncated or the profile restricted to tau >= 0. Step sizes such as 0.43 pp of GNI per year for Sweden and 0.35 for Portugal (Table 10) are implausibly large and not discussed. They look like single-episode artefacts (one large cut dominates the saturation level).
  - (h) The state x_t is last year's share, so GNI growth moves the state mechanically (acknowledged in one parenthesis, l.229). The first report suggested ODA_{t-1}/GNI_t; this was not done and no sensitivity is given.
  - (i) The permutation test (B=999) is known to be liberal under persistence, and ODA changes are persistent. The paper reports no autocorrelation of the actual series, so the reader cannot judge how liberal the test is for them. A block-permutation or phase-randomised version would answer this.
- Fix: items (a)-(i) above, in particular a size study of the PA test, B=999, a combined multiplicity rule or "descriptive" wording, a full table over donors with documented goals, and a correction of l.266.

### M5. Defence: no test of goal-seeking, and the headline "3.2% well outside the earlier uncertainty range" rests on one of two uncertainty measures
- Locations: l.293-295, Table `tab:def`, abstract, discussion l.319, cover letter.
- Problems.
  - (a) The two tests used for aid (state dependence; GP vs PA) are not run for defence, although the pooled fit has far fewer free "decisions" than structure (the 2022-2025 fit uses 123 observations, about 4 per ally). The out-of-sample comparison (Table 14, defence) gives GP 0.183 vs hold 0.191 and median change 0.170, so the median change is better than GP. The first report asked for a permutation test.
  - (b) The statement "well outside the earlier bootstrap interval" compares bootstrap intervals (3.21-3.95 vs 1.37-2.10). The profile 2% sets for the same quantity overlap heavily (1.12-3.61 vs 2.75-3.87; defence_uncertainty.csv). The paper reports both but the abstract and cover letter use only the favourable measure.
  - (c) The lower bootstrap limit for 2022-2025 (3.21) equals the point estimate (3.21): the point sits at the boundary of its own bootstrap distribution. This is the signature of a data-determined boundary (the lower edge is set by a few allies who stopped raising), not a well-behaved interval.
  - (d) The two periods are separated by an author-chosen event date (acknowledged). The shift is confounded with the invasion (acknowledged), and with the level effect of mean(1.48 vs 1.85) and the share of observations below the lower edge (84.8% and 92.7%): nearly all observations lie in the "step up" regime, so a larger common step up mechanically moves the fitted lower edge to the few allies above it.
  - (e) The table shows a "step down" of 0.20 and 0.21 although only 2.3% and 2.4% of ally-years are above the band. By the paper's own rule (l.239) such a step should be a dash.
  - (f) The old sign-based estimator (1.42 and 2.20) is mentioned as "superseded" (l.295). A reference to a superseded estimator in the replication files has no place in the paper; either move it to the repository or explain it in one sentence and cut.
- Fix: run the two tests for defence (permutation on a cluster/ally basis); present both uncertainty measures in the abstract and discussion ("rose from about 2% to 3.2%; the two uncertainty measures disagree on whether the shift is distinguishable"); add a placebo-style leave-one-ally-out check; replace the step-down value by a dash.

### M6. Theory: correct for K=1, but several statements are imprecise or over-stated
- (a) Remark (l.107): "the decision maker moves in constant steps omega_k^± while a single goal is outside its band". That is true only when the goal is farther than omega from the band edge (u >= omega^+). Between the edge and omega the move equals the distance to the edge (ramp, Theorem 1). State this.
- (b) Proposition 4 is correct under strictness, but its content is mostly an artefact of the normalisation lambda=1 together with a strict inequality. For K=1 the set is a half-line omega > 1 in the region where the goal is outside the band. The paper should say that the non-identification is of the *scale* relative to the linear cost and that identified relative ratios are not discussed. The final remark (l.97) about the noisy counterpart (Theorem 5) is too brief to support the abstract's contrast.
- (c) Algorithm 1 and Theorem 2: the O(T^3 log T) claim (l.190) is asserted, not proved. Either supply a two-line argument (it is simple) or label it "can be shown". The text says "growing roughly as T^3" (l.190) and then "T^2.3-T^2.9" a few lines later. Keep one.
- (d) Theorem 4 (consistency): the assumptions do not hold for any of the applications. Controlled state (aid, defence: x_{t+1} = x_t + Delta_t), discrete decisions with many zeros (central banks, B2 has no density), data-dependent search ranges, and fits at the lower bound of alpha are all admitted in l.214, which is honest. But then the Monte Carlo (l.218-225) uses an AR(1) *exogenous* state and a continuous noise, which is the one case covered by the theorem. Add one Monte Carlo with a controlled state (x_{t+1} = x_t + D_t^* + noise with an AR(1) shock) and discretised decisions, and report whether the estimator still behaves.
- (e) Theorem 4 point identification requires omega_0^± > 0 and an x-density that covers all four kinks. For aid and defence the data visit the upper regime in only ~2% of observations (l.295). That makes the upper edge and step "weakly determined" in the paper's own words, which is the empirical counterpart of the support condition failing. Say so in the identification discussion; it links theory to the applications better than the present "when to trust an estimate" paragraph.
- (f) Proposition 5 (rank condition) should say "if (alpha, c, d) are known *and the sets A_t, B_t are therefore known*". The current wording is correct but easy to misread; the abstract drops the qualifier (M1).

### M7. Model adequacy: calibration of diagnostics and paired tests
- Locations: l.310, l.314, Tables 12-14.
- Problems.
  - (a) The placebo uses one noise level (0.03), one T (60), one parameter set. The first report asked for variation in noise, T and persistence. This was not done (only the size study for persistent decisions was added).
  - (b) Out-of-sample comparisons still carry no significance statements, although a sign test on 23 donors and 14 banks is trivial (GP strictly best in 5/23 and 1/14, worse than hold in 12/23 and 11/14, as I verified from model_comparison.csv). The paper says "imprecise" but then makes comparative statements ("compares favourably with the implied target of partial adjustment", l.314) on 5 donors.
  - (c) That comparison is not matched for sample or "defined" status (PA target undefined for 5 donors in the CSV, see Section 5). The numbers quoted (Luxembourg 1.00 vs 1.87, Sweden 0.90 vs 0.75, Denmark 0.86 vs 1.41) are small-n anecdotes.
- Fix: run the placebo at two further noise levels and T = 30 and 120; add sign/Wilcoxon tests; turn the five-donor sentence into a table, or drop "compares favourably".

### M8. Fit to the special issue and positioning
- The paper is a good fit for "goal programming" and "AI for decision making" in the sense of learning a goal programme from data. The "multiple objective" side is thin (M1), and the "economic and social sciences" side is a mixture of one weak validation (central banks), one aid application with selective validation, one defence application with a confounded contrast and one null application (firms).
- The four-domain structure spreads the paper. The firms section is a null result of low value to a reader (l.302, a long paragraph on depository institutions and Basel III that concludes "does not test it").
- Recommendation: shorten firms to three sentences plus the table, move Appendix A/B and some of the Section 3 synthetic detail to an online supplement, and state in the introduction that the method is for one-goal problems at its core, with K>=2 treated as an extension with limited guarantees.

---

## 4. Minor issues

1. **LaTeX bug in Appendix Table A1 (l.334).** The header ends in `\\\\midrule` instead of `\\\midrule`. The compiled PDF (page 30) prints the literal word "midrule" in the first row, and the rule is missing. Fix.
2. **Notation clash in the MILP (l.114).** "fitted decisions D_t, residuals r_t >= |D_t - D_t|" uses D_t for both observed and fitted decisions, and "g_{kt} = alpha_k x_{kt} - D_t - c_k" uses D_t as fitted. Use D_t^obs (or y_t) for data. The first report's minor item 9 asked for this and it is not done.
3. **Symbol reuse.** b is the band half-width, but it is also the partial-adjustment slope (l.272, "Delta_t = a + b x_t", and "-a/b") and b_pi (Taylor). T is sample size and the horizon; L is the Lipschitz constant and the loss L_PA/L_GP. Rename the PA parameters.
4. **Development paragraph (l.244)** says earlier specifications had MAE "0.72-1.55 against 0.47". Appendix A also lists 0.94 and 1.83 (the latter against 0.22) and a sign-only rule that did slightly beat the benchmark (0.46 vs 0.48). State the range correctly or say which were included.
5. **Remark on rate-limit equivalence (l.107).** Good point, but the Table 12 placebo (quadratic programme with |Delta| <= 0.35) shows exactly this equivalence. Cite it there.
6. **Size results (l.270):** the text gives "9% (13% at 10%)" for AR(1) decisions, but permutation_extend.csv gives 9% and 12% (size_ar1). With 100 series the Monte Carlo SE is about 2-3 pp, so the "somewhat liberal" statement should come with this SE.
7. **Section 5.2 first paragraph.** State that the 2018 break is dropped for the real data, and say how the permuted level paths treat it (it is in the text, but spread over two places).
8. **Table 10 (aid)** has 8 columns with two-line cells. It repeats five rows of Table 11 (`tab:aidgt`). Merge the two (add "national goal" and "goal in band/set" columns, and shade the four dagger donors) or drop the redundant columns. Add the mean-level-minus-target column suggested in M4(f).
9. **Table 2 caption (datasets):** "firms: 93,223 firm-years" but the estimation uses at most 3,000 per industry (about 24,000 firm-years in Table 12). Say so in the caption. The abstract-level "13,763 firms" is not used for the estimation.
10. **India's 4% target.** n=34 quarters ends in 2019Q4, i.e. starts in about 2011. India's formal 4% (+-2) flexible inflation target dates from the 2015-16 agreement. Check that the "stated target validity date" is right for that window (it is the only exploratory bank for which I could not reconcile n with a formal start date). The confirmatory_windows.csv does not list Indonesia, although l.248 discusses it.
11. **Defence "31 allies, 2014-2025"**: Finland and Sweden joined in 2023/2024. State how pre-accession data are treated.
12. **Figure captions.** Fig. `fig:cb`: "vertical bars are 90% bootstrap intervals over the bounded replicates" repeats M2's problem; add the number of degenerate replicates to the figure for GB, TR, IN.
13. **Table 3 (synthetic evidence)** has no parameter-recovery columns although the text says "recovers aspiration levels, bands, transmission and, approximately, weights" (l.139). Either add them or refer to the K=2 recovery study.
14. **Section 4 first sentence of Discussion (l.319):** "revealed targets range from about 1% (Norway, Luxembourg, Sweden) to about 0.2-0.3% (Portugal, Japan, the United States)". Japan and US pass only the PA test, not both (they are not among the four double-pass donors). The abstract and the cover letter give a (slightly) different wording ("among donors whose decisions reject PA after adjustment"). Use one formulation everywhere.
15. **Cover letter.** "far closer than average inflation where the two diverged strongly" (one country, Turkey, plus Mexico) and "Sweden and Norway close to their national 1% goals" (Sweden's goal is outside both the band and the set) are stronger than the text. "Two calibrated tests" is not accurate for the PA test (M4a). "Exact mixed-integer linear estimator" (M1).
16. **Literature still missing.** (i) Revealed-preference foundations (Samuelson, Afriat, Varian) for the word "revealed". (ii) Inverse reinforcement learning / inverse optimal control (Ng and Russell 2000; Ziebart et al. 2008; Keshavarz et al. 2011 is cited, but not IRL). The first report asked for inverse optimal control and this is still absent. (iii) Taylor (1993) and Clarida-Gali-Gertler (2000) for the benchmark in M3, and Svensson for inflation-forecast targeting. (iv) Charnes-Cooper "goal interval programming" and Ignizio on aspiration levels, plus Simon's satisficing for the term "aspiration level". (v) Defence: burden-sharing and defence-demand literature (Olson-Zeckhauser; Sandler-Hartley; Dunne-Smith), relevant for the pooling and for interpreting the NATO 2% norm. (vi) Aid: the 0.7% target history and donor-specific commitments (for l.266).
17. **Page and structure.** 31 pages in the Springer layout. Section 4.1 contains very long paragraphs (Uncertainty, Robustness, each over 250 words with ten numbers). Move the numeric detail into tables and keep one message per paragraph.
18. **Reference to repository files inside a table caption** (Table 11: "data/aid/targets.csv and docs/lit/14_..."). Replace by a citation to the supplementary material.
19. **Statement in l.229** that "Central banks ... serve as validation" is inconsistent with the later conclusion that they provide only weak validation. Reword to "a check".

---

## 5. Number checks

Sources: results/*.csv and the tab_*.tex files. "Yes" means the text value equals the source value after rounding.

| # | Location | Text value | Source value | Match |
|---|---|---|---|---|
| 1 | l.250, Table 7 | MAE implied 0.64, mean inflation 0.85 (14 banks) | cb_benchmarks.csv: 0.644 / 0.846 | yes |
| 2 | l.250 | without Turkey: 0.61 vs 0.47; const 2.5%: 0.61 / 0.46 | 0.606 / 0.473; 0.607 / 0.462 | yes |
| 3 | Table 7 | Exploratory 0.45/0.47/0.44/0.44; Confirmatory 0.99/1.52/0.90/1.10; conf. without TR 0.96/0.47/0.50/0.75 | 0.451/0.472/0.444/0.444; 0.992/1.52/0.90/1.10; 0.955/0.474/0.50/0.75 | yes |
| 4 | Table 7, Taylor column | 0.81 vs 1.29 (n=7); confirmatory 1.65 / 0.96 (n=4); exploratory 0.81 / 0.62 (n=3) | recomputed: 1.287 / 0.813; 1.645 / 0.955; 0.81 / 0.62 | yes |
| 5 | l.250 | Taylor target defined in 7 banks | b_pi > 0 in 7 rows (SE, MX, CL, IL, NZ, CO, HU); b_pi <= 0 in 7 rows | yes (but see M3a) |
| 6 | l.258, Table 8 | degenerate replicates UK 42, TR 39, IN 29, NO 10 | bootstrap_cb_100_summary.csv: 42, 39, 29, 10 | yes |
| 7 | l.258 | 12 of 14 intervals contain stated target; MX 3.18-3.89, PL 0.66-2.18 excluded | covers_stated False for MX, PL only; values match | yes |
| 8 | l.258 | widths about 1 pp for AU, CA, GB, MX; >= 4 pp for CL, IL | 0.97, 0.97, 0.98, 0.71; 4.33, 4.00 | yes (but UK has 42% degenerate, M2b) |
| 9 | l.258 | Sweden interval 0.21-2.15; mean inflation 1.2 | 0.2135-2.1456; 1.197 | yes |
| 10 | l.263 | with 2 / 6 quarter horizon, 3 and 2 degenerate fits; MAE 0.80 / 0.93 vs 1.02 / 0.42; closer in 4/7 and 2/4 off-target | sensitivity_cb.csv recomputed: 3, 2 degenerate; 0.80/1.02, 0.93/0.42; 4 of 7 and 2 of 4 | yes |
| 11 | l.263 | end 2015: 0.75 vs 0.48, 4 of 5 off-target | 0.75 / 0.48; 4 of 5 | yes |
| 12 | l.263 | five seeds: best-of-five MAE 0.58 (0.53 without TR); HU 3.90 vs 4.97 (2% lower loss); AU 2.76 vs 2.63; six banks with seeds within 9% and targets > 0.5 pp apart (CL, HU, IL, IN, NO, SE) | cb_multiseed.csv: 0.577 (0.534); HU 3.90; AU 2.756; six banks identical | yes |
| 13 | l.140 | K=2 recovery: median loss 5% below true; stops above in 8/20 and 5/20; at most 31% above | k2_recovery.csv: 0.946 / 0.953; 8 and 5; max 1.31 | yes |
| 14 | l.140 | median abs errors tau1 0.02/0.09, b1 0.04/0.11, alpha1 0.03/0.14, tau2 0.17/0.56 | 0.021/0.088, 0.037/0.111, 0.031/0.141, 0.175/0.557 | yes |
| 15 | l.218-225 | Monte Carlo errors T=50/100/200 (0.040, 0.039, 0.020, 0.024; ...; 0.021, 0.017, 0.013, 0.009) | consistency_mc.csv: 0.0400, 0.0385, 0.0204, 0.0235; ...; 0.0212, 0.0169, 0.0125, 0.0094 | yes |
| 16 | Table 4 / l.190 | exact 0.02/0.10/0.53/3.97 s; heuristic 4.1/4.1/5.3 s; heuristic at optimum 10/9/10; one case 0.06% above | comp_study.csv: 0.020/0.100/0.532/3.974; 4.07/4.13/5.35; T=50 inst 1 gap 0.058% | yes |
| 17 | l.190 | "10-200 times the run time" | 5.3/0.53 = 10; 4.1/0.02 = 205 | yes |
| 18 | l.190 | run time "roughly T^3" and then "T^2.3-T^2.9" | slopes 2.3, 2.4, 2.9 | partly (inconsistent wording) |
| 19 | l.270 | state-dependence BH: seven donors at 10% (SWE, BEL, PRT, FRA, NOR, TUR, NZL), four at 5% | permutation_extend.csv p_bh: 0.023, 0.038, 0.038, 0.040, 0.060, 0.084, 0.085 | yes |
| 20 | l.272, Table 10 | PA test BH: five donors at 5% (PRT, SWE, NOR, LUX, TUR), plus JPN, FIN, USA at 10% | recomputed BH from pa_null_test.csv: 0.038, 0.038, 0.038, 0.046, 0.046; 0.058, 0.082, 0.086 | yes |
| 21 | l.270 | size: 2% at 5% and 7% at 10% (200 series, i.i.d.) | permutation_test.csv calibration: 0.02 / 0.07 | yes |
| 22 | l.270 | AR(1) decisions: 9% at 5%, 13% at 10% (100 series) | permutation_extend.csv size_ar1: 0.09 / **0.12** | **no** (13% vs 12%) |
| 23 | l.270 | regime-switching drift: 8% (13%) | size_regime: 0.08 / 0.13 | yes |
| 24 | l.274, Table 10 | revealed targets 0.90, 0.27, 0.98, 0.56 (SWE, PRT, NOR, TUR); LUX 1.00, FIN 0.59, JPN 0.28, USA 0.21 | aid_exact.csv: 0.90, 0.265, 0.98, 0.56; 1.00, 0.595, 0.285, 0.215 | yes |
| 25 | l.274 | UK near-optimal set -0.06 to 1.00; Turkey -0.27 to 0.58 | aid_exact.csv set2: [-0.06, 1.00]; [-0.27, 0.58] | yes |
| 26 | l.276, Table 11 | Sweden band 0.83-0.97, set 0.88-0.95, mean 0.77; NLD band 0.49-0.61, set 0.49-0.73, mean 0.73; DNK band 0.71-1.01 | aid_exact.csv | yes |
| 27 | l.187 | multistart matched exact loss for 5 of 10 donors, up to 5% above for others; NLD 0.55 vs 0.73; UK 0.49 vs 0.27 | not reproducible from the CSVs in results/ (heuristic runs for aid are only in aid_exact.log) | not checked |
| 28 | l.295 | defence 2015-2021: 85% below band; lower edge 1.99; bootstrap 1.37-2.10; 2% set 1.12-3.61; step up 0.02-0.06 | defence_exact.csv 0.848; defence_uncertainty.csv 1.99; 1.37-2.10; 1.12-3.61; 0.02-0.06 | yes |
| 29 | l.295 | 2022-2025: lower edge 3.21 (bootstrap 3.21-3.95), step up 0.12 (0.11-0.20); upper-edge share about 2% | defence_uncertainty.csv 3.21; 3.21-3.95; 0.12; 0.11-0.20; share_above 0.024 | yes (the bootstrap lower limit equals the point estimate, M5c) |
| 30 | l.295 | old sign-based estimator 1.42 and 2.20 | inverse_interval_gp_budgets.csv: 1.42, 2.2 | yes |
| 31 | l.310, Table 12 | coin flip: gain 3%, set width 3.5, GP beats hold 17%, 10% with set < 1; PA/QP tau 1.99; PA beats GP 95-100% | misspec_placebo.csv: 0.037 mean gain (0.028 median), 3.54 median width, 0.17, 0.10; 1.99/1.99; GP beats PA 0%/5%; median b-hat PA 0.29 | yes |
| 32 | l.314, Table 14 | GP strictly best in 5/23 donors and 1/14 banks (Mexico); worse than hold in 12 donors and 11 banks; means 0.056/0.052/0.049/0.050 and 0.481/0.413/0.380/0.380 | model_comparison.csv recomputed: 5 and 1; 12 and 11; same means | yes |
| 33 | l.314 | partial-adjustment implied target "undefined for 7 donors" | model_comparison.csv tau_pa is NaN for 5 donors (CHE, DEU, FIN, GBR, KOR) | **no** (7 vs 5) |
| 34 | l.314 | PA vs GP targets: LUX 1.87, SWE 0.75, DNK 1.41, NOR 1.01, NLD 0.75 | model_comparison.csv tau_pa: 1.87, 0.746, 1.41, 1.01, 0.746 | yes |
| 35 | l.248 | NZ passes the 0.5 pp filter by 0.04 pp | mean 2.543 vs target 2.0 -> 0.543 | yes |
| 36 | l.248 | sign test with three banks p = 0.125 | 1/8 | yes |
| 37 | l.244 vs Table A1 | earlier specifications MAE "0.72-1.55 vs 0.47" | Table A1 also lists 0.94, 1.83 (vs 0.22), 0.46 (vs 0.48) | partly |
| 38 | Table 10 | n, mean levels (SWE 0.77, NOR 0.80, LUX 0.63 ...) | aid_exact.csv mean_level | yes |

## 6. Status of the earlier report's points (docs/review_full_paper.md)

### Section 6 "Required revisions", major points

| # | Earlier point | Status | Comment |
|---|---|---|---|
| 1 | Reframe the central-bank claim: add constant/shrinkage benchmark, Taylor benchmark, result without Turkey, pooled 14 banks, band comparison | **Largely addressed** | Constant 2.5%, median of other banks, ex-Turkey and pooled comparisons were added, and the abstract and discussion were reframed (the paper now says the banks give no strong validation). The Taylor benchmark is degenerate for half of the banks (M3a). The comparison of the estimated band with official bands is still missing (M3c). |
| 2 | Verify the K=2 optimiser (20 instances at real sizes, multi-seed stability, exact checks) | **Partly addressed** | k2_recovery (20 instances per noise level) and cb_multiseed were added and are honestly reported. They show that the search misses the optimum in 8/20 and 5/20 instances and that six banks are seed-dependent. No bound or exact check, no K=1 reduction for banks (M1). |
| 3 | Identification and interpretation of "priorities" (fix Proposition 5, prove or drop joint identification, step-size interpretation) | **Partly addressed** | Proposition 5 now says "if", the step-size / rate-limit equivalence is stated, and joint identification is proved for K=1 (Theorem 4(iv)). The abstract and cover letter still present the rank condition without the "known (alpha, c, d)" qualifier; "priorities" remains in the title (M1, M6f). |
| 4 | Aid goal-seeking test: size under persistence, adjust for 23 tests, B>=999, reword | **Largely addressed** | BH adjustment, B=999 for the first test, size under AR(1) and regime-switching decisions, rewording to "state dependence" and the second test against partial adjustment. The PA test has no size study and B=199; the conjunction "pass both" has no error control (M4a-c). |
| 5 | National-goal comparison: pre-specified set and parameter, all donors, formal test, time-varying goals | **Partly addressed** | A single rule is stated (goal in band/set), and the comparison is called post hoc. Still five donors only, no formal test, no sub-period fit; EU-15 counterexamples are not scored; abstract still says "near" for Sweden (M4e). |
| 6 | Defence: uncertainty, period split, reconcile with earlier file, temper "matching 2%" | **Largely addressed** | Profile set and cluster bootstrap added, the old file explained, the 2% claim withdrawn. No permutation/PA test, and the 2022 contrast rests on one uncertainty measure (M5). |
| 7 | Bootstrap: >= 500 replicates, bounded quantities or profile sets, drop "11 of 14" | **Partly addressed** | B=100, degenerate replicates counted separately, "12 of 14" retained with a caveat. Lighter optimiser in replicates, conditioning on non-degenerate fits, tau still the target quantity, no coverage study (M2). |
| 8 | Consistency theorem: assumptions that fit the applications; K=1 only; exact minimiser vs heuristic | **Addressed** | The "Scope of the theorems" paragraph states the closed-loop, discrete-decision and compactness gaps and the K=1 limitation. Remaining request: a Monte Carlo with a controlled state (M6d). |
| 9 | Position against omitted literature; soften "no method found" | **Largely addressed** | Opportunistic disinflation, Rugemurcia, Surico, Kilian, Shapiro, online/contextual inverse optimisation, Chan, Zattoni, Ahmadi were added and the claim softened. Inverse reinforcement/optimal control, revealed-preference classics and Taylor-rule classics are still missing (minor 16). |

### Section 6 "Minor" points

| # | Earlier point | Status |
|---|---|---|
| 1 | Proposition 4 wording (relatively open, generic, noisy counterpart) | Addressed |
| 2 | Theorem 2: box on e, nonnegative omega candidates, O(T^3 log T), degeneracy | Addressed (the O(T^3 log T) statement is asserted, not proved, M6c) |
| 3 | Theorem 3: e-domain, certificate concerns loss not tau, UK example | Addressed |
| 4 | MILP constants and sensitivity to epsilon | Partly (constants reported; no sensitivity to epsilon) |
| 5 | "10-40 times" corrected to 10-200; exponent given | Addressed (wording inconsistency, minor 4/Check 18) |
| 6 | Sample selection (3,000 per industry; 2018/2019 wording; ID, CZ, KR, IS) | Addressed (Indonesia not in confirmatory_windows.csv, minor 10) |
| 7 | Text-table inconsistencies (US 0.21, discussion range, p-value interpretation) | Addressed (new mismatches: Checks 22 and 33; Japan/US wording in discussion, minor 14) |
| 8 | Placebo variations (noise, T, persistence; persistent non-goal-seeking behaviour) | Partly (persistent decisions added for the size test; no noise/T variation, M7a) |
| 9 | Notation table, D_t vs D_t^obs, Q_T defined early, shorter abstract | Partly (notation table and Q_T done, abstract shorter; D_t clash remains in the MILP, minor 2) |
| 10 | Paired tests for out-of-sample comparisons | Not addressed (M7b) |
| 11 | External timestamp or "pre-specified" wording | Addressed (now "pre-specified", with the same-day caveat) |
| 12 | Trim the firms paragraph on depository institutions | Partly (still a long paragraph, M8) |

### Other empirical points in the earlier Section 4

- **Pre-registration wording:** addressed.
- **Specification issues for banks** (realised inflation as state, policy-rate level missing, discrete moves, short windows): acknowledged in the text but not changed. This is acceptable as a limitation, but the "right magnitude" claim should account for it.
- **Aid: GNI-growth drift in the state, step-size plausibility, negative near-optimal sets, coverage of the 2% sets:** not addressed (M4g, M4h). The defence bootstrap gives a second uncertainty measure for the first time, but no calibration of the 2% sets.
- **Defence: pooling, period choice, 2025 estimate, sensitivity to data source:** acknowledged; sensitivity to COFOG data not reported (the old file is explained only for the NATO series).
- **Model comparison: aggregate PA better than GP and hold best:** acknowledged and the conclusion is stated correctly. The five-donor target comparison is still anecdotal (M7c).
