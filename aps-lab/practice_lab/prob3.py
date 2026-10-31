import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import RocCurveDisplay, confusion_matrix, roc_curve, roc_auc_score
from sklearn.pipeline import make_pipeline

import matplotlib.pyplot as plt

data = load_breast_cancer()
x = data.data
y = (data.target == 0).astype(int)
print(f"Number of malignant tumors: {np.sum(y==1)}")
print(f"Number of benign tumors: {np.sum(y==0)}")

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=67)

model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=2500)
)

model.fit(x_train, y_train)

y_preds = model.predict(x_test)

cm = confusion_matrix(y_test, y_preds)
tp, fp, fn, tn = cm.ravel()

print("\nConfusion Matrix")
print("----------------")
print("                 Predicted benign   Predicted malignant")
print("Actual benign         ", tn, "                 ", fp)
print("Actual malignant      ", fn, "                 ", tp)

sensitivity = tp/(tp + fn)
print(f"\nRecall: {sensitivity:.2f}")

specificity = tn/(tn + fp)
print(f"\nSpecificity: {specificity:.2f}")

precision = tp/(tp + fp)
print(f"\nPrecision: {precision:.2f}")

print("\nEvaluation Metrics")
print("------------------")
print("Sensitivity:", round(sensitivity, 4))
print("Specificity:", round(specificity, 4))
print("Precision:", round(precision, 4))

y_probs = model.predict_proba(x_test)[:, 1]

fpr, tpr, thresholds = roc_curve(y_test, y_probs)

auc_score = roc_auc_score(y_test, y_probs)
print(f"\nAUC Score: {auc_score:.4f}")

plt.figure(figsize=(8, 6))

plt.plot(fpr, tpr)
plt.show()