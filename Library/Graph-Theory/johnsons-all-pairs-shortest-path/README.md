# Johnson's Algorithm — All-Pairs Shortest Path

## Overview

Johnson's Algorithm solves the **All-Pairs Shortest Path (APSP)** problem on
**sparse weighted directed graphs**, including those with **negative edge weights**
(but no negative cycles). It combines two classic algorithms into a 3-phase approach:

| Phase | Algorithm Used | Purpose |
|-------|---------------|---------|
| 1 | **Bellman-Ford** | Compute reweighting potentials h[v] |
| 2 | Edge reweighting | Transform all weights to ≥ 0 |
| 3 | **Dijkstra × V** | Compute shortest paths from every vertex |

This elegant combination preserves shortest-path correctness while unlocking the
efficiency of Dijkstra's greedy approach — even in graphs with negative edges.

---

## Problem Statement

Given a weighted directed graph G = (V, E) with possibly negative edge weights
(but no negative cycles), find the shortest path between **every pair** of vertices.

- ✅ Handles **negative edge weights**
- ✅ Handles **sparse graphs** efficiently
- ✅ Detects **negative cycles** and raises an error
- ✅ Full **path reconstruction** for any pair

---

## Real-World Applications

### 1. Transport Network Planning 🚌
Government subsidised routes exist as negative-cost edges.
Johnson's finds the cheapest end-to-end travel cost across all city pairs.

### 2. Financial Arbitrage Detection 💱
Currency exchange rates converted to −log(rate).
A negative cycle = arbitrage opportunity (profit through circular exchange).
**Used in:** Trading systems, forex risk management.

### 3. Build System Optimization ⚙️
Software dependencies with caching shortcuts (negative = time saved).
Find the fastest compilation order for every module pair.
**Used in:** CI/CD pipelines (Bazel, Buck, Gradle).

### 4. Network Routing with SLA Credits 🌐
Some transit nodes offer bandwidth credits (negative cost hops).
Johnson's finds optimal routing tables for all node pairs.
**Used in:** SDN controllers, ISP routing optimization.

### 5. Game AI Navigation 🎮
Terrain with bonuses (negative cost cells) and penalties.
Precompute movement costs between all points of interest.
**Used in:** Strategy games, pathfinding engines.

---

## Algorithm Phases

### Phase 1 — Reweighting via Bellman-Ford

Add virtual vertex `s` with 0-weight edges to all vertices.
Run Bellman-Ford from `s` → yields potential h[v] = dist(s, v).

### Phase 2 — Edge Reweighting

Transform every edge weight:
```
w'(u, v) = w(u, v) + h[u] − h[v]   ≥ 0   always
```
This removes all negative edges while preserving shortest-path ordering.

### Phase 3 — V × Dijkstra + Unweighting

Run Dijkstra from every vertex on the reweighted graph.
Recover true distances: `dist(u,v) = d'(u,v) − h[u] + h[v]`

---

## Time & Space Complexity

| Graph Type | Time | vs Floyd-Warshall |
|------------|------|-------------------|
| **Sparse (E ≈ V)** | **O(V² log V)** | ✅ V/log V times faster |
| Moderately dense | O(VE log V) | — |
| Dense (E ≈ V²) | O(V³ log V) | ❌ Slower |

**Space:** O(V²) for the all-pairs distance and next-node matrices.

**Use Johnson's when:** Sparse graph + negative weights + need all pairs.

---

## Project Structure

```
johnsons-all-pairs-shortest-path/
├── core/
│   └── johnsons.py           # Full algorithm + utilities
├── docs/
│   ├── logic.md              # Reweighting math, walkthrough, pseudocode
│   └── complexity.md         # Phase-by-phase O() analysis + benchmarks
├── test-project/
│   ├── app.py                # 5 real-world scenario demos
│   └── instructions.md       # How to run
└── README.md                 # This file
```

---

## Quick Start

```bash
# No installation required — Python 3.8+ standard library only
cd test-project
python app.py
```

### Basic Usage

```python
from core.johnsons import johnsons, reconstruct_path

graph = {
    'A': {'B': 3,  'C': 8},
    'B': {'C': -4, 'D': 1},
    'C': {'D': 7},
    'D': {'A': 2},
}

distances, next_node = johnsons(graph)

# Shortest distance A → C
print(distances[('A', 'C')])    # -1

# The actual path
path = reconstruct_path(next_node, 'A', 'C')
print(' → '.join(path))         # A → B → C
```

### Negative Cycle Detection

```python
from core.johnsons import detect_negative_cycle

graph = {
    'X': {'Y': -1},
    'Y': {'Z': -1},
    'Z': {'X': -1},  # Negative cycle!
}

if detect_negative_cycle(graph):
    print("⚠️ Negative cycle detected — no valid shortest paths.")
```

### All Paths from One Source

```python
from core.johnsons import find_all_shortest_paths_from

results = find_all_shortest_paths_from(graph, 'A')
for dest, (dist, path) in results.items():
    print(f"A → {dest}: {dist}  via  {' → '.join(path or [])}")
```

---

## Example Output

```
══════════════════════════════════════════════════════════════════════════
  INTERCITY TRANSPORT NETWORK  —  Johnson's Algorithm
══════════════════════════════════════════════════════════════════════════

  Cities: Athens, Berlin, Cairo, Dublin, Edinburgh, Frankfurt
  Routes: 10
  Includes subsidised route: Berlin → Cairo (−€30)

  📊 All-pairs cheapest travel cost matrix (€):

            Athens  Berlin   Cairo  Dublin  Edinburgh  Frankfurt
  Athens│      0.0   120.0    80.0   120.0      210.0      270.0
  Berlin│      ∞       0.0   -30.0    20.0      110.0      170.0
  ...

  📍 Sample cheapest routes:
    Athens → Edinburgh: €210  via  Athens → Berlin → Cairo → Dublin → Edinburgh
    Berlin → Frankfurt: €170  via  Berlin → Cairo → Dublin → Edinburgh → Frankfurt
```

---

## API Reference

| Function | Description |
|----------|-------------|
| `johnsons(graph)` | Full APSP — returns `(distances, next_node)` |
| `reconstruct_path(next_node, src, dst)` | Returns ordered path list |
| `detect_negative_cycle(graph)` | Returns `True` if negative cycle exists |
| `get_distance_matrix(graph)` | Distances only (no path data) |
| `find_all_shortest_paths_from(graph, source)` | Single-source all destinations |
| `get_graph_diameter(graph)` | Longest shortest path in graph |
| `get_graph_center(graph)` | Vertex minimising max distance to others |

---

## When to Use Johnson's

✅ **Use when:**
- Graph is **sparse** (E much smaller than V²)
- **Negative edge weights** exist
- Need **all-pairs** results
- V > 300 (where Floyd-Warshall cubic cost is too high)

❌ **Don't use when:**
- Graph is **dense** → Floyd-Warshall is simpler and faster
- Weights are all **positive** + single source → plain Dijkstra
- **Negative cycle** present → no valid APSP possible

---

## Algorithm Comparison

| Algorithm | Time | Space | Negative Weights | Best For |
|-----------|------|-------|-----------------|---------|
| **Johnson's (this)** | **O(V² log V + VE)** | O(V²) | ✅ | **Sparse graphs** |
| Floyd-Warshall | O(V³) | O(V²) | ✅ | Dense graphs |
| Dijkstra (×V) | O(VE log V) | O(V) | ❌ | Sparse, positive only |
| Bellman-Ford (×V) | O(V²E) | O(V) | ✅ | Rarely preferred |

---

## Related Algorithms in This Library

| Algorithm | Folder | Relationship |
|-----------|--------|-------------|
| **Bellman-Ford** | `bellman-ford-negative-cycle-detector` | Used as Phase 1 of Johnson's |
| **Dijkstra** | `dijkstra-delivery-optimizer` | Used as Phase 3 of Johnson's |
| **Floyd-Warshall** | `floyd-warshall-all-pairs-shortest-path` | Solves same problem; better for dense graphs |

---

## References

- Johnson, D. B. (1977). *"Efficient algorithms for shortest paths in sparse networks."*
  Journal of the ACM, 24(1), 1–13.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.), Chapter 25.3.
- [Johnson's Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Johnson%27s_algorithm)

---

## License

See root repository LICENSE file.
