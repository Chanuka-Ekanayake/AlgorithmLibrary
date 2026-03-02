# Dinic's Algorithm (Maximum Flow)

## 1. Overview

When distributing heavy digital assets—like multi-gigabyte Machine Learning model weights—across a global Content Delivery Network (CDN), relying on basic pathfinding algorithms is a recipe for server bottlenecks. You do not just need a path to the buyer; you need to know the **absolute maximum data throughput** your entire infrastructure can sustain simultaneously across all available fiber-optic links.

**Dinic's Algorithm** is the industrial standard for solving the Maximum Flow problem. It outperforms older algorithms (like Ford-Fulkerson and Edmonds-Karp) by utilizing Breadth-First Search (BFS) to organize servers into rigid "Level Graphs" and Depth-First Search (DFS) to aggressively push data. By employing mathematical "Reverse Edges," it dynamically self-corrects bad routing decisions on the fly, guaranteeing maximum bandwidth utilization without infinitely looping.

---

## 2. Technical Features

- **Level Graph Structuring:** Uses BFS to assign a strict distance metric to every node. Data is mathematically forced to only flow "forward" toward the sink, entirely eliminating cyclic routing loops and wasted CPU cycles.
- **Dead-End Pruning:** During the flow-pushing phase, the engine tracks saturated connections using a pointer array. Once a path is full, it is permanently ignored for the rest of the phase, accelerating the DFS execution.
- **Residual Graph Self-Correction:** Automatically generates invisible reverse edges with 0 initial capacity. When flow is pushed forward, capacity is dynamically added backward, allowing the engine to push "negative flow" later to perfectly undo and redirect suboptimal routing decisions.
- **Bipartite Matching Speedup:** While it runs in $O(V^2 E)$ for general networks, it mathematically accelerates to a blistering $O(E \sqrt{V})$ when used to match independent sets, such as exclusively assigning $N$ buyers to $M$ available software license keys.

---

## 3. Architecture

```text
.
├── core/                  # Graph Routing Engine
│   ├── __init__.py        # Package initialization
│   └── network.py         # Level Graph (BFS) and Blocking Flow (DFS) implementation
├── docs/                  # Technical Documentation
│   ├── logic.md           # Residual graphs, phase transitions, and reverse edges
│   └── complexity.md      # O(V^2 E) bounds and comparisons to Edmonds-Karp
├── test-project/          # Global CDN Bandwidth Router Simulator
│   ├── app.py             # Calculates max ML model download speeds across edge servers
│   └── instructions.md    # Guide for evaluating network bottlenecks and throughput
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

Let $V$ be the number of Vertices (servers) and $E$ be the number of Edges (network cables).

| Metric               | General Network Specification | Bipartite Graph Specification |
| -------------------- | ----------------------------- | ----------------------------- |
| **Time Complexity**  | $O(V^2 E)$                    | $O(E \sqrt{V})$               |
| **Space Complexity** | $O(V + E)$                    | $O(V + E)$                    |
| **Flow Accuracy**    | 100% (Mathematical Maximum)   | 100% (Perfect Matching)       |

---

## 5. Deployment & Usage

### Integration

The `DinicMaxFlow` engine can be imported to power any backend service requiring throughput maximization or bipartite matching:

```python
from core.network import DinicMaxFlow

# 1. Initialize a network with 4 nodes (0=Datacenter, 3=Buyer)
cdn = DinicMaxFlow(4)

# 2. Add connections with specific bandwidth capacities (Gbps)
cdn.add_edge(0, 1, 10.0) # Datacenter -> US-East
cdn.add_edge(0, 2, 5.0)  # Datacenter -> US-West
cdn.add_edge(1, 2, 15.0) # US-East -> US-West
cdn.add_edge(1, 3, 5.0)  # US-East -> Buyer
cdn.add_edge(2, 3, 10.0) # US-West -> Buyer

# 3. Calculate absolute maximum theoretical throughput
max_bandwidth = cdn.calculate_max_flow(source=0, sink=3)
print(f"Maximum CDN Throughput: {max_bandwidth} Gbps")
# Output: Maximum CDN Throughput: 15.0 Gbps

```

### Running the Simulator

To observe the engine routing data through a complex topology of interconnected edge servers and identifying hidden network bottlenecks:

1. Navigate to the `test-project` directory:

```bash
cd test-project

```

2. Run the CDN Router Simulator:

```bash
python app.py

```

---

## 6. Industrial Applications

- **Content Delivery Networks (CDNs):** Calculating the maximum safe data flow across a global topology of edge servers to prevent targeted node failures during high-traffic product launches.
- **Bipartite Server Allocation:** Matching thousands of concurrent buyers to exclusive, containerized ML model instances in strict $O(E \sqrt{V})$ time.
- **Supply Chain Logistics:** Determining the maximum physical volume of hardware inventory that can be shipped through a constrained network of warehouses and transit routes.
