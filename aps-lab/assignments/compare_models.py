"""Compare a baseline and an improved classifier with paired inference.

Dataset: scikit-learn's Wisconsin Diagnostic Breast Cancer dataset.
Run: python compare_models.py [--bootstrap 10000] [--output results.json]

The script uses a single stratified, held-out test set for both models. The
bootstrap resamples paired test observations, and the one-sided exact McNemar
test counts which model is correct on discordant observations.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.stats import binomtest
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


SEED = 2026
TEST_SIZE = 0.20


def paired_bootstrap(
    correct_baseline: np.ndarray,
    correct_improved: np.ndarray,
    repetitions: int,
    rng: np.random.Generator,
) -> tuple[float, float, float]:
    """Percentile CI for the paired accuracy difference (improved - baseline)."""
    n = len(correct_baseline)
    differences = np.empty(repetitions, dtype=float)
    # Chunking keeps memory use predictable for large repetition counts.
    chunk_size = 1_000
    for start in range(0, repetitions, chunk_size):
        stop = min(start + chunk_size, repetitions)
        indices = rng.integers(0, n, size=(stop - start, n))
        differences[start:stop] = (
            correct_improved[indices].mean(axis=1)
            - correct_baseline[indices].mean(axis=1)
        )
    low, high = np.quantile(differences, [0.025, 0.975])
    observed = float(correct_improved.mean() - correct_baseline.mean())
    return observed, float(low), float(high)


def evaluate(bootstrap_repetitions: int = 10_000) -> dict[str, object]:
    data = load_breast_cancer()
    X = data.data
    # In this dataset 0 means malignant; make the clinically important class 1.
    y = (data.target == 0).astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=SEED,
        stratify=y,
    )

    baseline = make_pipeline(
        StandardScaler(), LogisticRegression(C=1.0, max_iter=2_000, random_state=SEED)
    )
    improved = HistGradientBoostingClassifier(
        max_iter=150,
        learning_rate=0.08,
        max_leaf_nodes=15,
        l2_regularization=1.0,
        random_state=SEED,
    )
    models = {"baseline_logistic_regression": baseline,
              "improved_hist_gradient_boosting": improved}

    predictions: dict[str, np.ndarray] = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions[name] = model.predict(X_test)

    baseline_pred = predictions["baseline_logistic_regression"]
    improved_pred = predictions["improved_hist_gradient_boosting"]
    baseline_correct = (baseline_pred == y_test).astype(np.int8)
    improved_correct = (improved_pred == y_test).astype(np.int8)

    observed, ci_low, ci_high = paired_bootstrap(
        baseline_correct,
        improved_correct,
        bootstrap_repetitions,
        np.random.default_rng(SEED + 1),
    )

    improved_only = int(np.sum((improved_pred == y_test) & (baseline_pred != y_test)))
    baseline_only = int(np.sum((baseline_pred == y_test) & (improved_pred != y_test)))
    discordant = improved_only + baseline_only
    # H1: the improved model is correct more often on discordant test cases.
    mcnemar_p = (
        float(binomtest(improved_only, discordant, p=0.5, alternative="greater").pvalue)
        if discordant
        else 1.0
    )

    model_metrics = {}
    for name, pred in predictions.items():
        model_metrics[name] = {
            "accuracy": float(accuracy_score(y_test, pred)),
            "malignant_precision": float(precision_score(y_test, pred, zero_division=0)),
            "malignant_recall": float(recall_score(y_test, pred, zero_division=0)),
        }

    return {
        "dataset": "Wisconsin Diagnostic Breast Cancer (scikit-learn bundled copy)",
        "dataset_reference": "https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic",
        "positive_class": "malignant",
        "seed": SEED,
        "test_fraction": TEST_SIZE,
        "train_size": int(len(y_train)),
        "test_size": int(len(y_test)),
        "bootstrap_repetitions": bootstrap_repetitions,
        "models": model_metrics,
        "paired_accuracy_difference_improved_minus_baseline": observed,
        "paired_bootstrap_95_percentile_ci": [ci_low, ci_high],
        "mcnemar_discordant_improved_only": improved_only,
        "mcnemar_discordant_baseline_only": baseline_only,
        "mcnemar_one_sided_exact_p_value": mcnemar_p,
        "alpha": 0.05,
        "decision": (
            "Evidence of higher accuracy for the improved model on this split."
            if mcnemar_p < 0.05 and ci_low > 0
            else "Insufficient evidence that the improved model has higher accuracy."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bootstrap", type=int, default=10_000,
                        help="number of paired bootstrap resamples (default: 10000)")
    parser.add_argument("--output", type=Path, help="optional path for machine-readable JSON")
    args = parser.parse_args()
    if args.bootstrap < 1:
        parser.error("--bootstrap must be at least 1")

    result = evaluate(args.bootstrap)
    rendered = json.dumps(result, indent=2)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
