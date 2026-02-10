# Customer Churn Prediction - Interactive Simulation

## Overview

This test project demonstrates **Logistic Regression** in action through a real-world business scenario: predicting customer churn for a telecommunications company.

## Business Problem

Telecom companies lose billions annually due to customer churn. By predicting which customers are likely to cancel their subscriptions, businesses can:

- Proactively offer retention incentives
- Allocate customer success resources efficiently
- Improve long-term revenue stability

## Features Used for Prediction

1. **Monthly Charges ($)**: Higher costs correlate with increased churn risk
2. **Tenure (months)**: Longer relationships reduce churn likelihood
3. **Support Tickets**: More complaints indicate dissatisfaction
4. **Contract Type**: Annual contracts show stronger commitment

## How to Run

### Prerequisites

```bash
pip install numpy
```

### Execute the Simulation

```bash
cd test-project
python app.py
```

## What the Simulation Does

### 1. Data Generation
- Creates 200 synthetic customer records
- 100 churned customers (high charges, short tenure, many tickets)
- 100 retained customers (moderate charges, long tenure, few tickets)

### 2. Model Training
- Splits data into 80% training, 20% testing
- Normalizes features for optimal gradient descent
- Trains using binary cross-entropy loss
- Displays progress every 100 iterations

### 3. Model Evaluation
- Reports training and testing accuracy
- Calculates precision, recall, and F1-score
- Shows learned feature weights (interpretability)

### 4. Interactive Prediction
- Allows you to input new customer details
- Provides churn probability estimate
- Suggests business actions based on risk level

## Expected Output

```
🏢 CUSTOMER CHURN PREDICTION SYSTEM 🏢
==================================================

✅ Generated 200 customer records
   - Churned: 100 customers
   - Retained: 100 customers

🚀 Training Logistic Regression Classifier...

Iteration 100/1000, Loss: 0.4521
Iteration 200/1000, Loss: 0.3845
...

📈 Performance Metrics:
   - Training Accuracy: 87.50%
   - Testing Accuracy: 85.00%
   - Precision: 0.83
   - Recall: 0.88
   - F1-Score: 0.85

🔍 Learned Feature Weights:
   Monthly Charges ($)           : +0.8234  ⬆️ INCREASES churn risk
   Tenure (months)              : -0.7521  ⬇️ DECREASES churn risk
   Support Tickets              : +0.6123  ⬆️ INCREASES churn risk
   Annual Contract (1=Yes)      : -0.4987  ⬇️ DECREASES churn risk
```

## Interpreting the Results

### Feature Weights

- **Positive weights** increase the log-odds of churn
  - Higher monthly charges → Higher churn risk
  - More support tickets → Higher churn risk

- **Negative weights** decrease the log-odds of churn
  - Longer tenure → Lower churn risk
  - Annual contract → Lower churn risk

### Probability Interpretation

- **0-30%**: Low risk - Customer likely to stay
- **30-70%**: Medium risk - Monitor and engage
- **70-100%**: High risk - Urgent retention actions needed

## Experiments to Try

### 1. Adjust Learning Rate
```
Learning rate: 0.01  → Slower convergence, more stable
Learning rate: 0.5   → Faster but might oscillate
```

### 2. Compare Regularization
```
none → May overfit on training data
l1   → Sparse weights (feature selection)
l2   → Distributed weights (all features contribute)
```

### 3. Test Edge Cases
```
Customer A: High charges, short tenure, many tickets → Should predict churn
Customer B: Low charges, long tenure, no tickets → Should predict retention
```

## Real-World Extensions

1. **Multi-class Classification**: Predict churn reason (price, service, competition)
2. **Feature Engineering**: Add interaction terms (charges × tickets)
3. **Threshold Tuning**: Adjust decision boundary based on business cost of false positives vs false negatives
4. **Time-Series Integration**: Include trend features (charges increasing over time)

## Key Takeaways

- Logistic Regression provides **interpretable** results (unlike black-box models)
- Feature normalization significantly improves **convergence speed**
- Regularization helps prevent **overfitting** on small datasets
- Probability outputs enable **risk-based decision making** rather than hard classifications

## Production Deployment

In a real system, this model would:
1. Train daily on historical data
2. Score all active customers each week
3. Trigger automated retention workflows for high-risk customers
4. Update model weights as new data arrives (online learning)
