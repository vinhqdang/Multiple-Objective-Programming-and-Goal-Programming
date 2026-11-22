# Cluster 2: learning meets goal programming (GP) and multiobjective optimization (MOO)

Method note. Papers were downloaded to /tmp/lit2/ and read with pdftotext (arXiv, JAIR/Springer open access). "Read scope" says what was actually read. Items marked ABSTRACT-ONLY or METADATA-ONLY were not read in full and are listed at the end. Locators (Sec./p.) refer to the arXiv/PDF version read. Statements tagged [inferred] are my own reading, not the authors' claims. The OpenAlex API budget was exhausted mid-search and the MDPI/CORE servers refused automated downloads (I did not work around that), so search coverage is incomplete (see "Coverage caveat").

---

## A. Decision-focused learning (DFL) with multiple objectives

### A1. Mandi, Kotary, Berden, Mulamba, Bucarey, Guns, Fioretto (2024) - DFL survey
- Citation: Mandi J., Kotary J., Berden S., Mulamba M., Bucarey V., Guns T., Fioretto F. (2024). Decision-Focused Learning: Foundations, State of the Art, Benchmark and Future Opportunities. Journal of Artificial Intelligence Research 80. DOI 10.1613/jair.1.15320; arXiv:2307.13565v4. https://arxiv.org/abs/2307.13565
- Read scope: full text retrieved (76 pp.). Read abstract, Introduction, problem setup (Sec. 2), Sec. 3.3 (extensions, incl. 3.3.2 multi-task DFL and 3.3.3 parameters in constraints), Sec. 6 future directions; searched whole text for multiobjective/Pareto/goal programming/inverse. I did not read the benchmark sections in detail.
- WHY: unify the literature on training ML models end-to-end with a downstream constrained optimization, because accuracy-trained predictions can give poor decisions.
- HOW: taxonomy of gradient-based (implicit differentiation of KKT, perturbation, surrogate losses such as SPO+) and gradient-free approaches; benchmark of 11 methods on 7 problems (all linear objectives).
- WHAT: DFL helps most under model misspecification and uncertainty. On multiobjective settings the survey says almost nothing: Sec. 3.3.2 (p. 31) covers only multi-task DFL (Tang & Khalil) and one paragraph on Dinh et al. (fair OWA multiobjective DFL). The words "goal programming" do not appear. Sec. 2 (p. ~6) assumes constraints are known and that predicted parameters enter the objective; Sec. 3.3.3 reviews predicting constraint parameters as a sparse, hard subfield. Sec. 6 (p. 53) states "Most DFL research has focused on optimization problems with linear objective functions" and that most techniques "are not equipped" for non-linear objectives; it also states that "the literature on robust DFL remains sparse" (p. 54).
- Relevance to us: it frames our situation. Cobb-Douglas outcome functions (nonlinear, parameters in the objective/goal constraints) and GP deviations are outside the survey's benchmarked scope, and the authors name both non-linear objectives and robust DFL as open.

### A2. Li, Wu, Feng, Hu, Fu, Ye (2024) - Multi-objective DFL (Cainiao/Alibaba)
- Citation: Li P., Wu L., Feng C., Hu H., Fu L., Ye J. (2024). Differentiation of Multi-objective Data-driven Decision Pipeline. arXiv:2406.00779. https://arxiv.org/abs/2406.00779 (no peer-reviewed venue found).
- Read scope: abstract, introduction, problem statement, motivating example, method (loss functions, differentiation), experimental setup and conclusion. Result tables skimmed, not audited.
- WHY: DFL had focused on single-objective problems; with unknown coefficients and several conflicting objectives, two-stage predict-then-optimize mismatches predicted and true Pareto sets.
- HOW: predict coefficients for each objective with a neural model; scalarize (instance-normalized weighted sum) and differentiate through the LP using a Wilder-et-al.-style quadratic regularizer (DSLP); train on a weighted sum of three losses: landscape loss (objective space, using a solution cache), Pareto-set loss (solution space) and decision loss (representative solution).
- WHAT: Motivating bi-objective quadratic example (Sec. 4) shows the overlap of predicted and true Pareto sets shrinks geometrically with dimension and number of objectives even for bounded coefficient error. Experiments (web-ad allocation, paper-reviewer bipartite matching on Cora, a three-objective problem), all multiobjective linear programs, beat two-stage and single-objective DFL baselines. Conclusion (Sec. 7): "Current research in multi-objective optimization and decision-focused learning remains limited."
- Relevance to us: closest "multi-objective DFL" precedent (2024) and a theoretical warning that coefficient errors distort the whole Pareto set. It is linear-program only, uses weighted-sum scalarization, no goal levels or deviation variables.

### A3. Dhakal & Lachner (2026) - ParetoSPO
- Citation: Dhakal A., Lachner T. (2026). Pareto-Informed Smart "Predict, then Optimize" for Multi-Objective Combinatorial Problems. arXiv:2611.23076v2 (18 Nov 2026). https://arxiv.org/abs/2611.23076 (preprint).
- Read scope: abstract, introduction, related work, method, setup, discussion/limitations/conclusion (read via raw text because the two-column layout garbles; results tables not audited).
- WHY: existing multiobjective DFL relies on linear scalarization, which reaches only the convex hull of the Pareto front.
- HOW: extend SPO+ so the regret target is chosen from the true Pareto front by cosine similarity to a sampled preference vector; one specialised model per preference ("model committee"); implemented in PyEPO.
- WHAT: beats two-stage MSE and scalarized SPO+ on multiobjective shortest path and multidimensional knapsack at several noise levels. Authors' stated limitations (Sec. 6): training cost grows linearly with the number of preferences and the model cannot generalise to unseen preferences; they propose a preference-conditioned model (COSMOS-like) as future work.
- Relevance to us: shows preference/aspiration vectors can be injected into the DFL loss. Needs true Pareto front at training time (cheap for small combinatorial problems, unclear for continuous budgets). Intro claims extension to multi-objective "remains unexplored" and does not cite Li et al. 2024 [inferred from reading its related-work section; I did not find that citation].

### A4. Dinh, Kotary, Fioretto (2024) - Fair multiobjective PtO
- Citation: Dinh M. H., Kotary J., Fioretto F. (2024). End-to-End Learning for Fair Multiobjective Optimization Under Uncertainty. arXiv:2402.07772. https://arxiv.org/abs/2402.07772 (cited in Mandi et al.; venue of final version not checked).
- Read scope: abstract, introduction, methods (OWA, Moreau-envelope smoothing), experiments overview (Markowitz portfolio with scenarios, resource allocation, learning-to-rank), conclusion. Appendix proofs not read.
- WHY: PtO had only handled differentiable or linear single objectives; fairness/robustness need OWA aggregates, which are nondifferentiable.
- HOW: smooth the OWA with its Moreau envelope (and a QP alternative) so end-to-end training differentiates the aggregated objective; exploit structure (totally unimodular constraints, Frank-Wolfe).
- WHAT: higher decision quality than two-stage, and Moreau scales where the QP form fails beyond about 5 scenarios (Sec. 5, portfolio). Pareto-efficiency is inherited from OWA monotonicity (Sec. 2).
- Relevance to us: the only DFL paper found that targets an equity-oriented aggregation of several objectives with resource allocation. OWA is a compromise-programming cousin of GP; same recipe (smooth the aggregator) could apply to GP's piecewise-linear deviation penalties [inferred].

### A5. Jiao, Zhang, Lin, Shang, Yan (2026) - Closed-loop DFL for cloud orchestration
- Citation: Jiao D., Zhang X., Lin H., Shang K., Yan S. (2026). Closed-Loop Decision-Focused Learning for User-Aware Cloud Orchestration under Uncertainty. arXiv:2608.05735. https://arxiv.org/abs/2608.05735 (preprint).
- Read scope: abstract, introduction, contributions, problem formulation, method outline; skimmed experiments.
- WHY: PtO pipelines decouple forecasting from scheduling under uncertain capacity constraints.
- HOW: MTGNN forecaster plus zeroth-order DFL (tree-structured Parzen estimator) feeding a neural Pareto local search that scalarizes by decomposition.
- WHAT: better violation-rate / satisfaction / utilisation trade-offs on four real traces.
- Relevance to us: a gradient-free DFL route (useful when the optimizer is a black box) and an example of predicting constraint parameters in a multiobjective problem. Application domain is far from public budgets; low priority.

---

## B. Inverse multiobjective optimization

### B1. Dong & Zeng (2018) - Inferring parameters through IMOP
- Citation: Dong C., Zeng B. (2018). Inferring Parameters Through Inverse Multiobjective Optimization. arXiv:1808.00935v1. https://arxiv.org/abs/1808.00935 (preprint; I did not find a journal version).
- Read scope: abstract, introduction and literature review, formulation (Sec. 2), conclusion, outline of algorithms and experiment set-up (50-page PDF; proofs not read).
- WHY: single-objective inverse optimization attributes data scatter to noise; if observed decisions are trade-offs among several criteria this corrupts inference.
- HOW: assume observed decisions are noisy efficient solutions of a convex multiobjective problem; since weighted-sum scalarization reaches every efficient point of a convex problem (their Prop. 2) they fit parameters theta and the weight samples jointly via a non-convex mixed-integer formulation solved heuristically (ADMM, clustering of observations by weight).
- WHAT: statistical-consistency analysis, link between identifiability and estimation accuracy (Sec. 7), accurate recovery on multiobjective LP/QP/nonlinear examples; also yields the distribution of weights over the decision-maker population.
- Relevance to us: this is the standard route to learn objective weights/preferences from observed decisions (e.g. past budget allocations), a possible alternative to eliciting GP weights and targets. It treats parameters of the decision model as unknown and learned, but from decisions, not from outcome data.

### B2. Wang, Dong, Zeng (2020/2022) - Online inverse MOO
- Citation: Wang Y., Dong C., Zeng B. Learning Multiobjective Program Through Online Learning (v1 title: Inverse Multiobjective Optimization Through Online Learning). arXiv:2010.06140v2, Dec 2022. https://arxiv.org/abs/2010.06140 (marked "Paper under review"; no peer-reviewed version found).
- Read scope: abstract, introduction, formulation, regret theorem statement, experiments (MQP and portfolio data of 30 blue-chip stocks), conclusion.
- WHY: observations arrive sequentially and are noisy or boundedly rational.
- HOW: online learning with implicit update rules on the inverse-MOP loss; regret analysis extending Kulis & Bartlett.
- WHAT: O(1/sqrt(T)) regret bound under regularity conditions; fast convergence and noise robustness empirically even when conditions fail. Authors flag relaxing those conditions and contextual-bandit extensions (Conclusion) as future work.
- Relevance to us: sequential updating of preference parameters as new fiscal years arrive; theory limited to settings with regularity conditions.

### B3. Dong & Zeng (2020) - Wasserstein distributionally robust IMOP
- Citation: Dong C., Zeng B. (2020). Wasserstein Distributionally Robust Inverse Multiobjective Optimization. arXiv:2009.14552 (OpenAlex also lists it as AAAI-21, DOI 10.1609/aaai.v35i7.16739; I read only the arXiv version). https://arxiv.org/abs/2009.14552
- Read scope: abstract, introduction, formulation, theory statements, conclusion, experiment description (MQP and portfolio).
- WHY: IMOP is sensitive to a misspecified decision model, too few or poor decisions, and an uninformative parameter space.
- HOW: minimise worst-case loss over a Wasserstein ball around the empirical distribution of decisions; semi-infinite reformulation with a cutting-plane algorithm (finite delta-optimal convergence).
- WHAT: sub-linear excess-risk rate; works on synthetic MQP and portfolio data. Sec. noting enumerating all weights is computationally intractable, so weight sampling is used (around p. 8; line "As it is practically infeasible due to computational intractability").
- Relevance to us: first-order template for carrying estimation uncertainty from a learned model into a multiobjective decision model. Applies to inverse problems, not to a forward GP with learned coefficients.

### B4. Gebken & Peitz (2021) - Inverse MOO from data
- Citation: Gebken B., Peitz S. (2021). Inverse multiobjective optimization: Inferring decision criteria from data. Journal of Global Optimization 80:3-29. DOI 10.1007/s10898-020-00983-z; arXiv:1901.06141. https://link.springer.com/article/10.1007/s10898-020-00983-z (open access).
- Read scope: abstract, introduction, problem definition, algorithm summary, conclusion/outlook (Springer version, 27 pp.; arXiv v1 abstract compared).
- WHY: identify the objectives for which given points form (part of) a Pareto set.
- HOW: treat the objectives as unknowns in the multiobjective KKT system, expand in a basis, solve a homogeneous linear system by SVD; unconstrained MOPs, noisy data tolerated.
- WHAT: reconstruction of objective vectors and surrogate models for expensive MOPs. Authors' open problems (Sec. 6, p. 27): the assumption that KKT multipliers (weights) are in the data is strong; no Hausdorff-distance guarantee for surrogates; non-uniqueness of the recovered objective (large null space).
- Relevance to us: shows the inverse side is identifiability-limited without weights data; a different philosophy (recover functional form) from our parametric Cobb-Douglas learning.

---

## C. Goal programming with learning, forecasting, uncertainty

### C1. Repetto, La Torre, Tariq (2021/2022) - GP to combine learned models
- Citation: Repetto M., La Torre D., Tariq M. Federated Deep Learning in Electricity Forecasting: An MCDM Approach. arXiv:2111.13834v3 (Jan 2022). https://arxiv.org/abs/2111.13834 (a web index listed the arXiv v2 as "Deep Learning with Multiple Data Set: A Weighted Goal Programming Approach"; published venue not verified).
- Read scope: abstract, introduction, Sec. 2-3 (weighted GP in Chebyshev form, ensemble weights), experimental setup and conclusion; skimmed numerical results.
- WHY: models trained on different data splits conflict; they want an interpretable, model- and metric-agnostic way to combine them.
- HOW: train K networks on K splits, then solve a Chebyshev weighted GP whose goals are target values of performance metrics; the optimal alpha gives a convex combination of the K predictors.
- WHAT: on GEFCom2017 hourly load, the GP ensemble beats a model trained on the whole dataset when splits overlap (RMSE/MAE/MASE/SMAPE). Authors claim the "intersections between MCDM and DL have not been explored yet" (Introduction).
- Relevance to us: GP used inside ML (selecting/aggregating learned models), the reverse direction of our design (ML feeding a GP of public goals). Shows GP accepts arbitrary learned-model metrics as criteria.

### C2. Liu & Chen (2015) - Uncertain multiobjective programming and uncertain GP
- Citation: Liu B., Chen X. (2015). Uncertain Multiobjective Programming and Uncertain Goal Programming. Journal of Uncertainty Analysis and Applications 3:10. DOI 10.1186/s40467-015-0036-6. https://doi.org/10.1186/s40467-015-0036-6 (open access).
- Read scope: full text (8 pp.).
- WHY: decision environments contain parameters better described by uncertainty theory (belief degrees) than by probability.
- HOW: replace objective functions with expected values of uncertain variables and constraints with chance (belief-measure) constraints; transform to crisp preemptive-priority GP via inverse uncertainty distributions (Theorems 1-3 and Eq. 21-22).
- WHAT: a closed-form crisp GP for independent uncertain parameters with monotone dependence; no numerical application or estimation from data.
- Relevance to us: shows how a GP absorbs parameter uncertainty by substituting expected values or quantiles; the parameters' distributions are assumed given, which is where learned-model uncertainty (posterior or bootstrap) would enter [inferred].

### C3. Zhao, Hua, Yan, Zhang, Xu, Yang (2019) - Learn-then-optimize budget allocation (single objective)
- Citation: Zhao K., Hua J., Yan L., Zhang Q., Xu H., Yang C. (2019). A Unified Framework for Marketing Budget Allocation. KDD '19. arXiv:1902.01128v3. https://arxiv.org/abs/1902.01128
- Read scope: abstract, introduction, framework overview, optimisation formulation, related work, conclusion.
- WHY: allocate marketing budgets across market segments using responses learned from data.
- HOW: forecast response with a semi-black-box model (logit demand curve extended by neural nets), then solve the allocation as a convex problem by dual binary search; supports cost, profit and ROI constraints.
- WHAT: deployed at Alibaba; offline and A/B tests reported about 6% more sales with 40% lower spend on one scenario (Sec. 6). Future work: contextual variables, boundary constraints, approximation error analysis. Single objective; estimation error is not propagated into the optimisation.
- Relevance to us: a clear instance of the "learn response function, plug into budget optimisation" pipeline, with a single objective and no treatment of estimation uncertainty.

---

## Abstract-only or metadata-only items (not read in full; do not rely on beyond the quoted gist)

| Item | Status | Gist |
|---|---|---|
| Bae, Park, Jeon, Kim (2026), A decision-focused learning framework for goal-based investing, Quantitative Finance 26(1):1-13, DOI 10.1080/14697688.2025.2596917 | abstract only (via IDEAS RePEc page); publisher PDF not retrievable; not on arXiv | DFL applied to goal-based investing; a new decision-quality metric for goal programming that prioritises investor goals; DFL improves decision quality and feasibility under uncertain markets. This is the closest paper to our project; priority download. |
| Mallidis, Yakavenka, Konstantinidis, Sariannidis (2021), A Goal Programming-Based Methodology for Machine Learning Model Selection Decisions: A Predictive Maintenance Application, Mathematics 9(19), art. 2405 | abstract only (IDEAS page); MDPI refused automated download | GP over accuracy and time criteria to choose among tree/forest/SVR/NN models; sensitivity analysis on weights. |
| Mensah & Rocca (2019), Light Robust Goal Programming, Math. Comput. Appl. 24(4):85, DOI 10.3390/mca24040085 | metadata only (MDPI refused download; I did not circumvent) | Generalises light robustness to GP under budget-of-uncertainty and ellipsoidal sets, per a search-engine snippet; unverified. |
| Lu & Tsai (2024), Generalized robust goal programming model, European Journal of Operational Research 319(2):638-657 | metadata only (IDEAS, restricted) | Robust GP; title/venue confirmed on IDEAS/EconPapers only. DOI not retrieved. |
| Ghasemi Bojd & Koosha (2018), A robust goal programming model for the capital budgeting problem, J. Operational Research Society 69(7):1105-1113 | metadata only (IDEAS, restricted) | GP for soft budget constraints with robust optimisation for uncertain cash flows (snippet). DOI not retrieved. |
| A clustering-based framework for preference inference in inverse multiobjective optimization, Omega (2026), DOI 10.1016/j.omega.2026.103675 | metadata only (OpenAlex record; publisher PDF blocked) | Recent successor to Dong & Zeng on preference inference; authors not recorded. |
| OPSEARCH (2026), "A data-driven hybrid forecasting integrating machine learning, and goal programming framework for ac..." (title truncated in OpenAlex), DOI 10.1007/s12597-026-01161-7 | metadata only | Possibly a direct ML-forecasting plus GP paper; full title and authors unverified; worth checking. |
| Information Sciences (2026), Goal programming-based Wasserstein distributionally robust equilibrium vehicle routing design with c... (title truncated), DOI 10.1016/j.ins.2026.123316 | metadata only (Crossref) | GP combined with data-driven distributionally robust optimisation; title and authors unverified. |
| Liu-style and older stochastic/chance-constrained GP (e.g. Charnes & Cooper 1968 "A stochastic approach to goal programming", Operations Research 16(3):576, DOI 10.1287/opre.16.3.576) | metadata only (Crossref) | Classical stochastic/chance-constrained GP; foundational, not retrieved. |

## Papers to download manually (paywalled or blocked, ranked by importance to us)
1. Bae et al., A decision-focused learning framework for goal-based investing. DOI 10.1080/14697688.2025.2596917.
2. OPSEARCH 2026 hybrid ML forecasting + goal programming. DOI 10.1007/s12597-026-01161-7.
3. Lu & Tsai, Generalized robust goal programming model, EJOR 2024, 319(2):638-657 (look up DOI via the EJOR page).
4. Mensah & Rocca, Light Robust Goal Programming. DOI 10.3390/mca24040085 (open access at MDPI; fetch in a browser).
5. Information Sciences 2026, GP-based Wasserstein DR equilibrium vehicle routing. DOI 10.1016/j.ins.2026.123316.
6. Mallidis et al., Mathematics 9(19):2405 (open access at MDPI; fetch in a browser; DOI not confirmed).
7. Omega 2026 clustering-based preference inference for inverse MOO. DOI 10.1016/j.omega.2026.103675.
8. Ghasemi Bojd & Koosha 2018, JORS 69(7):1105-1113 (DOI to be looked up).
9. Charnes & Cooper 1968. DOI 10.1287/opre.16.3.576.
Also not retrieved: Tang & Khalil (multi-task SPO+/PyEPO), Elmachtoub & Grigas (SPO+), Tan, Delong, Terekhov (Deep inverse optimization); they are cited by the papers above but I did not fetch them.

---

## Synthesis

### What is established
- Learning coefficients then optimising (predict-then-optimize) can produce poor decisions, and training on decision quality (DFL) helps especially under misspecification and uncertainty (Mandi et al., Sec. 3.3.1 discussion and Sec. 1; confirmed again in A2-A4).
- A multiobjective DFL literature now exists but is tiny: Li et al. 2024 (linear programs, weighted-sum scalarization, three loss terms), Dinh et al. 2024 (OWA aggregate), Dhakal & Lachner 2026 (preference-targeted Pareto-aware SPO+). Each shows gains over two-stage training.
- Li et al.'s motivating example (Sec. 4) shows that bounded coefficient error can make predicted and true Pareto sets overlap on an exponentially small share as dimension grows; i.e. the damage of estimation error is multiplied, not averaged, in multiobjective problems.
- On the inverse side, there are consistency and regret results for learning weights/parameters of a convex multiobjective model from noisy observed decisions (Dong & Zeng 2018; Wang et al.; Dong & Zeng 2020 with distributional robustness), plus a KKT-based functional reconstruction (Gebken & Peitz).
- GP has a classical route for uncertain parameters: replace by expectations or quantiles/chance constraints and obtain a crisp GP (Liu & Chen 2015, Eq. 21-22; the older chance-constrained GP literature, metadata only).

### Where approaches diverge
- Direction of information flow: DFL passes learned parameters into a decision model and trains on regret; inverse MOO learns the decision model (weights/objectives) from decisions; GP-in-ML (Repetto et al.) uses GP to combine learned predictors. No paper read connects all three.
- Scalarization: Li et al. and Dinh et al. rely on weighted-sum or OWA aggregates; Dhakal & Lachner argue scalarization misses non-convex fronts and use preference-targeted Pareto points. GP's aspiration-level deviation structure is absent from all three [inferred; no read paper uses goal constraints with deviation variables inside DFL].
- Problem class: all multiobjective DFL experiments are linear/combinatorial with parameters in the objective. The survey says most DFL techniques cannot handle non-linear objectives (Mandi et al., Sec. 6, p. 53) and that predicting constraint parameters is only partly solved (Sec. 3.3.3).
- Treatment of uncertainty: DFL minimises expected regret; inverse MOO offers a distributionally robust variant (Dong & Zeng 2020); uncertain GP assumes known parameter distributions (Liu & Chen). Robust DFL is called sparse by Mandi et al. (p. 54).

### Gaps (author-stated unless marked [inferred])
1. Non-linear objectives in DFL: "Most DFL research has focused on optimization problems with linear objective functions" (Mandi et al., Sec. 6, p. 53). Cobb-Douglas outcome models are non-linear in spending (log-linear in parameters) [inferred relevance].
2. Robust, risk-sensitive DFL: "the literature on robust DFL remains sparse" (Mandi et al., Sec. 6, p. 54).
3. Multiobjective DFL is nascent: "Current research in multi-objective optimization and decision-focused learning remains limited" (Li et al., Sec. 7); ParetoSPO says extension to multi-objective "remains unexplored" (Dhakal & Lachner, Sec. 1), and lists scalability in the number of preferences and no generalisation to unseen preferences as limitations (Sec. 6).
4. Parameters in goal constraints (targets and coefficients inside constraints) are the hard case for DFL (Mandi et al., Sec. 3.3.3) [GP puts learned coefficients in goal constraints, so this applies; inferred].
5. Inverse MOO limitations: identifiability of weights, strong data requirements (KKT multipliers) (Gebken & Peitz, Sec. 6); regularity conditions for regret bounds (Wang et al., Conclusion); sensitivity to misspecified decision structure and data quality (Dong & Zeng 2020, Abstract).
6. Learned-then-optimised budget pipelines ignore estimation error in the optimisation (Zhao et al. propose no such step; authors list other future work only, Sec. 6) [inferred].
7. [inferred] I found no read paper that (a) feeds learned economic elasticities (Cobb-Douglas or similar) into a GP, (b) propagates their estimation uncertainty into goal attainment, or (c) evaluates decision regret of a GP plan. The Bae et al. 2026 abstract (goal-based investing, DFL, GP decision-quality metric) is the nearest and must be read before claiming novelty on the DFL-for-GP point.

### Coverage caveat
Searches used arXiv API (title/abstract queries), OpenAlex (until its free budget ran out), Crossref and web search. Not found, but not proven absent: other DFL-for-multiobjective papers in OR journals, robust/stochastic GP full texts (all found were paywalled or blocked), and forecasting-plus-GP papers outside the 2026 OPSEARCH record. A follow-up search on Scopus/Web of Science for "goal programming" with "machine learning/neural network/forecast/regression" is recommended before finalising novelty claims.
