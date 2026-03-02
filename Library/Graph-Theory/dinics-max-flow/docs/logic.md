# Algorithm Logic: Dinic's Algorithm (Maximum Flow)

To understand Dinic's Algorithm, you have to imagine water flowing through a network of pipes. Each pipe has a strict maximum capacity. The goal is to push as much water as possible from the Source (your primary server) to the Sink (the buyer's machine).

The algorithm runs in continuous cycles of two distinct phases: **Structuring** and **Pushing**.

## 1. Phase 1: The Level Graph (Structuring)

If you let a routing algorithm wander blindly, it will waste CPU cycles sending data backward or in circles. Dinic's prevents this by running a Breadth-First Search (BFS) to build a **Level Graph**.

The BFS starts at the Source and assigns a "Level" (distance) to every server it touches.

- Source = Level 0
- Direct neighbors = Level 1
- Neighbors of neighbors = Level 2

**The Golden Rule of the Level Graph:** > _Data is strictly forbidden from moving sideways (Level 2 to Level 2) or backward (Level 2 to Level 1). It must always flow forward to exactly Level + 1._

If the BFS reaches the Sink, Phase 1 is complete. If the BFS cannot reach the Sink (because all forward pipes are completely full), the algorithm terminates—you have found the absolute maximum flow.

---

## 2. Phase 2: The Blocking Flow (Pushing)

Once the network is structured into levels, the algorithm runs a Depth-First Search (DFS) to push as much data as possible through the valid forward pipes.

Instead of pushing data one path at a time, it recursively saturates entire branches of the network.

### Dead-End Pruning

As the DFS pushes flow, it hits bottlenecks where pipes become 100% full. When a pipe is full, the DFS updates a pointer (the `start_index`) to permanently ignore that pipe for the rest of the phase. It never wastes time checking a dead end twice. It keeps pushing data until no more traffic can possibly reach the Sink through the current Level Graph. This state is called a **Blocking Flow**.

---

## 3. The Magic Trick: The Residual Graph

What happens if the DFS makes a "mistake"?

Imagine you have a 10 GB/s pipe that splits into two 5 GB/s pipes. The DFS might greedily push 10 GB/s down a path that eventually hits a 2 GB/s bottleneck further down the line, essentially trapping 8 GB/s of capacity that could have been routed elsewhere.

Dinic's Algorithm solves this flawlessly using **Reverse Edges**.

Every time you add a connection to the network, the engine automatically creates an invisible "Reverse Edge" pointing backward, starting with 0 capacity.

**How to "Undo" Traffic:**

1. You push 8 GB/s of data forward through Server A to Server B.
2. The engine reduces the forward capacity by 8.
3. Simultaneously, the engine **increases the Reverse Edge capacity by 8**.

In the next phase, if the algorithm desperately needs to route traffic through Server B to another destination, it is mathematically allowed to push data _backward_ across the Reverse Edge to Server A.

**Pushing "negative flow" backward perfectly cancels out the original forward flow.** It mathematically "redirects" the trapped data down a better path without requiring the algorithm to physically restart or recalculate the entire history of the network.

This Residual Graph self-correction is what guarantees the absolute mathematical maximum throughput every single time.
