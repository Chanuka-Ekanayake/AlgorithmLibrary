# Algorithm Logic: K-Nearest Neighbors (KNN)

## 1. The Core Intuition: "You Are the Company You Keep"

KNN is built on a simple but powerful idea: **similar things exist in close proximity**. If you want to know what genre a movie belongs to, look at the movies most similar to it and see what genres they are.

Unlike Decision Trees or Logistic Regression that learn explicit rules or boundaries during training, KNN learns **nothing** during training. It simply memorizes the entire dataset. All the work happens at prediction time — this is called **lazy learning** (or instance-based learning).

---

## 2. The Algorithm in Three Steps

### Step 1: Store Everything

```text
Training Phase:
  Input: Dataset of N labeled examples
  Action: Store them. That's it.
  Time:   O(1)
```

### Step 2: Measure Distance

When a new, unlabeled point arrives, compute the distance from this query point to **every** stored training point.

```text
Query point: Q = [5.5, 3.0]

Distances to all training points:
  Point [5.1, 3.5] -> d = 0.57  (Class A)
  Point [4.9, 3.0] -> d = 0.60  (Class A)
  Point [7.0, 3.2] -> d = 1.52  (Class B)
  Point [6.4, 3.2] -> d = 0.92  (Class B)
  Point [4.7, 3.2] -> d = 0.82  (Class A)
  Point [6.9, 3.1] -> d = 1.40  (Class B)
```

### Step 3: Vote

Select the K nearest neighbors and let them vote on the class.

```text
K = 3, Nearest Neighbors:
  1. [5.1, 3.5] -> d = 0.57  -> Class A  ✓
  2. [4.9, 3.0] -> d = 0.60  -> Class A  ✓
  3. [4.7, 3.2] -> d = 0.82  -> Class A  ✓

Vote Result: Class A wins (3-0)
Prediction:  Class A
```

---

## 3. Distance Metrics: How to Measure "Similarity"

The choice of distance metric profoundly affects KNN's behavior.

### 3.1 Euclidean Distance (L2)

The straight-line distance between two points. The default and most common choice.

$$d(a, b) = \sqrt{\sum_{i=1}^{d} (a_i - b_i)^2}$$

```text
a = [1, 2], b = [4, 6]
d = sqrt((4-1)^2 + (6-2)^2) = sqrt(9 + 16) = sqrt(25) = 5.0
```

**Best for:** Continuous features on similar scales.

### 3.2 Manhattan Distance (L1)

The "city block" distance — sum of absolute differences. Imagine navigating a grid of streets.

$$d(a, b) = \sum_{i=1}^{d} |a_i - b_i|$$

```text
a = [1, 2], b = [4, 6]
d = |4-1| + |6-2| = 3 + 4 = 7.0
```

**Best for:** High-dimensional data, features with different units, or sparse data. More robust to outliers than Euclidean.

### 3.3 Minkowski Distance (Lp)

The generalization that includes both:

$$d(a, b) = \left(\sum_{i=1}^{d} |a_i - b_i|^p\right)^{1/p}$$

- p=1: Manhattan
- p=2: Euclidean
- p->infinity: Chebyshev (max absolute difference)

---

## 4. Voting Strategies

### 4.1 Uniform Voting

Every neighbor gets exactly 1 vote. Simple majority wins.

```text
K = 5 Neighbors:
  d=0.5 -> Class A  (1 vote)
  d=0.8 -> Class A  (1 vote)
  d=1.2 -> Class B  (1 vote)
  d=1.5 -> Class B  (1 vote)
  d=2.0 -> Class B  (1 vote)

Result: Class B wins 3-2
```

**Problem:** A distant neighbor has the same influence as a very close one. The Class B neighbors at d=1.5 and d=2.0 are far away but still outvote the close Class A neighbors.

### 4.2 Distance-Weighted Voting

Closer neighbors get more influence. Weight = 1 / distance.

```text
K = 5 Neighbors:
  d=0.5 -> Class A  (weight = 2.00)
  d=0.8 -> Class A  (weight = 1.25)
  d=1.2 -> Class B  (weight = 0.83)
  d=1.5 -> Class B  (weight = 0.67)
  d=2.0 -> Class B  (weight = 0.50)

Class A total: 2.00 + 1.25 = 3.25
Class B total: 0.83 + 0.67 + 0.50 = 2.00

Result: Class A wins 3.25 vs 2.00
```

Distance-weighted voting correctly identifies that the two very close Class A neighbors should outweigh the three distant Class B neighbors.

---

## 5. The Critical Importance of Feature Normalization

### The Problem

Consider predicting house prices with two features:
- **Area:** 500 - 5000 sq ft (range: 4500)
- **Bedrooms:** 1 - 6 (range: 5)

Without normalization, the distance is completely dominated by Area:

```text
House A: [2000 sqft, 3 beds]
House B: [2010 sqft, 6 beds]
House C: [4000 sqft, 3 beds]

d(A, B) = sqrt((2010-2000)^2 + (6-3)^2) = sqrt(100 + 9)   = 10.4
d(A, C) = sqrt((4000-2000)^2 + (3-3)^2) = sqrt(4000000 + 0) = 2000.0
```

Bedrooms are essentially ignored because Area's range is 900x larger.

### The Solution: Min-Max Normalization

Scale all features to [0, 1]:

$$x_{norm} = \frac{x - x_{min}}{x_{max} - x_{min}}$$

```text
After normalization:
House A: [0.333, 0.400]
House B: [0.336, 1.000]
House C: [0.778, 0.400]

d(A, B) = sqrt((0.003)^2 + (0.600)^2) = 0.600
d(A, C) = sqrt((0.444)^2 + (0.000)^2) = 0.444
```

Now House C (same bedrooms, different area) is actually **closer** than House B (same area, different bedrooms), which is a much more reasonable similarity measure.

---

## 6. Choosing K: The Bias-Variance Trade-off

### K = 1 (Low Bias, High Variance)

- Every prediction is determined by a single nearest neighbor.
- Decision boundary is extremely jagged and complex.
- Memorizes noise in the training data.
- Training accuracy = 100% (always predicts the exact nearest point).
- Test accuracy is often poor (overfitting).

### K = N (High Bias, Low Variance)

- Every prediction uses the entire training set.
- Always predicts the majority class.
- Decision boundary is trivially simple.
- Ignores all local structure in the data.

### Sweet Spot: K = sqrt(N)

A common heuristic is K = sqrt(N) where N is the training set size.

```text
N = 100  -> K = 10
N = 1000 -> K = 31
N = 10000 -> K = 100
```

**Additional rules:**
- Use **odd K** for binary classification to avoid ties.
- Use **cross-validation** to find the optimal K for your specific dataset.

---

## 7. The Curse of Dimensionality

KNN's biggest weakness emerges in **high-dimensional feature spaces**.

### The Problem

As the number of dimensions (features) increases:

1. **All points become equidistant.** In 100+ dimensions, the difference between the nearest and farthest neighbor shrinks to near-zero. Every point looks equally "close."

2. **Data becomes sparse.** To maintain the same density of points, you need exponentially more data as dimensions increase. In 20D space, you'd need roughly 10^20 samples to have the same density as 100 samples in 2D.

3. **Distance metrics lose meaning.** Euclidean distance in 1000D space does not correlate well with intuitive "similarity."

### The Mitigation

- **Dimensionality reduction** (PCA, t-SNE) before applying KNN.
- **Feature selection** to keep only the most relevant features.
- **Locality-Sensitive Hashing (LSH)** — which you already have in `Library/Probabilistic/` — for approximate nearest-neighbor search in high dimensions.

---

## 8. KNN vs. Other Classifiers

| Property | KNN | Decision Tree | Logistic Regression |
| --- | --- | --- | --- |
| **Training time** | O(1) | O(n * m * log n) | O(n * m * iterations) |
| **Prediction time** | O(n * d) per query | O(log n) per query | O(d) per query |
| **Interpretability** | Low (black box) | High (rule-based) | Medium (coefficients) |
| **Handles non-linearity** | Yes (naturally) | Yes (axis-aligned) | No (linear boundary) |
| **Memory at inference** | O(n * d) full dataset | O(nodes) tree only | O(d) weights only |
| **Sensitive to scale** | Yes (needs normalization) | No | Yes |

**Rule of thumb:** Use KNN when you have a small-to-medium dataset, low dimensionality, and want a quick baseline without any tuning. Switch to a tree-based method (Random Forest, Gradient Boosting) for larger datasets.
