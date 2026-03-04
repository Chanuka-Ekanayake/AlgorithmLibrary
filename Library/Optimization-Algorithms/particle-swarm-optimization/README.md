# Particle Swarm Optimisation

## 1. Overview

**Particle Swarm Optimisation (PSO)** is a population-based metaheuristic that finds global minima of continuous objective functions by simulating the collective intelligence of a bird flock or fish school. Introduced by Kennedy & Eberhart in 1995, it remains one of the most widely deployed evolutionary computation algorithms in engineering, finance, and machine learning.

Its defining property is **swarm diversity**: unlike single-trajectory optimisers (Gradient Descent, Simulated Annealing), PSO evaluates dozens of candidate solutions in parallel, dramatically reducing the risk of entrapment in any single local minimum.

The classic demonstration domain is the **Rastrigin Function** — a highly multimodal surface with hundreds of local minima — where gradient-based methods immediate fail and single-point heuristics frequently get stuck.

---

## 2. Technical Features

- **Velocity Update Equation:** Each particle's movement is governed by three balanced forces — inertia (momentum), cognitive pull (personal best), and social pull (global best) — implemented via the canonical Kennedy & Eberhart velocity formula.
- **Clerc Constriction Coefficients:** Ships with the theoretically-derived hyperparameter values (ω = 0.729, c₁ = c₂ = 1.494) proven to guarantee convergence on well-behaved functions.
- **Swarm Initialisation:** Particles are scattered uniformly at random across the search bounds; initial velocities are set to half the per-dimension range to prevent immediate boundary collisions.
- **Bound Clamping:** Particle positions are hard-clamped to the feasible region after every update, enforcing the constraint that all evaluations remain within the defined search space.
- **Personal Best Tracking:** Each particle independently maintains its own historical best position, providing the cognitive memory that prevents the swarm from collapsing prematurely.
- **Three Built-in Benchmarks:** Ships with Sphere (convex sanity check), Rosenbrock (banana-valley challenge), and Rastrigin (multimodal stress test) as plug-in objective functions.
- **Reproducibility:** Accepts an optional `seed` parameter for the internal RNG, enabling bitwise-identical runs for testing and benchmarking.

---

## 3. Architecture

```text
.
├── core/                    # Optimisation Engine
│   ├── __init__.py          # Package initialisation
│   └── pso.py               # Particle, ParticleSwarmOptimizer, benchmark fns
├── docs/                    # Technical Documentation
│   ├── logic.md             # Swarm structure, velocity equations, theory
│   └── complexity.md        # Runtime analysis, hyperparameter sensitivity
├── test-project/            # Benchmark Suite
│   ├── app.py               # Sphere, Rosenbrock, Rastrigin benchmarks
│   └── instructions.md      # Hyperparameter experimentation guide
└── README.md                # Documentation Entry Point
```

---

## 4. Performance Specifications

| Metric | Specification |
|---|---|
| **Time Complexity** | O(N · T · (d + C)), where N = swarm size, T = iterations, d = dimensions, C = objective cost |
| **Space Complexity** | O(N · d + T), dominated by the swarm's position and velocity matrices |
| **Optimisation Target** | Minimises any scalar objective function — no gradient required |
| **Parallelism** | All N particle evaluations per iteration are fully independent — trivially parallelisable |
| **Failure Risk** | Premature convergence if social coefficient is too high or swarm is too small |

---

## 5. Deployment & Usage

### Integration

```python
from core.pso import ParticleSwarmOptimizer

DIMENSIONS = 10
BOUNDS = [(-5.12, 5.12)] * DIMENSIONS

optimizer = ParticleSwarmOptimizer(
    objective_fn    = ParticleSwarmOptimizer.rastrigin,
    dimensions      = DIMENSIONS,
    bounds          = BOUNDS,
    num_particles   = 30,
    max_iterations  = 200,
    inertia         = 0.729,
    cognitive_coeff = 1.494,
    social_coeff    = 1.494,
    seed            = 42,
)

best_position, best_cost, cost_history = optimizer.optimize()
print(f"Global best cost: {best_cost:.6f}")
print(f"Global best position: {best_position}")
```

### Custom Objective Function

```python
def my_function(position):
    # Any callable that takes a list[float] and returns a float
    return sum((x - 3.0) ** 2 for x in position)   # minimum at (3, 3, ..., 3)

optimizer = ParticleSwarmOptimizer(
    objective_fn = my_function,
    dimensions   = 5,
    bounds       = [(0.0, 10.0)] * 5,
    seed         = 0,
)
best_pos, best_cost, _ = optimizer.optimize()
```

### Running the Benchmark Suite

```bash
cd test-project
python app.py
```

---

## 6. Industrial Applications

- **Hyperparameter Tuning:** Search neural network architectures, learning rates, and regularisation coefficients without requiring gradient information through the training pipeline.
- **Antenna Design:** NASA and commercial telecoms use PSO to optimise antenna geometry for gain and bandwidth — a high-dimensional, evaluation-expensive problem with no closed-form gradient.
- **Power Systems:** Optimal power flow problems in electrical grids — minimise transmission loss subject to voltage, current, and generator constraints.
- **Financial Portfolio Optimisation:** Allocate capital across assets to maximise the Sharpe ratio — a noisy, non-differentiable objective unsuitable for gradient descent.
- **Robotics Path Planning:** Find minimum-energy trajectories in cluttered environments modelled as high-dimensional cost landscapes.
