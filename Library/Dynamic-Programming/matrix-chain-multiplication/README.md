# Matrix Chain Multiplication

This project implements the **Matrix Chain Multiplication** algorithm using a bottom-up Dynamic Programming approach to find the most efficient way to multiply an entire sequence of matrices. 

## Overview

The matrix chain multiplication problem is an optimization problem where we seek the optimal parenthesization of a sequence of matrices to minimize the total number of scalar multiplications required. 

This implementation provides:
- Calculation of the minimum number of scalar multiplications required.
- Reconstruction of the optimal parenthesization string.

## Structure

- `core/optimizer.py`: Contains the `MatrixChainOptimizer` class with the dynamic programming logic.
- `docs/logic.md`: Explanation of the dynamic programming approach and optimal substructure.
- `docs/complexity.md`: Detailed time and space complexity analysis.
- `test-project/`: A simple sample project to demonstrate how the core logic can be used.

## Usage

See the `test-project/` directory for an example of how to import and use the optimizer.
