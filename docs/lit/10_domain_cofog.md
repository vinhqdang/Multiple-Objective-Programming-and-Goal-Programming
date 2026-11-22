# Domain note: national budgets by function (COFOG), defence and fiscal limits (2026-11-22)

Scope: eleven sources retrieved in this session. Read scope is stated per paper (full text = PDF text extracted and read in parts; abstract = metadata or abstract only). The search was not systematic (no OpenAlex; several publisher PDFs blocked: Springer, CESifo, IMF PDF, SSRN), so absence claims are provisional. Data and targets are in `data/cofog/` (README there).

## Papers

### 1. Brender & Drazen (2009). Do Leaders Affect Government Spending Priorities? NBER WP 15368. https://www.nber.org/papers/w15368 (DOI 10.3386/w15368)
Read: full text PDF (abstract, introduction, index construction, parts of results); not read in detail: robustness tables.
- WHY: does a change of leader change the functional composition of the budget, i.e. are budgets a readout of leaders' preferences?
- HOW: own panel of central-government expenditure composition, 71 democracies, 1972-2003; an index of composition change (half the sum of absolute changes in category shares, range 0-100) over 1-4 year horizons; regressions on leader replacement, election years and political and economic controls.
- WHAT: leader replacement has no significant short-run effect on composition; larger changes appear over the medium term, mostly in developed countries; election years go with larger composition change in established democracies. The authors cite budget incrementalism and inertia (budget allocations "almost always change incrementally").
- Relevance: high for identification. Composition is sticky, so one-year allocations carry little preference information unless history (the status quo) is modelled; central government only, not general government COFOG.

### 2. Persson & Tabellini (1998). The Size and Scope of Government: Comparative Politics with Rational Politicians. NBER WP 6848. https://www.nber.org/papers/w6848 (DOI 10.3386/w6848)
Read: full text PDF, text extraction starts at the introduction (title page not in the extracted text); read introduction and first results section; theory sections skimmed.
- WHY: explain cross-country variation in size and composition of government spending by electoral rule and regime type.
- HOW: cross-section of democracies, central-government spending averaged 1988-92, OLS with controls (log income, openness, share above 65, ethno-linguistic fractionalisation); dependent variables total spending and a "public goods" aggregate (order and safety, transport, education; extended with health).
- WHAT: presidential regimes have central government about 10 percentage points of GDP smaller (sample mean just below 29%); the majoritarian effect is smaller and less significant. Residuals of plus or minus 10% of GDP remain after standard controls.
- Relevance: medium. Shows that institutions shift composition and size, hence a fitted "weight" per country would absorb political-institutional heterogeneity; cross-section, not a panel decision model.

### 3. Caselli & Wingender (2018). Bunching at 3 Percent: The Maastricht Fiscal Criterion and Government Deficits. IMF WP 18/182. https://www.imf.org/en/Publications/WP/Issues/2018/08/03/Bunching-at-3-Percent-The-Maastricht-Fiscal-Criterion-and-Government-Deficits-46135 (DOI 10.5089/9781484371732.001)
Read: abstract/summary page only (PDF blocked), so details below are as reported on that page and in a search snippet.
- WHY: does the 3% deficit ceiling act as a target for governments?
- HOW: treatment effects combined with bunching estimation, kernel density and logit models on deficits around the threshold.
- WHAT: the rule acts as a "magnet": about 20 percent excess mass around the ceiling after adoption, with most of the response coming from fewer high-deficit observations (the page does not say how it splits above or below 3%). The snippet noted that adoption often coincided with EU accession, so the two effects are hard to separate (not verified in the text).
- Relevance: high. First direct evidence that a published numeric limit behaves like an aspiration level in observed deficits; supports using the 3% as ground-truth target for a deficit goal, with the caveat that the limit is a ceiling (one-sided deviations).

### 4. von Hagen & Wolff (2006). What do deficits tell us about debt? Empirical evidence on creative accounting with fiscal rules in the EU. SFB/TR 15 Discussion Paper No. 148 (published version not retrieved). https://epub.ub.uni-muenchen.de/13403/1/148.pdf
Read: full text PDF (abstract, introduction, institutional section, parts of estimation and robustness).
- WHY: do EU governments circumvent deficit rules by creative accounting?
- HOW: relate the gap between debt change and deficit (stock-flow adjustment) to the deficit, on EU-15 data, comparing periods before and after the Maastricht/SGP rules, instrumenting; builds on Milesi-Ferretti (2003) where the incentive depends on reputation cost and the economic cost of compliance.
- WHAT: the rules induced governments to use stock-flow adjustments to hide deficits, more strongly for the cyclical component of the deficit; in the period before the rules the regressions imply no such correlation; results robust to dropping countries.
- Relevance: high for threats. Reported B9 near 3% can be manipulated, so the observed deficit is a noisy version of the intended one; this is measurement error correlated with distance to the target.

### 5. Gilbert & de Jong (2014). Does the Stability and Growth Pact induce a bias in the EC's fiscal forecasts? DNB Working Paper 451. https://www.dnb.nl/media/pkydyj24/working-paper-451.pdf
Read: full text PDF (abstract, introduction); methods and results not read in detail.
- WHY: enforcement hinges on EC forecasts; do governments' incentives bias them?
- HOW: real-time forecast errors, reconstruct the expectation that the 3% ceiling binds, instrumental approach, euro-area versus non-euro-area groups.
- WHAT: for euro-area countries EC forecasts are biased upwards when the deficit threatens to exceed 3% of GDP; no bias established for non-euro countries (no risk of fines); independent fiscal councils attenuate the bias.
- Relevance: medium-high. Corroborates that 3% is treated as a binding target by governments; shows forecast optimism as another channel that makes planned (ex ante) deficits differ from realised ones.

### 6. Runje & Kotarski (2026). Moving NATO Burden Sharing into the Future: Analyzing Burden Sharing in the Post-Cold War Era. Business Systems Research 17(1), 154-178. https://doi.org/10.2478/bsrj-2026-0008 (open PDF https://hrcak.srce.hr/file/500553)
Read: full text PDF, abstract, introduction, literature and method; results table skimmed.
- WHY: whether economic size, resource endowments or capability indices explain NATO allies' military spending (joint-product model of Olson and Zeckhauser tradition).
- HOW: unbalanced panel of NATO members 1990-2019, two-way fixed effects, dependent variable log military expenditure (level, not share of GDP), clustered errors; five predictors (GDP, gross and net resources, Productive Capacities Index, an adjusted composite capability index).
- WHAT: economic size and resource-endowment measures are the strongest within-country predictors; the capacity index is insignificant; results stable across samples and specifications. The paper recalls the Wales 2014 pledge (2% of GDP, 20% on equipment) and notes the limitation that the sample ends before 2022.
- Relevance: medium. Documents the standard econometric view of defence spending as a function of economic size and threat controls, not of a target; shows level-versus-share choice matters for the GDP denominator issue.

### 7. Kuokštytė & Kuokštis (2024). A spatiotemporal analysis of NATO member states' defense spending: how much do allies actually free ride? Political Science Research and Methods. https://doi.org/10.1017/psrm.2024.39
Read: full text of the research note (data, method, robustness, conclusion).
- WHY: free riding is usually measured as negative spatial interdependence of allies' spending, ignoring temporal dependence.
- HOW: 27 NATO allies, SIPRI military expenditure (constant 2020 USD), log GDP and population, country fixed effects, lagged dependent variable, spatial autocorrelation model estimated by ML, periods from 1975, 1991, 1999 to 2021; robustness: drop the US, Russian spending, host-nation support.
- WHAT: free riding exists and its spatiotemporal effect exceeds the short-run effect (e.g. a given increase by an ally leads over 15 years to a cumulative 0.21 to 0.31 percent decrease in another's own spending, depending on the period); robust to the variations tried.
- Relevance: medium. Indicates that allies' budgets respond to each other (strategic interdependence), a confounder for a single-actor inverse model, and that dynamics must be modelled.

### 8. Onder (2022). NATO Uyelerinin %2'lik Savunma Harcama Hedefine Yakinsamasinin Sinanmasi (Testing the convergence of NATO members to the 2% defence spending target). Selcuk Universitesi Sosyal Bilimler Meslek Yuksekokulu Dergisi. https://doi.org/10.29249/selcuksbmyd.1177073
Read: Crossref abstract only (Turkish).
- WHY/HOW: tests whether members converge to the 2% target, stochastic convergence analysis on 2015-2021 data.
- WHAT: apart from countries already meeting the target in 2021, ten countries (Italy, Norway, Czechia, Bulgaria, Netherlands, Denmark, Spain, Hungary, Germany, Albania) converge to 2%; counting the ten already above it, half of the countries missing the target converge to it; no sign that all members reach it despite the Russia factor.
- Relevance: high for the question "target or not", but only abstract-level; methods and robustness are not known to me.

### 9. Favero & Rovelli (2003). Macroeconomic Stability and the Preferences of the Fed: A Formal Analysis, 1961-98. Journal of Money, Credit and Banking. https://doi.org/10.1353/mcb.2003.0028 (SSRN version 2001: https://doi.org/10.2139/ssrn.280250; earlier "Modeling and Identifying Central Banks' Preferences", https://doi.org/10.2139/ssrn.156289)
Read: SSRN abstracts via Crossref only (the JMCB entry has no abstract).
- WHY: separate shifts in central-bank preferences from shifts in shock variance and policy efficiency.
- HOW: estimate a small structural macro model jointly with the first-order (Euler) conditions of the Fed's intertemporal optimisation (quadratic loss), by GMM; compare optimal and actual rate behaviour.
- WHAT: the (implicit) inflation target changed drastically in the Volcker-Greenspan period; the paper reports that strict inflation targeting dominates flexible targeting but does not describe actual policy exactly.
- Relevance: high as methodological precedent. It is a revealed-preference estimation of weights and implicit targets of a policy maker from its decisions, with the structural model of the economy supplied separately. It shows the same confounding (weights versus targets versus model) that an inverse GP will face.

### 10. Karami-Fard (2026). Need, Alignment, or Commerce? Recovering the Revealed Priorities of Foreign Aid Donors through Inverse Optimization. SSRN. https://doi.org/10.2139/ssrn.7302189
Read: Crossref abstract (full text blocked, SSRN 403).
- WHY: aid allocation is usually characterised by regression coefficients rather than as an optimisation.
- HOW: each donor-year is a constrained allocation over three objectives (need, diplomatic alignment, commerce); KL-divergence-based inverse optimisation recovers weights, with a fit diagnostic and bootstrap confidence intervals; 24 donors, 142 recipients, 2010-2022.
- WHAT: allocation is organised by a need-commerce axis more than by alignment; adding commerce raises mean fit from about 0.013 to 0.27; weights are stable to the diminishing-returns parameter (rank correlation about 0.98).
- Relevance: closest applied precedent to inverse GP on public allocations; weights only (no aspiration levels), objectives measured exogenously, and the fit is modest. Abstract-level reading.

### 11. Kancs (2026). Geoeconomic Stress and European Defence Readiness. arXiv:2610.33785. https://arxiv.org/abs/2610.33785
Read: abstract and first pages only.
- WHY/HOW: composite index of the economic-industrial capacity of 28 European Allies to sustain military capability under five geoeconomic stress scenarios.
- WHAT: baseline scores 0.471 to 0.759 (mean 0.610); combined stress lowers the mean by 19.5%. The authors argue attention should shift from expenditure targets alone to the capacity to convert resources into capability.
- Relevance: low-medium. Argues that spending-share targets (2%) are an input measure; a second-stage reason for weighting a capability goal in addition to the budget share.

## Synthesis

What is known.
- Composition of public budgets is sticky: leader changes show no short-run composition effect (Brender & Drazen), institutions shift size and scope (Persson & Tabellini). A one-year cross-section reveals institutions and the status quo as much as preferences.
- Numeric limits behave like targets. Deficits bunch near 3% and are pulled from high-deficit values (Caselli & Wingender, abstract level), governments use stock-flow adjustments and optimistic forecasts to appear compliant near the limit (von Hagen & Wolff; Gilbert & de Jong). This supports reading 3% as an aspiration level that governments manage towards, imperfectly and with measurement manipulation.
- Defence spending: determinants literature is regression-based on levels and size (Runje & Kotarski), with allied interdependence and free riding (Kuokštytė & Kuokštis). The one convergence test found (Onder, abstract) finds partial convergence to 2% in 2015-2021. No paper retrieved estimates what weight governments put on defence relative to other COFOG functions.
- Revealed-preference estimation of policy-maker objectives exists for central banks (Favero & Rovelli: weights and implicit targets) and for aid donors (Karami-Fard: weights only). I did not find, in this limited search, an inverse-optimisation or inverse-GP estimation of general-government functional budget priorities.

What inverse GP could add.
- Joint weights and aspiration levels per function with explicit kinks: the 2% and 3%/60% limits are one-sided goals, naturally represented by deviation variables, and the published values give a direct check on the estimated targets.
- Set-valued output (cone of consistent weights and targets), appropriate given the sticky and noisy budgets.
- Time variation: the Wales (2014), Vilnius (2023) and Hague (2025) pledges are known shifts in the defence target, usable as a break test (does the estimated defence aspiration level jump at 2014/2023/2025?).

Identification threats.
- GDP denominator: all quantities in % of GDP move when GDP changes (recessions raise ratios without any decision). Use MIO_EUR and PC_TOT alongside PC_GDP and treat the budget envelope (total expenditure) as the decision variable; NATO ratios use a real-GDP basis (Table 3 "based on 2021 prices"), Eurostat uses current GDP.
- Definitional gap between NATO and COFOG GF02 (README example: Poland 2023 2.2 vs 3.27); the 2% is on NATO's definition; also the Hague 3.5% core plus 1.5% related split has no COFOG counterpart.
- Multi-year commitments, procurement lumps and inertia (Brender & Drazen): defence in particular is a stock-like programme; annual shares reflect contracts signed earlier. Dynamic or incremental formulations needed.
- Joint products and strategic interdependence (Kuokštytė & Kuokštis; Runje & Kotarski): defence goals depend on allies' spending and on threat (e.g. Russian spending), not only on national preferences.
- Manipulated or optimistic deficits near 3% (von Hagen & Wolff; Gilbert & de Jong): measured B9 and debt are noisy and biased exactly where the target kink lies. Eurostat B9 is as notified, which these papers suggest can be managed.
- Political economy and heterogeneity: institutions and electoral timing shift composition (Persson & Tabellini; Brender & Drazen); weights are not purely social preferences.
- Structural confounding as in Favero & Rovelli: weights, targets and the model of how spending affects outcomes cannot be separated without outside information; for COFOG the "outcome" side is mostly unobserved, so goals would have to be stated on spending shares themselves.
- Many European governments are also subject to external EU constraints (SGP) and supranational programmes, making a single-actor optimisation incomplete; euro-area versus non-euro status matters (Gilbert & de Jong).

How the stated targets can serve as ground truth.
- Defence: Wales 2014 (2% of GDP, 20% on equipment), Vilnius 2023 (2% as floor), Hague 2025 (3.5% core plus 1.5% related by 2035) from `targets.csv`; compare the inferred defence aspiration level per country with 2%, and its shift after each summit. Use NATO's Table 3 series (`nato_defence_pc_gdp.csv.gz`) as the observed defence goal variable, since it matches the definition of the target. Expect a one-sided (floor) goal: allies above 2% (e.g. Greece, Estonia, Poland, UK, US) should show slack, not exact attainment; countries just under 2% before 2024 show the guideline as an aspiration they approached. The 2025e column in the NATO PDF is mostly at about 2.0 for several allies, which looks like targeting but is an estimate (flag `estimate`).
- Fiscal: 3% deficit and 60% debt (Protocol 12) as ceilings; test whether recovered deficit and debt goals sit at or below those values, and whether the deficit "bunching" shows up as kinks. In 2023 17 of the 31 geo codes in the debt file (including EA and EU aggregates) were above 60% (e.g. EL 164.0, IT 134.0, FR 109.5, ES 105.3, BE 102.3, PT 96.9), so for these the 60% debt limit is a distant aspiration or inactive; treat them separately from countries below it.
- R&D: Barcelona 3% (2002) and Europe 2020 3% are EU-level, not national, targets; they cannot validate country-level estimates without national targets (not retrieved). R&D is also not a COFOG division as such (R&D appears as groups inside several divisions; group labels were not checked here); R&D in the targets is measured on all sectors, public and private.
- Education and health: no spending-share target was found (Europe 2020 education targets are outcomes). No ground truth for those functions in this download.
- Caveat: stated targets are political statements; a mismatch between inferred and stated targets can mean that the model is wrong, that the government is not trying, or that the stated target is cheap talk. Matching is evidence, not proof, and failure to match is not a refutation.

## Items to read next (not retrieved)
Caselli & Wingender full text; Milesi-Ferretti (2003) model; Kim & Sandler (2023/24, Defence and Peace Economics, DOI 10.1080/10242694.2023.2230408, metadata only retrieved); Potrafke CESifo WP 8134 on COFOG political cycles (found by search, not read); Koen & van den Noord, Fiscal Gimmickry in Europe (OECD, DOI 10.1787/237714513517, metadata only); Hartley & Sandler 1999 (DOI 10.1177/0022343399036006004, metadata only); Karami-Fard full text.
