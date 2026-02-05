# Topological Sort - Task Scheduler & Dependency Resolver

## Overview
Topological Sort is a fundamental graph algorithm that produces a linear ordering of vertices in a Directed Acyclic Graph (DAG) such that for every directed edge u → v, vertex u comes before v in the ordering. It's essential for solving scheduling and dependency resolution problems.

## Problem Statement
Given a set of tasks with dependencies, determine a valid order to execute all tasks such that each task is executed only after all its dependencies are completed.

## Real-World Applications

### 1. Build Systems 🛠️
**Problem**: Compile source files in the correct order
- Determine which files to compile first based on dependencies
- Ensure header files are processed before implementation files
- Used in: Make, CMake, Gradle, Maven

### 2. Course Prerequisites 🎓
**Problem**: Schedule courses for a degree program
- Take prerequisite courses before advanced courses
- Plan semester-by-semester course load
- Optimize graduation timeline

### 3. Package Managers 📦
**Problem**: Install software packages in dependency order
- Install base libraries before dependent packages
- Prevent missing dependency errors
- Used in: pip, npm, apt, yum

### 4. Task Scheduling 📋
**Problem**: Execute project tasks in correct sequence
- Complete prerequisite tasks before dependent tasks
- Optimize project timeline
- Resource allocation planning

### 5. Module Import Resolution 📚
**Problem**: Resolve module dependencies in programming
- Detect circular imports
- Determine load order for modules
- Prevent runtime errors

## Algorithm Approaches

### 1. DFS-Based (Depth-First Search)
```
1. Perform DFS from each unvisited vertex
2. After exploring all neighbors, add vertex to stack
3. Reverse stack to get topological order
```
**Pros**: Simple recursive implementation
**Cons**: Requires extra step for cycle detection

### 2. Kahn's Algorithm (BFS-Based)
```
1. Calculate in-degree for all vertices
2. Add vertices with in-degree 0 to queue
3. Process queue: remove vertex, reduce neighbor in-degrees
4. Repeat until queue is empty
```
**Pros**: Built-in cycle detection, iterative
**Cons**: Slightly more complex setup

## Features
- ✅ **Two Algorithm Implementations**: DFS and Kahn's (BFS)
- ✅ **Cycle Detection**: Identifies circular dependencies
- ✅ **Named Vertex Support**: Work with task names instead of indices
- ✅ **Multiple Use Cases**: 5 real-world examples
- ✅ **Comprehensive Documentation**: Logic and complexity analysis

## Time Complexity
- **Both Algorithms**: O(V + E)
  - V = number of vertices (tasks)
  - E = number of edges (dependencies)

## Space Complexity
- **O(V + E)** for adjacency list representation
- **O(V)** for auxiliary data structures

## Project Structure
```
topological-sort-task-scheduler/
├── core/
│   └── topological_sort.py      # Algorithm implementation
├── docs/
│   ├── logic.md                 # Algorithm explanation
│   └── complexity.md            # Performance analysis
├── test-project/
│   ├── app.py                   # 5 real-world examples
│   └── instructions.md          # How to run
└── README.md                    # This file
```

## Quick Start

### Installation
No external dependencies required - uses only Python standard library.

### Running Examples
```bash
cd test-project
python app.py
```

### Basic Usage
```python
from core.topological_sort import TopologicalSort

# Create graph with 6 vertices
topo = TopologicalSort(6)

# Add dependencies (u -> v means v depends on u)
topo.add_edge(5, 2)  # Task 2 depends on task 5
topo.add_edge(5, 0)
topo.add_edge(4, 0)
topo.add_edge(4, 1)
topo.add_edge(2, 3)
topo.add_edge(3, 1)

# Get topological order
order = topo.topological_sort_kahn()
print(order)  # Output: [4, 5, 0, 2, 3, 1] (one valid ordering)
```

### Using Named Tasks
```python
from core.topological_sort import topological_sort_with_names

tasks = ["Install OS", "Install Python", "Install Django", "Run App"]
dependencies = [
    ("Install OS", "Install Python"),
    ("Install Python", "Install Django"),
    ("Install Django", "Run App"),
]

order = topological_sort_with_names(tasks, dependencies)
print(order)  
# Output: ['Install OS', 'Install Python', 'Install Django', 'Run App']
```

### Cycle Detection
```python
topo = TopologicalSort(3)
topo.add_edge(0, 1)
topo.add_edge(1, 2)
topo.add_edge(2, 0)  # Creates cycle!

if topo.has_cycle():
    print("Circular dependency detected!")
```

## Example Output

### Build System
```
BUILD SYSTEM - File Compilation Order
=====================================

✓ Build Order:
  1. Compile utils.py
  2. Compile config.py
  3. Compile database.py
  4. Compile models.py
  5. Compile api.py
  6. Compile main.py
```

### Course Planner
```
COURSE PLANNER - Semester Schedule
==================================

✓ Recommended Course Sequence:

  Semester 1:
    • CS101 - Intro to Programming
    • MATH101 - Calculus I

  Semester 2:
    • CS102 - Data Structures
    • MATH201 - Discrete Math

  Semester 3:
    • CS201 - Algorithms
    • CS202 - Database Systems
  ...
```

## Key Concepts

### Directed Acyclic Graph (DAG)
- **Directed**: Edges have direction (A → B)
- **Acyclic**: No cycles (cannot return to a vertex through directed edges)
- Topological sort only works on DAGs

### In-Degree
- Number of incoming edges to a vertex
- Vertices with in-degree 0 have no dependencies
- Can be executed immediately

### Multiple Valid Orderings
- A graph may have several valid topological sorts
- All orderings respect dependency constraints
- Different algorithms may produce different valid results

## When to Use

✅ **Use Topological Sort When**:
- Tasks have dependency relationships
- Need to find execution order
- Want to detect circular dependencies
- Working with DAGs

❌ **Don't Use When**:
- Graph has cycles (use cycle detection first)
- Graph is undirected
- Need shortest path (use Dijkstra/Bellman-Ford)
- Need all paths (use DFS/BFS)

## Performance Characteristics

| Graph Size | Vertices | Edges | Time |
|------------|----------|-------|------|
| Small | < 100 | < 1000 | < 1ms |
| Medium | 100-10K | 1K-100K | 1-100ms |
| Large | > 10K | > 100K | > 100ms |

## Advantages
- ✅ Linear time complexity O(V + E)
- ✅ Works on disconnected graphs
- ✅ Multiple algorithm choices
- ✅ Built-in cycle detection (Kahn's)
- ✅ Easy to understand and implement

## Limitations
- ❌ Only works on DAGs
- ❌ Multiple valid orderings (non-deterministic)
- ❌ Doesn't optimize for specific criteria
- ❌ No parallel execution insights

## Comparison with Other Algorithms

| Algorithm | Purpose | Time | Works on Cycles? |
|-----------|---------|------|------------------|
| Topological Sort | Task ordering | O(V+E) | No |
| Dijkstra | Shortest path | O(E log V) | No negative edges |
| DFS | Traversal | O(V+E) | Yes |
| BFS | Level-order | O(V+E) | Yes |

## Extensions & Variations

1. **All Topological Orderings**: Find all valid orderings (backtracking)
2. **Lexicographic Topological Sort**: Smallest lexical ordering
3. **Parallel Task Scheduling**: Maximum parallelism analysis
4. **Critical Path Method (CPM)**: Project scheduling with task durations

## Contributing
Follow the existing structure when adding examples or optimizations.

## Related Algorithms
- **DFS (Depth-First Search)**: Base algorithm for DFS approach
- **BFS (Breadth-First Search)**: Base algorithm for Kahn's approach
- **Strongly Connected Components**: Related to cycle detection
- **Critical Path Method**: Extends topological sort with time constraints

## References
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms)
- [Graph Algorithms - Wikipedia](https://en.wikipedia.org/wiki/Topological_sorting)

## License
See root repository LICENSE file.
