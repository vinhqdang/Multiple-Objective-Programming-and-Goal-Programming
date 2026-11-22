# Literature cluster 4: evidence and methods for data-driven public budget allocation

Scope: causal effects of school spending, OR/goal-programming models for allocating education or public budgets, and education production functions. Downloads are in /tmp/lit4/ (text extracted with pdftotext). "Read scope" says what was actually read. Statements marked [inferred] are my own inference, not the authors'. Where a locator is given it is the pdftotext line number of the extracted file in /tmp/lit4/ (e.g. jm.txt:303), or a section/table name.

Retrieval notes: OpenAlex hit its free daily budget after the first queries, arXiv returned nothing relevant for education-budget OR, and several publisher PDFs (Wiley, MDPI, Springer, SSRN, AEA for some DOIs) returned HTML walls rather than PDFs. I did not work around these. Papers I could not fetch are listed at the end as paywalled/metadata only, and none of them is used as evidence below.

---

## A. Causal evidence on school spending (read in full or near full)

### 1. Jackson, Johnson & Persico (2016)
- Citation: C. Kirabo Jackson, Rucker C. Johnson, Claudia Persico. "The Effects of School Spending on Educational and Economic Outcomes: Evidence from School Finance Reforms." Quarterly Journal of Economics 131(1), 2016. DOI 10.1093/qje/qjv036 (DOI confirmed by OpenAlex metadata). Version read: NBER WP 20847 (Jan 2015), https://www.nber.org/papers/w20847, file /tmp/lit4/jjp.pdf.
- Read scope: abstract, introduction, empirical strategy, first stage, the OLS-vs-IV comparison (Table 2), main results. Appendices skimmed only.
- WHY: Old correlational literature gave mixed answers on whether money matters. Authors want the effect of school spending on long-run adult outcomes, not just test scores.
- HOW: Link PSID children born 1955-1985 (followed to 2011) to district per-pupil spending. Court-ordered school finance reforms (SFRs), their timing and the funding-formula type, give the exogenous shifter. Event-study and IV. The endogenous regressor is the natural log of average per-pupil spending over ages 5-17 (jjp.txt:684, :899), instrumented by event-time indicators interacted with predicted spending change by district income group. First-stage F > 50 (jjp.txt:537).
- WHAT: A 10 percent increase in per-pupil spending in each of the 12 school years gives 0.27 more years of education, 7.25 percent higher wages and a 3.67 pp lower annual adult poverty rate (abstract, jjp.txt:60). For children from low-income families: 0.43 years of education, 9.5 percent higher earnings, 6.8 pp lower poverty (jjp.txt:182). Effects for non-poor children are small. Spending effects ran through lower student-teacher ratios, higher teacher pay and longer school years. Naive OLS comparison (jjp.txt:653-681): cross-sectional OLS shows a strong positive association with predicted outcomes (positive selection bias); within-district over-time OLS shows a negative association (compensatory/endogenous spending), whereas the IV variation is unrelated to predicted outcomes.
- Relevance: The only retrieved paper whose spending regressor is in logs, so its coefficients are elasticity-like (semi-elasticities per 10 percent). It also documents that the within-district fixed-effects variation we would use is itself biased downward. Its outcomes are adult attainment, not district graduation rates; effects are for 12 years of cumulative exposure, not contemporaneous spending.

### 2. Lafortune, Rothstein & Schanzenbach (2018)
- Citation: Julien Lafortune, Jesse Rothstein, Diane Whitmore Schanzenbach. "School Finance Reform and the Distribution of Student Achievement." American Economic Journal: Applied Economics 10(2), 2018. DOI 10.1257/app.20160567 (confirmed by OpenAlex metadata). Version read: NBER WP 22011 (rev. July 2016), /tmp/lit4/lrs.pdf.
- Read scope: abstract, introduction, implied-effect discussion, event-study results, equity/targeting section (partial). Data appendix not read.
- WHY: Post-1990 "adequacy" reforms are less studied than the 1970s-80s equity reforms. Does the money reach low-income districts and raise achievement?
- HOW: Event study around reform dates, using the apparent randomness of timing, on district finance data and NAEP representative samples (1990-2011). Outcomes are standardised scores (mean 0, SD 1 in first year).
- WHAT: Reforms raise spending in low-income districts sharply and persistently (about $1,200 and $700 per pupil per year in two spending measures, lrs.txt:250). Achievement effects phase in gradually: about 0.1 SD ten years after a reform (about one fifth of the high-low income gap). Implied effect 0.12 to 0.24 SD per $1,000 per pupil per year, "at least twice" the per-dollar effect of the Tennessee STAR class-size experiment (lrs.txt:258-262, footnote 7: about 0.06 SD per $1,000). Equity result (lrs.txt:296-320, :1648): reforms show no measurable effect on the income or race achievement gaps, not because money is unproductive but because low-income students are not concentrated in low-income districts, so district-based transfers are poorly targeted.
- Relevance: Strong for the equity-efficiency trade-off. A district-level allocation model targets districts, not students, and this paper shows how much that loses. Also gives a high-end per-dollar estimate to bracket the credible range.

### 3. Jackson & Mackevicius (2021)
- Citation: C. Kirabo Jackson, Claire Mackevicius. "The Distribution of School Spending Impacts." NBER Working Paper 28517 (Feb 2021, rev. July 2021), https://www.nber.org/papers/w28517, /tmp/lit4/jm.pdf. (I believe a later journal version exists under a different title; not retrieved or verified, so I cite the working paper.)
- Read scope: abstract, introduction, inclusion criteria, headline results, heterogeneity and diminishing-returns discussion, method sections skimmed. Study-by-study tables not read.
- WHY: Individual quasi-experimental studies are hard to compare and to generalise. Quantify the average and the spread of causal spending effects.
- HOW: Meta-analysis of 31 "credibly causal" US K-12 studies (quasi-experimental, spending shift demonstrated, variation shown unrelated to trends). For each study the same marginal parameter is computed: effect of a $1,000 per-pupil increase sustained four years. Precision-weighted method of moments, random-effects heterogeneity, and a meta-regression that tests for and removes study-level bias in ratio-type parameters.
- WHAT: Per $1,000 for four years: +0.0352 SD test scores (about 1.4 percentile points), +1.92 pp high school graduation (2.3 percent relative), +2.65 pp college-going (6.4 percent relative), all p < 0.0001. Heterogeneity explains 76-88 percent of cross-study variation; 90 percent prediction interval for test scores is -0.007 to 0.078 SD, for graduation -0.2 to 4.1 pp (jm.txt:236-246). Capital spending effects take about five years and are about half as large. Effects are somewhat larger for low-income populations (not significant). "Little evidence of diminishing marginal returns at current spending levels" (abstract, jm.txt:61; discussion around jm.txt:303-306). Small publication bias among imprecise studies with minimal effect on pooled estimates. Effects accumulate with years of exposure (jm.txt:762).
- Relevance: Best single source for a credible prior on the coefficient. Note the parameter is a linear marginal effect per dollar, not an elasticity, and the authors find constant effects across baseline spending levels, which is not what a log-log model implies (see synthesis).

### 4. Jackson, Wigger & Xiong (2018/2019)
- Citation: C. Kirabo Jackson, Cora Wigger, Heyu Xiong. "Do School Spending Cuts Matter? Evidence from The Great Recession." NBER Working Paper 24203 (Jan 2018, rev. Aug 2019), https://www.nber.org/papers/w24203, /tmp/lit4/jwx.pdf. (Journal version not retrieved.)
- Read scope: abstract, introduction, instrument description, first-stage and OLS-vs-IV discussion, main results. Heterogeneity and mechanism sections skimmed.
- WHY: Spending cuts in the 2007-09 recession and after; are the effects of cuts symmetric to increases, and are they distinct from the other effects of the recession?
- HOW: State-level panel with NAEP scores and college-going. Instruments: a state's historical reliance on state-collected taxes (more cyclical) interacted with recession timing, plus Bartik-type controls. Event studies and IV; three complementary identification variants.
- WHAT: A $1,000 cut in per-pupil spending (about 8.3 percent of spending, jwx.txt:97) lowers test scores by about 0.045 SD (jwx.txt:153) and college-going by 2.6 to 6.2 pp. Larger test-score effects in poor neighbourhoods. OLS comparison (jwx.txt:595-602): OLS with no controls gives 0.0109 SD per $1,000, falling to 0.00795 with Bartik controls and 0.00465 (not significant) with year fixed effects. IV is therefore about 4 to 10 times the OLS estimate.
- Relevance: Direct evidence on what a district or state fixed-effects OLS panel gives (small, insignificant, attenuated) versus identified IV effects, in the decade right before our 2010-2019 sample. The instrument (state tax reliance x recession) is a candidate for our own panel, though 2010-2019 spans the recovery rather than the cut. [inferred]

### 5. Rothstein & Schanzenbach (2021)
- Citation: Jesse Rothstein, Diane Whitmore Schanzenbach. "Does Money Still Matter? Attainment and Earnings Effects of Post-1990 School Finance Reforms." NBER Working Paper 29177 (Aug 2021), https://www.nber.org/papers/w29177, /tmp/lit4/rs.pdf. (Published later in the Journal of Labor Economics per my recollection; not verified.)
- Read scope: abstract, introduction, main results on attainment and earnings, cost-benefit passage.
- WHY: Follow Card-Krueger and use labour-market outcomes; check whether post-1990 reforms improved attainment and earnings, not only test scores.
- HOW: State-by-cohort panel design using exposure to school finance reforms (SFRs), building on LRS's spending first stage.
- WHAT: Ten years of exposure raises high school graduation by 2.0 pp and some-college by 1.4 pp (rs.txt:563-566); for Black students 3.4 pp and 6.7 pp (rs.txt:569-571); annual earnings rise by $163 per year of exposure, about $2,137 per year after full exposure; benefit-cost ratio about 1.5-to-1 (2.9-to-1 if gains persist to 62) (rs.txt:800-810). Authors note compensatory spending in the old observational work "would bias the estimated effect of school resources downward" (rs.txt:116-118).
- Relevance: Gives graduation-rate effects of a specific funding policy on the same outcome type as our EdFacts graduation rates, plus a cost-benefit anchor for aggregating goals.

### 6. Jackson (2018)
- Citation: C. Kirabo Jackson. "Does School Spending Matter? The New Literature on an Old Question." NBER Working Paper 25368 (Dec 2018), https://www.nber.org/papers/w25368, /tmp/lit4/jack18.pdf.
- Read scope: abstract, introduction, discussion of older literature, summaries of recent studies (Title I, textbooks, capital, school-finance reforms). Skimmed for the rest.
- WHY: Summarise why the older literature (Hanushek 2003 and others) could not support causal claims and what the new quasi-experimental studies show.
- HOW: Narrative review. Argues that Hanushek's 27 percent positive-significant versus 1 percent negative-significant studies are many more positives than chance (jack18.txt:109-128); that controls cannot fix omitted variables and can worsen bias (jack18.txt:143-151); that spending is correlated with property values and family income (jack18.txt:155, :174).
- WHAT: Qualitative: recent credible studies find positive effects, e.g. a 10 percent spending increase raising graduation by 3 or more pp in one cited study (jack18.txt:354) and 3 pp in another (jack18.txt:410). Notes that one textbook-funding result (0.07 SD for a one-time $96.90 per student) is unlikely to generalise because textbook spending may have been inefficiently low (jack18.txt:454-458).
- Relevance: Concise statement of the endogeneity problems a district-panel log-log regression would face, and of why spending type matters.

### 7. Handel & Hanushek (2023)
- Citation: Danielle V. Handel, Eric A. Hanushek. "U.S. School Finance: Resources and Outcomes." NBER Working Paper 30769 (Dec 2022, rev. Feb 2023), https://www.nber.org/papers/w30769; chapter in Handbook of the Economics of Education, DOI 10.1016/bs.hesedu.2023.03.003 (DOI from Crossref, chapter not read). /tmp/lit4/hh.pdf.
- Read scope: abstract, introduction, sections on the education production function and its estimation (hh.txt:570-870), the compilation of quasi-experimental estimates and the generalisation discussion (hh.txt:1291-1620, 2245-2262). Institutional chapters skimmed.
- WHY: Provide the sceptical counterpart to the Jackson-led literature: the new studies identify better, but how resources are used remains the key unknown.
- HOW: Reviews the historical production-function literature (Eq. 1 cumulative levels model; Eq. 2 value-added), then re-compiles 16-plus quasi-experimental spending studies and scales each to the effect of a 10 percent spending increase. Discusses publication bias and generalisation.
- WHAT: Median effect of a 10 percent spending increase on achievement across studies is 0.07 SD, with estimates ranging from -0.244 (not significant) to 0.543 (hh.txt:1440-1444). Pitfalls of the old production-function work: omitted variables correlated with school inputs; cumulative nature of achievement ignored in cross-sections; measurement error from lagged scores; and aggregation, since estimates using state-level resources in cross-state samples are much more likely to be positive and significant, which is consistent with omitted state policy environments (hh.txt:606-666, 758-800). Conclusion: estimates are "conditional upon the institutional and sampling background"; combining them "will depend on the institutional and environmental influences that are held constant" (hh.txt:1608-1622). Spending impacts do not easily generalise to national historical movements in spending (hh.txt:2251).
- Relevance: Authoritative statement of production-function pitfalls and of why one elasticity for all districts is hard to defend. Contains no Cobb-Douglas discussion (searched); its spending metric is percent change, which is elasticity-compatible. [inferred]

---

## B. OR and goal-programming allocation models (read)

None of these estimates the outcome coefficients causally; this is the main gap relative to our plan.

### 8. Hassan, Azmi, Guan & Hoe (2013)
- Citation: Nasruddin Hassan, Dian Farhana Azmi, Tan Sei Guan, Lam Weng Hoe. "A Goal Programming Approach for Library Acquisition Allocation." Applied Mathematical Sciences 7(140), 6977-6981, 2013. DOI 10.12988/ams.2013.310574. Open access PDF read in full (5 pages), /tmp/lit4/hassan13.pdf.
- WHY: Allocate a university library acquisitions budget across 30 subject areas under conflicting objectives.
- HOW: Lexicographic (pre-emptive) linear goal programming. Goals: total spend equals RM 2.13 million (P1), title count within 9,591-11,435 (P2), each subject's share of titles within min/max bounds (P3). Coefficients are average cost per title by subject and min/max shares set by a collection officer's judgement; data from the 2006 UKM Library Annual Report.
- WHAT: A feasible allocation meeting the five goals; no outcome model, no estimation, no sensitivity analysis. Hypothetical budget.
- Relevance: Template for the GP skeleton (deviation variables, priorities) we would cite. Contrast: coefficients are accounting averages, not learned effects, and bounds are judgemental.

### 9. Hassan (2017)
- Citation: Nasruddin Hassan. "Student Enrollment Allocation into Academic Departments Using Weighted Goal Programming." Proceedings of the 3rd International Seminar of Basic Sciences, Pattimura University, 2017, pp. 25-34. Open-access PDF read (10 pages), /tmp/lit4/hassan17.pdf. (No DOI retrieved; URL from the OJS article page https://ojs3.unpatti.ac.id/index.php/pcst/article/download/1513/1189.)
- WHY: Distribute first-year students across five departments subject to capacity, financial allocation, instructor numbers and affirmative-action quotas.
- HOW: Weighted non-pre-emptive GP. Goals on first-year capacity, total enrolment, native-student quota, student-faculty ratio and budget. Department cost is linear in enrolment with cost-per-student alphas (397, 1298, 666, 140, 966), data from the Faculty of Science and Technology, UKM. Goal weights k_ij take values 1-5 and are stated without a derivation (paper eqs. 15-16).
- WHAT: Feasible enrolment plan meeting the constraints. No social-outcome production function.
- Relevance: Shows the weighting convention (integer 1-5) and an affirmative-action (equity) goal inside a GP, to compare with our weights-from-data approach.

### 10. Sihombing (2023)
- Citation: Dame Ifa Sihombing. "Optimization on the Budgeting Allocation with Goal Programming in Departmen Mathematic Education Universitas HKBP Nommensen." ZERO: Jurnal Sains, Matematika dan Terapan 7(2), 141-146, Dec 2023. DOI 10.30829/zero.v7i2.19218. Open access PDF read (6 pages), /tmp/lit4/sih.pdf.
- WHY: Improve use of funds in a department of a private university with conflicting financial goals.
- HOW: Pre-emptive GP solved with LINGO on 2019-2022 budget estimates, five prioritised goals (personnel cost, overhead, capital expenditure, internal revenue, total budget).
- WHAT: Optimal deviation Z = 4.24; goals 1, 3 and 5 met, goals 2 (overhead) and 4 (revenue) not met.
- Relevance: Illustrates the most common education-budget GP in the applied literature: goals are budget lines, not student outcomes. This is exactly what an outcome-goal, data-learned GP would improve on. Small single-unit case, weak validation.

### 11. Namazi & Khodabakhshi (2023)
- Citation: Atieh Namazi, Mohammad Khodabakhshi. "A fair-biased allocation of investment between economic sectors using social accounting matrix multiplier analysis." Accounting 9, 191-202, 2023. DOI 10.5267/j.ac.2023.2.001. Open access PDF read (675 lines extracted), /tmp/lit4/nam.pdf.
- WHY: Allocate an investment budget among economic sectors to raise output, employment, income distribution.
- HOW: SAM multipliers (linear responses of output, employment, value added, government income, import needs, urban-rural income ratio to a unit of investment in each sector) are used as DEA inputs/outputs; a DEA-based fair revenue-allocation rule sets sector quotas; a "fair-biased" variant improves on it. Iran SAM.
- WHAT: The improved rule yields about 1.13 million jobs and 3.7 percent extra growth (conclusion, section 6).
- Relevance: A data-driven allocation where coefficients come from an estimated linear multiplier matrix. Closest in spirit to "coefficients learned from data", but multipliers are accounting-based, not causal or elasticity-based, and DEA is a different allocation mechanism from GP.

### 12. Sharify (2021) — abstract only
- Citation: Nooraddin Sharify. "Economic resources' allocation: A goal programming model integrated with a social accounting matrix." Soft Computing, 2021. DOI 10.1007/s00500-021-05746-w. Read scope: Crossref/publisher abstract only (full text paywalled; saved HTML in /tmp/lit4/sharify.pdf is the landing page).
- WHY/HOW/WHAT (from abstract only): GP integrated with a SAM (instead of input-output) to allocate economic resources among sectors for a province (Golestan, Iran). Goals: supply-demand balance and gross regional product, employment by educational group of workers, and income-distribution inequality. The abstract claims SAM-GP improves on I-O-GP.
- Relevance: Multi-goal GP with an inequality goal and coefficients from an empirical matrix; cite as an OR precedent. Cannot assess details beyond the abstract.

---

## C. Papers identified but not read (metadata or abstract only; DOIs confirmed through Crossref or Semantic Scholar)

Paywalled or unretrieved (important to obtain):
- Hyman, J. (2017) "Does Money Matter in the Long Run? Effects of School Spending on Educational Attainment." AEJ: Economic Policy. DOI 10.1257/pol.20150249. (AEA PDF returned HTML.)
- Candelaria, C., Shores, K. (2019) "Court-Ordered Finance Reforms in the Adequacy Era: Heterogeneous Causal Effects and Sensitivity." Education Finance and Policy. DOI 10.1162/edfp_a_00236.
- Kreisman, D., Steinberg, M. (2019) "The effect of increased funding on student achievement: Evidence from Texas's small district adjustment." Journal of Public Economics. DOI 10.1016/j.jpubeco.2019.04.003.
- Baron, E.J. (2022) "School Spending and Student Outcomes: Evidence from Revenue Limit Elections in Wisconsin." AEJ: Economic Policy. DOI 10.1257/pol.20200226.
- Brunner, E., Hyman, J., Ju, A. (2020) "School Finance Reforms, Teachers' Unions, and the Allocation of School Resources." Review of Economics and Statistics. DOI 10.1162/rest_a_00828.
- Page, M.E. et al. (2024) "New Advances on an Old Question: Does Money Matter for Children's Outcomes?" Journal of Economic Literature. DOI 10.1257/jel.20231553 (author list not checked).
- Todd, P., Wolpin, K. (2003) "On the Specification and Estimation of the Production Function for Cognitive Achievement." Economic Journal. DOI 10.1111/1468-0297.00097 (production-function pitfalls; discussed second-hand in Handel & Hanushek, hh.txt:16 footnote).
- Gigliotti, P., Sorensen, L. (2018) "Educational resources and student achievement: Evidence from the Save Harmless provision in New York." Economics of Education Review. DOI 10.1016/j.econedurev.2018.08.004.
- Tamiz, M., Jones, D., Romero, C. (1998) "Goal programming for decision making: An overview of the current state-of-the-art." European Journal of Operational Research. DOI 10.1016/S0377-2217(97)00317-2. (Must cite for GP methodology.)
- Min, H. (1988) "Three-phase hierarchical allocation of university resources via interactive fuzzy goal programming." Socio-Economic Planning Sciences. DOI 10.1016/0038-0121(88)90040-7.
- Papageorgiou, J. (1978) "A goal programming model for resource allocation in the school system of Greece." Kybernetes. DOI 10.1108/eb005487.
- Tingley, G. (1984) "A Goal Programming Example in Public Health Resource Allocation." Management Science. DOI 10.1287/mnsc.30.3.279.
- Ghernouk et al. (2026) "Educational Spending Efficiency: A Comparative Analysis Using Data Envelopment Analysis and Malmquist..." Economies. DOI 10.3390/economies14040110 (MDPI PDF blocked).

Cited inside papers I read but never retrieved (so not cited as sources here): Hanushek (2003, Economic Journal) and Hanushek (1997); Card & Krueger (1992a,b); Hanushek, Rivkin & Taylor (1996); Charnes & Cooper (goal programming origin, cited in hassan13.txt). I tried NBER w5006 for Card-Krueger; the scan is unreadable, so it is not confirmed.

---

## D. Synthesis

### (a) What effect sizes are credible, and how they compare with naive panel regressions

Credible range from quasi-experimental studies (all read):
- Test scores: 0.035 SD per $1,000 for four years pooled (Jackson & Mackevicius, #3); 0.045 SD per $1,000 (Jackson-Wigger-Xiong, #4); up to 0.12-0.24 SD per $1,000 for low-income districts in post-1990 reforms (LRS, #2); median 0.07 SD per 10 percent spending increase in the Handel-Hanushek compilation, with a range of -0.24 to 0.54 SD (#7). The 90 percent prediction interval for a new setting is -0.007 to 0.078 SD per $1,000 (#3).
- Graduation: +1.92 pp per $1,000 (#3), which is about 2.3 percent relative, so roughly +2.3 pp per 10 percent spending (using $1,000 about 8.3 percent of spending from #4, jwx.txt:97). Ten years of reform exposure gives +2.0 pp (#5). Taking a base graduation rate of about 83 percent (implied by #3), the implied elasticity of the graduation rate with respect to spending is on the order of 0.25-0.30. [inferred; my arithmetic, not an author-reported elasticity]
- Adult outcomes: 10 percent more spending for 12 years gives +0.27 years of schooling, +7 percent wages (#1).

Naive panel regressions:
- Cross-section OLS is biased upward because richer areas spend more (#1, #6). Within-district OLS is biased downward by compensatory spending: JJP find a significantly negative association between within-district spending changes and predicted outcomes (jjp.txt:653-672), and Rothstein-Schanzenbach make the same point (rs.txt:116-118).
- Quantified: the state-level OLS of Jackson-Wigger-Xiong gives 0.0109 SD per $1,000 with no controls and an insignificant 0.0047 with year fixed effects, against IV of 0.045-0.05 (jwx.txt:595-602). So fixed-effects OLS under-states causal effects by a large factor in this setting.
- Handel-Hanushek (#7) add that the historical cross-state production-function estimates were more positive when state-level resources were used, consistent with omitted state policy (hh.txt:758-800). The sign of the bias therefore depends on the variation used.

### (b) Is the planned design defensible?

Defensible as a descriptive or calibration exercise with prior-informed coefficients; not defensible as causal elasticities estimated by district fixed effects alone.
- What is defensible: the district panel is large and recent; log-spending specifications are used by JJP; effects are positive and roughly of the sizes above, so a log-log form with elasticities of order 0.1-0.3 for graduation is in the credible range. [inferred]
- What it lacks (identification):
  1. No exogenous spending shifter. Within-district variation in 2010-2019 is largely compensatory and cyclical (#1, #4). Candidates not yet checked in the data: state tax reliance x recession (#4), state formula changes and finance-reform timing (#1, #2, #5). [inferred which are usable in 2010-2019]
  2. Timing. Effects accumulate with years of exposure (jm.txt:762; JJP use 12-year average spending; RS use years of exposure). A contemporaneous log-log regression of graduation on current spending misspecifies the dynamic. A lag structure or cumulative spending is needed, and graduation-rate data begin in 2011 so long lags are truncated. [inferred]
  3. Functional form. Jackson & Mackevicius find "little evidence of diminishing marginal returns" and effects roughly constant per dollar across baseline spending (jm.txt:61, 303-306), whereas a Cobb-Douglas form implies marginal return proportional to y/x, which falls as spending rises. The log-log elasticity also imposes the same elasticity in all districts. Heterogeneity across studies is 76-88 percent of variance (#3) and effects are larger for poor districts (#1, #2, #4). So elasticities should be allowed to vary by district poverty, or a linear-in-dollars form tested as an alternative. [inferred for the comparison of forms]
  4. Outcome. EdFacts graduation rates are reported in ranges (midpoint used, per the data README), which adds measurement error, and rates near the ceiling make the log form implausible. A logit or the log of the non-graduation rate is a possible alternative. [inferred]
  5. Spending type. Effects differ by spending type: capital spending is about half as large and slower (#3); a textbook-only study is hard to generalise (#6). Total current expenditure mixes categories. [inferred for implications on our data]
  6. Scope. Findings are conditional on institutions and settings (#7, hh.txt:1608-1622), and district allocation reaches low-income students imperfectly (#2).

### (c) Existing OR allocation models to cite and compare with

From what was retrieved: Hassan et al. 2013 (library funds, lexicographic GP, #8); Hassan 2017 (student enrolment, weighted GP with an affirmative-action goal, #9); Sihombing 2023 (university department budget GP, #10); Namazi & Khodabakhshi 2023 (SAM multipliers + DEA fair allocation, #11); Sharify 2021 (GP + SAM with inequality goal, abstract only, #12). Common features: goals are budget lines, capacities or accounting multipliers; weights/priorities are judgemental; no causal estimation of coefficients; no uncertainty in the coefficients; evaluation on a single unit or a hypothetical. Still to obtain for the methods section: Tamiz-Jones-Romero (1998) as the GP survey; Min (1988) and Papageorgiou (1978) as education-specific GP precedents (all paywalled, metadata only).

Our contribution relative to these: coefficients from an econometric outcome model with identification and uncertainty (credible prior from #3), outcome-based rather than budget-line goals, and an explicit equity goal informed by #2. [inferred positioning]

### (d) Gaps

Author-stated:
- Spending effects depend on how money is used and mechanisms are not identified: "the research has not been successful at identifying mechanisms underlying successful use of resources or for ascertaining when added school investments are likely to be well-used" (Handel & Hanushek, abstract, hh.txt:55).
- Generalisation: estimates are conditional on institutional setting (hh.txt:1608-1622); Jackson & Mackevicius estimate heterogeneity (76-88 percent of variance) precisely because of this (jm.txt:72).
- Publication bias remains a caveat for compilations (hh.txt:1084); small bias among imprecise studies in #3.
- Targeting: district-level reforms do not reach low-income students well (lrs.txt:1648-1656).
- Definitions of low-income vary across studies and bias heterogeneity comparisons (jm.txt:2270-2275).

Own inferences [inferred]:
- No paper retrieved uses a Cobb-Douglas or log-log education production function for allocation; the log form appears only as a regressor (JJP). Elasticities from the quasi-experimental literature must be derived by us from per-$1,000 or per-10-percent estimates.
- No retrieved OR paper links GP coefficients to causal estimates, uses graduation or test outcomes as goals, or propagates coefficient uncertainty.
- The within-district fixed-effects panel for 2010-2019 has no tested instrument; whether state formula changes or tax-reliance shifts in that decade have a usable first stage is untested.
- Jackson & Mackevicius' working-paper version was retrieved; its marginal-effect parameter is linear per dollar, and the meta-analysis does not report elasticities.

Limits of this review: 12 papers actually read (7 causal-evidence papers in full or near full, 4 OR papers in full, 1 abstract only). The target of 10-14 is met, but several important published papers (Hyman, Candelaria-Shores, Kreisman-Steinberg, Baron, Todd-Wolpin, Tamiz et al.) are metadata only.
