# Hierholzer's Algorithm — Complexity Analysis

## Time Complexity: O(V + E)

Each edge is traversed exactly once. Each vertex is pushed and popped from
the stack exactly once.

| Operation | Cost |
|-----------|------|
| Build adjacency list | O(V + E) |
| Eulerian condition check | O(V + E) |
| Main traversal (each edge once) | O(E) |
| Path construction | O(V + E) |
| **Total** | **O(V + E)** |

This is **optimal** — you must visit every edge at least once.

---

## Space Complexity: O(V + E)

| Structure | Space |
|-----------|-------|
| Adjacency list (deque per vertex) | O(V + E) |
| DFS stack (worst: deep path) | O(V) |
| Result path | O(V + E) |
| **Total** | **O(V + E)** |

---

## Why `deque` over `list` for adjacency?

Using `deque.popleft()` is **O(1)** vs `list.pop(0)` which is **O(n)**.
This keeps the overall algorithm at O(V + E) rather than O(V·E).

---

## Performance Benchmarks (approximate)

| Graph Size | Vertices | Edges | Expected Time |
|------------|----------|-------|---------------|
| Small | < 1K | < 10K | < 5 ms |
| Medium | 10K | 100K | ~50 ms |
| Large | 100K | 1M | ~500 ms |

---

## Comparison with Alternatives

| Approach | Time | Notes |
|----------|------|-------|
| **Hierholzer's (this)** | **O(V + E)** | Optimal — iterative, no recursion issues |
| Fleury's Algorithm | O(E²) | Simpler to understand but very slow |
| Naive brute force | O(E!) | Completely impractical |

Hierholzer's is the **only practical choice** for large graphs.
