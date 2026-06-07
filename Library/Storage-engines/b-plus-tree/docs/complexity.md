# Complexity Analysis & Comparisons

This document analyzes the mathematical and computational efficiency of the B+ Tree and compares it with alternative storage indexing methods.

---

## 1. Complexity Table

For a B+ Tree of order $M$ containing $N$ keys:

| Operation | Best Case | Average Case | Worst Case | Space Complexity |
| --- | --- | --- | --- | --- |
| **Search (Point)** | $O(\log_M N)$ | $O(\log_M N)$ | $O(\log_M N)$ | $O(N)$ |
| **Search (Range)** | $O(\log_M N + K)$ | $O(\log_M N + K)$ | $O(\log_M N + K)$ | $O(N)$ |
| **Insertion** | $O(1)$ (No Split) | $O(\log_M N)$ | $O(\log_M N)$ (Propagating split) | $O(N)$ |
| **Deletion** | $O(1)$ (No Merge) | $O(\log_M N)$ | $O(\log_M N)$ | $O(N)$ |

*Note: $K$ is the number of keys matching the range query.*

### Why is Search Time Constrained?
Unlike Binary Search Trees (BST) which can become unbalanced ($O(N)$ search time), a B+ Tree is strictly self-balancing. Its height is guaranteed to be at most $\lceil \log_{\lceil M/2 \rceil} N \rceil$. With a typical page size of 4KB, $M$ (branching factor) can be in the hundreds, making the tree extremely flat (usually 3 to 4 levels for millions of rows), keeping point lookups extremely fast and consistent.

---

## 2. Comparison: B+ Tree vs. B-Tree vs. LSM-Tree

Different database engines optimize for different hardware constraints:

| Metric / Feature | B+ Tree | B-Tree | LSM-Tree (Log-Structured Merge-Tree) |
| --- | --- | --- | --- |
| **Read Performance** | Excellent ($O(\log_M N)$) | Good (but requires traversing upper-level nodes which can hold bulky data) | Slow (needs to check MemTable + multiple SSTables unless filtered by Bloom filters) |
| **Write Performance** | Moderate (requires random leaf node updates/splits) | Moderate (random write updates) | Extremely Fast (append-only writes to MemTable + Write-Ahead Log) |
| **Range Queries** | Best (leaves are linked sequentially; range search is a linear scan after initial lookup) | Poor (requires in-order tree traversal jumping back and forth across nodes) | Good (merges sorted runs, but requires reading multiple files) |
| **Space Utilization** | High (mostly packed node blocks, though splits can leave nodes 50% empty) | High | Highest (no fragmentation, though background compaction is needed) |
| **Real-World Engine** | SQLite, MySQL InnoDB, PostgreSQL | MongoDB (WiredTiger), Oracle DB | RocksDB, LevelDB, Apache Cassandra |
