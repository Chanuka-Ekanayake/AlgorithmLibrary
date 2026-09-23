# Borůvka's Parallel MST Optimizer

## 1. Overview

**Borůvka's Algorithm** (also known as Sollin's Algorithm) is a greedy graph algorithm used to find the **Minimum Spanning Tree (MST)** of a weighted, undirected graph. It is the **oldest known MST algorithm**, proposed by Otakar Borůvka in 1926 — before Kruskal's (1956) and Prim's (1957).

Its unique strength is its **natural parallelism**: in each round, every connected component independently selects its cheapest outgoing edge, and all selected edges are merged simultaneously. This makes it the algorithm of choice for **distributed systems, GPU computing, and MapReduce frameworks**.

---

## 2. Technical Features

* **Component-Based Merging:** Works on entire components simultaneously rather than individual vertices or globally sorted edges.
* **Natural Parallelism:** Each component's cheapest-edge search is independent, enabling O(log V) parallel rounds.
* **Optimized Cycle Detection:** Uses a **Disjoint Set Union (DSU)** with **Path Compression** and **Union by Rank** for near-constant time operations.
* **Network Simulation:** Includes a `test-project` that calculates the optimal cabling route for a global data center network.
* **Scalability:** Efficiently handles large graphs with a time complexity of O(E log V).

---

## 3. Architecture

```text
.
├── core/                  # Engine Logic
│   ├── __init__.py        # Public API exports
│   └── boruvka.py         # DSU structure and Borůvka's implementation
├── docs/                  # Technical Documentation
│   ├── logic.md           # Deep dive into component merging and parallelism
│   └── complexity.md      # Analysis of round-based convergence
├── test-project/          # Network Simulator
│   ├── app.py             # Global Network Optimizer CLI
│   ├── network_data.json  # Geographic dataset of data center hubs
│   └── instructions.md    # Operation and testing guide
└── README.md              # Documentation Entry Point (Current File)
```

---

## 4. Performance Specifications

| Metric | Specification |
| --- | --- |
| **Time Complexity** | O(E log V) |
| **Space Complexity** | O(V + E) |
| **Parallel Rounds** | O(log V) |
| **Paradigm** | Greedy Algorithm (Component Merging) |
| **Sub-Structure** | Disjoint Set Union (DSU) |

---

## 5. Deployment & Usage

### Integration

The `boruvkas_mst` function can be integrated into any connectivity or clustering project:

```python
from core.boruvka import boruvkas_mst

# Define an undirected weighted graph
network = {
    'A': {'B': 4, 'H': 8},
    'B': {'A': 4, 'H': 11, 'C': 8},
    'C': {'B': 8, 'D': 7, 'F': 4},
    'D': {'C': 7, 'E': 9, 'F': 14},
    'E': {'D': 9, 'F': 10},
    'F': {'E': 10, 'D': 14, 'C': 4, 'G': 2},
    'G': {'F': 2, 'H': 1},
    'H': {'A': 8, 'B': 11, 'G': 1},
}

mst, total_cost = boruvkas_mst(network)
# Result: MST with minimum total cost of 37
```

### Running the Simulator

To execute the Global Network Cost Optimization:

1. Navigate to the `test-project` directory:
```bash
cd test-project
```

2. Run the application:
```bash
python app.py
```

---

## 6. How It Works — The 3 Phases

Unlike Prim's (grow one tree) or Kruskal's (sort all edges), Borůvka's works in **rounds**:

### Phase 1: Initialize
Treat every vertex as its own isolated component (a "forest" of single nodes).

### Phase 2: Find Cheapest Edges (Parallelizable)
For **each** component, find the minimum-weight edge that connects it to a **different** component. All components do this independently — this is where parallelism shines.

### Phase 3: Merge Components
Add all cheapest edges to the MST and merge the connected components. The number of components **at least halves** each round.

**Repeat** Phases 2-3 until only one component remains. This takes at most **O(log V) rounds**.

---

## 7. Comparison: Borůvka's vs Kruskal's vs Prim's

| Feature | Borůvka's | Kruskal's | Prim's |
| --- | --- | --- | --- |
| **Year** | 1926 | 1956 | 1957 |
| **Strategy** | Component merging | Global edge sort | Vertex growth |
| **Data Structure** | DSU | DSU | Priority Queue |
| **Time Complexity** | O(E log V) | O(E log E) | O(E log V) |
| **Parallelism** | ✅ Natural (O(log V) rounds) | ❌ Sequential | ❌ Sequential |
| **Best For** | Parallel/Distributed systems | Sparse graphs | Dense graphs |

---

## 8. Industrial Applications

* **Distributed Computing:** Natural fit for MapReduce-based MST computation on massive graphs (e.g., social networks, web graphs).
* **GPU Computing:** Each component's cheapest-edge search maps directly to GPU thread blocks.
* **Telecommunications:** Designing backbone fiber networks where regional teams can independently identify optimal local connections.
* **Cluster Analysis:** Parallel hierarchical clustering for large-scale machine learning datasets.
* **Power Grid Design:** Distributed planning of transmission networks across multiple geographic regions.

---

## 9. Visual Example

```
Round 0: Each vertex is its own component
    A ─4─ B          Components: {A}, {B}, {C}, {D}, {E}
    |     |
    8     8          Each component picks its cheapest edge:
    |     |            A → B (4)    B → A (4)
    H ─1─ G ─2─ F     C → F (4)    D → C (7)
              |        E → D (9)    F → G (2)
              4        G → H (1)    H → G (1)
              |
              C ─7─ D ─9─ E

Round 1: After merging cheapest edges
    Components: {A,B}, {G,H}, {C,F}, {D}, {E}
    Edges added: A-B(4), G-H(1), C-F(4)

Round 2: Each component picks cheapest outgoing edge again
    {A,B} → H(8)     {G,H} → F(2)
    {C,F} → G(2)     {D} → C(7)     {E} → D(9)

    Components merge: {A,B,G,H,C,F}, {D}, {E}
    Edges added: G-F(2), A-H(8)

Round 3: Final merges
    {A,B,G,H,C,F} → D(7)     {D} → C(7)     {E} → D(9)
    Edges added: C-D(7), D-E(9)

MST Complete: Total Cost = 4+1+4+2+8+7+9 = 35
```

---

## 10. References

* Borůvka, O. (1926). "O jistém problému minimálním" (On a certain minimal problem)
* Cormen, T. H., et al. (2009). "Introduction to Algorithms" (3rd ed.), Chapter 23
* Chazelle, B. (2000). "A Minimum Spanning Tree Algorithm with Inverse-Ackermann Type Complexity"
