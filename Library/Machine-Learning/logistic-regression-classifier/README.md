# Logistic Regression: Binary & Multi-Class Classifier

## 1. Overview

**Logistic Regression** is a fundamental supervised learning algorithm used for classification tasks. Despite its name, it's a classification algorithm, not a regression one. It estimates the probability that a given input belongs to a particular class using the **sigmoid (logistic) function**.

In production systems, Logistic Regression is crucial for **Spam Detection**, **Customer Churn Prediction**, **Fraud Detection**, and **Medical Diagnosis**. Its interpretability and efficiency make it a go-to algorithm for binary classification problems.

This module provides a from-scratch implementation using **NumPy**, demonstrating how to build a production-grade classifier with gradient descent optimization and regularization techniques.

---

## 2. Key Engineering Features

* **Gradient Descent Optimization:** Uses iterative parameter updates to minimize the binary cross-entropy loss function.
* **Sigmoid Activation:** Maps linear predictions to probabilities between 0 and 1.
* **Regularization Support:** Implements both L1 (Lasso) and L2 (Ridge) regularization to prevent overfitting.
* **Probability Estimates:** Provides both class predictions and probability scores for confidence-based decision making.
* **Loss Tracking:** Monitors training progress through loss history for convergence analysis.

---

## 3. Folder Architecture

```text
.
├── core/                           # Optimized Python implementation
│   └── logistic_regression.py      # The core classification logic
├── docs/                           # Technical Deep-Dives
│   ├── logic.md                    # Mathematical foundation and algorithm walkthrough
│   └── complexity.md               # Big O analysis and performance metrics
├── test-project/                   # Customer Churn Prediction Simulator
│   ├── app.py                      # Interactive Classification CLI
│   ├── customer_data.csv           # Sample dataset for testing
│   └── instructions.md             # User guide for the simulation
└── README.md                       # Module Entry Point (Current File)
```

---

## 4. Performance Metrics

| Metric | Complexity | Description |
| --- | --- | --- |
| **Training Time** | O(n × d × i) | n=samples, d=features, i=iterations |
| **Prediction Time** | O(n × d) | Linear time for inference |
| **Space Complexity** | O(d) | Efficient memory footprint |
| **Convergence** | Gradient-based | Stops when loss stabilizes or max iterations reached |

---

## 5. Quick Start

### Basic Implementation

```python
import numpy as np
from core.logistic_regression import LogisticRegression

# Sample data: [Feature1, Feature2]
X_train = np.array([[1, 2], [2, 3], [3, 1], [6, 5], [7, 7], [8, 6]])
y_train = np.array([0, 0, 0, 1, 1, 1])  # Binary labels

# Create and train the classifier
clf = LogisticRegression(learning_rate=0.1, n_iterations=1000)
clf.fit(X_train, y_train)

# Make predictions
X_test = np.array([[2, 2], [7, 6]])
predictions = clf.predict(X_test)
probabilities = clf.predict_proba(X_test)

print(f"Predictions: {predictions}")  # Output: [0, 1]
print(f"Probabilities: {probabilities}")  # Output: [0.12, 0.89] (example)
```

### 🎮 Run the Interactive Simulation

1. Ensure you have **NumPy** installed: `pip install numpy`
2. Navigate to the test directory:
```bash
cd test-project
```

3. Run the application:
```bash
python app.py
```

---

## 6. Real-World Use Cases

* **Spam Detection:** Classify emails as spam or not spam based on content features.
* **Credit Scoring:** Predict loan default risk based on applicant information.
* **Medical Diagnosis:** Classify patients as having a disease or not based on symptoms.
* **Customer Churn:** Predict whether a customer will leave a service.
* **Click-Through Rate (CTR) Prediction:** Estimate the probability a user will click on an ad.
* **Fraud Detection:** Identify fraudulent transactions in real-time payment systems.

---

## 7. Why Logistic Regression?

* **Interpretability:** Coefficients directly indicate feature importance and direction of influence.
* **Probabilistic Output:** Unlike hard classifiers, provides probability estimates for risk assessment.
* **Efficiency:** Fast training and prediction, suitable for real-time applications.
* **Foundation:** Serves as the building block for neural networks (single neuron).
* **Industry Standard:** Widely used in production systems due to reliability and simplicity.

---

## 8. Advanced Features

* **Regularization:** L1 for feature selection, L2 for weight penalty
* **Custom Thresholds:** Adjust decision boundary for imbalanced datasets
* **Loss Monitoring:** Track convergence through training history
* **Gradient Clipping:** Numerical stability for extreme values
