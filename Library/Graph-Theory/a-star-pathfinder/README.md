# A* Search Pathfinding Engine

## 1. Overview

The **A* (A-Star)** algorithm is an informed search strategy used for pathfinding and graph traversal. It is the industry standard for robotics, autonomous navigation, and real-time strategy games. By combining the actual distance traveled with a heuristic estimation, A* identifies the most efficient path significantly faster than uninformed algorithms like Dijkstra or Breadth-First Search.

This module demonstrates the application of A* within a **2D Occupancy Grid**, simulating the navigation logic required for a warehouse automation robot.

---

## 2. Technical Features

* **Informed Search:** Utilizes the  function to prioritize the most promising paths.
* **Admissible Heuristic:** Implements **Manhattan Distance** for grid-based movement to ensure the algorithm always finds the optimal path.
* **Obstacle Avoidance:** Robust handling of binary occupancy grids where specific coordinates are marked as impassable.
* **Optimized Performance:** Uses a binary heap-based Priority Queue (`heapq`) to ensure  extraction of the next node.

---

## 3. Architecture

```text
.
├── core/                  # Engine Logic
│   └── astar.py           # A* algorithm implementation and heuristics
├── docs/                  # Technical Documentation
│   ├── logic.md           # Deep dive into Informed Search and Heuristics
│   └── complexity.md      # Space and Time complexity analysis
├── test-project/          # Simulation Environment
│   ├── app.py             # Interactive CLI Navigator
│   ├── warehouse_grid.py  # Modular grid and obstacle definitions
│   └── instructions.md    # Operation manual
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric | Specification |
| --- | --- |
| **Time Complexity** | , bounded by the heuristic efficiency |
| **Space Complexity** | , required for the Open List and Closed Set |
| **Heuristic Function** | Manhattan Distance ( Norm) |
| **Optimality** | Guaranteed (Admissible Heuristic) |

---

## 5. Deployment & Usage

### Integration

The core engine can be imported into any coordinate-based system:

```python
from core.astar import astar_search

# 0 = Path, 1 = Wall
grid = [
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
]

path = astar_search(grid, (0, 0), (2, 2))
print(f"Optimal Path: {path}")

```

### Running the Simulator

To execute the Warehouse Navigation simulation:

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

* **Autonomous Mobile Robots (AMR):** Path planning in dynamic warehouse environments.
* **Geospatial Systems:** Route calculation in modern GPS and mapping software.
* **Game Artificial Intelligence:** Real-time NPC navigation around complex geometry.
* **Network Packet Routing:** Optimizing data transmission paths in telecommunications.