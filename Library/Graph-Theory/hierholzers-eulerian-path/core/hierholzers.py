"""
Hierholzer's Algorithm — Eulerian Path and Eulerian Circuit Finder
Finds a path/circuit that visits every EDGE in a graph exactly once.
Works for both directed and undirected graphs in O(V + E) time.
"""

from collections import defaultdict, deque


class HierholzersEulerian:
    """
    Implementation of Hierholzer's Algorithm to find:

    - Eulerian Circuit : A closed path that visits every edge exactly once
                         and returns to the starting vertex.
    - Eulerian Path    : An open path that visits every edge exactly once
                         (starts and ends at different vertices).

    Supports both directed and undirected graphs.

    Time Complexity:  O(V + E)
    Space Complexity: O(V + E)
    """

    def __init__(self, directed=True):
        """
        Initialize an empty graph.

        Args:
            directed (bool): True for directed graph, False for undirected.
        """
        self.directed = directed
        self.graph = defaultdict(deque)   # adjacency list using deque for O(1) pops
        self.edge_count = defaultdict(int)
        self.vertices = set()

    def add_edge(self, u, v):
        """
        Add an edge to the graph.

        Args:
            u: Source vertex
            v: Destination vertex
        """
        self.graph[u].append(v)
        self.vertices.add(u)
        self.vertices.add(v)

        if not self.directed:
            self.graph[v].append(u)
            self.edge_count[(min(u, v), max(u, v))] += 1
        else:
            self.edge_count[(u, v)] += 1

    # ─────────────────────────────────────────────
    #  Condition Checks
    # ─────────────────────────────────────────────

    def _in_degree(self):
        """Compute in-degree for all vertices (directed graphs)."""
        in_deg = defaultdict(int)
        for u in self.graph:
            for v in self.graph[u]:
                in_deg[v] += 1
        return in_deg

    def has_eulerian_circuit(self):
        """
        Check if the graph has an Eulerian Circuit.

        Directed  : Every vertex has equal in-degree and out-degree.
        Undirected: Every vertex has even degree AND graph is connected.

        Returns:
            bool
        """
        if self.directed:
            in_deg = self._in_degree()
            for v in self.vertices:
                if len(self.graph[v]) != in_deg.get(v, 0):
                    return False
            return True
        else:
            for v in self.vertices:
                if len(self.graph[v]) % 2 != 0:
                    return False
            return True

    def has_eulerian_path(self):
        """
        Check if the graph has an Eulerian Path (but not necessarily a circuit).

        Directed  : Exactly one vertex has out_degree - in_degree = 1 (start),
                    exactly one has in_degree - out_degree = 1 (end),
                    all others balanced.
        Undirected: Exactly two vertices have odd degree.

        Returns:
            bool
        """
        if self.directed:
            in_deg = self._in_degree()
            start_candidates = end_candidates = 0
            for v in self.vertices:
                diff = len(self.graph[v]) - in_deg.get(v, 0)
                if diff == 1:
                    start_candidates += 1
                elif diff == -1:
                    end_candidates += 1
                elif diff != 0:
                    return False
            return start_candidates == 1 and end_candidates == 1
        else:
            odd_degree = sum(1 for v in self.vertices if len(self.graph[v]) % 2 != 0)
            return odd_degree == 2

    # ─────────────────────────────────────────────
    #  Core Algorithm
    # ─────────────────────────────────────────────

    def _find_start_vertex(self):
        """
        Determine the best starting vertex for the Eulerian traversal.

        - Circuit: any vertex with edges
        - Directed Path: vertex where out_degree - in_degree == 1
        - Undirected Path: any vertex with odd degree
        """
        if self.has_eulerian_circuit():
            # Start from any vertex that has edges
            for v in self.vertices:
                if self.graph[v]:
                    return v

        if self.directed:
            in_deg = self._in_degree()
            for v in self.vertices:
                if len(self.graph[v]) - in_deg.get(v, 0) == 1:
                    return v
        else:
            for v in self.vertices:
                if len(self.graph[v]) % 2 != 0:
                    return v

        return next(iter(self.vertices)) if self.vertices else None

    def find_eulerian_path(self):
        """
        Find an Eulerian Path or Circuit using Hierholzer's algorithm.

        The algorithm works iteratively:
        1. Start from the correct vertex.
        2. Follow edges greedily until stuck (no more edges from current vertex).
        3. Back-track to the last vertex that still has unused edges.
        4. Continue from there, inserting the new sub-circuit into the result.

        Returns:
            list: Ordered list of vertices forming the Eulerian path/circuit.
                  Returns [] if no Eulerian path or circuit exists.
        """
        if not self.has_eulerian_circuit() and not self.has_eulerian_path():
            return []

        # Work on a copy of adjacency lists so the original graph is preserved
        graph_copy = {v: deque(edges) for v, edges in self.graph.items()}

        start = self._find_start_vertex()
        if start is None:
            return []

        stack = [start]
        path = deque()

        while stack:
            v = stack[-1]
            if graph_copy.get(v):
                # Take the next unvisited edge
                next_v = graph_copy[v].popleft()
                if not self.directed:
                    # For undirected: remove the reverse edge too
                    graph_copy[next_v].remove(v)
                stack.append(next_v)
            else:
                # No more edges from v — add to result path
                path.appendleft(stack.pop())

        return list(path)

    def get_path_info(self):
        """
        Returns a human-readable summary of the Eulerian properties.

        Returns:
            dict: {
                'has_circuit': bool,
                'has_path': bool,
                'path': list,
                'type': str,  # 'circuit', 'path', or 'none'
            }
        """
        circuit = self.has_eulerian_circuit()
        path = self.has_eulerian_path()

        if circuit:
            result = self.find_eulerian_path()
            return {"has_circuit": True, "has_path": True, "path": result, "type": "circuit"}
        elif path:
            result = self.find_eulerian_path()
            return {"has_circuit": False, "has_path": True, "path": result, "type": "path"}
        else:
            return {"has_circuit": False, "has_path": False, "path": [], "type": "none"}


# ─────────────────────────────────────────────
#  Named-vertex helper utilities
# ─────────────────────────────────────────────

def find_eulerian_path_with_names(nodes, edges, directed=True):
    """
    Find an Eulerian path/circuit using human-readable node names.

    Args:
        nodes (list): List of node labels e.g. ["A", "B", "C"]
        edges (list): List of (source, destination) tuples
        directed (bool): True for directed, False for undirected

    Returns:
        dict: path_info with node names instead of indices
    """
    g = HierholzersEulerian(directed=directed)
    for u, v in edges:
        g.add_edge(u, v)

    return g.get_path_info()


def plan_route(locations, routes, directed=False):
    """
    Real-world utility: plan a route covering all roads exactly once.

    Args:
        locations (list): List of location names
        routes (list): List of (from, to) road connections
        directed (bool): Whether roads are one-way

    Returns:
        dict: Route plan with path and feasibility info
    """
    info = find_eulerian_path_with_names(locations, routes, directed=directed)

    if info["type"] == "circuit":
        summary = "✅ Perfect circuit — return to start after covering all routes."
    elif info["type"] == "path":
        start = info["path"][0] if info["path"] else "N/A"
        end = info["path"][-1] if info["path"] else "N/A"
        summary = f"✅ One-way path from '{start}' to '{end}' covers all routes."
    else:
        summary = "❌ No Eulerian path exists — some routes cannot be covered in one trip."

    return {
        "feasible": info["type"] != "none",
        "type": info["type"],
        "route": info["path"],
        "summary": summary,
        "total_stops": len(info["path"]),
    }
