# K-Nearest Neighbors (KNN) Classifier

## 1. Overview

The **K-Nearest Neighbors (KNN)** algorithm is an instance-based, non-parametric classifier that makes predictions by finding the K training samples closest to a query point and voting on the class. Unlike Decision Trees or Logistic Regression, KNN has **no training phase** — it memorizes the entire dataset and performs all computation at prediction time.

KNN is the foundational algorithm behind **recommendation engines**, **similarity search**, and **vector retrieval** in the age of LLMs and RAG (Retrieval-Augmented Generation). It powers the "Users who liked X also liked Y" logic in **Netflix**, **Spotify**, and **Amazon**.

---

## 2. Technical Features

- **Zero Training Time:** No model is built — the algorithm simply stores the dataset and computes distances at query time ("lazy learning").
- **Multiple Distance Metrics:** Supports Euclidean, Manhattan, and Minkowski distance functions for flexible similarity measurement.
- **Weighted Voting:** Supports both uniform voting (all neighbors equal) and distance-weighted voting (closer neighbors count more).
- **Built-in Normalization:** Includes Min-Max feature scaling to prevent features with large ranges from dominating the distance calculation.
- **Probability Estimates:** Returns class probability distributions based on neighbor vote proportions.
- **Pure Python:** No external dependencies — only standard library modules.

---

## 3. Architecture

```text
.
├── core/                  # Classification Engine
│   ├── __init__.py        # Package initialization
│   └── knn.py             # Distance metrics, neighbor search & voting logic
├── docs/                  # Technical Documentation
│   ├── logic.md           # Lazy learning, distance geometry & the curse of dimensionality
│   └── complexity.md      # Analysis of O(n·d) prediction cost & space trade-offs
├── test-project/          # The Movie Recommendation Engine
│   ├── app.py             # Predict movie preferences from viewing history
│   └── instructions.md    # Guide for exploring the recommendation output
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric                  | Specification                                     |
| ----------------------- | ------------------------------------------------- |
| **Training Time**       | O(1) — no training, just storage                  |
| **Prediction Time**     | O(n * d) per query (n=samples, d=features)        |
| **Space Complexity**    | O(n * d) — stores entire training set             |
| **Optimal K Range**     | Typically sqrt(n), always odd for binary tasks     |
| **Best Dimensionality** | d < 20 (degrades with high dimensions)            |

---

## 5. Deployment & Usage

### Integration

KNN is ideal for recommendation systems, anomaly detection, and similarity-based classification:

```python
from core.knn import KNNClassifier, accuracy_score

# Training data: [feature1, feature2] -> class
X_train = [
    [5.1, 3.5], [4.9, 3.0], [4.7, 3.2],  # Class 0
    [7.0, 3.2], [6.4, 3.2], [6.9, 3.1],  # Class 1
]
y_train = [0, 0, 0, 1, 1, 1]

# Create classifier
clf = KNNClassifier(k=3, metric='euclidean', weights='distance')
clf.fit(X_train, y_train)

# Predict
predictions = clf.predict([[5.0, 3.4], [6.7, 3.1]])
print(f"Predictions: {predictions}")  # [0, 1]

# Get probability estimates
probas = clf.predict_proba([[5.5, 3.0]])
print(f"Probabilities: {probas}")  # [{0: 0.67, 1: 0.33}]

# Evaluate
acc = accuracy_score([0, 1], predictions)
print(f"Accuracy: {acc:.2%}")  # 100.00%
```

### Running the Simulator

To see the Movie Recommendation Engine in action:

1. Navigate to the `test-project` directory:

```bash
cd test-project

```

2. Run the simulation:

```bash
python app.py

```

---

## 6. API Reference

### KNNClassifier

```python
KNNClassifier(
    k=5,                  # Number of neighbors to consider
    metric='euclidean',   # Distance metric: 'euclidean', 'manhattan', 'minkowski'
    weights='uniform',    # Voting weights: 'uniform' or 'distance'
    p=2,                  # Minkowski power parameter (p=2 is Euclidean)
    normalize=False       # Whether to apply Min-Max normalization
)
```

#### Methods

| Method | Description | Returns |
| --- | --- | --- |
| `fit(X, y)` | Store training data | self |
| `predict(X)` | Predict class labels | List of labels |
| `predict_proba(X)` | Predict class probabilities | List of dicts |
| `get_neighbors(sample, k)` | Find k nearest neighbors | List of (distance, index) |

### Helper Functions

| Function | Description |
| --- | --- |
| `accuracy_score(y_true, y_pred)` | Classification accuracy (0 to 1) |
| `train_test_split(X, y, test_ratio)` | Split data into train/test sets |
| `min_max_normalize(X)` | Scale features to [0, 1] range |

---

## 7. Industrial Applications

- **Recommendation Engines:** "Users who liked X also liked Y" in **Netflix**, **Spotify**, and **Amazon** product recommendations.
- **Vector Search & RAG:** Finding semantically similar document embeddings in **Pinecone**, **Weaviate**, and **ChromaDB** for LLM retrieval.
- **Anomaly Detection:** Identifying fraudulent transactions by finding samples far from their K nearest neighbors.
- **Medical Diagnosis:** Classifying diseases based on similarity to known patient profiles.
- **Image Recognition:** Classifying handwritten digits (MNIST) by pixel-value similarity.
- **Imputation:** Filling missing data by averaging values from the K nearest complete records.
