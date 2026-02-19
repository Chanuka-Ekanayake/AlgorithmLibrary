# Tarjan's SCC — Algorithm Logic

## Core Idea

Tarjan's algorithm finds all **Strongly Connected Components (SCCs)** in a
directed graph with a **single DFS pass** in **O(V + E)** time.

An SCC is a maximal group of vertices where every vertex can reach every other
vertex via directed edges.

---

## Key Data Structures

| Structure | Purpose |
|-----------|---------|
| `disc[v]` | Discovery timestamp when vertex `v` is first visited |
| `low[v]`  | Smallest discovery time reachable from `v`'s subtree (including back-edges) |
| `stack`   | Vertices currently in the DFS exploration path |
| `on_stack[v]` | Whether `v` is currently on the stack |

---

## Step-by-Step Walkthrough

```
Graph: A → B → C → A   (a cycle = one SCC)
       B → D            (D is isolated = its own SCC)
```

1. **Visit A** — disc[A]=0, low[A]=0, push A onto stack.
2. **Visit B** — disc[B]=1, low[B]=1, push B.
3. **Visit C** — disc[C]=2, low[C]=2, push C.
4. **C → A** is a back-edge (A is on stack) → `low[C] = min(2, disc[A]) = 0`
5. **Backtrack to B** → `low[B] = min(1, low[C]) = 0`
6. **Visit D** — disc[D]=3, low[D]=3, push D.
7. **Backtrack to D root** → `low[D] == disc[D]` → pop D → SCC: {D}
8. **Backtrack to B** → `low[B] = 0 ≠ disc[B]=1` → B is not a root yet.
9. **Backtrack to A** → `low[A] == disc[A] = 0` → pop until A → SCC: {A, B, C}

---

## SCC Root Detection

A vertex `v` is the **root of an SCC** when:
```
low[v] == disc[v]
```
This means no back-edge from `v`'s subtree can escape to an earlier ancestor,
so everything still on the stack above `v` belongs to the same SCC.

---

## Iterative vs Recursive

This implementation uses an **iterative DFS** with an explicit call stack.
This avoids Python's default recursion limit (~1000) for large graphs.

---

## Pseudo-code

```
function tarjan(graph):
    timer = 0
    disc, low = [-1] * V, [-1] * V
    on_stack = [False] * V
    stack = []
    sccs = []

    for each unvisited vertex v:
        DFS(v):
            disc[v] = low[v] = timer++
            push v onto stack, on_stack[v] = true

            for each neighbor w of v:
                if w not visited:
                    DFS(w)
                    low[v] = min(low[v], low[w])
                elif w is on stack:
                    low[v] = min(low[v], disc[w])

            if low[v] == disc[v]:   # v is SCC root
                pop stack until v → collect as one SCC

    return sccs
```

---

## Edge Cases

| Scenario | Behavior |
|----------|---------|
| Graph with no edges | Every vertex is its own SCC |
| Fully strongly connected graph | Single SCC containing all vertices |
| DAG (no cycles) | Every vertex is its own SCC |
| Disconnected graph | Handles each component independently |
