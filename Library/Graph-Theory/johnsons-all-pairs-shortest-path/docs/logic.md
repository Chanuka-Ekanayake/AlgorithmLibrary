# Algorithm Logic: Johnson's All-Pairs Shortest Path

## 1. The Core Problem

Johnson's Algorithm solves the **All-Pairs Shortest Path (APSP)** problem:
> Find the shortest path between **every pair** of vertices in a weighted directed graph.

The twist? The graph may contain **negative edge weights** — making Dijkstra alone
insufficient — but **no negative cycles** (which would make shortest paths undefined).

| Challenge | How Johnson's Handles It |
|-----------|--------------------------|
| Negative weights | Reweights edges to be non-negative |
| Sparse graph | Runs Dijkstra (not Floyd-Warshall) per vertex |
| Negative cycles | Detects them via Bellman-Ford and raises an error |

---

## 2. The Key Insight: Reweighting

### 2.1 Why Dijkstra Fails on Negative Weights

Dijkstra's greedy assumption — *"once a vertex is settled, its distance is final"* — breaks
when negative edges can improve an already-settled vertex.

```
A --(-5)--> B --( 3)--> C
A --( 1)-------------> C

Dijkstra settles C=1 via A→C.
But true shortest is A→B→C = -5+3 = -2. ❌
```

### 2.2 Johnson's Reweighting Formula

Introduce a **potential function h[v]** (one value per vertex), and define:

```
w'(u, v) = w(u, v) + h[u] − h[v]
```

**Property:** If h satisfies `h[v] ≤ h[u] + w(u,v)` for all edges (i.e., h[u] is a
valid shortest-path estimate), then `w'(u,v) ≥ 0`.

**Critical math — path distance is preserved:**
```
For any path P = v₀ → v₁ → … → vₖ:

reweighted length = Σ w'(vᵢ, vᵢ₊₁)
                  = Σ (w(vᵢ, vᵢ₊₁) + h[vᵢ] − h[vᵢ₊₁])
                  = original_length + h[v₀] − h[vₖ]

The h[v₀] − h[vₖ] term is constant for any path from v₀ to vₖ.
∴ The *shortest* reweighted path = the *shortest* original path. ✅
```

---

## 3. Where h[v] Comes From — The Virtual Source Trick

Johnson's obtains h by:

1. **Adding a virtual vertex `s`** with a zero-weight edge to every vertex.
2. **Running Bellman-Ford from `s`**.
3. Setting `h[v] = dist(s, v)`.

Because `s` reaches every vertex in one hop with cost 0, `h[v] ≤ 0` for all v.

The relaxation condition `h[v] ≤ h[u] + w(u,v)` is guaranteed by Bellman-Ford's
shortest-path property — this is exactly what makes `w'(u,v) ≥ 0`.

---

## 4. Step-by-Step Walkthrough

### Example Graph

```
     ─ 2 ─
A ────────→ B
│           │
4│          │─3
↓           ↓
D ←── 1 ── C
```

Edges: A→B(2), A→D(4), B→C(−3), C→D(1)

---

### Phase 1 — Add virtual source `s`, run Bellman-Ford

```
s →(0)→ A,  s →(0)→ B,  s →(0)→ C,  s →(0)→ D

Bellman-Ford distances from s:
  h[A] = 0
  h[B] = 0   (s→B direct)
  h[C] = −3  (s→B→C = 0+(−3))
  h[D] = −2  (s→B→C→D = 0+(−3)+1)
```

---

### Phase 2 — Compute reweighted edge costs w'

```
w'(A,B) = 2  + h[A] − h[B] = 2  + 0 − 0  =  2  ✅
w'(A,D) = 4  + h[A] − h[D] = 4  + 0 −(−2)=  6  ✅
w'(B,C) = −3 + h[B] − h[C] =−3  + 0 −(−3)=  0  ✅
w'(C,D) = 1  + h[C] − h[D] = 1  +(−3)−(−2)= 0  ✅
```

All reweighted costs ≥ 0 → Dijkstra is now safe! 🎉

---

### Phase 3 — Run Dijkstra from every vertex

**Dijkstra from A (reweighted graph):**
```
d'[A]=0, d'[B]=2, d'[C]=2, d'[D]=2
```

**Recover true distances by reversing reweighting:**
```
dist(A,B) = d'[A,B] − h[A] + h[B] = 2 − 0 + 0  =  2
dist(A,C) = d'[A,C] − h[A] + h[C] = 2 − 0 +(−3)= −1
dist(A,D) = d'[A,D] − h[A] + h[D] = 2 − 0 +(−2)=  0
```

Shortest path A→C = A→B→C = 2+(−3) = **−1** ✅

---

## 5. Path Reconstruction

The `next_node` matrix stores the **first step** towards each destination:

```python
# During Dijkstra from source s:
if new_dist < dist[v]:
    dist[v] = new_dist
    prev[v] = u          # predecessor of v is u

# After Dijkstra, trace back from dest to source to find first hop
cur = dest
while prev[cur] != source:
    cur = prev[cur]
next_node[(source, dest)] = cur
```

**Reconstruction:**
```python
path = [start]
while path[-1] != end:
    path.append(next_node[(path[-1], end)])
return path
```

---

## 6. Negative Cycle Detection

Bellman-Ford detects negative cycles by running **one extra relaxation pass** after
V−1 passes:

```
If any edge (u,v) can still be relaxed after V−1 passes:
    → a negative cycle exists in the graph
    → no finite shortest paths exist
    → raise ValueError immediately
```

---

## 7. Pseudo-code

```
JOHNSON(Graph G = (V, E)):

  // Phase 1: Virtual source reweighting
  G' = G + vertex s + edges {(s,v,0) for all v in V}
  h = BELLMAN-FORD(G', s)
  if h is None:
      raise "Negative cycle detected"

  // Phase 2: Reweight all edges
  for each edge (u,v,w) in E:
      w'(u,v) = w + h[u] - h[v]   ← always ≥ 0

  // Phase 3: Dijkstra from every vertex
  for each u in V:
      d'[u] = DIJKSTRA(G_reweighted, u)
      for each v in V:
          dist[u][v] = d'[u][v] - h[u] + h[v]   ← true distance

  return dist
```

---

## 8. Edge Cases

| Scenario | Result |
|----------|--------|
| No edges | dist[u][v] = ∞ for all u ≠ v |
| Negative cycle | ValueError raised immediately |
| Graph with isolated vertices | dist = ∞ to/from isolated vertex |
| Only positive weights | Bellman-Ford returns h[v]=0 for all v (safe) |
| Self-loops (positive) | Ignored — dist[v][v] = 0 always |
| Multiple edges same pair | Minimum weight used automatically |

---

## 9. Comparison: Johnson's vs Floyd-Warshall

| Property | Johnson's | Floyd-Warshall |
|----------|-----------|----------------|
| Time (sparse, E ≈ V) | **O(V² log V)** ✅ | O(V³) ❌ |
| Time (dense, E ≈ V²) | O(V³ log V) ❌ | **O(V³)** ✅ |
| Space | O(V²) | O(V²) |
| Negative weights | ✅ Yes | ✅ Yes |
| Implementation | Moderate | Simple |
| Best for | **Sparse graphs** | Dense graphs |
