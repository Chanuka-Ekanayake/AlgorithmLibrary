"""
Tarjan's Strongly Connected Components (SCC) Algorithm Implementation
Finds all SCCs in a directed graph using a single DFS pass with a stack.
"""

from collections import defaultdict


class TarjansSCC:
    """
    Implementation of Tarjan's Algorithm to find all Strongly Connected
    Components (SCCs) in a directed graph.

    A Strongly Connected Component is a maximal set of vertices such that
    there is a path from each vertex to every other vertex in the same set.

    Time Complexity:  O(V + E)
    Space Complexity: O(V + E)
    """

    def __init__(self, vertices):
        """
        Initialize the directed graph.

        Args:
            vertices (int): Number of vertices in the graph
        """
        self.vertices = vertices
        self.graph = defaultdict(list)
        self._timer = 0

    def add_edge(self, u, v):
        """
        Add a directed edge from u to v.

        Args:
            u (int): Source vertex
            v (int): Destination vertex
        """
        self.graph[u].append(v)

    def _dfs(self, u, disc, low, on_stack, stack, sccs):
        """
        Iterative DFS to avoid Python recursion limit on large graphs.

        Args:
            u (int): Starting vertex
            disc (list): Discovery time for each vertex
            low (list): Lowest discovery time reachable
            on_stack (list): Whether vertex is currently on the stack
            stack (list): The DFS stack for SCC detection
            sccs (list): Accumulator list for completed SCCs
        """
        # Use an explicit call stack: (vertex, iterator-index)
        call_stack = [(u, 0)]
        disc[u] = low[u] = self._timer
        self._timer += 1
        stack.append(u)
        on_stack[u] = True

        while call_stack:
            v, idx = call_stack[-1]
            neighbors = self.graph[v]

            if idx < len(neighbors):
                # Advance the iterator index
                call_stack[-1] = (v, idx + 1)
                w = neighbors[idx]

                if disc[w] == -1:
                    # Tree edge — recurse
                    disc[w] = low[w] = self._timer
                    self._timer += 1
                    stack.append(w)
                    on_stack[w] = True
                    call_stack.append((w, 0))
                elif on_stack[w]:
                    # Back edge — update low
                    low[v] = min(low[v], disc[w])
            else:
                # Done with this vertex — pop and propagate low values
                call_stack.pop()
                if call_stack:
                    parent = call_stack[-1][0]
                    low[parent] = min(low[parent], low[v])

                # If v is an SCC root, pop the stack to get the full SCC
                if low[v] == disc[v]:
                    scc = []
                    while True:
                        node = stack.pop()
                        on_stack[node] = False
                        scc.append(node)
                        if node == v:
                            break
                    sccs.append(sorted(scc))

    def find_sccs(self):
        """
        Find all Strongly Connected Components in the graph.

        Returns:
            list[list[int]]: A list of SCCs, each SCC is a sorted list of vertex indices.
        """
        disc = [-1] * self.vertices
        low = [-1] * self.vertices
        on_stack = [False] * self.vertices
        stack = []
        sccs = []
        self._timer = 0

        for v in range(self.vertices):
            if disc[v] == -1:
                self._dfs(v, disc, low, on_stack, stack, sccs)

        return sccs


# ─────────────────────────────────────────────
#  Named-vertex helper utilities
# ─────────────────────────────────────────────

def find_sccs_with_names(nodes, edges):
    """
    Find SCCs using human-readable node names.

    Args:
        nodes (list[str]): Node labels, e.g. ["A", "B", "C"]
        edges (list[tuple]): Directed edges as (source, destination)

    Returns:
        list[list[str]]: SCCs where each entry contains node names.
    """
    node_to_idx = {node: idx for idx, node in enumerate(nodes)}
    graph = TarjansSCC(len(nodes))

    for u, v in edges:
        graph.add_edge(node_to_idx[u], node_to_idx[v])

    raw_sccs = graph.find_sccs()
    return [[nodes[i] for i in scc] for scc in raw_sccs]


def analyze_graph_connectivity(nodes, edges):
    """
    Full SCC analysis: returns SCCs plus condensation graph statistics.

    Args:
        nodes (list[str]): Node labels
        edges (list[tuple]): Directed edges as (source, destination)

    Returns:
        dict: {
            'sccs': list of SCC node-name groups,
            'num_sccs': int,
            'is_strongly_connected': bool,
            'trivial_sccs': list (single-node SCCs),
            'non_trivial_sccs': list (multi-node SCCs)
        }
    """
    sccs = find_sccs_with_names(nodes, edges)
    trivial = [s for s in sccs if len(s) == 1]
    non_trivial = [s for s in sccs if len(s) > 1]

    return {
        "sccs": sccs,
        "num_sccs": len(sccs),
        "is_strongly_connected": len(sccs) == 1,
        "trivial_sccs": trivial,
        "non_trivial_sccs": non_trivial,
    }
