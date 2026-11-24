Dear Guest Editors,

Please consider the enclosed manuscript, "Revealed Aspiration Levels: Inverse Interval Goal Programming for Recovering the Targets and Priorities Behind Public Decisions", for the Annals of Operations Research special issue "Multiple Objective Programming and Goal Programming: Artificial Intelligence for Decision Making in Economic and Social Sciences". The manuscript is original, has not been published, and is not under consideration elsewhere.

**Contribution to multiple objective programming and goal programming.** Goal programming normally starts from aspiration levels and priorities supplied by a decision maker. The manuscript studies the inverse problem: recovering aspiration levels, tolerance bands and deviation weights of an interval goal program from a sequence of observed decisions. We prove that optimal decisions lie at breakpoints, that only effective weights are identifiable, that aspiration levels are revealed exactly when a decision stops at a band edge, and that the type of adjustment cost determines what can be learned: with a linear cost the weights are not point-identified, while with a quadratic cost (gradual adjustment) they are, under a rank condition. A change of variables makes all optimality conditions linear in the unknowns, which yields an exact mixed-integer linear estimator.

**Contribution to artificial intelligence for decision making.** The method learns a goal program from data. We give a scalable learning algorithm that combines parallel multistart local search on the decision loss with exact linear-programming and large-neighbourhood polishing, document its accuracy on synthetic data with known parameters, and quantify uncertainty by block bootstrap. Placebo experiments show when the fit diagnostics alone would mislead, and two calibrated tests, one of state dependence and one against partial adjustment, guard against reading targets into behaviour that has none.

**Contribution to economic and social sciences.** Public actors announce targets; their decisions reveal what they pursue. We check the method on central banks, whose targets are public: the implied targets have the right magnitude and are far closer than average inflation where the two diverged strongly, but over fourteen banks they are no closer than a constant 2.5%, and we say so. We then estimate revealed aid targets for 23 donor countries; among the donors whose decisions reject partial adjustment after multiplicity adjustment, revealed targets range from about 0.2% to about 1% of gross national income against a common commitment of 0.7%, with Sweden and Norway close to their national 1% goals. For NATO allies the revealed lower edge of spending rose to 3.2% of GDP after 2022, well outside its earlier uncertainty range. We report where the method is less reliable (outcomes already at target; a weakly determined pre-2022 defence edge; corporate leverage with a single goal).

All data are public (BIS, OECD, Eurostat, NATO, SEC EDGAR), and the code that reproduces every table is available at https://github.com/vinhqdang/Multiple-Objective-Programming-and-Goal-Programming.

Sincerely,

Quang-Vinh Dang
British University Vietnam, Hung Yen, Vietnam
vinh.dq4@buv.edu.vn
