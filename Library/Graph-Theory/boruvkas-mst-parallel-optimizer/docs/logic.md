# Algorithm Logic: Borůvka's Minimum Spanning Tree (MST)

## 1. The Core Concept

The goal of Borůvka's algorithm is to connect all nodes in a graph with the **minimum total edge weight** possible, without creating any cycles. It achieves this through a unique **component-merging** strategy that operates in parallel rounds.

Borůvka's is the **oldest MST algorithm** (1926), predating both Kruskal's (1956) and Prim's (1957). Its original motivation was designing an optimal electrical power network for Moravia (Czech Republic).

---

## 2. The Step-by-Step Process

1. **Initialize:** Treat every node as an individual, isolated component (a "forest" of single-node trees).
2. **For each component:** Find the minimum-weight edge that connects it to a **different** component. This step is inherently parallelizable — each component's search is independent.
3. **Merge:** Add all identified cheapest edges to the MST and merge the corresponding components using Union-Find.
4. **Repeat:** Go back to Step 2 with the reduced set of components.
5. **Terminate:** Stop when only one component remains (all vertices are connected).

---

## 3. Why Components Halve Each Round

This is the key insight that guarantees O(log V) rounds:

- In each round, **every** component finds at least one outgoing edge.
- That edge connects it to another component.
- After merging, two components become one.
- Therefore, the number of components is **at most halved** each round.
- Starting with V components: V → V/2 → V/4 → ... → 1
- This takes at most **⌈log₂ V⌉** rounds.

---

## 4. The Engine: Disjoint Set Union (DSU)

To efficiently track which vertices belong to which component and to merge components, we use the DSU data structure — the same one used in Kruskal's algorithm.

### 4.1 Path Compression (The "Find" Optimization)

When we look for the "root" of a node, we make every node along the path point directly to the root. This flattens the tree structure, ensuring that future lookups happen in near-constant time.

### 4.2 Union by Rank (The "Merge" Optimization)

When merging two components, we always attach the shorter tree to the root of the taller tree. This prevents the structure from becoming a long, inefficient chain.

---

## 5. Visualizing Component Merging

### Round-by-Round Execution

Consider a graph with 6 vertices:

```
    A ──3── B ──5── C
    |       |       |
    7       2       6
    |       |       |
    D ──4── E ──1── F
```

**Round 0 — Initial State:**
Components: {A}, {B}, {C}, {D}, {E}, {F}

**Round 1 — Each component picks cheapest outgoing edge:**
- {A}: cheapest is A-B (3)
- {B}: cheapest is B-E (2)
- {C}: cheapest is C-B (5)
- {D}: cheapest is D-A (7) — but A-D also = D-E (4), pick D-E (4)
- {E}: cheapest is E-F (1)
- {F}: cheapest is F-E (1)

**Edges selected:** E-F(1), B-E(2), A-B(3), D-E(4)

**After merging:** {A, B, D, E, F} and {C}
Components remaining: 2

**Round 2 — Each component picks cheapest outgoing edge:**
- {A,B,D,E,F}: cheapest to {C} is B-C (5)
- {C}: cheapest to {A,B,D,E,F} is C-B (5)

**Edge selected:** B-C(5)

**After merging:** {A, B, C, D, E, F}
Components remaining: 1 → **DONE**

**MST:** E-F(1) + B-E(2) + A-B(3) + D-E(4) + B-C(5) = **15**

---

## 6. The Parallelism Advantage

### 6.1 Why Borůvka's Is Naturally Parallel

In Kruskal's, edges must be processed in sorted order — this is inherently **sequential**. In Prim's, the priority queue grows from a single tree — also **sequential**.

In Borůvka's, each component's cheapest-edge search is **independent**:

```
Round k:
  Component 1 → search cheapest edge → O(edges in component 1)
  Component 2 → search cheapest edge → O(edges in component 2)
  Component 3 → search cheapest edge → O(edges in component 3)
  ...
  All searches run IN PARALLEL
  Total work per round: O(E)
  Total rounds: O(log V)
```

### 6.2 MapReduce Implementation Pattern

```
MAP Phase:    For each edge (u, v, w), emit:
              (component(u), (w, u, v))
              (component(v), (w, u, v))

REDUCE Phase: For each component, find minimum edge
              Emit merge instruction

MERGE Phase:  Update component assignments
```

This maps perfectly to distributed frameworks like Hadoop, Spark, or Pregel.

---

## 7. Handling Duplicate Edge Weights

If two edges have the same weight, the algorithm might select contradictory edges. The standard solution is **tie-breaking by edge identity**:

- Assign each edge a unique ID (e.g., lexicographic order of endpoints).
- When weights are equal, prefer the edge with the smaller ID.
- This guarantees a unique MST and avoids ambiguity.

Our implementation handles this by consistent comparison ordering.

---

## 8. Correctness Proof

### 8.1 The Safe Edge Lemma

**Lemma:** The minimum-weight edge crossing any cut is safe to add to the MST.

**Borůvka's applies this lemma simultaneously to all cuts** defined by the current components. Each component's cheapest outgoing edge crosses the cut (component, everything else), so by the lemma, it is safe to add.

### 8.2 Termination

- Each round merges at least one pair of components.
- The number of components strictly decreases.
- When one component remains, all vertices are connected.
- The result has exactly V-1 edges (a spanning tree).

### 8.3 Optimality

- Every edge added is the minimum crossing some cut.
- By the Cut Property, each such edge belongs to some MST.
- Therefore, the result is an MST. ∎

---

## 9. Logic Constraints

* **Undirected Graphs:** Borůvka's is designed for undirected graphs where connections are bidirectional.
* **Connectivity:** If the original graph is not connected, Borůvka's will find the Minimum Spanning Forest (the MST for each individual connected component).
* **Edge Uniqueness:** For guaranteed uniqueness of the MST, edge weights should be distinct (or tie-breaking must be applied).

---

## 10. Industrial Application: Parallel Network Design

In the test-project, Borůvka's logic is applied to **Global Data Center Interconnect Optimization**:

* **Nodes:** Geographic data center locations (e.g., London, New York, Tokyo, Singapore).
* **Edges:** The cost of laying high-speed fiber-optic cables between them.
* **Parallelism:** Each regional team independently identifies their cheapest cross-region link.
* **The Result:** A blueprint for a global network that connects every hub for the absolute lowest infrastructure cost, computed in O(log V) parallel rounds.
