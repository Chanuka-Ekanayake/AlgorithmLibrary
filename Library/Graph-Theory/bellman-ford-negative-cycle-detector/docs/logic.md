# Algorithm Logic: Bellman-Ford Shortest Path

## 1. The Core Concept

The **Bellman-Ford algorithm** uses **Dynamic Programming** to find the shortest paths from a single source to all vertices in a weighted directed graph. It processes edges repeatedly, gradually improving distance estimates until optimal values are reached.

The key innovation is its ability to handle **negative edge weights** while also detecting **negative cycles** that would make shortest path calculations undefined.

---

## 2. The Fundamental Principle: Edge Relaxation

### 2.1 What is Relaxation?

For any edge (u → v) with weight w:

**Relaxation Check:** If `distance[u] + w < distance[v]`, then update `distance[v] = distance[u] + w`

This means: "If going through u gives a shorter path to v than we currently know, update it."

### 2.2 Visual Example

```text
Initial state:
   A(0) ──4──> B(∞)
   
After relaxing edge A→B:
   A(0) ──4──> B(4)
   
If we later find:
   C(1) ──2──> B(4)
   
After relaxation:
   C(1) ──2──> B(3)  [Updated because 1+2 < 4]
```

---

## 3. Why |V| - 1 Iterations?

### 3.1 Mathematical Proof

**Theorem:** In a graph with V vertices and no negative cycles, the shortest path between any two vertices contains at most V - 1 edges.

**Proof:**
1. A path with V or more edges must repeat at least one vertex (Pigeonhole Principle)
2. If it repeats a vertex, it contains a cycle
3. If the cycle has positive or zero weight, removing it creates a shorter path
4. Therefore, the shortest simple path has ≤ V - 1 edges

**Algorithm Guarantee:** After i iterations, we've correctly computed all shortest paths of length ≤ i edges.

After V - 1 iterations → All shortest paths are found.

---

## 4. Step-by-Step Execution

### 4.1 Initialization Phase

```python
distances = {node: ∞ for all nodes}
distances[source] = 0
predecessors = {node: None for all nodes}
```

### 4.2 Main Relaxation Loop

```text
FOR i = 1 to |V| - 1:
    FOR each edge (u → v) with weight w:
        IF distance[u] + w < distance[v]:
            distance[v] = distance[u] + w
            predecessor[v] = u
```

**Iteration Insight:**
- **Iteration 1:** Finds shortest paths using exactly 1 edge
- **Iteration 2:** Finds shortest paths using up to 2 edges
- **Iteration k:** Finds shortest paths using up to k edges

### 4.3 Example Walkthrough

Graph:
```text
A ─(-1)→ B
B ─(3)─→ C
A ─(4)─→ C
```

**Iteration 0 (Init):**
```
A: 0, B: ∞, C: ∞
```

**Iteration 1:**
```
Relax A→B: B = 0 + (-1) = -1  ✓
Relax A→C: C = 0 + 4 = 4      ✓
Relax B→C: C = -1 + 3 = 2     ✓ [Better!]

Result: A: 0, B: -1, C: 2
```

**Iteration 2:**
```
No improvements possible → Algorithm terminates early
```

---

## 5. Negative Cycle Detection

### 5.1 The Insight

If after V - 1 iterations we can **still** relax any edge, it means we're in a negative cycle.

**Why?** Because we've already checked all possible simple paths. If improvement is still possible, we're going around a cycle that reduces cost indefinitely.

### 5.2 Detection Algorithm

```python
# After main loop:
FOR each edge (u → v) with weight w:
    IF distance[u] + w < distance[v]:
        RETURN "Negative cycle detected!"
```

### 5.3 Example of Negative Cycle

```text
A ─(1)→ B ─(-3)→ C ─(1)→ A

Starting at A:
Round 1: A=0, B=1, C=-2
Round 2: A=-1, B=0, C=-3
Round 3: A=-2, B=-1, C=-4
...continues forever...
```

After V - 1 iterations, distances keep improving → Negative cycle exists.

---

## 6. Comparison: Bellman-Ford vs Dijkstra

| Aspect | Bellman-Ford | Dijkstra |
|--------|-------------|----------|
| **Approach** | Dynamic Programming | Greedy Algorithm |
| **Edge Processing** | All edges, V-1 times | Priority queue order |
| **Negative Weights** | ✅ Handles correctly | ❌ Produces wrong results |
| **Complexity** | O(V × E) | O(E log V) |
| **Cycle Detection** | ✅ Built-in | ❌ N/A |

**Key Difference:** Dijkstra assumes finding the minimum distance once means it's final. This fails with negative weights because later paths might be cheaper.

---

## 7. Optimization: Early Termination

```python
for i in range(V - 1):
    updated = False
    for each edge:
        if relax(edge):
            updated = True
    
    if not updated:
        break  # No changes → We're done early!
```

**Best Case:** O(E) if the graph has structure allowing quick convergence.

**Worst Case:** O(V × E) for dense graphs with complex dependencies.

---

## 8. Real-World Intuition: Currency Arbitrage

### 8.1 The Problem

Currency exchange rates can create arbitrage opportunities:

```
USD → EUR: rate 0.85
EUR → GBP: rate 1.20
GBP → USD: rate 1.00
```

Conversion: 1 USD → 0.85 EUR → 1.02 GBP → 1.02 USD (Profit!)

### 8.2 Graph Representation

Model exchange rates as **negative logarithms**:

```
weight(A→B) = -log(exchange_rate)
```

**Why?** Because:
- Multiplication becomes addition: log(a × b) = log(a) + log(b)
- Profit (rate > 1) becomes negative weight
- Shortest path = maximum product = arbitrage opportunity

A negative cycle in this graph = arbitrage opportunity!

---

## 9. Edge Cases & Considerations

### 9.1 Unreachable Nodes

If `distance[v] = ∞` after the algorithm, node v is unreachable from the source.

### 9.2 Negative Cycles Not Reachable from Source

Bellman-Ford only detects negative cycles reachable from the source node.

### 9.3 Graph Representation

Works with:
- Directed graphs ✅
- Undirected graphs (model as bidirectional edges) ✅
- Disconnected graphs ✅
- Self-loops ✅

---

## 10. Pseudocode

```text
BELLMAN-FORD(Graph G, Vertex source):
    // Initialize
    FOR each vertex v in G:
        distance[v] ← ∞
        predecessor[v] ← NULL
    distance[source] ← 0
    
    // Relax edges repeatedly
    FOR i = 1 to |V| - 1:
        FOR each edge (u, v) with weight w in G:
            IF distance[u] + w < distance[v]:
                distance[v] ← distance[u] + w
                predecessor[v] ← u
    
    // Check for negative cycles
    FOR each edge (u, v) with weight w in G:
        IF distance[u] + w < distance[v]:
            RETURN "Negative cycle detected"
    
    RETURN distance, predecessor
```

---

## 11. Implementation Notes

### 11.1 Data Structures Used

- **Adjacency List:** `Dict[str, List[Tuple[str, float]]]` for efficient edge iteration
- **Distance Array:** `Dict[str, float]` for O(1) lookups
- **Predecessor Map:** `Dict[str, Optional[str]]` for path reconstruction

### 11.2 Why Not Priority Queue?

Unlike Dijkstra, we must check **all edges** in each iteration regardless of current distances, making a priority queue unnecessary and inefficient.

---

## 12. Applications in Software Engineering

1. **Network Routing:** BGP protocols with route preferences (negative weights)
2. **Financial Systems:** Arbitrage detection in trading algorithms
3. **Game AI:** Pathfinding with rewards (negative costs) and penalties
4. **Resource Scheduling:** Task dependencies with bonuses/penalties
5. **Constraint Satisfaction:** Finding feasible solutions in systems with negative constraints

---

## 13. Summary

**Bellman-Ford = Dynamic Programming + Edge Relaxation**

- Iteratively improves distance estimates
- Handles negative weights correctly
- Detects negative cycles as a bonus
- Slower than Dijkstra but more versatile

Use when: Negative weights exist or cycle detection is needed.
