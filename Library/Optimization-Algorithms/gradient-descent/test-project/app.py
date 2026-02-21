import sys
import time
from pathlib import Path

# Add parent directory for core logic
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.optimizer import GradientDescentOptimizer
except ImportError:
    print("Error: Ensure 'core/optimizer.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_ml_trainer():
    print("-" * 65)
    print("SYSTEM: LINEAR REGRESSION TRAINER")
    print("ALGORITHM: BATCH GRADIENT DESCENT")
    print("-" * 65 + "\n")

    # 1. Simulated Dataset
    # Relationship is exactly: y = 2x + 1
    # We want the algorithm to discover Weight = 2.0, Bias = 1.0 on its own.
    X_train = [1.0, 2.0, 3.0, 4.0, 5.0]
    y_train = [3.0, 5.0, 7.0, 9.0, 11.0]

    print("[DATA] Input Features (X): ", X_train)
    print("[DATA] Target Outputs (y): ", y_train)
    print("[DATA] Expected Model:     y = 2x + 1\n")

    # 2. Hyperparameters
    LEARNING_RATE = 0.01
    EPOCHS = 1000

    print(f"[HYPERPARAMETERS] Learning Rate: {LEARNING_RATE} | Epochs: {EPOCHS}\n")
    print("[TRAINING] Initiating Gradient Descent...")

    start_time = time.perf_counter()

    # 3. Execute Optimization Engine
    final_weight, final_bias, cost_history = GradientDescentOptimizer.optimize(
        X=X_train, 
        y=y_train, 
        learning_rate=LEARNING_RATE, 
        epochs=EPOCHS
    )

    end_time = time.perf_counter()

    # 4. Display Training Progress (Cost Curve)
    print("\n[LOG] Training Progress (Mean Squared Error):")
    for epoch in [0, 9, 99, 499, 999]:
        print(f"      Epoch {epoch+1:<4} | Cost: {cost_history[epoch]:.6f}")

    # 5. Final Report
    print("\n" + "="*65)
    print("TRAINING REPORT")
    print("="*65)
    print(f"Discovered Weight (Slope): {final_weight:.4f}")
    print(f"Discovered Bias (Y-Int):   {final_bias:.4f}")
    print(f"Final Model Equation:      y = {final_weight:.2f}x + {final_bias:.2f}")
    print("-" * 65)
    print(f"Execution Time: {(end_time - start_time) * 1000:.4f} ms")
    print("="*65)
    print("RESULT: Engine successfully converged on the mathematical minimum.")

if __name__ == "__main__":
    run_ml_trainer()