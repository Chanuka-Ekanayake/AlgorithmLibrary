# Algorithm Logic: Kruskal's Minimum Spanning Tree

## 1. The Core Concept

**Kruskal's algorithm** builds a Minimum Spanning Tree (MST) by considering edges globally rather than growing from a single vertex. It sorts all edges by weight and greedily adds the cheapest edges that don't create cycles.

**Key Insight:** Process edges in order of cost, always choosing the cheapest available edge that connects two different components.

---

## 2. The Fundamental Principle: Greedy Edge Selection

### 2.1 Cut Property (Theoretical Foundation)

**Same as Prim's:** For any cut (S, V-S), the minimum-weight edge crossing the cut must be in **some** MST.

**Kruskal's Perspective:** At each step, we consider the global minimum edge. If it connects two different components, it's the minimum edge crossing the cut between those components → safe to add!

### 2.2 Why Greedy Works

**Proof Sketch:**
1. Sort edges: e₁, e₂, ..., eₘ (by weight)
2. At step i, we consider edge eᵢ = (u, v)
3. If u and v in different components:
   - There's a cut (component(u), V - component(u))
   - eᵢ is minimum edge crossing this cut (all smaller edges already processed)
   - By cut property → eᵢ is safe ✓
4. Result: MST with minimum total weight

---

## 3. Visual Walkthrough

### 3.1 Example Graph

```
    4       1       2
A ──── B ──── C ──── D
 \           / \     /
  3        4    5   9
   \      /      \ /
    ────F────────E
```

**Edges:** A-B=4, B-C=1, C-D=2, A-F=3, F-C=4, C-E=5, D-E=9

### 3.2 Step-by-Step Execution

**Step 0: Sort edges by weight**
```
Sorted: [(B,C,1), (C,D,2), (A,F,3), (A,B,4), (F,C,4), (C,E,5), (D,E,9)]
```

**Initial Components:** {A}, {B}, {C}, {D}, {E}, {F}

---

**Step 1: Process B-C (weight 1)**
```
Components before: {A}, {B}, {C}, {D}, {E}, {F}
B and C in different components? YES
Add B-C to MST ✓
Components after: {A}, {B,C}, {D}, {E}, {F}
MST edges: [(B,C,1)]
Cost: 1
```

---

**Step 2: Process C-D (weight 2)**
```
Components: {A}, {B,C}, {D}, {E}, {F}
C and D in different components? YES
Add C-D to MST ✓
Components after: {A}, {B,C,D}, {E}, {F}
MST edges: [(B,C,1), (C,D,2)]
Cost: 3
```

---

**Step 3: Process A-F (weight 3)**
```
Components: {A}, {B,C,D}, {E}, {F}
A and F in different components? YES
Add A-F to MST ✓
Components after: {A,F}, {B,C,D}, {E}
MST edges: [(B,C,1), (C,D,2), (A,F,3)]
Cost: 6
```

---

**Step 4: Process A-B (weight 4)**
```
Components: {A,F}, {B,C,D}, {E}
A and B in different components? YES
Add A-B to MST ✓
Components after: {A,F,B,C,D}, {E}
MST edges: [(B,C,1), (C,D,2), (A,F,3), (A,B,4)]
Cost: 10
```

---

**Step 5: Process F-C (weight 4)**
```
Components: {A,F,B,C,D}, {E}
F and C in different components? NO (both in {A,F,B,C,D})
Skip F-C ✗ (would create cycle)
```

---

**Step 6: Process C-E (weight 5)**
```
Components: {A,F,B,C,D}, {E}
C and E in different components? YES
Add C-E to MST ✓
Components after: {A,F,B,C,D,E} (all vertices)
MST edges: [(B,C,1), (C,D,2), (A,F,3), (A,B,4), (C,E,5)]
Cost: 15
```

**DONE:** Have V-1 = 5 edges, all vertices connected!

**Final MST:**
```
    4       1       2
A ──── B ──── C ──── D
 \                    
  3                   
   \                  
    F           5     
             ──── E   
```

---

## 4. Union-Find Data Structure

### 4.1 Why Union-Find?

**Problem:** How to check if two vertices are in the same component efficiently?

**Naive Solution:** DFS/BFS each time → O(V) per check → O(V × E) total ✗

**Smart Solution:** Union-Find → O(α(V)) per check → O(E × α(V)) total ✓

### 4.2 Union-Find Operations

**Two main operations:**

1. **Find(v):** Return the representative (root) of v's component
2. **Union(u, v):** Merge components containing u and v

**Initial State:**
```
Parent: A→A, B→B, C→C, D→D, E→E, F→F
(each vertex is its own parent/root)
```

**After adding B-C:**
```
Union(B, C):
  Find(B) = B
  Find(C) = C
  B ≠ C → merge components
  Make C's parent = B

Parent: A→A, B→B, C→B, D→D, E→E, F→F
```

**After adding C-D:**
```
Union(C, D):
  Find(C) = Find(B) = B (path: C→B)
  Find(D) = D
  B ≠ D → merge components
  Make D's parent = B

Parent: A→A, B→B, C→B, D→B, E→E, F→F
```

**After adding F-C (attempt):**
```
Union(F, C):
  Find(F) = F
  Find(C) = B (path: C→B)
  F ≠ B → would merge... but already same component!
  Actually: F→F, but C→B, so different → merge

Wait, let me recalculate after A-F and A-B...

After A-F: A→A, F→A, B→B, C→B, D→B, E→E
After A-B: Find(A)=A, Find(B)=B → merge
           Make B's parent = A
           Now: A→A, F→A, B→A, C→B→A, D→B→A, E→E

Now F-C:
  Find(F) = A (path: F→A)
  Find(C) = A (path: C→B→A)
  A = A → same component! Skip ✓
```

### 4.3 Path Compression

**Optimization:** When finding root, make all nodes on path point directly to root.

**Example:**
```
Before Find(C):
C → B → A (root)

After Find(C):
C → A
B → A
(path compressed)
```

**Benefit:** Future operations are faster!

### 4.4 Union by Rank

**Optimization:** Always attach smaller tree under larger tree.

**Rank:** Approximate tree height

```
Union by rank:
  rank[A] = 2, rank[B] = 1
  
  Before:       After:
    A    B        A
   / \   |       /|\
  •   •  •      • • B
                    |
                    •
```

**Benefit:** Keeps trees shallow → faster Find operations

---

## 5. Correctness Proof

### 5.1 Theorem: Kruskal's Produces MST

**Claim:** Kruskal's algorithm produces a minimum spanning tree.

**Proof by Induction:**

**Invariant:** After processing k edges, the selected edges form a subset of some MST.

**Base Case (k=0):** Empty set is subset of any MST ✓

**Inductive Step:** Assume invariant holds for k edges. Consider edge eₖ₊₁ = (u, v).

**Case 1:** u and v in same component
- Adding eₖ₊₁ would create cycle
- Skip it
- Invariant still holds (nothing changed) ✓

**Case 2:** u and v in different components
- Let S = component(u), T = component(v)
- eₖ₊₁ is minimum edge crossing cut (S, V-S)
  - Why? All smaller edges already processed
  - They either:
    - Connected vertices within S
    - Connected vertices within T
    - Connected other components
  - None crossed S-T cut (else u,v would be in same component)
- By Cut Property: eₖ₊₁ is in some MST
- By induction: Current edges are subset of MST M
- If eₖ₊₁ ∈ M, we're done ✓
- If eₖ₊₁ ∉ M:
  - M must have another edge e' crossing S-T cut
  - weight(eₖ₊₁) ≤ weight(e') (eₖ₊₁ is minimum)
  - Swapping e' for eₖ₊₁ gives another MST
  - So current edges ∪ {eₖ₊₁} is subset of MST ✓

**Conclusion:** Algorithm maintains invariant throughout. Final result (V-1 edges) is an MST. ∎

---

## 6. Cycle Detection with Union-Find

### 6.1 Why Union-Find Prevents Cycles

**Key Property:** Adding edge (u, v) creates cycle ⟺ u and v already in same component

**Proof:**
- **⟹** If cycle exists, there's path u → ... → v in current MST
  - So u and v are connected (same component) ✓
- **⟸** If u and v in same component, path exists u → ... → v
  - Adding (u, v) creates cycle: u → ... → v → u ✓

**Algorithm checks:** `Find(u) == Find(v)` → same component → would create cycle → skip!

### 6.2 Example of Cycle Prevention

```
Current MST:
    1       2
B ──── C ──── D

Components: {B,C,D}

Now consider edge B-D (weight 5):
  Find(B) = B (root)
  Find(D) = B (path: D→C→B)
  B == B → same component!
  
If we added B-D:
    1       2
B ──── C ──── D
 \_____5_____/
(creates triangle cycle)

Algorithm prevents this ✓
```

---

## 7. Comparison: Kruskal's vs Prim's

### 7.1 Algorithmic Differences

| Aspect | Kruskal's | Prim's |
|--------|-----------|--------|
| **Strategy** | Sort all edges globally | Grow tree from start vertex |
| **View** | Edge-centric | Vertex-centric |
| **Data Structure** | Union-Find | Priority Queue |
| **Edge Processing** | By weight order | By connection to current tree |
| **Starting Point** | None needed | Requires start vertex |

### 7.2 Example Showing Different Order

**Graph:**
```
   3        2
A ─── B ─── C
  \___ 1 ___/
```

**Kruskal's Order:**
1. A-C (1) - global minimum
2. B-C (2) - next minimum
Done!

**Prim's Order (start A):**
1. A-C (1) - minimum from A
2. B-C (2) - minimum from {A,C}
Done!

**Same MST, different process!**

### 7.3 When Each Wins

**Kruskal's Better:**
- Sparse graphs (E ≈ V)
- Edges already sorted
- Disconnected graphs
- Parallel processing possible

**Prim's Better:**
- Dense graphs (E ≈ V²)
- Starting from specific vertex
- Incremental construction
- Better cache locality

---

## 8. Time Complexity Breakdown

### 8.1 Detailed Analysis

```python
def kruskals_mst(graph):
    # Extract edges: O(E)
    edges = []
    for u in graph:
        for v in graph[u]:
            edges.append((weight, u, v))
    
    # Sort edges: O(E log E)
    edges.sort()
    
    # Initialize Union-Find: O(V)
    uf = UnionFind(vertices)
    
    # Process edges: O(E × α(V))
    for weight, u, v in edges:
        if uf.union(u, v):  # O(α(V))
            mst.append((u, v, weight))
            if len(mst) == V - 1:
                break
    
    # Total: O(E) + O(E log E) + O(V) + O(E α(V))
    #      = O(E log E) (dominant term)
```

### 8.2 Why O(E log E), not O(E log V)?

**Observation:** In simple graph, E ≤ V(V-1)/2 < V²

Therefore: log E ≤ log V² = 2 log V

So: O(E log E) = O(E log V) - **same asymptotic complexity!**

### 8.3 Union-Find Complexity

**α(n) = Inverse Ackermann function**

| n | α(n) |
|---|------|
| 10 | 2 |
| 100 | 3 |
| 10,000 | 4 |
| 10^80 (atoms in universe) | 5 |

**Practically:** α(n) ≤ 5 for all realistic inputs → **nearly constant time!**

---

## 9. Space Complexity

### 9.1 Memory Usage

| Component | Size | Description |
|-----------|------|-------------|
| Edge list | O(E) | All edges extracted |
| Union-Find parent | O(V) | One parent per vertex |
| Union-Find rank | O(V) | One rank per vertex |
| MST edges | O(V) | V-1 edges in result |
| **Total** | **O(V + E)** | Linear space |

---

## 10. Edge Cases & Considerations

### 10.1 Disconnected Graphs

**Problem:** MST undefined for disconnected graphs.

**Kruskal's Solution:** Naturally finds Minimum Spanning Forest!

```python
# Algorithm still works:
for weight, u, v in edges:
    if uf.union(u, v):
        mst.append((u, v, weight))

# Just stops early when len(mst) < V-1
# Each component gets its own MST
```

### 10.2 Negative Weights

**Works perfectly!** No issues like shortest path algorithms.

```
Example:
A ──-5── B ───3── C

MST: A-B (-5), B-C (3), total cost = -2
```

### 10.3 Equal Weight Edges

**Multiple valid MSTs may exist.**

```
   2        2
A ─── B ─── C

Two MSTs possible:
1. A-B (2), B-C (2)
2. A-B (2), A-C (2)  [if A-C exists with weight 2]

All have same total weight.
```

---

## 11. Real-World Intuition: Cable Network

### 11.1 Scenario

**Problem:** Connect 5 buildings with minimum cable cost.

**Costs:**
```
A-B: $100, A-C: $150
B-C: $80, B-D: $120
C-D: $90, C-E: $110
D-E: $70
```

### 11.2 Kruskal's Solution

**Step 1: Sort all possible cables by cost**
```
1. D-E: $70
2. B-C: $80
3. C-D: $90
4. A-B: $100
5. C-E: $110
6. B-D: $120
7. A-C: $150
```

**Step 2: Install cables in order (skip if creates loop)**

| Cable | Cost | Install? | Reason |
|-------|------|----------|--------|
| D-E | $70 | ✓ | First cable |
| B-C | $80 | ✓ | Connects new buildings |
| C-D | $90 | ✓ | Extends network |
| A-B | $100 | ✓ | Adds building A |
| C-E | $110 | ✗ | E already connected via D |
| B-D | $120 | ✗ | Would create loop B-C-D-B |
| A-C | $150 | ✗ | Not needed, have 4 cables |

**Final Network:**
```
A──$100──B──$80──C
               │
             $90│
               │
         E──$70──D

Total: $340
Savings: $660 - $340 = $320 (48%)
```

---

## 12. Optimality Guarantee

### 12.1 Greedy Choice Property

**At each step, Kruskal's makes the locally optimal choice (minimum weight edge).**

**This leads to global optimum because:**
1. Cut property guarantees each edge is safe
2. Processing in sorted order ensures minimum total weight
3. Union-Find ensures no cycles (maintains tree structure)

### 12.2 Uniqueness

**MST is unique ⟺ all edge weights are distinct**

**Proof:**
- If all weights distinct → only one edge crossing each cut has minimum weight
- Therefore only one valid MST ✓

**If ties exist:** Multiple MSTs possible, all with same total cost.

---

## 13. Algorithm Variations

### 13.1 Reverse-Delete Algorithm

**Idea:** Start with all edges, delete maximum weight edges that don't disconnect graph.

**Relationship:** Dual of Kruskal's
- Kruskal's: Add minimum edges
- Reverse-Delete: Remove maximum edges

**Same result:** Both produce MST!

### 13.2 Filtered Kruskal's

**Optimization:** Pre-filter obviously bad edges before sorting.

```python
# Remove edges heavier than any path between their endpoints
filtered_edges = [e for e in edges if not dominated(e)]
filtered_edges.sort()
# Then run standard Kruskal's
```

**Benefit:** Smaller edge set → faster sorting

---

## 14. Summary

**Kruskal's Algorithm = Sort & Unite**

**Core Idea:** Process edges cheapest-first, unite components without creating cycles.

**Key Properties:**
- ✅ Always finds MST
- ✅ O(E log E) time complexity
- ✅ Simple conceptual model
- ✅ Works on disconnected graphs
- ✅ Handles negative weights
- ❌ Slower than Prim's for dense graphs
- ❌ Requires global edge sorting

**When to use:** Need MST with edge-based approach, especially for sparse graphs or when edges are pre-sorted.
