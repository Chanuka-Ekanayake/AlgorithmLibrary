# Algorithm Logic: Push-Relabel Maximum Flow (Goldberg-Tarjan)

To understand the **Push-Relabel Algorithm**, contrast it with augmenting path algorithms like Ford-Fulkerson or Dinic's. 

Augmenting path algorithms find complete end-to-end paths from the source $s$ to the sink $t$ across the entire network before pushing flow. While effective on sparse graphs, repeatedly traversing the whole network becomes expensive in dense, highly interconnected networks.

Push-Relabel abandons global path searches in favor of **purely local node operations**, modeling fluid dynamics with gravity, water reservoirs, and elevation.

---

## 1. The Physical Intuition: Gravity and Reservoirs

Imagine a network of water reservoirs connected by pipes:

1. **Source Elevation:** The source reservoir sits on top of a mountain at height $h(s) = |V|$.
2. **Sink Elevation:** The sink reservoir rests at sea level at height $h(t) = 0$.
3. **Intermediate Reservoirs:** All other nodes begin at height $0$.
4. **Water Push (Gravity):** Water can only flow **downhill** from a reservoir at height $h(u)$ to an adjacent reservoir at height $h(v)$ if $h(u) = h(v) + 1$.
5. **Preflow (Excess Storage):** Unlike standard flow conservation where $\text{inflow} = \text{outflow}$ at every second, nodes are allowed to temporarily hold surplus water (called **excess flow**, $e(u) > 0$). Such a node is termed **active**.

---

## 2. Core Operations

Push-Relabel operates by repeatedly performing two fundamental operations on active vertices until no more flow can move toward the sink:

```text
               [Active Node u: e(u) > 0]
                         |
           ------------------------------
           |                            |
[Downhill edge exists?]         [All edges level or uphill?]
  h(u) == h(v) + 1                  h(u) <= h(v)
           |                            |
           v                            v
        PUSH()                       RELABEL()
  Send flow to neighbor        Raise height of node u
```

### Operation A: Push
A push from an active node $u$ across an edge $(u, v)$ is legal if and only if:
1. $u$ has positive excess: $e(u) > 0$
2. The edge $(u, v)$ has remaining residual capacity: $c_f(u, v) = c(u, v) - f(u, v) > 0$
3. Downhill condition: $h(u) = h(v) + 1$

The amount pushed is:
$$\Delta = \min(e(u), c_f(u, v))$$

- **Saturating Push:** If $\Delta = c_f(u, v)$, the residual capacity of $(u, v)$ becomes zero.
- **Non-Saturating Push:** If $\Delta = e(u) < c_f(u, v)$, the excess at $u$ is completely depleted to 0.

### Operation B: Relabel
If an active node $u$ still has excess water ($e(u) > 0$), but all reachable residual neighbors $v$ are at the same height or higher ($h(u) \le h(v)$), water cannot flow downhill.

To unblock the reservoir, we **lift** node $u$:
$$h(u) = 1 + \min \{ h(v) \mid (u, v) \in E_f \}$$

Lifting node $u$ ensures that at least one residual edge leaving $u$ is now downhill ($h(u) = h(v) + 1$), allowing pushes on the next iteration.

---

## 3. The Discharge Loop & Returning Trapped Flow

A vertex is **discharged** by repeatedly pushing through its incident edges. If its excess remains positive after inspecting all incident edges, it is relabeled and scanning restarts.

What happens if excess water cannot reach the sink?
- Eventually, node heights can rise above $|V|$.
- When $h(u) > |V|$, the node is higher than the source ($h(s) = |V|$).
- The excess water flows downhill **back into the source** along reverse edges!
- Once all trapped water drains back to the source or reaches the sink, every intermediate node has excess $e(u) = 0$, guaranteeing strict flow conservation.

---

## 4. Performance Accelerators

### 4.1 Highest-Label Selection
Instead of selecting active vertices arbitrarily or using FIFO queues, this engine utilizes a **bucket array indexed by height**.
- At each step, it discharges vertices from the maximum active height level (`max_height`).
- This bounds non-saturating pushes to $O(V^2 \sqrt{E})$ instead of $O(V^3)$, providing peak throughput on dense topologies.

### 4.2 The Gap Heuristic
During relabeling, we track how many vertices reside at each height using a frequency count table `count[h]`.
- If a height level $k$ becomes completely empty (`count[k] == 0`) and $k < |V|$, a "gap" has opened in the elevation profile.
- Any node with height $k < h(u) < |V|$ can never reach the sink again (because there are no nodes at height $k$ to step down onto).
- The Gap Heuristic instantly raises all such nodes to at least $|V| + 1$, skipping redundant relabel iterations and sending stranded excess directly back to the source.

---

## 5. Minimum Cut Derivation

By the **Max-Flow Min-Cut Theorem**, the maximum flow value equals the capacity of the minimum $s-t$ cut.

Once the algorithm converges:
1. Run a Breadth-First Search (BFS) from the source $s$ traversing only edges with remaining residual capacity $c_f(u, v) > 0$.
2. The set of all visited vertices forms the **Source Partition ($S$)**.
3. All unvisited vertices form the **Sink Partition ($T$)**.
4. Edges spanning from $S$ to $T$ are 100% saturated and identify the critical structural bottlenecks in the system.
