# Wavelet Tree

## 1. Overview

The **Wavelet Tree** is a succinct range query data structure that operates on a static integer array and answers order-statistics queries in `O(log V)` time per query — where `V` is the number of distinct values. It simultaneously indexes by *position* and *value*, enabling queries that neither a Segment Tree nor a Binary Search Tree can answer efficiently on their own.

This module is demonstrated through a **streaming sensor analytics** use case: a factory floor processes thousands of real-time readings per second, and operators query medians, thresholds, and value frequencies across rolling index windows — all without re-sorting.

---

## 2. Key Engineering Features

- **O(log V) Range Order-Statistics** — k-th smallest, count less than, range frequency, and range median in logarithmic time.
- **O(n log V) Build** — A single recursive partitioning pass per tree level.
- **Coordinate Compression** — Automatically remaps arbitrary integers to a compact range, keeping depth proportional to distinct value count, not magnitude.
- **Zero Dependencies** — Pure Python standard library; no external packages required.
- **Type-Safe Implementation** — Built with Python's `typing` module for IDE support and maintainability.

---

## 3. Folder Architecture

```text
.
├── core/
│   └── wavelet_tree.py      # Core logic: Build, k-th Smallest, Count Less Than, Range Frequency
├── docs/
│   ├── logic.md             # Recursive construction, index translation, query walk-throughs
│   └── complexity.md        # O(log V) analysis, space breakdown, comparison vs alternatives
├── test-project/
│   ├── app.py               # 3 real-world scenarios + stress test (300 random queries)
│   └── instructions.md      # How to run the simulation
└── README.md                # Module Entry Point (Current File)
```

---

## 4. Performance Benchmarks

| Operation | Time Complexity | Detail |
|---|---|---|
| **Build** | `O(n log V)` | One pass over n elements at each of log V levels. |
| **k-th Smallest** | `O(log V)` | One root-to-leaf descent; O(1) work per level. |
| **Count Less Than** | `O(log V)` | One root-to-leaf descent + O(log V) binary search for threshold. |
| **Range Frequency** | `O(log V)` | Two `count_less_than` calls. |
| **Range Median** | `O(log V)` | One `kth_smallest` call. |
| **Space** | `O(n log V)` | Prefix arrays stored at each of the log V levels. |

> `V` = number of **distinct values** in the array (after coordinate compression).

---

## 5. Quick Start

### Basic Usage

```python
from core.wavelet_tree import WaveletTree

readings = [72, 58, 85, 91, 63, 85, 77, 68, 85, 54, 90, 61]
wt = WaveletTree(readings)

# What is the median reading across sensors 2–9?
print(wt.range_median(2, 9))          # 77

# How many sensors in 0–7 are below the alert threshold of 75?
print(wt.count_less_than(0, 7, 75))   # 4

# How often does 85°C appear in sensors 3–11?
print(wt.range_frequency(3, 11, 85))  # 2

# What is the 2nd smallest reading in sensors 0–5?
print(wt.kth_smallest(0, 5, 2))       # 63
```

### Run the Simulation

```bash
cd test-project
python app.py
```

---

## 6. Real-World Use Cases

- **IoT & Sensor Systems** — Median and threshold analytics over rolling sensor windows without re-sorting per query.
- **Database Query Engines** — Answer `COUNT(*) WHERE value < X AND id BETWEEN L AND R` in built-once, query-many mode.
- **Financial Tick Data** — "How many trades in window [T1, T2] were under price P?" at millisecond latency.
- **Bioinformatics** — The Wavelet Tree underlies the FM-index (BWT-based full-text search), enabling O(log V) pattern search in compressed genomes.
- **Competitive Programming** — Canonical solution for offline range k-th-order queries where V and n are both large.
