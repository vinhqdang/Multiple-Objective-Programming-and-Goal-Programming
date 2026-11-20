# Notes on the two theory papers (read 2026-11-20)

Both read from the supplied PDFs: abstract, introduction, definitions, algorithm statement, main theorem statements, finite-termination section (paper 15); abstract, structure and theorem list (paper 14). Proofs were not checked line by line.

## Paper 15: Upadhyay, Poddar, Caristi, Barilla. Inertial proximal point algorithm on Hadamard manifolds (DOI 10.1007/s10479-025-06912-1)
- Problem (NMQOP): minimise Psi(w) = (Psi_1..Psi_m)(w) over a Hadamard manifold M^n (R^n is a special case), unconstrained.
- Assumptions: A1 each Psi_i >= 0; A2 locally Lipschitz; A3 quasiconvex; A4 the set (Psi(w0) - R^m_+) intersect Psi(M) is R^m_+-complete.
- Algorithm (IPPA): inertial extrapolation y^k from w^k, w^(k-1) with weight tau_k; next iterate solves a scalarised proximal subproblem <Psi(w), u_k> + (eta_k/2) dist^2(w, y^k) over the set C_k = {w : Psi(w) <= Psi(w^k)}, with u_k a weight vector chosen each iteration.
- Results: sequence well defined (Thm 3.1); if dist(w^(k+1), w^k) -> 0 every cluster point is Pareto-Mordukhovich critical (Thm 4.1); convergence of the whole sequence to such a point (Thm 4.4); weak Pareto optimal if components are geodesically convex (Cor 4.1); finite termination under extra conditions (Thm 5.1). The authors state parts are new even in R^n.
- Correction to my earlier message: I said I had not found an inertial multiobjective proximal method on Hadamard manifolds. This paper is exactly that.
- Limits relevant to goal programming: unconstrained (the budget constraint is not part of the model); no noise or learned objectives; needs A4.

## Paper 14: Upadhyay, Poddar, Barilla. Robust conic multiobjective semi-infinite programming with vanishing constraints on Riemannian manifolds (DOI 10.1007/s10479-025-06918-9)
- Studies the robust counterpart (RMSIPVC) of uncertain multiobjective semi-infinite programs with vanishing constraints.
- Defines constraint qualifications ACQ, BCQ, RCQ with Mordukhovich subdifferentials; RCQ is the weakest; proves KKT-type necessary conditions under RCQ. Optimality conditions only, no algorithm.

## Possible links to goal programming (not established results)
- Goal deviations d_k(x) = max(0, T_k - c_k'x)/T_k are nonnegative, Lipschitz and convex, so they satisfy A1-A3 on R^n. Goal programming can be read as the multiobjective problem min (d_1..d_K), and IPPA does not need goal weights.
- Ratio goals (cost per beneficiary) are quasiconvex but not convex; they fit A3 and are outside the linear-programming form of goal programming.
- Robust goal constraints (c in an uncertainty set) are semi-infinite constraints; minimum-funding rules (a unit gets 0 or at least a minimum) are vanishing-type constraints. Paper 14's conditions would apply only after the model is stated in its form, which I have not done.
- Nothing here yet is a new theorem. Any claim needs a proof I have not written.
