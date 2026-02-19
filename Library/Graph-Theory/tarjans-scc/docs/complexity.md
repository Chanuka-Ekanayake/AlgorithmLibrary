# Tarjan's SCC — Complexity Analysis

## Time Complexity: O(V + E)

Each vertex is visited exactly once, and each edge is examined exactly once
during the DFS traversal.

| Operation | Cost |
|-----------|------|
| DFS traversal | O(V + E) |
| Stack push/pop (each vertex once) | O(V) |
| SCC root check + collection | O(V) |
| **Total** | **O(V + E)** |

This is **optimal** — any algorithm must inspect every vertex and edge at least
once.

---

## Space Complexity: O(V + E)

| Structure | Space |
|-----------|-------|
| Adjacency list (graph) | O(V + E) |
| `disc`, `low`, `on_stack` arrays | O(V) |
| DFS stack (worst case, path graph) | O(V) |
| SCC output | O(V) |
| **Total** | **O(V + E)** |

---

## Performance Benchmarks (approximate)

| Graph Size | Vertices | Edges | Expected Time |
|------------|----------|-------|---------------|
| Small | < 1K | < 10K | < 5 ms |
| Medium | 10K | 100K | ~50 ms |
| Large | 100K | 1M | ~500 ms |
| Very Large | 1M | 10M | ~5 s |

---

## Comparison with Alternatives

| Algorithm | Time | Passes | Notes |
|-----------|------|--------|-------|
| **Tarjan's (this)** | **O(V+E)** | **1 DFS** | Optimal — single pass |
| Kosaraju's | O(V+E) | 2 DFS | Simpler to understand, same asymptotic |
| Naive (all-pairs reachability) | O(V³) | — | Impractical for large graphs |

---

## Why Use Tarjan's Over Kosaraju's?

- **One DFS** vs two — less constant-factor overhead
- **No graph transposition** needed (Kosaraju requires reversing all edges)
- Slightly **better cache performance** in practice
- Discovery of SCCs in **reverse topological order** of the condensation graph
