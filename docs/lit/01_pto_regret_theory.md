# Literature cluster 1: theory of predict-then-optimize / estimate-then-optimize regret

Scope: papers relevant to judging whether the quadratic plug-in bound in `docs/06_quadratic_bound_proof.md` is known. All PDFs were downloaded from arxiv.org into /tmp/lit1/ and read with pdftotext. Statements in quotes or paraphrased with a locator are from the text I read. Anything I infer is marked [inferred]. The OpenAlex API returned a rate-limit error (free daily budget exhausted), so paper discovery used the arXiv API instead; no paper listed here was cited without being downloaded and opened.

Our result in one line (from docs/06): for a weakly Pareto point of the learned problem, with weights w supporting it, w_c > 0 on a strongly convex spend term (H1) and no goal at a kink (H2), the true gap is at most B e^{-theta_lo} (sum_k w_k ||Delta a_k||)^2 / (2 w_c).

---

## Papers read

### 1. Elmachtoub & Grigas (2022), Smart "Predict, then Optimize"
- Citation: A. N. Elmachtoub, P. Grigas. Smart "Predict, then Optimize". venue as given in the arXiv listing/memory: Management Science 68(1), 2022 (not verified from the PDF) (arXiv:1710.08005v5, 19 Nov 2020). https://arxiv.org/abs/1710.08005
- Read scope: abstract, introduction and related literature (Sec 1.2), SPO loss definitions (Sec 2, Defs 1-2), SPO+ and Props 2-4, Assumption 1 and Theorem 1, Prop 5-6 statements. Did not read the appendix proofs or experiments in detail.
- WHY: Standard prediction metrics ignore how predictions are used downstream; need a loss that measures decision error.
- HOW: Define the SPO loss l_SPO(c_hat, c) = max_{w in W*(c_hat)} c'w - z*(c) (Def 2, the "unambiguous" version), derive the convex surrogate SPO+ via duality, and prove Fisher consistency.
- WHAT: Theorem 1 (Fisher consistency of SPO+) under Assumption 1: (1) W*(E[c|x]) a.s. a singleton, (2) c|x centrally symmetric about its mean, (3) c|x continuous on R^d, (4) interior of S nonempty. The setting is a linear objective c'w over a convex compact S. Related literature (Sec 1.2) notes that Kao et al. 2009 and Donti et al. 2017 treat strongly convex (quadratic) problems, "which must be addressed in our setting to avoid degenerate prediction models" (non-uniqueness). No regret rate, no second-order statement, no nonsmooth or multiobjective objective.
- Relevance to us: defines regret = decision loss of plug-in solution. Their regret is for linear objectives, where the per-instance regret is first order in the cost error (see item 3).

### 2. Liu & Grigas (2021), Risk bounds and calibration for SPO+
- Citation: H. Liu, P. Grigas. Risk Bounds and Calibration for a Smart Predict-then-Optimize Method. arXiv:2108.08887v2 (Oct 2021; the NeurIPS 2021 venue is from memory, not verified from the PDF). https://arxiv.org/abs/2108.08887
- Read scope: abstract, introduction, Sec 3 (Thm 2, Cor 3.1), Sec 4 (Assumption 4.1, Thm 3, Lemmas 1-2, Cor 4.1), conclusion. Not the appendix.
- WHY: Quantify how excess SPO+ surrogate risk transfers to excess true SPO risk.
- HOW: Calibration functions delta(eps); polyhedral feasible set and a distribution class P_{M,alpha,beta} lower-bounded by a Gaussian density; then feasible sets that are level sets of a mu-strongly convex, L-smooth function.
- WHAT: Thm 2 (polyhedral): calibration function >= (alpha Xi_S / (4 sqrt(2 pi e) ...)) * min(eps/(D_S M), ...)^2 (constants garbled in my text extraction), i.e. an O(eps^2) calibration, giving Cor 3.1 an O(n^{-1/4}) excess SPO risk rate. Thm 3 (strongly convex level sets, Assumption 4.1): calibration function >= (mu^{9/2} / (4(1+beta^2) L^{9/2})) * eps, i.e. O(eps), "significantly strengthening" the polyhedral case; Cor 4.1 then gives O(n^{-1/2}). The authors note the squared-loss surrogate already has O(1/sqrt n) from Hu et al. 2020 (polyhedral case) and that "an interesting open question concerns whether the rate can also be improved for the SPO+ surrogate" (Sec 3, after Cor 3.1). In this paper, strong convexity is in the feasible region (curved constraint set), objective stays linear. It is not strong convexity of the objective as in our spend term.
- Relevance to us: shows that curvature (of the set) improves rates for a linear objective. Different mechanism from ours (curvature of objective), same family of "curvature gives fast transfer".

### 3. Hu, Kallus & Mao (2022), Fast rates for contextual linear optimization
- Citation: Y. Hu, N. Kallus, X. Mao. Fast Rates for Contextual Linear Optimization. Management Science 2022 (venue not verified from the PDF; arXiv:2011.03030v3, 31 Aug 2021). https://arxiv.org/abs/2011.03030
- Read scope: abstract, introduction, Sec 2.1-2.2 (Thm 1-4), Sec 3 (Assumption 2, Thm 6-8, Cor 3-4), discussion of regret rates. Not the appendices.
- WHY: Show that naive estimate-then-optimize (ETO) can beat integrated/ERM approaches in regret rate.
- HOW: Contextual linear optimization pi*(x) in argmin f*(x)'z over a polytope; a margin ("noise") condition on near-dual-degeneracy; pointwise concentration of the estimator.
- WHAT: Thm 4 (slow rate, no margin): Regret(pi_fhat) <= 2 B E_D E_X ||f*(X) - fhat(X)||. This is first order in the estimation error per instance (Cauchy-Schwarz). Assumption 2 (margin): P_X(0 < Delta(X) <= delta) <= (gamma delta / B)^alpha, where Delta(x) is the gap between the optimal value and the best suboptimal vertex. Thm 8: if P(||fhat(x) - f*(x)|| >= delta) <= C1 exp(-C2 a_n delta^2) pointwise, then Regret(pi_fhat) <= C(alpha, gamma) B a_n^{-(1+alpha)/2}; for GLM a_n = n gives n^{-(1+alpha)/2}, i.e. rate 1/n with alpha = 1. If Delta(X) is bounded away from zero (strict separation) the condition holds for alpha -> infinity. ERM/IERM reach only the slower rate (eta log n / n)^{(1+alpha)/(2+alpha)} (Thm 6, Cor 3), so ETO's exponent is faster by a factor (2+alpha)/2. The fast rate arises from the margin, which makes the decision locally constant, not from curvature. In the regime where the decision is locally constant, regret is zero w.h.p.; in the regime near degeneracy regret is first order in the error.
- Relevance to us: the clearest statement that for piecewise-linear (linear-programming) structure regret is first order per instance and "fast" only after averaging over a margin distribution. Sign stability (H2) is the analogue of the margin condition for goal kinks, but in a continuous (strongly convex) problem the solution moves smoothly instead of staying fixed.

### 4. Elmachtoub, Lam, Zhang & Zhao (2023/2025), ETO vs IEO vs SAA
- Citation: A. N. Elmachtoub, H. Lam, H. Zhang, Y. Zhao. Estimate-Then-Optimize versus Integrated-Estimation-Optimization versus Sample Average Approximation: A Stochastic Dominance Perspective. arXiv:2304.06833v4 (May 2025). https://arxiv.org/abs/2304.06833
- Read scope: abstract, introduction, Sec 3-4 (Assumptions 1-3, Props 1-2, Thms 1-3, Cor 1, proof sketch around eqs (6)-(7)), start of Sec 5 (constrained case). Not the appendices.
- WHY: Compare three data-driven pipelines when the parametric model is well-specified or misspecified.
- HOW: Asymptotic M-estimation plus a second-order delta method on the regret.
- WHAT: Assumption 2: second-order Taylor expansions of v0(w) and v0(w_theta) at the optimum (first and second-order optimality conditions). Eqs (6)-(7): R(w) = (1/2)(w - w*)' grad_ww v0(w*) (w - w*) + o(||w - w*||^2) and R(w_theta) = (1/2)(theta - theta0)' grad_thetatheta v0(w_theta0) (theta - theta0) + o(||theta - theta0||^2). Thm 1: all regrets vanish when well-specified. Thm 2: n R(what) converges in distribution to G = (1/2) N' H N, with G_ETO <=_st G_IEO <=_st G_SAA. Sec 1: "the regrets of all considered methods are roughly equivalent to quadratic functions of the estimated parameters"; "regrets ... vanish at a rate of O(1/n)". Constrained case (Sec 5): uses the Lagrangian, and second-order conditions do not make the Hessian positive definite, hence pseudoinverses. Requires twice differentiability of v(w, theta) at (w*, theta0) and of w_theta in theta (Assumption 3).
- Relevance to us: this is the strongest asymptotic statement that plug-in (ETO) regret is quadratic in the parameter error for smooth, well-specified problems. It is asymptotic and smooth; it does not cover kinks (max(0, l_k)) or vector objectives.

### 5. Elmachtoub, Lam, Lan & Zhang (2025), Dissecting the impact of model misspecification
- Citation: A. N. Elmachtoub, H. Lam, H. Lan, H. Zhang. Dissecting the Impact of Model Misspecification in Data-driven Optimization. arXiv:2503.00626v3 (v3 dated 20 Oct 2026 on the PDF). https://arxiv.org/abs/2503.00626
- Read scope: abstract, introduction, Assumptions 1-2, Thms 1-2 statements, outline of Thms 3-5 (Table 1 discussion). Not the proofs.
- WHY: Understand when integrated estimation-optimization beats ETO as a function of misspecification.
- HOW: Expand regret into zeroth, first and second-order terms in n and compare tails.
- WHAT: Assumptions: convex feasible set, c(., z) convex, v(w, Q) rho_c-strongly convex in w, Lipschitz and bounded costs. Thm 2: under misspecification the zeroth-order regret limits are kappa0^ETO >= kappa0^IEO >= 0; ETO's disadvantage is a nonvanishing term, so quadratic-in-estimation-error behaviour is a well-specified phenomenon. Thm 1: an IEO generalization bound with rate O(1/sqrt n).
- Relevance to us: reminds that quadratic behaviour is only for the well-specified case. In our paper the Cobb-Douglas model is the truth in the experiment, so the well-specified case applies; with real data, misspecification adds a first-order floor [inferred].

### 6. Tan & Frazier (2022), Regret bounds for estimate-then-optimize
- Citation: S. Tan, P. Frazier. Regret Bounds and Experimental Design for Estimate-then-Optimize. arXiv:2210.15576v1 (Oct 2022), math.OC. https://arxiv.org/abs/2210.15576
- Read scope: abstract, introduction, Sec 3 (Assumptions 3.1-3.3, Thm 3.4), Sec 4 (Assumption 4.1, Lemma 4.3, Thm 4.4), Sec 5 intro, conclusion. Did not read examples/appendix.
- WHY: Choose experiments to minimise downstream decision regret.
- HOW: A deterministic regret bound by Taylor expansion, then sub-Gaussian concentration.
- WHAT: Setting: smooth, unconstrained min_x f(x, theta*), x* interior. Assumptions: 3.1 first-order optimality at (x*, theta*); 3.2 rho-strong convexity of f in x near x*(theta) for each theta; 3.3 bounded curvature beta1 and a third-order cross-derivative bound beta2 (|D_theta^2 D_x f [x - x*, dtheta, dtheta]| <= beta2 ||x - x*|| ||dtheta||^2). Thm 3.4: if x* is in the strongly convex ball of thetahat, then f(xhat, theta*) - f(x*, theta*) <= (4 beta1 / rho^2) || (d^2 f / dx dtheta)|_{x*,theta*} (thetahat - theta*) ||^2 + (4 beta2^2 / rho^2) ||thetahat - theta*||^4 (second coefficient as extracted: 4 beta2^2 / rho^2 times ||thetahat - theta*||^4; the extraction was partly garbled so constants are approximate). Thm 4.4: with probability 1 - alpha e^{-beta n} - 2/n^2, regret <= (4 beta1/rho^2) Tr(D Sigma D'/n) + lower order, for thetahat - theta* = Sigma^{1/2} X / sqrt(n), X sub-Gaussian. Related-work comment: ETO differs from ERM/SAA except when f is linear in theta.
- Relevance to us: this is the closest known finite-sample (non-asymptotic) deterministic quadratic regret bound for plug-in. Same structure as ours (strong convexity plus cross-derivative times parameter error, squared). Ours has the same form with D = the (constant) cross-derivative of a linear-in-parameter model, so the beta2 term vanishes [inferred].

### 7. Ho-Nguyen & Kilinc-Karzan (2022), Risk guarantees for end-to-end prediction and optimization
- Citation: N. Ho-Nguyen, F. Kilinc-Karzan. Risk Guarantees for End-to-End Prediction and Optimization Processes. venue not verified from the PDF (arXiv:2012.15046v1, Dec 2020). https://arxiv.org/abs/2012.15046
- Read scope: abstract, introduction, calibration definitions and Thms 1-4, Cor 3, Remark 7 (Sec 4-5), related-work paragraph. Not the experiments or proofs.
- WHY: Close the gap of formal guarantees linking prediction risk to optimization (decision) risk.
- HOW: Calibration of surrogate losses; equivalence of Fisher consistency and calibration (Thm 2).
- WHAT: Thm 4: squared loss is uniformly calibrated with delta(eps) >= eps^2 / B_X^2. Cor 3: (1/B_X^2) (R(g,P) - R*(P))^2 <= R_LS(g,P) - R_LS*(P), i.e. true excess risk <= B_X sqrt(excess squared-error risk), a first-order dependence on the root-mean-square prediction error, for a linear-in-c objective f(x) + c'x over a general convex set X. They note Kao et al. 2009 treat strongly convex quadratic f with linear predictors.
- Relevance to us: shows that, without curvature in the cost that does not involve the uncertain parameter, the transfer from prediction error to decision error is first order (sqrt of squared-loss excess risk) even for a smooth convex f. Strong convexity in the decision variable with the uncertain parameter only entering linearly is what gives the square in our theorem [inferred: Cor 3 is a worst-case bound and does not claim tightness].

### 8. Mandi et al. (2024), Decision-focused learning survey
- Citation: J. Mandi, J. Kotary, S. Berden, M. Mulamba, V. Bucarey, T. Guns, F. Fioretto. Decision-Focused Learning: Foundations, State of the Art, Benchmark and Future Opportunities. accepted to JAIR (arXiv:2307.13565v4, 4 Sep 2024). https://arxiv.org/abs/2307.13565 (authors as printed on the arXiv PDF: Mandi, Kotary, Berden, Mulamba, Bucarey, Guns, Fioretto; abstract verified, I then read only the DFL-multiobjective paragraph and the future-opportunities section.)
- Read scope: title page, text around "fair multiobjective optimization" (p. 31), "Theoretical guarantees" paragraph of the future-opportunities section, mentions of nonlinear programs. A survey, not read in full.
- WHAT: States: "While there has been extensive work on providing theoretical guarantees for the SPO+ loss, not all DFL methods offer theoretical guarantees on minimizing regret", and calls for "robust theoretical guarantees ... particularly in the presence of non-linear constraints" and extending frameworks to a wider array of problems. Describes Dinh, Kotary & Fioretto (2024) as DFL for OWA multiobjective aggregation (nondifferentiable).
- Relevance to us: independent confirmation from a survey that regret theory beyond linear objectives and for multiobjective problems is thin.

### 9. Dinh, Kotary & Fioretto (2024), End-to-end learning for fair multiobjective optimization under uncertainty
- Citation: M. H. Dinh, J. Kotary, F. Fioretto. End-to-End Learning for Fair Multiobjective Optimization Under Uncertainty. arXiv:2402.07772v1 (Feb 2024). https://arxiv.org/abs/2402.07772
- Read scope: abstract, introduction, Sec 4.2 (Moreau envelope smoothing of OWA), grep of theorem/guarantee terms. No regret theorem found in the text.
- WHY: Predict-then-optimize with OWA (piecewise linear, fairness) objectives.
- HOW: Replace the nondifferentiable OWA by its Moreau envelope (beta-smooth) so gradients can be backpropagated; Frank-Wolfe with Moreau smoothing.
- WHAT: Purely algorithmic/empirical (portfolio, resource allocation experiments). I found no regret or error-propagation bound for the plug-in solution. The OWA objective is piecewise linear, so by item 3 the first-order regret behaviour is expected there [inferred].
- Relevance to us: an example of multiobjective/minimax-type predict-then-optimize with no guarantee.

### 10. Dhakal & Lachner (2026), ParetoSPO
- Citation: A. Dhakal, T. Lachner. Pareto-Informed Smart "Predict, then Optimize" for Multi-Objective Combinatorial Problems. arXiv:2611.23076v2 (18 Nov 2026). https://arxiv.org/abs/2611.23076
- Read scope: abstract, introduction, related work, discussion/limitations; grep for theorem/bound. Not the method details.
- WHY: Scalarised DFL only reaches the convex hull of the Pareto front.
- HOW: SPO+-style loss whose target is a point on the true Pareto front chosen by cosine similarity with a sampled preference vector; hypervolume regret as the metric.
- WHAT: The introduction states that extending single-objective DFL to multi-objective problems "remains unexplored" and the work is empirical (shortest path and knapsack). No theorem, no bound on Pareto gap. 
- Relevance to us: the multiobjective predict-then-optimize setting has an empirical literature but, in what I found, no regret theory; our "weak-Pareto gap" notion is not defined there.

### 11. Liu, Xu, He & Fang (2024), SPO with dependent data (skimmed, abstract only)
- Citation: J. Liu, T. Xu, J. He, C. Fang. Smart Predict-then-Optimize Method with Dependent Data: Risk Bounds and Calibration of Autoregression. arXiv:2411.12653v1 (Nov 2024). https://arxiv.org/abs/2411.12653
- Read scope: title and abstract only (header). Included only as evidence that the SPO+ calibration line continues for linear objectives; not used for any claim.

(Also downloaded but only searched, not read: Bertsimas & Kallus, From predictive to prescriptive analytics, arXiv:1402.5481; not cited for any claim.)

---

## Is our quadratic bound known?

Short answer: the phenomenon is known; the specific statement is, as far as I found in this cluster, not in print. Honest assessment with evidence:

**What is clearly known**
1. Quadratic (second-order) regret for plug-in solutions under strong convexity is established for smooth problems: Tan & Frazier Thm 3.4 (deterministic, finite-sample, unconstrained, interior optimum, strongly convex in x, with an extra fourth-order term) and Elmachtoub-Lam-Zhang-Zhao eqs (6)-(7) and Thm 2 (asymptotic n R -> (1/2) N'HN, including constrained problems via Lagrangians). Our Steps 4-5 (strong convexity plus gradient error gives gap <= ||g||^2 / (2 mu)) are the same mechanism; Tan & Frazier's bound is of the form (const / rho^2) ||D (thetahat - theta*)||^2, ours is ||g||^2/(2 mu) with g the "gradient mismatch", the same shape.
2. For piecewise-linear structure, regret is first order in the estimation error per instance (Hu-Kallus-Mao Thm 4: Regret <= 2 B E||f* - fhat||; Ho-Nguyen & Kilinc-Karzan Cor 3: true excess risk <= B_X sqrt(excess squared-loss risk)), and faster rates need margin (separation) assumptions plus averaging over contexts (HKM Assumption 2, Thm 8; rate n^{-(1+alpha)/2}). Our Remark 2 (loss first order when a goal is met exactly at a binding trade-off) agrees with this: the kink is the same near-degeneracy that HKM's margin condition excludes.
3. Quadratic-versus-first-order depends on curvature of the objective or feasible set: Liu & Grigas Thm 3 (curved level-set feasible region improves calibration from eps^2 to eps).

**What our theorem adds (to the extent I could check) [inferred]**
- Nonsmooth objective with sign condition. Existing smooth theory (Tan-Frazier, ELZZ) assumes twice differentiability at the optimum. Our objectives max(0, l_k) are not differentiable at kinks. (H2) says each weighted goal with w_k > 0 is strictly on one side of its kink at both the true and learned functions, which makes the subgradient unique and locally the objective smooth in the active pieces. A smooth-theory result would apply locally to the weighted sum after (H2), so the nonsmoothness handling is more a bookkeeping step than a new technique. I did not find any paper in this cluster treating the sign-stability condition as such. (H2) is the kink-analogue of HKM's strict-separation margin.
- Multiobjective weak-Pareto gap. We bound the simultaneous improvement t available in all true objectives, via supporting weights w from a separation argument (Step 1) applied to the learned problem. No paper in the cluster defines a gap of this type: the multiobjective PTO papers found (Dinh et al., Dhakal & Lachner) are empirical, and the survey says guarantees are missing. The reduction (weak Pareto point of a convex vector problem is a minimiser of a weighted sum, standard convex-analysis fact) and the passage from the scalarised regret to the vector gap (Step 6, t sum w_i = t) are elementary, so the novelty here is modest and of the "framework" type, not a new proof technique [inferred].
- A priori the weights w are those supporting the learned solution, so the bound is in terms of data-dependent w, not a worst case over w; this is a feature of our statement. The bound requires w_c > 0, so a weakly Pareto point where all weight sits on goals gets no guarantee. No paper in the cluster has an analogue.
- Constants: linear-in-parameter goals mean the cross-derivative d^2 f / dx dtheta is constant and Tan-Frazier's beta2 term vanishes, so a single clean square [inferred].

**Which results nearly imply ours**
- If one applies Tan-Frazier Thm 3.4 to the weighted-sum scalarisation S_w with the (H2)-restricted smooth pieces, one obtains a quadratic bound on S_w(thetahat) - S_w(theta_w*) of the same form, but (a) it requires w to be fixed independently of the data, whereas our w depends on thetahat; (b) it needs twice differentiability and x* interior; (c) the bound is on a minimiser's regret, and one still needs Step 6 to turn it into a vector gap. So Tan-Frazier "nearly implies" the scalar part for a fixed w. Our direct argument sidesteps (a) because Step 5 only uses the supporting inequality at thetahat, which is valid for the data-dependent w. This is a real, if small, difference.
- ELZZ's second-order expansion gives the same order of magnitude asymptotically for smooth problems.

**Overall judgement [inferred].** Treat our result as a correct and useful specialisation of a known principle (strong convexity gives regret ~ (gradient error)^2 / (2 mu)), carried to the nonsmooth, multiobjective, weakly-Pareto setting with a sign-stability condition. Do not claim the quadratic rate itself as new; claim (i) the weak-Pareto gap formulation, (ii) the data-dependent supporting weights, (iii) the explicit treatment of kinks via sign stability and the first-order counterexample (Remark 2), and (iv) the explicit constant in terms of elasticities. The accurate positioning in the introduction: "quadratic regret for plug-in solutions under strong convexity is known for smooth problems (Tan & Frazier 2022; Elmachtoub et al. 2023); we extend it to ...". I did not search outside arXiv, so an unseen paper in Math Programming, e.g. on stability of parametric convex programs, may state a stronger result; classical sensitivity results for strongly convex programs (Lipschitz stability of solutions, Polyak-Lojasiewicz-type bound f - f* <= ||grad f||^2/(2 mu)) are standard convex analysis I did not retrieve here, so they are not cited [inferred].

---

## Gaps (open problems the papers state, with locators)

- Liu & Grigas 2021, Sec 3 after Cor 3.1: whether the O(n^{-1/4}) rate for SPO+ in the polyhedral case "can also be improved" to O(n^{-1/2}) as for squared loss; Sec 6 lists further directions (the conclusion page says several intriguing future directions exist; I read only the first part).
- Tan & Frazier 2022, Sec 7 (Conclusion): extending to dropping insensitive components of theta / model selection and non-parametric (infinite-dimensional theta) models, "more technical machinery would likely be necessary". Also, their theory is limited to smooth, unconstrained problems with interior optimum (Assumption 3.1; Sec 3).
- Hu, Kallus & Mao 2022, discussion of regret rates and specification: if the model class is misspecified the regret does not converge to zero for plug-in approaches; best-in-class guarantees need IERM. Fast rates hold only under the noise condition (Assumption 2) and well-specification (Assumption 1).
- Elmachtoub, Lam, Zhang & Zhao 2025, Sec 1 and Sec 5: in the constrained case second-order conditions do not make the Hessian positive definite and a pseudoinverse appears, which complicates the dominance result; the analysis is asymptotic and local (twice differentiable, Assumption 3).
- Elmachtoub et al. 2025 (Dissecting), Thm 2 and Table 1: misspecification creates a nonvanishing zeroth-order regret for ETO, so rates for plug-in in misspecified models remain a separate question.
- Mandi et al. 2024 survey, future opportunities, "Theoretical guarantees": regret guarantees are missing for most DFL methods and for problems with non-linear constraints; frameworks should be extended to "a wider array of CO problems".
- Dhakal & Lachner 2026, intro: extension of SPO-type decision-focused learning to multiobjective problems "remains unexplored" (theory absent; their work is empirical). Dinh et al. 2024: no guarantees for OWA/multiobjective PtO were found.
- Ho-Nguyen & Kilinc-Karzan 2022, intro: formal guarantees linking prediction performance to optimization performance were "notably lacking" before their work, and their bounds are worst-case first-order (sqrt) transfers for linear-in-c objectives; whether curvature in x sharpens them (as our Step 5 does) is not discussed [inferred].
- Not in any paper read, [inferred] open for us: a lower bound showing the quadratic rate is attained; behaviour when (H2) fails with positive probability (the kink case); a probabilistic margin version of (H2) in the style of HKM Assumption 2 giving rates for the estimated elasticities; extension to nonconvex goals.
