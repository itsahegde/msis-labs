import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_curve, auc
from sklearn.model_selection import train_test_split

# Step 1: Generate an imbalanced dataset
X, y = make_classification(
    n_samples=1000,
    n_features=20,
    n_informative=2,
    n_redundant=10,
    n_clusters_per_class=1,
    weights=[0.9, 0.1],  # 90% Class 0 (Majority), 10% Class 1 (Minority)
    flip_y=0,
    random_state=42,
)

# Step 2: Split data preserving class distribution
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Step 3: Train Logistic Regression with class weight handling
model = LogisticRegression(class_weight="balanced", random_state=42)
model.fit(X_train, y_train)

# Step 4: Get probability predictions for minority class (Class 1)
y_probs = model.predict_proba(X_test)[:, 1]
y_preds = model.predict(X_test)

# Step 5: Evaluate Precision-Recall Curve and Area Under Curve (PR-AUC)
precision, recall, thresholds = precision_recall_curve(y_test, y_probs)
pr_auc = auc(recall, precision)

# Plot Precision-Recall Curve
plt.figure(figsize=(6, 4))
plt.plot(recall, precision, label=f"PR Curve (PR-AUC = {pr_auc:.3f})")
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision-Recall Curve for Imbalanced Classification")
plt.legend()
plt.grid(True)
plt.show()

print("Confusion Matrix:\n", confusion_matrix(y_test, y_preds))
print("\nClassification Report:\n", classification_report(y_test, y_preds))