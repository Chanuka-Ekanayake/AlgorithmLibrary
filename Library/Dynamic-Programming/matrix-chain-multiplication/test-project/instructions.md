# Test Project Instructions

This directory contains a sample script `app.py` that demonstrates how to use the `MatrixChainOptimizer` from the core algorithm library.

## Prerequisites

- Python 3.x installed on your system.

## Running the Example

1. Open your terminal.
2. Navigate to the `matrix-chain-multiplication` directory (or run it directly from there):
   ```bash
   cd path/to/matrix-chain-multiplication
   ```
3. Execute the Python script:
   ```bash
   python3 test-project/app.py
   ```

## Output

You should see an output similar to the following, showing the minimum number of scalar multiplications and the optimal parenthesization for the example dimension array:

```text
=== Matrix Chain Multiplication Optimizer ===
Matrix dimensions array: [30, 35, 15, 5, 10, 20, 25]
Number of matrices: 6

Results:
Minimum Scalar Multiplications: 15125
Optimal Parenthesization:       ((A1(A2A3))((A4A5)A6))
=============================================
```
