import pandas as pd
import numpy as np

np.random.seed(67)

n = 12
p = 0.20
mins = 20000

x = np.random.binomial(n, p, size=mins)

