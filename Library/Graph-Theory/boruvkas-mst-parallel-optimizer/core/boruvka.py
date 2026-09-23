"""
Borůvka's Algorithm Implementation
Provides an optimized Minimum Spanning Tree (MST) solution for
undirected, weighted graphs using a component-merging strategy.

LOGIC OVERVIEW:
Borůvka's is a greedy algorithm that finds the MST by repeatedly finding
the minimum-weight outgoing edge for each connected component, then merging
those components. Each iteration at least halves the number of components,
guaranteeing O(log V) rounds.

KEY ADVANTAGE: Naturally parallelizable — each component's cheapest edge
can be found independently, making it ideal for distributed/parallel systems.

TRADE-OFF: Requires unique edge weights (or tie-breaking) to guarantee a
unique MST. Slightly more complex bookkeeping than Prim's or Kruskal's.
"""

from typing import Dict, List, Tuple, Set, Optional, Union

# Type alias for clarity: Graph represented as adjacency list
# Each node maps to a dictionary of {neighbor: weight}
Graph = Dict[str, Dict[str, Union[int, float]]]


class DisjointSetUnion:
    """
    An optimized DSU (Union-Find) structure for string-labeled vertices.
    Implements Path Compression and Union by Rank to achieve O(α(N))
    time complexity, where α is the inverse Ackermann function.
    """

    def __init__(self, vertices: List[str]):
        self.parent: Dict[str, str] = {v: v for v in vertices}
        self.rank: Dict[str, int] = {v: 0 for v in vertices}

    def find(self, x: str) -> str:
        """Finds the root representative of the element with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: str, y: str) -> bool:
        """
        Merges two sets using rank optimization to keep the tree shallow.
        Returns True if a merge occurred, False if they were already in the same set.
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        # Union by rank: Attach smaller tree under the larger tree
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_x] = root_y
            self.rank[root_y] += 1

        return True


def boruvkas_mst(
    graph: Graph
) -> Tuple[List[Tuple[str, str, float]], float]:
    """
    Borůvka's algorithm for finding the Minimum Spanning Tree (MST) of a graph.

    LOGIC OVERVIEW:
    Unlike Prim's (vertex-growth) or Kruskal's (global edge sort), Borůvka's
    works in rounds. Each round finds the cheapest outgoing edge for every
    connected component and merges them. The number of components halves each
    round, completing in O(log V) iterations.

    KEY ADVANTAGE: Each component's cheapest edge search is independent,
    making this algorithm ideal for parallel and distributed execution.

    TRADE-OFF: Slightly more complex than Kruskal's; requires tie-breaking
    for graphs with duplicate edge weights.

    Args:
        graph: Undirected graph as adjacency list {node: {neighbor: weight}}

    Returns:
        A tuple containing:
        1. mst_edges: List of (u, v, weight) tuples forming the MST
        2. total_cost: Total weight of the MST
    """
    if not graph:
        return [], 0.0

    # --- 1. Initialization ---
    # Collect all vertices (including those only appearing as neighbors)
    all_vertices: Set[str] = set(graph.keys())
    for neighbors in graph.values():
        all_vertices.update(neighbors.keys())

    vertices = list(all_vertices)
    num_vertices = len(vertices)

    if num_vertices <= 1:
        return [], 0.0

    dsu = DisjointSetUnion(vertices)
    mst_edges: List[Tuple[str, str, float]] = []
    total_cost = 0.0
    num_components = num_vertices

    # --- 2. Main Loop: Merge components until only one remains ---
    while num_components > 1:
        # For each component, find its cheapest outgoing edge
        # Key: component root -> (weight, u, v)
        cheapest: Dict[str, Optional[Tuple[float, str, str]]] = {}

        # Scan every edge in the graph
        for u in graph:
            for v, weight in graph[u].items():
                root_u = dsu.find(u)
                root_v = dsu.find(v)

                # Skip edges within the same component (would create a cycle)
                if root_u == root_v:
                    continue

                # Update cheapest edge for component of u
                if root_u not in cheapest or weight < cheapest[root_u][0]:
                    cheapest[root_u] = (weight, u, v)

                # Update cheapest edge for component of v
                if root_v not in cheapest or weight < cheapest[root_v][0]:
                    cheapest[root_v] = (weight, u, v)

        # If no cheapest edges found, graph is disconnected
        if not cheapest:
            break

        # Merge components using their cheapest edges
        edges_added_this_round = 0
        for component_root, edge_info in cheapest.items():
            if edge_info is None:
                continue

            weight, u, v = edge_info

            # Only merge if they are still in different components
            if dsu.union(u, v):
                mst_edges.append((u, v, weight))
                total_cost += weight
                num_components -= 1
                edges_added_this_round += 1

        # Safety: if no edges were added, graph is disconnected
        if edges_added_this_round == 0:
            break

    return mst_edges, total_cost


def build_mst_graph(mst_edges: List[Tuple[str, str, float]]) -> Graph:
    """
    Converts MST edge list to adjacency list representation.

    Args:
        mst_edges: List of MST edges as (u, v, weight) tuples

    Returns:
        Graph representation of the MST
    """
    mst_graph: Graph = {}

    for u, v, weight in mst_edges:
        if u not in mst_graph:
            mst_graph[u] = {}
        if v not in mst_graph:
            mst_graph[v] = {}

        mst_graph[u][v] = weight
        mst_graph[v][u] = weight

    return mst_graph


def is_graph_connected(graph: Graph) -> bool:
    """
    Checks if the graph is connected using DFS.
    MST only exists for connected graphs.

    Args:
        graph: The graph to check

    Returns:
        True if graph is connected, False otherwise
    """
    if not graph:
        return True

    # Collect all vertices
    all_vertices: Set[str] = set(graph.keys())
    for neighbors in graph.values():
        all_vertices.update(neighbors.keys())

    start = next(iter(graph))
    visited: Set[str] = set()
    stack = [start]

    while stack:
        node = stack.pop()
        if node in visited:
            continue

        visited.add(node)

        if node in graph:
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)

    return len(visited) == len(all_vertices)


def calculate_mst_savings(
    graph: Graph,
    mst_edges: List[Tuple[str, str, float]]
) -> Tuple[float, float, float]:
    """
    Calculates the cost savings of using MST versus connecting all edges.

    Args:
        graph: Original graph
        mst_edges: MST edges

    Returns:
        Tuple of (total_graph_cost, mst_cost, savings_percent)
    """
    # Calculate total cost of all edges in graph
    total_graph_cost = 0.0
    counted_edges: Set[Tuple[str, str]] = set()

    for u in graph:
        for v, weight in graph[u].items():
            edge = tuple(sorted([u, v]))
            if edge not in counted_edges:
                total_graph_cost += weight
                counted_edges.add(edge)

    mst_cost = sum(weight for _, _, weight in mst_edges)
    savings_percent = (
        (total_graph_cost - mst_cost) / total_graph_cost * 100
        if total_graph_cost > 0 else 0
    )

    return total_graph_cost, mst_cost, savings_percent


def get_mst_diameter(mst_edges: List[Tuple[str, str, float]]) -> float:
    """
    Calculates the diameter of the MST (longest shortest path in the tree).

    The MST is a tree, so there is exactly one path between any two vertices.
    The diameter is the maximum distance between any two vertices.

    Args:
        mst_edges: List of MST edges

    Returns:
        The diameter (longest path length)
    """
    if not mst_edges:
        return 0.0

    mst_graph = build_mst_graph(mst_edges)

    # Find diameter using two BFS passes
    start = next(iter(mst_graph))
    farthest, _ = _bfs_farthest(mst_graph, start)
    _, diameter = _bfs_farthest(mst_graph, farthest)

    return diameter


def _bfs_farthest(
    graph: Graph,
    start: str
) -> Tuple[str, float]:
    """
    Helper: BFS to find farthest node from start and its distance.

    Args:
        graph: The graph
        start: Starting node

    Returns:
        Tuple of (farthest_node, distance)
    """
    from collections import deque

    visited = {start}
    queue = deque([(start, 0.0)])
    farthest_node = start
    max_distance = 0.0

    while queue:
        node, distance = queue.popleft()

        if distance > max_distance:
            max_distance = distance
            farthest_node = node

        if node in graph:
            for neighbor, weight in graph[node].items():
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + weight))

    return farthest_node, max_distance


def get_mst_statistics(
    graph: Graph,
    mst_edges: List[Tuple[str, str, float]]
) -> Dict[str, Union[int, float]]:
    """
    Computes various statistics about the MST.

    Args:
        graph: Original graph
        mst_edges: MST edges

    Returns:
        Dictionary of statistics
    """
    all_vertices: Set[str] = set(graph.keys())
    for neighbors in graph.values():
        all_vertices.update(neighbors.keys())

    mst_cost = sum(weight for _, _, weight in mst_edges)
    total_cost, _, savings_pct = calculate_mst_savings(graph, mst_edges)
    diameter = get_mst_diameter(mst_edges)

    weights = [weight for _, _, weight in mst_edges]

    return {
        'num_vertices': len(all_vertices),
        'num_mst_edges': len(mst_edges),
        'mst_total_cost': mst_cost,
        'original_total_cost': total_cost,
        'cost_savings_percent': savings_pct,
        'mst_diameter': diameter,
        'min_edge_weight': min(weights) if weights else 0,
        'max_edge_weight': max(weights) if weights else 0,
        'avg_edge_weight': sum(weights) / len(weights) if weights else 0,
    }
