# Multiple Objective Programming and Goal Programming

Material for a submission to the *Annals of Operations Research* special issue
"Multiple Objective Programming and Goal Programming: Artificial Intelligence for Decision Making in Economic and Social Sciences"
(deadline 30 June 2027; https://link.springer.com/collections/bffeaajcfi).

- `docs/01_plan_and_outline.md` plan and outline
- `docs/02_collection_scan.md` scan of the collection's current papers
- `paper/` LaTeX manuscript (`main.tex`, build with pdflatex and bibtex)
- `code/gp_ml.py` simulation; `code/make_report.py` tables and figure
- `results/results.json` raw simulation output

Reproduce: `pip install numpy scipy scikit-learn matplotlib`, then `python code/gp_ml.py` (about 2 minutes) and `python code/make_report.py`.
