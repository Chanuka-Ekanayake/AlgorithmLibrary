# Topological Sort - Complexity Analysis

## Time Complexity

### DFS-Based Approach
**O(V + E)** where V = vertices, E = edges

**Breakdown**:
- Visiting all vertices: O(V)
- Exploring all edges: O(E)
- Stack reversal: O(V)
- **Total**: O(V + E)

**Detailed Analysis**:
```
for each vertex:              O(V)
    if not visited:
        DFS(vertex):          O(E) total across all calls
            visit neighbors
            push to stack
            
reverse stack:                O(V)
```

### Kahn's Algorithm (BFS)
**O(V + E)** where V = vertices, E = edges

**Breakdown**:
- Calculate in-degrees: O(V + E)
- Initialize queue: O(V)
- Process each vertex once: O(V)
- Process each edge once: O(E)
- **Total**: O(V + E)

**Detailed Analysis**:
```
calculate in_degree:          O(V + E)
    for each vertex:          O(V)
        for each edge:        O(E)

initialize queue:             O(V)
    
while queue not empty:        O(V) iterations
    dequeue vertex:           O(1)
    add to result:            O(1)
    for each neighbor:        O(E) total
        reduce in_degree:     O(1)
        enqueue if needed:    O(1)
```

### Cycle Detection
**O(V + E)**
- DFS color method traverses all vertices and edges once

## Space Complexity

### DFS-Based Approach
**O(V)**

**Components**:
- Visited array: O(V)
- Recursion stack (worst case): O(V)
- Result stack: O(V)
- Adjacency list: O(V + E)
- **Total**: O(V + E) dominated by adjacency list

**Worst Case Recursion Depth**:
- Linear chain graph: O(V) depth
- Example: 0 → 1 → 2 → ... → n-1

### Kahn's Algorithm
**O(V + E)**

**Components**:
- In-degree array: O(V)
- Queue (max size): O(V)
- Result list: O(V)
- Adjacency list: O(V + E)
- **Total**: O(V + E)

### Cycle Detection
**O(V)**
- Color array: O(V)
- Recursion stack: O(V) worst case

## Comparison of Approaches

| Aspect | DFS | Kahn's (BFS) |
|--------|-----|--------------|
| Time | O(V + E) | O(V + E) |
| Space | O(V + E) | O(V + E) |
| Cycle Detection | Extra DFS needed | Built-in |
| Implementation | Recursive (simpler) | Iterative |
| Stack Depth | O(V) worst case | O(1) |

## Performance Characteristics

### Best Case
**O(V + E)**
- No matter the graph structure, must visit all vertices and edges
- Even disconnected or simple graphs require full traversal

### Average Case
**O(V + E)**
- Consistent performance across different graph structures

### Worst Case
**O(V + E)**
- Dense graphs (E ≈ V²): O(V²)
- Sparse graphs (E ≈ V): O(V)
- Still linear in terms of graph size

## Graph Density Impact

### Sparse Graphs (E ≈ V)
- Time: O(V)
- Common in trees and dependency graphs
- Most practical applications

### Dense Graphs (E ≈ V²)
- Time: O(V²)
- Less common for topological sort applications
- Example: Complete DAG

## Practical Performance

### Small Graphs (V < 100)
- **Execution time**: < 1ms
- Both algorithms perform identically
- Choose based on code readability

### Medium Graphs (100 < V < 10,000)
- **Execution time**: 1-100ms
- Performance difference negligible
- Kahn's might be slightly faster (no recursion overhead)

### Large Graphs (V > 10,000)
- **Execution time**: 100ms - seconds
- Kahn's algorithm preferred (iterative, no stack overflow risk)
- Memory usage becomes more significant

## Memory Optimization Tips

1. **Use iterative DFS instead of recursive**
   - Avoid stack overflow for deep graphs
   - Manual stack management

2. **In-place modifications**
   - Reuse in-degree array for other purposes
   - Clear queue after use

3. **Sparse graph representation**
   - Use adjacency lists, not matrices
   - Save O(V²) space

## Optimization Scenarios

### When to use DFS:
- Simple implementation needed
- Graph is shallow (low depth)
- Recursion is acceptable

### When to use Kahn's:
- Need built-in cycle detection
- Very deep graphs (avoid stack overflow)
- Prefer iterative solutions
- Need to count processed vertices

## Comparison with Other Sorting Algorithms

| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| Topological Sort | O(V + E) | O(V) | DAG ordering |
| QuickSort | O(n log n) | O(log n) | Array sorting |
| MergeSort | O(n log n) | O(n) | Array sorting |
| BFS | O(V + E) | O(V) | Level-order traversal |
| DFS | O(V + E) | O(V) | Graph traversal |

## Real-World Performance Example

### Build System (1000 files, 5000 dependencies):
```
Graph size: V = 1000, E = 5000
Expected time: ~5-10ms
Memory usage: ~50KB

Operations:
- Create graph: 2ms
- Topological sort: 3ms
- Convert to names: 2ms
```

### Course Scheduling (500 courses, 1000 prerequisites):
```
Graph size: V = 500, E = 1000
Expected time: ~2-5ms
Memory usage: ~25KB
```

## Scalability
- **Linear scalability**: Doubles vertices → doubles time
- **Excellent for large graphs**: No exponential blow-up
- **Bounded memory**: Predictable space requirements
- **Cache-friendly**: Sequential memory access patterns (Kahn's)
