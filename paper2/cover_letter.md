Dear Guest Editors,

Please consider the enclosed manuscript, "Revealed Aspiration Levels: Inverse Interval Goal Programming for Recovering the Targets and Priorities Behind Public Decisions", for the Annals of Operations Research special issue "Multiple Objective Programming and Goal Programming: Artificial Intelligence for Decision Making in Economic and Social Sciences". The manuscript is original, has not been published, and is not under consideration elsewhere.

**Contribution to multiple objective programming and goal programming.** Goal programming normally starts from aspiration levels and priorities supplied by a decision maker. The manuscript studies the inverse problem: recovering aspiration levels, tolerance bands and deviation weights of an interval goal program from a sequence of observed decisions. We prove that optimal decisions lie at breakpoints, that only effective weights are identifiable, that aspiration levels are revealed exactly when a decision stops at a band edge, and that the type of adjustment cost determines what can be learned: with a linear cost the weights are only set-identified, while with a quadratic cost (gradual adjustment) weights and aspiration levels are both point-identified. A change of variables makes all optimality conditions linear in the unknowns, which yields an exact mixed-integer linear estimator.

**Contribution to artificial intelligence for decision making.** The method learns a goal program from data. We give a scalable learning algorithm that combines parallel multistart local search on the decision loss with exact linear-programming and large-neighbourhood polishing, document its accuracy on synthetic data with known parameters, and quantify uncertainty by block bootstrap. Placebo experiments show when the fit diagnostics alone would mislead, and a permutation test with checked size guards against reading targets into behaviour that has none.

**Contribution to economic and social sciences.** Public actors announce targets; their decisions reveal what they pursue. We validate the method on central banks, whose targets are public, with a test whose sample, specification and success criterion were fixed and recorded before estimation: where inflation had deviated from target, the revealed target was closer to the announced one than average inflation in every case. We then estimate revealed aid targets for 23 donor countries; a calibrated permutation test finds goal-seeking for 14 of them at the 10% level, and among these the revealed targets range from about 0.2% to about 1% of gross national income against a common commitment of 0.7%, and the shift in the spending behaviour of NATO allies after 2022. We report where the method is less reliable (outcomes already at target; corporate leverage with a single goal).

All data are public (BIS, OECD, Eurostat, NATO, SEC EDGAR), and the code that reproduces every table is available at https://github.com/vinhqdang/Multiple-Objective-Programming-and-Goal-Programming.

Sincerely,

Quang-Vinh Dang
British University Vietnam, Hung Yen, Vietnam
vinh.dq4@buv.edu.vn
