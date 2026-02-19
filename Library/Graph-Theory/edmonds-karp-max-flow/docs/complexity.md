# Technical Specification: Edmonds-Karp Max Flow

## 1. Executive Summary

The Edmonds-Karp algorithm is a specific implementation of the Ford-Fulkerson method for computing the maximum flow in a flow network. It uses Breadth-First Search (BFS) to find the shortest augmenting path in terms of number of edges.

* **Category:** Graph Theory
* **Difficulty:** Intermediate
* **Primary Goal:** Finding the maximum flow possible from a source node to a sink node in a network.

---

## 2. Mathematical Foundation & Intuition

### 2.1 The Logic

The algorithm works by repeatedly finding the shortest augmenting path from the source to the sink in the residual graph. An augmenting path is a path where every edge has unused capacity. By pushing flow along this path, we increase the total flow. We repeat this until no more augmenting paths exist.

### 2.2 Mathematical Notation

* Let $G = (V, E)$ be a directed graph where each edge $(u, v) \in E$ has a capacity $c(u, v) \geq 0$.
* A flow $f(u, v)$ must satisfy:
    1.  **Capacity Constraint:** $0 \leq f(u, v) \leq c(u, v)$
    2.  **Flow Conservation:** For every vertex $v$ other than source $s$ and sink $t$, the total flow entering $v$ must equal the total flow satisfying $v$.
* The objective is to maximize $|f| = \sum_{v \in V} f(s, v)$.

---

## 3. Algorithm Breakdown

1.  **Initialization:** Start with zero flow. Create a residual graph where residual capacity equals original capacity.
2.  **Iterative Process:**
    *   Find the shortest path from source to sink using BFS in the residual graph.
    *   Calculate the bottleneck capacity (minimum residual capacity) along this path.
    *   Augment the flow by adding this bottleneck value to the edges along the path.
    *   Update the residual graph: decrease forward edge capacity, increase backward edge capacity.
3.  **Termination:** Stop when no path exists from source to sink in the residual graph.

### Pseudocode

```text
Algorithm EdmondsKarp(Graph, s, t):
  MaxFlow = 0
  WHILE BFS(ResidualGraph, s, t) finds a path P:
    PathFlow = min(ResidualCapacity(u, v) for (u, v) in P)
    MaxFlow += PathFlow
    FOR each edge (u, v) in P:
      ResidualGraph[u][v] -= PathFlow
      ResidualGraph[v][u] += PathFlow
  RETURN MaxFlow
```

---

## 4. Complexity Analysis

| Metric | Complexity | Description |
| --- | --- | --- |
| **Time Complexity** | $O(V E^2)$ | BFS takes $O(E)$. The loop runs at most $O(V E)$ times because each augmentation increases the shortest path distance or saturates an edge critical to the shortest path. |
| **Space Complexity** | $O(V^2)$ or $O(E)$ | Depends on graph representation (Adjacency Matrix vs Adjacency List). We use Adjacency List (Dict of Dicts). |

---

## 5. Real-World Application Scenario

### 5.1 The Scenario

**Problem:** A water distribution network needs to determine the maximum volume of water that can be pumped from a reservoir (source) to a treatment plant (sink) through a system of pipes with varying diameters (capacities).

### 5.2 System Integration

* **Input Data Source:** GIS data of the pipe network.
* **Downstream Impact:** Helps engineers identify bottlenecks in the network and plan capacity upgrades.

---

## 6. Implementation Notes & Best Practices

* **Data Structures Used:**
    *   `Dict[str, Dict[str, int]]` for the graph (Adjacency List).
    *   `collections.deque` for the BFS queue.
* **Optimization Techniques:**
    *   Using BFS ensures we find the *shortest* number of edges, which guarantees the $O(V E^2)$ bound (unlike DFS which could be much slower).
* **Edge Cases Handled:**
    *   Disconnected graph (BFS returns False).
    *   Cycles (handled naturally by residual graph logic).

---

## 7. Performance Benchmarking

(Pending specific environment tests)
