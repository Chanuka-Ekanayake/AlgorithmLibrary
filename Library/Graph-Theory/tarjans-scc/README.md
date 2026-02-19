# Tarjan's SCC — Strongly Connected Components Finder

## Overview
Tarjan's Algorithm identifies all **Strongly Connected Components (SCCs)** in a
directed graph in a single DFS pass. An SCC is a maximal set of vertices where
every vertex can reach every other vertex. It is one of the most elegant and
efficient graph algorithms, running in optimal **O(V + E)** time.

## Problem Statement
Given a directed graph, find all groups of vertices where every vertex is
reachable from every other vertex in that group.

**Key insight**: SCCs reveal hidden cyclical structure in directed graphs — from
circular service dependencies to mutual social relationships.

## Real-World Applications

### 1. Microservice Architecture 🏗️
**Problem**: Detect circular service dependencies in distributed systems
- Find services that must be deployed together (they form a cycle)
- Identify tight coupling that should be refactored
- **Used in**: DevOps pipelines, Docker/Kubernetes deploy ordering

### 2. Social Network Analysis 👥
**Problem**: Discover mutual-influence communities
- Find groups where everyone follows everyone else
- Identify tightly-knit cliques vs peripheral users
- **Used in**: Facebook, LinkedIn, Twitter recommendation engines

### 3. Compiler Design 🖥️
**Problem**: Detect recursive function/variable cycles
- Identify mutually recursive functions for optimization
- Detect infinite dependency loops at compile time
- **Used in**: GCC, LLVM, language interpreters

### 4. Deadlock Detection 🔒
**Problem**: Find deadlocks in resource allocation graphs
- An SCC of size > 1 signals a potential deadlock
- **Used in**: Operating systems, database transaction managers

### 5. Web Crawling & Link Analysis 🌐
**Problem**: Find groups of mutually-linking web pages
- PageRank treats SCCs specially for rank computation
- **Used in**: Google Search, web archiving tools

## Algorithm: Tarjan's (1972)

### Core Concepts
- Use DFS and assign each vertex a **discovery time** (`disc`) and a **low value** (`low`)
- Maintain a **stack** of currently active vertices
- A vertex `v` is an **SCC root** when `low[v] == disc[v]`
- When a root is detected, pop the stack to collect the full SCC

### Key Properties
- **Single DFS pass** — only visits each vertex and edge once
- **Produces SCCs in reverse topological order** of the condensation DAG
- **Iterative implementation** — avoids Python recursion limits on large graphs

## Features
- ✅ **Optimal O(V + E)** time complexity
- ✅ **Single DFS pass** — no graph transposition needed
- ✅ **Iterative DFS** — works on large graphs without hitting Python recursion limits
- ✅ **Named vertex support** — work with meaningful labels, not just indices
- ✅ **Full connectivity analysis** — trivial vs non-trivial SCCs, is_strongly_connected flag
- ✅ **5 real-world scenarios** included in test-project

## Time Complexity
- **O(V + E)** — optimal, every vertex and edge visited once

## Space Complexity
- **O(V + E)** — for graph storage, disc/low arrays, and stack

## Project Structure
```
tarjans-scc/
├── core/
│   └── tarjans_scc.py        # Algorithm implementation
├── docs/
│   ├── logic.md              # Step-by-step algorithm walkthrough
│   └── complexity.md         # Time & space analysis + benchmarks
├── test-project/
│   ├── app.py                # 5 real-world demonstrations
│   └── instructions.md       # How to run
└── README.md                 # This file
```

## Quick Start

### No installation required — standard library only.

```bash
cd test-project
python app.py
```

### Basic Usage (index-based)
```python
from core.tarjans_scc import TarjansSCC

g = TarjansSCC(4)
g.add_edge(0, 1)
g.add_edge(1, 2)
g.add_edge(2, 0)   # cycle: 0 → 1 → 2 → 0
g.add_edge(2, 3)

sccs = g.find_sccs()
print(sccs)  # [[3], [0, 1, 2]]
```

### Named Vertices
```python
from core.tarjans_scc import find_sccs_with_names

nodes = ["Auth", "User", "Order", "Payment"]
edges = [
    ("Auth",    "User"),
    ("User",    "Order"),
    ("Order",   "Payment"),
    ("Payment", "Order"),  # cycle!
]

sccs = find_sccs_with_names(nodes, edges)
print(sccs)
# [['Order', 'Payment'], ['User'], ['Auth']]
```

### Full Connectivity Analysis
```python
from core.tarjans_scc import analyze_graph_connectivity

result = analyze_graph_connectivity(nodes, edges)
print(result["is_strongly_connected"])   # False
print(result["non_trivial_sccs"])        # [['Order', 'Payment']]
print(result["num_sccs"])                # 3
```

## Example Output

```
============================================================
  MICROSERVICE ARCHITECTURE — Circular Dependency Detector
============================================================

📦 Services: 8  |  Calls: 10
🔍 Strongly Connected? False

📊 Strongly Connected Components (6 found):

  ✅  SCC 1: [API-Gateway]
  ✅  SCC 2: [Auth-Service]
  ✅  SCC 3: [User-Service]
  🔁  SCC 4: [Order-Service ↔ Payment-Service]
  ✅  SCC 5: [Inventory-Service]
  🔁  SCC 6: [Analytics-Service ↔ Notification-Service]

⚠️  CIRCULAR DEPENDENCIES DETECTED:
   → Order-Service ↔ Payment-Service
   → Analytics-Service ↔ Notification-Service

💡 Recommendation: Refactor to break cycles using an event bus or
   shared library to decouple these services.
```

## Key Concepts

### Strongly Connected Component (SCC)
A maximal group where every vertex can reach every other vertex.

**Visual Example:**
```
A → B → C
↑       |
└───────┘
All three form one SCC (every vertex can reach every other)

A → B → C → D
        ↑   |
        └───┘
SCCs: {A}, {B}, {C, D}
```

## When to Use

✅ **Use Tarjan's When:**
- Looking for circular dependencies (services, modules, tasks)
- Detecting deadlocks in resource allocation
- Finding communities in directed social graphs
- Compressing a directed graph into its condensation DAG

❌ **Don't Use When:**
- Graph is undirected (use Articulation Points instead)
- You only need one SCC check — use simple DFS reachability
- Graph changes frequently (consider online SCC algorithms)

## Comparison with Alternatives

| Algorithm | Passes | Needs Transposition | SCCs in Topo Order |
|-----------|--------|--------------------|--------------------|
| **Tarjan's (this)** | **1** | **No** | **Yes** |
| Kosaraju's | 2 | Yes | Partial |
| Naive | V | No | No |

## Contributing
Follow the existing structure when adding examples or optimizations.

## Related Algorithms
- **Topological Sort**: Valid only on DAG (condensation of SCC graph)
- **Articulation Points**: Undirected equivalent of SCC analysis
- **Kosaraju's Algorithm**: Alternative SCC algorithm (2 DFS passes)
- **Dijkstra / Bellman-Ford**: Shortest paths within an SCC

## References
- [Tarjan 1972 — Original Paper](https://epubs.siam.org/doi/10.1137/0201010)
- [Introduction to Algorithms (CLRS), Chapter 22](https://mitpress.mit.edu/books/introduction-algorithms)
- [Tarjan's SCC — Wikipedia](https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm)

## License
See root repository LICENSE file.
