# Complexity Analysis: Dijkstra's Algorithm

Understanding the performance boundaries of Dijkstra's algorithm is essential for implementing it in high-concurrency environments, such as real-time e-commerce logistics or network routing.

## 1. Time Complexity

The time complexity of this implementation is:


### 1.1 Why ?

The performance is determined by two main operations within the logic:

1. **Extracting the Minimum ():** We use a Binary Heap (Python's `heapq`). For every vertex () we visit, we perform a `heappop` operation.
2. **Relaxation of Edges ():** For every edge () in the graph, we potentially perform a `heappush` to update the distance to a neighbor.

**Total:** .

### 1.2 Comparison with Other Structures

| Data Structure | Time Complexity | Best For |
| --- | --- | --- |
| **Unordered List** |  | Dense graphs where . |
| **Binary Heap** |  | Standard, sparse graphs (Most real-world maps). |
| **Fibonacci Heap** |  | Theoretically fastest, but hard to implement. |

---

## 2. Space Complexity

The space complexity is:


### 2.1 Memory Usage Breakdown

* **Adjacency List:** Stores all vertices and edges, requiring  space.
* **Distances/Predecessors Dicts:** Each stores  elements, requiring  space.
* **Priority Queue:** In the worst case, it can hold  elements, requiring  space.

---

## 3. The "Big O" in Real-World Terms

To put this into a **Software Engineering** perspective, consider an e-commerce delivery system for a city:

* **Small City (, ):** The algorithm completes in microseconds.
* **Large Metropolis (, ):** The  factor keeps the computation time within a few milliseconds, making it suitable for real-time API responses.
* **Global Routing ():** At this scale, a single Dijkstra run might become slow. This is where engineers implement **Heuristics** (like A* Search) or **Graph Partitioning** to speed up the calculation.

---

## 4. Limitations & Constraints

1. **Non-Negative Weights:** Dijkstra **cannot** handle negative edge weights. If an edge has a negative value, the "Greedy" property breaks, and the algorithm may provide an incorrect shortest path.
* *Solution:* Use the **Bellman-Ford Algorithm** if negative weights are required.


2. **Single Source:** It only finds paths from *one* specific starting point.
* *Solution:* For "All-Pairs Shortest Path," use the **Floyd-Warshall Algorithm**.



---

## 5. Summary Table for Quick Reference

| Case | Complexity |
| --- | --- |
| **Best Case** |  (If the destination is the first neighbor explored) |
| **Average Case** |  |
| **Worst Case** |  |
| **Auxiliary Space** |  |