import sys
import io
import time
from pathlib import Path

# Fix Windows console encoding for Unicode output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path for core logic access
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.neural_network import NeuralNetwork
except ImportError:
    print("Error: Ensure 'core/neural_network.py' and 'core/__init__.py' exist.")
    sys.exit(1)


def run_xor_demo():
    print("\n" + "=" * 65)
    print("  NEURAL NETWORK SIMULATOR")
    print("  Algorithm: Backpropagation (Multi-Layer Perceptron)")
    print("=" * 65)
    print("  Problem: The XOR Logic Gate")
    print("  Why XOR? It is 'non-linearly separable'. A basic linear model")
    print("  (like Logistic Regression) cannot solve it. It requires a hidden")
    print("  layer and non-linear activation (Sigmoid) to warp the space.")
    print("=" * 65 + "\n")

    # 1. Dataset: XOR Truth Table
    # X = [Input A, Input B]
    # y = [A XOR B]
    X_train = [
        [0.0, 0.0],
        [0.0, 1.0],
        [1.0, 0.0],
        [1.0, 1.0]
    ]
    y_train = [
        [0.0],  # 0 XOR 0 = 0
        [1.0],  # 0 XOR 1 = 1
        [1.0],  # 1 XOR 0 = 1
        [0.0]   # 1 XOR 1 = 0
    ]

    # 2. Initialize Network
    # 2 Inputs, 4 Hidden Neurons, 1 Output
    nn = NeuralNetwork(input_nodes=2, hidden_nodes=4, output_nodes=1, learning_rate=0.2)

    print("[1] INITIAL STATE (Before Training - Random Weights)")
    print("-" * 50)
    for x, y in zip(X_train, y_train):
        prediction = nn.predict(x)[0]
        print(f"  Input: {x} | Target: {y[0]} | Prediction: {prediction:.4f}")
    
    print(f"  Initial MSE: {nn.calculate_mse(X_train, y_train):.6f}\n")
    time.sleep(1.0)

    # 3. Train the Network
    print("[2] TRAINING PHASE (Backpropagation in action)")
    print("-" * 50)
    
    epochs = 10000
    start_time = time.time()
    
    # We call train with verbose=True to see the MSE drop over time
    nn.train(X_train, y_train, epochs=epochs, verbose=True)
    
    elapsed = time.time() - start_time
    print(f"\n  Training completed in {elapsed:.2f} seconds.\n")
    time.sleep(1.0)

    # 4. Final Evaluation
    print("[3] FINAL STATE (After Training)")
    print("-" * 50)
    for x, y in zip(X_train, y_train):
        prediction = nn.predict(x)[0]
        # Round to 0 or 1 for final boolean answer
        boolean_answer = 1 if prediction > 0.5 else 0
        
        match = "PASS" if boolean_answer == int(y[0]) else "FAIL"
        print(f"  Input: {x} | Target: {y[0]} | Pred: {prediction:.4f} -> [{boolean_answer}] ({match})")


if __name__ == "__main__":
    run_xor_demo()
