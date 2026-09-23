# Complexity Analysis: Borůvka's Algorithm

Borůvka's Algorithm is a greedy strategy used to find the **Minimum Spanning Tree (MST)**. Its efficiency is determined by the number of merging rounds and the cost of scanning edges within each round.

## 1. Time Complexity

The overall time complexity is:

**O(E log V)**

### 1.1 Parameter Breakdown

* **V:** The number of vertices (nodes) in the graph.
* **E:** The number of edges (connections) in the graph.

### 1.2 Step-by-Step Justification

1. **Round Count:** Each round at least halves the number of connected components. Starting with V components, we reach 1 component in at most **⌈log₂ V⌉** rounds.

2. **Work Per Round:** In each round, we scan **all E edges** to find the cheapest outgoing edge for each component.
   * Edge scanning: **O(E)** per round.
   * DSU find operations: **O(E · α(V))** per round, where α is the inverse Ackermann function (effectively constant).
   * Component merging (union operations): **O(V)** per round.

3. **Total Complexity:**
   * O(log V) rounds × O(E · α(V)) per round
   * = **O(E · α(V) · log V)**
   * Since α(V) ≤ 5 for all practical V, this simplifies to **O(E log V)**.

---

## 2. Space Complexity

The space complexity is:

**O(V + E)**

### 2.1 Memory Allocation

* **DSU Storage:** Two dictionaries (`parent` and `rank`) of size **O(V)**.
* **Graph Storage:** Adjacency list requires **O(V + E)** space.
* **Cheapest Edge Map:** One entry per component, at most **O(V)** per round.
* **MST Edge List:** Stores V-1 edges, **O(V)** space.

---

## 3. Round-by-Round Convergence Analysis

| Round | Max Components | Work Per Round | Cumulative Work |
| --- | --- | --- | --- |
| 0 | V | O(E) | O(E) |
| 1 | V/2 | O(E) | O(2E) |
| 2 | V/4 | O(E) | O(3E) |
| k | V/2^k | O(E) | O(kE) |
| log₂ V | 1 | O(E) | O(E log V) |

**Key Insight:** Although the number of components shrinks, we still scan all edges each round because edges can span between any components. The total work is O(E) × O(log V) rounds = **O(E log V)**.

---

## 4. Comparison: Borůvka's vs Kruskal's vs Prim's

| Feature | Borůvka's | Kruskal's | Prim's |
| --- | --- | --- | --- |
| **Paradigm** | Component merging | Edge-based (Greedy) | Vertex-based (Greedy) |
| **Data Structure** | DSU | DSU | Priority Queue (Min-Heap) |
| **Time (Sequential)** | O(E log V) | O(E log E) | O(E log V) |
| **Time (Parallel)** | **O(E) with O(log V) rounds** | Not parallelizable | Not parallelizable |
| **Best For** | **Parallel/distributed systems** | Sparse graphs | Dense graphs |
| **Bottleneck** | Edge scanning per round | Edge sorting | Priority queue operations |

---

## 5. Parallel Complexity Analysis

### 5.1 PRAM Model (Shared Memory)

With O(E) processors:

| Phase | Parallel Time | Work |
| --- | --- | --- |
| Find cheapest per component | O(log V) | O(E) |
| Merge components | O(α(V)) | O(V) |
| **Total per round** | **O(log V)** | **O(E)** |
| **All rounds** | **O(log² V)** | **O(E log V)** |

### 5.2 MapReduce Model (Distributed)

| Metric | Complexity |
| --- | --- |
| **Communication rounds** | O(log V) |
| **Data shuffled per round** | O(E) |
| **Total data shuffled** | O(E log V) |
| **Reducers needed** | O(V) per round (one per component) |

### 5.3 GPU Model

| Metric | Complexity |
| --- | --- |
| **Thread blocks** | O(V) — one per component |
| **Threads per block** | O(max degree) |
| **Kernel launches** | O(log V) |
| **Total work** | O(E log V) |

---

## 6. Engineering Trade-offs

* **Sequential vs Parallel:** On a single core, Borůvka's has similar performance to Kruskal's. Its advantage only materializes with parallel execution.
* **Edge Scanning Overhead:** Unlike Kruskal's (which sorts once), Borůvka's rescans all edges each round. For very sparse graphs with large V, Kruskal's may be faster sequentially.
* **Memory Locality:** Component-based scanning has worse cache locality than Prim's vertex-based approach on dense graphs.
* **Implementation Complexity:** More complex than Kruskal's due to round management and component tracking, but simpler than Prim's with Fibonacci heaps.

---

## 7. Performance Metrics Table

| Metric | Complexity |
| --- | --- |
| **Best-Case Time** | Ω(E) — when graph is already a tree |
| **Average-Case Time** | Θ(E log V) |
| **Worst-Case Time** | O(E log V) |
| **Auxiliary Space** | O(V) |
| **Parallel Depth** | O(log² V) with O(E) processors |

---

## 8. When to Choose Borůvka's

### ✅ Choose Borůvka's when:
- You have access to parallel hardware (multi-core, GPU, cluster)
- The graph is distributed across multiple machines
- You are using MapReduce or similar frameworks
- You need O(log V) communication rounds in a distributed system

### ❌ Choose alternatives when:
- Single-threaded execution → Kruskal's (simpler) or Prim's (better for dense)
- Graph is very sparse (E ≈ V) → Kruskal's
- Graph is very dense (E ≈ V²) → Prim's with array
- Edges are pre-sorted → Kruskal's (skips sorting step)

---

## 9. Scaling Analysis

| Vertices | Edges (E=10V) | Rounds | Sequential Time | Parallel Time (E processors) |
| --- | --- | --- | --- | --- |
| 1,000 | 10,000 | 10 | ~1 ms | ~0.1 ms |
| 10,000 | 100,000 | 14 | ~15 ms | ~1 ms |
| 100,000 | 1,000,000 | 17 | ~200 ms | ~10 ms |
| 1,000,000 | 10,000,000 | 20 | ~3 sec | ~100 ms |

**Observation:** The parallel speedup grows with graph size, making Borůvka's increasingly attractive for large-scale problems.
