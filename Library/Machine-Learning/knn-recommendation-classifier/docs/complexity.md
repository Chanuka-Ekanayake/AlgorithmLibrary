# Complexity Analysis: K-Nearest Neighbors (KNN)

KNN has a unique complexity profile: **zero training cost** but **expensive prediction**. This is the exact opposite of most classifiers, which spend time training a model so that predictions are fast.

## 1. Time Complexity

### 1.1 Training: O(1) — or O(n * d) with Normalization

KNN's "training" phase is simply storing the dataset:

| Operation | Without Normalization | With Normalization |
| --- | --- | --- |
| **Store data** | O(n * d) copy | O(n * d) copy |
| **Compute min/max** | N/A | O(n * d) |
| **Normalize features** | N/A | O(n * d) |
| **Total** | O(n * d) | O(n * d) |

Where n = number of training samples, d = number of features.

No model is learned. No parameters are optimized. The data is simply memorized.

### 1.2 Prediction: O(n * d) per Query

For each query point, KNN must:

| Step | Complexity | Description |
| --- | --- | --- |
| **Compute distances** | O(n * d) | Distance to each of n training points, each requiring d operations |
| **Sort/select K nearest** | O(n * log n) | Full sort, or O(n * log K) with a min-heap |
| **Vote on class** | O(K) | Count votes from K neighbors |
| **Total (single query)** | O(n * d + n * log K) | Dominated by distance computation |
| **Total (batch of m queries)** | O(m * n * d) | Linear in query count |

### 1.3 Distance Computation Breakdown

Each distance calculation costs O(d):

| Metric | Operations per Pair | Formula |
| --- | --- | --- |
| **Euclidean** | d multiplications + d additions + 1 sqrt | sqrt(sum((a_i - b_i)^2)) |
| **Manhattan** | d subtractions + d abs operations | sum(abs(a_i - b_i)) |
| **Minkowski** | d power operations + 1 root | (sum(abs(a_i - b_i)^p))^(1/p) |

Manhattan is slightly faster than Euclidean (avoids multiplication and square root), but the difference is negligible for typical feature counts.

---

## 2. Space Complexity

### 2.1 Storage Requirements

| Component | Space | Description |
| --- | --- | --- |
| **Training data (X)** | O(n * d) | Entire feature matrix must be kept in memory |
| **Training labels (y)** | O(n) | One label per training sample |
| **Normalization params** | O(d) | Min and max per feature (if normalization enabled) |
| **Total** | O(n * d) | Dominated by training data storage |

### 2.2 Prediction-Time Memory

| Component | Space | Description |
| --- | --- | --- |
| **Distance array** | O(n) | One distance value per training point |
| **Neighbor list** | O(K) | Top-K nearest neighbors |
| **Vote counts** | O(C) | One counter per class (C = number of classes) |
| **Total per query** | O(n) | Dominated by distance array |

### 2.3 Comparison with Model-Based Classifiers

| Classifier | Inference Memory | What's Stored |
| --- | --- | --- |
| **KNN** | O(n * d) | Entire training dataset |
| **Decision Tree** | O(nodes) | Tree structure only |
| **Logistic Regression** | O(d) | Weight vector only |
| **SVM** | O(sv * d) | Support vectors only |

KNN has the **highest memory footprint** at inference time because it must retain all training data. This is its primary scalability limitation.

---

## 3. Effect of K on Complexity

The value of K has minimal impact on time complexity but affects prediction quality:

| K Value | Selection Cost | Vote Cost | Accuracy Trend |
| --- | --- | --- | --- |
| K = 1 | O(n) single pass | O(1) | High variance, low bias |
| K = sqrt(n) | O(n * log K) | O(K) | Balanced |
| K = n | O(n) trivial | O(n) | High bias, low variance |

The distance computation (O(n * d)) always dominates, so K has negligible impact on total prediction time.

---

## 4. Optimization Techniques

### 4.1 KD-Tree: O(d * log n) Average Prediction

A space-partitioning tree that enables efficient nearest-neighbor search:

| Metric | Brute Force | KD-Tree |
| --- | --- | --- |
| **Build time** | O(1) | O(n * d * log n) |
| **Query time** | O(n * d) | O(d * log n) average |
| **Space** | O(n * d) | O(n * d) |
| **Best for** | d > 20 or small n | d < 20 |

**Limitation:** KD-Trees degrade to O(n * d) when d > 20 due to the curse of dimensionality.

### 4.2 Ball Tree: O(d * log n) for Higher Dimensions

Better than KD-Tree for moderate dimensionality:

| Metric | KD-Tree | Ball Tree |
| --- | --- | --- |
| **Effective range** | d < 20 | d < 100 |
| **Build time** | O(n * d * log n) | O(n * d * log n) |
| **Query time** | O(d * log n) | O(d * log n) |

### 4.3 Locality-Sensitive Hashing (LSH): O(1) Approximate

For very high dimensions (d > 100), exact KNN becomes impractical. LSH provides **approximate** nearest neighbors in near-constant time:

| Metric | Exact KNN | LSH (Approximate) |
| --- | --- | --- |
| **Query time** | O(n * d) | O(d) per hash lookup |
| **Accuracy** | 100% | ~90-99% (tunable) |
| **Best for** | Small n, low d | Large n, high d |

> **Note:** You already have an LSH implementation in `Library/Probabilistic/locality-sensitive-hashing/` — it pairs directly with this KNN module for high-dimensional similarity search.

---

## 5. Scalability Analysis

### 5.1 By Dataset Size

| Dataset Size | Prediction Time (d=10) | Memory | Practicality |
| --- | --- | --- | --- |
| n = 100 | < 1 ms | ~8 KB | Trivial |
| n = 10,000 | ~10 ms | ~800 KB | Fast |
| n = 100,000 | ~100 ms | ~8 MB | Acceptable |
| n = 1,000,000 | ~1 sec | ~80 MB | Slow for real-time |
| n = 10,000,000 | ~10 sec | ~800 MB | Impractical (use LSH) |

### 5.2 By Dimensionality

| Dimensions (d) | Distance Cost | Quality | Recommendation |
| --- | --- | --- | --- |
| d = 2-5 | Very fast | Excellent | Use KNN directly |
| d = 5-20 | Fast | Good | Use KNN + KD-Tree |
| d = 20-100 | Moderate | Degrading | Use KNN + Ball Tree + normalization |
| d = 100-1000 | Expensive | Poor | Use PCA + KNN, or LSH |
| d > 1000 | Impractical | Meaningless | Use LSH or learned embeddings |

---

## 6. KNN vs. Other Classifiers: Full Complexity Comparison

| Classifier | Train Time | Predict Time | Train Space | Predict Space |
| --- | --- | --- | --- | --- |
| **KNN (brute)** | O(1) | O(n * d) | O(n * d) | O(n * d) |
| **KNN (KD-Tree)** | O(n * d * log n) | O(d * log n) | O(n * d) | O(n * d) |
| **Decision Tree** | O(n * m * log n) | O(log n) | O(n * log n) | O(nodes) |
| **Logistic Regression** | O(n * d * iter) | O(d) | O(d) | O(d) |
| **K-Means** | O(n * k * d * iter) | O(k * d) | O(k * d) | O(k * d) |
| **Random Forest** | O(T * n * m * log n) | O(T * log n) | O(T * n) | O(T * nodes) |

### Key Insight

KNN trades **fast training** for **slow prediction**. This makes it ideal for:
- Prototyping and baselines (instant "training")
- Small datasets where prediction cost is acceptable
- Scenarios where the model must be retrained frequently

And unsuitable for:
- Real-time prediction on large datasets
- Deployment on memory-constrained devices
- High-dimensional feature spaces

---

## 7. References

- Cover, T., & Hart, P. (1967). "Nearest Neighbor Pattern Classification." *IEEE Transactions on Information Theory*.
- Friedman, J., Bentley, J., & Finkel, R. (1977). "An Algorithm for Finding Best Matches in Logarithmic Expected Time." *ACM Transactions on Mathematical Software*.
- Indyk, P., & Motwani, R. (1998). "Approximate Nearest Neighbors: Towards Removing the Curse of Dimensionality." *STOC*.
- Beyer, K., et al. (1999). "When Is Nearest Neighbor Meaningful?" *ICDT*.
