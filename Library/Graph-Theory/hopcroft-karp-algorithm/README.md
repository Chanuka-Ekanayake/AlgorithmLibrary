# Hopcroft-Karp Algorithm

The Hopcroft-Karp algorithm finds a maximum cardinality matching in a bipartite graph. It is one of the most efficient algorithms for this problem, running in $O(E \sqrt{V})$ time.

## Overview
A bipartite graph consists of two disjoint sets of vertices (for example, workers and jobs), such that edges only go between sets, never internally within a set. The objective is to match the highest possible number of edges while making sure no two edges share a common vertex.

The Hopcroft-Karp algorithm operates by using breadth-first search (BFS) to identify layers of shortest augmenting paths and then depth-first search (DFS) to augment along these shortest paths, leading to the overall $O(E \sqrt{V})$ running time.

## Algorithm Details
- **Time Complexity:** $O(E \sqrt{V})$
  - Where $E$ is the number of edges and $V$ is the number of vertices.
- **Space Complexity:** $O(V + E)$
  - To store distances, match maps, and the original graph edges itself.

## Directory Structure
- `core/`: Contains the actual implementation (`hopcroft_karp.py`).
- `docs/`: In-depth documentation covering `logic` and `complexity`.
- `test-project/`: A sample runnable application (`app.py`) showcasing a real-world use-case.
