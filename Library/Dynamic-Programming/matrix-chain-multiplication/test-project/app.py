import sys
import os

# Add the parent directory to the Python path to import from core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.optimizer import MatrixChainOptimizer

def main():
    print("=== Matrix Chain Multiplication Optimizer ===")
    
    # Example dimensions:
    # A1: 30x35
    # A2: 35x15
    # A3: 15x5
    # A4: 5x10
    # A5: 10x20
    # A6: 20x25
    
    dimensions = [30, 35, 15, 5, 10, 20, 25]
    print(f"Matrix dimensions array: {dimensions}")
    print(f"Number of matrices: {len(dimensions) - 1}")
    
    min_ops, parens = MatrixChainOptimizer.optimize_multiplication_order(dimensions)
    
    print("\nResults:")
    print(f"Minimum Scalar Multiplications: {min_ops}")
    print(f"Optimal Parenthesization:       {parens}")
    print("=============================================")

if __name__ == "__main__":
    main()
