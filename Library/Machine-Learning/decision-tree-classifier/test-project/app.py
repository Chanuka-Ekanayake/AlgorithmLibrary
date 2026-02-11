"""
Customer Churn Prediction - Decision Tree Demo

This interactive application demonstrates the Decision Tree classifier
for predicting customer churn in a telecommunications company.

Features:
- Age, Monthly charges, Contract length, Tech support, Total calls
- Binary classification: Churn (1) or Stay (0)
- Feature importance analysis
- Tree complexity metrics
- Accuracy evaluation

Dataset: Synthetic telecom customer data
"""

import sys
import os

# Add parent directory to path to import decision_tree module
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.decision_tree import DecisionTreeClassifier, accuracy_score
from typing import List, Tuple


def load_data() -> Tuple[List[List[float]], List[int], List[str]]:
    """
    Load customer churn dataset.
    
    Returns:
        (X, y, feature_names) where:
        - X: Feature matrix
        - y: Churn labels (0=stay, 1=churn)
        - feature_names: Names of features
    """
    # Feature names
    feature_names = [
        "Age",
        "Monthly Charges ($)",
        "Contract Length (months)",
        "Tech Support (0/1)",
        "Total Service Calls"
    ]
    
    # Training data: [Age, Monthly_Charges, Contract_Length, Tech_Support, Service_Calls]
    X_train = [
        # Customers who stayed (churn=0)
        [25, 45.0, 24, 1, 2],
        [30, 55.0, 12, 1, 1],
        [35, 65.0, 24, 1, 3],
        [40, 50.0, 24, 1, 2],
        [28, 48.0, 12, 1, 1],
        [33, 52.0, 24, 1, 2],
        [45, 70.0, 24, 1, 1],
        [38, 58.0, 12, 1, 2],
        [27, 46.0, 24, 1, 1],
        [42, 68.0, 24, 1, 3],
        [31, 54.0, 12, 1, 2],
        [36, 62.0, 24, 1, 1],
        [29, 49.0, 24, 1, 2],
        [44, 72.0, 24, 1, 1],
        [32, 56.0, 12, 1, 3],
        
        # Customers who churned (churn=1)
        [22, 85.0, 1, 0, 8],
        [26, 90.0, 1, 0, 9],
        [24, 88.0, 1, 0, 7],
        [23, 92.0, 1, 0, 10],
        [21, 87.0, 1, 0, 8],
        [25, 95.0, 1, 0, 11],
        [27, 89.0, 1, 0, 9],
        [20, 86.0, 1, 0, 7],
        [28, 93.0, 1, 0, 10],
        [24, 91.0, 1, 0, 8],
        [22, 84.0, 1, 0, 9],
        [26, 94.0, 1, 0, 11],
        [23, 88.0, 1, 0, 7],
        [25, 90.0, 1, 0, 10],
        [21, 85.0, 1, 0, 8],
    ]
    
    # Labels: 0=stay, 1=churn
    y_train = [0] * 15 + [1] * 15
    
    # Test data
    X_test = [
        [34, 60.0, 24, 1, 2],   # Should stay (similar to stay group)
        [37, 57.0, 12, 1, 3],   # Should stay
        [41, 66.0, 24, 1, 1],   # Should stay
        [23, 88.0, 1, 0, 9],    # Should churn (high charges, no support, many calls)
        [22, 92.0, 1, 0, 10],   # Should churn
        [24, 87.0, 1, 0, 8],    # Should churn
        [30, 75.0, 6, 0, 5],    # Ambiguous case
        [35, 80.0, 3, 0, 6],    # Ambiguous case
    ]
    
    y_test = [0, 0, 0, 1, 1, 1, 1, 0]  # True labels
    
    return X_train, y_train, X_test, y_test, feature_names


def print_header(title: str):
    """Print formatted section header."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def print_data_summary(X_train, y_train, X_test, y_test, feature_names):
    """Print dataset summary statistics."""
    print_header("Dataset Summary")
    
    print(f"\nFeatures ({len(feature_names)}):")
    for i, name in enumerate(feature_names):
        values = [sample[i] for sample in X_train]
        print(f"  {i+1}. {name:30} | Range: [{min(values):.1f}, {max(values):.1f}]")
    
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"  - Stayed (0): {y_train.count(0)} customers ({y_train.count(0)/len(y_train)*100:.1f}%)")
    print(f"  - Churned (1): {y_train.count(1)} customers ({y_train.count(1)/len(y_train)*100:.1f}%)")
    
    print(f"\nTest set: {len(X_test)} samples")
    print(f"  - Stayed (0): {y_test.count(0)} customers")
    print(f"  - Churned (1): {y_test.count(1)} customers")


def print_tree_structure(clf):
    """Print tree structure and complexity metrics."""
    print_header("Decision Tree Structure")
    
    print(f"\nTree Complexity Metrics:")
    print(f"  - Maximum Depth: {clf.get_depth()}")
    print(f"  - Number of Leaves: {clf.get_n_leaves()}")
    print(f"  - Total Nodes: {clf.get_n_leaves() * 2 - 1}")  # Approximation
    
    print(f"\nHyperparameters:")
    print(f"  - max_depth: {clf.max_depth}")
    print(f"  - min_samples_split: {clf.min_samples_split}")
    print(f"  - min_samples_leaf: {clf.min_samples_leaf}")
    print(f"  - criterion: {clf.criterion}")


def print_feature_importance(clf, feature_names):
    """Print and visualize feature importance."""
    print_header("Feature Importance Analysis")
    
    importances = clf.feature_importances()
    
    # Sort by importance
    sorted_indices = sorted(range(len(importances)), key=lambda i: importances[i], reverse=True)
    
    print("\nRanked Features (most important first):\n")
    
    for rank, idx in enumerate(sorted_indices, 1):
        importance = importances[idx]
        bar_length = int(importance * 50)  # Scale to 50 chars
        bar = "█" * bar_length
        
        print(f"{rank}. {feature_names[idx]:30} | {importance:6.2%} | {bar}")
    
    print("\nInterpretation:")
    print("  - Higher percentage = more important for predictions")
    print("  - Tree uses these features more often for splits")
    print("  - Top features drive customer churn decisions")


def print_predictions(X_test, y_test, predictions, feature_names):
    """Print detailed predictions with explanations."""
    print_header("Test Set Predictions")
    
    print("\n{:<5} {:<40} {:<12} {:<12} {:<8}".format(
        "No.", "Customer Profile", "Predicted", "Actual", "Correct?"
    ))
    print("-" * 85)
    
    for i, (sample, pred, true) in enumerate(zip(X_test, predictions, y_test), 1):
        # Create profile string
        profile = f"Age:{sample[0]:2}, Charge:${sample[1]:4.0f}, Contract:{sample[2]:2}mo"
        
        pred_label = "CHURN" if pred == 1 else "STAY"
        true_label = "CHURN" if true == 1 else "STAY"
        correct = "✓" if pred == true else "✗"
        
        print(f"{i:<5} {profile:<40} {pred_label:<12} {true_label:<12} {correct:<8}")


def interactive_prediction(clf, feature_names):
    """Allow user to input custom customer data for prediction."""
    print_header("Interactive Prediction")
    
    print("\nEnter customer details to predict churn:")
    print("(Press Enter for default values)\n")
    
    # Get user input with defaults
    try:
        age = input(f"  {feature_names[0]} [default: 30]: ").strip()
        age = float(age) if age else 30.0
        
        charges = input(f"  {feature_names[1]} [default: 60.0]: ").strip()
        charges = float(charges) if charges else 60.0
        
        contract = input(f"  {feature_names[2]} [default: 12]: ").strip()
        contract = float(contract) if contract else 12.0
        
        support = input(f"  {feature_names[3]} [default: 1]: ").strip()
        support = float(support) if support else 1.0
        
        calls = input(f"  {feature_names[4]} [default: 3]: ").strip()
        calls = float(calls) if calls else 3.0
        
        # Make prediction
        custom_sample = [[age, charges, contract, support, calls]]
        prediction = clf.predict(custom_sample)[0]
        
        print(f"\n{'─' * 70}")
        print(f"PREDICTION: Customer will {'CHURN ❌' if prediction == 1 else 'STAY ✓'}")
        print(f"{'─' * 70}")
        
        # Explain prediction
        print("\nKey factors:")
        if prediction == 1:
            print("  ⚠ High risk indicators detected:")
            if charges > 80:
                print("    - Very high monthly charges")
            if contract <= 3:
                print("    - Short contract (month-to-month)")
            if support == 0:
                print("    - No tech support subscription")
            if calls > 7:
                print("    - Excessive service calls")
        else:
            print("  ✓ Retention indicators:")
            if charges < 70:
                print("    - Reasonable monthly charges")
            if contract >= 12:
                print("    - Long-term contract")
            if support == 1:
                print("    - Has tech support")
            if calls <= 3:
                print("    - Few service calls")
        
    except ValueError:
        print("\nInvalid input! Using defaults instead.")
        interactive_prediction(clf, feature_names)
    except KeyboardInterrupt:
        print("\n\nExiting interactive mode...")


def main():
    """Main application entry point."""
    print("\n" + "🌲" * 35)
    print(" " * 15 + "DECISION TREE CLASSIFIER")
    print(" " * 12 + "Customer Churn Prediction Demo")
    print("🌲" * 35)
    
    # Load data
    X_train, y_train, X_test, y_test, feature_names = load_data()
    
    # Show dataset summary
    print_data_summary(X_train, y_train, X_test, y_test, feature_names)
    
    # Train decision tree
    print_header("Training Decision Tree")
    print("\nBuilding tree with hyperparameters:")
    print("  - max_depth: 5 (prevent overfitting)")
    print("  - min_samples_split: 2 (allow fine splits)")
    print("  - criterion: gini (faster computation)")
    
    clf = DecisionTreeClassifier(
        max_depth=5,
        min_samples_split=2,
        min_samples_leaf=1,
        criterion='gini'
    )
    
    clf.fit(X_train, y_train)
    print("\n✓ Training complete!")
    
    # Show tree structure
    print_tree_structure(clf)
    
    # Show feature importance
    print_feature_importance(clf, feature_names)
    
    # Make predictions on test set
    predictions = clf.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    print_predictions(X_test, y_test, predictions, feature_names)
    
    print_header("Model Performance")
    print(f"\nTest Accuracy: {accuracy:.1%}")
    print(f"  - Correct predictions: {sum(1 for p, t in zip(predictions, y_test) if p == t)}/{len(y_test)}")
    print(f"  - Incorrect predictions: {sum(1 for p, t in zip(predictions, y_test) if p != t)}/{len(y_test)}")
    
    # Detailed metrics
    tp = sum(1 for p, t in zip(predictions, y_test) if p == 1 and t == 1)
    tn = sum(1 for p, t in zip(predictions, y_test) if p == 0 and t == 0)
    fp = sum(1 for p, t in zip(predictions, y_test) if p == 1 and t == 0)
    fn = sum(1 for p, t in zip(predictions, y_test) if p == 0 and t == 1)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    
    print(f"\nDetailed Metrics:")
    print(f"  - Precision (churn): {precision:.1%} (of predicted churns, how many actually churned)")
    print(f"  - Recall (churn): {recall:.1%} (of actual churns, how many we caught)")
    print(f"  - True Positives: {tp} | True Negatives: {tn}")
    print(f"  - False Positives: {fp} | False Negatives: {fn}")
    
    # Interactive mode
    while True:
        print("\n" + "─" * 70)
        choice = input("\nTry interactive prediction? (y/n): ").strip().lower()
        
        if choice == 'y':
            interactive_prediction(clf, feature_names)
        elif choice == 'n':
            break
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")
    
    print("\n" + "=" * 70)
    print(" " * 20 + "Thank you for using Decision Tree Demo!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
