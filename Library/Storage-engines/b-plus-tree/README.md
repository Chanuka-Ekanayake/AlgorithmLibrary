# B+ Tree Indexing Engine (Leaf-Linked)

## 1. Overview

The **B+ Tree Indexing Engine** is a read-optimized, self-balancing search tree designed for high-performance retrieval and disk-block storage layouts. 

In traditional relational databases (like MySQL InnoDB or SQLite), fast query lookups are achieved by storing rows in sorted order of their keys using a **B+ Tree**. By separating index-routing keys from the actual data records (which are kept strictly in leaf nodes) and connecting all leaf nodes sequentially, the B+ Tree optimizes both single point lookups and range scans.

---

## 2. Technical Features

* **Balanced Flat Architecture:** High branching factor ($M$) ensures the tree height remains small, keeping query costs minimal and deterministic.
* **Leaf-Level Linked List:** All leaf nodes are linked sequentially, enabling rapid range scans ($O(\log_M N + K)$) without traversing up and down the tree hierarchy.
* **Simulated Block I/O Metrics:** The implementation tracks simulated "Page Reads" and "Page Writes" to highlight B+ Tree performance.
* **Splitting & Propagation:** Automated leaf and internal node splits keep the tree fully balanced at all times.

---

## 3. Architecture

```text
.
├── core/                  # Core B+ Tree logic
│   ├── __init__.py        # Package initialization
│   └── bplus_tree.py      # B+ Tree splitting, searching, and range queries
├── docs/                  # Detailed documentation
│   ├── logic.md           # Node split mechanics & traversal logic
│   └── complexity.md      # Big O complexity & comparison with LSM-Trees
├── test-project/          # Database indexing simulator
│   ├── app.py             # ToyDB simulation script
│   └── instructions.md    # Instructions on running the simulator
└── README.md              # Main entry point documentation
```

---

## 4. Performance Specifications

| Metric | Specification | Description |
| --- | --- | --- |
| **Point Query Time** | $O(\log_M N)$ | Logarithmic search depth. |
| **Range Query Time** | $O(\log_M N + K)$ | Traverses straight to start key, then scans leaves sequentially. |
| **Space Overhead** | $O(N)$ | Extra space for routing nodes. |
| **Disk/Page Optimizations** | Block-aligned | Minimizes disk seek penalty by grouping keys into "pages". |

---

## 5. Deployment & Usage

### Integration Example

```python
from core.bplus_tree import BPlusTree

# Initialize a B+ Tree of order 4
db_index = BPlusTree(order=4)

# Insert records (key, value)
db_index.insert(1001, {"username": "alice", "email": "alice@email.com"})
db_index.insert(1005, {"username": "bob", "email": "bob@email.com"})

# Point lookup
user_data, page_reads = db_index.search(1001)
print(f"User found: {user_data} (Reads: {page_reads})")

# Range Scan
results, page_reads = db_index.search_range(1000, 1010)
print(f"Users in range: {results} (Reads: {page_reads})")
```

### Running the Simulator

To run the B+ Tree database simulator and view the index stats:

1. Navigate to the `test-project` directory:
   ```bash
   cd test-project
   ```
2. Run the simulation script:
   ```bash
   python app.py
   ```

---

## 6. Industrial Applications

* **Relational Databases:** The standard index driver for **MySQL InnoDB**, **PostgreSQL**, **SQLite**, and **Oracle**.
* **Filesystems:** Used to organize directory indices and file block addresses in **NTFS**, **ext4**, and **XFS**.
* **KV Stores:** High-speed clustered index organization in disk-based key-value stores.
