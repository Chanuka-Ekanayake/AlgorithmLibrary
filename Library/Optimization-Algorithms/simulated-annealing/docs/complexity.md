# Complexity Analysis: Simulated Annealing

Unlike sorting or graph traversal algorithms with deterministic runtimes, Simulated Annealing's complexity is governed by its **cooling schedule** — the hyperparameters chosen by the engineer.

---

## 1. Time Complexity

| Factor | Symbol | Description |
|---|---|---|
| Temperature steps | **K** | Number of times the temperature is reduced until `T < min_temp` |
| Iterations per step | **I** | Candidate evaluations performed at each temperature level |
| Cost function evaluation | **C** | Cost of evaluating one candidate (e.g. O(n) for TSP tour length) |
| **Total Time Complexity** | **O(K · I · C)** | Scales linearly with the cooling budget and evaluation cost |

### Calculating K (Number of Temperature Steps)

Given geometric cooling `T_new = α × T`:

$$
K = \frac{\ln(T_{\min}) - \ln(T_{\text{init}})}{\ln(\alpha)}
\approx \frac{\ln(T_{\text{init}} / T_{\min})}{-\ln(\alpha)}
$$

For `T_init = 1000`, `T_min = 1e-8`, `α = 0.995`:

$$
K \approx \frac{\ln(10^{11})}{-\ln(0.995)} \approx \frac{25.3}{0.00501} \approx 5{,}050 \text{ steps}
$$

With `I = 100` iterations per step and a TSP cost of O(n):

$$
\text{Total} = 5{,}050 \times 100 \times O(n) = O(505{,}000 \cdot n)
$$

This is effectively **O(n)** per problem instance for fixed hyperparameters.

---

## 2. Space Complexity

| Component | Complexity | Description |
|---|---|---|
| Current solution | **O(n)** | A copy of the active candidate (e.g. city tour of n cities) |
| Best solution | **O(n)** | A separate copy tracking the global best found so far |
| Candidate (neighbour) | **O(n)** | Temporary copy generated each iteration |
| Cost history | **O(K)** | One float recorded per temperature step for convergence plots |
| **Total Space Complexity** | **O(n + K)** | Dominated by solution size and cooling budget |

---

## 3. Hyperparameter Sensitivity

### 3.1 Initial Temperature (T_init)

- **Too Low:** Algorithm starts already cold — behaves like a greedy hill-climber and immediately traps in a local minimum.
- **Too High:** Accepts almost every move at the beginning; effectively a random walk that wastes compute exploring the worst solutions.
- **Rule of Thumb:** Set T_init so that `P(accept) ≈ 0.8` for the *average* cost delta in your domain.

### 3.2 Cooling Rate (α)

| α | Cooling Speed | Quality | Compute Cost |
|---|---|---|---|
| 0.999 | Very slow | ⭐⭐⭐⭐⭐ | Very high |
| 0.995 | Moderate | ⭐⭐⭐⭐ | Moderate |
| 0.99  | Fast | ⭐⭐⭐ | Low |
| 0.90  | Very fast | ⭐⭐ | Very low |

### 3.3 Iterations Per Temperature (I)

Increasing `I` gives the algorithm more chances to find a good solution at each temperature level before cooling. This is especially useful when the neighbourhood function produces many rejections (low acceptance rate in late stages).

---

## 4. Comparison vs. Other Optimisers

| Algorithm | Escapes Local Minima? | Complexity | Guarantees Global Optimum? |
|---|---|---|---|
| Hill Climbing | ❌ No | O(K · C) | ❌ No |
| Gradient Descent | ❌ No (convex only) | O(E · N) | ✅ (convex) / ❌ (non-convex) |
| **Simulated Annealing** | ✅ Yes (probabilistic) | O(K · I · C) | ❌ No (but asymptotically yes) |
| Genetic Algorithm | ✅ Yes | O(G · P · C) | ❌ No |
| Brute Force (TSP) | ✅ Yes | O(n!) | ✅ Yes |

> **Key insight:** SA sacrifices the global optimality guarantee of brute force for a **tractable runtime**, and sacrifices the speed of hill climbing for **reliable escape from local minima**. This tradeoff is ideal for NP-hard problems where finding a near-optimal solution quickly is more valuable than finding the perfect solution slowly.

---

## 5. Engineering Constraints

- **No Gradient Required:** SA works on any problem where you can define a cost function and a neighbourhood move — including discrete, combinatorial, and non-differentiable domains where gradient-based methods fail entirely.
- **Reproducibility:** Because the algorithm relies on random sampling (Boltzmann rolls), results are non-deterministic by default. Always pass a `seed` when reproducibility is required for testing or benchmarking.
- **Reheating:** For multi-modal landscapes, advanced practitioners implement **reheating** — increasing the temperature mid-run when the algorithm appears stuck — to periodically refresh the exploration phase.
