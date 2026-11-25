"""Lag-1 autocorrelation of annual ODA/GNI changes per donor (persistence check for the permutation test)."""
import sys; sys.path.insert(0, "code")
import numpy as np, pandas as pd, aid_profile as A
rows = [(k, len(g), np.corrcoef(g.delta.values[:-1], g.delta.values[1:])[0, 1]) for k, g in A.data().items()]
pd.DataFrame(rows, columns=["donor", "n", "acf1"]).round(3).to_csv("results/aid_autocorr.csv", index=False)
