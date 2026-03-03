# Simulated Annealing Optimizer

## 1. Overview

**Simulated Annealing (SA)** is a probabilistic metaheuristic that solves optimisation problems that are far too large or non-convex for exact methods. Unlike Gradient Descent — which demands a smooth, differentiable cost surface — SA works on *any* problem where you can compute a cost and generate a nearby alternative solution.

Its defining feature is controlled randomness: at high temperatures, the algorithm deliberately accepts worse solutions to explore broadly. As the temperature cools, it becomes increasingly selective, converging on the best region it has found. This mechanism lets SA escape the **local minima traps** that cripple greedy algorithms.

The classic demonstration domain is the **Travelling Salesman Problem (TSP)**: given N cities, find the shortest closed tour that visits every city exactly once.

---

## 2. Technical Features

- **Boltzmann Acceptance:** Probabilistically accepts worse solutions using `P = e^(-Δ/T)`, trading exploitation for exploration and escaping local minima in a principled way.
- **Geometric Cooling Schedule:** Temperature is reduced by a multiplicative factor (α) each step, giving engineers direct control over the quality-vs-speed tradeoff.
- **Configurable Neighbourhood:** The `neighbour_fn` is injected at construction time — making the engine domain-agnostic and reusable across TSP, scheduling, VLSI layout, and more.
- **2-opt TSP Move:** Ships with the industry-standard route mutation: reverse a random sub-segment of the tour to eliminate path crossings.
- **Best-Solution Tracking:** Maintains a separate `best_solution` alongside the `current_solution`, ensuring the global best is never overwritten by a probabilistically-accepted worse state.
- **Reproducibility:** Accepts an optional `seed` for the internal RNG, enabling deterministic runs for testing and benchmarking.

---

## 3. Architecture

```text
.
├── core/                   # Optimisation Engine
│   ├── __init__.py         # Package initialisation
│   └── annealer.py         # Boltzmann acceptance, cooling loop, TSP helpers
├── docs/                   # Technical Documentation
│   ├── logic.md            # Temperature, acceptance criterion, cooling theory
│   └── complexity.md       # Runtime analysis and hyperparameter sensitivity
├── test-project/           # TSP Route Optimisation Simulator
│   ├── app.py              # 10-city circular TSP with known optimal distance
│   └── instructions.md     # Hyperparameter experimentation guide
└── README.md               # Documentation Entry Point
```

---

## 4. Performance Specifications

| Metric | Specification |
|---|---|
| **Time Complexity** | O(K · I · C), where K = temperature steps, I = iterations/step, C = cost function evaluation |
| **Space Complexity** | O(n + K), where n = solution size, K = number of cooling steps |
| **Optimisation Target** | Minimises any scalar cost function (no gradient required) |
| **Failure Risk** | Premature convergence if cooling rate is too aggressive (α too small) |

---

## 5. Deployment & Usage

### Integration

```python
from core.annealer import SimulatedAnnealingOptimizer

optimizer = SimulatedAnnealingOptimizer(
    cost_fn              = SimulatedAnnealingOptimizer.tsp_cost,
    neighbour_fn         = SimulatedAnnealingOptimizer.tsp_neighbour,
    initial_temp         = 1000.0,
    cooling_rate         = 0.995,
    min_temp             = 1e-8,
    iterations_per_temp  = 100,
    seed                 = 42,
)

best_tour, best_cost, cost_history = optimizer.optimize(initial_tour)
print(f"Best tour distance found: {best_cost:.4f}")
```

### Running the Simulator

```bash
cd test-project
python app.py
```

---

## 6. Industrial Applications

- **Logistics & Routing:** Carrier networks (UPS, FedEx) use SA-inspired heuristics to solve vehicle routing problems with thousands of delivery stops.
- **VLSI Chip Design:** Placing millions of transistors on a silicon die to minimise wire length and heat density — a purely combinatorial problem with no gradient.
- **Job-Shop Scheduling:** Assigning tasks to machines in a factory to minimise makespan, subject to precedence constraints.
- **Protein Folding:** Exploring the astronomically large conformational space of protein structures to find minimum-energy configurations.
