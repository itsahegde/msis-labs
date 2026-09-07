import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.pipeline import make_pipeline
from sklearn.datasets import load_breast_cancer

data = load_breast_cancer()
x = data.data
y = data.target
x = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series((data.target==0).astype(int), name="malignant")

class_counts = y.value_counts().sort_index()
class_distribution = pd.DataFrame({"Class": data.target_names, "Count": class_counts.values, "Probability": class_counts.values/len(y)})
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)


pipeline = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
pipeline.fit(x_train, y_train)
y_pred = pipeline.predict(x_test)
y_probs = pipeline.predict_proba(x_test)[:, 1]

thresholds = np.arange(0.1, 1.0, 0.1)

metrics_data = []

for t in thresholds:

    y_pred = (y_probs >= t).astype(int)
    
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    metrics_data.append({
        'Threshold': round(t, 2),
        'Accuracy': round(acc, 4),
        'Precision': round(prec, 4),
        'Recall': round(rec, 4),
        'F1-Score': round(f1, 4),
        'TP': tp,
        'TN': tn,
        'FP': fp,
        'FN': fn
    })

threshold_df = pd.DataFrame(metrics_data)
print(threshold_df)