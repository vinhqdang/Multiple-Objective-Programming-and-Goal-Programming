# Plan and outline

**Target:** Annals of Operations Research special issue "Multiple Objective Programming and Goal Programming: Artificial Intelligence for Decision Making in Economic and Social Sciences". Deadline 30 June 2027. Article type: Original Research; answer "yes" to the special-issue question and give the issue title. A cover letter is required.

**Topics addressed (from the call):** 2 Goal programming techniques and formulations; 3 GP in public policy; 4 AI-enhanced decision support for resource allocation; 6 Integrating machine learning with MOP; 13 Optimization models for social welfare.

## Research question
When marginal effects in a goal-programming budget model are learned from data, does adjusting predictions for uncertainty improve realised goal attainment, and does the answer depend on the GP variant (weighted-sum vs Chebyshev)?

## Design
- Model: WGP and Chebyshev GP over R units and K goals, budget, equity cap and floor.
- Learning: ridge regression per goal; cross-validated residual SD.
- Method under test: shrink predicted effects by lambda residual SDs before solving.
- Evaluation: score allocations with true effects; compare equal split, plug-in, shrunk, oracle; vary n, tau (unit-level noise), sigma (measurement noise).
- Status: implemented and run in simulation (`code/`, `results/`). No field data.

## Manuscript outline
1. Introduction and positioning
2. Model (WGP, CGP, learning, shrinkage)
3. Simulation design
4. Results (main, paired, sensitivity, optimism diagnostic)
5. Discussion and limitations
6. Conclusion

## Before submission
- Replace the synthetic study or add a real-data case (regional budgets with observed outcomes), or reposition as a methods/simulation paper.
- Add a data-driven rule for choosing lambda; test nonlinear learners and decision-focused training.
- Extend with aspiration-level learning and lexicographic GP.
- Run a systematic literature search; the related-work section is currently short.
- If extending a MOPGP'25 conference paper, cite it and say what is new.
- Write the cover letter (contribution to MOPGP, AI, and economic and social sciences).
- Check the journal's submission guidelines for format requirements.
