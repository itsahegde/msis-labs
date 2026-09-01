from data import get_data
from evaluate import build_and_train_pipeline, evaluate_thresholds


def main():
 
    X_train, X_test, y_train, y_test = get_data()

    pipeline = build_and_train_pipeline(X_train, y_train)

    threshold_df = evaluate_thresholds(pipeline, X_test, y_test)

    print("Metrics across thresholds:")
    print(threshold_df)


if __name__ == "__main__":
    main()