# Push-Relabel Algorithm (Maximum Flow & Minimum Cut)

## 1. Overview

In dense networks and mesh topologies—such as multi-core semiconductor interconnects, dense telecommunications backbones, and distributed cross-cloud ingestion meshes—traditional augmenting-path algorithms (Ford-Fulkerson, Edmonds-Karp, and Dinic's) incur significant CPU overhead by continually traversing the entire network end-to-end to find paths.

The **Push-Relabel Algorithm (Goldberg-Tarjan)** solves the Maximum Flow and Minimum Cut problems by abandoning global path searches in favor of **localized vertex operations**. Modeling fluid dynamics under gravity, nodes maintain an internal reservoir ("preflow") and an elevation ("height"). Excess flow is pushed downhill along residual edges, and vertices are dynamically lifted ("relabeled") when water accumulates. This achieves superior asymptotic and practical performance, particularly on dense graphs ($E \approx V^2$).

---

## 2. Technical Features

- **Highest-Label Selection ($O(V^2 \sqrt{E})$):** Uses an array of height buckets to always discharge the highest active vertex first, minimizing non-saturating pushes.
- **Gap Heuristic Pruning:** Detects empty height levels (`count[h] == 0`) and automatically lifts disconnected vertices above the source height ($V$), accelerating convergence by bypassing redundant relabels.
- **Strict Flow Conservation Guarantee:** Excess flow that cannot reach the sink is elevated above height $V$ and drained back to the source, ensuring net zero excess across all intermediate vertices.
- **Automated Min-Cut Isolation:** Performs residual reachability analysis post-convergence to segment the network into Source ($S$) and Sink ($T$) partitions, pinpointing exact structural bottlenecks.
- **Edge-Level Telemetry:** Exposes granular per-edge flow utilization metrics, distinguishing saturated links from under-utilized pathways.

---

## 3. Architecture

```text
.
├── core/                  # Push-Relabel Core Engine
│   ├── __init__.py        # Package exports
│   └── push_relabel.py    # Preflow, Height Buckets, Gap Heuristic & Min-Cut logic
├── docs/                  # In-Depth Technical Documentation
│   ├── logic.md           # Reservoir fluid dynamics, Push/Relabel operations & heuristics
│   └── complexity.md      # O(V^2 sqrt(E)) proofs and comparison with Dinic's/Edmonds-Karp
├── test-project/          # Cloud Ingestion Mesh Simulator
│   ├── app.py             # Simulates distributed data ingestion and bottleneck analysis
│   └── instructions.md    # Guide for running and testing the simulator
└── README.md              # Documentation Entry Point
```

---

## 4. Performance Specifications

Let $V$ be the number of Vertices (nodes/routers) and $E$ be the number of Edges (channels/links).

| Metric | Sparse Graph ($E = O(V)$) | Dense Graph ($E = O(V^2)$) |
| :--- | :--- | :--- |
| **Push-Relabel (Highest-Label)** | $O(V^{2.5})$ | **$O(V^3)$** |
| **Dinic's Algorithm** | $O(V^3)$ | $O(V^4)$ |
| **Edmonds-Karp** | $O(V^3)$ | $O(V^5)$ |
| **Space Complexity** | $O(V + E)$ | $O(V + E)$ |
| **Flow Optimality** | 100% (Mathematical Maximum) | 100% (Mathematical Maximum) |

---

## 5. Deployment & Usage

### Integration

Import the engine into any Python service requiring maximum flow routing or bottleneck detection:

```python
from core.push_relabel import PushRelabelMaxFlow

# 1. Initialize a network with 4 nodes (0=Source, 3=Sink)
router = PushRelabelMaxFlow(num_nodes=4)

# 2. Define directional channel capacities (Gbps)
router.add_edge(source=0, target=1, capacity=10.0)
router.add_edge(source=0, target=2, capacity=5.0)
router.add_edge(source=1, target=2, capacity=15.0)
router.add_edge(source=1, target=3, capacity=5.0)
router.add_edge(source=2, target=3, capacity=10.0)

# 3. Compute maximum throughput
max_flow = router.calculate_max_flow(source=0, sink=3)
print(f"Maximum Throughput: {max_flow:.2f} Gbps")

# 4. Extract Min-Cut partitions to identify bottlenecks
source_cut, sink_cut = router.get_min_cut(source=0)
print(f"Bottleneck Partition - S: {source_cut}, T: {sink_cut}")
```

### Running the Simulator

To test the engine under an interconnected multi-region cloud mesh scenario:

1. Navigate to the `test-project` directory:
   ```bash
   cd test-project
   ```

2. Run the pipeline optimizer:
   ```bash
   python app.py
   ```

---

## 6. Industrial Applications

- **Semiconductor & VLSI Circuit Design:** Pin-routing, wire-density congestion reduction, and signal flow optimization on integrated circuits.
- **Cross-Region Cloud Ingestion:** Maximizing data lake ingestion bandwidth across multi-hop transit nodes while identifying saturated cross-connects.
- **Image Segmentation & Computer Vision:** Min-cut graph partitioning for background/foreground segmentation in medical imaging and video processing.
- **Bipartite & Transportation Scheduling:** Assigning distributed workloads to server clusters under strict capacity constraints.
