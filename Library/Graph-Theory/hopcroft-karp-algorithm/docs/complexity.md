# Complexity of Hopcroft-Karp Algorithm

## Time Complexity
The time complexity of the Hopcroft-Karp algorithm on a bipartite graph $G = (U \cup V, E)$ is **$O(E \sqrt{V})$**.

- **$V$**: The total number of vertices in the bipartite graph ($|U| + |V|$).
- **$E$**: The total number of edges in the bipartite graph.

### Why $O(E \sqrt{V})$?
The algorithm proceeds in phases. In each phase, a Breadth-First Search (BFS) combined with a Depth-First Search (DFS) is used to find a maximal set of shortest disjoint augmenting paths.
1. The work done in each individual phase (one BFS + one DFS process) is bounded by **$O(E)$**.
2. It can be mathematically proven that the length of the shortest augmenting path strictly increases after each phase. Because of the bipartite nature and the maximum paths found per step, the algorithm requires at most **$O(\sqrt{V})$** phases to complete.

Therefore, combining the two facts, the total time complexity is strictly bounded by $O(E \sqrt{V})$.

## Space Complexity
The overall space complexity is **$O(V + E)$**.

- **Graph Storage:** The adjacency list representation of the bipartite graph requires $O(V + E)$ space.
- **Matching Details:** Keeping track of matched pairs (`pair_u`, `pair_v`) demands $O(V)$ space.
- **BFS Structure:** The `dist` dictionary mapping distances for all nodes requires $O(V)$ auxiliary space. A queue to perform BFS needs $O(V)$ space.
- **DFS Recursion:** Due to recursion during the augmentation phase, the call stack might grow up to the depth of the graph, bounded by $O(V)$ space.

Because each of these components uses at most linear space in the numbers of vertices and edges, the overall space footprint remains well-optimized at **$O(V + E)$**.
