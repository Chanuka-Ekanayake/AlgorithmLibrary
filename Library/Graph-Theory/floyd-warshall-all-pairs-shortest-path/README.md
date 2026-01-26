# Floyd-Warshall Algorithm: All-Pairs Shortest Path & Network Analysis

## 1. Overview

The **Floyd-Warshall Algorithm** is a dynamic programming algorithm that computes shortest paths between **all pairs of vertices** in a weighted directed graph. It's the go-to solution when you need a complete distance matrix showing how to get from any node to any other node optimally.

This makes it essential for network analysis, routing tables, social network metrics, and any scenario requiring comprehensive path information.

---

## 2. Key Engineering Features

* **All-Pairs Solution:** Computes shortest paths between every pair of vertices in one execution
* **Negative Weight Support:** Handles negative edge weights correctly (detects negative cycles)
* **Dense Graph Optimization:** More efficient than running Dijkstra V times for dense graphs
* **Simple Implementation:** Clean triple-nested loop structure, easy to understand and maintain
* **Network Metrics:** Enables calculation of graph diameter, center, and transitive closure
* **Path Reconstruction:** Full path recovery between any vertex pair

---

## 3. Folder Architecture

```text
.
├── core/                          # Algorithm Implementation
│   └── floyd_warshall.py          # Main algorithm + network analysis utilities
├── docs/                          # Technical Documentation
│   ├── logic.md                   # DP approach and algorithm mechanics
│   └── complexity.md              # O(V³) analysis and comparisons
├── test-project/                  # Real-World Simulation
│   ├── app.py                     # City logistics network analyzer
│   ├── instructions.md            # User guide
│   └── city_network.txt           # Sample transportation network
└── README.md                      # Module Entry Point (Current File)
```

---

## 4. Performance Benchmarks

| Operation | Complexity | Efficiency Note |
|-----------|-----------|-----------------|
| **Time Complexity** | O(V³) | Three nested loops over vertices |
| **Space Complexity** | O(V²) | Stores distance matrix |
| **Best for** | Dense graphs, all-pairs queries | When E ≈ V² |
| **Negative Cycle Detection** | O(1) | Check diagonal after main loop |

**Comparison with Alternatives:**
- **V × Dijkstra:** O(V²log V) for sparse graphs - Better when E << V²
- **V × Bellman-Ford:** O(V² × E) - Only for negative weights
- **Floyd-Warshall:** O(V³) - Best for dense graphs or all-pairs needs

---

## 5. Quick Start

### Installation

```python
# No external dependencies required - uses standard Python
from core.floyd_warshall import floyd_warshall, reconstruct_path
```

### Basic Usage

```python
# Define a graph (adjacency list format)
graph = {
    'A': {'B': 3, 'C': 8, 'E': -4},
    'B': {'D': 1, 'E': 7},
    'C': {'B': 4},
    'D': {'A': 2, 'C': -5},
    'E': {'D': 6}
}

# Calculate all-pairs shortest paths
distances, next_node = floyd_warshall(graph)

# Get distance between specific vertices
print(f"Distance A → C: {distances[('A', 'C')]}")

# Reconstruct the actual path
path = reconstruct_path(next_node, 'A', 'C')
print(f"Path: {' → '.join(path)}")
```

---

## 6. Real-World Applications

### 6.1 Network Routing Tables

**Scenario:** Internet routers need to know the best path to every other router in the network.

Floyd-Warshall computes the complete routing table in one pass.

### 6.2 City Transportation Planning

**Scenario:** Urban planners need to analyze travel times between all district pairs to optimize public transit.

### 6.3 Social Network Analysis

**Scenario:** Calculate degrees of separation, network diameter, and identify central influencers.

### 6.4 Supply Chain Optimization

**Scenario:** Distribution network with multiple warehouses - find optimal routes between all warehouse pairs.

---

## 7. How It Works

### The Algorithm in 3 Steps:

1. **Initialize:** Set up distance matrix with direct edges; infinity for no edge
2. **Iterate:** For each possible intermediate vertex k, check if path i→k→j is shorter than direct i→j
3. **Update:** Keep the minimum distance; repeat for all vertex combinations

### The Key Insight: Dynamic Programming

**Recurrence Relation:**
```
dist[i][j][k] = min(
    dist[i][j][k-1],                    // Don't use vertex k
    dist[i][k][k-1] + dist[k][j][k-1]   // Use vertex k as intermediate
)
```

After considering all vertices as intermediates, we have the shortest paths.

---

## 8. When to Use Floyd-Warshall

### ✅ Use When:

- Need shortest paths between **all** vertex pairs
- Graph is dense (E ≈ V²)
- Negative weights exist (but no negative cycles)
- Need graph diameter, center, or other network metrics
- V is small to moderate (< 1,000 vertices)

### ❌ Don't Use When:

- Only need single-source shortest paths → Use Dijkstra or Bellman-Ford
- Graph is very large (V > 10,000) → Memory and time prohibitive
- Graph is sparse (E << V²) → Running Dijkstra V times is faster

---

## 9. Algorithm Comparison

| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| **Floyd-Warshall** | O(V³) | O(V²) | All pairs, dense graphs |
| **Dijkstra (single)** | O(E log V) | O(V) | Single source, positive weights |
| **V × Dijkstra** | O(V²log V + VE log V) | O(V) | All pairs, sparse graphs |
| **Bellman-Ford** | O(V × E) | O(V) | Single source, negative weights |
| **Johnson's** | O(V²log V + VE) | O(V²) | All pairs, sparse with negatives |

---

## 10. Advanced Features

### Network Diameter

```python
from core.floyd_warshall import get_graph_diameter

diameter = get_graph_diameter(graph)
print(f"Maximum shortest path in network: {diameter}")
```

### Graph Center (Optimal Hub Location)

```python
from core.floyd_warshall import get_graph_center

center, eccentricity = get_graph_center(graph)
print(f"Optimal hub location: {center}")
print(f"Maximum distance from hub: {eccentricity}")
```

### Transitive Closure (Reachability)

```python
from core.floyd_warshall import transitive_closure

reachable = transitive_closure(graph)
if reachable[('A', 'D')]:
    print("Can reach D from A")
```

### Negative Cycle Detection

```python
from core.floyd_warshall import detect_negative_cycle

distances, _ = floyd_warshall(graph)
if detect_negative_cycle(graph, distances):
    print("⚠️ Graph contains negative cycle!")
```

---

## 11. Test Project: City Logistics Network

The included test project simulates a multi-city transportation network where you can:

- Load city connections with travel costs
- Find optimal routes between any city pairs
- Identify the best hub location (graph center)
- Analyze network connectivity
- Detect problematic routes (negative cycles)

Run the simulation:

```bash
cd test-project
python app.py
```

---

## 12. Performance Characteristics

### Scalability Limits

| Vertices (V) | Time (approx) | Memory |
|--------------|---------------|--------|
| 100 | 1 ms | 80 KB |
| 500 | 125 ms | 2 MB |
| 1,000 | 1 second | 8 MB |
| 5,000 | 2 minutes | 200 MB |
| 10,000 | 16 minutes | 800 MB |

**Practical Limit:** V < 5,000 for interactive applications

### Dense vs Sparse Graphs

**Dense (E ≈ V²):**
- Floyd-Warshall: O(V³) ✓ Optimal
- V × Dijkstra: O(V³ log V) ✗ Slower

**Sparse (E ≈ V):**
- Floyd-Warshall: O(V³) ✗ Wasteful
- V × Dijkstra: O(V² log V) ✓ Better

---

## 13. Implementation Highlights

### Memory Optimization

The implementation uses dictionaries instead of 2D arrays for the distance matrix, making it memory-efficient for graphs that don't use all possible edges.

### Path Reconstruction

The `next_node` matrix allows O(V) path reconstruction for any vertex pair without additional computation.

### Negative Weight Handling

Unlike Dijkstra, Floyd-Warshall correctly handles negative weights and provides negative cycle detection.

---

## 14. Common Pitfalls & Solutions

### Pitfall 1: Forgetting Self-Loops

**Issue:** Not initializing dist[v][v] = 0

**Solution:** Always set diagonal to 0 during initialization

### Pitfall 2: Incorrect Loop Order

**Issue:** Wrong nesting of k, i, j loops

**Solution:** k (intermediate) must be outermost loop

### Pitfall 3: Large Graph Memory Issues

**Issue:** O(V²) space for huge graphs

**Solution:** Use sparse representations or alternative algorithms

---

## 15. Extensions & Variants

### Parallel Floyd-Warshall

The algorithm can be parallelized across the k-loop iterations:
```python
for k in vertices:
    parallel_for i, j:
        update dist[i][j]
```

### Minimax Path (Bottleneck Shortest Path)

Modify the min operator to find paths that minimize maximum edge:
```python
dist[i][j] = min(dist[i][j], max(dist[i][k], dist[k][j]))
```

---

## 16. License

MIT License - See root LICENSE file.

---

## 17. References

* Floyd, R. W. (1962). "Algorithm 97: Shortest Path". Communications of the ACM.
* Warshall, S. (1962). "A theorem on Boolean matrices". Journal of the ACM.
* Cormen, T. H., et al. (2009). "Introduction to Algorithms" (3rd ed.), Chapter 25.2.
