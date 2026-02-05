# Topological Sort - Algorithm Logic

## Overview
Topological Sort is a linear ordering of vertices in a Directed Acyclic Graph (DAG) where for every directed edge u → v, vertex u comes before v in the ordering. It's essential for scheduling tasks with dependencies.

## Core Concept
The algorithm arranges vertices such that all dependencies are satisfied - no task is scheduled before its prerequisites are completed.

## Key Properties
- **Only works on DAGs**: Graphs must be directed and acyclic
- **Multiple valid orderings**: A graph may have several valid topological sorts
- **Cycle detection**: If a cycle exists, topological sort is impossible

## Algorithm Approaches

### 1. DFS-Based Approach
**Intuition**: Visit nodes depth-first and add them to result after visiting all dependencies.

**Steps**:
1. Mark all vertices as unvisited
2. For each unvisited vertex, perform DFS
3. After visiting all neighbors, push vertex to stack
4. Reverse stack to get topological order

**Why it works**: A vertex is added to the stack only after all its descendants (dependencies) are processed.

### 2. Kahn's Algorithm (BFS-Based)
**Intuition**: Repeatedly remove vertices with no incoming edges.

**Steps**:
1. Calculate in-degree for all vertices
2. Add all vertices with in-degree 0 to queue
3. While queue is not empty:
   - Remove vertex from queue
   - Add to result
   - Reduce in-degree of all neighbors
   - Add neighbors with in-degree 0 to queue
4. If result size < total vertices, cycle exists

**Why it works**: Vertices with no dependencies can be processed first. As we process them, we "remove" them from the graph, exposing new vertices with no remaining dependencies.

## Cycle Detection
**DFS Color Method**:
- **White**: Unvisited vertex
- **Gray**: Currently being processed (in recursion stack)
- **Black**: Completely processed

If we encounter a **gray** vertex during DFS, we've found a back edge (cycle).

## Real-World Applications

### 1. Task Scheduling
- **Problem**: Schedule tasks where some tasks must complete before others
- **Example**: Build systems (compile A before B), project management

### 2. Course Prerequisites
- **Problem**: Order courses so prerequisites are taken first
- **Example**: CS101 → CS201 → CS301

### 3. Dependency Resolution
- **Problem**: Determine package installation order
- **Example**: Package managers (npm, pip, apt)

### 4. Compilation Order
- **Problem**: Compile source files in correct order
- **Example**: Java class dependencies, Makefile targets

## Example Walkthrough

### Graph:
```
    5 → 0 ← 4
    ↓       ↓
    2 → 3 → 1
```

### Dependencies:
- 5 → 0, 5 → 2
- 4 → 0, 4 → 1
- 2 → 3
- 3 → 1

### DFS Approach:
1. Start DFS from 5: 5 → 2 → 3 → 1 (push: 1, 3, 2, 5)
2. DFS from 4: 4 → 0 (push: 0, 4)
3. Stack: [1, 3, 2, 5, 0, 4]
4. Reverse: **[4, 0, 5, 2, 3, 1]** or **[5, 4, 2, 0, 3, 1]**

### Kahn's Approach:
1. In-degrees: [2, 2, 1, 1, 0, 0]
2. Queue: [4, 5]
3. Process 4: Remove 4, reduce in-degree of 0 and 1
4. Process 5: Remove 5, reduce in-degree of 0 and 2
5. Queue: [0, 2]
6. Continue until all processed
7. Result: **[4, 5, 0, 2, 3, 1]** or similar valid ordering

## Edge Cases
1. **Empty graph**: Return empty list
2. **Single vertex**: Return that vertex
3. **Disconnected components**: Process all components
4. **Cycle exists**: Return None or error
5. **All vertices independent**: Any order is valid

## Advantages
- **Linear time complexity**: O(V + E)
- **Cycle detection**: Built-in cycle checking (Kahn's)
- **Flexible**: Multiple algorithm variants available
- **Practical**: Solves real scheduling problems

## Choosing the Right Approach
- **DFS**: Simpler implementation, recursive
- **Kahn's**: Better for cycle detection, iterative, easier to understand
- **Both**: Have same time complexity O(V + E)
