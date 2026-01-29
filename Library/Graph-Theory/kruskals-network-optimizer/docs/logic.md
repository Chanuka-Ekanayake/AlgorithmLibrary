# Algorithm Logic: Kruskal's Minimum Spanning Tree (MST)

## 1. The Core Concept

The goal of Kruskal's algorithm is to connect all nodes in a graph with the **minimum total edge weight** possible, without creating any cycles. In network engineering, this is used to find the most cost-effective way to link data centers, cities, or electrical grids.

Kruskal's is a **Greedy Algorithm**. It builds the MST by always picking the smallest available edge, provided it doesn't create a loop.

---

## 2. The Step-by-Step Process

1. **Initialize:** Treat every node as an individual, isolated tree (a "forest").
2. **Sort:** Sort all edges in the graph by their weight in ascending order.
3. **Iterate:** Take the edge with the smallest weight.
4. **Check for Cycles:**
* If the two nodes connected by the edge are already in the same tree, **discard** the edge (adding it would create a cycle).
* If they are in different trees, **merge** (Union) the two trees into one and add the edge to the MST.


5. **Terminate:** Stop when there are  edges in the MST, where  is the number of nodes.

---

## 3. The Engine: Disjoint Set Union (DSU)

To make cycle detection efficient, we use the DSU data structure. Without it, we would have to perform a full graph search (like BFS or DFS) every time we considered an edge, which would be incredibly slow.

### 3.1 Path Compression (The "Find" Optimization)

When we look for the "root" of a node, we make every node along the path point directly to the root. This flattens the tree structure, ensuring that future lookups happen in near-constant time.

### 3.2 Union by Rank (The "Merge" Optimization)

When merging two trees, we always attach the shorter tree to the root of the taller tree. This prevents the structure from becoming a long, inefficient chain.

---

## 4. Visualizing the "Greedy" Choice

Unlike Prim's algorithm, which grows a single tree from a starting point, Kruskal's can have multiple "islands" of connected nodes growing simultaneously across the map. Eventually, these islands are linked together by the smallest possible bridges.

---

## 5. Industrial Application: Data Center Interconnect (DCI)

In your 2026 portfolio project, Kruskal's logic is applied to **Regional Network Optimization**:

* **Nodes:** Geographic server locations (e.g., London, New York, Tokyo).
* **Edges:** The cost of laying high-speed fiber-optic cables between them.
* **The Result:** A blueprint for a global network that connects every hub for the absolute lowest infrastructure cost.

---

## 6. Logic Constraints

* **Undirected Graphs:** Kruskal's is designed for undirected graphs where connections are bidirectional.
* **Connectivity:** If the original graph is not connected, Kruskal's will find the Minimum Spanning Forest (the MST for each individual connected component).
