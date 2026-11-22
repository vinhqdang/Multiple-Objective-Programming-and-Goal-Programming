# Literature cluster 3: multiobjective proximal/descent methods and stability of Pareto sets under perturbation

Compiled 2026-11-22. Downloads are in /tmp/lit3/ (text extracted with pdftotext -layout). Every paper below was retrieved and opened unless it is listed under "Abstract/metadata only". Proofs were not checked line by line. Theorem numbers refer to the version I read (stated per entry). Statements marked [inferred] are my own reading, not claims of the authors.

Notation used below: F = (F_1..F_m) objective; "weakly Pareto" = no point improves all components strictly; u0(x) = sup_z min_i [F_i(x) - F_i(z)] is the Tanabe-Fukuda-Yamashita merit (gap) function (zero iff x weakly Pareto optimal).

Important link to docs/06 [inferred]: the "true gap" g_Theta(theta_hat) in docs/06 is exactly u0 of the true objective with the sup restricted to the box Theta (t >= 0 is automatic since z = x gives 0). So the literature on u0 (papers 8, 9, 10, 11, 12, 16) is the right vocabulary for the quantity we bound.

---

## A. Proximal point and inertial methods

### 1. Bento, Ferreira, Pereira (2017). Proximal point method for vector optimization on Hadamard manifolds
- Citation: G. C. Bento, O. P. Ferreira, Y. R. L. Pereira, Operations Research Letters (2017), DOI 10.1016/j.orl.2017.10.017; arXiv:1512.06081, https://arxiv.org/abs/1512.06081 (I read arXiv v1, 8 pp).
- Read scope: whole paper (it is short), including the proof of Thm 3.1.
- WHY: extend the Bonnel-Iusem-Svaiter proximal point method for vector optimization from R^n to Hadamard manifolds, with a general closed pointed convex cone C.
- HOW: iterate p^(k+1) = argmin over Omega_k = {F(p) <=_C F(p^k)} of f_k(F(p)) + (lambda_k/2) d^2(p,p^k), where f_k is a Gerstewitz-type nonlinear scalarisation f_k(y) = max_{z in Z} <y,z>/<e^k,z>. Fejer convergence to the intersection of the level sets.
- WHAT: Thm 3.1: if F is C-convex, (A1) C = {y : <y,z> >= 0, z in Z} with Z compact, (A2) the intersection of all Omega_k is nonempty (guaranteed by C-completeness of (F(p0) - C) cap F(M)), and {lambda_k} bounded, then the sequence is well defined and converges to a weakly efficient point. Sect. 4: Thm 4.1 relates weak sharp minima of F to those of f o F; the authors only "expect" finite termination (stated as future work). No inertia, no inexactness, no perturbation. Convex, not quasiconvex.

### 2. Apolinario, Papa Quiroz, Oliveira (2016). A scalarization proximal point method for quasiconvex multiobjective minimization
- Citation: H. C. F. Apolinario, E. A. Papa Quiroz, P. R. Oliveira, Journal of Global Optimization (2016), DOI 10.1007/s10898-015-0367-3; arXiv:1403.0150 (v4), https://arxiv.org/abs/1403.0150. Year of the journal version taken from OpenAlex metadata (2015 online); I read the arXiv version.
- Read scope: abstract, introduction, Sect. 3 (algorithm, assumptions, Fejer convergence, main theorem and corollaries), start of Sect. 4 (applications).
- WHY: Bonnel et al. proximal method needs convexity; extend to locally Lipschitz quasiconvex F on R^n (motivation: demand theory).
- HOW: SPPM step: find x^(k+1) in Omega_k = {F <= F(x^k)} with 0 in Clarke subdifferential of <F(.),z_k> + (alpha_k/2)<e^k,z_k>||. - x^k||^2 plus normal cone N_Omega_k. Uses Clarke subdifferentials, Fejer convergence to E = {x : F(x) <= F(x^k) for all k}.
- WHAT: assumptions (H1) F locally Lipschitz, (H2) F is R^m_+-quasiconvex, (H3) (F(x0) - R^m_+) cap F(R^n) is R^m_+-complete. Thm 3.4.1: if 0 < alpha_k < alpha_tilde the sequence converges to a Pareto-Clarke critical point. Cor 3.4.1: if F is R^m_+-convex the limit is weak Pareto. Cor 3.4.2: C^1 case gives Pareto critical point. Assumptions are the ones reused (with the Mordukhovich subdifferential) in the IPPA paper; (H3) is the "A4" of docs/04. Exact subproblem; no inexactness.

### 3. Papa Quiroz, Apolinario, Villacorta, Oliveira (2015 preprint). A linear scalarization proximal point method for quasiconvex multiobjective minimization
- Citation: E. A. Papa Quiroz, H. C. F. Apolinario, K. D. V. Villacorta, P. R. Oliveira, arXiv:1510.00461 (v1, 2 Oct 2015), https://arxiv.org/abs/1510.00461. I did not confirm a journal version.
- Read scope: abstract, introduction, statements of Thms 4.1.1, 4.3.1-4.3.3, 4.4.1, 5.1.1, and the full inexact algorithm (Sect. 5) including the key estimate.
- WHY: allow lower semicontinuous (not locally Lipschitz) quasiconvex F, constrained problems, and an implementable inexact step.
- HOW: ISPP algorithm: x^(k+1) in Omega_k with 0 in eps_k-subdifferential of Psi_k + alpha_k(x^(k+1) - x^k) + N_Omega_k, where sum of delta_k < infinity (eqs. (38)-(40)); in the C^1 case g_k = grad Psi_k(x^(k+1)) + eps_k h_k, ||h_k|| <= 1.
- WHAT: Thm 5.1.1: under (C1.2),(C2),(C3),(C4) and 0 < alpha_k < alpha_tilde the ISPP sequence converges to a Pareto critical point. Error model = subproblem (inner solve) inexactness that is summable; objective F itself is exact.

### 4. Yin, Tang (2026). Multiobjective inertial gradient systems with time scaling; implicit discretisation MIPP
- Citation: Y.-D. Yin (Yingdong Yin), L. Tang, arXiv:2508.07254 (v3, 7 Jan 2026; v3 title "Fast Convergence of Multiobjective Inertial Gradient Systems with Time Scaling"); published as "Fast Convex Optimization via Multiobjective Inertial Gradient Systems with Time Scaling", J. Oper. Res. Soc. China (2026), DOI 10.1007/s40305-026-00700-9 (from OpenAlex; I read the arXiv text only). https://arxiv.org/abs/2508.07254
- Read scope: abstract, introduction, preliminaries (merit function), statements of Thms 2.1, 4.1, 4.2, 4.3, 5.1, 5.2, the energy computation for MIPP (Sect. 5), Remark 1, conclusion.
- WHY: accelerate multiobjective inertial dynamics; give the multiobjective analogue of inertial proximal/FISTA-type rates.
- HOW: Lyapunov analysis of a second-order ODE with vanishing damping alpha/t and time-scaled gradient term; its implicit discretisation is MIPP: y_k = x_k + (k-1)/(k+alpha-1)(x_k - x_(k-1)), x_(k+1) = prox_{lambda_k Phi_(x_k)}(y_k) with Phi_x(z) = max_i (f_i(z) - f_i(x)).
- WHAT: all f_i convex (Thm 5.1: lsc suffices for the rate). Thm 5.1: u0(x_k) = O(1/(k^2 beta_k)) and ||x_k - x_(k-1)|| = O(1/k). Thm 5.2: under Assumption 2.1 (finite distance R to the weak Pareto level set) and either continuity or F^inf in F(P), x_k converges to a weakly Pareto point. Remark 1 (after Thm 4.3): for m > 1 the o(1/t^2) / ||x'(t)|| = o(1/t) conclusions cannot be derived because min_i (f_i(x) - f_i(x*)) need not be nonnegative; "an open problem we leave for future work". Convex only: no quasiconvexity, no manifolds, no noise. This is the inertial multiobjective proximal method that the user asked about (arXiv 2508.07254).

### 5. Tanabe, Fukuda, Yamashita (2023). An accelerated proximal gradient method for multiobjective optimization
- Citation: H. Tanabe, E. H. Fukuda, N. Yamashita, Computational Optimization and Applications (2023), DOI 10.1007/s10589-023-00497-w; arXiv:2202.10994 (v4), https://arxiv.org/abs/2202.10994.
- Read scope: abstract, introduction, Sect. 2-3 (merit function, Prop 3.1, Thm 3.1), Thm 5.1, Thm 5.2, Cor 5.2, conclusions. Dual subproblem section skimmed only.
- WHY: accelerated (FISTA-like) multiobjective method with a proven rate had been open.
- HOW: subproblem includes the extra terms f_i(y) - F_i(x) so that max over i can be telescoped; solved through the dual.
- WHAT: Thm 2.1 (from Tanabe et al. 2023 merit paper): u0 >= 0 and u0(x) = 0 iff x is weakly Pareto. Prop 3.1: p_l(x) = x iff x weakly Pareto iff theta_l(x) = 0 (a stopping test). Thm 3.1: plain proximal gradient gives u0(x_k) <= l R/(2k) under Assumption 3.1 (finite R). Thm 5.1: F_i(x^k) <= F_i(x^0) for all k (not monotone). Thm 5.2 and Cor 5.2: u0(x_k) = O(1/k^2); accumulation points weakly Pareto. Conclusion: convergence of the iterates themselves is not proved; extension to vector optimization is future work. Exact gradients assumed.

### 6. Tanabe, Fukuda, Yamashita (2022). Convergence rates analysis of a multiobjective proximal gradient method
- Citation: H. Tanabe, E. H. Fukuda, N. Yamashita, Optimization Letters (2022), DOI 10.1007/s11590-022-01877-7; arXiv:2010.08217 (v5), https://arxiv.org/abs/2010.08217.
- Read scope: abstract, introduction, statements of Thms 3.1, 3.2, 5.1, 5.2, 5.3, 5.4 (proofs not read).
- WHY/HOW: rates for the multiobjective proximal gradient method via merit functions, extending the Polyak-Lojasiewicz inequality.
- WHAT: Thm 5.1 (nonconvex): min_j w_1(x_j) = O(1/k); Thm 5.2 (all F_i convex, Assumption 5.1): u0(x_k) <= lR/(2k); strongly convex gives linear rate; a multiobjective proximal-PL inequality gives linear rate (Thm 5.4 with constant tau). Exact subproblems and gradients.

### 7. Bello-Cruz, Melo, Prudente, Serra (2025). A proximal gradient method with an explicit line search for multiobjective optimization
- Citation: Y. Bello-Cruz, J. G. Melo, L. F. Prudente, R. V. G. Serra, Computational Optimization and Applications (2025), DOI 10.1007/s10589-025-00711-x; arXiv:2404.10993 (v1, Apr 2024), https://arxiv.org/abs/2404.10993.
- Read scope: abstract, introduction, Thm 3.2, Thm 4.4, Thm 5.4 statement and first lines of proof.
- WHAT: convex F_j = G_j + H_j, backtracking line search needing one proximal subproblem per iteration. Thm 4.4: sequence converges to a weakly Pareto point under (A1). Thm 5.4: an epsilon-approximate weakly Pareto point (|theta_alpha(x^k)| <= eps) in O(1/eps) iterations. Relevant only as a definition of an epsilon-approximate weakly Pareto point through a stationarity residual.

### 8. Tanabe, Fukuda, Yamashita (2023). New merit functions for multiobjective optimization and their properties
- Citation: H. Tanabe, E. H. Fukuda, N. Yamashita, Optimization (2023), DOI 10.1080/02331934.2023.2232794; arXiv:2010.09333 (v3, 9 Apr 2023), https://arxiv.org/abs/2010.09333.
- Read scope: abstract, introduction, Sect. 3 (definitions and basic properties, Thms 3.1, 3.2, 3.4, 3.9), Thm 4.1, Thm 4.2, Sect. 6 (proximal-PL and error bounds, Prop 6.2).
- WHY: a merit function should return zero exactly at solutions, be continuous, have bounded level sets, and give error bounds; the paper builds these for lsc, convex and composite multiobjective problems.
- HOW: u0 (sup over z of min_i [F_i(x) - F_i(z)]), regularised u_l, and for composite F_i = f_i + g_i the partially linearised w_l(x) = sup_y min_i [grad f_i(x)'(x-y) + g_i(x) - g_i(y) - (l/2)||x-y||^2].
- WHAT: Thm 3.1: u0 >= 0, zero iff weakly Pareto. Thm 3.2: u0 is lsc. Thm 3.4: u_l and its maximiser map are locally Lipschitz/Holder (the text near eq. (15)-(16) gives local Holder continuity of the maximiser map with exponent 1/2). Thm 4.1(i): if each f_i is mu_i-strongly convex, mu = min mu_i >= 0, then u0(x) <= w_mu(x) and u_l(x) <= w_(mu+l)(x). Thm 4.2: w_r <= w_l <= (r/l) w_r for r >= l. Def 6.1 and Prop 6.2: proximal-PL inequality w_L >= tau u0, with tau = min(mu/L, 1) when f_i are strongly convex. Error bounds to the solution set, not perturbation of F.
- Relevance [inferred]: Thm 4.1(i) is the same mechanism as Steps 4-6 of docs/06 (strong convexity turns a stationarity residual into a gap bound of order residual squared over mu), but it is stated for the exact objective and its own stationarity measure, not for a point computed from a different objective.

---

## B. Inexact or perturbed versions of these algorithms

### 9. Fan, Tang, Yang (2026). An inexact proximal gradient method for composite multiobjective optimization with absolute and relative stopping criteria
- Citation: Z. Fan, L. Tang, X. Yang, arXiv:2611.22361 (v1, 17 Nov 2026), https://arxiv.org/abs/2611.22361. Preprint; no journal version found.
- Read scope: abstract, introduction, Defs 3-4 (approximate optimality condition AOC), Assumption 1, Lemma 10, Thms 4, 5, 6, conclusion.
- WHY: subproblems of the multiobjective proximal gradient method are not available in closed form; existing convergence results assume exact solves.
- HOW: AOC with eps_1, eps_2 and a residual w: w in (u - x)/beta + sum lambda_i grad f_i(x) + eps_1-subdifferential of h + sum lambda_i g_i(u), and 0 in -phi(u - beta w; x) + eps_2-normal cone of the simplex at lambda. Armijo-type line search tolerating the errors; inner inexact projected gradient + ADMM.
- WHAT: Assumption 1: initial level set of F is nonempty and bounded. With summable errors eta_k: Thm 4: iterates bounded, every accumulation point lies in the reference set U_inf, each F_i(x^k) converges, sum ||x^(k+1) - x^k||^2 < inf. Thm 5: with weighted summability (sum (l+1) eta_l finite) min_i [F_i(x^k) - F_i(z)] <= R_k(z)/(2 beta_min gamma_min k), i.e. O(1/k) in u0. Thm 6: every accumulation point is weakly Pareto for F. The perturbation is solver error that vanishes (summable); F is exactly known. Future work named: Nesterov acceleration with inexact stopping.

### 10. Zhang, Yang (2023 preprint). The convergence rate of the accelerated proximal gradient algorithm for multiobjective optimization is faster than O(1/k^2)
- Citation: J. Zhang, X. Yang, arXiv:2312.06913 (v1, 12 Dec 2023), https://arxiv.org/abs/2312.06913. Preprint ("Noname manuscript"); journal version not confirmed.
- Read scope: abstract, introduction, Thm 1 statement, Sect. 5 "Stability" (inexact version with additive gradient error), Thm 3, conclusion.
- WHY: improve the O(1/k^2) of Tanabe et al. to o(1/k^2) with extrapolation (k-1)/(k+alpha-1), alpha > 3, and handle inexactness.
- HOW: errors enter as grad f_i(y) + eps in the subproblem (their eq. (18)); the Lyapunov energy picks up the terms (k+alpha-1)<eps^(k+1), x* - u^(k+1)>.
- WHAT: Thm 1(v): u0(x_k) = o(1/k^2), ||x_(k+1) - x_k|| = o(1/k). Thm 3: if sum_k (k+alpha-1)||eps_k|| < infinity, the conclusions of Thm 1 hold for the inexact algorithm (same rate). This is the only retrieved result in which the objective's gradient is perturbed (additively), but the perturbation must be summable with weights growing in k; a persistent perturbation is not covered. The conclusion states this resolves the open issue raised in the Tanabe et al. paper.

### 11. Liu, Vicente (2019/2021). The stochastic multi-gradient algorithm for multi-objective optimization and its application to supervised machine learning
- Citation: S. Liu, L. N. Vicente, arXiv:1907.04472 (v3, 5 Feb 2021), https://arxiv.org/abs/1907.04472. The text I have does not state the journal; I did not confirm a published version.
- Read scope: abstract, introduction, Assumptions 5.1-5.7, Thms 5.1, 5.2, 5.3 and the discussion preceding Assumption 5.6.
- WHY: real MOO problems have noisy/uncertain data; study the stochastic analogue of the multi-gradient (Fliege-Svaiter) method.
- HOW: stochastic multi-gradient direction from a quadratic subproblem; it is biased even if individual gradient estimators are unbiased; analysis of the weighted function S(x,lambda) = sum lambda_i f_i(x) with lambda_k the multipliers at iteration k.
- WHAT: Assumption 5.1 (Lipschitz gradients), 5.2 (unbiased individual gradients with bounded bias/variance, bias <= alpha_k(C_i + C_hat_i ||grad f_i||)), 5.3 (bounded feasible set), 5.4 (Lipschitz subproblem solution), 5.5 strong convexity. Thm 5.1 (strong convexity, alpha_k = c/(k+1)): min_s E[S(x_s,lambda_s)] - E[S(x*,lambda_bar_k)] <= const/(c(k+1)). Thm 5.2 (with Assumption 5.6, grad_x S(x*, lambda_k)'(x_k - x*) >= 0): E||x_k - x*||^2 <= max{...}/k, plus the same rate for S(.,lambda*). Thm 5.3 (convex, alpha_k = alpha_bar/sqrt(k)): O(1/sqrt(k)). They note explicitly that lambda* is only defined at convergence ("the multi-gradient method cannot anticipate which optimal weights are being approached"), which is why Assumption 5.6 is needed. Noise is in the iteration, the objective is the true expected one.

### 12. Norkin (2026). Sample average approximation of multiobjective stochastic optimization problems with application in insurance
- Citation: B. V. Norkin, arXiv:2609.18159 (v1, 16 Sep 2026), https://arxiv.org/abs/2609.18159. Preprint (UDK 368:519.21; the paper works with maximisation).
- Read scope: abstract, introduction, Definitions 2-3, examples E1-E5, Theorem 1 with its proof, Lemmas 2-3, Theorem 2.
- WHY: replace a stochastic vector objective by sample averages and finite feasible samples; define approximate solutions as epsilon-nondominated points.
- HOW: continuous convergence / graphical convergence from below of F^i to F on X_i -> X; X*(eps) = set of eps-nondominated points; Hoeffding bound gives sup_(x in X_i) ||F^i - F|| -> 0 a.s.
- WHAT: Thm 1: if X_i -> X compact and F^i converges graphically from below to F, eps_i -> eps, then for each eps' < eps: X*(eps') subset liminf X_i*(eps_i) subset limsup X_i*(eps_i) subset X*(eps). Thm 2: a.s. version for random search, using sup-norm convergence of the empirical objective (E4/E5). Qualitative outer-semicontinuity of eps-nondominated sets under uniform approximation of the objective; there is no rate and no quantitative relation between the size of the objective error and the size of eps.

---

## C. Stability and sensitivity of efficient / Pareto sets

### 13. Tanino (1988). Sensitivity analysis in multiobjective optimization
- Citation: T. Tanino, J. Optim. Theory Appl. (1988), DOI 10.1007/BF00939554 (from OpenAlex). I read the IIASA working paper WP-86-5 (Feb 1986), http://pure.iiasa.ac.at/id/eprint/2854/1/WP-86-005.pdf, which carries the "not for quotation" header and may differ from the journal text.
- Read scope: preface, introduction, Sect. 2 (Thm 2.1), Sect. 3 (Prop 3.1, Cor 3.1, Thm 3.2), Sect. 4 (Lemma 4.1, Thm 4.1), Sect. 5 (Thm 5.1), conclusion.
- WHY: only qualitative continuity of the perturbation map W(u) = Min_P Y(u) (set of minimal points of the perturbed feasible set) was known; derive quantitative information.
- HOW: Aubin's contingent derivative of set-valued maps, applied to the perturbation map of problems with parametrised constraints, linked to Lagrange multipliers.
- WHAT: Thm 2.1: Min_P D(F+P)(f,z)(v) subset DF(f,z)(v). Thm 3.2: if Y is P-minicomplete near u and upper locally Lipschitz at u, and y is properly P-minimal, then Min_P DY(u,y)(v) subset DW(u,y)(v). Thm 4.1: conditions (i) X upper locally Lipschitz, (ii) X compact near u, (iii) y properly P-minimal, (iv) uniqueness of the preimage, (v) a Lipschitz-type condition at (u,y) give a relation for all directions. Thm 5.1: contingent derivative of W in terms of the Lagrange multiplier vector for problems with C^1 data and right-hand-side-perturbed inequality constraints. The perturbation parameter enters the constraint right-hand side or smoothly. Authors' open problems (Sect. 6): the contingent derivative is not completely characterised; "the Lipschitz continuity of the perturbation map is not studied here"; effects of convexity or linearity are to be clarified. Derivative = first-order object.

### 14. Tanino (1988). Stability and sensitivity analysis in convex vector optimization
- Citation: T. Tanino, SIAM J. Control Optim. (1988), DOI 10.1137/0326031 (from OpenAlex). Read the IIASA working paper WP-86-15 (March 1986), http://pure.iiasa.ac.at/id/eprint/2844/1/WP-86-015.pdf.
- Read scope: abstract, introduction, statements of Thms 3.1, 3.2, 4.1, 4.2, 5.1, 5.2, 5.3 (proofs skimmed), remarks on conditions.
- WHAT: perturbation map W(u) = Min_P Y(u) for convex problems. Thm 3.1: W is upper semicontinuous at u if u in int dom Y, Y upper semicontinuous at u, and W(u) = w-Min_P Y(u) (weakly minimal points). Thm 4.2: W is lower semicontinuous at u if u in int dom Y, X(u) closed near u, and a boundedness condition on the level-set map holds. Thm 5.1-5.3: contingent derivative characterisation under minicompleteness and normal minimality. Here Y is the image of the feasible set with the objective fixed; perturbation parameters enter jointly with the constraints; results are semicontinuity and first-order derivatives, not rates.

### 15. An, Tung (2024). Sensitivity analysis in parametric convex vector optimization
- Citation: D. T. V. An, L. T. Tung, Set-Valued and Variational Analysis (2024), DOI 10.1007/s11228-024-00733-3; arXiv:2306.06947 (v1, 12 Jun 2023), https://arxiv.org/abs/2306.06947.
- Read scope: abstract, introduction, statements of Thms 1-6 and the concluding remarks (proofs and examples skimmed).
- WHAT: for f(p,x) K-convex and K-closed, C(p) closed convex (parameter p), the Frechet coderivative of the profile of the perturbation map F, weak perturbation map W and proper perturbation map P. Thm 1: formula for D*(F+K)(p,y)(y*) = union over (p*,x*) in D*(f+K) of p* + D*C(p,x)(x*), under (i) R_+(reg H - dom f) closed subspace and (ii) R_+(P - dom C) closed subspace. Thms 2-4: same for F, W, P under domination conditions; with f C^1, D*(W+K)(p,y)(y*) = grad_p f^*(y*) + D*C(grad_x f^*(y*)). Thms 5-6: constraint systems. First-order (coderivative) information; the introduction places it in the line Tanino, Chuong-Yao, Taa, An-Gutierrez. No quantitative error bound on a solution computed at a perturbed parameter.

### 16. Canovas, Lopez, Mordukhovich, Parra (2020). Subdifferentials and stability analysis of feasible set and Pareto front mappings in linear multiobjective optimization
- Citation: M. J. Canovas, M. A. Lopez, B. S. Mordukhovich, J. Parra, Vietnam J. Math. (2020), DOI 10.1007/s10013-020-00402-6; arXiv:1907.09985 (v1), https://arxiv.org/abs/1907.09985.
- Read scope: abstract, introduction (problem MLP(b), definitions, contributions), statements of Thms 1, 2, 3, 7, 8, 9 (proofs not read).
- WHAT: multiobjective LP min (<c_1,x>,...,<c_q,x>) s.t. <a_t,x> <= b_t; only the right-hand side b is perturbed, the objective vectors c_1..c_q are fixed (their eq. (1)). The epigraphical Pareto front map EP(b) = P(b) + R^q_+ is studied: subdifferentials via coderivatives, Lipschitz-like property, Lipschitz modulus formulas (Thms 7, 8: relation between the moduli of the feasible-set and Pareto-front maps; Thm 9: ordinary LP case). The introduction notes that Lipschitzian behaviour of the optimal set under objective perturbation was treated for LP in earlier work ([5], [6] of that paper), and that coderivative analysis of frontier and solution maps for generalised order optimality exists in infinite dimensions (Huy-Mordukhovich-Yao 2008, abstract only seen via OpenAlex). Closest quantitative Lipschitz result found, but perturbations hit constraints, not the objective coefficients.

---

## D. Abstract/metadata only (full text not retrievable: paywalled or blocked)

- Zhao, Qi, Jolaoso, Shehu, Yao, Yao (2024). An inexact proximal point method for quasiconvex multiobjective optimization. Computational and Applied Mathematics, DOI 10.1007/s40314-024-02828-x. Abstract: absolute and relative error criteria; convergence to a Pareto stationary point (C^1) or weak Pareto point (convex lsc); linear rate under relative error with bounded regularisation parameters plus a growth condition, superlinear if the parameters go to zero. A Southampton eprint (eprints.soton.ac.uk/492782) exists but the proxy returned an anti-bot page.
- Upadhyay, Poddar, Chuong (2026). Convergence analysis of an inexact inertial proximal point algorithm for multiobjective quasiconvex optimization problems. Numerical Algorithms, DOI 10.1007/s11075-026-02423-7. Abstract: IIPPA-QD (inexact inertial PPA with quasi-distance, limiting subdifferential), well-definedness, cluster points are Pareto critical, weak Pareto under convexity, finite termination rule. Most relevant paywalled paper: it is the inexact inertial version of the IPPA we use.
- Upadhyay, Poddar, Yao, Zhao (2025). Inexact proximal point method with a Bregman regularization for quasiconvex multiobjective optimization problems via limiting subdifferentials. Annals of Operations Research, DOI 10.1007/s10479-024-06461-z. Abstract: IPPMB1/IPPMB2 under two error criteria; convergence to Pareto-Mordukhovich critical points; linear/superlinear rates for IPPMB2.
- Papa Quiroz, Baygorrea Cusihuallpa, Maculan (2020). Inexact proximal point methods for multiobjective quasiconvex minimization on Hadamard manifolds. J. Optim. Theory Appl., DOI 10.1007/s10957-020-01725-7. Abstract: two inexact scalarization PPMs on Hadamard manifolds; convergence to Pareto critical points, weak Pareto in the convex case; demand-theory application.
- Bonnel, Iusem, Svaiter (2005). Proximal methods in vector optimization. SIAM J. Optim. 15(4), 953-970. Not retrieved (SIAM page blocked). Existence and citation details confirmed only through the reference lists of papers 1 and 2; the DOI is not confirmed.

---

## Synthesis

### (a) Is there an existing bound on the weak-Pareto gap of a point computed from a perturbed objective, and of what order?

In the 16 papers read, no. What exists falls into four groups, none of which gives the statement of docs/06:
1. Qualitative stability: Tanino (13, 14) gives upper/lower semicontinuity of the efficient set map; Norkin (12) gives outer semicontinuity of epsilon-nondominated sets under uniform approximation of the objective (Thm 1, Thm 2). No rate: the relation between the objective error and the tolerance is not quantified.
2. First-order sensitivity: contingent derivative (Tanino 13, 14) and coderivative (An-Tung 15), Lipschitz moduli of the Pareto-front map (Canovas et al. 16). These describe how the efficient set or front moves to first order in a parameter, and the parameter is a constraint right-hand side or a smooth parameter, not the coefficient vector of nonsmooth goal functions. They bound a distance between sets (or its derivative), not the improvement that remains available at a computed point.
3. Gap/merit functions: Tanabe et al. (8) define exactly the gap u0 and prove u0 <= w_mu under strong convexity (Thm 4.1(i)) and error bounds through a proximal-PL inequality (Prop 6.2). Order: the gap is bounded by a stationarity-type quantity (their w), and the strongly convex mechanism produces residual-squared over mu behaviour [inferred]. But this is for a single exact objective.
4. Perturbed algorithms: see (b).

Order in the perturbation [inferred]: first-order results (Tanino, An-Tung, Canovas) are statements about derivatives/Lipschitz moduli of the solution or front map, so a displacement of the solution is O(perturbation). The gap in the objective values at a point that is only perturbed-optimal is a different quantity. In the scalar strongly convex case the standard fact is "regret <= ||g||^2/(2 mu)" with g = O(perturbation), i.e. second order in the perturbation; this is what docs/06 Steps 4-6 do, and Tanabe et al. Thm 4.1(i) is the same inequality in merit-function language. The second-order claim fails when the true objective is nonsmooth at the learned optimum (docs/06 Remark 2: kink case is first order); that corresponds to the condition that is needed in Tanino's framework for Lipschitz behaviour but is not covered by a quadratic bound [inferred]. I did not find a printed statement of "weak Pareto gap of a weakly Pareto point of a perturbed convex multiobjective problem is O(perturbation^2) under sign stability of subgradients"; the answer to "does it exist" is "not found in this cluster". The literature on predict-then-optimize regret (other clusters) may contain the scalar analogue; I did not search it here.

### (b) What do inexact/perturbed multiobjective proximal methods guarantee?

- All guarantees are about the objective the method is given: summable subproblem or gradient errors do not change the limit set. Fan et al. (9): summable (weighted summable for the rate) eta_k gives bounded iterates, accumulation points weakly Pareto for F (Thm 4, 6) and u0 = O(1/k) (Thm 5). Zhang-Yang (10): sum (k+alpha-1)||eps_k|| < infinity keeps the o(1/k^2) rate of u0 (Thm 3). Papa Quiroz et al. (3): sum delta_k < infinity in the eps-subdifferential keeps convergence to a Pareto critical point (Thm 5.1.1). Zhao et al. (abstract only): absolute/relative error criteria, linear rate with a growth condition. Upadhyay et al. (abstract only): inexact inertial, Pareto critical limit points.
- Stochastic version: Liu-Vicente (11) gets O(1/k) (strongly convex) and O(1/sqrt k) (convex) rates in expectation for the weighted function, with diminishing step sizes and a bias bound that must shrink with the step size.
- A fixed perturbation of the objective itself (the situation of learned coefficients) is not covered by any of them: a nonvanishing error is outside the summability assumptions. Norkin (12) covers an objective approximated by F^i with sup-norm error going to 0, giving only set-valued semicontinuity.
- Conclusion for our paper [inferred]: the algorithm theory (IPPA, Cor 4.1 of the IPPA paper) gives a weakly Pareto point of the learned problem; whatever passes from learned to true must come from a separate sensitivity argument such as docs/06. The inexact-solver literature only justifies stopping the inner proximal solves early.

### (c) Gaps stated by the authors (with locators) and my inferences

Author-stated:
- Tanino WP-86-5, Sect. 6: Lipschitz continuity of the perturbation map not studied; converse inclusion of Thm 3.2 open; effect of convexity/linearity to be clarified.
- Tanabe et al. APG (5), Conclusion: convergence of the iterates themselves not proved; extension to vector optimization (variable domination structure) is future work.
- Bento et al. (1), Sect. 4: finite termination under weak sharp minima is only expected ("We foresee further progress"), no proof.
- Yin-Tang (4), Remark 1 after Thm 4.3: o(1/t^2) for min_i (f_i(x(t)) - f_i(x*)) cannot be derived for m > 1; proving ||x'(t)|| = o(1/t) or a counterexample is an open problem.
- Fan et al. (9), Sect. 7: acceleration with inexact stopping rules is future work.
- Liu-Vicente (11), text before Assumption 5.6: the limiting weights are not known a priori, so an extra assumption relating lambda_k to lambda* is needed.
- Canovas et al. (16), eq. (1) and introduction: only right-hand-side perturbation is analysed; objective vectors c_i are fixed (not stated as a gap, but it is a scope limit).

My inferences [inferred]:
- No quantitative stability result in this cluster treats perturbation of the objective coefficients of a nonsmooth convex multiobjective problem, nor the gap u0 at a perturbed solution.
- No retrieved inexact method treats a persistent (non-summable) objective error; "inexact" always means vanishing solver error.
- Inertial multiobjective proximal results found: IPPA (Hadamard, quasiconvex, no rate), MIPP (Euclidean, convex, O(1/(k^2 beta_k)) in u0, Yin-Tang 4), and the paywalled inexact inertial paper of Upadhyay et al. 2026. The combination "inertial + inexact + rate in u0 + quasiconvex" is not available in the papers read.
- The supporting-weights step of docs/06 (Step 1) matches the way Liu-Vicente and Tanabe et al. use weights; the novelty claimed in docs/06 would be the sign-stable true subgradient (Step 3) combined with strong convexity of the known cost term. I have not seen that in any of the 16 papers.

---

## Paywalled or not retrieved: please download

1. Upadhyay, Poddar, Chuong. Convergence analysis of an inexact inertial proximal point algorithm for multiobjective quasiconvex optimization problems. Numerical Algorithms. DOI 10.1007/s11075-026-02423-7.
2. Zhao, Qi, Jolaoso, Shehu, Yao, Yao. An inexact proximal point method for quasiconvex multiobjective optimization. Comput. Appl. Math. DOI 10.1007/s40314-024-02828-x (Southampton eprint 492782 may work in a browser).
3. Upadhyay, Poddar, Yao, Zhao. Inexact proximal point method with a Bregman regularization for quasiconvex multiobjective optimization problems via limiting subdifferentials. Ann. Oper. Res. DOI 10.1007/s10479-024-06461-z.
4. Papa Quiroz, Baygorrea Cusihuallpa, Maculan. Inexact proximal point methods for multiobjective quasiconvex minimization on Hadamard manifolds. J. Optim. Theory Appl. DOI 10.1007/s10957-020-01725-7.
5. Bonnel, Iusem, Svaiter. Proximal methods in vector optimization. SIAM J. Optim. 15(4), 953-970 (2005); DOI to be confirmed.
6. Tanino. Sensitivity analysis in multiobjective optimization. JOTA, DOI 10.1007/BF00939554, and Stability and sensitivity analysis in convex vector optimization, SIAM J. Control Optim., DOI 10.1137/0326031 (journal versions; I read working papers).
7. Found in searches but not read (candidate leads): Papa Quiroz, Oliveira, Full convergence of the proximal point method for quasiconvex functions on Hadamard manifolds, ESAIM COCV, DOI 10.1051/cocv/2011102 (publisher PDF returned an anti-bot page); Huy, Mordukhovich, Yao, Coderivatives of frontier and solution maps in parametric multiobjective optimization, Taiwanese J. Math. (2008), DOI 10.11650/twjm/1500405137 (open PDF on Project Euclid, not downloaded); Bento, Cruz Neto, Lopez-Acedo, Proximal point method for locally Lipschitz functions in multiobjective optimization with application to the compromise problem, SIAM J. Optim. (2018), DOI 10.1137/16M107534X; Lara, Tran, Proximal point type algorithms for solving multiobjective optimization problems beyond convexity, Optimization (2026), DOI 10.1080/02331934.2026.2628001. These exist per OpenAlex metadata only.

OpenAlex search budget was exhausted partway through (rate limit message), so the search for perturbation/Hausdorff stability papers was completed with the arXiv API only; the search for a published rate result on perturbed multiobjective problems may be incomplete.
