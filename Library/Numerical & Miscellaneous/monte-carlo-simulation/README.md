# Monte Carlo Simulation Algorithm Library

Welcome to the **Monte Carlo Simulation** implementation for the Numeric & Miscellaneous Algorithm Library.

## Overview

The **Monte Carlo Method** relies on repeated random sampling to arrive at numerical results. It is famously used to estimate the probability of outcomes in processes that are difficult or mathematically impossible to predict deterministically due to the intervention of random variables. 

This implementation provides a clear, documented, and fully tested Python suite showcasing three specific domain applications of the algorithm:
1. **Numerical Integration:** Estimating the mathematical constant Pi ($\pi$).
2. **Stochastic Processes:** Simulating independent 1D Random Walks.
3. **Quantitative Finance:** Simulating expected future stock prices using Geometric Brownian Motion (GBM).

## File Structure

The project is structured into three main directories:

- **`core/`**: Contains the core Python implementation.
  - `monte_carlo_simulation.py`: The executable class providing Monte Carlo methods and a beautifully formatted CLI runner demonstration.
- **`docs/`**: Contains theoretical definitions and complexity analysis.
  - `Logic.md`: Explains the underlying probabilistic math (Law of Large Numbers, Central Limit Theorem) and outlines the logic of each use case.
  - `Complexity.md`: Discusses the unique $\mathcal{O}(\frac{1}{\sqrt{N}})$ Error Convergence Rate and explains why the algorithm completely ignores the "Curse of Dimensionality".
- **`test-project/`**: Contains the unit test suite.
  - `test_monte_carlo_simulation.py`: Exhaustive `unittest` suite validating boundaries, statistical logic, error bounds, and expected values using seeded and unseeded deterministic assertions.

---

## How it Works

The beauty of the Monte Carlo algorithm lies in its brute-force reliance on the Law of Large Numbers. Consider the Pi Estimation logic:
1. Imagine an inscribed circle of radius $r=1$ inside a square of side $2$.
2. The area ratio of the circle to the square is exactly $\frac{\pi}{4}$.
3. We generate $N$ random $(x, y)$ coordinate darts uniformly distributed within the square.
4. By using the Pythagorean theorem, we count how many darts land inside the circle ($x^2 + y^2 \leq 1$).
5. Multiply the ratio by 4, and as $N \to \infty$, the estimate beautifully converges precisely on $\pi$.

---

## Quick Start & Usage

### 1. Running the Core Example

The `core/monte_carlo_simulation.py` file includes a runnable example demonstrating all three simulations.

```bash
python3 "Library/Numaric & Miscellaneous/monte-carlo-simulation/core/monte_carlo_simulation.py"
```

**Expected Output:**
```
=== Monte Carlo Simulations ===

1. Estimating Pi with 1,000,000 samples...
   Estimated Pi : 3.141972
   Actual Pi    : 3.141592653589793
   Error        : 0.000379

2. Simulating 1D Random Walk (1000 steps, 5000 simulations)...
   Average Final Position : 0.692 (Expected ~0)
   Average Distance       : 25.045 (Theoretical ~25.231)

3. Simulating Asset Prices (GBM)
   S0=$100.0, Return=8.0%, Volatility=20.0%, Horizon=1.0yr, 10000 sims...
   Simulated Expected Price : $108.57
   Theoretical Expected Price: $108.33
   Max Price observed       : $361.64
   Min Price observed       : $31.81
```

### 2. Using the Module

You can easily incorporate these scalable methods into larger statistical and financial modeling applications.

```python
from core.monte_carlo_simulation import MonteCarloSimulator

# Predict Expected Business Revenue paths over 30 days
paths = MonteCarloSimulator.simulate_asset_price_paths(
    S0=50000, 
    mu=0.15, 
    sigma=0.30, 
    time_horizon_years=1.0, 
    time_steps=30, 
    num_simulations=50_000
)

print(MonteCarloSimulator.expected_asset_price(paths))
```

---

## Testing

The project is highly tested. The test suite uses seeded randomness where appropriate to assert that the simulated standard error bounds properly hug theoretical deterministic constants.

**Run the tests using standard `unittest` module:**

```bash
python3 -m unittest "Library/Numaric & Miscellaneous/monte-carlo-simulation/test-project/test_monte_carlo_simulation.py"
```

---

## Algorithmic Limitations

While Monte Carlo elegantly bypassed the *Curse of Dimensionality* (making it the de-facto algorithm for highly complex multi-dimensional probabilistic modeling), its fatal flaw is the **Convergence Rate**.

Due to the Central Limit Theorem, the standard error decreases only by the square root of $N$. Meaning to get an extra decimal point of accuracy (i.e. reduce error by 10x), you must run **100 times** as many simulations. This makes brute-force Monte Carlo incredibly computationally expensive when strict accuracy is mechanically required.
