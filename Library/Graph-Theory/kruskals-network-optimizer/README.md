# Kruskal's Network Optimizer

## 1. Overview

**Kruskal's Algorithm** is a greedy graph algorithm used to find the **Minimum Spanning Tree (MST)** of a weighted, undirected graph. Its primary goal is to connect all vertices in a network with the minimum possible total edge weight, ensuring there are no cycles.

In modern systems engineering, this is the go-to logic for designing cost-effective physical networks, such as fiber-optic layouts, electrical grids, and regional data center interconnects (DCI).

---

## 2. Technical Features

* **Greedy Optimization:** Always selects the lowest-cost edge available that does not violate the "no-cycle" rule.
* **Optimized Cycle Detection:** Utilizes a **Disjoint Set Union (DSU)** data structure with **Path Compression** and **Union by Rank** for near-constant time operations.
* **Network Simulation:** Includes a `test-project` that calculates the optimal cabling route for a global data center network.
* **Scalability:** Efficiently handles sparse graphs with a time complexity of .

---

## 3. Architecture

```text
.
├── core/                  # Engine Logic
│   └── kruskal.py         # DSU structure and Kruskal's implementation
├── docs/                  # Technical Documentation
│   ├── logic.md           # Deep dive into cycle detection and DSU
│   └── complexity.md      # Analysis of sorting vs. union-find performance
├── test-project/          # Network Simulator
│   ├── app.py             # Regional Network Optimizer CLI
│   ├── locations.json     # Geographic dataset of server hubs
│   └── instructions.md    # Operation and testing guide
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric | Specification |
| --- | --- |
| **Time Complexity** |  |
| **Space Complexity** |  |
| **Paradigm** | Greedy Algorithm |
| **Sub-Structure** | Disjoint Set Union (DSU) |

---

## 5. Deployment & Usage

### Integration

The `KruskalMST` class can be integrated into any connectivity or clustering project:

```python
from core.kruskal import KruskalMST

# Format: (weight, u, v)
potential_connections = [(10, 0, 1), (20, 1, 2), (5, 0, 2)]
node_count = 3

mst, total_cost = KruskalMST.calculate_mst(node_count, potential_connections)
# Result: MST with edges (0, 2) and (0, 1) | Cost: 15

```

### Running the Simulator

To execute the Network Cost Optimization:

1. Navigate to the `test-project` directory:
```bash
cd test-project

```


2. Run the application:
```bash
python app.py

```



---

## 6. Industrial Applications

* **Telecommunications:** Designing the backbone of regional fiber networks to minimize trenching costs.
* **Cluster Analysis:** Used in Single-Linkage Hierarchical Clustering to identify data groupings.
* **Circuit Design:** Minimizing the length of wires needed to connect various components on a PCB or VLSI chip.
* **Logistics:** Planning pipeline routes for water, gas, or sewage systems across new urban developments.