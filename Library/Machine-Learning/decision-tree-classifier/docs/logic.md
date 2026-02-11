# Decision Tree Logic & Theory

## Table of Contents
1. [Introduction](#introduction)
2. [Core Concepts](#core-concepts)
3. [Algorithm Details](#algorithm-details)
4. [Mathematical Foundation](#mathematical-foundation)
5. [Tree Construction Process](#tree-construction-process)
6. [Splitting Criteria](#splitting-criteria)
7. [Prediction Process](#prediction-process)
8. [Feature Importance](#feature-importance)
9. [Overfitting & Pruning](#overfitting--pruning)
10. [Practical Considerations](#practical-considerations)

---

## Introduction

Decision trees are **supervised learning algorithms** that learn to partition the feature space into regions and assign a class label to each region. They create a flowchart-like structure where:

- **Internal nodes** test a feature against a threshold
- **Branches** represent the outcome of the test  
- **Leaf nodes** contain the class prediction

The tree is built **top-down** using a **greedy algorithm** that recursively selects the best feature split at each node.

### Why Decision Trees?

1. **Interpretability**: Trees mirror human decision-making
2. **No Preprocessing**: Works with raw features (no scaling needed)
3. **Non-linearity**: Can model complex decision boundaries
4. **Feature Selection**: Implicitly selects important features
5. **Mixed Data Types**: Handles categorical and numerical features

---

## Core Concepts

### Tree Structure

```
                    [Root Node]
                   Age <= 30?
                  /          \
               Yes            No
              /                \
      [Node]                  [Node]
   Income <= 50k?         Education >= 12?
     /        \              /           \
   Yes         No          Yes            No
   /            \          /               \
[Leaf]       [Leaf]    [Leaf]           [Leaf]
Deny         Approve   Approve          Approve
```

### Key Terminology

**Root Node**: Top of tree, contains all samples  
**Internal Node**: Decision point based on feature test  
**Leaf Node**: Terminal node with class prediction  
**Branch**: Connection between nodes  
**Depth**: Length of longest path from root to leaf  
**Splitting**: Dividing node into child nodes  
**Impurity**: Measure of class mixture in node  
**Information Gain**: Reduction in impurity from split

---

## Algorithm Details

### CART (Classification and Regression Trees)

Our implementation uses the **CART algorithm**, which:

1. Uses **binary splits** (≤ threshold vs > threshold)
2. Supports **Gini impurity** or **entropy** for splits
3. Grows tree **recursively** until stopping criteria met
4. Assigns **majority class** to leaf nodes

### Pseudocode

```
function BuildTree(X, y, depth):
    # Base cases (stopping criteria)
    if depth >= max_depth or len(y) < min_samples_split or all_same_class(y):
        return LeafNode(majority_class(y))
    
    # Find best split
    best_gain = -∞
    for each feature f in features:
        for each threshold t in unique_values(f):
            (X_left, y_left), (X_right, y_right) = split(X, y, f, t)
            gain = information_gain(y, y_left, y_right)
            if gain > best_gain:
                best_gain = gain
                best_feature = f
                best_threshold = t
    
    # If no good split found, make leaf
    if best_gain <= 0:
        return LeafNode(majority_class(y))
    
    # Recursively build children
    left_child = BuildTree(X_left, y_left, depth + 1)
    right_child = BuildTree(X_right, y_right, depth + 1)
    
    return InternalNode(best_feature, best_threshold, left_child, right_child)
```

---

## Mathematical Foundation

### Impurity Measures

#### Gini Impurity

Measures probability of incorrect classification if we randomly assign a label according to class distribution:

$$
\text{Gini}(S) = 1 - \sum_{i=1}^{C} p_i^2
$$

Where:
- $S$ = set of samples at node
- $C$ = number of classes  
- $p_i$ = proportion of samples in class $i$

**Properties**:
- Range: $[0, 0.5]$ for binary classification
- 0 = pure node (all samples same class)
- 0.5 = maximum impurity (equal class distribution)

**Example**:
```
Node with 100 samples: 60 class A, 40 class B
p_A = 60/100 = 0.6
p_B = 40/100 = 0.4

Gini = 1 - (0.6² + 0.4²)
     = 1 - (0.36 + 0.16)
     = 1 - 0.52
     = 0.48
```

#### Entropy

Measures information content or uncertainty:

$$
\text{Entropy}(S) = -\sum_{i=1}^{C} p_i \log_2(p_i)
$$

**Properties**:
- Range: $[0, \log_2(C)]$
- 0 = pure node
- $\log_2(C)$ = maximum entropy

**Example**:
```
Node with 100 samples: 60 class A, 40 class B
p_A = 0.6, p_B = 0.4

Entropy = -(0.6 × log₂(0.6) + 0.4 × log₂(0.4))
        = -(0.6 × -0.737 + 0.4 × -1.322)
        = -(-0.442 - 0.529)
        = 0.971
```

### Information Gain

Reduction in impurity from a split:

$$
\text{Gain}(S, A) = \text{Impurity}(S) - \sum_{v \in \text{Values}(A)} \frac{|S_v|}{|S|} \text{Impurity}(S_v)
$$

Where:
- $A$ = feature being split on
- $S_v$ = subset of $S$ where feature $A$ has value $v$

**Example**:
```
Parent: 100 samples (60 A, 40 B) → Gini = 0.48

Split on "Age <= 30":
  Left:  40 samples (10 A, 30 B) → Gini = 1 - (0.25² + 0.75²) = 0.375
  Right: 60 samples (50 A, 10 B) → Gini = 1 - (0.83² + 0.17²) = 0.278

Weighted child impurity:
  (40/100) × 0.375 + (60/100) × 0.278 = 0.15 + 0.167 = 0.317

Information Gain:
  0.48 - 0.317 = 0.163
```

Higher gain = better split!

---

## Tree Construction Process

### Step-by-Step Example

**Dataset**: Loan Approval

| Age | Income | Credit Score | Approved |
|-----|--------|--------------|----------|
| 25  | 30k    | 600          | No       |
| 35  | 50k    | 700          | Yes      |
| 45  | 70k    | 750          | Yes      |
| 22  | 25k    | 580          | No       |
| 50  | 80k    | 800          | Yes      |
| 28  | 35k    | 620          | No       |

**Step 1: Start at Root**
- All 6 samples
- Classes: 3 Yes, 3 No
- Gini = 1 - (0.5² + 0.5²) = 0.5

**Step 2: Evaluate All Possible Splits**

Try Age <= 30:
```
Left (Age <= 30):  4 samples (1 Yes, 3 No) → Gini = 0.375
Right (Age > 30):  2 samples (2 Yes, 0 No) → Gini = 0.0
Weighted Gini = (4/6) × 0.375 + (2/6) × 0.0 = 0.25
Gain = 0.5 - 0.25 = 0.25
```

Try Income <= 40k:
```
Left (Income <= 40k):  4 samples (1 Yes, 3 No) → Gini = 0.375
Right (Income > 40k):  2 samples (2 Yes, 0 No) → Gini = 0.0
Weighted Gini = 0.25
Gain = 0.25
```

Try Credit Score <= 650:
```
Left (Score <= 650):   4 samples (0 Yes, 4 No) → Gini = 0.0
Right (Score > 650):   2 samples (3 Yes, 0 No) → Gini = 0.0
Weighted Gini = 0.0
Gain = 0.5
```

**Best split: Credit Score <= 650** (highest gain)

**Step 3: Recursively Build Children**

Left child (Credit Score <= 650):
- 4 samples, all No
- Pure node → Make leaf with prediction "No"

Right child (Credit Score > 650):
- 2 samples, all Yes  
- Pure node → Make leaf with prediction "Yes"

**Final Tree**:
```
         Credit Score <= 650?
            /            \
          Yes            No
         /                \
    [Leaf: No]        [Leaf: Yes]
```

---

## Splitting Criteria

### Binary Splits (CART)

CART always creates **binary splits**:
- Left child: samples where feature ≤ threshold
- Right child: samples where feature > threshold

**Threshold Selection**:
For each feature, consider midpoints between consecutive unique values:

```
Feature values: [10, 20, 30, 40]
Candidate thresholds: [15, 25, 35]
  (midpoints between consecutive values)
```

### Multi-way Splits (ID3/C4.5)

Alternative algorithms like ID3 use **multi-way splits**:
- Create one child for each unique value
- Can handle categorical features more naturally
- Our CART implementation uses binary splits for simplicity

---

## Prediction Process

### Traversal Algorithm

```python
def predict(sample, node):
    # If leaf node, return class
    if node.is_leaf():
        return node.value
    
    # Otherwise, test feature and recurse
    if sample[node.feature] <= node.threshold:
        return predict(sample, node.left)
    else:
        return predict(sample, node.right)
```

### Example Prediction

Tree:
```
         Income <= 50k?
            /         \
          Yes          No
         /              \
    Age <= 30?      [Leaf: Yes]
      /      \
    Yes       No
    /          \
[Leaf: No]  [Leaf: Yes]
```

Predict for sample: `{Age: 25, Income: 40k}`

1. Root: Income (40k) <= 50k? → **Yes**, go left
2. Node: Age (25) <= 30? → **Yes**, go left  
3. Leaf: Return **"No"**

---

## Feature Importance

### Calculation Method

Feature importance = **Total impurity reduction** from all splits using that feature, weighted by number of samples.

$$
\text{Importance}(f) = \sum_{\text{splits on } f} \frac{n_{\text{node}}}{n_{\text{total}}} \times \Delta \text{Impurity}
$$

Where:
- $n_{\text{node}}$ = samples at node
- $\Delta \text{Impurity}$ = impurity reduction from split

### Example

Tree with 100 samples:
```
         Feature 0 <= 5?  (100 samples, Gain = 0.2)
            /         \
          ...          ...
       Feature 1 <= 10?  (40 samples, Gain = 0.1)
         /         \
       ...         ...
```

Raw importance:
- Feature 0: (100/100) × 0.2 = 0.2
- Feature 1: (40/100) × 0.1 = 0.04

Normalized:
- Feature 0: 0.2 / 0.24 = 0.833
- Feature 1: 0.04 / 0.24 = 0.167

Feature 0 is **5× more important** than Feature 1.

---

## Overfitting & Pruning

### Overfitting Problem

**Unpruned trees** memorize training data:
```
Tree depth: 50
Leaves: 1000
Training accuracy: 100%
Test accuracy: 60%  ← OVERFITTING!
```

**Signs of overfitting**:
- Very deep tree (depth > 20)
- Many leaves (leaves ≈ training samples)
- High training accuracy, low test accuracy
- Tiny splits (1-2 samples per leaf)

### Pre-Pruning (Early Stopping)

Stop growing tree before it's complete:

1. **max_depth**: Limit tree depth
   ```python
   clf = DecisionTreeClassifier(max_depth=5)
   ```

2. **min_samples_split**: Minimum samples to split node
   ```python
   clf = DecisionTreeClassifier(min_samples_split=20)
   ```

3. **min_samples_leaf**: Minimum samples in leaf
   ```python
   clf = DecisionTreeClassifier(min_samples_leaf=10)
   ```

4. **max_leaves**: Limit number of leaf nodes
   (Not in our implementation, but common)

### Post-Pruning

Grow full tree, then prune back:

1. **Reduced Error Pruning**: Remove nodes that don't hurt validation accuracy
2. **Cost Complexity Pruning**: Balance tree size vs accuracy using parameter α

$$
\text{Cost}(T) = \text{Error}(T) + \alpha \times |T|
$$

Where:
- $|T|$ = number of leaves
- $\alpha$ = complexity parameter

(Not implemented in basic version)

### Choosing Hyperparameters

**Rule of thumb**:
```
max_depth: 3-10 for most problems
min_samples_split: 2-50 (higher for noisy data)
min_samples_leaf: 1-20 (higher for smooth boundaries)
```

**Cross-validation**: Try multiple values and select best.

---

## Practical Considerations

### Handling Imbalanced Data

**Problem**: Tree biased toward majority class

**Solutions**:
1. **Class weights**: Penalize misclassifying minority class more
2. **Resampling**: Oversample minority or undersample majority
3. **Stratified splitting**: Maintain class proportions in splits

### Missing Values

**Problem**: What if feature value is unknown?

**Solutions**:
1. **Surrogate splits**: Use alternative feature for missing values
2. **Separate branch**: Add "missing" branch to node
3. **Imputation**: Fill missing values before training

(Our basic implementation assumes no missing values)

### Categorical Features

**Encoding options**:
1. **One-hot encoding**: Convert to binary features
2. **Ordinal encoding**: Assign numeric values
3. **Native support**: Multi-way splits (not in CART)

### Ensemble Methods

**Single trees are unstable** → Small data changes = big tree changes

**Solution**: **Combine multiple trees**

1. **Random Forest**: Train many trees on bootstrap samples
   - Each tree uses random feature subset
   - Predictions voted/averaged
   - Much more robust than single tree

2. **Gradient Boosting**: Sequentially train trees
   - Each tree corrects errors of previous
   - XGBoost, LightGBM = state-of-the-art

---

## Comparison: Gini vs Entropy

| Property | Gini | Entropy |
|----------|------|---------|
| **Computation** | Faster (no logarithm) | Slower |
| **Range (binary)** | [0, 0.5] | [0, 1] |
| **Tree structure** | Similar | Similar |
| **Preference** | Isolates frequent classes | More balanced splits |
| **Use case** | General purpose | When balance important |

**In practice**: Very similar results, Gini slightly faster.

---

## Summary

**Decision Trees**:
- ✅ Highly interpretable
- ✅ No feature scaling needed
- ✅ Handles non-linearity
- ❌ Prone to overfitting
- ❌ Unstable (high variance)
- ❌ Greedy (locally optimal)

**Best practices**:
1. Start with shallow trees (max_depth=3-5)
2. Tune hyperparameters with cross-validation
3. Use feature importance to understand model
4. Consider ensemble methods for production
5. Visualize tree to verify it makes sense

**Next steps**:
- Implement pruning techniques
- Add visualization export
- Build Random Forest ensemble
- Support regression tasks

---

For complexity analysis, see [complexity.md](complexity.md).  
For practical examples, see [test-project/app.py](../test-project/app.py).
