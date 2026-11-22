# Cluster 05: inverse optimization theory and data-driven methods

Compiled 2026-11-22. Papers were downloaded to /tmp/litA/ and read with pdftotext. "Read scope" says what was actually read. Nothing below is cited from memory; every item was retrieved (PDF, arXiv abstract, publisher metadata via Crossref, or an author page) and checked. Statements marked [inferred] are mine, not the authors'. Theorem numbers refer to the version I read (arXiv version named in each entry); journal numbering may differ.

Notation used throughout. Forward problem FOP(theta; s): min over x in X(s) of F_theta(s, x), with context/signal s, decision x, and parameter theta to be learned. Observations (s_i, x_i), i = 1..N.

Project mapping used in the relevance lines. Forward model = a goal program (GP) for a state: x = allocation across spending categories/districts, theta = goal weights and/or aspiration levels (and possibly lexicographic priorities), s = state-year context (enrollment, revenue by source, constraints). Observation = realised allocation.

---

## 1. Papers read

### 1.1 Ahuja & Orlin 2001 (metadata and abstract only)

- Citation: R. K. Ahuja and J. B. Orlin, "Inverse Optimization", Operations Research 49(5):771-783, 2001. DOI 10.1287/opre.49.5.771.10607. https://doi.org/10.1287/opre.49.5.771.10607
- Read scope: Crossref metadata and the abstract (retrieved from api.crossref.org). The full text is paywalled (INFORMS); not read. Its content below is the abstract plus how three later papers describe it (Chan et al. review Sec. 3.1.1; Esfahani et al. Sec. 1; Fatemi et al. Sec. 1).
- WHY: given a feasible x0 and a cost vector c, perturb c to d so that x0 becomes optimal and ||d - c||_p is minimal.
- HOW: for LP, optimality of x0 is characterised by complementary slackness, so the inverse problem is itself an LP under L1 and L-infinity norms. Network problems (shortest path, assignment, min cut, min-cost flow) reduce to problems of the same or a closely related kind.
- WHAT: results (i)-(v) in the abstract: inverse LP is an LP under L1/L-inf; inverse shortest-path/assignment/min-cut are of the same kind; inverse min-cost flow reduces to unit-capacity min-cost flow or min-mean-cycle; if P is polynomially solvable with linear costs, so is its inverse under L1/L-inf.
- Key formulation: single observation; forward = LP or combinatorial; infers cost vector; loss = norm distance from a prior cost c ("closest cost that makes x0 optimal"). Exact fit, no noise model.
- Statistical guarantees: none (deterministic, one observation).
- Relevance: the prior-anchored formulation is the template for "closest weights to the stated policy weights that rationalise the observed budget". It cannot handle 10 years x 50 states of noisy data without the data-driven extensions below.

### 1.2 Keshavarz, Wang & Boyd 2011

- Citation: A. Keshavarz, Y. Wang, S. Boyd, "Imputing a convex objective function", Proceedings of the 2011 IEEE International Symposium on Intelligent Control (part of IEEE Multi-Conference on Systems and Control), pp. 613-619. DOI 10.1109/ISIC.2011.6045410. PDF: https://web.stanford.edu/~boyd/papers/pdf/imputed_objective_msc.pdf
- Read scope: full text (7 pages).
- WHY: recover an unknown convex objective from observed (approximately) optimal decisions at several parameter values, e.g. consumer utility from purchases.
- HOW: write f = sum_i alpha_i f_i over known convex basis functions; treat the KKT conditions as linear in (alpha, lambda, nu) and minimise a convex penalty phi of the stationarity and complementarity residuals (their problem (3)). Normalisation (alpha_0 = 1, i.e. one fixed part of the objective) removes the trivial solution alpha = 0 (Sec. III).
- WHAT: a convex program in (alpha, lambda^(k), nu^(k)); examples include consumer demand and a controller-complexity application.
- Key formulation: forward = convex program with known constraints g_i, A(p), b(p); inferred = nonnegative weights alpha on basis functions; loss = KKT residual penalty phi(r_stat, r_comp) (primal residuals are not in the objective because data are taken as feasible).
- Guarantees: none. No theorem. The paper itself notes non-uniqueness (any increasing convex transform of a consistent f is consistent) and non-existence of exactly consistent objectives under noise (Sec. II).
- Caveat from later work: the KKT-residual method is statistically inconsistent under noise in the decision data (Aswani et al. 2018, Prop. 1 and Cor. 2, section 1.4 below).
- Relevance: this is the natural first estimator for goal weights because a GP is an LP with deviation variables (an affine basis; weights nonnegative) and the KKT/dual conditions are linear in the weights. It is the cheapest baseline to run on the districts data. Its bias under noise must be reported, not hidden. Written for a smooth convex setting; GP deviation terms are piecewise-linear, so use the LP-dual version (Ahuja-Orlin, Chan et al.) [inferred].

### 1.3 Bertsimas, Gupta & Paschalidis 2015

- Citation: D. Bertsimas, V. Gupta, I. Ch. Paschalidis, "Data-driven estimation in equilibrium using inverse optimization", Mathematical Programming 153(2):595-633, 2015. DOI 10.1007/s10107-014-0819-4. arXiv 1308.3397. https://arxiv.org/abs/1308.3397
- Read scope: abstract, Sec. 1-2 formulation, Sec. 6-7 (ambiguity sets, generalization guarantees, Theorems 6-8), parts of the appendix. Numerical sections skimmed.
- WHY: estimate the parameters of an equilibrium or utility model (Nash, Wardrop) from observed equilibria.
- HOW: write the equilibrium as a variational inequality (VI); an observed x is epsilon-approximate if the VI gap is epsilon; choose the function f (parametric, or nonparametric via kernels and regularisation) that minimises the average or maximal VI approximation error (their problem (12), (22), (28)).
- WHAT: a convex program for monotone f; an ambiguity-set construction that returns all "statistically plausible" functions (Sec. 6, Remark 9); out-of-sample bounds.
- Key formulation: forward = VI on a feasible set F = {x: Ax = b, x in C}; inferred = f(.; theta) or a kernel function; loss = VI (first-order) suboptimality, max over y in F of f(x)'(x - y).
- Guarantees (i.i.d. data, Assumptions 3-5: i.i.d. draws, Slater, observed x in F almost surely; Assumption 6: bounded set): Theorem 6 (data-dependent, scenario-program-type): with prob. >= 1 - beta(alpha) the next observation is a z_N-approximate equilibrium with prob. >= 1 - alpha, for the infinity-norm problem. Theorem 7: expected VI error of f_N is within an O(1/sqrt(N)) term of the training error z_N, w.p. >= 1 - beta. Theorem 8 (strong monotonicity gamma): ||x_{N+1} - x_hat|| <= sqrt(z_N / gamma). All bounds are conditional on z_N being small, i.e. on the model fitting (Remark 8).
- Not shown: consistency to a true parameter; the authors discuss multiple, equally good solutions (the "Rashomon effect", end of Sec. 6) and offer ambiguity sets and generalisation as the remedy. Aswani et al. 2018 later show this VI estimator is not estimation- or risk-consistent in their predictability sense.
- Relevance: provides generalisation (out-of-sample VI-error) bounds usable as a certificate of how well estimated goal weights explain held-out state-years, and the idea of reporting a set of plausible weight vectors rather than a point.

### 1.4 Aswani, Shen & Siddiq 2018

- Citation: A. Aswani, Z.-J. M. Shen, A. Siddiq, "Inverse Optimization with Noisy Data", Operations Research 66(3):870-892, 2018. DOI 10.1287/opre.2017.1705. arXiv 1507.03266 (v4). https://arxiv.org/abs/1507.03266
- Read scope: abstract, Sec. 1-2, Theorems 1-6 statements and the proofs of Theorems 2-4, the discussion of identifiability (IC), the conclusion. Appendix proofs of Prop. 1 skimmed. Numerics skimmed.
- WHY: real decision data are noisy (measurement noise, bounded rationality, model mismatch). The aim is a statistical-inference view of inverse optimization, with consistency as a minimal requirement.
- HOW: define the risk Q(theta) = E[ min over x in S(u, theta) of ||y - x||^2 ] (squared distance from observed y to the forward solution set); estimate by sample average (IOP-SAA). Because Q is only lower semicontinuous, they regularise (epsilon-optimal solution sets, duality-based reformulation of the bilevel program) and use epi-convergence.
- WHAT: NP-hardness of the problem (Theorem 1, Corollary 1); consistency results (Theorems 2-4); two algorithms (enumeration, semiparametric kernel) that retain consistency (Theorems 5-6).
- Key formulation: forward = convex program FOP: min f(x,u,theta) s.t. g(x,u,theta) <= 0, A1 (f, g continuous and convex in x), A2 (Theta convex); inferred = theta; loss = predictability (decision-space squared distance) loss.
- Guarantees and assumptions: R1 (feasible sets closed, bounded, nonempty interior), R2 (Theta closed bounded, E[y^2] < infinity). Theorem 2 (regularised problem, any fixed epsilon > 0): risk consistency, Q(theta_n; epsilon) converges in probability to its minimum. Theorem 3: risk consistency for the unregularised problem if f is strictly convex in x. Theorem 4: estimation consistency, theta_n converges in probability to theta_0, under the identifiability condition IC: (i) y = xi + w, xi in S(u, theta_0), E[w] = 0, finite variance, w independent of (u, xi); (ii) for every theta != theta_0 there is a positive-probability set of u where the solution sets differ; (iii) S(u, theta) is single-valued almost surely. Proposition 1 and Corollary 2: the VI method (Bertsimas et al. 2015) and the KKT method (Keshavarz et al. 2011) are NOT estimation consistent and NOT risk consistent, because they minimise suboptimality in objective value or constraint violation while noise perturbs the decision.
- Authors' own statements on limits: statistical consistency only (no rates); the problem is NP-hard so only low-dimensional theta or the semiparametric algorithm; ||.||_2 can be replaced by other losses "but we do not consider those extensions" (Sec. 1.1).
- Relevance: the central warning for our project. If observed allocations are noisy realisations of an optimum, KKT-residual estimation of goal weights is biased, and only a decision-space loss gives consistency. Condition IC(ii) says weights are recoverable only if different weight vectors give different optima on a set of contexts of positive probability, i.e. state-years must sit in different corners of the feasible region. IC(iii) fails for ordinary LP-type goal programs (multi-valued optima at ties), so for piecewise-linear GP one needs the random-coefficient case or a smoothed GP [inferred]. IC(i) needs noise independent of context; public-finance residuals are unlikely to satisfy that (e.g. state fixed effects) [inferred].

### 1.5 Mohajerin Esfahani, Shafieezadeh-Abadeh, Hanasusanto & Kuhn 2018

- Citation: P. Mohajerin Esfahani, S. Shafieezadeh-Abadeh, G. A. Hanasusanto, D. Kuhn, "Data-driven inverse optimization with imperfect information", Mathematical Programming 167(1):191-234, 2018 (online 2017). DOI 10.1007/s10107-017-1216-6. arXiv 1512.05489 (v2). https://arxiv.org/abs/1512.05489
- Read scope: abstract, Sec. 1-4 (setup, loss functions, Proposition 2.5, Definitions 4.1-4.3, Proposition 4.4), statements of Theorems 5.2-6.3, Proposition 6.4. Proofs and numerics skimmed.
- WHY: an observer wants to learn an agent's objective when the true objective lies outside the search space, the agent is boundedly rational, or the data are noisy.
- HOW: distributionally robust program. Minimise over theta the worst-case risk over a Wasserstein ball around the empirical signal-response distribution (their problem (13)); risk measure either expectation or CVaR. Introduces the suboptimality loss; shows it is convex and tractable, in contrast to the NP-hard predictability loss.
- WHAT: out-of-sample guarantee (Proposition 4.4); exact conic reformulation for linear hypotheses with the suboptimality loss (Theorem 5.2), safe approximation for quadratic hypotheses (Theorem 6.3), with an ex post exactness check (Proposition 6.4); intractability for quadratic and bilinear hypotheses in general (Theorem 6.1, Corollary 6.2).
- Key formulation: forward = parametric program min over x in X(s) of F(s, x); hypothesis class F_theta; losses: identifiability (Def. 2.1, unobservable), predictability (Def. 2.2), suboptimality (Def. 2.3: F_theta(s,x) - min_y F_theta(s,y)), first-order (Def. 2.4). Proposition 2.5: if F_theta is convex and gamma-strongly convex in x, first-order loss >= suboptimality loss >= (gamma/2) x predictability loss.
- Guarantees and assumptions: Proposition 4.4 (light-tail A = E[exp(||xi||^a)] < infinity for some a > 1; Wasserstein distance between in-sample and out-of-sample laws <= known eps_0; dimension condition m + n != 2p): the ball radius eps >= eps_0 + eps_N(beta) contains the true out-of-sample law w.p. >= 1 - beta, so the optimal worst-case value is a (1 - beta)-confidence upper bound on the out-of-sample risk. Without measurement noise, accumulation points of the estimates minimise the true risk almost surely (stated, via a theorem from their DRO paper, not reproved here). The radius shrinks like N^(-1/(m+n)) in high dimensions (curse of dimensionality in eps_N).
- Authors' comment worth keeping: "it is fundamentally impossible to learn F from the available training data. At best we can learn the set of its minimizers X*(s)" (Sec. 2), since strictly increasing transforms of F share minimizers.
- Relevance: gives a finite-sample certificate for out-of-sample explanatory power of an inferred weight vector, and an explicit statement of the identifiability limit (only the minimiser map is identified). With linear hypotheses and suboptimality loss it is an LP/conic program, which fits goal programs (GP objectives are linear in the weights).

### 1.6 Chan, Mahmood & Zhu, "Inverse Optimization: Theory and Applications"

- Citation: T. C. Y. Chan, R. Mahmood, I. Y. Zhu, "Inverse Optimization: Theory and Applications", Operations Research 73(2):1046-1074, 2025 (Crossref issued March 2025). DOI 10.1287/opre.2022.0382. arXiv 2109.03920 (v2, 2022). https://arxiv.org/abs/2109.03920
- Read scope: abstract, Sec. 1-2 (taxonomy), Sec. 3.1 opening, Sec. 4.1 (distance loss, Theorem 2, relaxed problem (14)), risk measures (Table 1), Table 2 (loss functions), Sec. 5.1 opening, application passages (radiation therapy, portfolio, Nash), conclusion. Not read in full (about 46 pages plus appendix). The arXiv 2022 text may differ from the 2025 journal version.
- WHY: no review since Heuberger 2004; a framework and a consolidated application list.
- HOW: taxonomy along three axes: forward problem structure (linear, conic, convex, discrete, sequential), parameter type (objective, constraints), model-data fit (perfect: "classical"; imperfect: "data-driven"). Classical problem (1): min h(theta) s.t. theta in the inverse-feasible set for every observation. Data-driven problem (2): min kappa h(theta) + (1/N) sum loss(x_i, X_opt_i(theta)).
- WHAT: loss and risk-measure catalogue. Table 2 lists distance (statistical property: consistency, Aswani et al.), absolute suboptimality (generalisation bound for linear models via VI equivalence), relative suboptimality (no guarantee listed), variational inequality (generalisation bound, Bertsimas et al.), KKT residual (no guarantee listed). Table 1: expected value, VaR (stability), CVaR (out-of-sample guarantee, Esfahani et al.). Sec. 5: online learning and inverse RL.
- Guarantees: restates Theorem 2 of Aswani et al. (risk consistency; assumptions: bounded closed feasible sets with nonempty interior, continuity and strict convexity of f in x, compact convex Theta, finite second moment) and notes parameter consistency needs identifiability (e.g. strict convexity).
- Open problems stated by the authors (Sec. 8): (1) more efficient solution methods because "many inverse models do not scale well with data" (each observation with its own feasible region adds variables and constraints); (2) "inverse models that can better incorporate distributional information": the literature has "little to no distributional assumptions about the input data, model parameters, or the degree of model mis-specification", unlike statistics and econometrics.
- Multiobjective content: Sec. 4 passage on Dong & Zeng (2021) (distributionally robust inverse multiobjective with distance loss, semi-infinite reformulation); radiation-therapy section (weights of a weighted-sum objective learned from past plans; Chan et al. 2014).
- Relevance: the reference taxonomy for our paper. Positions "weights/aspirations of a goal program" as the objective-parameter, convex/linear forward, data-driven cell. Lists no goal-programming or public-budget application [inferred from the application sections I read; not an exhaustive check].

### 1.7 Bärmann, Pokutta & Schneider (online inverse optimization)

- Citation: A. Bärmann, A. Martin, S. Pokutta, O. Schneider, "An Online-Learning Approach to Inverse Optimization", arXiv 1810.12997 (v2, 2020). https://arxiv.org/abs/1810.12997. The conference predecessor is Bärmann, Pokutta, Schneider, "Emulating the Expert: Inverse Optimization through Online Learning", ICML 2017 (the arXiv text cites it as Bärmann et al. 2017; I did not retrieve the ICML paper itself).
- Read scope: abstract, Sec. 1-3 (problem, losses, Proposition 3.1, Theorem 3.5, Theorem 3.14), remarks on stability; Sec. 4-5 skimmed.
- WHY: learn a decision-maker's linear objective from a sequence of (parameter p_t, expert decision x_t) pairs, using only a linear optimisation oracle over X(p).
- HOW: online learning. Regret loss f_t(c) = max over x in X(p_t) of c'x - c'x_t (convex, subgradient (x_bar_t - x_t), Prop. 3.1), minimised with multiplicative weights or online gradient descent; implicit variants for noisy data.
- WHAT: convergence of the average cumulative error at rate O(1/sqrt(T)); extension to approximately-learned nonlinear, dynamic and parametrised objectives, and suboptimal observed decisions; online-to-batch conversion to the stochastic offline case.
- Key formulation: forward = max {c_true' x : x in X(p)}, X(p) polyhedral or mixed-integer; inferred c in a known convex compact F; loss = suboptimality of the expert decision under c.
- Guarantees: Theorem 3.5: with diam_inf X(p_t) <= K, (1/T) sum_t (c_t - c_true)'(x_bar_t - x_t) <= 2K sqrt(ln n / T) and both component sums are nonnegative and bounded by the same quantity. Theorem 3.14 (i.i.d. samples; Algorithms 2, 3 or a strongly-convex regularised Algorithm 4): E[ max over x in X(p) of c_bar'x - c_bar'x_expert ] is O(1/sqrt(T)) for the averaged iterate c_bar. These are bounds on cost deviation (regret in the expert's own objective), not on parameter error; the paper itself notes that how to handle noise and learn the constraint side remains limited (Sec. 1 and 3.5; a remark states that some convergence property "remains open", near line 1034 of the text).
- Relevance: scalable estimator when many state-year observations arrive and when the forward problem is an LP/MIP solved by an oracle (an LP-based goal program is exactly that). The guarantee is on decision quality, not on identifying the weights.

### 1.8 Dong & Zeng, inverse multiobjective optimization (inference of parameters)

- Citation: C. Dong, B. Zeng, "Inferring Parameters Through Inverse Multiobjective Optimization", arXiv 1808.00935 (v1, 2018). https://arxiv.org/abs/1808.00935. The peer-reviewed version I could verify is the shorter C. Dong, B. Zeng, "Wasserstein Distributionally Robust Inverse Multiobjective Optimization", AAAI-21, 35(7):5914-5921, DOI 10.1609/aaai.v35i7.16739 (metadata only; not read).
- Read scope: abstract, Sec. 1-3 (formulation, Props 1-2, Corollary 1, Assumptions 1-3, Theorems 1-4), part of the proofs; numerical section not read.
- WHY: observed decisions are trade-offs between several criteria; assuming a single objective with noise corrupts inference. Infer the parameters of a multiobjective decision problem (and the population distribution of weights) from noisy observations.
- HOW: forward problem DMP: min over x in X(theta) of (f_1..f_p)(x, theta), efficient set X_E(theta) represented by the weighted-sum problem WP with w in the simplex. Corollary 1: S(w,theta) over positive w subset of X_E subset of S(w,theta) over all w (convex DMP). Loss l_K(y, theta) = min over sampled weights k in [K] of ||y - x_k||^2 with x_k in S(w_k, theta) (binary selection of which efficient point explains each observation); risk M_K(theta) = E[l_K]. Estimator: empirical risk minimisation (IMOP-EMP-WS) as a mixed-integer program, solved with ADMM and clustering heuristics.
- WHAT: parameters theta of the objectives and constraints (not the individual weights, which are treated as latent per-observation); the distribution of weights can be recovered "under suitable conditions" (abstract).
- Guarantees and assumptions: Assumption 1 (Theta convex; f, g convex in x), Assumption 2 (Theta compact), Assumption 3 (support of y inside a ball of radius R). Theorem 1 (strictly convex f): M(theta_N) converges in probability to M(theta*), i.e. risk consistency. Theorem 2 (sampled weights, strongly convex f): same for M_K. Theorem 3 (both empirical and weight samples): the proof is stated as "essentially the same" and omitted. Theorem 4 (Rademacher generalisation bound): with probability >= 1 - delta, M_K(theta_N_K) <= its empirical value + (1/sqrt(N)) (2K(B^2 + 2BR) + (B+R)^2 sqrt(log(1/delta)/2)), for each K [as printed; read as scaling like K/sqrt(N)]. Authors' remark after Theorem 3: the optimal set Theta* "is often not a singleton even when the objective functions are strongly convex", so risk consistency (persistence in the sense of Greenshtein and Ritov 2004) is "a more realistic standard" than parameter consistency.
- Not covered: the proofs of Theorems 2-3 are only sketched; sampling error from the K weight vectors is not quantified beyond the generalisation bound's dependence on K.
- Relevance: the closest formal precedent for inferring weights of a multi-criteria decision (GP is the weighted-sum/min-distance scalarisation of the same family). It confirms that weights are generically not point-identified and that statements should be made about the induced decisions. Their per-observation weight is a latent variable: heterogeneity across states fits our setting, where each state may carry its own weights [inferred].

### 1.9 Dong, Wang & Zeng, online learning of a multiobjective program

- Citation: C. Dong, Y. Wang, B. Zeng, "Learning Multiobjective Program Through Online Learning", arXiv 2010.06140 (v2, 2022, marked "paper under review"). https://arxiv.org/abs/2010.06140. Related arXiv 1810.01920 (Generalized inverse optimization through online learning) was downloaded but not read.
- Read scope: abstract, Sec. 1-3 (Assumptions 3.1-3.3, Lemma 3.1, Theorem 3.2), conclusion. Experiments not read.
- WHY / HOW: sequentially arriving decisions (possibly noisy or boundedly rational) from a multiobjective program; online implicit-update algorithms with the same weight-sampling loss l(y, theta) as 1.8.
- WHAT: regret bound. Assumptions: 3.1 (X(theta) closed, bounded, nonempty relative interior), 3.2 (kappa-Lipschitz h on Y), 3.3 (a convexity-type compatibility condition: either alpha x1 + beta x2 is efficient for alpha theta1 + beta theta2, or an efficient point is within a stated distance of that combination). Theorem 3.2: with step size eta_t proportional to 1/sqrt(t), R_T = sum_t (l(y_t, theta_t) - l(y_t, theta*)) <= 4 sqrt(2) (B+R) D kappa sqrt(T) / lambda.
- Relevance: online variant, so appropriate if we model each fiscal year as a new round. Assumption 3.3 is hard to verify for goal programs with kinks [inferred]. The regret is in the surrogate loss, not in the identification of weights.

### 1.10 Besbes, Fonseca & Lobel, contextual inverse optimization

- Citation: O. Besbes, Y. Fonseca, I. Lobel, "Contextual Inverse Optimization: Offline and Online Learning", Operations Research 73(1):424-443, 2025. DOI 10.1287/opre.2021.0369. arXiv 2106.14015 (v3, 2023). https://arxiv.org/abs/2106.14015
- Read scope: abstract, Sec. 1, Sec. 3 (offline minimax), Theorems 1-4 statements, conclusion list of open directions. Proofs not read.
- WHY: instead of the loss, one observes after the fact the action the all-knowing oracle would have taken; minimise regret against that oracle.
- HOW: knowledge set C of cost vectors consistent with observations (a cone); "circumcenter" proxy cost minimises worst-case angle to C; offline minimax regret is a function of the uncertainty angle alpha(C). Online: ellipsoidal-cone updates and projections.
- WHAT: Theorem 1 (offline minimax regret): worst-case regret of the circumcenter policy <= sin alpha(C) if alpha(C) < pi/2, else 1; and no policy can do better in the worst case. Theorem 3 (pointed initial cone): worst-case regret O(d^2 ln(T tan alpha(C_0))). Theorem 4 (general): O(d^4 ln T) in polynomial time. Theorem 2: the greedy circumcenter policy is insufficient.
- Key formulation: forward = min over x in X_t of c'x plus a context function f_t; inferred = c on the sphere; data noiseless (the conclusion lists noisy feedback as a future direction, near line 1401); the regret is in the oracle's own objective.
- Relevance: identifies the geometric quantity that governs what can be learned, the uncertainty angle of the cone of consistent weights. [inferred] For goal weights normalised to the simplex, the analogue is the diameter of the set of weight vectors consistent with all observed allocations, which is also the natural identification-set measure to report.

### 1.11 Zattoni Scroccaro, Atasoy & Mohajerin Esfahani

- Citation: P. Zattoni Scroccaro, B. Atasoy, P. Mohajerin Esfahani, "Learning in Inverse Optimization: Incenter Cost, Augmented Suboptimality Loss, and Algorithms", Operations Research 73(5):2661-2679, 2025. DOI 10.1287/opre.2023.0254. arXiv 2305.07730 (v2, 2024). https://arxiv.org/abs/2305.07730
- Read scope: abstract, Sec. 1-4 (consistent-cost cone, circumcenter, incenter, ASL), Theorems 3.2 and 3.5, Corollary 3.6, Sec. 4 relaxation for inconsistent data, Sec. 5 statement of Proposition 5.2; appendix statements only.
- WHY: pick a single cost vector from the cone C of vectors consistent with the data; circumcenter (Besbes et al.) is intractable and cannot handle inconsistent data.
- HOW: incenter = vector in C farthest in angle from the boundary of C (a robustness-to-noise interpretation); tractable convex reformulation. For inconsistent data, relax by the Augmented Suboptimality Loss ASL(theta; s, x_hat) = max over x in X(s) of {<theta, phi(s, x_hat) - phi(s, x)> + d(x_hat, x)}, which reduces to the usual suboptimality loss when d = 0 and is a convex surrogate of the predictability loss (Appendix A). Stochastic approximate mirror descent for discrete feasible sets with high cardinality.
- Key formulation: forward = min over x in X(s) of <theta, phi(s,x)>; C := {theta: <theta, phi(s_i, x_hat_i) - phi(s_i, x_i)> <= 0 for all x_i in X(s_i), all i} (Def. 2.2); trivial theta = 0 excluded by normalisation (scale invariance noted: argmin unchanged by alpha theta, alpha > 0); loss = ASL plus regulariser kappa R(theta) (problem (14)).
- Guarantees: Theorem 3.2 (circumcenter inner maximisation is NP-hard for polyhedral cones); Theorem 3.5/Cor. 3.6 (tractable incenter reformulation); Prop. 5.2 (convergence rate of the mirror-descent method for the approximate-subgradient scheme). No statistical consistency theorem for the noisy case in the parts I read.
- Relevance: practical estimator with a margin (distance term) that avoids ties and the trivial solution, directly relevant to weights on the simplex. The ASL margin d(x_hat, x) is the analogue of a loss-augmented margin in structured prediction [inferred].

### 1.12 Fatemi, Maskan, Sra & Mohajerin Esfahani, tight generalisation bounds, noiseless IO

- Citation: P. Fatemi, H. Maskan, S. Sra, P. Mohajerin Esfahani, "Tight Generalization Bounds for Noiseless Inverse Optimization", arXiv 2605.08866 (v2, 4 Nov 2026), stat.ML. https://arxiv.org/abs/2605.08866. Preprint; no venue verified.
- Read scope: abstract, Sec. 1-3 (Proposition 2.1, Theorem 2.2, Assumption 1, Propositions 2.4, 3.1, 3.5, Theorem 3.2), Sec. 6, scenario-program appendix statements.
- WHY / HOW: linear score F_theta(s,a) = <theta, psi(s,a)>; the expert picks argmax with unknown theta*. Learner picks a consistent theta_hat by solving a scenario program (the consistency constraints are the scenario constraints) and uses Campi-Garatti scenario theory, plus an incenter variant for uniqueness.
- WHAT / guarantees: Proposition 2.1: if T >= N(epsilon, beta) (the binomial tail condition), then w.p. >= 1 - beta, P_S(a_theta*(s) not in A_theta_hat(s)) <= epsilon; in particular for T >= 2(d + log(1/beta)) the mismatch probability is at most (2/T)(d + log(1/beta)), i.e. O(d/T). Theorem 2.2: with the incenter estimator and int(C_T) nonempty a.s., P_S(A_theta_hat(s) = {a_theta*(s)}) >= 1 - epsilon for T >= N(epsilon, beta). Proposition 3.1 and Theorem 3.2 show the O(d/T) rate is tight (minimax lower bound over learners; tightness for the estimator class), and the regret lower bound matches the adversarial online upper bounds.
- Authors' stated limitations (Sec. 6): faster rates under extra structure are open; active choice of contexts; "Noisy dataset ... extending the analysis to noisy observations is an important next step"; theory of the trade-off between computation and generalisation.
- Relevance: fast O(d/T) rate means that with d goals and T observed state-years, weights consistent with data predict well out of sample, if the data are noiseless and the model is well specified. With 10 years x 50 states, d of order 5-10, the nominal bound is of order 1/50 - 1/100 [inferred, rough]; but noiseless consistency of real budget data with a linear score is the unlikely assumption.

### 1.13 Ahmadi, Ganjkhanloo & Ghobadi, non-identifiability

- Citation: F. Ahmadi, F. Ganjkhanloo, K. Ghobadi, "From Non-Identifiability to Goal-Integrated Decision-Making in Parametric Inverse Optimization", arXiv 2603.17033 (v1, 17 Mar 2026), math.OC. https://arxiv.org/abs/2603.17033. Preprint (manuscript header reads "Authors' Names Blinded"); no venue verified. Not peer reviewed as far as I can tell.
- Read scope: abstract, Sec. 1-2 (model, Assumptions 1-6, Theorems 1-3, Propositions 1-5), Sec. 3 statements (Theorem 4-7, Assumptions 7-8), Sec. 4 definitions (Observation-Constraint Tradeoff, Assumption 9), conclusion and limitations. The dietary application and numerics were not read.
- WHY: formal conditions for when inverse recovery of objective parameters is possible; they argue non-identifiability is the generic case.
- HOW: objective f(x, theta) = sum_j theta_j phi_j(x), theta >= 0 with normalisation (Assumption 3: ||theta||_q = 1, theta_j0 >= alpha > 0). KKT stationarity: A(z)theta in -N_Omega(z), with A(z) the gradient matrix of the basis functions. Identification set for multiple observations is the intersection of normal-cone conditions.
- WHAT / theory: Theorem 1: for inverse LP, if two non-collinear active constraint normals are shared (Prop. 2), the feasible set C intersect Theta has at least two points, for normalisation on the sphere or the simplex; Corollary 1: regularisation does not remove this. Theorem 2: global non-identifiability for convex models under any of the Prop. 4 conditions. Theorem 3 (identifiability): under Assumptions 4 (mu-strong convexity), 5 (one-dimensional normal cones, i.e. each observation on a smooth boundary with one active constraint) and 6 (orthogonal persistent excitation: S = sum_k A(z^k)' P_k A(z^k) positive definite, P_k projecting orthogonally to the normal), theta is unique; Proposition 5: singular S implies non-uniqueness. Sources of ambiguity (Remark 3): high-dimensional normal cones (vertices) and rank-deficient basis gradients. Inverse Learning (IL) targets the latent optimum instead of theta: Theorem 4 (problem size independent of K), Theorem 6 (consistency of the recovered solution and outer semicontinuity of the parameter set, under Assumption 8: x^k = z_0 + xi^k with i.i.d. zero-mean noise and a SINGLE latent optimum z_0), Theorem 7 (solution identifiability). "Goal-integrated" models trade observational fidelity against adherence to expert-specified constraints ("goals" here are constraints that may be active; not goal programming in the OR sense).
- Authors' limitations: the single-latent-optimum noise model does not cover heterogeneous populations or changing contexts; formulations are nonconvex (MIP or heuristics); extension to contextual and heterogeneous settings is future work (conclusion).
- Relevance: most directly relevant theory for our project, with the caveat that the paper is an unreviewed preprint. Corner solutions are the typical output of a goal program (observations at vertices of the feasible region with many active constraints), which is precisely the high-dimensional normal-cone case where Theorem 1 says weights are not identified [inferred]. Its Assumption 6 gives a checkable rank condition on the data to report.

### 1.14 Chan, Sandholtz & Yousefi, Bayesian uncertainty quantification

- Citation: T. C. Y. Chan, N. Sandholtz, N. Yousefi, "Uncertainty Quantification in Data-Driven Inverse Optimization via Bayesian Inference", arXiv 2605.25288 (v1, 24 May 2026), math.OC. https://arxiv.org/abs/2605.25288. Preprint.
- Read scope: abstract, Sec. 1-3, identifiability definition, Lemma 1, Theorem 1 with proof, Remarks 3-5; Sec. 6 onward skimmed (not read in detail); numerical sections not read.
- WHY: data-driven IO returns point estimates; credible regions are needed.
- HOW: two generative models of decision data: noise in decision space (perturbed optimal solution) and noise in objective space (perturbed cost vector then forward solve); hierarchical Bayesian model with MCMC.
- WHAT / theory: Definition 1 (identifiability: same data law implies same parameter). Lemma 1 (identification): the globally identified set Theta_N* = intersection over i of {theta: x*(u_i, theta) = x*(u_i, theta*)} shrinks almost surely to {theta*} if for every theta != theta* some neighbourhood and a positive-probability set of covariates u give x*(u, theta') != x*(u, theta*) for all theta' in the neighbourhood. Theorem 1 (posterior consistency): the posterior concentrates on any open set containing theta* almost surely, under (A1) covariate variation: P_U(u: x*(u,theta) != x*(u,theta*)) > 0 for all theta != theta*; (A2) observation densities distinct for distinct optima; (A3) continuity at theta* and an integrable KL bound; (A4) prior support. Proof uses Schwartz's theorem (Remark 3 gives conditions for Gaussian and von Mises-Fisher models).
- Authors' point: the equivalence class Theta*(u) of parameters producing the same optimum at covariate u is generally not a singleton; identification accumulates only through covariate variation (Sec. 5 text before Lemma 1).
- Relevance: gives the formal "variation in the context is what identifies the weights" statement we need, and a method for credible regions of goal weights. Requires a correctly specified forward model and a likelihood, both strong in public-budget data; the paper explicitly assumes convex forward problems [inferred for GP: needs the smoothed or penalised version].

### 1.15 Cai et al. 2026 and Gupta et al. 2026 (efficient online inverse linear optimization; recent, unrefereed)

- Citations: (a) Y. Cai, A. Gupta, V. Gupta, G. Guruganesh, Y. Jiang, C. Liaw, A. Mehta, R. Paes Leme, G. Velegkas, D. Wang, "Efficient Online Inverse Optimization with O(d) Regret", arXiv 2609.13440 (v1, 11 Sep 2026), cs.LG. https://arxiv.org/abs/2609.13440. (b) A. Gupta, G. Guruganesh, H. Lin, V. Mirrokni, R. Paes Leme, D. P. Woodruff, "Optimal and Efficient Online Inverse Optimization", arXiv 2610.08735 (v1, 6 Oct 2026), cs.LG. https://arxiv.org/abs/2610.08735.
- Read scope: abstracts, introductions, Table 1 of each, Theorem 1.1 and Definition 3.4/Theorem 3.6 of (a); Theorem 2.1/Corollary 2.2 statements of (b). Proofs not checked.
- Important provenance flag: paper (a) states that its main result "was entirely obtained by Cogentic, an agentic framework for mathematical discovery, using Gemini 3.1 Pro", with the authors verifying the proofs; the exposition was AI-aided. Both are v1 preprints. Treat as unrefereed.
- WHAT: online inverse linear optimization (hidden w*, adversarial action sets X_t in the unit ball, expert maximises <w*, .>). Regret R_T = sum_t <w*, x_t - x_hat_t>. Table 1 in both gives the state of the art: Barmann et al. O(sqrt T); Besbes et al. O(d^4 ln T); Gollapudi et al. O(d ln T); Sakaue et al. O(d ln T); Cai et al. O(d) uniform in T with O(d^2) time per round (Theorem 1.1: Reg_T <= 6 sqrt(3) d R <= 11 d R); Gupta et al. O(sqrt d) (Theorem 2.1 and Corollary 2.2) in polynomial time; lower bound Omega(sqrt d). Paper (a) adds a C-corrupted-oracle variant (Definition 3.4, Theorem 3.6: Reg_T <= 8 sqrt(3) d R + 6C), where C bounds the total amount by which the expert's own criterion ranks its action below the learner's.
- Relevance: shows regret for learning linear scalarisation weights is horizon-free in the noiseless adversarial model, so the cost-of-learning is d, not T. The corruption variant is the only noise-robust statement I found in this online line; it bounds the sum of expert errors rather than a stochastic noise model [inferred].

### 1.16 Gebken & Peitz, inverse multiobjective optimization (Pareto criticality)

- Citation: B. Gebken, S. Peitz, "Inverse multiobjective optimization: Inferring decision criteria from data", Journal of Global Optimization 80(1):3-29, 2021 (Crossref issue date Dec 2020). DOI 10.1007/s10898-020-00983-z. arXiv 1901.06141 (v1 read). https://arxiv.org/abs/1901.06141
- Read scope: abstract, Sec. 1, Sec. 3.1-3.2 (formulation, Algorithm 1, Theorem 3.2, Remark 3.3), conclusion; Sec. 4 noisy-data examples only glanced at.
- WHY / HOW: find an objective vector f (components in a span of basis functions) such that given points are extended Pareto critical, i.e. Df(x)' alpha = 0 for data (x, alpha), alpha in the simplex. Reduces to a homogeneous linear system L c = 0; with noise, solve min ||L c||_2 over ||c||_2 = 1 by SVD (their (7), (9)).
- WHAT: Theorem 3.2: the returned f satisfies ||Df(x)' alpha||_2 <= s_{i*} for every data point, and if s_{i*} = 0 all data are extended Pareto critical. Remark 3.3(c): even then the extended critical set may be larger than the data (not necessarily desirable); dimension of the solution space read off the singular values; sparse choice (L1) suggested for interpretability. Experiments use k = 2 objectives, n = 2 variables with monomial bases; the authors list higher-dimensional behaviour and better bases as open (Sec. 6).
- Key distinction: the data contain the KKT multiplier alpha (the weights), i.e. the weights at each observation are treated as known. In our problem weights are the unknown, so this paper solves a different (easier) inverse problem [inferred from the formulation: D subset of R^n x simplex].
- Guarantees: deterministic residual bound only; no statistical consistency.
- Relevance: gives a basis-expansion KKT residual estimator (the same family as Keshavarz et al.) for multiobjective problems and singular-value diagnostics of (non-)uniqueness, usable as a data-rank diagnostic.

### 1.17 Skimmed, not counted in the 16

- Chan, Lee & Terekhov, "Inverse Optimization: Closed-form Solutions, Geometry and Goodness of Fit" (Management Science 65(3):1115-1135, 2019; the journal reference is taken from the bibliography of Besbes et al.), arXiv 1511.04650. Read: abstract and statement list. Single suboptimal observation; Theorem 1 gives a closed-form cost vector; goodness-of-fit metric rho (coefficient of complementarity, R^2-like). The authors state it treats a single data point "as a necessary foundational step" toward multiple points (near the end of the introduction). https://arxiv.org/abs/1511.04650
- Lin, Delage & Chan, "Conformal Inverse Optimization", NeurIPS 37:63534-63564 (2024) (venue from the bibliography of Chan et al. 2026), arXiv 2402.01489. Read: abstract, Assumptions 1-3, Theorem 2. Learns an uncertainty set for theta by conformal prediction (validity P(Theta_hat intersect C(theta_bar, alpha_gamma) nonempty) >= gamma for a validation set exchangeable with the new decision, eq. (11)); then solves a robust forward problem. https://arxiv.org/abs/2402.01489

---

## 2. Synthesis

### 2.1 Taxonomy of losses (what the inverse problem minimises)

| Loss | Definition in these papers | Convex in theta? | Statistical status |
|---|---|---|---|
| Predictability / distance (decision-space) | min over y in X*_theta(s) of ||x - y||^2 (Esfahani Def. 2.2; Aswani RISK; Chan review ell_D) | No, bilevel; NP-hard (Aswani Thm 1) | Risk consistency (Aswani Thms 2-3), estimation consistency under IC (Thm 4). Needs strictly convex f or regularisation. |
| Absolute suboptimality | F_theta(s,x) - min_y F_theta(s,y) | Yes for linear/convex hypotheses | Out-of-sample certificate via DRO (Esfahani Prop. 4.4); dominated by predictability up to gamma/2 (Prop. 2.5); consistency only under extra conditions; Aswani Prop. 1 shows the related KKT/VI estimators are inconsistent under decision-space noise. |
| Relative suboptimality | ratio form | Linear-program reformulations | No guarantee listed (Chan review Table 2) |
| First-order / VI loss | max over y of grad F_theta(s,x)'(x - y) | Yes | Generalisation bound, conditional on the training error being small (Bertsimas Thms 6-8); not consistent (Aswani Prop. 1) |
| KKT residual | stationarity and complementarity residuals | Yes (linear in weights) | None (Keshavarz); inconsistent under noise (Aswani) |
| Augmented suboptimality (ASL) | max over x of {suboptimality + d(x_hat, x)} | Yes | Convex surrogate of predictability (Scroccaro App. A); algorithmic rate only in the parts read |
| Regret / cost deviation under the expert's objective | sum of c'(x_bar_t - x_t) | Yes | O(1/sqrt T) average (Barmann Thm 3.5); logarithmic regret (Besbes Thm 4); O(d) uniform regret (Cai Thm 1.1), all noiseless |
| Weighted-sum selected efficient point (multiobjective) | min over sampled weights of distance to efficient points | MIP | Risk consistency and Rademacher bound (Dong & Zeng Thms 1-4) |
| Likelihood-based | Gaussian/vMF around x*(u, theta) | Not convex | Posterior consistency (Chan et al. 2026 Thm 1) |

### 2.2 What is identifiable

1. Only the minimiser map is identified, never the objective or its scale. Esfahani et al. Sec. 2 state this directly. Scale invariance: the argmin of <theta, phi> is unchanged by alpha theta, alpha > 0 (Scroccaro Sec. 3), and monotone transformations of F are observationally equivalent (Keshavarz Sec. II). A normalisation is therefore mandatory (Keshavarz alpha_0 = 1; Ahmadi Assumption 3; simplex for weights).
2. Parameter-level non-identifiability is generic for linear or piecewise-linear forward problems. Ahmadi et al. Theorem 1: observations at points sharing at least two non-collinear active constraint normals leave a multi-point consistent set, and regularisation does not help (Cor. 1). Dong & Zeng remark that Theta* is often not a singleton even with strongly convex objectives. Bertsimas et al. name the "Rashomon effect".
3. Sufficient conditions for point identification found in the papers: strict or strong convexity of the forward objective in x (so the optimum is single-valued); one-dimensional normal cones at observed optima (smooth boundary, one active constraint); full-rank or orthogonal excitation of the basis gradients across observations (Ahmadi Assumptions 4-6, Theorem 3); covariate variation, i.e. different parameters generate different optima on a positive-probability set of contexts (Aswani IC(ii); Chan et al. Lemma 1 and A1). Aswani IC(iii) requires the forward optimum to be unique almost surely.
4. Noise changes the target: with noise, exact identification sets become empty and what is estimable is the risk minimiser (persistence, Greenshtein and Ritov 2004, as used by Aswani and Dong & Zeng), unless IC holds.
5. Set-valued answers are a principled alternative: the cone of consistent weights (Besbes, Scroccaro), ambiguity sets of plausible functions (Bertsimas Sec. 6), the full parameter set compatible with a latent optimum (Ahmadi IL, Theorem 5), credible regions (Chan et al. 2026), conformal uncertainty sets (Lin et al.).

### 2.3 Statistical theory for noisy observations (what exists)

- Consistency: Aswani et al. 2018 (Theorems 2-4), i.i.d. context and additive decision noise independent of context; no rates. Dong & Zeng Thms 1-3 (risk consistency) for the multiobjective case.
- Finite-sample bounds: Esfahani et al. Prop. 4.4 (Wasserstein radius ~ N^(-1/(m+n)) in high dimension, plus the known noise level eps_0); Bertsimas et al. Thms 6-8 (O(1/sqrt N) over the training error, or a scenario-type bound); Dong & Zeng Theorem 4 (Rademacher, ~K/sqrt N).
- Rates: noiseless case O(d/T) generalisation (Fatemi et al. Prop. 2.1, tight by Thm 3.2); online regret O(sqrt T), O(d^4 ln T) , O(d) (Barmann Thm 3.5; Besbes Thm 4; Cai Thm 1.1).
- Uncertainty quantification: Bayesian posterior consistency (Chan et al. 2026 Thm 1) and conformal validity (Lin et al. Thm 2), the latter for the case where the decision maker's perceived parameters vary i.i.d.
- Noise-robust online: only the corrupted-oracle regret (Cai et al. Thm 3.6), and implicit-update online algorithms with Lipschitz losses (Dong et al. Thm 3.2).
- Unsupported by any paper read: consistency or rates when the noise depends on the context; panel dependence (the same state across years, i.e. non-i.i.d. observations); misspecified forward models beyond Aswani's risk-consistency statement; piecewise-linear, goal-programming-type forward objectives.

### 2.4 Open problems stated by the authors (with locators)

- Chan, Mahmood & Zhu (arXiv 2109.03920), Sec. 8: efficient large-scale methods; incorporating distributional information about the data, parameters and degree of misspecification.
- Fatemi et al. (arXiv 2605.08866), Sec. 6: faster rates under strong convexity/smoothness or distributional assumptions on the context; active learning of contexts; noisy observations (called "an important next step"); computation versus generalisation.
- Ahmadi et al. (arXiv 2603.17033), conclusion: heterogeneous populations and time-varying preferences; scalable decomposition for the nonconvex IL; extension to contextual settings with covariate-dependent objectives.
- Gebken & Peitz (arXiv 1901.06141), Sec. 6: higher-dimensional (more than two variables, two objectives) examples; better bases than monomials.
- Besbes et al. (arXiv 2106.14015), conclusion (near line 1401 of the text I read): noisy feedback; Barmann et al. (arXiv 1810.12997): the authors state that an extension "remains open" near the end of Sec. 3 (line 1034 of the text; the exact statement is about a dual-regret scheme, which I did not fully read).
- Dong, Wang & Zeng (arXiv 2010.06140), Sec. 5: integrating contextual-bandit algorithms.
- Aswani et al. (arXiv 1507.03266), Sec. 1.1: only l2 loss analysed; absolute deviation or likelihood losses "can be proved" but are not done.
- Lin et al. and Chan et al. 2026: UQ currently requires a correctly specified forward model (their assumptions); no formal treatment of misspecification (A2, A3 of Chan et al. Theorem 1).

### 2.5 Gaps relevant to our project [inferred]

These are my own readings of the above; none is stated by the authors.

- G-IO-1. No paper in this cluster treats a goal-programming forward model (weighted deviations from aspiration levels, lexicographic priorities). The nearest are the weighted-sum inverse multiobjective works (Dong & Zeng; Chan et al. 2014 radiation therapy as cited in the review) and Gebken & Peitz. The aspiration levels would enter as constraint-side parameters (right-hand sides), whereas the data-driven literature "focuses on estimating objective function parameters" (Chan review Sec. 4); joint estimation of weights and aspirations is a form of the "estimating constraints" literature that Chan et al. treat separately (Sec. 3.1 of the Chan et al. review; I did not read that part).
- G-IO-2. Goal programs have a piecewise-linear objective and typically vertex optima. That is exactly the combination in which Ahmadi Theorem 1 gives non-identifiability and Aswani IC(iii) fails; a point-identification claim would need either strict convexification (a quadratic or Huber-type deviation penalty), explicit random coefficients, or a restriction to identified sets and decision-level guarantees.
- G-IO-3. Statistical theory assumes i.i.d. observations. District/state-year panels violate this (serial correlation, state effects). A cluster-bootstrap or block version of Esfahani-type certificates is not established.
- G-IO-4. Observations come from many states solving the same forward structure but with possibly different weights. Dong & Zeng's latent per-observation weight and the "heterogeneous population" limitation noted by Ahmadi et al. point to a hierarchical (state-level) model; Chan et al. 2026 show a hierarchical Bayesian route for a common theta only.
- G-IO-5. A budget allocation that is a mixture of political bargaining, legal formulas, and inertia is unlikely to be exactly optimal for a stable goal program; Esfahani's bounded-rationality loss (Definition 3.1, not read in detail) and the corrupted-oracle regret (Cai Def. 3.4) are the closest formal vehicles for such deviations.

### 2.6 Suggested use in the paper [inferred]

Frame the estimand as the identified set of weights (and aspirations) consistent with, or near, the observed allocations, plus a decision-level (predictability) risk; report both (i) the KKT/suboptimality estimator as a cheap baseline with its documented bias (Aswani Prop. 1) and (ii) a decision-space or ASL-type estimator with simplex normalisation, together with a data-rank diagnostic in the spirit of Ahmadi Assumption 6 and credible/conformal regions where a likelihood is defensible.

---

## 3. Important papers not read (paywalled or not retrieved)

- Ahuja & Orlin 2001, Operations Research 49(5):771-783, DOI 10.1287/opre.49.5.771.10607 (abstract only, via Crossref).
- Dong & Zeng, "Wasserstein Distributionally Robust Inverse Multiobjective Optimization", AAAI-21, DOI 10.1609/aaai.v35i7.16739 (arXiv 2009.14552 was listed by the arXiv API but not downloaded).
- Chan, Craig, Lee & Sharpe, "Generalized inverse multiobjective optimization with application to cancer therapy", Operations Research 62(3), 2014 (cited via the Chan review and Chan et al. 2026 bibliographies; not retrieved, DOI not verified here).
- Chan & Lee, "Trade-off preservation in inverse multi-objective convex optimization", EJOR (cited in the Chan review bibliography; not retrieved; DOI not verified).
- Bärmann, Pokutta & Schneider, ICML 2017, "Emulating the expert" (PMLR; not retrieved).
- Shahmoradi & Lee, quantile-loss inverse LP (cited by Chan et al. 2026 as 2022; not retrieved).
- Babier, Chan, Lee, Mahmood & Terekhov, "An ensemble learning framework for model fitting and evaluation in inverse linear optimization" (arXiv 1804.04576, listed by arXiv API; not read).
- Besbes et al. on circumcenter/online and Sakaue et al. variable-metric work (cited via Cai et al. Table 1; not retrieved).
- Gollapudi et al. (O(d ln T) centroid regret) and Dewasurendra (O(d) regret), both cited via Cai et al. Table 1 and not retrieved.
- Iyengar & Kang 2005 and Zhang & Xu 2010 (inverse conic programming; cited by Chan et al. 2026 Sec. 2; not retrieved). No paper on inverse conic programs specifically was read in full; the conic content here comes from Esfahani et al. (conic-representable supports, Assumption 5.1 and Theorem 5.2) and the review.

---

## 4. Retrieval log

arXiv PDFs in /tmp/litA/: 2109.03920, 1507.03266, 1512.05489, 1308.3397, 1810.12997, 1808.00935, 2010.06140, 2106.14015, 2305.07730, 2605.08866, 2603.17033, 2605.25288, 2609.13440, 2610.08735, 1511.04650, 2402.01489, 1901.06141, 1810.01920 (not read), 2102.10742 ("Comparing Inverse Optimization and Machine Learning Methods for Imputing a Convex Objective Function", first author E. H. Iraj per the arXiv API; downloaded, not read). Keshavarz et al. 2011 PDF from the author's page (web.stanford.edu/~boyd/papers/pdf/imputed_objective_msc.pdf). Venue, volume and page data for 1.2-1.6, 1.10, 1.11, 1.16 were checked against api.crossref.org. Note that the arXiv IDs 2603.17033, 2605.08866, 2605.25288, 2609.13440 and 2610.08735 postdate my training and were confirmed only through the arXiv listing and the downloaded PDFs.
