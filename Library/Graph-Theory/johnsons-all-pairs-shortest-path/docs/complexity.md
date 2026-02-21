# Complexity Analysis: Johnson's Algorithm

## 1. Time Complexity: O(V² log V + VE)

### 1.1 Phase-by-Phase Breakdown

| Phase | Operation | Cost |
|-------|-----------|------|
| **1 — Bellman-Ford** | Relax all E edges, V times | **O(VE)** |
| **2 — Reweighting** | Update each of E edges once | O(E) |
| **3 — V × Dijkstra** | Dijkstra from each of V vertices | **O(V(E log V))** = O(VE log V) |
| **Total** | | **O(VE log V)** worst-case |

> **Simplified form:** O(V² log V + VE) — because Bellman-Ford O(VE) and
> Dijkstra O(VE log V) are both present; the dominant term depends on E.

---

### 1.2 Complexity for Common Graph Densities

| Graph Type | E | Johnson's Time | Floyd-Warshall |
|------------|---|----------------|----------------|
| **Sparse** (tree-like) | O(V) | **O(V² log V)** ✅ | O(V³) |
| **Moderately sparse** | O(V log V) | O(V² log² V) ✅ | O(V³) |
| **Dense** | O(V²) | O(V³ log V) ❌ | **O(V³)** ✅ |
| **Complete graph** | V(V−1) | O(V³ log V) ❌ | **O(V³)** ✅ |

**Key takeaway:** Johnson's beats Floyd-Warshall when **E is small relative to V²**.

---

### 1.3 Break-Even Point

Johnson's is faster than Floyd-Warshall when:

```
VE log V < V³
E log V  < V²
E        < V² / log V
```

For V = 1,000 → E < 1,000,000 / 10 = **100,000 edges** → Johnson's wins.

---

## 2. Space Complexity: O(V²)

| Structure | Size | Notes |
|-----------|------|-------|
| `distances` matrix | O(V²) | All-pairs result |
| `next_node` matrix | O(V²) | Path reconstruction |
| Bellman-Ford `h[]` potentials | O(V) | Reweighting values |
| Dijkstra heap (per run) | O(E) | Freed after each source |
| **Total** | **O(V²)** | Dominated by result matrices |

---

## 3. Why O(V² log V + VE), Not O(V³)?

### For Sparse Graphs (E ≈ kV for small constant k):

```
Bellman-Ford:   O(V × kV)       = O(kV²)       = O(V²)
V × Dijkstra:   O(V × kV log V) = O(kV² log V)  = O(V² log V)

Total: O(V² log V)   vs   Floyd-Warshall: O(V³)
```

**Speed ratio:** V / log V — on 10,000 vertices ≈ **750× faster** than Floyd-Warshall!

---

## 4. Algorithm Component Analysis

### 4.1 Bellman-Ford Phase

```
Outer loop: V − 1 iterations
Inner loop: relax E edges each pass
Operations: (V−1) × E = O(VE)
```

**Early termination:** If no update in a pass, convergence is reached — can exit early.
Best case for Bellman-Ford: O(E) (DAG with correct ordering).

### 4.2 Dijkstra Phase (with Binary Heap)

```
Per source:
  - Each vertex extracted once:  O(V log V)
  - Each edge relaxed at most once:  O(E log V)
  Total per source:  O((V + E) log V) ≈ O(E log V) for connected graphs

For all V sources:  V × O(E log V) = O(VE log V)
```

**With Fibonacci Heap:** Dijkstra becomes O(E + V log V), making Johnson's total
**O(V² + VE)** — optimal but complex to implement.

---

## 5. Performance Benchmarks (Approximate)

### Sparse Graph (E ≈ 3V — road network):

| V | E | Johnson's | Floyd-Warshall |
|---|---|-----------|----------------|
| 100 | 300 | < 1 ms | 1 ms |
| 1,000 | 3,000 | ~5 ms | ~1 sec |
| 10,000 | 30,000 | ~800 ms | ~16 min |
| 100,000 | 300,000 | ~2 min | impractical |

### Dense Graph (E ≈ V²):

| V | E | Johnson's | Floyd-Warshall |
|---|---|-----------|----------------|
| 100 | 10,000 | ~5 ms | 1 ms |
| 500 | 250,000 | ~5 sec | ~125 ms |
| 1,000 | 1,000,000 | ~40 sec | ~1 sec |

---

## 6. Comparison with All-Pairs Algorithms

| Algorithm | Time | Space | Negative Weights | Best For |
|-----------|------|-------|------------------|----------|
| **Johnson's** | **O(V² log V + VE)** | O(V²) | ✅ Yes | **Sparse graphs** |
| Floyd-Warshall | O(V³) | O(V²) | ✅ Yes | Dense graphs |
| V × Dijkstra | O(VE log V) | O(V) | ❌ No (positive only) | Sparse, positive weights |
| V × Bellman-Ford | O(V²E) | O(V) | ✅ Yes | Rarely preferred |

---

## 7. Scalability Guide

### When to Choose Johnson's

```
✅ Sparse graphs   (road networks, dependency graphs, citation graphs)
✅ Negative weights present
✅ V > 500 where Floyd-Warshall becomes slow
✅ All-pairs result needed (not just single source)
```

### When NOT to Use Johnson's

```
❌ Dense graphs (E ≈ V²) — Floyd-Warshall is simpler and faster
❌ Only positive weights + only single source — use plain Dijkstra
❌ Negative cycles exist — algorithm correctly detects and rejects these
```

---

## 8. Doubling Analysis

For **sparse** graphs (E = cV):

| V | V² log V | Growth |
|---|----------|--------|
| 100 | ~66,000 | — |
| 200 | ~303,000 | ~4.6× |
| 400 | ~1,370,000 | ~4.5× |
| 800 | ~6,110,000 | ~4.5× |

Doubling V multiplies time by ≈ **4–4.5×** (vs 8× for Floyd-Warshall O(V³)).

---

## 9. Summary

| Metric | Value |
|--------|-------|
| **Worst-case time** | O(VE log V) |
| **Sparse graph time** | **O(V² log V)** |
| **Dense graph time** | O(V³ log V) — worse than Floyd-Warshall |
| **Space** | O(V²) |
| **Negative weight support** | ✅ Yes |
| **Negative cycle detection** | ✅ Yes (via Bellman-Ford) |
| **Practical sweet spot** | Sparse graphs with V > 300 |

**Bottom line:** Johnson's is the gold standard for **sparse graphs with negative weights**.
For dense graphs, Floyd-Warshall remains simpler and faster.
