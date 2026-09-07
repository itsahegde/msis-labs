import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split


def get_data(test_size=0.2, random_state=42):

    raw_data = load_breast_cancer()

    X = pd.DataFrame(raw_data.data, columns=raw_data.feature_names)
    
    y = pd.Series((raw_data.target == 0).astype(int), name="malignant")

    class_counts = y.value_counts().sort_index()
    class_distribution = pd.DataFrame(
        {
            "Class": raw_data.target_names,
            "Count": class_counts.values,
            "Probability": class_counts.values / len(y),
        }
    )
    print("Class Distribution:\n", class_distribution, "\n")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    return X_train, X_test, y_train, y_test