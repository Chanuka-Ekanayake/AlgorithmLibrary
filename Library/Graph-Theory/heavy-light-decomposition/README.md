# Heavy-Light Decomposition

## 1. Overview

**Heavy-Light Decomposition (HLD)** is an advanced tree optimization technique that turns expensive tree path queries into a small number of contiguous array queries. It is especially useful when a system needs repeated operations such as path sums, path updates, or subtree analytics on a rooted tree.

This package targets the common engineering case where a network, dependency graph, or org chart must support fast updates across routes between two nodes.

---

## 2. Key Engineering Features

- **Fast Path Queries** - Breaks any tree path into $O(\log n)$ chain segments.
- **Fast Path Updates** - Supports bulk updates across a route without touching every node individually.
- **Subtree Queries** - Uses the HLD index map to make subtree ranges contiguous.
- **Reusable Core** - The implementation wraps a lazy segment tree so the decomposition stays focused on tree structure.
- **Pure Python** - No external dependencies required.

---

## 3. Folder Architecture

```text
.
├── core/
│   ├── __init__.py        # Package export
│   └── hld.py             # Heavy-light decomposition + lazy segment tree
├── docs/
│   ├── logic.md           # Why heavy and light edges help reduce path work
│   └── complexity.md      # Complexity breakdown and trade-offs
├── test-project/
│   ├── app.py             # Demo scenarios and correctness checks
│   └── instructions.md    # How to run the demo
└── README.md              # Module entry point
```

---

## 4. Performance Benchmarks

| Operation | Time Complexity | Note |
|---|---|---|
| **Build** | $O(n)$ | One DFS plus one decomposition pass. |
| **Path Query** | $O(\log^2 n)$ | At most $O(\log n)$ chains, each queried in $O(\log n)$. |
| **Path Update** | $O(\log^2 n)$ | Same chain decomposition as path query. |
| **Subtree Query** | $O(\log n)$ | Subtrees become contiguous ranges after indexing. |
| **Subtree Update** | $O(\log n)$ | Range update on the contiguous subtree interval. |
| **Space** | $O(n)$ | Adjacency lists, decomposition arrays, and segment tree storage. |

---

## 5. Quick Start

```python
from core.hld import HeavyLightDecomposition

# Tree edges are zero-indexed.
edges = [
    (0, 1),
    (0, 2),
    (1, 3),
    (1, 4),
    (2, 5),
    (2, 6),
]
values = [5, 3, 7, 2, 4, 6, 1]

hld = HeavyLightDecomposition(7, edges, values)
print(hld.query_path(3, 6))
hld.update_path(3, 6, 2)
print(hld.query_subtree(1))
```

---

## 6. Real-World Use Cases

- **Network Operations** - Aggregate traffic or apply maintenance changes along a route in a hierarchy-shaped network.
- **Org Charts** - Query or update compensation totals across reporting chains.
- **Dependency Trees** - Analyze cumulative cost across a build or service dependency path.
- **Game Trees** - Maintain buffs or scores across parent-child quest paths.

---

## 7. References

- Heavy-Light Decomposition is a standard technique in advanced tree algorithm design.
- Pairing HLD with a lazy segment tree is the typical production implementation for path sum workloads.
