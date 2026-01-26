# Algorithm Logic: Floyd-Warshall All-Pairs Shortest Path

## 1. The Core Concept

The **Floyd-Warshall algorithm** is a classic example of **Dynamic Programming** applied to graph theory. It computes the shortest paths between **all pairs of vertices** by systematically considering each vertex as a potential intermediate point in paths.

The key insight: If the shortest path from i to j goes through vertex k, then the subpaths i→k and k→j must also be shortest paths.

---

## 2. The Fundamental Principle

### 2.1 Dynamic Programming Formulation

**State Definition:**  
`dist[i][j][k]` = shortest path from i to j using only vertices {1, 2, ..., k} as intermediates

**Recurrence Relation:**
```
dist[i][j][k] = min(
    dist[i][j][k-1],                    // Path not using vertex k
    dist[i][k][k-1] + dist[k][j][k-1]   // Path through vertex k
)
```

**Base Case:**  
`dist[i][j][0]` = weight of edge (i, j) if it exists, else ∞

**Goal:**  
`dist[i][j][V]` = shortest path from i to j (can use any vertex as intermediate)

### 2.2 Space Optimization

We can optimize the 3D array to 2D by observing that we only need the previous "layer":

```python
# Instead of dist[i][j][k], use dist[i][j]
# Update in-place as we only need k-1 values
for k in vertices:
    for i in vertices:
        for j in vertices:
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

This reduces space from O(V³) to O(V²).

---

## 3. Visual Walkthrough

### 3.1 Example Graph

```
    1
A ──→ B
│     │
4│     │2
│     ↓
↓     D
C ←──
   3
```

### 3.2 Initialization (k = 0)

Distance matrix with direct edges only:

```
     A    B    C    D
A    0    1    4    ∞
B    ∞    0    ∞    2
C    ∞    ∞    0    ∞
D    ∞    ∞    3    0
```

### 3.3 Iteration 1: Consider A as Intermediate

**Question:** Can any path be improved by going through A?

Check all pairs (i, j):
- B→C: `dist[B][C]` vs `dist[B][A] + dist[A][C]` = ∞ vs ∞+4 → No change
- B→D: Already has path B→D=2, B→A→D=∞ → No change
- ...no improvements

Matrix stays the same.

### 3.4 Iteration 2: Consider B as Intermediate

**Can paths improve by going through B?**

- A→D: `dist[A][D]=∞` vs `dist[A][B] + dist[B][D] = 1+2 = 3` ✓ **Update!**

```
     A    B    C    D
A    0    1    4    3  ← Updated
B    ∞    0    ∞    2
C    ∞    ∞    0    ∞
D    ∞    ∞    3    0
```

### 3.5 Iteration 3: Consider C as Intermediate

**Can paths improve through C?**

- A→D: Current=3, via C = `dist[A][C] + dist[C][D]` = 4+∞ → No
- ...no improvements

### 3.6 Iteration 4: Consider D as Intermediate

**Can paths improve through D?**

- A→C: Current=4, via D = `dist[A][D] + dist[D][C] = 3+3 = 6` → No improvement
- B→C: Current=∞, via D = `dist[B][D] + dist[D][C] = 2+3 = 5` ✓ **Update!**

**Final Matrix:**

```
     A    B    C    D
A    0    1    4    3
B    ∞    0    5    2
C    ∞    ∞    0    ∞
D    ∞    ∞    3    0
```

---

## 4. Why Does This Work?

### 4.1 Mathematical Proof

**Theorem:** After k iterations, `dist[i][j]` contains the shortest path from i to j using only vertices {1, 2, ..., k} as intermediates.

**Proof by Induction:**

**Base Case (k=0):** Only direct edges, which is correct.

**Inductive Step:** Assume true for k-1. For iteration k:
- Either the shortest path doesn't use k → dist[i][j][k-1] is correct
- Or it uses k → path is i→...→k→...→j
  - Subpath i→k must be shortest using {1..k-1} (inductive hypothesis)
  - Subpath k→j must be shortest using {1..k-1} (inductive hypothesis)
  - Therefore dist[i][k][k-1] + dist[k][j][k-1] is optimal through k

By induction, theorem holds for all k. ∎

### 4.2 Optimal Substructure

Key DP property: **Shortest paths have shortest subpaths**

If shortest path A→D is A→B→D, then:
- A→B must be shortest path from A to B
- B→D must be shortest path from B to D

This property allows us to build solutions incrementally.

---

## 5. Loop Order Matters!

### 5.1 Correct Order: k-i-j

```python
for k in vertices:      # MUST be outermost
    for i in vertices:
        for j in vertices:
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

**Why?** We must fully consider vertex k as an intermediate for ALL pairs before moving to k+1.

### 5.2 Wrong Order: i-j-k (INCORRECT!)

```python
for i in vertices:
    for j in vertices:
        for k in vertices:
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

**Problem:** This updates dist[i][j] using inconsistent k values. We might use vertex k as intermediate before we've finished computing paths involving k.

---

## 6. Path Reconstruction

### 6.1 Next Matrix

To reconstruct paths, maintain a `next[i][j]` matrix:

```python
# Initialization
for i, j with direct edge:
    next[i][j] = j

# During update
if dist[i][k] + dist[k][j] < dist[i][j]:
    dist[i][j] = dist[i][k] + dist[k][j]
    next[i][j] = next[i][k]  # Follow path from i towards k
```

### 6.2 Reconstructing the Path

```python
def get_path(next, i, j):
    if next[i][j] is None:
        return []  # No path
    
    path = [i]
    while i != j:
        i = next[i][j]
        path.append(i)
    return path
```

**Example:**  
If shortest A→D goes A→B→D:
- next[A][D] = B (first step towards D from A)
- next[B][D] = D (last step)

Reconstruction: A → next[A][D]=B → next[B][D]=D ✓

---

## 7. Negative Cycle Detection

### 7.1 The Principle

After running Floyd-Warshall, if any `dist[v][v] < 0`, a negative cycle exists.

**Why?** 
- Initially, dist[v][v] = 0 (vertex to itself)
- If dist[v][v] becomes negative, there's a cycle from v back to v with negative weight

### 7.2 Example

```
A → B (weight -1)
B → C (weight -1)
C → A (weight -1)

After Floyd-Warshall:
dist[A][A] = -3  (cycle A→B→C→A has weight -3)
dist[B][B] = -3
dist[C][C] = -3
```

All vertices in the cycle will have negative self-distance.

---

## 8. Comparison with Other Algorithms

### 8.1 vs Dijkstra (Run V Times)

**Dijkstra V times:**
- Time: O(V × E log V) = O(V²log V) for sparse graphs
- Space: O(V)
- Limitation: Cannot handle negative weights

**Floyd-Warshall:**
- Time: O(V³)
- Space: O(V²)
- Handles negative weights

**When to use what:**
- Sparse graph (E << V²) + positive weights → V × Dijkstra
- Dense graph (E ≈ V²) → Floyd-Warshall
- Need negative weight support → Floyd-Warshall or Bellman-Ford

### 8.2 vs Bellman-Ford (Run V Times)

**Bellman-Ford V times:**
- Time: O(V² × E) = O(V⁴) for dense graphs
- Space: O(V)

**Floyd-Warshall:**
- Time: O(V³) ✓ Better for dense graphs
- Space: O(V²)

### 8.3 vs Johnson's Algorithm

**Johnson's Algorithm:**
- Time: O(V²log V + VE) = O(V²log V) for sparse graphs
- Reweights graph, then runs Dijkstra V times
- Complex implementation

**Floyd-Warshall:**
- Time: O(V³)
- Simple implementation
- Better for dense graphs

---

## 9. Real-World Intuition: City Road Network

### 9.1 The Scenario

You have a road network with 5 cities: {A, B, C, D, E}

**Direct Roads:**
```
A→B: 100 km
B→C: 80 km
A→C: 200 km (highway, but long)
C→D: 50 km
D→E: 60 km
```

**Question:** What's the shortest route from A to E?

### 9.2 Floyd-Warshall Process

**k=A:** Can any route improve by going through A?
- B→C: Direct=80 vs via A=∞ → No

**k=B:** Routes through B?
- A→C: Direct=200 vs A→B→C=100+80=180 ✓ Better!

**k=C:** Routes through C?
- A→D: Direct=∞ vs A→C→D=180+50=230 ✓

**k=D:** Routes through D?
- A→E: Direct=∞ vs A→D→E=230+60=290 ✓

**k=E:** No improvements.

**Result:** A→E shortest path = 290 km via A→B→C→D→E

---

## 10. Edge Cases & Considerations

### 10.1 Disconnected Graphs

If no path exists from i to j, `dist[i][j]` remains ∞.

This is correct behavior - use it to detect connectivity.

### 10.2 Self-Loops

Self-loops (edge from v to v) are handled naturally:
- Positive self-loop: Ignored (dist[v][v] stays 0)
- Negative self-loop: Detected as negative cycle

### 10.3 Multiple Edges

If multiple edges exist between i and j, initialization should use the minimum weight edge.

---

## 11. Pseudocode

```text
FLOYD-WARSHALL(Graph G):
    // Step 1: Initialize
    FOR each vertex v in G:
        dist[v][v] ← 0
        next[v][v] ← v
    
    FOR each edge (u, v) with weight w in G:
        dist[u][v] ← w
        next[u][v] ← v
    
    FOR all other pairs (i, j):
        dist[i][j] ← ∞
        next[i][j] ← NULL
    
    // Step 2: Main Loop
    FOR k = 1 to V:
        FOR i = 1 to V:
            FOR j = 1 to V:
                IF dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] ← dist[i][k] + dist[k][j]
                    next[i][j] ← next[i][k]
    
    // Step 3: Check for negative cycles
    FOR each vertex v in G:
        IF dist[v][v] < 0:
            RETURN "Negative cycle detected"
    
    RETURN dist, next
```

---

## 12. Applications in Software Engineering

### 12.1 Network Routing (OSPF, BGP)

Routers use Floyd-Warshall variants to compute routing tables showing the next hop for any destination.

### 12.2 Game Development

Precompute pathfinding costs between all locations for AI navigation.

### 12.3 Social Network Analysis

- **Closeness Centrality:** Sum of distances from a node to all others
- **Network Diameter:** Maximum shortest path length
- **Graph Density:** Ratio of connected pairs

### 12.4 Transportation Planning

Optimize bus routes, delivery schedules, and logistics networks.

---

## 13. Advanced Variants

### 13.1 Minimax Path (Bottleneck Shortest Path)

Find path minimizing the maximum edge:

```python
dist[i][j] = min(dist[i][j], max(dist[i][k], dist[k][j]))
```

**Use case:** Network bandwidth optimization.

### 13.2 Maximum Reliability Path

Find most reliable path (maximizing product of edge reliabilities):

```python
# Convert to logs: product becomes sum
reliability[i][j] = max(reliability[i][j], 
                        reliability[i][k] * reliability[k][j])
```

### 13.3 Transitive Closure

Boolean version to find reachability:

```python
reach[i][j] = reach[i][j] OR (reach[i][k] AND reach[k][j])
```

---

## 14. Summary

**Floyd-Warshall = Dynamic Programming on Graph Paths**

**Core Idea:**  
Systematically consider each vertex as a potential intermediate point, updating all pairs of paths that can benefit.

**Key Properties:**
- ✅ Solves all-pairs shortest path problem
- ✅ Handles negative weights
- ✅ Detects negative cycles
- ✅ Simple implementation
- ❌ O(V³) time limits scalability
- ❌ O(V²) space for large graphs

**When to use:** Dense graphs with < 5,000 vertices where you need comprehensive distance information.
