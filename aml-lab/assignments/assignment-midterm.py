import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_diabetes, load_iris, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, silhouette_score, adjusted_rand_score,
    pairwise_distances
)
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import linkage, dendrogram

results = []


def save_regression_result(name, y_true, y_pred):
    results.append({
        "Task": "Regression",
        "Model": name,
        "R2": r2_score(y_true, y_pred),
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred))
    })


def save_classification_result(name, y_true, y_pred):
    results.append({
        "Task": "Classification",
        "Model": name,
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, average="weighted", zero_division=0),
        "Recall": recall_score(y_true, y_pred, average="weighted", zero_division=0),
        "F1": f1_score(y_true, y_pred, average="weighted", zero_division=0)
    })
    print(f"\n{name} confusion matrix:")
    print(confusion_matrix(y_true, y_pred))


def impurity(labels, criterion):
    _, counts = np.unique(labels, return_counts=True)
    probabilities = counts / counts.sum()
    if criterion == "entropy":
        return -np.sum(probabilities * np.log2(probabilities + 1e-12))
    return 1 - np.sum(probabilities ** 2)


def best_split(X, y, feature_names, criterion):
    best_gain = -1
    best_feature = None
    best_threshold = None
    parent_impurity = impurity(y, criterion)

    for j in range(X.shape[1]):
        values = np.unique(X[:, j])
        thresholds = (values[:-1] + values[1:]) / 2
        for threshold in thresholds:
            left = y[X[:, j] <= threshold]
            right = y[X[:, j] > threshold]
            if len(left) == 0 or len(right) == 0:
                continue
            child_impurity = (
                len(left) / len(y) * impurity(left, criterion)
                + len(right) / len(y) * impurity(right, criterion)
            )
            gain = parent_impurity - child_impurity
            if gain > best_gain:
                best_gain = gain
                best_feature = feature_names[j]
                best_threshold = threshold

    return best_feature, best_threshold, best_gain


# 1(a): Linear, Ridge and Lasso regression
print("\n1(a) Linear Regression, Ridge and Lasso")
diabetes = load_diabetes()
X_reg_train, X_reg_test, y_reg_train, y_reg_test = train_test_split(
    diabetes.data, diabetes.target, test_size=0.2, random_state=42
)

regression_models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
    "Lasso Regression": make_pipeline(StandardScaler(), Lasso(alpha=0.1, max_iter=10000))
}

for name, model in regression_models.items():
    model.fit(X_reg_train, y_reg_train)
    predictions = model.predict(X_reg_test)
    save_regression_result(name, y_reg_test, predictions)
    print(name, "R2:", round(r2_score(y_reg_test, predictions), 3))


# 1(b): Decision tree, entropy, information gain and Gini impurity
print("\n1(b) Decision Tree")
iris = load_iris()
X_tree_train, X_tree_test, y_tree_train, y_tree_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
)

feature, threshold, gain = best_split(iris.data, iris.target, iris.feature_names, "entropy")
print("Best entropy split:", feature, "threshold:", round(threshold, 3))
print("Information gain:", round(gain, 4))
feature_gini, threshold_gini, gain_gini = best_split(
    iris.data, iris.target, iris.feature_names, "gini"
)
print("Best Gini split:", feature_gini, "threshold:", round(threshold_gini, 3))
print("Gini impurity reduction:", round(gain_gini, 4))

tree_models = {
    "Decision Tree (Entropy)": DecisionTreeClassifier(criterion="entropy", max_depth=3, random_state=42),
    "Decision Tree (Gini)": DecisionTreeClassifier(criterion="gini", max_depth=3, random_state=42)
}

for name, model in tree_models.items():
    model.fit(X_tree_train, y_tree_train)
    predictions = model.predict(X_tree_test)
    save_classification_result(name, y_tree_test, predictions)

plt.figure(figsize=(12, 6))
plot_tree(
    tree_models["Decision Tree (Entropy)"],
    feature_names=iris.feature_names,
    class_names=iris.target_names,
    filled=True,
    rounded=True
)
plt.title("Decision Tree using Entropy")
plt.tight_layout()


# 1(c): Logistic regression, sigmoid, decision boundary, L2 and L1 regularization
print("\n1(c) Logistic Regression")
cancer = load_breast_cancer()
X_log_train, X_log_test, y_log_train, y_log_test = train_test_split(
    cancer.data, cancer.target, test_size=0.2, random_state=42, stratify=cancer.target
)

logistic_models = {
    "Logistic Regression (Ridge/L2)": make_pipeline(
        StandardScaler(), LogisticRegression(penalty="l2", solver="liblinear", max_iter=5000)
    ),
    "Logistic Regression (Lasso/L1)": make_pipeline(
        StandardScaler(), LogisticRegression(penalty="l1", solver="liblinear", max_iter=5000)
    )
}

for name, model in logistic_models.items():
    model.fit(X_log_train, y_log_train)
    predictions = model.predict(X_log_test)
    save_classification_result(name, y_log_test, predictions)


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


logistic_l2 = logistic_models["Logistic Regression (Ridge/L2)"]
logits = logistic_l2.decision_function(X_log_test[:5])
print("Sigmoid of first five decision scores:", np.round(sigmoid(logits), 3))
print("Predicted probabilities:", np.round(logistic_l2.predict_proba(X_log_test[:5])[:, 1], 3))

X_boundary = cancer.data[:, :2]
X_boundary_train, X_boundary_test, y_boundary_train, y_boundary_test = train_test_split(
    X_boundary, cancer.target, test_size=0.2, random_state=42, stratify=cancer.target
)
boundary_model = make_pipeline(StandardScaler(), LogisticRegression(solver="liblinear"))
boundary_model.fit(X_boundary_train, y_boundary_train)
xx, yy = np.meshgrid(
    np.linspace(X_boundary[:, 0].min() - 1, X_boundary[:, 0].max() + 1, 250),
    np.linspace(X_boundary[:, 1].min() - 1, X_boundary[:, 1].max() + 1, 250)
)
mesh = np.c_[xx.ravel(), yy.ravel()]
probs = boundary_model.predict_proba(mesh)[:, 1].reshape(xx.shape)
plt.figure(figsize=(8, 5))
plt.contourf(xx, yy, probs, levels=[0, 0.5, 1], alpha=0.25)
plt.contour(xx, yy, probs, levels=[0.5], linewidths=2)
plt.scatter(X_boundary_test[:, 0], X_boundary_test[:, 1], c=y_boundary_test, edgecolors="black", s=25)
plt.xlabel("Mean radius")
plt.ylabel("Mean texture")
plt.title("Logistic Regression Decision Boundary")
plt.tight_layout()


# 1(d): K-nearest neighbors
print("\n1(d) K-Nearest Neighbors")
knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
knn.fit(X_tree_train, y_tree_train)
knn_predictions = knn.predict(X_tree_test)
save_classification_result("KNN (k=5)", y_tree_test, knn_predictions)


# 1(e): Naive Bayes
print("\n1(e) Naive Bayes")
naive_bayes = GaussianNB()
naive_bayes.fit(X_tree_train, y_tree_train)
nb_predictions = naive_bayes.predict(X_tree_test)
save_classification_result("Gaussian Naive Bayes", y_tree_test, nb_predictions)


# 2(a): Distances, similarities, K-Means and hierarchical clustering
print("\n2(a) Distances and Clustering")
X_iris_scaled = StandardScaler().fit_transform(iris.data)
print("Euclidean distance matrix for first five Iris rows:")
print(np.round(pairwise_distances(X_iris_scaled[:5], metric="euclidean"), 2))
print("Cosine similarity matrix for first five Iris rows:")
print(np.round(cosine_similarity(X_iris_scaled[:5]), 2))

kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
kmeans_labels = kmeans.fit_predict(X_iris_scaled)

hierarchical = AgglomerativeClustering(n_clusters=3, linkage="ward")
hierarchical_labels = hierarchical.fit_predict(X_iris_scaled)

for name, labels in [("K-Means", kmeans_labels), ("Hierarchical Clustering", hierarchical_labels)]:
    silhouette = silhouette_score(X_iris_scaled, labels)
    ari = adjusted_rand_score(iris.target, labels)
    results.append({"Task": "Clustering", "Model": name, "Silhouette": silhouette, "ARI": ari})
    print(name, "Silhouette:", round(silhouette, 3), "ARI:", round(ari, 3))

linkage_methods = ["single", "complete", "average", "ward"]
fig, axes = plt.subplots(2, 2, figsize=(14, 9))
for ax, method in zip(axes.ravel(), linkage_methods):
    linkage_matrix = linkage(X_iris_scaled, method=method)
    dendrogram(linkage_matrix, truncate_mode="lastp", p=15, show_leaf_counts=True, ax=ax)
    ax.set_title(f"Dendrogram: {method.title()} Linkage")
    ax.set_xlabel("Cluster or sample")
    ax.set_ylabel("Distance")
plt.tight_layout()


# 2(b): Bagging and boosting
print("\n2(b) Random Forest and Boosting")
ensemble_models = {
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42),
    "AdaBoost": AdaBoostClassifier(n_estimators=100, random_state=42)
}

for name, model in ensemble_models.items():
    model.fit(X_log_train, y_log_train)
    predictions = model.predict(X_log_test)
    save_classification_result(name, y_log_test, predictions)


# 2(c): Gaussian Mixture Model
print("\n2(c) Gaussian Mixture Model")
gmm = GaussianMixture(n_components=3, random_state=42)
gmm_labels = gmm.fit_predict(X_iris_scaled)
gmm_silhouette = silhouette_score(X_iris_scaled, gmm_labels)
gmm_ari = adjusted_rand_score(iris.target, gmm_labels)
results.append({"Task": "Clustering", "Model": "Gaussian Mixture Model", "Silhouette": gmm_silhouette, "ARI": gmm_ari})
print("GMM Silhouette:", round(gmm_silhouette, 3), "ARI:", round(gmm_ari, 3))


# 2(d): Principal Component Analysis
print("\n2(d) Principal Component Analysis")
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_iris_scaled)
print("Explained variance ratio:", np.round(pca.explained_variance_ratio_, 3))
print("Total variance explained by two components:", round(pca.explained_variance_ratio_.sum(), 3))

plt.figure(figsize=(8, 5))
for class_id, class_name in enumerate(iris.target_names):
    plt.scatter(
        X_pca[iris.target == class_id, 0],
        X_pca[iris.target == class_id, 1],
        label=class_name,
        s=35
    )
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("PCA of Iris Dataset")
plt.legend()
plt.tight_layout()


# 3: Model performance comparison
print("\n3. Model Performance Comparison")
comparison = pd.DataFrame(results)
print(comparison.round(3).to_string(index=False))

plt.show()
