# Complexity Analysis: Particle Swarm Optimisation

PSO is an iterative, population-based algorithm. Its complexity is governed by the size of the swarm and the number of iterations — both chosen by the engineer as hyperparameters.

---

## 1. Time Complexity

| Factor | Symbol | Description |
|---|---|---|
| Swarm size | **N** | Number of particles |
| Iterations | **T** | Number of velocity/position update cycles |
| Objective evaluation | **C** | Cost of evaluating f(x) once (e.g. O(d) for Rastrigin) |
| Dimensions | **d** | Dimension of the search space |
| **Total Time Complexity** | **O(N · T · (d + C))** | One velocity update (O(d)) + one evaluation (O(C)) per particle per iteration |

### Concrete Example

For the Rastrigin benchmark (`C = O(d)`) with a 10-dimensional search space:
- N = 30 particles, T = 200 iterations, d = 10
- Total evaluations: 30 × 200 = **6,000 function calls**
- Per call: O(10) = constant
- **Effective total: O(60,000)** — runs in milliseconds

---

## 2. Space Complexity

| Component | Complexity | Description |
|---|---|---|
| All particle positions | **O(N · d)** | One d-dimensional position vector per particle |
| All particle velocities | **O(N · d)** | One d-dimensional velocity vector per particle |
| Personal bests | **O(N · d)** | One d-dimensional p_best per particle |
| Global best | **O(d)** | Single shared position vector |
| Cost history | **O(T)** | One float per iteration for the convergence log |
| **Total Space Complexity** | **O(N · d + T)** | Dominated by the swarm's position/velocity matrices |

---

## 3. Hyperparameter Sensitivity

### 3.1 Swarm Size (N)

| N | Behaviour | Typical Use |
|---|---|---|
| 10–20 | Fast but may miss valleys on complex surfaces | Low-dimensional, quick prototyping |
| 30–50 | **Recommended default** — good balance of coverage and speed | Most practical problems |
| 100+ | Thorough global exploration; expensive per iteration | High-dimensional or critical production problems |

> **Rule of thumb:** N ≈ 10 + 2√d (Clerc, 2006) provides a dimensionality-aware swarm size.

### 3.2 Inertia Weight (ω)

| ω | Effect |
|---|---|
| 0.9–1.2 | Strong momentum → broad exploration, slow convergence |
| **0.729** | **Classic Shi/Eberhart value** — theoretical convergence guarantee |
| 0.4–0.6 | Rapid local search → risk of premature convergence |

### 3.3 Cognitive & Social Coefficients (c₁, c₂)

| Configuration | Behaviour |
|---|---|
| c₁ >> c₂ | Particles prioritise personal memory → slow to share discoveries |
| c₁ << c₂ | Swarm collapses to global best rapidly → high risk of premature convergence |
| **c₁ = c₂ ≈ 1.494** | **Clerc's constriction balance** — recommended for most problems |

---

## 4. Comparison vs. Other Optimisers

| Algorithm | Gradient Required? | Escapes Local Minima? | Complexity | Parallelisable? |
|---|---|---|---|---|
| Gradient Descent | ✅ Yes | ❌ No (non-convex) | O(T · d) | ❌ Sequential |
| Hill Climbing | ❌ No | ❌ No | O(T · C) | ❌ Sequential |
| Simulated Annealing | ❌ No | ✅ Yes (probabilistic) | O(K · I · C) | ❌ Sequential |
| **Particle Swarm** | ❌ No | ✅ Yes (swarm diversity) | O(N · T · C) | ✅ Yes (per-particle) |
| Genetic Algorithm | ❌ No | ✅ Yes | O(G · P · C) | ✅ Yes (per-individual) |

> **Key insight:** PSO's main advantage over Simulated Annealing is **natural parallelism** — all N particle evaluations in each iteration are completely independent and can be computed simultaneously on multi-core hardware, making real-world wall-clock time far lower than the sequential complexity formula suggests.

---

## 5. Convergence Behaviour

### 5.1 Early Phase (iterations 1–~30% of T)
- Swarm is spread across the bounds
- Global best improves rapidly as particles discover better regions
- Cost curve drops steeply

### 5.2 Mid Phase (~30–70% of T)
- Particles begin converging toward the current global best
- Occasional "jumps" as a distant particle finds a superior valley
- Cost curve flattens with periodic step improvements

### 5.3 Late Phase (~70–100% of T)
- Swarm has largely collapsed around the global best region
- Fine-grained local refinement dominates
- Cost curve is nearly flat — further improvement is marginal

---

## 6. Engineering Constraints

- **No Gradient Required:** PSO operates purely on function evaluations — it works on discontinuous, non-differentiable, noisy, and black-box objective functions where gradient-based methods fail entirely.
- **Premature Convergence:** The classic risk. The swarm can collapse around a local minimum if the social component (c₂) is too high or if the landscape has a very dominant but suboptimal basin. Countermeasures: lower c₂, increase N, or add velocity clamping.
- **Discretisation:** Standard PSO is defined for continuous spaces. Discrete variants (binary PSO, integer PSO) use modified velocity and position update rules.
- **Reproducibility:** Because r₁ and r₂ are stochastic, results vary between runs. Always pass a `seed` when reproducibility is needed for testing or benchmarking.
- **Stagnation Detection:** Advanced practitioners monitor whether g_best has improved in the last K iterations and re-initialise the swarm if stagnation is detected — a technique called *restart PSO*.
