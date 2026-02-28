# Fenwick Tree (Binary Indexed Tree)

## 1. Overview

As an e-commerce platform scales, serving real-time analytics—such as tracking cumulative revenue over the last 30 days or monitoring the live bandwidth consumed by ML model downloads—becomes computationally expensive. Standard arrays offer fast updates but slow sum queries. Prefix arrays offer fast queries but slow updates.

The **Fenwick Tree**, or Binary Indexed Tree (BIT), is the industrial solution to this bottleneck. It is a highly memory-efficient data structure that mathematically balances the workload, executing both point updates and prefix sum queries in strict time. It achieves this by delegating responsibility for specific data ranges to specific indices based entirely on their binary representation.

---

## 2. Technical Features

- **Blazing-Fast Operations:** Locks both data updates and cumulative sum queries at time, allowing dashboards to process thousands of live transactions per second without lag.
- **Bitwise Navigation:** Replaces slow loops and heavy tree-node objects with pure bitwise operations. It utilizes the Two's Complement trick () to instantly isolate the Least Significant Bit (LSB) and traverse the mathematical tree structure.
- **Minimal Memory Footprint:** Operates entirely within a flat, 1-dimensional array of size . Unlike a Segment Tree which requires memory allocation, the Fenwick Tree has strictly structural overhead.
- ** Linear Initialization:** Features a bulk-build protocol to ingest massive historical datasets in a single linear pass, bypassing the expensive cost of inserting records one by one.

---

## 3. Architecture

```text
.
├── core/                  # Analytics Data Structure
│   ├── __init__.py        # Package initialization
│   └── bit.py             # Point updates, prefix queries, and range queries
├── docs/                  # Technical Documentation
│   ├── logic.md           # Two's Complement and LSB isolation mechanics
│   └── complexity.md      # O(log N) bounds and memory efficiency vs Segment Trees
├── test-project/          # Real-Time Sales Analytics Simulator
│   ├── app.py             # Live high-frequency transaction processing
│   └── instructions.md    # Guide for evaluating range queries and zero-lag updates
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Operation               | Time Complexity | Space Complexity         |
| ----------------------- | --------------- | ------------------------ |
| **Point Update**        |                 |                          |
| **Prefix Query**        |                 |                          |
| **Range Query**         |                 |                          |
| **Bulk Initialization** |                 | (for the internal array) |

---

## 5. Deployment & Usage

### Integration

The `FenwickTree` can be imported to power any backend service requiring continuous stream ingestion and live range metrics:

```python
from core.bit import FenwickTree

# 1. Initialize with 10 days of historical sales data
historical_sales = [1200, 1500, 900, 2200, 3100, 1800, 2500, 1700, 2900, 3400]
sales_tree = FenwickTree.build_from_array(historical_sales)

# 2. Query the total revenue from Day 3 to Day 7
q_revenue = sales_tree.query_range(3, 7)
print(f"Mid-week Revenue: ${q_revenue}")

# 3. Process a live transaction on Day 10 (Add $500)
sales_tree.add(10, 500)

# 4. Instantly get the updated Year-To-Date total
ytd = sales_tree.query_prefix(10)
print(f"Updated YTD Revenue: ${ytd}")

```

### Running the Simulator

To observe the engine ingesting historical data and processing a burst of live transactions while instantly updating dashboard metrics:

1. Navigate to the `test-project` directory:

```bash
cd test-project

```

2. Run the Analytics Simulator:

```bash
python app.py

```

---

## 6. Industrial Applications

- **High-Frequency Trading:** Maintaining live, cumulative order-book volumes that must be updated and queried in sub-millisecond timeframes.
- **E-Commerce Dashboards:** Powering real-time revenue, traffic, and inventory metric displays across arbitrary date ranges (e.g., "Last 7 Days", "Q3 Total").
- **Network Telemetry:** Monitoring cumulative bandwidth consumption per user or microservice, ensuring instant cut-offs when API rate limits or data caps are exceeded.
