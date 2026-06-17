# Fortune's Algorithm for Voronoi Diagrams

## 1. Overview

A **Voronoi Diagram** is a partition of a 2D plane into regions close to a set of generator points (sites). For each site, there is a corresponding cell consisting of all points closer to that site than to any other.

**Fortune's Algorithm** is a sweep-line algorithm that builds the Voronoi Diagram in $O(N \log N)$ time and $O(N)$ space. It is mathematically elegant and highly efficient, avoiding the $O(N^2)$ complexity of naive incremental construction.

---

## 2. Technical Features

- **$O(N \log N)$ Complexity**: Built using a sweep line moving top-to-bottom, keeping track of a parabolic beach line.
- **Robust Bounding Box Clipping**: Uses the Liang-Barsky line clipping algorithm to cleanly bound infinite rays and line segments.
- **Pure Python**: Zero third-party dependencies, structured with type hints and mathematical clarity.

---

## 3. Architecture

```text
.
├── core/                   # Geometry Engine
│   ├── __init__.py         # Package entry
│   └── fortunes_voronoi.py # Sweep-line implementation
├── docs/                   # Technical Documentation
│   ├── logic.md            # Parabolic intersections & math
│   └── complexity.md       # Event loop runtime analysis
├── test-project/           # Verification Suite
│   ├── app.py              # Visual SVG exporter & test runner
│   └── instructions.md     # Execution instructions
└── README.md               # Home documentation
```

---

## 4. Performance Specifications

| Metric | Specification |
| :--- | :--- |
| **Time Complexity** | **$O(N \log N)$** (priority queue & beach line lookup) |
| **Space Complexity** | **$O(N)$** (active arcs and event storage) |
| **Stability** | Robust handling of collinear sites & parallel boundaries |

---

## 5. Deployment & Usage

```python
from core.fortunes_voronoi import Point, fortunes_algorithm

# Define input sites
sites = [
    Point(100, 100), 
    Point(700, 200), 
    Point(400, 600)
]

# Compute Voronoi Diagram
diagram = fortunes_algorithm(sites)

print(f"Generated {len(diagram.vertices)} vertices:")
for v in diagram.vertices:
    print(f"Vertex at: {v}")

print(f"Generated {len(diagram.edges)} edges:")
for edge in diagram.edges:
    print(f"Edge from {edge.start} to {edge.end}")
```

---

## 6. Industrial Applications

- **Network Planning**: Placing wireless towers/cell towers such that each point in a city connects to the nearest station.
- **Robotics Pathfinding**: Identifying the "medial axis" (widest channels) between obstacles for safe robot traversal.
- **Geographic Information Systems (GIS)**: Analyzing catchment zones for public services, school districts, or delivery warehouses.
- **Procedural Generation**: Building natural-looking maps, country borders, and rivers in game development (using Lloyd's relaxation).
