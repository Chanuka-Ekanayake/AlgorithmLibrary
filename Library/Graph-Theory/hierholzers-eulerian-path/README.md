# Hierholzer's Algorithm — Eulerian Path & Circuit Finder

## Overview
Hierholzer's Algorithm finds an **Eulerian Path** or **Eulerian Circuit** in a
graph — a traversal that visits every **edge** exactly once. It extends Euler's
famous 1736 solution to the Königsberg Bridge Problem, which founded graph theory.
Runs in optimal **O(V + E)** time using an iterative stack-based approach.

## Problem Statement
Given a graph, find a walk that uses every edge exactly once:
- **Eulerian Circuit**: Starts and ends at the same vertex
- **Eulerian Path**: Starts and ends at different vertices

## Real-World Applications

### 1. Delivery & Logistics Route Planning 🚚
**Problem**: Cover every street / delivery stop exactly once to minimize fuel
- Find a circuit that returns to depot after covering all routes
- **Used in**: FedEx, UPS, waste collection, street sweepers

### 2. Network Infrastructure Inspection 🔌
**Problem**: Inspect every cable link in a network with minimum revisits
- **Used in**: Telecom maintenance, power grid audits

### 3. DNA Sequence Assembly 🧬
**Problem**: Reconstruct a DNA strand from short k-mer fragments
- Eulerian path through the De Bruijn graph reconstructs the sequence
- **Used in**: Genome sequencing (Illumina, Oxford Nanopore pipelines)

### 4. Pen-Drawing / Puzzle Solving ✏️
**Problem**: Can a figure be drawn without lifting the pen?
- If graph has Eulerian path/circuit → YES
- **Used in**: Puzzle games, VLSI circuit routing

### 5. Graph Theory Foundation 🎓
**Problem**: The historic Königsberg Bridge Problem (1736)
- Showed that no Eulerian path or circuit exists when more than two vertices have odd degree (as in the Königsberg graph, which has four)
- **Used in**: Teaching graph theory, algorithm courses

## Algorithm: Hierholzer's (1873)

### Core Idea
1. Start at the correct vertex (path start or any vertex for circuit)
2. Follow edges greedily until stuck (no more unused edges)
3. Back-track to last vertex with unused edges
4. Insert new sub-circuit into existing result
5. Repeat until all edges are used

### Existence Conditions
| Graph Type | Circuit | Path |
|------------|---------|------|
| Directed | All: `out = in` | One: `out−in=+1`, one: `in−out=+1` |
| Undirected | All vertices: even degree | Exactly 2 vertices: odd degree |

## Features
- ✅ **Optimal O(V + E)** time complexity
- ✅ **Iterative DFS** — no Python recursion limits
- ✅ **Both directed and undirected** graphs supported
- ✅ **Auto-detects** circuit vs path vs impossible
- ✅ **Named vertex support** with `find_eulerian_path_with_names()`
- ✅ **Route planner utility** — `plan_route()` for real-world use
- ✅ **5 real-world scenarios** in test-project

## Time Complexity
- **O(V + E)** — optimal, must visit every vertex and edge

## Space Complexity
- **O(V + E)** — adjacency lists, stack, result path

## Project Structure
```
hierholzers-eulerian-path/
├── core/
│   └── hierholzers.py          # Algorithm implementation
├── docs/
│   ├── logic.md                # Step-by-step walkthrough
│   └── complexity.md           # Performance analysis
├── test-project/
│   ├── app.py                  # 5 real-world demonstrations
│   └── instructions.md         # How to run
└── README.md                   # This file
```

## Quick Start

### No installation required — standard library only.

```bash
cd test-project
python app.py
```

### Basic Usage (directed graph)
```python
from core.hierholzers import HierholzersEulerian

g = HierholzersEulerian(directed=True)
g.add_edge(0, 1)
g.add_edge(1, 2)
g.add_edge(2, 0)   # circuit: 0 → 1 → 2 → 0
g.add_edge(0, 3)
g.add_edge(3, 0)

info = g.get_path_info()
print(info["type"])   # 'circuit'
print(info["path"])   # [0, 1, 2, 0, 3, 0]
```

### Named Vertices
```python
from core.hierholzers import find_eulerian_path_with_names

nodes = ["Depot", "A", "B", "C"]
edges = [("Depot", "A"), ("A", "B"), ("B", "C"), ("C", "Depot")]

info = find_eulerian_path_with_names(nodes, edges, directed=True)
print(info["path"])   # ['Depot', 'A', 'B', 'C', 'Depot']
```

### Route Planner
```python
from core.hierholzers import plan_route

locations = ["Warehouse", "Stop-A", "Stop-B", "Stop-C"]
roads = [("Warehouse", "Stop-A"), ("Stop-A", "Stop-B"),
         ("Stop-B", "Stop-C"), ("Stop-C", "Warehouse")]

result = plan_route(locations, roads, directed=True)
print(result["summary"])
print(result["route"])
```

## Example Output

```
==============================================================
  DELIVERY VAN — Cover Every Street Exactly Once
==============================================================

  📦 Locations : 6
  🛣️  Roads     : 8
  🔍 Feasible  : True
  📝 Type      : Circuit

  📍 Optimal Delivery Route:
     Depot → Zone-A → Zone-B → Zone-C → Zone-A → Zone-D → Zone-E → Zone-B → Depot

  💡 ✅ Perfect circuit — return to start after covering all routes.

==============================================================
  KÖNIGSBERG BRIDGE PROBLEM — Euler's Original (1736)
==============================================================

  🏛️  Landmasses : North, South, East, Island
  🌉 Bridges    : 7

  Has Eulerian Circuit : False
  Has Eulerian Path    : False

  ❌ RESULT: It is IMPOSSIBLE to cross every bridge exactly once.
     Euler proved this in 1736 — the birth of Graph Theory! 🎓
```

## Key Concepts

### Eulerian Path vs Circuit
```
Circuit: A → B → C → A         (returns to start, every edge once)
Path:    A → B → C → D         (different start and end)
```

### Degree Conditions (Undirected)
```
Even degree = can pass through (enter and exit)
Odd degree  = must be an endpoint (start or finish)
Exactly 2 odd-degree vertices → Eulerian Path exists
0 odd-degree vertices → Eulerian Circuit exists
```

## When to Use

✅ **Use Hierholzer's When:**
- Need to cover every edge exactly once (roads, cables, links)
- Solving pen-drawing / one-stroke puzzles
- Reconstructing sequences from overlapping fragments
- Finding delivery circuits that return to origin

❌ **Don't Use When:**
- Need to visit every **vertex** (not edge) — use Hamiltonian Path / TSP
- Graph doesn't meet Eulerian conditions — no path exists
- Dynamic graph where edges change frequently

## Comparison with Alternatives

| Algorithm | Time | Notes |
|-----------|------|-------|
| **Hierholzer's (this)** | **O(V + E)** | Optimal, iterative |
| Fleury's Algorithm | O(E²) | Much slower, not practical |
| Brute Force | O(E!) | Completely impractical |

## Related Algorithms
- **Hamiltonian Path**: Visit every *vertex* (not edge) once — NP-complete
- **Topological Sort**: Order a DAG — related DFS-based technique
- **Tarjan's SCC**: Find strongly connected components (required for Eulerian check)
- **Dijkstra**: Shortest path between vertices

## References
- [Hierholzer 1873 — Original Paper](https://link.springer.com/article/10.1007/BF01442866)
- [Euler Paths — Wikipedia](https://en.wikipedia.org/wiki/Eulerian_path)
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms)

## License
See root repository LICENSE file.
