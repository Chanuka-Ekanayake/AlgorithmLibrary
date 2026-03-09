# Newton's Method

Newton's Method (also known as the Newton-Raphson method) is a powerful, widely-used, and highly famous numerical algorithm for finding successively better approximations to the roots (or zeroes) of a real-valued function. By applying the method to the derivative of a particular function, it can also be leveraged directly for optimization—finding local minima or maxima on complex curves.

This directory contains robust, pure Python implementations of Newton's Method for single-variable root finding, single-variable optimization, and multivariable systems of equations.

## Mathematical Outline

### 1. Root Finding (Single Variable)

Given a function $f(x)$ and an initial guess $x_0$, a better approximation $x_1$ is given by adjusting the point by drawing a tangent to the curve at the evaluation point:

$$
x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}
$$

The process is repeated iteratively until a sufficiently accurate value is reached and the system identifies stabilization (i.e., $|x_{n+1} - x_n| < \text{tolerance}$ or $|f(x_n)| < \text{tolerance}$).

### 2. Optimization (Single Variable)

To find a local minimum or maximum of a particular function $f(x)$, we search for the critical points by finding the roots of its derivative $f'(x) = 0$. Using Newton's Method, the iteration formula correspondingly becomes:

$$
x_{n+1} = x_n - \frac{f'(x_n)}{f''(x_n)}
$$

### 3. Multivariate Systems (Non-linear Equations)

For a system of non-linear equations $\mathbf{F}(\mathbf{x}) = \mathbf{0}$, the update rule uses the Jacobian matrix $\mathbf{J}$ instead of a single scalar derivative. The conceptual generalization is identical but generalized across an $n$-dimensional domain:

$$
\mathbf{x}_{n+1} = \mathbf{x}_n - \mathbf{J}^{-1}(\mathbf{x}_n) \mathbf{F}(\mathbf{x}_n)
$$

Computationally, instead of wastefully inverting the entirety of the Jacobian matrix, we solve the generalized linear system $\mathbf{J}(\mathbf{x}_n) \Delta \mathbf{x} = -\mathbf{F}(\mathbf{x}_n)$ for $\Delta \mathbf{x}$ using methods such as standard Gaussian elimination, and then update $\mathbf{x}_{n+1} = \mathbf{x}_n + \Delta \mathbf{x}$.

---

## Implementations Included

The directory and folder structure is organized meticulously as follows to partition different domains:

- `newtons_method.py`
  Contains standard implementations for 1D single-variable scenarios:
  - `newtons_method_root`: Solves mathematically for $f(x) = 0$.
  - `newtons_method_optimization`: Solves mathematically for $f'(x) = 0$.
  - Helper methods to numerically approximate the first and second derivatives if analytical derivatives aren't explicitly provided.

- `newtons_method_multivariate.py`
  Contains complex generalized algorithms for multi-dimensional vector functions:
  - `newtons_method_multivariate`: Solves vector-valued multi-equation systems $\mathbf{F}(\mathbf{x}) = \mathbf{0}$.
  - Custom pure Python Linear Algebra helpers (such as Gaussian Elimination pivot solvers, array Vector Norms, Matrix representation tracking).
  - Numerical approximation fallback architectures for both the Jacobian and Hessian matrices.

- `test_newtons_method.py`
  Comprehensive unified unit testing frameworks covering dangerous edge cases, typical standard paths, quadratic minimum optimizations, and multi-variable multidimensional equations.

---

## Complexity Analysis

### Time Complexity

- **Single Variable**: The algorithm has a theoretical **Quadratic Convergence** rate, meaning the number of correct accurate decimal digits approximately doubles with each sequential step, assuming the initial starting guess is sufficiently close enough to the true underlying root and the system derivative is non-zero at the target root.
  However, if runtime numerical differentiation and fallback logic is utilized, it might constrain standard operation towards linear or superlinear convergence. In standard structural form, each subsequent iterative step takes $O(1)$ functional evaluations.

- **Multivariate**: In an $n$-dimensional coordinate space, evaluating the explicit Jacobian analytically takes $O(n^2)$ time assuming functional independence. Solving the resultant linear system $\mathbf{J} \Delta\mathbf{x} = -\mathbf{F}$ explicitly takes $O(n^3)$ operations if naïve unoptimized Gaussian elimination is utilized. Therefore, each total step takes $O(n^3)$ numerical operations. An ad-hoc numerical Jacobian approximation fallback system takes an extra auxiliary $O(n)$ distinct scale evaluations of $\mathbf{F}$.

### Space Complexity

- **Single Variable**: $O(1)$ complexity, since only the single current numerical estimate $x_n$ and variables strictly related to iteration tolerance limits and sequence counts need to be tracked inside memory.
- **Multivariate**: $O(n^2)$ complexity is strictly required for adequately storing the $n \times n$ structural Jacobian square matrix layout and heavily augmented structural matrices fundamentally utilized when recursively solving the required standard linear equations.

---

## Standard Run Examples

### 1. Basic Single Variable Root Finding Search

If we want to efficiently find the square root of $9$, what we essentially need is to find the positive mathematical cross root of the function $f(x) = x^2 - 9$.

```python
from newtons_method import newtons_method_root

def f(x): return x**2 - 9
def df(x): return 2*x

root, iters, converged = newtons_method_root(f, df, x0=1.0)
print(f"Algorithm root approximation: {root}") # Standard Output: 3.0
```

### 2. Complex Multivariate System Root Finding

To cleanly solve the intersecting multi-domain system of equations:
- $x^2 + y^2 = 4$
- $x^2 - y = 1$

```python
from newtons_method_multivariate import newtons_method_multivariate

def F(v):
    x, y = v[0], v[1]
    return [
        x**2 + y**2 - 4.0,
        x**2 - y - 1.0
    ]

root, iters, converged = newtons_method_multivariate(F, [1.0, 1.0])
print(f"Intersection of functions calculated at: {root}") 
```

---

## Pros and Cons Evaluation

**Distinct Advantages**:
- A fundamentally exceedingly fast inherent characteristic relative speed of convergence (reaching the quadratic threshold).
- Highly generalized structural framework adapting reasonably seamlessly towards multivariable structural setups without changing the underlying mathematical theories significantly.
- Functions effectively utilized interchangeably for basic functional root-finding requirements alongside optimizing system limits.

**Distinct Limitations**:
- Inherently highly sensitive and reactive towards the original initial random evaluation guess $x_0$. If an explicitly given initial target $x_0$ is measured significantly far away from the true underlying root function value, the mathematical process may diverge completely destructively.
- The standard mechanism structurally necessitates directly computing the formal mathematical derivative corresponding exactly towards the initial arbitrary function. If explicit mathematical analytical derivatives are strictly impossible and computational runtime numerical differentiation is mandatorily utilized instead, the ultimate evaluation measurement precision and the systemic convergence rates might substantially suffer negatively.
- A critical mathematical flaw guarantees if the associated underlying calculated mathematical derivative ever evaluates functionally equivalently towards absolute $0$ dynamically during an active structural iteration, then the standard evaluation method completely fails internally immediately dynamically because of a devastating programmatic arithmetic division by zero (indicating structurally interacting with functionally a geometrically explicitly mathematically isolated explicitly flat horizontal curve region).
