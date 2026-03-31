# Hopcroft-Karp Algorithm

## Overview
The Hopcroft-Karp algorithm is a widely used algorithm that takes a bipartite graph and produces a maximum cardinality matching. It works in $O(E \sqrt{V})$ time, making it much faster than simple augmenting path algorithms like Ford-Fulkerson, which run in $O(VE)$ time.

The algorithm uses a combination of Breadth-First Search (BFS) and Depth-First Search (DFS) to find multiple augmenting paths simultaneously and augment the matching in bulk.

## Core Logic

A bipartite graph consists of two disjoint sets of vertices, $U$ and $V$, such that every edge connects a vertex in $U$ to a vertex in $V$. The goal is to find the largest possible set of edges such that no two edges share a common vertex (maximum matching).

### Step-by-Step Execution

1. **Initialization:**
   - Maintain a set of matchings for nodes in $U$ (`pair_u`) and $V$ (`pair_v`).
   - Initially, all matchings are `None` (empty).

2. **Breadth-First Search (BFS):**
   - The algorithm starts with a BFS from all **unmatched nodes** in $U$.
   - It assigns a distance (or level) to each node as it traverses the graph. 
   - Wait condition: The BFS halts and indicates a successful phase when it discovers at least one augmenting path reaching an unmatched node in $V$.
   - It constructs a layered directed graph that contains all shortest augmenting paths.

3. **Depth-First Search (DFS):**
   - Along the layered graph constructed by BFS, a DFS is performed starting from each originally unmatched node in $U$.
   - The DFS attempts to construct actual augmenting paths.
   - When an augmenting path is found (reaching an unmatched node in $V$ through the pre-calculated shortest path distances), we flip the edges in the path (i.e. we update the matchings for all nodes along the path).
   
4. **Termination:**
   - The algorithm repeats the BFS and DFS steps.
   - It ends when the BFS step fails to find any new augmenting paths, meaning the current matching is optimal and cannot be improved.

## Algorithm Characteristics
- The key optimization is that BFS finds the *length* of the shortest augmenting paths, and DFS simultaneously augments along *maximally disjoint* paths of this length.
- Because it groups the shortest augmenting paths by length, it only takes $O(\sqrt{V})$ phases to find the maximum matching.
