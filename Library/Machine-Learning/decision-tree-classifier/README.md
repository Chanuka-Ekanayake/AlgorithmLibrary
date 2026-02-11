# Decision Tree Classifier

A pure Python implementation of the **CART (Classification and Regression Trees)** algorithm for building decision trees. This classifier uses information gain (based on Gini impurity or entropy) to recursively split data and create a tree structure for classification tasks.

## 📋 Overview

Decision trees are supervised learning algorithms that partition the feature space into regions and assign a class label to each region. They work by recursively splitting the data based on features that maximize information gain, creating a tree where:

- **Internal nodes** represent decision points (feature tests)
- **Branches** represent outcomes of tests
- **Leaf nodes** represent class predictions

### Key Features

✅ **CART Algorithm**: Industry-standard decision tree implementation  
✅ **Multiple Split Criteria**: Supports both Gini impurity and entropy  
✅ **Hyperparameter Control**: max_depth, min_samples_split, min_samples_leaf  
✅ **Feature Importance**: Calculate which features are most influential  
✅ **Pure Python**: No external dependencies, easy to understand and modify  
✅ **Educational**: Clear implementation showing tree construction step-by-step

## 🎯 Use Cases

- **Customer Churn Prediction**: Will a customer leave based on usage patterns?
- **Loan Approval**: Should a loan be approved based on applicant features?
- **Medical Diagnosis**: Disease classification from symptoms and test results
- **Quality Control**: Classify products as pass/fail based on measurements
- **Email Spam Detection**: Classify emails based on content features

## 🚀 Quick Start

```python
from core.decision_tree import DecisionTreeClassifier, accuracy_score

# Sample data: [feature1, feature2] -> class
X_train = [
    [5.1, 3.5], [4.9, 3.0], [4.7, 3.2],  # Class 0
    [7.0, 3.2], [6.4, 3.2], [6.9, 3.1],  # Class 1
]
y_train = [0, 0, 0, 1, 1, 1]

X_test = [[5.0, 3.4], [6.7, 3.1]]
y_test = [0, 1]

# Train classifier
clf = DecisionTreeClassifier(max_depth=3, criterion='gini')
clf.fit(X_train, y_train)

# Make predictions
predictions = clf.predict(X_test)
print(f"Predictions: {predictions}")  # [0, 1]

# Evaluate
acc = accuracy_score(y_test, predictions)
print(f"Accuracy: {acc:.2%}")  # 100.00%

# Analyze tree
print(f"Tree depth: {clf.get_depth()}")
print(f"Number of leaves: {clf.get_n_leaves()}")
print(f"Feature importances: {clf.feature_importances()}")
```

## 📊 Algorithm Details

### How It Works

1. **Start at Root**: Begin with all training samples
2. **Find Best Split**: For each feature and threshold:
   - Split data into left (≤ threshold) and right (> threshold)
   - Calculate information gain
3. **Recursive Splitting**: Apply same process to child nodes
4. **Stopping Criteria**: Stop when:
   - Maximum depth reached
   - Node is pure (all same class)
   - Too few samples to split
5. **Leaf Assignment**: Assign most common class to leaf nodes

### Split Criteria

**Gini Impurity** (default):
```
Gini = 1 - Σ(p_i²)
```
- Measures probability of incorrect classification
- Favors purity (lower is better)
- Faster to compute

**Entropy** (information gain):
```
Entropy = -Σ(p_i * log₂(p_i))
```
- Measures information content
- Based on information theory
- Can produce more balanced trees

### Information Gain

```
Gain = Impurity(parent) - Weighted_Average(Impurity(children))
```

Split that maximizes information gain is selected.

## 🔧 API Reference

### DecisionTreeClassifier

```python
DecisionTreeClassifier(
    max_depth=None,           # Maximum tree depth (None = unlimited)
    min_samples_split=2,      # Minimum samples to split a node
    min_samples_leaf=1,       # Minimum samples in leaf node
    criterion='gini'          # Split criterion: 'gini' or 'entropy'
)
```

#### Methods

**`fit(X, y)`**
- Train the decision tree
- **Args**: 
  - `X`: List of feature vectors (n_samples × n_features)
  - `y`: List of labels (n_samples)
- **Returns**: self

**`predict(X)`**
- Predict classes for samples
- **Args**: `X` - List of feature vectors
- **Returns**: List of predicted class labels

**`predict_proba(X)`**
- Predict class probabilities
- **Args**: `X` - List of feature vectors
- **Returns**: List of dicts mapping class → probability

**`get_depth()`**
- Get maximum depth of tree
- **Returns**: Integer depth

**`get_n_leaves()`**
- Count number of leaf nodes
- **Returns**: Integer count

**`feature_importances()`**
- Calculate feature importance scores
- **Returns**: List of importance values (sum to 1.0)

### Helper Functions

**`accuracy_score(y_true, y_pred)`**
- Calculate classification accuracy
- **Returns**: Float in [0, 1]

## 📈 Complexity Analysis

### Time Complexity

**Training**: `O(n × m × log n)`
- `n` = number of samples
- `m` = number of features
- For each of `O(log n)` levels:
  - Try `m` features
  - Sort `O(n)` samples
  - Split `O(n)` samples

**Prediction**: `O(depth)` per sample
- Average: `O(log n)`
- Worst case: `O(n)` for degenerate tree

### Space Complexity

**Training**: `O(n × log n)`
- Tree structure: `O(number of nodes)`
- Recursive calls: `O(depth)` stack space
- Best case (balanced): `O(n)`
- Worst case (degenerate): `O(n²)`

**Prediction**: `O(1)` per sample (not counting tree storage)

See [complexity.md](docs/complexity.md) for detailed analysis.

## 🎓 Hyperparameter Tuning

### max_depth
- **Low values (1-3)**: Prevents overfitting, creates simple rules
- **High values (10+)**: Captures complex patterns, risks overfitting
- **None**: Grows until pure leaves (often overfits)

### min_samples_split
- **High values (20+)**: Forces generalization
- **Low values (2-5)**: Allows fine-grained splits

### min_samples_leaf
- **High values**: Smoother decision boundaries
- **Low values**: More complex, potentially overfit

### criterion
- **'gini'**: Faster, isolates frequent classes
- **'entropy'**: More balanced, theoretically motivated

## 🔍 Feature Importance

Decision trees naturally provide feature importance:

```python
importances = clf.feature_importances()
for i, imp in enumerate(importances):
    print(f"Feature {i}: {imp:.4f}")
```

Importance = Weighted sum of impurity reduction from splits using that feature.

## ⚖️ Pros & Cons

### Advantages
✅ **Interpretable**: Easy to visualize and explain decisions  
✅ **No Scaling Needed**: Works with features on different scales  
✅ **Handles Non-linearity**: Can model complex decision boundaries  
✅ **Fast Prediction**: O(log n) inference time  
✅ **Feature Importance**: Built-in feature ranking

### Disadvantages
❌ **Overfitting**: Can create overly complex trees  
❌ **Instability**: Small data changes can drastically change tree  
❌ **Greedy**: Locally optimal splits, not globally optimal  
❌ **Bias to Dominant Classes**: Imbalanced data issues  
❌ **Poor Extrapolation**: Can't predict beyond training data range

## 🆚 Comparison with Other Classifiers

| Algorithm | Interpretability | Training Speed | Accuracy | Overfitting Risk |
|-----------|-----------------|----------------|----------|------------------|
| Decision Tree | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Logistic Regression | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Random Forest | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| SVM | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Neural Network | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🧪 Testing

Run the interactive test project:

```bash
cd test-project
python app.py
```

The test project demonstrates:
- Customer churn prediction with real-world features
- Feature importance analysis
- Tree depth and complexity metrics
- Accuracy evaluation on test set

## 📚 Educational Resources

### Theory
- See [docs/logic.md](docs/logic.md) for detailed algorithm explanation
- See [docs/complexity.md](docs/complexity.md) for performance analysis

### Further Reading
- **"Classification and Regression Trees"** by Breiman et al. (1984)
- **"The Elements of Statistical Learning"** - Chapter 9
- **CART vs ID3**: CART uses binary splits, ID3 uses multi-way splits
- **Random Forest**: Ensemble of decision trees for better accuracy

## 🔗 Related Algorithms

- **[Logistic Regression](../logistic-regression/README.md)**: Linear classification baseline
- **[K-Means](../k-means-product-clustering/README.md)**: Unsupervised clustering
- **Random Forest** (potential future addition): Ensemble of decision trees
- **Gradient Boosting** (potential future addition): Boosted decision trees

## 🤝 Contributing

Contributions welcome! Potential improvements:
- Regression support (decision tree regressor)
- Pruning techniques (post-pruning, cost complexity)
- Handling missing values
- Categorical feature support
- Tree visualization export (Graphviz, ASCII)
- Cross-validation utilities

## 📄 License

MIT License - See repository root for details

## 📧 Support

For questions or issues:
1. Check [docs/logic.md](docs/logic.md) for algorithm details
2. See test project for usage examples
3. Open an issue on GitHub

---

**Algorithm Library** | Pure Python Machine Learning Implementations
