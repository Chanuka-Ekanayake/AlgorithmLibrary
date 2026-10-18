# Complexity Analysis: Push-Relabel Maximum Flow

The Push-Relabel algorithm represents an asymptotic shift from global augmenting paths to localized node operations. By working with height labels and preflows, the bounds are governed strictly by the number of relabels and saturating/non-saturating pushes.

---

## 1. Time Complexity

Let $V = |V|$ be the number of vertices and $E = |E|$ be the number of edges.

| Strategy / Variant                     | Time Complexity          | Performance Characteristic                                 |
| -------------------------------------- | ------------------------ | ---------------------------------------------------------- |
| **Generic Push-Relabel**               | $O(V^2 E)$               | Arbitrary vertex selection for discharge.                  |
| **FIFO Push-Relabel**                  | $O(V^3)$                 | First-In-First-Out active node queue.                      |
| **Highest-Label Push-Relabel (This)**  | **$O(V^2 \sqrt{E})$**    | Bucket queue prioritizing vertices with maximum height.    |
| **Dense Networks ($E \approx V^2$)**   | **$O(V^3)$**             | Drastically beats augmenting-path algorithms.              |

---

## 2. Rigorous Bound Breakdown

The overall runtime is composed of three operations:

### 2.1 Bound on Relabel Operations: $O(V^2)$
- The height of the source is initialized to $V$, and the sink is fixed at $0$.
- Any node $u \neq s, t$ only relabels while it has excess. If it cannot reach the sink, its excess must return to the source. The shortest path in the residual graph back to the source has length at most $V - 1$.
- Therefore, the height $h(u)$ of any vertex never exceeds $2V - 1$.
- Each relabel strictly increases $h(u)$ by at least 1.
- With $V - 2$ intermediate nodes and a maximum height of $2V$, the total number of relabel calls across the entire execution is at most:
  $$(V - 2) \times (2V - 1) = O(V^2)$$

### 2.2 Bound on Saturating Pushes: $O(V E)$
- An edge $(u, v)$ undergoes a saturating push when $\Delta = c_f(u, v)$, reducing its residual capacity to zero.
- For $(u, v)$ to undergo another saturating push, flow must first be pushed in the opposite direction along $(v, u)$, which requires $h(v) = h(u) + 1$.
- Between successive saturating pushes on the same directed edge, $h(u)$ must increase by at least 2.
- Since $h(u) \le 2V - 1$, each edge can experience at most $V$ saturating pushes.
- Total saturating pushes over all $2E$ directed edges is bounded by:
  $$2E \times V = O(V E)$$

### 2.3 Bound on Non-Saturating Pushes: $O(V^2 \sqrt{E})$
- A non-saturating push exhausts the excess $e(u)$ to $0$ without saturating the edge $(u, v)$.
- By always discharging the vertex with the **highest label**, the potential function $\Phi = \max \{ h(u) \mid e(u) > 0 \}$ can be used to show that the number of non-saturating pushes is strictly bounded by $O(V^2 \sqrt{E})$.
- When combined with $O(1)$ bucket transitions, the overall runtime evaluates to $O(V^2 \sqrt{E})$.

---

## 3. Algorithm Comparison Matrix

| Algorithm | Asymptotic Complexity | Sparse Graph ($E = O(V)$) | Dense Graph ($E = O(V^2)$) | Algorithmic Paradigm |
| :--- | :--- | :--- | :--- | :--- |
| **Ford-Fulkerson** | $O(E \times |f_{\max}|)$ | Weak (capacity-dependent) | Extremely Slow | Global DFS Augmenting Paths |
| **Edmonds-Karp** | $O(V E^2)$ | $O(V^3)$ | $O(V^5)$ | Global BFS Shortest Augmenting Paths |
| **Dinic's Algorithm** | $O(V^2 E)$ | $O(V^3)$ | $O(V^4)$ | Level Graphs + Blocking Flow |
| **Push-Relabel (Highest Label)** | **$O(V^2 \sqrt{E})$** | **$O(V^{2.5})$** | **$O(V^3)$** | Local Preflow + Height Relabeling |

### Why Push-Relabel Excels on Dense Topologies:
In fully connected or mesh architectures (such as crossbar network switches, VLSI microchips, and dense data center clusters), $E \approx V^2$:
- Edmonds-Karp runs in $O(V^5)$.
- Dinic's Algorithm runs in $O(V^4)$.
- **Push-Relabel runs in $O(V^3)$** — an order of magnitude faster than Dinic's and two orders faster than Edmonds-Karp.

---

## 4. Space Complexity

| Component | Space Required | Purpose |
| :--- | :--- | :--- |
| **Adjacency List (`graph`)** | $O(V + E)$ | Forward and residual edge descriptors. |
| **Excess Array (`excess`)** | $O(V)$ | Floating-point excess flow held at each vertex. |
| **Height Array (`height`)** | $O(V)$ | Elevation metric controlling downhill pushes. |
| **Height Frequency Table (`count`)** | $O(V)$ | Enables $O(1)$ empty-level detection for the Gap Heuristic. |
| **Bucket Queue (`buckets`)** | $O(V)$ | Direct height-indexed buckets for $O(1)$ highest-label lookup. |
| **Total Space** | **$O(V + E)$** | Linear in graph size, zero matrix overhead. |
