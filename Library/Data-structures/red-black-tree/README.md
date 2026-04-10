# Red-Black Tree

A Red-Black Tree is a **self-balancing Binary Search Tree** that enforces four structural coloring invariants to guarantee $O(\log n)$ worst-case performance for search, insert, and delete — regardless of the insertion order.

Unlike a Treap (which relies on random priorities for *expected* balance), the Red-Black Tree provides a **deterministic height bound**: no root-to-leaf path can be more than twice as long as any other. This makes it the data structure of choice in latency-sensitive systems — it underpins Java's `TreeMap` / `TreeSet`, C++ STL `std::map`, and the Linux kernel's Completely Fair Scheduler.

## Quick File Structure

1. `core/red_black_tree.py`: Full implementation of the Red-Black Tree — node structure, rotations, insert/delete fixup, search, and in-order traversal.
2. `docs/logic.md`: Detailed explanation of the four invariants, the sentinel NIL node, and the step-by-step logic of each fixup case.
3. `docs/complexity.md`: Time and space complexity analysis, height bound proof, rotation budget, and a feature comparison with the Treap.
4. `test-project/`: A runnable simulation covering insertions, searches, deletions, duplicate handling, and a sequential-insert stress test.
