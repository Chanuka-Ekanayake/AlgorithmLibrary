# Johnson's Algorithm — Test Project

## How to Run

No installation required — uses Python standard library only.

```bash
cd test-project
python app.py
```

Requires **Python 3.8+**.

---

## What This Demo Does

The app walks you through **5 real-world scenarios** that showcase
Johnson's Algorithm for all-pairs shortest paths on graphs with
negative edge weights:

| # | Scenario | Real-World Use |
|---|----------|---------------|
| 1 | Intercity Transport Network | Government-subsidised routes (negative = subsidy) |
| 2 | Software Build Pipeline | Caching shortcuts that reduce build time |
| 3 | Currency Arbitrage Detector | Log-transformed exchange rates, negative cycle = profit loop |
| 4 | Airline Fuel Cost Optimizer | Stopovers with fuel credits |
| 5 | Manual Graph Builder | Build any graph and run Johnson's interactively |

---

## Project Structure

```
johnsons-all-pairs-shortest-path/
├── core/
│   └── johnsons.py          ← Algorithm implementation
├── docs/
│   ├── logic.md             ← Step-by-step explanation
│   └── complexity.md        ← O(V² log V + VE) analysis
├── test-project/
│   ├── app.py               ← This demo app
│   └── instructions.md      ← This file
└── README.md
```

---

## Importing the Core

```python
from core.johnsons import johnsons, reconstruct_path, detect_negative_cycle

graph = {
    'A': {'B': 4, 'C': 2},
    'B': {'C': -1, 'D': 5},
    'C': {'D': 8},
    'D': {},
}

distances, next_node = johnsons(graph)
print(distances[('A', 'D')])      # 9
print(reconstruct_path(next_node, 'A', 'D'))  # ['A', 'B', 'D']
```
