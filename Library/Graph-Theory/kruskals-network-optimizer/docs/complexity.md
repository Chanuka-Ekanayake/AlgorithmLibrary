# Complexity Analysis: Kruskal's Algorithm

Kruskal's Algorithm is a greedy strategy used to find the **Minimum Spanning Tree (MST)**. Its efficiency is primarily determined by two factors: the sorting of edges and the performance of the cycle-detection mechanism.

## 1. Time Complexity

The overall time complexity is:


### 1.1 Parameter Breakdown

* **:** The number of vertices (nodes) in the graph.
* **:** The number of edges (connections) in the graph.

### 1.2 Step-by-Step Justification

1. **Edge Sorting:** The algorithm begins by sorting all  edges based on their weights. This takes ****.
2. **Union-Find Operations:** We iterate through the sorted edges and perform  and  operations.
* With **Path Compression** and **Union by Rank**, each DSU operation takes nearly constant time, specifically ****, where  is the inverse Ackermann function (which is  for all practical purposes).
* Total DSU time: ****.


3. **Total Complexity:** . Since  grows significantly faster than , the sorting step dominates.

---

## 2. Space Complexity

The space complexity is:


### 2.1 Memory Allocation

* **DSU Storage:** We maintain two arrays (`parent` and `rank`) of size ****.
* **Edge List:** Storing the graph and the resulting MST requires space proportional to ****.
* **Sorting Space:** Depending on the sorting algorithm used (e.g., Timsort in Python), additional temporary space of up to **** may be required.

---

## 3. Comparison: Kruskal's vs. Prim's

| Feature | Kruskal's Algorithm | Prim's Algorithm |
| --- | --- | --- |
| **Paradigm** | Edge-based (Greedy) | Vertex-based (Greedy) |
| **Data Structure** | Disjoint Set Union (DSU) | Priority Queue (Min-Heap) |
| **Best For** | **Sparse Graphs** (fewer edges) | **Dense Graphs** (many edges) |
| **Time Complexity** |  |  or  |

---

## 4. Engineering Trade-offs

* **Sorting Overhead:** The main bottleneck is sorting. If the edges are already sorted or the weights are in a small range (allowing for Linear Sorting), Kruskal's becomes exceptionally fast.
* **Disconnected Components:** Kruskal's naturally handles disconnected graphs by forming a "Minimum Spanning Forest," whereas Prim's would require manual restarts to cover all components.

---

## 5. Performance Metrics Table

| Metric | Complexity |
| --- | --- |
| **Best-Case Time** |  |
| **Average-Case Time** |  |
| **Worst-Case Time** |  |
| **Auxiliary Space** |  |