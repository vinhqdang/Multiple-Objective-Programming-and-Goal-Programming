# 07. Revealed social preferences in economics and school-finance allocation

Cluster C of the literature review for "inverse goal programming for public budgets". Date of retrieval: 2026-11-22. All texts were downloaded to /tmp/litC/ and converted with pdftotext -layout. "Read scope" says what was actually read. Where I only saw an abstract I say so and the paper is not used for any claim beyond the abstract. Statements marked [inferred] are my own reasoning, not the authors'.

Papers read (18): Behrman & Craig 1987; Bourguignon & Spadaro (working paper version of the 2012 article); Bargain et al. (IZA DP 7215); Saez & Stantcheva 2016; Hendren 2020; Lockwood & Weinzierl 2016; Capozza & Srinivasan 2026; Hendren & Sprung-Keyser 2020 (abstract only); Fernandez & Rogerson 1992; Poterba 1996/1997; Lafortune, Rothstein & Schanzenbach 2018; Jackson, Johnson & Persico (2014 working paper, 2016 QJE); Jackson, Wigger & Xiong 2018/2021 (abstract and introduction only); Shores, Candelaria & Kabourek (2019 and 2021 versions); Baker et al. National Report Card; Chingos & Blagg 2017; Calabrese, Epple & Romano 2024.

The data we hold (docs: data/us_districts/README.md) are US district panels 2010-2019 from the Urban Institute Education Data Portal (NCES CCD finance and enrollment, EdFacts graduation rates). Relevance notes below refer to that.

---

## A. Revealed preferences from the allocation of public services

### A1. Behrman & Craig 1987
- Citation: Jere R. Behrman and Steven G. Craig (1987), "The Distribution of Public Services: An Exploration of Local Governmental Preferences", American Economic Review 77(1): 37-49. JSTOR stable URL http://www.jstor.org/stable/1806727 (no Crossref DOI found). Read from a copy hosted at uh.edu/~bsorense/BehrmanCraig1987.pdf.
- Read scope: full text of pp. 37-46 (abstract, model, functional forms, data, Tables 1-3, discussion of results); the appendix and last pages were skimmed only.
- WHY: Earlier work (surveyed by Gramlich & Rubinfeld 1982) tested only whether spending is pro-poor or pro-rich. The authors argue expenditure is an input, and what governments care about is the service outcome, so the pro-poor input pattern cannot reveal distributional concern (p. 38 lists three scenarios giving the same input pattern).
- HOW: The local government acts "as if" it maximises a welfare function W(S,N) over neighbourhood outcomes S_j subject to a resource constraint and a production constraint S_j = f(P_j, X_j), where X_j are fixed neighbourhood characteristics. The first-order conditions equate the marginal rate of substitution along the iso-welfare curve to the marginal rate of transformation along the production frontier. Two parametric welfare functions: Kolm-Pollak (absolute inequality aversion) and CES (relative). Equation (9) is estimated by instrumental variables (the allocation and the outcome are simultaneous).
- WHAT: Preference parameters inferred are (i) q, an inequality-aversion parameter (equity-productivity trade-off), and (ii) neighbourhood weights a_j ("unequal concern") made functions of neighbourhood characteristics. Identification comes from variation in marginal products across neighbourhoods induced by different X_j: the production function pins down the frontier, and where the observed allocation sits on it traces out the iso-welfare curve (Fig. 1, pp. 40-41). Footnote 18 and p. 42 note that levels of the weights are not separately identified from constants and the production elasticity. Data: 79 police beats in Baltimore, fiscal 1972, survey-reported and officially reported crime, police patrols per capita. Result (Table 3): q about -4.0 (KP, equal concern), substantial inequality aversion but a remaining trade-off; weights fall with neighbourhood income and with the share over 65, race not significant; KP fits better than CES. The government responds to officially reported crime, not survey-reported crime (Table 2).
- Relevance to us: This is the closest ancestor of what we want: an "as if" welfare function with an equity parameter and group weights, estimated from an allocation, with the production side explicit. An inverse GP approach would differ by (a) replacing smooth welfare with goal targets and deviation penalties (weights and targets rather than curvature), (b) allowing several outcomes with priorities. But the identification logic (needs an explicit outcome production function; weights are only identified relative to it) carries over unchanged. It is a single cross-section of one city and one service, which is also what we have per state-year [inferred].

### A2. Bourguignon & Spadaro (published 2012)
- Citation: François Bourguignon and Amedeo Spadaro (2012), "Tax-benefit revealed social preferences", Journal of Economic Inequality 10(1): 75-108, DOI 10.1007/s10888-010-9153-0 (published version paywalled). Read: EUROMOD Working Paper EM9/08 (Oct 2008), https://www.iser.essex.ac.uk/research/publications/working-papers/euromod/em9-08.pdf, which the authors describe as a revised version of PSE WP 2005-22.
- Read scope: abstract, introduction, model and optimal-inverse derivation (up to eq. 6 and Proposition 1 on Paretianity), conclusion; empirical section on France skimmed.
- WHY: Standard applied optimal-tax work picks a social welfare function and computes the optimal schedule; results are very sensitive to that choice. They invert the problem and ask what welfare function would make the observed schedule optimal, and whether it is concave and Paretian.
- HOW: Mirrlees/Saez optimal-income-tax first-order condition: the left side involves the social welfare derivative G'(V(w)); the right side involves the observed marginal tax rate, labour-supply elasticity and ability density. With the elasticity and density estimated, the condition is solved for the marginal social welfare weights. Participation margin added (Saez 2002 style).
- WHAT: Inferred object: the marginal social welfare weight schedule G'(V) along the income (ability) distribution. Identification: assumes the observed schedule is optimal; needs an estimate of labour-supply elasticities and the ability distribution. Data: French fiscal data and EUROMOD microsimulation. Result: with low elasticities the revealed weights are positive and decreasing; with elasticities near those for secondary workers the weights turn negative at the top (non-Paretian). Authors conclude (Section 7) that the authority either assumes low behavioural response, has non-Paretian preferences, or does not optimise (political-economy forces).
- Relevance: Template for "inverse optimum". Key differences from our problem: the fiscal side has a rich first-order condition tied to a behavioural elasticity; public school spending has no analogous elasticity, and the "weights" must be tied to an outcome production function as in A1 [inferred].

### A3. Bargain, Dolls, Neumann, Peichl & Siegloch (IZA DP 7215)
- Citation: Olivier Bargain, Mathias Dolls, Dirk Neumann, Andreas Peichl, Sebastian Siegloch, "Comparing Inequality Aversion across Countries When Labor Supply Responses Differ", IZA Discussion Paper 7215, February 2013, https://docs.iza.org/dp7215.pdf. A related published version exists: "Tax-Benefit Revealed Social Preferences in Europe and the US", Annals of Economics and Statistics 113/114 (2014) 257-289, DOI 10.15609/annaeconstat2009.113-114.257 (not retrieved; I did not verify that its text equals the IZA paper).
- Read scope: abstract, introduction, identification discussion, results summary, conclusion; labour-supply estimation skimmed.
- WHY: Cross-country comparisons of revealed inequality aversion had used uniform elasticities; differences in behavioural response could distort the ranking.
- HOW: Estimate extensive and intensive labour-supply elasticities for 17 EU countries and the US on the same microdata (EUROMOD, TAXSIM), then invert the optimal tax condition to retrieve a social inequality-aversion parameter per country.
- WHAT: Inferred: a single inequality-aversion parameter per country (welfare function with constant inequality aversion). Identification: "the key identifying assumption is that the social planner optimally chooses taxes ... such that the resulting income distribution ... corresponds to the planner's redistributive preferences" (their discussion of eq. 1). Findings: three groups; Nordic and some Continental countries near Rawlsian, Southern Europe and the US near utilitarian; if behavioural response is set to zero the differences shrink. Authors' stated limit: only direct taxes and transfers considered, "non-cash benefits and public goods" left out; political economy suggested as an extension (conclusion).
- Relevance: Shows that the inferred preference parameter moves a lot with the assumed behavioural responses (an identification pitfall). For us it supports reporting inferred priorities as sets or bands rather than point estimates [inferred]. They explicitly flag that public goods and in-kind spending (our case) are not covered.

### A4. Saez & Stantcheva 2016
- Citation: Emmanuel Saez and Stefanie Stantcheva (2016), "Generalized Social Marginal Welfare Weights for Optimal Tax Theory", American Economic Review 106(1): 24-45, DOI 10.1257/aer.20141362. Read: NBER WP 18835 (revised July 2015).
- Read scope: abstract, introduction, Section I framework, discussion of reverse-engineering, online appendix C on survey elicitation; the specific application sections skimmed.
- WHY: Welfarist utilitarian weights tie the weights to concave utility; actual policy and public views also reflect libertarian, equality-of-opportunity and poverty-alleviation views.
- HOW: The primitive is a set of generalised social marginal welfare weights, not a social welfare function. A tax system is locally optimal if no small budget-neutral reform has positive weighted sum of money-metric gains and losses. Weights can depend on income, taxes paid, characteristics outside utility.
- WHAT: Inferred object (in their appendix C): the weights themselves, either reverse-engineered from the current system (they cite Christiansen & Jansen 1978, Bourguignon & Spadaro 2012, Zoutman et al.) or elicited by survey (about 1,100 MTurk respondents, December 2012). Identification of the weights is not the paper's aim; it is a normative-framework paper. Authors note the approach is local (cannot rank two local optima) and that they "take society's preferences as given and do not analyze how they could arise through the political process" (footnote 1).
- Relevance: Gives the modelling language for a goal-programming reading: weights on groups are decision-maker parameters, not utility derivatives, and can attach to characteristics such as being a disadvantaged student. It supports our framing that "priorities" are not welfare in the utilitarian sense [inferred].

### A5. Hendren 2020
- Citation: Nathaniel Hendren (2020), "Measuring economic efficiency using inverse-optimum weights", Journal of Public Economics 187: 104198, DOI 10.1016/j.jpubeco.2020.104198. Read: NBER WP 20351 (revised April 2020).
- Read scope: abstract, introduction, assumptions and propositions (headings and Prop. 2), results on weights, Section 8 limitations; proofs not read.
- WHY: Kaldor-Hicks efficiency ignores that redistribution is costly; weighting surplus requires interpersonal comparison, which depends on ethical choices.
- HOW: The weight at income y is the marginal cost to the government of giving $1 to people near y, g(y), which equals the inverse-optimum weight that would rationalise the status quo tax schedule. Estimated from the joint distribution of income and marginal tax rates in the universe of 2012 US tax returns plus taxable-income elasticities (bounds first, then point estimates).
- WHAT: Inferred: g(y), about 1.15 at the bottom and 0.65 at the top, a ratio of about 1.77 (poor weighted 1.5-2 times the rich). Identification: the status quo is assumed optimal; the weights are driven by the local Pareto parameter and elasticities; bounds hold regardless of the elasticity. Authors' limits (Section 8): no general-equilibrium response to tax changes; weights "are not structural parameters. They are endogenous to the economic environment", and weights from one country should not be transplanted to another (France gives near zero at the top).
- Relevance: Most relevant for us conceptually: the weights are the dual (shadow prices) of the status-quo optimum. An inverse GP approach computes duals of an assumed program. This literature has already insisted the result is conditional on assumed behavioural parameters, so any inverse-GP claim should be framed the same way [inferred].

### A6. Lockwood & Weinzierl 2016
- Citation: Benjamin B. Lockwood and Matthew C. Weinzierl (2016), "Positive and normative judgments implicit in U.S. tax policy, and the costs of unequal growth and recessions", Journal of Monetary Economics 77: 30-47, DOI 10.1016/j.jmoneco.2015.10.006. Read: NBER WP 21927 (January 2016).
- Read scope: abstract, introduction (all), discussion of limitations and trilemma; data section and appendices skimmed.
- WHY: To test whether inverse-optimum weights can serve as a normative benchmark.
- HOW: Inverse-optimum inference on US federal tax policy 1979-2010 using CBO income distributions and conventional optimal-tax conditions.
- WHAT: Inferred: marginal social welfare weights by income and year, and implied perceived elasticity of taxable income. Result: rates on high earners are much lower than conventional optimal-tax analysis recommends; weights differ greatly before and after the 1986 reform. Authors state a trilemma: at most two of (a) the inference yields normatively relevant weights, (b) perceived elasticities lie in conventional ranges, (c) true weights satisfy conventional principles can hold. They conclude existing data "are simply insufficient to identify the true explanation".
- Relevance: A direct warning for us: revealed weights confound preferences, beliefs about response, and political-economy distortions. We should not label recovered weights "the state's values" without further structure [inferred].

### A7. Capozza & Srinivasan 2026
- Citation: Francesco Capozza and Krishna Srinivasan (18 September 2026), "Who Should Get Money? Estimating Welfare Weights in the U.S.", working paper, https://krishnasrini.com/papers/welfare_weights.pdf (pre-registered, N about 2,000; no journal DOI found).
- Read scope: abstract and introduction; elicitation design skimmed.
- WHY: Weights are usually imposed or inferred from policy; policy-implied weights may conflate normative judgments with political-economy forces (their footnote 1 cites Stantcheva 2016 and Lockwood & Weinzierl 2016).
- HOW: Incentivised experiment: "Social Architects" redistribute money between pairs of recipients with real disposable incomes; choices identify weights.
- WHAT: Inferred: income elasticity of welfare weights, between -0.85 and -0.71; the elicited weights are 8-9 times as progressive as those implied by the US tax schedule and 4-5 times as progressive as those implied by tax and transfer policies.
- Relevance: Gives a stated-preference benchmark against which revealed weights from allocations could be compared. It also shows a large gap between stated and revealed progressivity, which is the object an inverse method would quantify for school funding [inferred].

### A8. Hendren & Sprung-Keyser 2020 (abstract only)
- Citation: Nathaniel Hendren and Ben Sprung-Keyser (2020), "A Unified Welfare Analysis of Government Policies", Quarterly Journal of Economics 135(3), DOI 10.1093/qje/qjaa006; NBER WP 26144.
- Read scope: abstract and the first page only (the text layer of the downloaded PDF is garbled after the front matter). Do not rely on more than the abstract.
- Abstract content used: 133 policies; MVPF = willingness to pay over net government cost; direct investment in low-income children's health and education has highest MVPFs (above 5 on average); many such policies pay for themselves.
- Relevance: gives the "efficiency side" (value per dollar by target group) that must be paired with revealed weights to say whether an allocation is consistent with a welfare-maximising planner. If MVPF of education spending on poor children is above 5 and allocations still show only modest progressivity, that gap is a candidate "revealed weight" [inferred].

---

## B. School finance: what formulas and reforms reveal

### B1. Baker, Farrie, Johnson, Luhm & Sciarra (National Report Card, 6th ed.)
- Citation: Bruce Baker, Danielle Farrie, Monete Johnson, Theresa Luhm, David G. Sciarra (January 2017), "Is School Funding Fair? A National Report Card", 6th edition, Education Law Center, https://edlawcenter.org/assets/files/pdfs/School%20Funding/NRC_VI_Final.pdf.
- Read scope: major findings, fairness-measure definitions, Appendix A methodology; state-by-state tables skimmed.
- WHY: Provide a comparative grade of state school finance systems.
- HOW: Four indicators: funding level (regression-predicted state-and-local revenue per pupil at 20% poverty, controlling for regional wages, size, density), funding distribution (ratio of predicted funding at 30% poverty to 0% poverty within each state), effort (state spending over GDP), coverage (share of children in public schools). Data: Census F-33 and SAIPE poverty.
- WHAT: No preference parameter is inferred; the progressivity ratio is a descriptive statistic. Finding for 2014 data: 12 states progressive, 15 flat, 21 regressive (21 up from 14).
- Relevance: Defines the standard "fairness" statistic against which an inferred weight on poor students should be compared. The scale (0% to 30% poverty) is also the kind of normative benchmark an inverse GP model could replace with an inferred target [inferred]. Note the report states it does not benchmark against an adequacy target ("States are not evaluated using specific thresholds").

### B2. Chingos & Blagg 2017
- Citation: Matthew M. Chingos and Kristin Blagg (June 2017), "Do Poor Kids Get Their Fair Share of School Funding?", Urban Institute brief, https://www.urban.org/research/publication/do-poor-kids-get-their-fair-share-school-funding (PDF: https://www.urban.org/sites/default/files/publication/90586/school_funding_brief_1.pdf).
- Read scope: the first 7 of the report's pages (introduction, measure, comparison with existing measures, Maryland example); state ranking tables not read in detail.
- WHY: Regression-based progressivity measures are sensitive to specification, especially in states with few districts.
- HOW: Progressivity = enrolment-weighted mean per-pupil funding in the districts of poor students minus the same for non-poor students; funding from F-33, poverty from SAIPE, cost-adjusted with local non-teacher college-graduate wages.
- WHAT: No preference parameter. Findings: 35 states have a poverty weight in the formula, but many states with progressive formulas on paper are not progressive in practice because local funding is regressive and poor students are sorted into districts. Their measure correlates r = 0.77 with Baker et al. 2017; revenue-based and spending-based versions correlate r = 0.89 (0.76 excluding Alaska).
- Relevance: This is our same data source family (F-33, SAIPE, CCD). It supplies a ready, transparent statistic for the target "priority on poor students" that an inverse model can be calibrated to. It also shows a decomposition we must model: formula (state) versus local revenue [inferred].

### B3. Lafortune, Rothstein & Schanzenbach 2018
- Citation: Julien Lafortune, Jesse Rothstein, Diane Whitmore Schanzenbach (2018), "School Finance Reform and the Distribution of Student Achievement", American Economic Journal: Applied Economics 10(2): 1-26, DOI 10.1257/app.20160567. Read: NBER WP 22011.
- Read scope: abstract and introduction (about 8 pages); event study specification and tables skimmed.
- WHY: Evidence on adequacy-era (post-1990) reforms was missing.
- HOW: Event study exploiting the timing of reforms, with NAEP data to build a state-year panel of relative achievement in low-income districts.
- WHAT: Reforms raise state revenue in all districts, more in low-income districts: about +$1,200 absolute and +$700 relative per pupil per year; achievement rises about 0.1 SD ten years after; implied 0.12-0.24 SD per $1,000. Footnote 6 reports that legislators facing court orders to raise funding for poor districts "often respond by increasing overall funding, as a way of disguising the resulting redistribution".
- Relevance: Effect sizes are the production side that an inverse model needs, and the footnote is direct evidence that the observed allocation is a political compromise (level and distribution move together), which complicates inference of weights from one cross-section [inferred].

### B4. Jackson, Johnson & Persico
- Citations: C. Kirabo Jackson, Rucker Johnson, Claudia Persico (2016), "The Effects of School Spending on Educational and Economic Outcomes: Evidence from School Finance Reforms", Quarterly Journal of Economics 131(1): 157-218, DOI 10.1093/qje/qjv036 (NBER WP 20847, retrieved). Also NBER WP 20118 (May/August 2014), "The Effect of School Finance Reforms on the Distribution of Spending, Academic Achievement, and Adult Outcomes", retrieved.
- Read scope: WP 20118 abstract and the first pages of the introduction; WP 20847 abstract only.
- WHY/HOW: Event-study of court-ordered reforms and their funding-formula type on spending of low- versus high-income districts, then link to adult outcomes in the PSID.
- WHAT: All reforms reduce spending inequality, but equity-based reforms reduce variance with little effect on level, adequacy-based raise overall spending, and the "tax price" of the formula matters (WP 20118 abstract). A 10% increase in per-pupil spending for 12 years gives 0.27 more years of education, 7.25% higher wages, and 3.67 percentage point lower adult poverty, with larger effects for poor children (WP 20847 abstract).
- Relevance: Reform type (equity versus adequacy) is itself a coarse revealed-priority label. The formula "tax price" is a parameter we can read as the price of the equity goal [inferred].

### B5. Jackson, Wigger & Xiong 2021
- Citation: C. Kirabo Jackson, Cora Wigger, Heyu Xiong (2021), "Do School Spending Cuts Matter? Evidence from the Great Recession", American Economic Journal: Economic Policy 13(2): 304-335, DOI 10.1257/pol.20180674. Read: NBER WP 24203 (January 2018).
- Read scope: abstract and the opening of the introduction only.
- WHAT: National spending fell by roughly 7% in the Great Recession; instrumenting with states' historical reliance on state taxes finds cuts lowered test scores and college-going, more for children in poor neighbourhoods.
- Relevance: Identification of exogenous budget shocks via the revenue mix (the 2010-2019 window of our data covers the recovery). Instrument idea can separate preference from capacity in revealed allocation [inferred]. Not read beyond the abstract, so I cannot say how they treat how states distributed the cuts.

### B6. Shores, Candelaria & Kabourek
- Citation: Kenneth A. Shores, Christopher A. Candelaria, Sarah E. Kabourek (2023), "Spending More on the Poor? A Comprehensive Summary of State-Specific Responses to School Finance Reforms from 1990-2014", Education Finance and Policy 18(3): 395-422, DOI 10.1162/edfp_a_00360. Read: EdWorkingPaper 19-52 v2 (https://www.edworkingpapers.com/sites/default/files/ai19-52_v2.pdf) and the July 2021 manuscript (https://www.edworkingpapers.com/sites/default/files/Manuscript_SchFinHet_R04_webpost_20210701.pdf).
- Read scope: abstract, introduction, conclusion; methods (augmented synthetic control) skimmed.
- WHY: National averages hide state heterogeneity in how reforms changed resource allocation.
- HOW: Augmented synthetic control for each state and district income tercile (66-67 reforms, 26 states), then descriptive regressions of effect sizes on formula features, multiple reforms, union strength.
- WHAT: Average spending effect +6% in low-income and +1% in high-income districts, but across low-income districts 2 of 26 reforms lowered spending and 14 states saw no change; formula components and union strength predict effect sizes. Low-income districts spent more on capital than on salaries.
- Relevance: A state-by-state heterogeneity result: states do not share one equity weight. That supports estimating state-level priority parameters, and shows the policy levers (formula weights) are observable inputs for the inverse step [inferred].
- Not read: Candelaria & Shores (2019), "Court-ordered finance reforms in the adequacy era: heterogeneous causal effects and sensitivity", Education Finance and Policy 14(1): 31-60, DOI 10.1162/edfp_a_00236 (existence confirmed on Crossref; text not retrieved).

---

## C. Political economy of education spending with explicit preferences

### C1. Poterba 1996/1997
- Citation: James M. Poterba (1997), "Demographic Structure and the Political Economy of Public Education", Journal of Policy Analysis and Management 16(1): 48-66, DOI 10.1002/(SICI)1520-6688(199724)16:1<48::AID-PAM3>3.0.CO;2-I. Read: NBER WP 5677 (July 1996).
- Read scope: abstract, introduction, results discussion for Table 3 and the circuit-breaker extension, conclusions; data section skimmed.
- WHY/HOW: State panel 1961-1991: regress log per-child education spending on elderly share, school-age share, income, poverty, urban share, race measures, with state and year fixed effects, to test generational competition.
- WHAT: Elasticity of per-child spending with respect to the over-65 share about -0.25 with state and time effects, larger when elderly and children are from different racial groups. The preference-like quantity is reduced-form, not a welfare weight. The author states the circuit-breaker results have standard errors as large as the coefficients and "warrant further study" (Section 3 end).
- Relevance: A cautionary baseline: demographic determinants of spending level explain part of the allocation, so any inverse model must control for voter composition or accept that the "weights" include electoral power [inferred].

### C2. Fernandez & Rogerson 1992
- Citation: Raquel Fernandez and Richard Rogerson (1992), "Income Distribution, Communities and the Quality of Public Education: A Policy Analysis", NBER Working Paper 4158, DOI 10.3386/w4158. (A later version appeared as Fernandez & Rogerson 1996, QJE; I did not verify the QJE record in this session.)
- Read scope: abstract and introduction only.
- WHAT: Multi-community model with majority vote on the income tax rate and endogenous residence. Compares policies (subsidies, spending floors or ceilings, redistribution) by welfare and by education quality; identifies policies making everyone better off.
- Relevance: Theory of the forward problem (preferences produce allocations); no estimation. Useful for naming the political mechanism (median voter) that an inverse analysis cannot distinguish from a planner [inferred].

### C3. Calabrese, Epple & Romano 2024/2025
- Citation: Stephen Calabrese, Dennis Epple, Richard Romano (2025), "The Political Economy of School Finance Systems with Endogenous State and Local Tax Policies", International Economic Review, DOI 10.1111/iere.12762; NBER WP 33212 (November 2024), retrieved.
- Read scope: abstract, introduction, and calibration section headings; equilibrium proofs not read.
- WHY/HOW: General-equilibrium model: households vary in income and taste for school quality, sort among districts, and vote at both state and district level over taxes; regimes: flat grant, foundation, categorical grants, power equalisation. Calibrated to 2010-11 data.
- WHAT: The model predicts majority preference for mixed state-and-local foundation regimes with categorical grants, as observed, and reproduces cross-state differences in expenditure and the state share. Their reduced-form regression (eq. 1) of 2020-21 state spending on income, dispersion, Democratic vote share and rural share supports state-level taste differences. Preferences are the household taste parameters, calibrated not estimated by inversion.
- Relevance: This is the structural alternative to inverse optimisation: preferences sit with voters and the formula is an equilibrium outcome. An inverse-GP "planner" is a reduced-form shortcut for this; any claim about "government priorities" should say whether it means the median voter's [inferred].

### Not retrieved
- Behrman, Pollak & Taubman (1982), "Parental preferences and provision for progeny", Journal of Political Economy 90(1): 52-73, DOI 10.1086/261039. Paywalled; metadata from RePEc search result. Relevant as the household-level analogue (estimating an inequality-aversion parameter from allocation across children). Not read.
- Behrman & Craig is the only paper in this cluster I found that estimates inequality aversion from the allocation of a public service across groups. I did not find a published school-finance paper that estimates welfare weights from state-aid decisions (see synthesis).

---

## Synthesis

### (a) What economics already does, with identification strategies and pitfalls

1. Revealed social weights via inverse optimum in taxation (A2, A3, A5, A6). Strategy: assume the observed schedule is optimal for a planner; plug in estimated behavioural elasticities and the income distribution; solve the first-order condition for the weights. Pitfalls stated by the authors: weights move with the assumed elasticity (A3: the cross-country ranking changes; A2: weights turn negative at the top for plausible elasticities); the trilemma of A6; weights are endogenous, not structural, and do not transfer across settings (A5, Section 8.4).
2. Revealed weights in public-service allocation (A1). Strategy: an explicit outcome production function plus first-order condition equating the marginal rate of substitution to the marginal rate of transformation; two parameters, inequality aversion and group weights; IV for simultaneity. Pitfall: only products of weights, constants and production elasticities are identified (fn. 18); a single city and year; the government responded to officially reported crime rather than the true outcome, showing the choice of outcome measure changes the answer.
3. Framework and stated preference (A4, A7). Weights are primitives; elicited from surveys or experiments. Capozza & Srinivasan find stated weights much more progressive than weights implied by the US tax and transfer system, so revealed and stated differ strongly.
4. School finance (B1-B6, C1-C3) is mostly descriptive or causal, not preference-inferring. The evidence supplies (i) progressivity statistics (Baker et al. ratio of funding at 30% to 0% poverty; Chingos & Blagg enrolment-weighted gap), (ii) formula features (35 states have a poverty weight per Chingos & Blagg), (iii) causal effects of money on outcomes by group (Lafortune et al., Jackson et al.), (iv) political-economy determinants (Poterba; Calabrese et al.). Preference parameters appear only as calibrated household tastes (Calabrese et al.) or reduced-form coefficients (Poterba).

### (b) What an inverse goal-programming approach could add (critical)

- Economics already does essentially the same thing at the level of principle: "find the objective that rationalises the observed choice" is the inverse-optimum idea (Bourguignon & Spadaro, Hendren) and, for allocations, Behrman & Craig. An inverse GP paper must not claim novelty for the idea of recovering priorities from allocations [inferred].
- What could be genuinely different [inferred]: (1) Goal-based preference structure: targets (aspiration levels) plus deviation weights, possibly lexicographic or with asymmetric penalties, rather than a smooth concave welfare function with one curvature parameter. Behrman & Craig's welfare function has symmetric smooth curvature and group weights; it cannot represent "the state aims for a floor on poor-district spending and does not care beyond". Whether data can distinguish a target from a smooth concave function is an open identification question and must be tested, not assumed. (2) Several outcomes with explicit priorities (equity, adequacy, graduation, effort) and a constraint set made of legal and fiscal rules, which is natural in GP and awkward in the Mirrlees setup. (3) Set-valued inference: the inverse problem for a polyhedral or kinked objective generally has a set of weights consistent with an observation; reporting that set (a cone of weights) is more honest than a point estimate, and matches the sensitivity the tax literature found [inferred]. (4) Link to decision-focused learning in the other clusters: the estimated production side (effect of $1,000 on graduation by group) enters the inverse step, and its error propagates into the inferred weights.
- Risks: the identification pitfalls in (a) apply with more force. With one observation per state-year and a fixed production model, many weight vectors are observationally equivalent; weights are identified only relative to the assumed production function and goal targets (as in Behrman & Craig fn. 18). Political economy (median voter, court orders, disguised redistribution per Lafortune et al. fn. 6) means "planner" priorities are not what the data reveal. The gap Capozza & Srinivasan document (revealed far less progressive than stated) is the most interesting empirical target but admits many explanations besides weak priority on equity.
- Practical consequence for our data (US districts 2010-2019): the natural unit is state-year with districts as the "neighbourhoods" of Behrman & Craig; per-pupil spending is an input and graduation rate an outcome. Revenue source (federal, state, local) matters: Chingos & Blagg show local revenue offsets state progressivity, so priorities should be inferred from the controllable layer (state aid), not from total spending.

### (c) Open problems stated by authors (with locators)

- Bargain et al. (IZA DP 7215), conclusion: extend to non-cash benefits and public goods; other behavioural margins (migration, evasion, long-run education and career choices); model the political process that produced the system.
- Hendren (NBER WP 20351), Section 8.2-8.4: general-equilibrium effects of tax changes; heterogeneity of surplus conditional on income; weights are not structural and not transferable across countries.
- Lockwood & Weinzierl (NBER WP 21927), introduction: the trilemma, and that existing data cannot identify which of the three conditions fails; instability of inferred weights over time (pre- and post-1986).
- Bourguignon & Spadaro (EM9/08), Section 7: the authority may not optimise at all; political-economy forces and constraints such as piecewise-linear schedules.
- Saez & Stantcheva (NBER WP 18835), footnote 1 and Section I: preferences taken as given, political process not analysed; the approach is local and cannot rank two local optima.
- Poterba (NBER WP 5677), Section 3 end: circuit-breaker laws endogenous; better data and valid instruments needed.
- Shores et al. (EdWorkingPaper 19-52 v2), introduction: only five of 27 reform states had been evaluated individually; they call for understanding which state features predict effects.
- Chingos & Blagg, "Comparison with existing measures": divergence between revenue-based and spending-based progressivity "warrants further investigation".

### Papers important but paywalled or not retrieved (DOIs)
- Bourguignon & Spadaro 2012 published version: 10.1007/s10888-010-9153-0 (read the 2008 working paper instead).
- Saez & Stantcheva 2016 published version: 10.1257/aer.20141362 (read NBER WP).
- Hendren 2020: 10.1016/j.jpubeco.2020.104198 (read NBER WP).
- Hendren & Sprung-Keyser 2020: 10.1093/qje/qjaa006 (abstract only read).
- Behrman, Pollak & Taubman 1982: 10.1086/261039 (not read).
- Candelaria & Shores 2019: 10.1162/edfp_a_00236 (not read).
- Bargain et al. 2014 Annals of Economics and Statistics: 10.15609/annaeconstat2009.113-114.257 (not read; check whether identical to IZA DP 7215).
- Kitchens (2021), "Partisan Politics and Public Education: Finding the Formula for (Electoral) Success", State Politics & Policy Quarterly, DOI 10.1177/1532440020933205 (found on Crossref; not read; may be relevant for partisanship and formula design).
- Lockwood & Weinzierl 2016 (JME): 10.1016/j.jmoneco.2015.10.006.
