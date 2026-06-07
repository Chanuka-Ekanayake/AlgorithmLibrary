# Running the ToyDB Index Simulator

This simulation demonstrates how a B+ Tree index accelerates lookups and range queries in a mock database.

### 1. Prerequisites

Make sure you have Python installed:
```bash
python --version
```

### 2. Execution

Run the simulation script directly from this directory:
```bash
python app.py
```

### 3. What to Audit in the Output

* **Tree Visualizer:** Witness the tree restructuring and balance itself as new users are registered.
* **Point Query Cost:** Observe how finding a user in a dataset requires only 2–3 "page reads", compared to scanning the whole database.
* **Range Scan Efficiency:** Notice how scanning a range of users traverses directly to the start node and follows leaf links, requiring only a fraction of node reads.
