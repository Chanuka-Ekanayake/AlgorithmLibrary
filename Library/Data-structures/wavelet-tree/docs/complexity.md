# Complexity Analysis: Wavelet Tree

## 1. Time Complexity

Let `n` be the number of elements in the array and `V` be the number of **distinct values** (after coordinate compression).

| Operation | Time Complexity | Detail |
|---|---|---|
| **Build** | `O(n log V)` | Each of the `O(log V)` levels scans all `n` elements once. |
| **k-th Smallest** | `O(log V)` | Descends one root-to-leaf path; one O(1) lookup per level. |
| **Count Less Than** | `O(log V)` | The threshold x is binary-searched in `O(log V)`, then one path. |
| **Range Frequency** | `O(log V)` | Two `count_less_than` calls → `2 × O(log V)`. |
| **Range Median** | `O(log V)` | One `kth_smallest` call. |

### 1.1 Why O(log V) Per Query?

The tree has exactly `⌈log₂ V⌉` levels. At each level, the algorithm does:
- One prefix-array lookup (constant time, O(1))
- One index translation (constant time, O(1))
- One branch decision

So the total work per query is proportional to the tree depth, which is `O(log V)`.

> **Key difference from a Segment Tree:** A Segment Tree operates in `O(log n)` and is indexed by *position*. A Wavelet Tree operates in `O(log V)` and is indexed by *value range*. For order-statistics queries like "k-th smallest" the Wavelet Tree is the significantly simpler and more powerful choice.

---

## 2. Space Complexity

| Component | Space | Detail |
|---|---|---|
| **Prefix arrays (all levels)** | `O(n log V)` | Each level stores an array of length `n+1`. There are `O(log V)` levels. |
| **Node objects** | `O(V)` | At most `2V − 1` nodes in a full binary tree over `V` leaves. |
| **Coordinate compression map** | `O(V)` | Two arrays of length `V`: the sorted unique values and their ranks. |
| **Total** | **`O(n log V)`** | Dominated by the prefix arrays. |

For an array of 1,000,000 elements with 65,536 distinct values:
```
Space ≈ n × log₂(V) × sizeof(int) = 1e6 × 16 × 4 bytes ≈ 64 MB
```

---

## 3. Wavelet Tree vs. Alternative Approaches

| Query Type | Sorted Array | Merge Sort Tree | **Wavelet Tree** | Persistent Seg. Tree |
|---|---|---|---|---|
| k-th Smallest in Range | `O(n log n)` (re-sort) | `O(log² n)` | **`O(log V)`** | `O(log n)` |
| Count Less Than in Range | `O(n)` | `O(log² n)` | **`O(log V)`** | `O(log n)` |
| Range Frequency | `O(n)` | `O(log² n)` | **`O(log V)`** | `O(log n)` |
| Build Time | `O(n log n)` | `O(n log n)` | `O(n log V)` | `O(n log n)` |
| Space | `O(n)` | `O(n log n)` | `O(n log V)` | `O(n log n)` |
| Range Updates | ✗ | ✗ | ✗ | ✓ (with extra cost) |

**Key takeaway:** The Wavelet Tree wins on query speed when `V << n`, and its build cost is often lower than a Merge Sort Tree's.

---

## 4. Engineering Impact: When to Use It

Choose a Wavelet Tree when your problem requires:

1. **Order-statistics range queries** — "What is the median value in this data window?"
2. **Range frequency queries** — "How often does value X appear between indices L and R?"
3. **Threshold counting** — "How many readings exceeded the alert level in this sensor window?"
4. The dataset is **static** (no range updates needed).
5. Values come from a **dense integer range** or can be compressed to one.

### Real-World Scenarios

- **Sensor / IoT analytics** — Find the median or anomaly threshold across a sensor window without re-sorting on every query.
- **Database query engines** — Answer `SELECT COUNT(*) WHERE value < X AND id BETWEEN L AND R` in O(log V) after a one-time build.
- **Financial tick data** — "How many trades in time range [T1, T2] were below price P?" answered per millisecond.
- **Bioinformatics** — Count pattern occurrences within a genome substring (Wavelet Trees underlie the BWT-based FM-index).
- **Competitive programming** — Offline range k-th order queries in competitive contexts where `n` and `V` are both large.

---

## 5. Potential Optimizations

- **Bitwise level storage**: Replace prefix-count arrays with **bit arrays + O(1) rank/select** structures to reduce space to `O(n log V / word_size)` — this is the approach used in production succinct indices.
- **Pointer-free flat layout**: Store all levels in a single flat array (like a heap) to improve cache performance.
- **Persistent Wavelet Tree**: Version the structure to support queries on historical snapshots, supporting dynamic insertion at `O(log V)` per element.
- **Parallel build**: Each tree level is an independent pass over the array — trivially parallelizable.
