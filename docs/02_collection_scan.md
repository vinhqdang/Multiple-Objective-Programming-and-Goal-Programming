# Collection scan, v2 (replaces the title-only version)

Source: Crossref and OpenAlex metadata, plus the open-access PDFs from link.springer.com. Direct page fetches from this session all redirected to the Springer login, so no paywalled text was read. Access status is OpenAlex's `is_oa` flag as of 2026-11-20.

| # | Title | Access | What I actually read |
|---|---|---|---|
| 1 | Efficiency and environmental performance evaluation of the water industry: a dynamic four-stage network data envelopment analysis | PAYWALLED (closed) | nothing (no abstract in public metadata) |
| 2 | A multi-objective stochastic home health care routing and scheduling problem under demand and service time uncertainty | PAYWALLED (closed) | nothing (no abstract in public metadata) |
| 3 | Integrating internal and external attributes in clustering: a goal programming-data envelopment analysis model | PAYWALLED (PDF supplied) | abstract, introduction, GP-DEA model, case study, limitations, conclusion |
| 4 | Environmental and financial performance in the S&P 500: a novel mcdm approach | open access | abstract only (PDF downloaded, body not read) |
| 5 | Artificial intelligence for socially responsible investment: a multi-objective decision-making framework | open access | abstract + intro, literature review, methodology (first ~400 lines) read |
| 6 | Equity-oriented design of vaccine supply chains under pandemic conditions through bi-level fuzzy goal programming | PAYWALLED (PDF supplied) | abstract, objectives, gap statement, methodology, conclusion/limitations (key sections, not every table or proof) |
| 7 | A hybrid fuzzy MCDM framework for enhancing urban recycling in Chilean regions | open access | abstract only (PDF downloaded, body not read) |
| 8 | Not just hype: a multi-criteria decision framework for ranking generative AI strategies in sustainable tourism | PAYWALLED (PDF supplied) | abstract, objectives, gap statement, methodology, conclusion/limitations (key sections, not every table or proof) |
| 9 | A novel max–min BWM method to boost the digital transformation of resilience supply chains | open access | abstract only (PDF downloaded, body not read) |
| 10 | Existence and multiplicity of solutions for discrete variable-order fractional boundary value problems with nonlocal constraints | PAYWALLED (closed) | nothing (no abstract in public metadata) |
| 11 | A range-adjusted robust DEA model for evaluating multi-efficiencies in retail chain stores | PAYWALLED (closed) | nothing (no abstract in public metadata) |
| 12 | Human-centric optimization of multi-row facility layouts: an NSGA-II-based approach balancing noise exposure and space utilization | PAYWALLED (closed) | nothing (no abstract in public metadata) |
| 13 | Location and allocation of primary and backup shelters in transboundary disasters | open access | abstract only (PDF downloaded, body not read) |
| 14 | Constraint qualifications and optimality criteria for robust conic multiobjective semi-infinite programming problems with vanishing constraints on Riemannian manifolds | PAYWALLED (closed) | nothing (no abstract in public metadata) |
| 15 | Inertial proximal point algorithm on Hadamard manifolds: convergence analysis and finite termination | PAYWALLED (closed) | nothing (no abstract in public metadata) |
| 16 | Intelligent multi-objective decision support system for efficient resource allocation in cloud computing | PAYWALLED (PDF supplied) | abstract, objectives, gap statement, methodology, conclusion/limitations (key sections, not every table or proof) |
| 17 | A decision framework for supplier selection and order allocation for environmentally-sustainable perishable food supply chains | PAYWALLED (closed) | nothing (no abstract in public metadata) |
| 18 | Exploiting experts’ asymmetric knowledge structures for consensus reaching: a multi-criteria group decision making model with three-way conflict analysis and opinion dynamics | PAYWALLED (closed) | nothing (no abstract in public metadata) |
| 19 | Scheduling technicians and tasks through an adaptive multi-objective biased random-key genetic algorithm | PAYWALLED (closed) | nothing (no abstract in public metadata) |

## Findings so far (5 papers only)
- Paper 5 (Truyols-Pont et al.) is the closest to my idea: machine-learning forecasts (LSTM, random forest, GRU, ARIMA, ANN) feed a Black-Litterman model with CVaR and ESG criteria, framed as multi-objective programming, applied to the water-sector stock market. It is finance, not goal programming, and it does not examine how forecast error affects the optimiser's output. Its literature review cites end-to-end Black-Litterman work (Duraj and Yu, 2023) that trains view generation jointly with allocation, so 'predict then optimise' is already present in portfolio work.
- Papers 4, 7, 9 are MCDM weighting/ranking methods (TOPSIS/VIKOR/COPRAS, fuzzy weights, max-min BWM). Paper 13 is a stochastic bi-objective shelter location model. Abstracts only.
- The other 14 papers, including both with goal programming in the title (3, 6), are unread.

## Findings from the four PDFs supplied by the user (3, 6, 8, 16)
- **3, Omrani (GP-DEA clustering):** lexicographic goal programming finds common DEA weights per cluster. GP is a weight-finding device. Real data: 288 Iranian hospitals (2016) plus literature examples. No learned coefficients. Future work lists robust/stochastic DEA and integration with machine-learning clustering.
- **6, Hosseini-Motlagh et al. (vaccine supply chain):** bi-level model solved with fuzzy goal programming. Demand and costs are triangular fuzzy numbers from expert judgement (fuzzy chance-constrained programming, credibility measure). Case: Arak, Iran. No data-driven estimation. Future work lists real-time data and hybrid stochastic-fuzzy models.
- **16, Qi et al. (cloud resource allocation):** modified feeding-birds metaheuristic with Q-learning, evaluated in CloudSim against HBCA, MOPSO, TPOSIS. 'Multi-objective' means makespan, energy and utilisation; there is no goal-programming formulation and no coefficient uncertainty.
- **8, Zeqiri and Ben Youssef (generative AI in tourism):** 35 interviews on the French Riviera, AHP weights, TOPSIS/PROMETHEE II/ELECTRE III ranking. AI is the subject of the decision, not a tool inside the model. Future work lists stochastic or fuzzy preferences.

## What this does and does not support
- In the nine papers I could read (four in key sections, paper 5 in part, four at abstract level), none learns the coefficients of a goal-programming model from data and then studies how prediction error affects the allocation. Paper 5 (finance, Black-Litterman) is the nearest and is not goal programming.
- This is a statement about nine papers of one special-issue collection, not about the literature. Novelty also has to be checked outside the collection (decision-focused learning, goal programming with estimated parameters, robust goal programming). I have not done that search.
- Still unread and possibly relevant by title: 2 (stochastic multi-objective routing), 12 (NSGA-II layout), 17, 18, 19. Papers 1, 10, 11, 14, 15 are unlikely to bear on this topic, but I have not read them.

## Not yet supported
The gap claim is supported for the nine papers listed above and unverified for the other ten.

## Papers I need from you (paywalled)
1, 2, 3, 6, 8, 10, 11, 12, 14, 15, 16, 17, 18, 19. Papers 3, 6, 8, 16 have now been supplied and read. Most useful next: 2, 12, 17, 18, 19.
