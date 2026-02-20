# Hierholzer's Algorithm — Logic Deep Dive

## The Core Problem

An **Eulerian Path** visits every **edge** in a graph exactly once.
An **Eulerian Circuit** does the same but also returns to the starting vertex.

> Named after Leonhard Euler, who solved the famous **Königsberg Bridge Problem** in 1736
> — the birth of graph theory.

---

## Existence Conditions

### Directed Graph
| Type | Condition |
|------|-----------|
| **Circuit** | Every vertex: `out_degree == in_degree` |
| **Path** | Exactly one vertex: `out - in = +1` (start), one: `in - out = +1` (end), rest balanced |

### Undirected Graph
| Type | Condition |
|------|-----------|
| **Circuit** | Every vertex has **even** degree |
| **Path** | Exactly **two** vertices have odd degree (they are the endpoints) |

---

## Step-by-Step Walkthrough

```
Graph: A → B → C → D → B → A
              ↑           |
              └─── D ─────┘

Edges: A→B, B→C, C→D, D→B, B→A
```

**Step 1** — Start at A (out_degree − in_degree = +1 for directed path)
```
stack = [A],  path = []
```

**Step 2** — Follow edges greedily:
```
A → B → C → D → B → A  (stuck: A has no more outgoing edges)
stack = [A, B, C, D, B, A]
```

**Step 3** — A has no edges → pop A to `path`:
```
stack = [A, B, C, D, B],  path = [A]
```

**Step 4** — B has no edges → pop B to `path`:
```
stack = [A, B, C, D],  path = [B, A]
```

**Step 5** — D still has edge D → B (unused) → continue:
```
D → B  then B has no edges → pop B and D to path
path = [B, D, B, A]
```

**Step 6** — Unwind the rest:
```
Final path = [A, B, C, D, B, A]  ← reversed from deque
```

---

## Key Insight: Why the Stack + Path Trick Works

When we get "stuck" at a vertex (no more edges), we know all edges from that vertex
are already used. We **backtrack** to find unvisited edges and insert a new sub-circuit
into the existing result. The final order is built by prepending to the result path.

---

## Undirected Graphs: Edge Removal

For undirected graphs, when we traverse edge `(u, v)`, we must also remove
`(v, u)` from the adjacency list to prevent reusing it in the reverse direction.

---

## Pseudo-code

```
function hierholzer(graph, start):
    stack = [start]
    path = []

    while stack is not empty:
        v = stack.top()
        if v has remaining edges:
            next = graph[v].pop()
            stack.push(next)
        else:
            path.prepend(stack.pop())

    return path
```

---

## Edge Cases

| Scenario | Result |
|----------|--------|
| Single vertex, no edges | Circuit of length 1 |
| Graph with isolated vertices | No Eulerian path |
| Disconnected graph | No Eulerian path |
| All edges form one big cycle | Eulerian Circuit |
| Linear chain (path graph) | Eulerian Path, not a circuit |
