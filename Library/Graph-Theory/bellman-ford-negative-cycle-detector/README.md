# Bellman-Ford Algorithm: Negative Cycle Detection & Arbitrage Finder

## 1. Overview

The **Bellman-Ford Algorithm** is a fundamental graph algorithm that computes shortest paths from a single source vertex to all other vertices in a weighted directed graph. Unlike Dijkstra's algorithm, Bellman-Ford can handle graphs with **negative edge weights** and can detect the presence of **negative-weight cycles**.

This capability makes it essential for financial arbitrage detection, network routing with penalties, and any system where costs can be negative.

---

## 2. Key Engineering Features

* **Negative Weight Support:** Unlike Dijkstra, Bellman-Ford correctly handles negative edge weights.
* **Negative Cycle Detection:** Identifies when a negative-weight cycle exists, which would allow infinite cost reduction.
* **Dynamic Programming Approach:** Uses iterative edge relaxation to guarantee optimal solutions.
* **Path Reconstruction:** Includes predecessor tracking for full path recovery.
* **Versatile Applications:** Currency arbitrage, network delay with penalties, game theory optimization.

---

## 3. Folder Architecture

```text
.
├── core/                      # Algorithm Implementation
│   └── bellman_ford.py        # Main algorithm with cycle detection
├── docs/                      # Technical Documentation
│   ├── logic.md               # Algorithm explanation and DP approach
│   └── complexity.md          # Performance analysis vs Dijkstra
├── test-project/              # Real-World Simulation
│   ├── app.py                 # Currency arbitrage detector
│   ├── instructions.md        # User guide
│   └── exchange_rates.txt     # Sample currency exchange data
└── README.md                  # Module Entry Point (Current File)
```

---

## 4. Performance Benchmarks

| Operation | Complexity | Efficiency Note |
|-----------|-----------|-----------------|
| **Time Complexity** | O(V × E) | V iterations, each checking E edges |
| **Space Complexity** | O(V) | Stores distances and predecessors |
| **Best for** | Graphs with negative weights | Required when negatives exist |
| **Cycle Detection** | O(E) | Additional edge check after main loop |

**Comparison with Dijkstra:**
- Dijkstra: O(E log V) - Faster but fails with negative weights
- Bellman-Ford: O(V × E) - Slower but handles all cases

---

## 5. Quick Start

### Installation

```python
# No external dependencies required - uses standard Python typing
from core.bellman_ford import bellman_ford, detect_negative_cycle_nodes
```

### Basic Usage

```python
# Define a graph with negative weights
graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', -3), ('D', 2)],
    'C': [('D', 3)],
    'D': []
}

# Calculate shortest paths from node 'A'
distances, predecessors, has_cycle = bellman_ford(graph, 'A')

if has_cycle:
    print("⚠️ Negative cycle detected!")
else:
    print(f"Shortest distance to D: {distances['D']}")
```

---

## 6. Real-World Applications

### 6.1 Currency Arbitrage Detection

**Scenario:** A trader wants to detect arbitrage opportunities across currency exchanges where conversion rates create a "negative cycle" (profit loop).

Example: USD → EUR → GBP → USD with rates creating profit.

### 6.2 Network Routing with Penalties

**Scenario:** Some network links have "penalties" (negative weights) for preferred routing, while others have costs.

### 6.3 Game Theory & Reward Systems

**Scenario:** In game development, certain paths may give rewards (negative costs), and you need to find optimal routes considering both costs and rewards.

---

## 7. How It Works

### The Algorithm in 3 Steps:

1. **Initialize:** Set source distance to 0, all others to infinity
2. **Relax Edges:** For |V| - 1 iterations, update distances if a shorter path is found
3. **Detect Cycles:** Run one more iteration - if any distance improves, a negative cycle exists

### Why |V| - 1 Iterations?

In a graph with V vertices, the longest simple path has at most V - 1 edges. Each iteration guarantees finding paths of length ≤ i edges. Therefore, V - 1 iterations guarantee finding all shortest paths.

---

## 8. Test Project: Currency Arbitrage Detector

The included test project simulates a real-world foreign exchange market where you can:

- Load currency exchange rates
- Detect arbitrage opportunities (negative cycles)
- Calculate optimal conversion paths
- Add custom currency pairs

Run the simulation:

```bash
cd test-project
python app.py
```

---

## 9. When to Use Bellman-Ford vs Dijkstra

| Factor | Bellman-Ford | Dijkstra |
|--------|-------------|----------|
| **Negative Weights** | ✅ Supported | ❌ Fails |
| **Speed** | O(V × E) | O(E log V) ⚡ |
| **Cycle Detection** | ✅ Built-in | ❌ Not applicable |
| **Use Case** | Finance, penalties | Navigation, costs |

**Rule of Thumb:** Use Dijkstra unless you have negative weights or need cycle detection.

---

## 10. Advanced Features

### Negative Cycle Identification

```python
from core.bellman_ford import detect_negative_cycle_nodes

cycle_nodes = detect_negative_cycle_nodes(graph, 'A')
if cycle_nodes:
    print(f"Negative cycle found: {' → '.join(cycle_nodes)}")
```

### Path Reconstruction

```python
from core.bellman_ford import reconstruct_path

path = reconstruct_path(predecessors, 'A', 'D')
print(f"Optimal path: {' → '.join(path)}")
```

---

## 11. License

MIT License - See root LICENSE file.

---

## 12. References

* Bellman, R. (1958). "On a routing problem". Quarterly of Applied Mathematics.
* Ford, L. R.; Fulkerson, D. R. (1962). Flows in Networks.
* Cormen, T. H., et al. (2009). "Introduction to Algorithms" (3rd ed.), Chapter 24.
