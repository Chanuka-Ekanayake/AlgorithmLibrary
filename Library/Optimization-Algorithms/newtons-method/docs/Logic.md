# Logic Behind Newton's Method

Newton’s Method (also widely known as the Newton-Raphson method) is an iterative numerical algorithm designed to find successively better approximations to the roots (or zeroes) of a real-valued function. By leveraging the principles of calculus, it achieves rapid convergence, often quadratically, when the initial guess is sufficiently close to the true root.

This document systematically details the mathematical derivation, geometric interpretations, and algorithmic design underlying both the single-variable and multivariable implementations of Newton's Method.

---

## 1. Geometric Interpretation and Derivation

### 1.1 The Tangent Line Approximation
The core intuition behind Newton's Method is that a continuous and differentiable function $f(x)$ can be closely approximated by its tangent line in the immediate vicinity of a given point $x_n$.

Suppose we have a current approximation $x_n$ for the root of the function. The equation of the tangent line to the curve $y = f(x)$ at the point $(x_n, f(x_n))$ is given by the point-slope form:
$$ y - f(x_n) = f'(x_n) \cdot (x - x_n) $$

We want to find where this tangent line intersects the x-axis, as this intersection point often provides a better approximation of the function's actual root than our current guess $x_n$. To do this, we set $y = 0$ and solve for $x$:
$$ 0 - f(x_n) = f'(x_n) \cdot (x - x_n) $$

Isolating $x$ yields our next iteration point, $x_{n+1}$:
$$ x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)} $$

### 1.2 Iterative Refinement
This process is repeated to generate a sequence of approximations $\{x_n\}$:
1. Evaluate $f(x_n)$ and the derivative $f'(x_n)$.
2. Compute the next guess $x_{n+1} = x_n - f(x_n) / f'(x_n)$.
3. Check for convergence by verifying if $|x_{n+1} - x_n| < \epsilon$ (step size tolerance) or $|f(x_n)| < \epsilon$ (function value tolerance).
4. If the conditions are met, $x_{n+1}$ is declared the root.

---

## 2. Using Newton's Method for Optimization

Newton's Method is not restricted merely to root-finding; it is equally powerful as an optimization algorithm. According to Fermat's theorem, local extrema (minima or maxima) of a differentiable function occur at critical points where the first derivative is zero ($f'(x) = 0$).

Therefore, optimizing a function $g(x)$ is mathematically equivalent to finding the roots of its derivative, $f(x) = g'(x)$. Substituting this into the standard Newton's equation yields the optimization update rule:
$$ x_{n+1} = x_n - \frac{g'(x_n)}{g''(x_n)} $$

Here, $g''(x_n)$ represents the second derivative (or curvature) of the function. This update step geometrically fits a parabola to the local curvature of the function at $x_n$ and jumps directly to the vertex of that parabola.

---

## 3. Extension to Multivariable Systems

In many practical applications, we don't just have one variable, but an entire system of non-linear equations to solve simultaneously. 

### 3.1 The Multivariable Root-Finding Problem
Let $\mathbf{F}(\mathbf{x}) = \mathbf{0}$ represent a system of $n$ equations with $n$ variables. Here, $\mathbf{x}$ is a vector $[x_1, x_2, \dots, x_n]^T$ and $\mathbf{F}$ is a vector-valued function.

The standard single-variable derivative $f'(x)$ is replaced by the Jacobian matrix $\mathbf{J}(\mathbf{x})$, which contains all first-order partial derivatives:
$$ \mathbf{J}_{ij} = \frac{\partial F_i}{\partial x_j} $$

The update rule generalizes directly to:
$$ \mathbf{x}_{n+1} = \mathbf{x}_n - \mathbf{J}(\mathbf{x}_n)^{-1} \mathbf{F}(\mathbf{x}_n) $$

### 3.2 Solving the Linear System
Matrix inversion ($\mathbf{J}^{-1}$) is computationally expensive and numerically unstable. Instead of explicitly computing the inverse, we restructure the equation into a generalized linear system:
$$ \mathbf{J}(\mathbf{x}_n) \Delta\mathbf{x} = -\mathbf{F}(\mathbf{x}_n) $$

We solve for the update vector $\Delta\mathbf{x}$ using standard linear algebra techniques such as Gaussian Elimination or LU Decomposition. Once $\Delta\mathbf{x}$ is found, the variables are updated:
$$ \mathbf{x}_{n+1} = \mathbf{x}_n + \Delta\mathbf{x} $$

---

## 4. Edge Cases and Mitigations

While Newton's Method exhibits remarkable speed, it is sensitive to several geometric edge cases and numerical pitfalls.

### 4.1 Zero Derivative (Singular Jacobian)
If $f'(x_n) = 0$, the tangent line becomes perfectly horizontal and will never intersect the x-axis. Mathematically, this causes a division by zero.
**Mitigation**: The algorithm explicitly checks for an exactly zero derivative and raises a `ZeroDivisionError` or halts the iteration gracefully before performing the division. In the multivariate case, this corresponds to checking if the Jacobian matrix is singular (determinant is zero).

### 4.2 Divergence and Oscillation
If the starting guess $x_0$ is too far from the actual root, the sequence may diverge towards infinity or enter an infinite loop oscillating between two points (e.g., $x_n$ and $x_{n+1}$).
**Mitigation**: A hard cap on the maximum number of iterations (`max_iter`) is enforced. If the algorithm does not converge within this limit, it returns the best available approximation with a `False` flag indicating non-convergence.

### 4.3 Missing Analytical Derivatives
Explicit mathematical formulas for derivatives are not always available or are too complex to code.
**Mitigation**: The implementation provides a structured fallback utilizing finite differences to compute numerical derivatives. For a small step size $h$:
$$ f'(x) \approx \frac{f(x+h) - f(x-h)}{2h} $$
While this introduces marginal truncation errors, it safely allows Newton's Method to operate smoothly as a black-box solver.

---

## 5. Summary

The logical foundation of Newton's method relies strictly on iterative geometric approximations utilizing localized curve data. Whether navigating flat local planes for optimization or multidimensional vector intersection tracking, its structural paradigm perfectly reflects a fundamental balance between extreme algorithmic speed and sensitivity to initial structural configurations.
