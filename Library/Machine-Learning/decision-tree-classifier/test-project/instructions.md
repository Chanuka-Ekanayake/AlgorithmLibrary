# Decision Tree Test Project - Instructions

## Overview

This interactive application demonstrates the Decision Tree Classifier algorithm for predicting customer churn in a telecommunications company. The demo shows how decision trees learn from customer data to identify patterns that lead to churn.

## Dataset

### Features (5 total)

1. **Age** - Customer age in years (20-45)
2. **Monthly Charges** - Monthly bill amount in dollars ($45-$95)
3. **Contract Length** - Contract duration in months (1-24)
4. **Tech Support** - Has tech support subscription (0=No, 1=Yes)
5. **Total Service Calls** - Number of calls to customer service (1-11)

### Target Variable

- **Churn Status**
  - 0 = Customer stayed
  - 1 = Customer churned (left company)

### Dataset Composition

- **Training Set**: 30 samples (15 stayed, 15 churned)
- **Test Set**: 8 samples (mixed for evaluation)

### Data Patterns

**Customers who STAY** typically have:
- Lower monthly charges ($45-$72)
- Longer contract lengths (12-24 months)
- Tech support subscription (1)
- Fewer service calls (1-3)

**Customers who CHURN** typically have:
- High monthly charges ($84-$95)
- Short contracts (month-to-month, 1 month)
- No tech support (0)
- Many service calls (7-11)

## Running the Demo

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (pure Python)

### Execution

```bash
cd test-project
python app.py
```

### Alternative

From repository root:

```bash
python Library/Machine-Learning/decision-tree-classifier/test-project/app.py
```

## What the Demo Shows

### 1. Dataset Summary

- Feature statistics (ranges, distributions)
- Training/test set composition
- Class balance information

### 2. Tree Training

- Hyperparameters used
- Training process completion
- Tree construction details

### 3. Tree Structure

**Complexity Metrics**:
- Maximum depth (how deep the tree goes)
- Number of leaf nodes (decision endpoints)
- Total nodes (internal + leaf nodes)

**Hyperparameters**:
- `max_depth=5` - Limits tree depth to prevent overfitting
- `min_samples_split=2` - Minimum samples required to split node
- `min_samples_leaf=1` - Minimum samples in leaf nodes
- `criterion='gini'` - Uses Gini impurity for splits

### 4. Feature Importance

Ranked list showing which features are most influential in predictions:

```
1. Monthly Charges     | 45.23% | ████████████████████
2. Contract Length     | 28.67% | ██████████████
3. Total Service Calls | 15.89% | ███████
4. Tech Support        | 8.12%  | ████
5. Age                 | 2.09%  | █
```

**Interpretation**:
- Higher percentage = more important for decision-making
- Top features drive the churn predictions
- Tree splits more often on important features

### 5. Test Predictions

Detailed prediction results for each test sample:

```
No.  Customer Profile                      Predicted   Actual      Correct?
--------------------------------------------------------------------------------
1    Age:34, Charge:$60, Contract:24mo    STAY        STAY        ✓
2    Age:23, Charge:$88, Contract:1mo     CHURN       CHURN       ✓
...
```

Shows:
- Customer features
- Model's prediction
- True label
- Whether prediction was correct

### 6. Performance Metrics

**Accuracy**: Overall correctness rate

**Detailed Metrics**:
- **Precision**: Of predicted churns, how many actually churned?
- **Recall**: Of actual churns, how many did we catch?
- **Confusion Matrix**: True/False Positives/Negatives

Example:
```
Test Accuracy: 87.5%
  - Correct predictions: 7/8
  - Incorrect predictions: 1/8

Detailed Metrics:
  - Precision (churn): 100.0%
  - Recall (churn): 75.0%
  - True Positives: 3 | True Negatives: 4
  - False Positives: 0 | False Negatives: 1
```

### 7. Interactive Prediction

Try custom customer profiles:

```
Enter customer details to predict churn:
  Age [default: 30]: 28
  Monthly Charges ($) [default: 60.0]: 85.0
  Contract Length (months) [default: 12]: 1
  Tech Support (0/1) [default: 1]: 0
  Total Service Calls [default: 3]: 9

──────────────────────────────────────────────────────────────────────
PREDICTION: Customer will CHURN ❌
──────────────────────────────────────────────────────────────────────

Key factors:
  ⚠ High risk indicators detected:
    - Very high monthly charges
    - Short contract (month-to-month)
    - No tech support subscription
    - Excessive service calls
```

**Try different scenarios**:
- Loyal customer: age=35, charges=55, contract=24, support=1, calls=2
- At-risk customer: age=25, charges=90, contract=1, support=0, calls=10
- Borderline case: age=30, charges=75, contract=6, support=0, calls=5

## Understanding the Output

### Tree Depth

- **Low depth (1-3)**: Simple rules, may underfit
- **Medium depth (4-7)**: Good balance
- **High depth (10+)**: Complex rules, may overfit

Our demo uses `max_depth=5` for good generalization.

### Feature Importance

**High importance** (>20%):
- Critical features that strongly influence churn
- Focus retention efforts on these factors

**Medium importance** (5-20%):
- Moderate influence, worth monitoring

**Low importance** (<5%):
- Minimal impact on decisions
- May be redundant or not useful

### Prediction Confidence

Decision trees make **deterministic** predictions:
- Follow same path for same input
- Leaf node contains final prediction
- No probability distribution (in basic version)

For probabilistic predictions, see ensemble methods (Random Forest).

## Learning Objectives

After running this demo, you should understand:

1. **How decision trees split data** based on feature values
2. **Information gain** and impurity metrics guide splits
3. **Feature importance** identifies key predictors
4. **Hyperparameters** control tree complexity
5. **Overfitting risks** with deep trees
6. **Practical applications** in customer analytics

## Experimentation Ideas

### Modify Hyperparameters

Edit `app.py` line ~270 to try different settings:

```python
# Original
clf = DecisionTreeClassifier(max_depth=5, criterion='gini')

# Try deeper tree (may overfit)
clf = DecisionTreeClassifier(max_depth=10, criterion='gini')

# Try entropy instead of Gini
clf = DecisionTreeClassifier(max_depth=5, criterion='entropy')

# Require more samples per split
clf = DecisionTreeClassifier(max_depth=5, min_samples_split=5)
```

Compare:
- Accuracy changes
- Tree complexity changes
- Feature importance changes

### Add More Data

Extend the training set in `load_data()` function:

```python
# Add more customer examples
X_train.append([32, 60.0, 18, 1, 2])  # Add new customer
y_train.append(0)  # Add corresponding label
```

Observe:
- Does accuracy improve with more data?
- How does tree structure change?

### Test Edge Cases

In interactive mode, try:

1. **Perfect customer**: Low charges, long contract, has support, few calls
2. **High-risk customer**: High charges, no contract, no support, many calls
3. **Contradictory features**: Low charges but many calls
4. **Neutral customer**: All average values

### Visualize Decisions

To understand how tree makes decisions, trace a prediction manually:

```
Sample: Age=28, Charges=85, Contract=1, Support=0, Calls=9

Tree might decide:
  Root: Charges <= 75? NO → go right
  Node: Contract <= 6? YES → go left
  Node: Support == 1? NO → go left
  Leaf: Predict CHURN
```

## Common Issues

### ImportError

If you get `ModuleNotFoundError: No module named 'core'`:

**Solution**: Run from test-project directory:
```bash
cd test-project
python app.py
```

The script adds parent directory to path automatically.

### Low Accuracy

If accuracy is poor (<70%):

- Check data quality (correct labels?)
- Try different hyperparameters
- Add more training data
- Check for class imbalance

### Tree Too Simple

If tree has depth 1-2:

- Reduce `min_samples_split`
- Increase `max_depth`
- Check if data has clear patterns

### Tree Too Complex

If tree has depth >10:

- Decrease `max_depth`
- Increase `min_samples_split`
- Increase `min_samples_leaf`

## Further Exploration

### Related Files

- [../core/decision_tree.py](../core/decision_tree.py) - Core algorithm implementation
- [../docs/logic.md](../docs/logic.md) - Detailed algorithm explanation
- [../docs/complexity.md](../docs/complexity.md) - Performance analysis
- [../README.md](../README.md) - Algorithm overview

### Next Steps

1. **Try other datasets**: Modify `load_data()` for different problems
2. **Compare criteria**: Run with both Gini and entropy, compare results
3. **Build ensemble**: Combine multiple trees (Random Forest concept)
4. **Add visualization**: Export tree structure to Graphviz
5. **Implement pruning**: Add post-pruning to reduce overfitting

### Real-World Applications

Adapt this code for:
- **Loan approval**: Predict creditworthiness
- **Medical diagnosis**: Disease classification from symptoms
- **Email filtering**: Spam vs. legitimate emails
- **Product recommendations**: User preferences
- **Quality control**: Defect detection

## Questions?

If you encounter issues or have questions:

1. Check [../docs/logic.md](../docs/logic.md) for algorithm details
2. Review [../README.md](../README.md) for API reference
3. Examine source code in [../core/decision_tree.py](../core/decision_tree.py)
4. Open an issue on GitHub repository

---

**Happy Learning!** 🌲📊

Experiment with the demo to build intuition for how decision trees work!
