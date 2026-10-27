

import numpy as np
import pandas as pd
from scipy.stats import ttest_rel
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

# ---------------------- Config ----------------------
RANDOM_STATE = 42
N_BOOT       = 5000
rng          = np.random.default_rng(RANDOM_STATE)

# ---------------------- Data ----------------------
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=RANDOM_STATE
)
n_test = len(y_test)

def bootstrap_ci(correct, n_boot=N_BOOT):
    means = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n_test, n_test)
        means[i] = correct[idx].mean()
    return np.percentile(means, [2.5, 97.5])

# ---------------------- 1. Baseline  ----------------------
clf_b = DecisionTreeClassifier(random_state=RANDOM_STATE)
clf_b.fit(X_train, y_train)
pred_b    = clf_b.predict(X_test)
prob_b    = clf_b.predict_proba(X_test)[:, 1]
correct_b = (pred_b == y_test).astype(int)
acc_b     = accuracy_score(y_test, pred_b)
ci_b      = bootstrap_ci(correct_b)

# ---------------------- 2. Improved  ----------------------
clf_i = RandomForestClassifier(n_estimators=500, random_state=RANDOM_STATE)
clf_i.fit(X_train, y_train)
pred_i    = clf_i.predict(X_test)
prob_i    = clf_i.predict_proba(X_test)[:, 1]
correct_i = (pred_i == y_test).astype(int)
acc_i     = accuracy_score(y_test, pred_i)
ci_i      = bootstrap_ci(correct_i)

# ---------------------- Difference, CI, simple paired test ----------------------
diff = acc_i - acc_b

diff_boot = np.empty(N_BOOT)
for i in range(N_BOOT):
    idx = rng.integers(0, n_test, n_test)
    diff_boot[i] = correct_i[idx].mean() - correct_b[idx].mean()
diff_ci = np.percentile(diff_boot, [2.5, 97.5])

t_stat, p_val = ttest_rel(correct_i, correct_b)

# ---------------------- Results DataFrame ----------------------
df = pd.DataFrame([
    {
        "Model":     "Baseline (Decision Tree)",
        "Accuracy":  round(acc_b, 4),
        "F1":        round(f1_score(y_test, pred_b), 4),
        "AUC":       round(roc_auc_score(y_test, prob_b), 4),
        "CI_Lower":  round(ci_b[0], 4),
        "CI_Upper":  round(ci_b[1], 4),
    },
    {
        "Model":     "Improved (Random Forest)",
        "Accuracy":  round(acc_i, 4),
        "F1":        round(f1_score(y_test, pred_i), 4),
        "AUC":       round(roc_auc_score(y_test, prob_i), 4),
        "CI_Lower":  round(ci_i[0], 4),
        "CI_Upper":  round(ci_i[1], 4),
    },
    {
        "Model":     "Difference (Improved - Baseline)",
        "Accuracy":  round(diff, 4),
        "F1":        None,
        "AUC":       None,
        "CI_Lower":  round(diff_ci[0], 4),
        "CI_Upper":  round(diff_ci[1], 4),
    },
])

print(df.to_string(index=False))
print(f"\nPaired t-test p-value: {p_val:.4f}")
print("Conclusion: "
      + ("Improvement is statistically significant."
         if (p_val < 0.05 and diff_ci[0] > 0)
         else "Difference is not statistically significant."))