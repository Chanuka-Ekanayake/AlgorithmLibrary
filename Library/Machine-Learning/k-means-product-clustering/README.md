# K-Means Clustering: Automated Product Tiering

## 1. Overview

**K-Means Clustering** is a powerful unsupervised machine learning algorithm used to partition a dataset into  distinct, non-overlapping subgroups. In an e-commerce or SaaS environment, K-Means is essential for **Customer Segmentation**, **Anomaly Detection**, and **Automated Product Categorization**.

This module provides a from-scratch implementation of K-Means using **NumPy**, demonstrating how a marketplace for software and ML models can automatically group products into "Business Tiers" (e.g., Free, Pro, Enterprise) based on their technical specifications.

---

## 2. Key Engineering Features

* **Vectorized Math:** Leverages NumPy for high-speed Euclidean distance calculations, ensuring the algorithm can scale to large datasets.
* **Expectation-Maximization Logic:** Follows the iterative process of centroid assignment and mean-based updating until convergence.
* **Dynamic Tiering CLI:** An interactive test project that allows users to cluster models by "Logic Complexity" and "Compute Demand."
* **Predictive Capabilities:** Includes a prediction function to assign newly added products to existing clusters based on previously trained centroids.

---

## 3. Folder Architecture

```text
.
├── core/                  # Optimized Python implementation
│   └── kmeans.py          # The core clustering logic
├── docs/                  # Technical Deep-Dives
│   ├── logic.md           # The EM (Expectation-Maximization) process
│   └── complexity.md      # Mathematical Big O analysis
├── test-project/          # Business Tier Simulator
│   ├── app.py             # Interactive Clustering CLI
│   ├── model_data.csv     # Sample dataset for testing
│   └── instructions.md    # User guide for the simulation
└── README.md              # Module Entry Point (Current File)

```

---

## 4. Performance Metrics

| Metric | Complexity | Description |
| --- | --- | --- |
| **Time Complexity** |  | Linear scaling with respect to samples (). |
| **Space Complexity** |  | Efficient memory footprint for high-dimensional data. |
| **Convergence** | Tolerance-based | Stops automatically once centroids stabilize. |

---

## 5. Quick Start

### Basic Implementation

```python
import numpy as np
from core.kmeans import KMeans

# Sample data: [Complexity, Compute]
data = np.array([[1, 2], [1, 1], [9, 8], [8, 9]])

# Cluster into 2 groups
clf = KMeans(k=2)
clf.fit(data)

print(clf.labels) # Output: [0, 0, 1, 1] (Example)

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

* **Logistics:** Grouping delivery locations to optimize warehouse placement.
* **Cybersecurity:** Detecting unusual patterns in network traffic (outlier detection).
* **Search Optimization:** Clustering vector embeddings to speed up nearest-neighbor searches.
* **Marketing:** Segmenting users based on purchase behavior for targeted campaigns.