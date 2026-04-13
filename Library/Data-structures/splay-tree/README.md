# Splay Tree

A **Splay Tree** is a self-balancing Binary Search Tree that optimizes for recently accessed elements through a **splaying operation**. After any access (search, insert, delete), the accessed node is rotated to the root, making it O(1) to access again immediately. This makes splay trees extremely efficient for workloads where certain elements are accessed frequently.

Unlike Red-Black Trees which enforce strict color-based invariants, or Treaps which use randomized priorities, splay trees use **adaptive rebalancing**: the tree shape changes based on access patterns. This provides **amortized O(log n)** performance for all operations, with exceptional performance for skewed access patterns.

Splay trees are used in:
- **Ordered sets/maps with temporal locality** (custom associative containers optimized for repeated accesses)
- **Network routers** (splaying improves cache locality)
- **Data compression** (Move-To-Front encoding)
- **Self-adjusting algorithms** where access patterns dominate

## Quick File Structure

1. `core/splay_tree.py`: Complete implementation — node structure, splay operation, search, insert, delete, and helper rotations.
2. `docs/logic.md`: Step-by-step explanation of the splay operation, zig/zig-zig/zig-zag cases, and how splaying maintains balance implicitly.
3. `docs/complexity.md`: Amortized analysis, O(log n) per operation, comparison with Red-Black Trees and Treaps.
4. `test-project/`: Runnable simulation with insertions, searches, deletions, and stress tests demonstrating adaptive performance.
