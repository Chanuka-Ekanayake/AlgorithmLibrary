# Segment Tree with Lazy Propagation

## 1. Overview

The **Segment Tree with Lazy Propagation** is a powerful data structure that answers **range queries** (sum, min, max) and applies **range updates** — both in `O(log n)` time. It is the go-to choice whenever an algorithm must repeatedly ask "what is the total of elements X through Y?" and also modify ranges of elements efficiently.

This module demonstrates a production-grade implementation tailored for an **E-commerce Price Engine** where product prices must be queried and bulk-adjusted in real-time.

---

## 2. Key Engineering Features

- **O(log n) Range Updates** — Apply a value to any contiguous sub-array without visiting every element.
- **O(log n) Range Queries** — Retrieve the sum of any sub-array in logarithmic time.
- **Lazy Propagation** — Defers expensive tree-wide updates using "lazy tags," only resolving them when required.
- **Type-Safe Implementation** — Built with Python's `typing` module for maintainability and IDE support.
- **Zero Dependencies** — Pure Python standard library, no external packages needed.

---

## 3. Folder Architecture

```text
.
├── core/
│   └── segment_tree.py      # Core logic: Build, Update, Query, Lazy Push-Down
├── docs/
│   ├── logic.md             # How the tree and lazy propagation work step-by-step
│   └── complexity.md        # O(log n) analysis and comparison vs other structures
├── test-project/
│   ├── app.py               # 3 real-world scenarios + stress test
│   └── instructions.md      # How to run the simulation
└── README.md                # Module Entry Point (Current File)
```

---

## 4. Performance Benchmarks

| Operation | Time Complexity | Note |
|---|---|---|
| **Build** | `O(n)` | One pass bottom-up construction. |
| **Range Query** | `O(log n)` | At most `4 log n` nodes visited. |
| **Range Update** | `O(log n)` | Lazy tags avoid redundant work. |
| **Point Query** | `O(log n)` | Special case of range query. |
| **Point Update** | `O(log n)` | Special case of range update. |
| **Space** | `O(n)` | Two arrays of size `~4n`. |

---

## 5. Quick Start

### Basic Usage

```python
from core.segment_tree import SegmentTree

# Build tree from an array
prices = [999, 1499, 2499, 3999, 1299, 799, 4999, 2199]
st = SegmentTree(prices)

# Range sum query: total price of products 1–5
total = st.query(1, 5)
print(total)  # 9595

# Range update: apply a -200 discount to products 1–5
st.update(1, 5, -200)

# Query again after the discount
new_total = st.query(1, 5)
print(new_total)  # 8595

# Point query: price of product at index 3
print(st.point_query(3))  # 3799
```

### Run the Simulation

```bash
cd test-project
python app.py
```

---

## 6. Real-World Use Cases

- **Financial Systems** — Query traded volume over a date range; apply bulk corrections for corporate actions.
- **Gaming Leaderboards** — Grant score bonuses to an entire rank bracket; query bracket totals.
- **Database Engines** — Range `UPDATE` on indexed columns (e.g., `price += 5 WHERE id BETWEEN 100 AND 500`).
- **Image Processing** — Adjust brightness of a pixel sub-row; query average intensity of a region.
- **Competitive Programming** — Foundational structure for interval DP, geometry, and scheduling problems.
