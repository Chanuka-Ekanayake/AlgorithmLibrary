import sys
import os
import numpy as np

# Add the parent directory to the path to import the core logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.logistic_regression import LogisticRegression

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_customer_data(n_samples=200):
    """
    Generate synthetic customer data for churn prediction.
    Features: [Monthly Charges, Tenure (months), Support Tickets, Contract Type]
    """
    np.random.seed(42)
    
    # Churned customers (label = 1)
    churned_charges = np.random.uniform(70, 100, n_samples // 2)
    churned_tenure = np.random.uniform(1, 12, n_samples // 2)
    churned_tickets = np.random.uniform(3, 10, n_samples // 2)
    churned_contract = np.random.choice([0, 1], n_samples // 2, p=[0.8, 0.2])  # 0=monthly, 1=annual
    
    # Retained customers (label = 0)
    retained_charges = np.random.uniform(30, 70, n_samples // 2)
    retained_tenure = np.random.uniform(12, 60, n_samples // 2)
    retained_tickets = np.random.uniform(0, 3, n_samples // 2)
    retained_contract = np.random.choice([0, 1], n_samples // 2, p=[0.3, 0.7])
    
    # Combine data
    X = np.column_stack([
        np.concatenate([churned_charges, retained_charges]),
        np.concatenate([churned_tenure, retained_tenure]),
        np.concatenate([churned_tickets, retained_tickets]),
        np.concatenate([churned_contract, retained_contract])
    ])
    
    y = np.concatenate([np.ones(n_samples // 2), np.zeros(n_samples // 2)])
    
    # Shuffle
    indices = np.random.permutation(n_samples)
    X, y = X[indices], y[indices]
    
    return X, y

def normalize_features(X):
    """Normalize features to have mean=0 and std=1 for better convergence."""
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    return (X - mean) / (std + 1e-8), mean, std

def customer_churn_simulation():
    clear_screen()
    print("=" * 60)
    print("🏢 CUSTOMER CHURN PREDICTION SYSTEM 🏢")
    print("=" * 60)
    print("\n📊 Use Case: Telecom Company Customer Retention")
    print("Predict whether a customer will cancel their subscription.\n")
    
    # 1. GENERATE DATASET
    print("🔄 Generating synthetic customer data...")
    X, y = generate_customer_data(n_samples=200)
    
    # Feature names for interpretation
    feature_names = ["Monthly Charges ($)", "Tenure (months)", "Support Tickets", "Annual Contract (1=Yes)"]
    
    print(f"✅ Generated {len(X)} customer records")
    print(f"   - Features: {len(feature_names)}")
    print(f"   - Churned: {int(np.sum(y))} customers")
    print(f"   - Retained: {int(len(y) - np.sum(y))} customers\n")
    
    # 2. TRAIN-TEST SPLIT
    split_idx = int(0.8 * len(X))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    # 3. FEATURE NORMALIZATION
    X_train_norm, mean, std = normalize_features(X_train)
    X_test_norm = (X_test - mean) / (std + 1e-8)
    
    print("📚 Dataset Split:")
    print(f"   - Training: {len(X_train)} samples")
    print(f"   - Testing: {len(X_test)} samples\n")
    
    # 4. USER INPUT FOR HYPERPARAMETERS
    print("⚙️  Model Configuration:")
    try:
        lr = float(input("Learning rate (default 0.1): ") or 0.1)
        iterations = int(input("Number of iterations (default 1000): ") or 1000)
        regularization = input("Regularization type (l1/l2/none, default l2): ") or "l2"
        if regularization.lower() == "none":
            regularization = None
    except ValueError:
        lr, iterations, regularization = 0.1, 1000, "l2"
    
    # 5. TRAINING
    print(f"\n🚀 Training Logistic Regression Classifier...")
    print(f"   - Learning Rate: {lr}")
    print(f"   - Iterations: {iterations}")
    print(f"   - Regularization: {regularization}\n")
    
    model = LogisticRegression(
        learning_rate=lr,
        n_iterations=iterations,
        regularization=regularization,
        lambda_param=0.01
    )
    
    model.fit(X_train_norm, y_train)
    
    # 6. EVALUATION
    clear_screen()
    print("=" * 60)
    print("✅ TRAINING COMPLETE - MODEL EVALUATION")
    print("=" * 60)
    
    train_accuracy = model.score(X_train_norm, y_train)
    test_accuracy = model.score(X_test_norm, y_test)
    
    print(f"\n📈 Performance Metrics:")
    print(f"   - Training Accuracy: {train_accuracy:.2f}%")
    print(f"   - Testing Accuracy: {test_accuracy:.2f}%")
    
    # Calculate additional metrics
    y_pred = model.predict(X_test_norm)
    true_positives = np.sum((y_pred == 1) & (y_test == 1))
    false_positives = np.sum((y_pred == 1) & (y_test == 0))
    true_negatives = np.sum((y_pred == 0) & (y_test == 0))
    false_negatives = np.sum((y_pred == 0) & (y_test == 1))
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"   - Precision: {precision:.2f}")
    print(f"   - Recall: {recall:.2f}")
    print(f"   - F1-Score: {f1_score:.2f}")
    
    # 7. FEATURE IMPORTANCE
    print(f"\n🔍 Learned Feature Weights:")
    for name, weight in zip(feature_names, model.weights):
        direction = "⬆️ INCREASES" if weight > 0 else "⬇️ DECREASES"
        print(f"   {name:30s}: {weight:+.4f}  {direction} churn risk")
    print(f"   {'Bias (Intercept)':30s}: {model.bias:+.4f}")
    
    # 8. PREDICTION ON NEW CUSTOMER
    print("\n" + "=" * 60)
    print("🔮 PREDICT CHURN RISK FOR A NEW CUSTOMER")
    print("=" * 60)
    
    try:
        print("\nEnter customer details:")
        charges = float(input("Monthly Charges ($30-$100): "))
        tenure = float(input("Tenure in months (1-60): "))
        tickets = float(input("Support Tickets (0-10): "))
        contract = int(input("Annual Contract? (0=No, 1=Yes): "))
        
        new_customer = np.array([[charges, tenure, tickets, contract]])
        new_customer_norm = (new_customer - mean) / (std + 1e-8)
        
        probability = model.predict_proba(new_customer_norm)[0]
        prediction = model.predict(new_customer_norm)[0]
        
        print(f"\n📊 Prediction Results:")
        print(f"   - Churn Probability: {probability:.1%}")
        print(f"   - Risk Level: ", end="")
        
        if probability < 0.3:
            print("🟢 LOW (Customer likely to stay)")
        elif probability < 0.7:
            print("🟡 MEDIUM (Requires attention)")
        else:
            print("🔴 HIGH (Urgent retention needed)")
        
        print(f"\n   - Final Prediction: {'❌ WILL CHURN' if prediction == 1 else '✅ WILL STAY'}")
        
        # Business recommendation
        print(f"\n💡 Recommended Action:")
        if probability > 0.7:
            print("   - Offer loyalty discount")
            print("   - Assign dedicated account manager")
            print("   - Propose annual contract upgrade")
        elif probability > 0.3:
            print("   - Send satisfaction survey")
            print("   - Monitor account activity")
        else:
            print("   - Standard service level")
            
    except ValueError:
        print("❌ Invalid input. Skipping prediction.")
    
    # 9. LOSS CONVERGENCE
    print(f"\n📉 Training Loss Curve:")
    loss_samples = [0, len(model.losses)//4, len(model.losses)//2, 3*len(model.losses)//4, len(model.losses)-1]
    for idx in loss_samples:
        iteration = idx + 1
        loss = model.losses[idx]
        print(f"   Iteration {iteration:4d}: Loss = {loss:.6f}")
    
    print("\n" + "=" * 60)
    print("Thank you for using the Customer Churn Prediction System!")
    print("=" * 60)

if __name__ == "__main__":
    customer_churn_simulation()
