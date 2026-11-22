# Cluster B: inverse multiobjective optimization and inverse goal programming (2026-11-22)

Scope: papers that infer weights, targets, priorities or objective parameters from observed decisions, with attention to inverse goal programming (GP) and to identifiability. Complements notes 02 (section B there summarises Dong & Zeng and Gebken & Peitz at lower depth; they are re-read here).

How papers were obtained: arXiv PDFs (pdftotext), Author Accepted Manuscript at U Toronto TSpace (Chan et al. 2014), PMC (Naghavi et al.), journal PDF from the Thamar University site (Saif & Weber). Elsevier/ScienceDirect, SSRN and Springer (Roland et al.) blocked automated retrieval; for these only metadata/abstract was obtained and they are listed in "Not read in full" and never described beyond what the abstract says. The arXiv search API returned few hits for GP-related queries, OpenAlex hit its daily budget, so coverage is not systematic. Downloads are in /tmp/litB/.

Read scope key: "full" = read through, proofs excluded; "partial" = sections named.

---

## A. Inverse goal programming and GP-like inverse models

### A1. Saif & Weber - Inverse Linear Goal Programming Problem
- Citation: Saif N.M.A., Weber G.-W. Inverse Linear Goal Programming Problem. Thamar University Journal of Natural & Applied Sciences, 2010, vol. A(3), 67-76 (journal header; Crossref lists the record with year 2023, vol. 3(3), DOI 10.59167/tujnas.v3i3.1284, so the year is uncertain). PDF: https://journal.tu.edu.ye/index.php/TUJNAS/article/download/1284/1036
- Read scope: full (10 pp.); equations are garbled in pdftotext, so formulation was reconstructed from text and the dual (3)-(11).
- WHY: extend Ahuja-Orlin inverse optimization to linear goal programming with several goals.
- HOW: forward model is a weighted LGP min sum_i (w_i^+ d_i^+ + w_i^- d_i^-) s.t. c_i x + d_i^- - d_i^+ = b_i (goal i) and a_j x <= b_j, with goal levels b_i fixed. Given a feasible (x0, d0), find the smallest L1 change of the weight vectors w^+, w^- making (x0, d0) optimal. Uses the LP dual (dual variables bounded by the weights, -w^- <= y <= w^+), restricts to the binding constraints, and obtains closed-form weight updates (eqs. 8-11). Specialised to an inverse multi-objective assignment problem.
- WHAT: the inverse GP under L1 norm reduces to a problem of the same kind. No numerical experiment, no real data, single observation, no noise, no statistics, no inference of goal levels.
- Formulation: forward = weighted LGP; inferred = deviation weights only (b fixed); loss = L1 distance of weights to given prior weights; exact consistency (observation must be optimal).
- Guarantees/assumptions: exact optimality of the observation; L1 norm; LP structure; no guarantee beyond reduction.
- Application: assignment problem (illustrative).
- Relevance: the only paper retrieved with "inverse goal programming" in the title. It fixes targets and infers (adjusts) weights. Closest in model class, far from our setting (panel data, noise, targets).

### A2. Chan, Craig, Lee & Sharpe (2014) - Generalized inverse multiobjective optimization
- Citation: Chan T.C.Y., Craig T., Lee T., Sharpe M.B. (2014). Generalized Inverse Multiobjective Optimization with Application to Cancer Therapy. Operations Research 62(3):680-695. DOI 10.1287/opre.2014.1267. Author manuscript: https://utoronto.scholaris.ca/bitstreams/3935ea3b-8caa-4a72-9ab6-5db1643206f1/download
- Read scope: abstract, introduction, clinical formulation (Sec. 2, Table 1), Sec. 3.1-3.5 (formulation, Props. 1-5, Thm 1, Cor. 2); computational section and appendix skimmed only.
- WHY: standard inverse LP returns the zero vector or is infeasible if the observed plan is interior or infeasible; radiation-therapy weights are set by trial and error.
- HOW: forward = weighted-sum MOLP min alpha'Cx s.t. Ax=b, x>=0. Inverse replaces strong duality by a duality gap: GIOP_r (relative gap, alpha'Cx_hat = eps_r b'p) and GIOP_a (absolute gap), solved as LPs. The gap minimisation is interpreted as the dual of Benson's method.
- WHAT: Thm 1: the optimal alpha* is exactly the optimal inverse solution for a projected point Cx* = Cx_hat/eps_r* (or Cx_hat - eps_a* e) on the weakly nondominated set. Cor. 2: alpha* is unique iff Cx* lies in the relative interior of a facet of the Pareto surface; at a vertex or on a lower-dimensional face many weight vectors fit. On prostate cases, a few objectives with inverse weights give clinically acceptable plans, and influential objectives are identified.
- Formulation: forward = weighted sum of known linear criteria; inferred = weights only; loss = relative or absolute duality gap; single observation.
- Guarantees: geometric (projection and uniqueness characterisation); no statistical guarantees.
- Application: prostate IMRT. The clinical formulation (Sec. 2.2, Table 1) already has goal-programming structure: each criterion is a dose threshold (aspiration) and violations are penalised, with weights. The paper infers weights and keeps thresholds fixed.
- Relevance: key template for weights from one observed allocation, and the explicit uniqueness statement (Cor. 2) is the identifiability result we need to reuse for weights at a vertex of the attainable set.

### A3. Chan & Lee (2018) - Trade-off preservation in inverse multiobjective convex optimization
- Citation: Chan T.C.Y., Lee T. (2018). Trade-off preservation in inverse multi-objective convex optimization. European Journal of Operational Research 270(1):25-39. DOI 10.1016/j.ejor.2018.02.045; arXiv:1706.06926 (read). https://arxiv.org/abs/1706.06926
- Read scope: abstract, introduction, background (Sec. 2 incl. Examples 2.1-2.2), Sec. 3.1-3.2 (definitions, Thm 3.1), conclusion; clinical experiments not read.
- WHY: approximate inverse models return a weight vector but do not say how the observed non-Pareto point is moved to the Pareto set; the move should respect the decision maker's trade-offs.
- HOW: forward = convex weighted sum min sum alpha_k f_k(x). Define "trade-off preservation": the projected Pareto point satisfies f_k(x*) - f_k(x_hat) = mu_k * eps for scaling factors mu (relative: mu_k = f_k(x_hat); absolute: mu_k = 1). Inverse problem min eps s.t. mu_k eps >= f_k(x) - f_k(x_hat), x feasible; the weights are the Lagrange multipliers of those constraints (Thm 3.1).
- WHAT: model is convex, specialises to Chan et al. 2014 (duality gap) and Keshavarz et al. 2011. [inferred] The absolute version, min eps s.t. f_k(x) <= f_k(x_hat) + eps, is a Chebyshev deviation problem with target vector equal to the observed outcomes, so the multipliers are the Chebyshev weights; this is the closest formal bridge to GP found.
- Formulation: inferred = weights; loss = trade-off-preserving optimality gap; single observation.
- Guarantees: exactness of the equivalence (Thm 3.1); no statistics. Assumes known convex criteria, positive f_k, Slater.
- Application: prostate cancer plans.
- Relevance: gives a principled way to handle observed allocations that are not on the model's Pareto set (our districts will not be exactly optimal for any model).

### A4. Naghavi, Foroughi & Zarepisheh (2019) - Inverse optimization for multi-objective linear programming
- Citation: Naghavi M., Foroughi A.A., Zarepisheh M. (2019). Inverse optimization for multi-objective linear programming. Optimization Letters (2019; volume/pages not verified; DOI 10.1007/s11590-019-01394-0). Author manuscript: https://pmc.ncbi.nlm.nih.gov/articles/PMC9175571/
- Read scope: abstract, introduction, Sec. 2-4 (formulation, Lemma 2, Thm 2), conclusion.
- WHY: classical inverse LP perturbs costs to make a point optimal; the multiobjective analogue (Pareto optimality) had not been done in general.
- HOW: IMOLP: min ||C - C_hat|| s.t. x_hat is weakly efficient for MOLP(C_hat). By the weighted-sum theorem, x_hat weakly efficient iff exists w in the simplex with w C_hat in the cone of active constraint normals K_hat. The problem is non-convex because of w times C_hat.
- WHAT: Thm 2: an optimal solution exists that changes only one criterion row; d(conv(C), K_hat) is a lower bound, giving an algorithm that solves a series of convex problems (one per objective).
- Formulation: forward = MOLP; inferred = the criteria matrix (not weights); loss = matrix norm. Weights are existential, not reported.
- Guarantees: exact (no noise); the conclusion states results hold only if the criteria matrix can be modified without restriction.
- Application: numerical illustration only.
- Relevance: different inferred object (coefficients, not preferences). The characterisation w in simplex with w C_hat in K_hat is exactly the set of consistent weights for an LP forward model, a polyhedral cone; this is our identifiability set.

### A5. Ahmadi, McNutt & Ghobadi (2024) - Improving observed decisions' quality using inverse optimization
- Citation: Ahmadi F., McNutt T.R., Ghobadi K. (2024). arXiv:2407.14438v1. Venue not found (preprint). https://arxiv.org/abs/2407.14438
- Read scope: abstract and introduction only; model section skimmed.
- WHY: constraint thresholds of treatment planning may be too tight, so the observed plan is not best possible, but the planner's preferences should be preserved.
- HOW: inverse optimization model that projects an observed solution onto desired hyperplanes or expands the feasible set while keeping distance to the observed decision small.
- WHAT: on four prostate cases, dose-volume histograms improve with target coverage maintained.
- Relevance (weak): changes thresholds (constraint right-hand sides) rather than inferring them from many decisions; shows threshold-type parameters can be treated as variables in an inverse model. Not read deeply.

---

## B. Statistical inverse multiobjective optimization (weights/parameters from many noisy decisions)

### B1. Dong & Zeng (2018) - Inferring parameters through inverse multiobjective optimization
- Citation: Dong C., Zeng B. (2018). arXiv:1808.00935v1. No journal version found. https://arxiv.org/abs/1808.00935
- Read scope: abstract, introduction and literature review, Sec. 2 (formulation), Sec. 4 (identifiability: Defs 6-7, Thm 5, Props 8, Alg. 1, Sec. 4.4), Sec. 7 conclusion, experiment set-up. Consistency proofs (Sec. 3, appendix) not read.
- WHY: single-objective inverse optimization treats scatter of decisions as noise, but decisions may be trade-offs of several criteria.
- HOW: forward = convex multiobjective DMP min_x {f_1(x,theta),...,f_p(x,theta)} s.t. x in X(theta). Observations y_i are noisy efficient points. Loss l(y,theta) = min distance from y to the efficient set X_E(theta). Since every efficient point of a convex problem solves a weighted-sum problem (their Prop. 2), X_E is approximated by solutions of weighted sums with K sampled weights (surrogate loss l_K, IMOP-EMP-WS); weights are latent per observation and are not identified individually. Solved by KKT-based MINLP, ADMM and a K-means-like algorithm.
- WHAT: risk consistency and uniform convergence in N and K (Props 3-7); parameter consistency under identifiability (Thm 5, noise-free, strongly convex f). Definition 7: DMP is identifiable at theta if X_E(theta) is not covered by X_E(theta') for any other theta'. Prop. 8: two different strongly convex MQPs (Examples 1-2) have the same efficient set, so are not distinguishable; Alg. 1 tests identifiability from data; Sec. 4.4 lists three remedies (more data, partial knowledge of weight-decision map, known parameter subsets). Authors also recover the distribution of weights across decision makers.
- Formulation: inferred = parameters of objectives and constraints (theta) plus a distribution over weights; loss = distance to efficient set (weights marginalised out).
- Guarantees/assumptions: convexity, compact Theta, bounded support, strong convexity for parameter consistency; no noise for Thm 5.
- Application: synthetic MQP, portfolio data.
- Relevance: strongest identifiability treatment for multiobjective inference. Its efficient-set loss is deliberately agnostic to which weights generated each decision, which is what we want when weights vary by district and year. It requires smooth strongly convex objectives, which GP deviation terms (|g - b|) are not [inferred].

### B2. Dong, Chen & Zeng (2018) - Generalized inverse optimization through online learning
- Citation: Dong C., Chen Y., Zeng B. (2018). arXiv:1810.01920v2 (preprint; publication venue not verified). https://arxiv.org/abs/1810.01920
- Read scope: abstract, introduction, related work, regret theorem statement (Thm 3.2), conclusion.
- WHY: batch inverse optimization does not scale or work online.
- HOW: implicit online update of the preference/constraint parameters given (signal u_t, noisy decision y_t) pairs, with loss = distance of y_t to the model's optimal set.
- WHAT: O(sqrt(T)) regret and statistical consistency under regularity assumptions (strong convexity, bounded sets, Lipschitz in theta).
- Relevance: single-objective predecessor of B3, signal-dependent (context u_t): a budget envelope per district-year is such a signal.

### B3. Wang, Dong & Zeng - Learning multiobjective program through online learning
- Citation: Dong C., Wang Y., Zeng B. arXiv:2010.06140v2 (Dec 2022; v1 title "Inverse Multiobjective Optimization Through Online Learning"; marked "Paper under review"). https://arxiv.org/abs/2010.06140
- Read scope: abstract, introduction, formulation, Assumptions 3.1-3.3, Lemma 3.1, Thm 3.2, experiments (MQP, portfolio), conclusion (Sec. 5).
- WHY/HOW: same IMOP loss (distance to efficient set, surrogate with sampled weights) learned sequentially with implicit updates.
- WHAT: Thm 3.2: regret R_T <= 4 sqrt(2)(B+R) D kappa sqrt(T)/lambda under strong convexity (lambda), Lipschitz change of w'f in theta (kappa) and a convex-combination Assumption 3.3. Conclusion: relax the conditions; view as a contextual bandit.
- Relevance: sequential updating of preference parameters as fiscal years arrive. The theory needs strong convexity, which excludes linear and L1-goal objectives (the fast-converging experiments are on QP).

### B4. Dong & Zeng (2021) - Wasserstein distributionally robust inverse multiobjective optimization
- Citation: Dong C., Zeng B. (2021). AAAI-21, 35(7). DOI 10.1609/aaai.v35i7.16739; arXiv:2009.14552. https://arxiv.org/abs/2009.14552
- Read scope: abstract, introduction, Defs 2.2-2.3, Sec. 3 assumptions, Lemma 3.1, Remark 3.6, conclusion.
- WHY: IMOP is sensitive to misspecification and poor data.
- HOW: minimise worst-case expected distance-to-efficient-set loss over a Wasserstein ball around the empirical distribution of decisions; semi-infinite program solved by cutting planes.
- WHAT: excess risk bound O(1/sqrt(N)) that, as the authors note (Remark 3.6), does not depend on the radius of the Wasserstein ambiguity set because the proof uses Lipschitz continuity of the loss; bounded support of decisions is assumed and flagged as restrictive (authors' future work: light tails).
- Relevance: template for carrying observation noise into the inferred preferences; our district data have heavy tails [inferred], so the bounded-support assumption is a real limitation.

### B5. Gebken & Peitz (2021) - Inverse multiobjective optimization: inferring decision criteria from data
- Citation: Gebken B., Peitz S. (2021). Journal of Global Optimization 80:3-29. DOI 10.1007/s10898-020-00983-z; arXiv:1901.06141. https://arxiv.org/abs/1901.06141
- Read scope: abstract, introduction, definition of extended Pareto critical sets, algorithm summary, conclusion/outlook (arXiv v1).
- WHY/HOW: treat the objective vector as unknown in the multiobjective KKT system with KKT multipliers alpha (the weights) given in the data; express objectives in a finite basis; solve a homogeneous linear system by SVD (Algorithm 1).
- WHAT: reconstructs objectives from clean or noisy data, also used for surrogate models. Outlook (Sec. 6): only k=2 objectives and n=2 variables tested; monomial bases only. The result is non-unique (null space).
- Relevance: needs the weights as data, which we do not have; useful as a contrast case and for the non-uniqueness statement.

### B6. Carrizosa, Gomez-Vargas & Piccialli (2026) - clustering-based preference inference (abstract only)
- Citation: Omega (2026), DOI 10.1016/j.omega.2026.103675 (hybrid open access, ScienceDirect blocked the PDF). Abstract retrieved from OpenAlex.
- Abstract-level content: inverse multiobjective optimization that clusters decision makers by preference structure rather than by decisions, minimises regret of observed decisions under the inferred preference structure (MIQP), adds interpretability requirements and a warm-start heuristic; validated on synthetic data and a diet recommendation problem.
- Relevance: the most recent preference-inference work found; heterogeneous decision makers (districts) fit our setting. Must be read in full before any novelty claim about clustered weights.

---

## C. General inverse optimization theory used for identifiability, consistency and generalisation

### C1. Aswani, Shen & Siddiq (2018) - Inverse optimization with noisy data
- Citation: Operations Research (2018; volume/pages not verified); DOI 10.1287/opre.2017.1705; arXiv:1507.03266v4 (read). https://arxiv.org/abs/1507.03266
- Read scope: abstract, introduction, definitions of risk and estimation consistency, identifiability condition IC, Appendix B.
- WHY/HOW: bilevel predictability-loss inverse problem with noisy optimal solutions; NP-hard; duality-based reformulation with regularisation (epi-convergence).
- WHAT: risk consistency and, under IC, estimation consistency. IC requires (i) y = xi + w noise with xi in S(u, theta0), (ii) different theta give different solution sets on a positive-probability set of signals u, (iii) multivalued solution sets have probability zero. Appendix B example: FOP-II, min (x - theta)^2 s.t. x <= 1, is not identifiable (if y = 1, any theta in [1,2] fits), but adding an exogenous signal u (FOP-III: min (x - theta - u)^2, x <= 1) restores identifiability when P(u <= -1) > 0.
- Relevance: FOP-II is the aspiration-level problem in miniature: a target theta beyond a binding cap is unidentifiable from the decision, and variation in an exogenous context (budget, enrolment) is what restores identifiability. We use this as the template for the GP identifiability argument below.

### C2. Mohajerin Esfahani, Shafieezadeh-Abadeh, Hanasusanto & Kuhn (2018) - Data-driven inverse optimization with imperfect information
- Citation: Mathematical Programming (2017 online, print 2018; volume/pages not verified); DOI 10.1007/s10107-017-1216-6; arXiv:1512.05489v2. https://arxiv.org/abs/1512.05489
- Read scope: abstract, introduction, Defs 2.3-2.4, Remark 2.5-2.6, summary of contributions.
- HOW/WHAT: suboptimality loss l_theta(s,x) = F_theta(s,x) - min_y F_theta(s,y); distributionally robust (Wasserstein) minimisation with out-of-sample guarantees; tractable convex programs for linear F. Remark 2.5: even with a correct model class, with moderate sample size multiple parameters have zero in-sample risk and the returned theta0 may differ from the true theta*.
- Relevance: suboptimality loss is the natural fit measure for a GP objective F(x; w, b) = sum_i w_i |g_i(x) - b_i| with unknown (w, b): no solver for the true model is needed to evaluate loss on the data. Convexity of the joint (w, b) problem is not established here [inferred: unlikely, product terms].

### C3. Chan, Lee & Terekhov (2019) - Closed-form solutions, geometry, goodness of fit
- Citation: Management Science (2019; volume/pages not verified); DOI 10.1287/mnsc.2017.2992; arXiv:1511.04650v2. https://arxiv.org/abs/1511.04650
- Read scope: abstract and introduction; the multiobjective remark (employing the forward and inverse multiobjective formulation of Chan et al. 2014) skimmed.
- WHAT: unified inverse linear model with a goodness-of-fit metric rho (coefficient of complementarity, like R^2). Relevance: a candidate fit statistic for how well a GP model explains observed allocations.

### C4. Chan, Mahmood & Zhu (2025) - Inverse optimization: theory and applications (survey)
- Citation: Operations Research (2025), DOI 10.1287/opre.2022.0382; arXiv:2109.03920v2. https://arxiv.org/abs/2109.03920
- Read scope: abstract, introduction; Sec. 4 consistency and the multiobjective paragraph (Sec. 4.5); applications (finance, healthcare, etc.); conclusion (Sec. 8, p. 46). Searched the full text for goal programming, lexicographic, aspiration: no occurrence. "Multi-objective" appears in the DRO paragraph on Dong & Zeng and in routing/preferences applications.
- WHAT: states that parameter consistency needs identifiability assumptions such as a strictly convex forward objective (Aswani et al.). Stated open directions (Sec. 8): scalability (every data point with its own feasible region adds variables and constraints) and incorporating distributional information.
- Relevance: evidence (negative search result in a 46-page survey) that inverse GP is not an established subfield.

### C5. Zattoni Scroccaro, Atasoy & Mohajerin Esfahani (2025) - Incenter cost and augmented suboptimality loss
- Citation: Operations Research (2025), DOI 10.1287/opre.2023.0254; arXiv:2305.07730v2. https://arxiv.org/abs/2305.07730
- Read scope: abstract, introduction, Sec. 2-3.1 (consistent cost set C, circumcenter, incenter definition).
- WHAT: the set of cost vectors consistent with the data is a cone (Def. 2.2); picking an arbitrary nonzero point is arbitrary. The incenter selects the most interior (robust) consistent cost, with convex reformulation; Augmented Suboptimality Loss extends it to inconsistent data; Python package InvOpt.
- Relevance: a principled tie-break among non-unique weight vectors on a non-unique Pareto face. Applies directly to the cone of consistent GP weights.

### C6. Besbes, Fonseca & Lobel (2025) - Contextual inverse optimization
- Citation: Operations Research (2025), DOI 10.1287/opre.2021.0369; arXiv:2106.14015v3. https://arxiv.org/abs/2106.14015
- Read scope: abstract, Sec. 1.1 contributions, Sec. 3.2 (uncertainty angle, circumcenter), conclusion.
- WHAT: from observed optimal actions in changing contexts, characterise the set C(D) of consistent cost vectors; worst-case regret for any future problem is sin(alpha(C(D))), alpha = uncertainty angle (1 if alpha > pi/2); offline minimax policy is the circumcenter; naive online circumcenter can have linear regret; a logarithmic cumulative regret algorithm. Handles multiple optimal solutions by worst-case over ties (Sec. 3).
- Relevance: gives a decision-relevant (regret) view of non-identifiability: we need not identify weights if the induced allocations are insensitive within C(D). Future work stated: dimension dependence, impossibility results, noisy feedback (Sec. 7, line ~1401).

### C7. Fatemi, Maskan, Sra & Mohajerin Esfahani (2026) - Tight generalization bounds for noiseless inverse optimization
- Citation: arXiv:2605.08866v2 (4 Nov 2026), NeurIPS 2026 (as printed on the PDF). https://arxiv.org/abs/2605.08866
- Read scope: abstract, introduction and contributions, Sec. 2 (set-level and action-level mismatch, tie handling), remarks near the incenter estimator, future-work remark.
- WHAT: O(d/T) high-probability bound on set-level mismatch P(a_theta*(s) not in A_theta_hat(s)) for any consistent estimator (scenario-program view); action-level bound via an incenter estimator that promotes uniqueness of the chosen action; matching lower bound; ties on the boundary of the consistent cone can persist on unseen states. Future work: approximate (noisy) demonstrations.
- Relevance: first tight sample-complexity statement for IO; the d/T rate with d = number of unknown weights plus targets gives a back-of-envelope for how many district-years are needed (noiseless case only).

### C8. Li (2021) - Inverse optimization of convex risk functions
- Citation: Management Science (2021; volume/pages not verified); DOI 10.1287/mnsc.2020.3851; arXiv:1607.07099v2. https://arxiv.org/abs/1607.07099
- Read scope: abstract and introduction only.
- WHAT: non-parametric inverse framework recovering a convex risk function that makes observed portfolio decisions optimal, optionally using pairwise comparisons elicited from the decision maker as extra information; reformulated as convex programs.
- Relevance (weak): precedent for combining revealed decisions with elicited comparisons; relevant if a GP-form class is replaced by a monotone convex aggregator.

---

## Not read in full (metadata or abstract only)
| Paper | DOI | What was obtained | Why it matters |
|---|---|---|---|
| Roland, De Smet & Figueira (2013), Inverse multi-objective combinatorial optimization, Discrete Applied Mathematics | 10.1016/j.dam.2013.04.024 | metadata; described second-hand by Dong & Zeng 2018 (Sec. 1.1: minimal adjustment of objective coefficients so that a given set of feasible solutions becomes efficient; branch-and-bound and cutting planes, not numerically evaluated) | first inverse MOCO paper |
| Roland, De Smet & Figueira (2012), stability radius for MOCO by inverse optimization, 4OR | 10.1007/s10288-012-0215-y | abstract (Springer page): stability radius of an efficient solution under Chebyshev-norm adjustment of objective coefficients | sensitivity of efficiency to coefficients |
| Roland, Figueira & De Smet (2016), compromise solutions in project portfolio selection with multiple experts by inverse optimization, Computers & Operations Research | 10.1016/j.cor.2015.07.006 | metadata only | MCDM group compromise via inverse optimization; likely closest to MCDM-weight inference |
| Carrizosa et al. (2026), Omega | 10.1016/j.omega.2026.103675 | abstract (OpenAlex) | recent IMO preference clustering |
| Karami-Fard (2026), "Need, Alignment, or Commerce? Recovering the Revealed Priorities of Foreign Aid Donors through Inverse Optimization", SSRN | 10.2139/ssrn.7302189 | title and author via Crossref; SSRN blocked (403) | revealed priorities of budget allocators via inverse optimization: possibly the closest application precedent for public budgets; read first |
| Mohanty & Vijayaraghavan (1995), A multi-objective programming problem and its equivalent goal programming problem with appropriate priorities and aspiration levels: a fuzzy approach, Computers & OR | 10.1016/0305-0548(94)00066-h | title via Crossref | forward direction (find GP priorities and aspiration levels equivalent to an MOP); related to the inverse GP idea |
| Rao, Tiwari & Mohanty (1988), A preference structure on aspiration levels in a GP problem, Fuzzy Sets and Systems | 10.1016/0165-0114(88)90185-6 | title via Crossref | aspiration levels as preference |
| Ahmadi, Dai & Ghobadi (2022), You Are What You Eat: A Preference-Aware Inverse Optimization Approach, SSRN | 10.2139/ssrn.4298746 | title via Crossref | preference-aware IO |

Cited-for-orientation only, not retrieved: Ahuja & Orlin (2001, Oper. Res. 49(5)), Keshavarz, Wang & Boyd (2011), Bertsimas, Gupta & Paschalidis (2015).

---

## Synthesis

### (a) Does inverse goal programming (joint inference of weights and aspiration levels) exist?
- Explicit "inverse goal programming": one paper found, Saif & Weber (A1). It adjusts the deviation weights of a linear GP so that one given feasible solution becomes optimal, with targets b fixed, exact optimality, no noise, no data, no numerical results.
- Joint inference of weights and aspiration levels from observed decisions: not found in anything retrieved. Evidence: the 2025 Operations Research survey (C4) contains no mention of goal programming, lexicographic or aspiration; none of the 18 papers read infers goal levels. This is a negative result from a non-systematic search (arXiv API and OpenAlex were weak for this query; Elsevier/SSRN papers unread), not proof of absence.
- Closest constructions: (i) Chan et al. 2014 (A2): clinical objectives are thresholds with penalised violations (GP structure) but only weights are inferred, thresholds fixed. (ii) Chan & Lee (A3): the absolute trade-off preservation model is [inferred] a Chebyshev deviation from a target equal to the observed outcome vector, with weights as multipliers. (iii) Dong & Zeng (B1, B3, B4): infer parameters theta of objectives and constraints, which could in principle include target parameters, but require smooth strongly convex objectives. (iv) Ahmadi et al. (A5): treats constraint thresholds as adjustable. (v) Mohanty & Vijayaraghavan 1995 and Karami-Fard 2026 (not read) are the two unread items most likely to contradict or sharpen this conclusion. Lexicographic priority inference: no paper retrieved addresses it.

### (b) Identifiability of weights and targets in GP from observed solutions
Read evidence:
- Weights, known targets, LP forward: the consistent weights form a polyhedral cone (Naghavi A4 Lemma 2; Zattoni Scroccaro C5 Def. 2.2; Chan et al. A2). Cor. 2 of A2: unique (after normalisation) iff the projected point is in the relative interior of a facet of the attainable set; at vertices or low-dimensional faces, a whole set of weights fits. Generic noisy data land in the interior of facets, so uniqueness is likely for a single observation under continuous noise but fragile [A2 states the likelihood is low of hitting a non-facet-interior point in their computations].
- Even strictly convex smooth MOPs can be non-identifiable (Dong & Zeng Prop. 8, Examples 1-2); identifiability is defined through efficient sets (Def. 7) and remedied by more data, partial knowledge of weight-decision map, or known parameter subsets (Sec. 4.4).
- A target beyond a binding constraint is not identifiable from the decision (Aswani et al., Appendix B, FOP-II), and exogenous variation in context restores identifiability (FOP-III; condition IC).
- Ties and non-uniqueness are best handled by choosing the incenter (C5, C7) or by worst-case/regret reasoning (circumcenter, C6).
Inferred consequences for GP [inferred, not proved in any paper read]:
1. Under pure under-achievement deviations (all goals unmet), the GP objective is linear in outcomes, sum_i w_i (b_i - f_i(x)), so targets drop out and the problem is inverse weighted-sum; targets are only bounded below (b_i >= f_i(x_hat)). Targets become informative only through the kink, i.e. goals attained exactly (d_i = 0) or over-attained, which gives a weight interval rather than a point.
2. For Chebyshev GP, min max_i w_i (b_i - f_i(x)), an observation fixes only the products w_i (b_i - f_i(x_hat)) among active goals; weights and targets are confounded up to that product (by standard reference-point scalarisation theory, which was not retrieved), so one observation identifies neither separately.
3. Variation across district-years in budget constraints and context (the signal u of Aswani/Besbes) plus an assumption of common weights/targets (or a low-dimensional heterogeneity structure, cf. Dong & Zeng weight distributions, Carrizosa et al. clustering) is the realistic route to identification. The Fatemi et al. bound O(d/T) (noiseless) suggests T must scale with the number of weights plus targets.
4. The inferred object may best be the allocation-relevant set (set-level mismatch, C7; regret, C6) rather than point estimates of (w, b).

### (c) Open problems stated by the authors (locators)
- Scalability when each data point has its own feasible region; incorporating distributional information: Chan, Mahmood & Zhu 2025, Sec. 8, p. 46.
- Higher-dimensional examples and better bases than monomials; non-uniqueness of the recovered objective: Gebken & Peitz, Sec. 6 (arXiv v1 pp. 18-19).
- Relaxing the regularity conditions of the regret bound; contextual-bandit view: Dong, Wang & Zeng, Sec. 5; relaxing bounded support to light tails: Dong & Zeng 2021, Remark 3.6.
- Results hold only when the criteria matrix can be changed without restriction: Naghavi et al., Sec. 5.
- Dimension dependence of regret, impossibility results, noisy feedback: Besbes et al., conclusion (line ~1401 of the PDF text); approximate/noisy demonstrations: Fatemi et al., Remark after eq. (19).
- Choice of weight normalisation matters for the inferred weights (illustrated in Chan & Lee Examples 2.1-2.2, Sec. 2.3).
- [inferred] Not addressed anywhere read: nonsmooth (L1/goal) forward objectives in the statistical IMOP theory (all regret and consistency proofs assume strong convexity or linear structure); joint (w, b) estimation; lexicographic priorities; panel data with common preference and varying budget envelope; use of external causal estimates of effects as the known model (our forward model).

### Relevance to the project (summary) [inferred]
Treat the district allocation as a weighted GP forward model whose goals and weights are unknown; use the suboptimality loss (C2) or Chan-Lee trade-off-preserving loss (A3) for fit, Aswani IC and Dong & Zeng Def. 7 to state identifiability conditions, an incenter selection (C5) for non-unique weights, and Besbes regret (C6) as the decision-relevant uncertainty measure. Highest-priority downloads: Karami-Fard SSRN 2026, Roland et al. 2013 and 2016, Carrizosa et al. 2026 (full text), Mohanty & Vijayaraghavan 1995.
