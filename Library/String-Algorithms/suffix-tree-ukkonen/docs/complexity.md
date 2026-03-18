# Suffix Tree Complexity Analysis

## 1. Time Complexity

Ukkonen's Algorithm has a worst-case time complexity of **O(N)** for a string of length $N$. This efficiency is achieved through several amortized techniques.

### Build (Amortized Analysis)
- **Incrementing Phase**: There are $N$ phases.
- **Rule 1 (Leaf Extensions)**: Performed in $O(1)$ by using a global `current_end`.
- **Rule 3 (Early Termination)**: Stops the current phase extension instantly, occurring at most $N$ times.
- **Rule 2 (Splitting Edges)**: Each split node and leaf is created only once. The total number of nodes is bounded by $2N$.
- **Skip/Count Trick**: The `active_node` only moves down the tree. The total number of downward steps across all phases is bounded by the final tree depth, which is $O(N)$.

### Search
- **Pattern Match**: Locating a pattern of length $M$ takes **O(M)**. We traverse the tree from the root, comparing at most $M$ characters.

---

## 2. Space Complexity

- **Storage**: **O(N)**.
- Each node stores a constant amount of information (start, end, suffix link, child pointers).
- With $N$ suffixes, the total number of edges/nodes is at most $2N - 1$.
- Total space is linear with respect to the input string.

---

## 3. Comparison with Suffix Array

| Metric | Suffix Tree (Ukkonen) | Suffix Array (Manber-Myers) |
| :--- | :--- | :--- |
| **Construction Time** | $O(N)$ | $O(N \log N)$ or $O(N)$ with advanced algo |
| **Search Time** | $O(M)$ | $O(M \log N)$ |
| **Space Overhead** | Large (many pointers/objects) | Small (integer arrays) |
| **Implementation** | Complex Logic | Simpler |
| **Best For** | Heavy string indexing (Bioinformatics) | Large-scale text search where memory is tight |
