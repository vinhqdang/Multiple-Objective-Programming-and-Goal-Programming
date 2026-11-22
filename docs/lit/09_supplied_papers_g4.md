# Papers supplied by the project owner for direction G4 (read 2026-11-22)

## Roland, Figueira & De Smet (2016). Finding compromise solutions in project portfolio selection with multiple experts by inverse optimization. Computers & Operations Research 66, 12-19. https://doi.org/10.1016/j.cor.2015.07.006
- Read: abstract, introduction, conclusion (sections 1 and 7); formulation sections skimmed.
- WHY: a group of experts evaluates projects differently; a compromise portfolio is needed.
- HOW: multiobjective knapsack where each objective is one expert's evaluation. The inverse problem finds the minimal adjustment of the experts' evaluation coefficients (under several distances) so that some portfolio becomes ideal (optimal for all experts). Two algorithms: one inverse problem per efficient solution, and a cutting-plane method. Monotonicity and dominance properties proved.
- WHAT: computational results on random knapsack instances and two illustrative examples.
- Relevance: low for G4. It uses inverse optimization to define a compromise among objectives, not to infer weights or targets from observed decisions. Useful only as an example of adjusting objective coefficients in an inverse multiobjective problem.

## Carrizosa, Gomez-Vargas & Piccialli (2026). A clustering-based framework for preference inference in inverse multiobjective optimization. Omega 145, 103675. https://doi.org/10.1016/j.omega.2026.103675 (open access, CC BY-NC-ND)
- Read: abstract, introduction and contributions (sections 1, 1.2), section headings, conclusions (section 6).
- WHY: decision makers are heterogeneous; estimating one weight vector per decision maker from noisy, weakly informative decisions is unstable.
- HOW: infer linear objective functions and preference (weight) vectors jointly while clustering decision makers by preference structure. Loss is regret (objective value of the observed decision minus the optimal value under inferred preferences), giving MIQPs; interpretability through sparse cluster-representative weights from an expert-driven catalogue; alternating heuristic for warm starts. Model II covers partially known objectives.
- WHAT: synthetic data and a diet recommendation problem.
- Limits stated by the authors (section 6): linear objectives only; nonlinear objectives would need convex duality, conic formulations or piecewise-linear surrogates, not assessed; equal treatment of instances (OWA mentioned as an alternative).
- Relevance: high as a method neighbour. Clustering states or districts by revealed priority profile is directly usable for G4, and regret is the loss family recommended in notes 05-06. It does not infer aspiration levels (targets), has no goal-deviation (kinked) objectives and no identification theory for them, which is the space G4 would occupy.
