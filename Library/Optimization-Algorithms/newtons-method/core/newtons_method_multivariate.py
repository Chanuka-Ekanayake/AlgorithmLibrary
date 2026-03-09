"""
Multivariate Newton's Method implementation.

This module provides the tools to solve systems of non-linear equations
and optimize multivariable functions using Newton's method. 
It operates using pure Python lists without relying on external libraries like NumPy.

Contents:
- `compute_jacobian`: Finite differences approximation for the Jacobian matrix.
- `compute_hessian`: Finite differences approximation for the Hessian matrix.
- `gaussian_elimination_solve`: Solves a linear system Ax = b.
- `newtons_method_multivariate`: Solves a system of equations F(x) = 0.
- `newtons_method_multivariate_optimization`: Finds a local minimum of a scalar function.
"""

import math
from typing import List, Callable, Optional, Tuple
import logging

# Basic logging configuration for the module
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Type aliases for enhanced readability
Vector = List[float]
Matrix = List[List[float]]


def _add_vectors(u: Vector, v: Vector) -> Vector:
    """Adds two vectors component-wise."""
    return [ui + vi for ui, vi in zip(u, v)]


def _subtract_vectors(u: Vector, v: Vector) -> Vector:
    """Subtracts vector v from vector u component-wise."""
    return [ui - vi for ui, vi in zip(u, v)]


def _scalar_multiply(c: float, v: Vector) -> Vector:
    """Multiplies vector v by a scalar c."""
    return [c * vi for vi in v]


def _vector_norm(v: Vector) -> float:
    """Computes the Euclidean norm of a vector."""
    return math.sqrt(sum(vi ** 2 for vi in v))


def gaussian_elimination_solve(A: Matrix, b: Vector) -> Vector:
    """
    Solves the linear system Ax = b using Gaussian elimination with partial pivoting.
    
    Args:
        A: A square n x n matrix of floats.
        b: A column vector of length n.
        
    Returns:
        Vector x such that Ax = b.
        
    Raises:
        ValueError: If A is singular or not square.
    """
    n = len(A)
    if n == 0 or len(A[0]) != n:
        raise ValueError("Matrix A must be square and non-empty.")
    
    # Create augmented matrix [A | b]
    aug = [row[:] + [b[i]] for i, row in enumerate(A)]
    
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i + 1, n):
            if abs(aug[k][i]) > abs(aug[max_row][i]):
                max_row = k
                
        if abs(aug[max_row][i]) < 1e-12:
            raise ValueError(f"Matrix is singular or nearly singular at row {i}.")
            
        # Swap rows for numerical stability
        aug[i], aug[max_row] = aug[max_row], aug[i]
        
        # Eliminate below
        for k in range(i + 1, n):
            factor = aug[k][i] / aug[i][i]
            for j in range(i, n + 1):
                aug[k][j] -= factor * aug[i][j]
                
    # Back substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = sum(aug[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (aug[i][n] - s) / aug[i][i]
        
    return x


def compute_jacobian(
    F: Callable[[Vector], Vector],
    x: Vector,
    h: float = 1e-5
) -> Matrix:
    """
    Approximate the Jacobian matrix of a vector-valued function F at point x 
    using forward finite differences.
    
    Args:
        F: A function taking a vector of length n and returning a vector of length m.
        x: The evaluation point (length n).
        h: The step size for numerical differentiation.
        
    Returns:
        An m x n Jacobian matrix.
    """
    n = len(x)
    fx = F(x)
    m = len(fx)
    
    # Initialize an m x n matrix with zeros
    J = [[0.0 for _ in range(n)] for _ in range(m)]
    
    for j in range(n):
        # Compute partial derivative w.r.t x_j
        x_plus = x[:]
        x_plus[j] += h
        
        fx_plus = F(x_plus)
        for i in range(m):
            J[i][j] = (fx_plus[i] - fx[i]) / h
            
    return J


def compute_hessian(
    f: Callable[[Vector], float],
    x: Vector,
    h: float = 1e-5
) -> Matrix:
    """
    Approximate the Hessian matrix of a scalar-valued function f at point x 
    using central finite differences.
    
    Args:
        f: A function taking a vector of length n and returning a float.
        x: The evaluation point (length n).
        h: The step size for numerical differentiation.
        
    Returns:
        An n x n Hessian matrix.
    """
    n = len(x)
    H = [[0.0 for _ in range(n)] for _ in range(n)]
    
    fx = f(x)
    
    for i in range(n):
        for j in range(n):
            if i == j:
                # Diagonal elements (second partial with respect to same variable)
                x_plus = x[:]
                x_plus[i] += h
                x_minus = x[:]
                x_minus[i] -= h
                H[i][i] = (f(x_plus) - 2 * fx + f(x_minus)) / (h ** 2)
            else:
                # Off-diagonal elements (mixed partial derivatives)
                x_pp = x[:]
                x_pp[i] += h
                x_pp[j] += h
                
                x_pm = x[:]
                x_pm[i] += h
                x_pm[j] -= h
                
                x_mp = x[:]
                x_mp[i] -= h
                x_mp[j] += h
                
                x_mm = x[:]
                x_mm[i] -= h
                x_mm[j] -= h
                
                H[i][j] = (f(x_pp) - f(x_pm) - f(x_mp) + f(x_mm)) / (4 * h ** 2)
                
    return H


def newtons_method_multivariate(
    F: Callable[[Vector], Vector],
    x0: Vector,
    J: Optional[Callable[[Vector], Matrix]] = None,
    tol: float = 1e-7,
    max_iter: int = 100,
    verbose: bool = False
) -> Tuple[Vector, int, bool]:
    """
    Multivariate Newton's Method for solving systems of non-linear equations F(x) = 0.
    
    Args:
        F: Vector-valued function representing the system of equations.
        x0: Initial guess (length n).
        J: Optional function returning the Jacobian matrix at x. If None, 
           numerical approximation is used.
        tol: Tolerance for convergence based on the norm of F(x) or step size.
        max_iter: Maximum number of iterations allowed.
        verbose: If True, prints iteration tracking.
        
    Returns:
        Tuple containing the estimated root vector, the number of iterations used, 
        and a boolean flag indicating whether the algorithm converged.
    """
    x_n = x0[:]
    
    for i in range(max_iter):
        Fx_n = F(x_n)
        
        # Check standard convergence based on function output norm
        if _vector_norm(Fx_n) < tol:
            if verbose:
                logger.info(f"Root found at iteration {i}, |F|={_vector_norm(Fx_n):.2e}")
            return x_n, i, True
            
        # Determine Jacobian
        if J is not None:
            Jx_n = J(x_n)
        else:
            Jx_n = compute_jacobian(F, x_n)
            
        try:
            # We want to solve J * dx = -F
            neg_Fx_n = _scalar_multiply(-1.0, Fx_n)
            dx = gaussian_elimination_solve(Jx_n, neg_Fx_n)
        except ValueError as e:
            if verbose:
                logger.warning(f"Failed to solve linear system at iteration {i}: {e}")
            return x_n, i, False
            
        # Apply Newton update step
        x_next = _add_vectors(x_n, dx)
        
        # Check convergence based on the update step size
        if _vector_norm(dx) < tol:
            if verbose:
                logger.info(f"Converged on step size at iteration {i}")
            return x_next, i + 1, True
            
        x_n = x_next
        
    if verbose:
        logger.warning(f"Failed to converge after {max_iter} iterations.")
        
    return x_n, max_iter, False
