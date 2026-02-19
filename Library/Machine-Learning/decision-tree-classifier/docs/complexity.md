# Time & Space Complexity Analysis

## Table of Contents
1. [Overview](#overview)
2. [Training Complexity](#training-complexity)
3. [Prediction Complexity](#prediction-complexity)
4. [Space Complexity](#space-complexity)
5. [Detailed Analysis](#detailed-analysis)
6. [Optimization Strategies](#optimization-strategies)
7. [Comparison with Other Algorithms](#comparison-with-other-algorithms)
8. [Practical Performance](#practical-performance)

---

## Overview

### Quick Reference

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| **Training** | O(n × m × log n) | O(n × log n) |
| **Prediction (single)** | O(log n) avg, O(n) worst | O(1) |
| **Prediction (batch)** | O(k × log n) avg | O(k) |
| **Feature importance** | O(nodes) | O(m) |

Where:
- **n** = number of training samples
- **m** = number of features
- **k** = number of prediction samples
- **nodes** = number of nodes in tree

### Best/Average/Worst Case

| Case | Training | Prediction | Tree Structure |
|------|----------|------------|----------------|
| **Best** | O(n × m) | O(log n) | Balanced, shallow |
| **Average** | O(n × m × log n) | O(log n) | Reasonably balanced |
| **Worst** | O(n² × m) | O(n) | Degenerate (linear) |

---

## Training Complexity

### Overall: O(n × m × log n)

Decision tree training involves recursively building the tree by finding the best split at each node.

### Breakdown

#### 1. Tree Depth: O(log n) to O(n)

**Balanced tree** (best case):
- Depth = O(log n)
- Each level splits data roughly in half
- Example: 1000 samples → ~10 levels

**Degenerate tree** (worst case):
- Depth = O(n)
- Each split separates only 1 sample
- Essentially a linked list

**Typical case**:
- Depth = O(log n) with stopping criteria
- max_depth parameter limits depth

#### 2. Splits Per Node: O(m × n)

For each node, we must:

**Step A: Iterate through features** - O(m)
```python
for feature in range(m):  # O(m)
    # Evaluate splits for this feature
```

**Step B: Get unique values** - O(n)
```python
unique_values = sorted(set(X[:, feature]))  # O(n log n) for sorting
```

**Step C: Try each threshold** - O(n) thresholds × O(n) split cost
```python
for threshold in thresholds:  # O(n) thresholds
    split_data(X, y, feature, threshold)  # O(n) to partition
    calculate_gain(y, y_left, y_right)     # O(n) to compute impurity
```

Total per node: **O(m × n log n)** (dominated by sorting)

#### 3. Total Training Cost

```
Cost = (nodes in tree) × (cost per node)
     = O(n) × O(m × n log n)    # Worst case: O(n) nodes
     = O(n² × m × log n)
```

**BUT** in practice with balanced tree:
```
Cost = O(log n) levels × O(n) samples per level × O(m) features
     = O(n × m × log n)
```

### Detailed Example

**Dataset**: n=1000 samples, m=10 features

**Balanced tree** (max_depth=10):
```
Level 0: 1000 samples × 10 features × 1000 thresholds ≈ 10M operations
Level 1: 500+500 samples × 10 features × 500 thresholds ≈ 5M operations  
Level 2: 250×4 samples × 10 features × 250 thresholds ≈ 2.5M operations
...
Total: ~10 levels × average 5M ops ≈ 50M operations
```

**Actual formula**:
```
O(n × m × log n) = O(1000 × 10 × log₂(1000))
                 = O(1000 × 10 × 10)
                 = O(100,000) comparisons
```

### Factors Affecting Training Time

1. **Number of samples (n)**
   - Linear impact on each level
   - Logarithmic impact on depth

2. **Number of features (m)**
   - Linear impact (must try all features)
   - Can optimize with feature sampling

3. **Number of unique values**
   - More unique values = more thresholds to try
   - Continuous features worse than discrete

4. **Stopping criteria**
   - max_depth: Limits depth directly
   - min_samples_split: Reduces nodes
   - Early stopping: Faster training

---

## Prediction Complexity

### Single Sample: O(log n) average, O(n) worst

Prediction traverses tree from root to leaf.

### Analysis

**Balanced tree** (best case):
```python
def predict(sample, node):
    if node.is_leaf():           # O(1)
        return node.value
    
    if sample[node.feature] <= node.threshold:  # O(1)
        return predict(sample, node.left)        # Recurse
    else:
        return predict(sample, node.right)       # Recurse
```

- Depth of balanced tree: O(log n)
- Operations per level: O(1)
- **Total: O(log n)**

**Degenerate tree** (worst case):
- Depth: O(n)
- **Total: O(n)**

### Batch Prediction: O(k × log n)

Predicting k samples:
```python
predictions = [predict(sample) for sample in X]  # k iterations
```

- Each prediction: O(log n)
- k predictions: **O(k × log n)**

### Example

**Tree**: depth=10 (balanced)
```
1 prediction:     10 comparisons
100 predictions:  1,000 comparisons  
1000 predictions: 10,000 comparisons
```

**Very fast!** Much faster than training.

---

## Space Complexity

### Tree Storage: O(n × log n) average

### Breakdown

#### 1. Node Storage

Each node stores:
```python
class TreeNode:
    feature: int          # 4 bytes
    threshold: float      # 8 bytes
    left: pointer         # 8 bytes
    right: pointer        # 8 bytes
    value: Any            # variable
    samples: int          # 4 bytes
    impurity: float       # 8 bytes
    # Total: ~40 bytes per node
```

#### 2. Number of Nodes

**Balanced tree**:
- Let L = number of leaf nodes
- Depth: d ≈ log₂(L) for a full, balanced binary tree
- Internal nodes: L - 1
- Leaf nodes: L
- **Total nodes: 2L - 1 = O(L)**  
  If each leaf contains on average k samples, then L ≈ n / k and total nodes are O(n / k) = O(n).

**With min_samples_leaf**:
- Each leaf has ≥ min_samples_leaf samples
- Max leaves: n / min_samples_leaf
- **Total nodes: O(n / min_samples_leaf)**

#### 3. Total Space

**Best case** (balanced, max_depth limited):
```
Nodes = O(2^max_depth)
Space = O(2^max_depth × 40 bytes)

Example: max_depth=10
Nodes = 2^10 = 1024
Space ≈ 40 KB
```

**Average case** (balanced tree):
```
Nodes = O(n)
Space = O(n × 40 bytes)

Example: n=1000
Space ≈ 40 KB
```

**Worst case** (degenerate tree):
```
Nodes = O(n)
Each node has left child only
Space = O(n × 40 bytes)

Example: n=1000
Space ≈ 40 KB
```

### Auxiliary Space During Training

**Recursive call stack**:
- Depth: O(log n) to O(n)
- Each frame: O(1)
- **Total: O(log n) to O(n)**

**Data copies** (our implementation):
- Each split creates new lists
- Worst case: O(n) copies per node
- **Total: O(n²) worst case**

**Optimization** (not in our implementation):
- Use indices instead of copying
- **Reduces to O(n) auxiliary space**

---

## Detailed Analysis

### Training: Step-by-Step

```python
def build_tree(X, y, depth=0):
    # Check stopping criteria - O(1)
    if should_stop(X, y, depth):
        return make_leaf(y)  # O(n) to count classes
    
    # Find best split - O(m × n log n)
    best_feature, best_threshold = find_best_split(X, y)
    
    # Split data - O(n)
    (X_left, y_left), (X_right, y_right) = split(X, y, best_feature, best_threshold)
    
    # Recursively build children - T(n/2) + T(n/2)
    left = build_tree(X_left, y_left, depth + 1)
    right = build_tree(X_right, y_right, depth + 1)
    
    return Node(best_feature, best_threshold, left, right)
```

### Recurrence Relation

**Balanced tree**:
```
T(n) = 2 × T(n/2) + O(m × n log n)

Solve using Master Theorem:
a=2, b=2, f(n)=O(m × n log n)

log_b(a) = log₂(2) = 1
f(n) = Ω(n^c) where c=1

f(n) is polynomially larger than n^log_b(a)
→ T(n) = O(f(n)) = O(m × n log n)
```

**Worst case** (degenerate):
```
T(n) = T(n-1) + O(m × n log n)
     = O(m × n² log n)
```

### Impurity Calculation: O(n)

**Gini impurity**:
```python
def gini(y):
    counts = Counter(y)           # O(n)
    n = len(y)
    gini = 1.0
    for count in counts.values(): # O(C) where C = classes
        p = count / n
        gini -= p ** 2
    return gini                   # Total: O(n)
```

**Entropy**:
```python
def entropy(y):
    counts = Counter(y)           # O(n)
    n = len(y)
    ent = 0.0
    for count in counts.values(): # O(C)
        p = count / n
        ent -= p * log(p)         # log() is O(1)
    return ent                    # Total: O(n)
```

**Information gain**:
```python
def information_gain(y, y_left, y_right):
    n = len(y)
    n_left = len(y_left)
    n_right = len(y_right)
    
    parent_imp = impurity(y)                    # O(n)
    left_imp = impurity(y_left)                 # O(n_left)
    right_imp = impurity(y_right)               # O(n_right)
    
    weighted = (n_left/n)*left_imp + (n_right/n)*right_imp
    
    return parent_imp - weighted                # Total: O(n)
```

---

## Optimization Strategies

### 1. Pre-sorting Features

**Problem**: Sorting at each node is expensive

**Solution**: Pre-sort features once
```python
# Before building tree
sorted_indices = [sort(X[:, f]) for f in range(m)]  # O(m × n log n)

# At each node, use pre-sorted indices
# Reduces per-node cost from O(m × n log n) to O(m × n)
```

**Trade-off**:
- Training: O(m × n log n) → O(m × n log n) (same asymptotic)
- Space: O(m × n) for indices

### 2. Feature Sampling

**Technique**: Only consider random subset of features

```python
# Instead of trying all m features
n_features_to_try = int(sqrt(m))  # e.g., for Random Forest

# Reduces cost per node from O(m × ...) to O(sqrt(m) × ...)
```

### 3. Sample Sampling (Bootstrap)

**Technique**: Train on random subset of data

```python
# Sample with replacement
sample_indices = random.choices(range(n), k=n)
X_sample = X[sample_indices]

# Reduces n, speeds up training
```

### 4. Early Stopping

**Aggressive stopping criteria**:
```python
clf = DecisionTreeClassifier(
    max_depth=5,           # Limit depth
    min_samples_split=20,  # Require more samples to split
    min_samples_leaf=10    # Require more samples in leaves
)
```

**Impact**:
- Reduces depth from O(log n) to constant
- Reduces nodes from O(n) to O(2^max_depth)

### 5. Parallel Splits

**Technique**: Evaluate features in parallel

```python
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor() as executor:
    gains = executor.map(evaluate_feature, features)

# Doesn't reduce asymptotic complexity
# But can give m-fold speedup on m cores
```

---

## Comparison with Other Algorithms

### Training Time

| Algorithm | Time Complexity | Notes |
|-----------|----------------|--------|
| **Decision Tree** | O(n × m × log n) | Depends on depth |
| Logistic Regression | O(n × m × iter) | iter = iterations to converge |
| K-Means | O(n × k × iter) | k = clusters |
| SVM (linear) | O(n² × m) to O(n³ × m) | Depends on solver |
| Random Forest | O(t × n × m × log n) | t = trees |
| Naive Bayes | O(n × m) | Very fast |

### Prediction Time

| Algorithm | Time Complexity |
|-----------|----------------|
| **Decision Tree** | O(log n) avg |
| Logistic Regression | O(m) |
| K-Means | O(k × m) |
| SVM | O(sv × m) (sv = support vectors) |
| Random Forest | O(t × log n) |
| Naive Bayes | O(m) |

### Space Complexity

| Algorithm | Space Complexity |
|-----------|------------------|
| **Decision Tree** | O(n) nodes |
| Logistic Regression | O(m) weights |
| K-Means | O(k × m) centroids |
| SVM | O(sv × m) support vectors |
| Random Forest | O(t × n) nodes |
| Naive Bayes | O(m × C) statistics |

---

## Practical Performance

### Scalability Analysis

**Small datasets** (n < 1,000):
```
Training: < 1 second
Prediction: microseconds
Bottleneck: Usually not a concern
```

**Medium datasets** (1,000 < n < 100,000):
```
Training: seconds to minutes
Prediction: milliseconds
Bottleneck: Number of features, tree depth
```

**Large datasets** (n > 100,000):
```
Training: minutes to hours
Prediction: still fast (milliseconds)
Bottleneck: O(n² × m) worst case, memory for n samples
```

### Memory Requirements

**Example**: n=100,000 samples, m=50 features

**Training**:
```
Original data: 100,000 × 50 × 8 bytes = 40 MB
Tree nodes: ~100,000 nodes × 40 bytes = 4 MB
Auxiliary space: varies, up to 40 MB
Total: ~80 MB
```

**Prediction** (tree only):
```
Tree storage: 4 MB
Very memory efficient!
```

### Performance Tips

1. **Limit tree depth** for faster training
   ```python
   clf = DecisionTreeClassifier(max_depth=10)
   ```

2. **Increase min_samples_split** to reduce nodes
   ```python
   clf = DecisionTreeClassifier(min_samples_split=50)
   ```

3. **Feature selection** to reduce m
   ```python
   # Use only important features
   important_features = [0, 2, 5, 7]
   X_reduced = X[:, important_features]
   ```

4. **Sample data** for very large datasets
   ```python
   # Train on subset
   indices = random.sample(range(n), k=10000)
   clf.fit(X[indices], y[indices])
   ```

---

## Summary

### Time Complexity

- **Training**: O(n × m × log n) average
- **Prediction**: O(log n) average per sample
- **Best for**: Fast prediction on trained model

### Space Complexity

- **Tree storage**: O(n) nodes average
- **Very efficient** for prediction
- **Memory during training** can be high (O(n²) worst case)

### Optimization

- Pre-sorting: Constant factor speedup
- Feature/sample sampling: Reduces m and n
- Early stopping: Limits depth and nodes
- Parallelization: Utilizes multiple cores

### When to Use

✅ **Good for**:
- Need interpretable model
- Fast prediction required
- Non-linear decision boundaries
- Mixed feature types

❌ **Avoid when**:
- Very large datasets (n > 1M)
- Need globally optimal solution
- Unstable predictions problematic

**Better alternatives**:
- Random Forest: More stable, better accuracy
- Gradient Boosting: State-of-the-art performance
- Logistic Regression: Faster training, linear problems

---

For algorithm details, see [logic.md](logic.md).  
For practical usage, see [test-project/app.py](../test-project/app.py).
