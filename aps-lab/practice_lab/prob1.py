import pandas as pd
import numpy as np

np.random.seed(67)
n=10000

p_fraud = 0.08
p_flag_given_fraud = 0.85
p_flag_given_genuine = 0.10

fraud = np.random.randn(n) < p_fraud

flag = np.zeros(n, dtype=bool)

flag[fraud] = (np.random.rand(fraud.sum())) < p_flag_given_fraud
flag[~fraud] = np.random.rand((~fraud).sum()) < p_flag_given_genuine

df = pd.DataFrame({
    "true_fraud_status": fraud,
    "system_fraud_flag": flag
})

table = pd.crosstab( df['true_fraud_status'], df['system_fraud_flag'])
table.index = ['Genuine', 'Fraud']
table.columns = ['Not Flagged', 'Flagged']

TP = np.sum(fraud & flag)
FP = np.sum(~fraud & flag)
TN = np.sum(~fraud & ~flag)
FN = np.sum(fraud & ~flag)

p_flag_mean = np.mean(flag)

p_flag_given_fraud = TP/(TP+FN)
p_fraud_given_flag = TP/(TP+FP)

print(f"p(flag|fraud) = {p_flag_given_fraud:.4f}")
print(f"p(fraud|flag) = {p_fraud_given_flag:.4f}")

p_genuine = 1 - p_fraud

p_flag_theory = (
    p_flag_given_fraud * p_fraud + p_flag_given_genuine * p_genuine
)








