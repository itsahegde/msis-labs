# EDA: A Practical Workflow

Treat EDA as a repeatable loop: **question → inspect → clean → visualize → hypothesize → document**. Below is the workflow to follow on any tabular dataset, with code.

## 0. Setup and framing

Before touching the data, write down the **goal** (e.g., "predict churn") and the **target variable**. This determines what you look for, such as leakage, class imbalance, and which features matter.

```python
import pandas as pd, numpy as np
import matplotlib.pyplot as plt, seaborn as sns
from scipy import stats

df = pd.read_csv("data.csv")
```

## 1. First look: structure

```python
df.shape
df.head()
df.info()                      # dtypes, non-null counts
df.describe(include="all").T   # summary stats
df.nunique().sort_values()     # spot IDs, constants, low-cardinality columns
```

**What to look for:** wrong dtypes (dates stored as strings, numbers stored as objects), ID columns (drop them from analysis), constant columns, and suspicious min/max values (age = -1, 999).

## 2. Data quality

```python
# Missing values
miss = df.isna().mean().sort_values(ascending=False)
print(miss[miss > 0])
sns.heatmap(df.isna(), cbar=False)   # shows missingness patterns

# Duplicates
df.duplicated().sum()

# Inconsistent categories ("Male", "male ", "M")
for c in df.select_dtypes("object"):
    print(c, df[c].unique()[:20])
```

**Think about *why* data is missing**: MCAR, MAR, or MNAR. Missingness itself can be a signal (e.g., `df["income_missing"] = df["income"].isna()`), so check whether it correlates with the target.

## 3. Univariate analysis

```python
num_cols = df.select_dtypes("number").columns
cat_cols = df.select_dtypes(["object", "category"]).columns

# Numeric: distribution shape
for c in num_cols:
    fig, ax = plt.subplots(1, 2, figsize=(10, 3))
    sns.histplot(df[c], kde=True, ax=ax[0])
    sns.boxplot(x=df[c], ax=ax[1])
    plt.title(f"{c} | skew={df[c].skew():.2f}")
    plt.show()

# Categorical: frequency
for c in cat_cols:
    print(df[c].value_counts(normalize=True).head(10))
```

**What to look for:**
- **Skewness** (|skew| > 1 → consider log/Box-Cox transform)
- **Rare categories** (candidates for grouping into "Other")
- **Multimodal distributions** (may indicate hidden subgroups)

## 4. Outlier detection

```python
def iqr_outliers(s):
    q1, q3 = s.quantile([.25, .75])
    iqr = q3 - q1
    return ((s < q1 - 1.5*iqr) | (s > q3 + 1.5*iqr)).sum()

{c: iqr_outliers(df[c]) for c in num_cols}
```

The important judgment call is whether each outlier is an **error** (fix or remove), a **rare but real value** (keep, maybe transform), or **the thing you're trying to detect** (e.g., fraud). Don't delete outliers automatically.

## 5. Target analysis

```python
# Classification
df["target"].value_counts(normalize=True).plot(kind="bar")   # class imbalance?

# Regression
sns.histplot(df["target"], kde=True)    # skewed? try np.log1p(target)
```

## 6. Bivariate analysis (feature vs. target)

```python
# Numeric feature vs. categorical target
sns.boxplot(x="target", y="feature", data=df)

# Categorical feature vs. categorical target
pd.crosstab(df["cat_feature"], df["target"], normalize="index").plot(kind="bar", stacked=True)

# Numeric feature vs. numeric target
sns.scatterplot(x="feature", y="target", data=df)

# Statistical tests
stats.chi2_contingency(pd.crosstab(df["cat_feature"], df["target"]))   # cat vs cat
stats.f_oneway(*[g["feature"] for _, g in df.groupby("target")])        # num vs cat
```

## 7. Multivariate analysis

```python
# Correlation (Spearman is more robust to non-linearity and outliers)
corr = df[num_cols].corr(method="spearman")
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0)

# Multicollinearity
from statsmodels.stats.outliers_influence import variance_inflation_factor
X = df[num_cols].dropna()
pd.Series([variance_inflation_factor(X.values, i) for i in range(X.shape[1])], index=X.columns)
# VIF > 5-10 → problematic for linear models

# Pairwise relationships, colored by target
sns.pairplot(df, vars=list(num_cols[:5]), hue="target")
```

## 8. Leakage and feature ideas

- **Leakage check:** is any feature suspiciously correlated with the target (|r| > 0.9)? Does it use information that wouldn't be available at prediction time?
- **Feature engineering ideas:** ratios, date parts (month, day-of-week), binning, interaction terms, and missingness flags.

## 9. Document your findings

End each EDA with a short written summary: key patterns, data issues found, decisions made (e.g., "log-transformed `income` due to skew of 3.2"), and a list of preprocessing steps for modeling. This habit matters for coursework and for real projects.

## Common mistakes to avoid

1. **Computing statistics on the full dataset before the train/test split.** Imputation values, scaling parameters, and encodings should come from training data only.
2. **Treating correlation as causation**, or only checking linear correlation.
3. **Skipping domain context.** Always ask "does this value make sense in the real world?"
4. **Over-relying on auto-EDA tools** (`ydata-profiling`, `sweetviz`). They're great for a quick overview, but do the manual workflow first so you understand what they're showing.

## Suggested practice path

| Dataset | Why it's good |
|---|---|
| **Titanic** | Classic; missing values, mixed types, categorical features |
| **House Prices (Kaggle)** | Skewed target, many features, outliers, multicollinearity |
| **Telco Customer Churn** | Class imbalance, dtype problems, business framing |

For each one, aim to produce a notebook following steps 1-9 and write your conclusions in markdown cells. As you progress, add time-series EDA (trend, seasonality, autocorrelation) and, since you're in Big Data Analytics, practice the same workflow in **PySpark** for datasets that don't fit in memory.