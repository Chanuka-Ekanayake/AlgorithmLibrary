# Red-Black Tree — Complexity Analysis

## Time Complexity

All core operations run in **worst-case** $O(\log n)$ time. This is a stronger guarantee than a Treap (which is only expected $O(\log n)$) because the Red-Black invariants enforce a deterministic height bound.

| Operation | Best Case | Average Case | Worst Case |
|-----------|-----------|--------------|------------|
| **Search** | $O(1)$ | $O(\log n)$ | $O(\log n)$ |
| **Insert** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ |
| **Delete** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ |

### Why is the height bounded?

The four Red-Black invariants guarantee that the **black-height** $bh$ (number of BLACK nodes on any root-to-leaf path) is the same for all paths. The minimum number of nodes in a tree of black-height $bh$ is $2^{bh} - 1$ (a perfectly full all-black tree). Since RED nodes cannot appear consecutively, the longest root-to-leaf path is at most $2 \cdot bh$ nodes long. Combining these:

$$n \geq 2^{bh} - 1 \implies bh \leq \log_2(n+1)$$

$$\text{height} \leq 2 \cdot bh \leq 2 \log_2(n+1) = O(\log n)$$

### Rotation budget

- **Insert fixup** performs at most **2 rotations** (Case 2 converts to Case 3, which terminates).
- **Delete fixup** performs at most **3 rotations** (Case 1 converts to 2/3/4; Case 3 converts to 4, which terminates).

The recoloring loop in insert and delete can propagate $O(\log n)$ levels up the tree, but each recolor is $O(1)$.

---

## Space Complexity

| Resource | Complexity |
|----------|------------|
| **Node storage** | $O(n)$ — one node per inserted key |
| **Sentinel NIL** | $O(1)$ — a single shared sentinel replaces all null pointers |
| **Call-stack depth** | $O(1)$ — all traversal and fixup routines are iterative (no recursion) |

### Comparison with Treap

| Property | Red-Black Tree | Treap |
|----------|---------------|-------|
| Height guarantee | **Worst-case** $O(\log n)$ | *Expected* $O(\log n)$ |
| Rotations per insert | ≤ 2 | $O(\log n)$ expected |
| Rotations per delete | ≤ 3 | $O(\log n)$ expected |
| Random state needed | No | Yes (priorities) |
| Implementation complexity | Higher | Lower |

The Red-Black Tree trades a more complex implementation for a stronger performance guarantee, making it the preferred choice in latency-sensitive applications such as Linux's Completely Fair Scheduler and Java's `TreeMap`.
