import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def build_and_train_pipeline(X_train, y_train, max_iter=1000):
    
    pipeline = make_pipeline(StandardScaler(), LogisticRegression(max_iter=max_iter))
    pipeline.fit(X_train, y_train)
    return pipeline


def evaluate_thresholds(pipeline, X_test, y_test, step=0.1):
   
    y_probs = pipeline.predict_proba(X_test)[:, 1]
    thresholds = np.arange(0.1, 1.0, step)

    metrics_data = []

    for t in thresholds:
        y_pred = (y_probs >= t).astype(int)

        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        metrics_data.append(
            {
                "Threshold": round(t, 2),
                "Accuracy": round(acc, 4),
                "Precision": round(prec, 4),
                "Recall": round(rec, 4),
                "F1-Score": round(f1, 4),
                "TP": tp,
                "TN": tn,
                "FP": fp,
                "FN": fn,
            }
        )

    return pd.DataFrame(metrics_data)