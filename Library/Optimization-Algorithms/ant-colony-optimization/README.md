# Ant Colony Optimization (ACO)

## 1. Overview

**Ant Colony Optimization (ACO)** is a probabilistic technique for solving computational problems which can be reduced to finding good paths through graphs. It is inspired by the behavior of ants in finding paths from the colony to food.

In the real world, ants wander randomly, and upon finding food return to their colony while laying down pheromone trails. If other ants find such a path, they are likely not to keep traveling at random, but to instead follow the trail, returning and reinforcing it if they eventually find food. 

In ACO, artificial ants build solutions to optimization problems and exchange information on their quality via a communication scheme that is reminiscent of the one adopted by real ants. The classic demonstration domain is the **Traveling Salesman Problem (TSP)**: given $N$ cities, find the shortest closed tour that visits every city exactly once.

---

## 2. Technical Features

- **Pheromone-based learning:** Retains memory of good edges in the graph using a global "pheromone" matrix ($O(n^2)$ space for $n$ cities).
- **Heuristic visibility:** Ants do not walk blindly; they combine pheromone trails ($\tau$) with an inverse-distance heuristic ($\eta$) to pick the next step intuitively.
- **Evaporation:** Prevents premature convergence to local optima. Pheromone values fade over time, allowing the colony to gradually "forget" bad initial trails and explore broader search spaces.
- **Global Deposit:** In this simple variant (Ant System), ants drop pheromones globally after all have finished touring, in proportion to the quality (inverse length) of their tours.

---

## 3. Architecture

```text
.
├── core/                   # Optimisation Engine
│   ├── __init__.py
│   └── aco.py              # Transition rules, pheromone updates
├── docs/                   # Technical Documentation
│   ├── logic.md            # Theory of ant selection and pheromones
│   └── complexity.md       # Runtime analysis and hyperparameter tuning
├── test-project/           # TSP Route Optimisation Simulator
│   ├── app.py              # Visual/CLI evaluation of the algorithm on city graphs
│   └── instructions.md     # Hyperparameter simulation guide
└── README.md               # Documentation Entry Point
```

---

## 4. Performance Specifications

| Metric | Specification |
|---|---|
| **Time Complexity** | $O(N_i \cdot N_a \cdot N_c^2)$, where $N_i$ = iterations, $N_a$ = ants, $N_c$ = cities |
| **Space Complexity** | $O(N_c^2)$ to store the pheromone trails and distance matrix |
| **Optimisation Target** | Combinatorial problems equivalent to shortest paths on graphs |
| **Failure Risk** | Too high evaporation -> never converges. Too low evaporation -> early convergence to poor local optima. |

---

## 5. Deployment & Usage

### Integration

```python
from core.aco import AntColonyOptimizer

optimizer = AntColonyOptimizer(
    dist_matrix = my_distance_matrix,
    n_ants = 20,
    n_iterations = 100,
    alpha = 1.0,
    beta = 2.0,
    evaporation_rate = 0.5,
    q = 100
)

best_tour, best_length, cost_history = optimizer.optimize()
print(f"Shortest path found: {best_length}")
```

### Running the Simulator

```bash
cd test-project
python app.py
```

---

## 6. Industrial Applications

- **Logistics & Routing:** Finding optimum vehicle routing schedules for delivery networks under dynamic constraints.
- **Telecommunications:** Routing packets in heavily loaded communication networks intelligently.
- **Urban Transport:** Optimizing public transportation timetables and schedules.
- **Computational Biology:** Protein folding and sequence alignment.
