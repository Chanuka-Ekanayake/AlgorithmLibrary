"""
Newton's Method Algorithm Implementation

This module provides implementations for Newton's Method, a powerful root-finding algorithm
that produces successively better approximations to the roots (or zeroes) of a real-valued 
function. It is also highly effective for optimization (finding local minima/maxima) 
when applied to the derivative of the function.

Contents:
- `newtons_method_root`: Finds a root of the function f(x) = 0.
- `newtons_method_optimization`: Finds a local extremum by seeking a root of f'(x) = 0.
- Helper functions to compute numerical derivatives if not provided.

Reference:
https://en.wikipedia.org/wiki/Newton%27s_method
"""

import math
from typing import Callable, Tuple, Optional, Union
import logging


# Module-level logger; configuration is the responsibility of the calling application.
logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.addHandler(logging.NullHandler())


def compute_numerical_derivative(
    f: Callable[[float], float], 
    x: float, 
    h: float = 1e-5
) -> float:
    """
    Computes the numerical derivative of a single-variable function at point x 
    using the central difference formulation.
    
    Args:
        f: The function to differentiate.
        x: The point at which to evaluate the derivative.
        h: The step size for the central difference.

    Returns:
        The estimated derivative f'(x).
    """
    return (f(x + h) - f(x - h)) / (2 * h)


def compute_numerical_second_derivative(
    f: Callable[[float], float], 
    x: float, 
    h: float = 1e-5
) -> float:
    """
    Computes the numerical second derivative of a function at point x.
    
    Args:
        f: The function to differentiate twice.
        x: The point at which to evaluate the second derivative.
        h: The step size.

    Returns:
        The estimated second derivative f''(x).
    """
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)


def newtons_method_root(
    f: Callable[[float], float],
    f_prime: Optional[Callable[[float], float]] = None,
    x0: float = 0.0,
    tol: float = 1e-7,
    max_iter: int = 1000,
    verbose: bool = False
) -> Tuple[float, int, bool]:
    """
    Finds a root of the function f(x) = 0 using Newton's method.
    
    If the derivative f_prime is not provided, it will be estimated numerically.
    
    Args:
        f: Function for which we are finding the root.
        f_prime: Derivative of f. Optional. If None, numerical diff is used.
        x0: Initial guess for the root.
        tol: Tolerance for convergence. Stopping criterion is |x_{n+1} - x_n| < tol 
             or |f(x_n)| < tol.
        max_iter: Maximum number of iterations.
        verbose: If True, prints iteration details.

    Returns:
        Tuple containing:
        - The estimated root.
        - The number of iterations taken.
        - Boolean indicating whether it successfully converged.
    
    Raises:
        ZeroDivisionError: If the derivative becomes exactly zero during iteration.
    """
    x_n = x0
    
    for i in range(max_iter):
        fx_n = f(x_n)
        
        # Check standard convergence based on function value
        if abs(fx_n) < tol:
            if verbose:
                logger.info(f"Converged at iteration {i} with f(x)={fx_n:.2e}")
            return x_n, i, True
        
        # Compute derivative
        if f_prime is not None:
            dfx_n = f_prime(x_n)
        else:
            dfx_n = compute_numerical_derivative(f, x_n)
            
        if dfx_n == 0:
            if verbose:
                logger.warning(f"Derivative became zero at iteration {i}, x={x_n}")
            raise ZeroDivisionError(f"Derivative is zero at x = {x_n}. Method fails.")
            
        # Newton-Raphson update step
        x_next = x_n - fx_n / dfx_n
        
        # Check convergence based on step size
        step_size = abs(x_next - x_n)
        if step_size < tol:
            if verbose:
                logger.info(f"Converged at iteration {i} with step size={step_size:.2e}")
            return x_next, i + 1, True
            
        x_n = x_next
        
    if verbose:
        logger.warning(f"Failed to converge after {max_iter} iterations.")
        
    return x_n, max_iter, False


def newtons_method_optimization(
    f: Callable[[float], float],
    f_prime: Optional[Callable[[float], float]] = None,
    f_double_prime: Optional[Callable[[float], float]] = None,
    x0: float = 0.0,
    tol: float = 1e-7,
    max_iter: int = 1000,
    verbose: bool = False
) -> Tuple[float, int, bool]:
    """
    Finds a local extremum of the function f by finding the root of f'(x) = 0.
    
    Args:
        f: Primary scalar function to optimize.
        f_prime: First derivative of f. If None, evaluated numerically.
        f_double_prime: Second derivative of f. If None, evaluated numerically.
        x0: Initial guess for the extremum.
        tol: Tolerance for convergence based on step size or |f'(x)|.
        max_iter: Maximum permitted iterations.
        verbose: Toggle for iteration tracking.
        
    Returns:
        Tuple containing estimated extremum point, number of iterations, 
        and convergence flag.
    """
    x_n = x0
    
    for i in range(max_iter):
        # Determine f'(x_n)
        if f_prime is not None:
            df_n = f_prime(x_n)
        else:
            df_n = compute_numerical_derivative(f, x_n)
            
        # Check convergence: slope near zero means we are at an extremum or saddle point
        if abs(df_n) < tol:
            if verbose:
                logger.info(f"Optimization converged at iteration {i}, f'(x)={df_n:.2e}")
            return x_n, i, True
            
        # Determine f''(x_n)
        if f_double_prime is not None:
            ddf_n = f_double_prime(x_n)
        else:
            ddf_n = compute_numerical_second_derivative(f, x_n)
            
        if ddf_n == 0:
            if verbose:
                logger.warning(f"Second derivative became zero at iteration {i}, x={x_n}")
            raise ZeroDivisionError(f"Second derivative is zero at x = {x_n}.")
            
        # Update step (finding root of first derivative)
        x_next = x_n - df_n / ddf_n
        
        step_size = abs(x_next - x_n)
        if step_size < tol:
            if verbose:
                logger.info(f"Optimization converged at iteration {i} (step size={step_size:.2e})")
            return x_next, i + 1, True
            
        x_n = x_next
        
    if verbose:
        logger.warning(f"Optimization failed to converge after {max_iter} iterations.")
        
    return x_n, max_iter, False


def newtons_method(*args, **kwargs):
    """
    Alias for newtons_method_root to maintain backward compatibility 
    or to use the default standard approach.
    """
    return newtons_method_root(*args, **kwargs)
