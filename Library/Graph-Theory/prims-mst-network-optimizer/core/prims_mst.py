import heapq
from typing import Dict, List, Tuple, Set, Optional, Union

# Type alias for clarity: Graph represented as adjacency list
# Each node maps to a dictionary of {neighbor: weight}
Graph = Dict[str, Dict[str, Union[int, float]]]

def prims_mst(
    graph: Graph,
    start_node: Optional[str] = None
) -> Tuple[List[Tuple[str, str, float]], float]:
    """
    Prim's algorithm for finding the Minimum Spanning Tree (MST) of a graph.
    
    LOGIC OVERVIEW:
    Prim's is a greedy algorithm that grows the MST one edge at a time, always
    adding the minimum-weight edge that connects a vertex in the tree to a
    vertex outside the tree. Uses a priority queue for efficient edge selection.
    
    KEY ADVANTAGE: Efficient for dense graphs; always finds optimal MST.
    TRADE-OFF: Requires connected graph; doesn't work on directed graphs.
    
    Args:
        graph: Undirected graph as adjacency list {node: {neighbor: weight}}
        start_node: Optional starting vertex (if None, uses arbitrary node)
    
    Returns:
        A tuple containing:
        1. mst_edges: List of (u, v, weight) tuples forming the MST
        2. total_cost: Total weight of the MST
    """
    
    if not graph:
        return [], 0.0
    
    # --- 1. Initialization ---
    # Start from arbitrary node if not specified
    if start_node is None:
        start_node = next(iter(graph))
    
    if start_node not in graph:
        raise ValueError(f"Start node '{start_node}' not in graph")
    
    # Track vertices included in MST
    in_mst: Set[str] = {start_node}
    
    # MST edges (u, v, weight)
    mst_edges: List[Tuple[str, str, float]] = []
    
    # Total cost of MST
    total_cost = 0.0
    
    # Priority queue: (weight, from_vertex, to_vertex)
    # Contains edges from vertices in MST to vertices not yet in MST
    pq: List[Tuple[float, str, str]] = []
    
    # Add all edges from start node to priority queue
    for neighbor, weight in graph[start_node].items():
        heapq.heappush(pq, (weight, start_node, neighbor))
    
    # --- 2. Main Loop: Grow MST one edge at a time ---
    while pq and len(in_mst) < len(graph):
        # Get minimum weight edge from queue
        weight, u, v = heapq.heappop(pq)
        
        # Skip if both vertices already in MST (edge would create cycle)
        if v in in_mst:
            continue
        
        # Add edge to MST
        mst_edges.append((u, v, weight))
        total_cost += weight
        in_mst.add(v)
        
        # Add all edges from newly added vertex to priority queue
        if v in graph:
            for neighbor, edge_weight in graph[v].items():
                if neighbor not in in_mst:
                    heapq.heappush(pq, (edge_weight, v, neighbor))
    
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
        # Add edge u-v (undirected)
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
    
    # Start DFS from arbitrary vertex
    start = next(iter(graph))
    visited = set()
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
    
    # Check if all vertices were visited
    all_vertices = set(graph.keys())
    for neighbors in graph.values():
        all_vertices.update(neighbors.keys())
    
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
        Tuple of (total_graph_cost, mst_cost, savings)
    """
    # Calculate total cost of all edges in graph
    total_graph_cost = 0.0
    counted_edges = set()
    
    for u in graph:
        for v, weight in graph[u].items():
            # Avoid counting each undirected edge twice
            edge = tuple(sorted([u, v]))
            if edge not in counted_edges:
                total_graph_cost += weight
                counted_edges.add(edge)
    
    # MST cost
    mst_cost = sum(weight for _, _, weight in mst_edges)
    
    # Savings
    savings = total_graph_cost - mst_cost
    savings_percent = (savings / total_graph_cost * 100) if total_graph_cost > 0 else 0
    
    return total_graph_cost, mst_cost, savings_percent


def find_all_msts(graph: Graph) -> List[List[Tuple[str, str, float]]]:
    """
    Returns a list of minimum spanning trees (MSTs) for the given graph.
    
    Current behavior:
        This helper currently computes a single MST using ``prims_mst`` and
        returns it wrapped in a list. It does *not* enumerate all possible MSTs
        when multiple MSTs exist due to tied edge weights; it only returns one
        representative MST.
    
    Args:
        graph: The graph to analyze.
    
    Returns:
        List of MSTs, where each MST is a list of edges. At present this list
        contains either zero or one MST.
    """
    # NOTE: This function intentionally returns a single MST wrapped in a list.
    # Full enumeration of all MSTs in the presence of equal-weight edges is
    # not implemented here and would be significantly more expensive.
    mst_edges, _ = prims_mst(graph)
    return [mst_edges] if mst_edges else []


def get_mst_diameter(mst_edges: List[Tuple[str, str, float]]) -> float:
    """
    Calculates the diameter of the MST (longest path in the tree).
    
    The MST is a tree, so there's exactly one path between any two vertices.
    Diameter is the maximum distance between any two vertices.
    
    Args:
        mst_edges: List of MST edges
    
    Returns:
        The diameter (longest path length)
    """
    if not mst_edges:
        return 0.0
    
    # Build MST graph
    mst_graph = build_mst_graph(mst_edges)
    
    # Find diameter using two BFS passes
    # 1. BFS from arbitrary node to find farthest node
    start = next(iter(mst_graph))
    farthest, _ = _bfs_farthest(mst_graph, start)
    
    # 2. BFS from that farthest node to find actual diameter
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


def compare_with_kruskal_result(
    graph: Graph,
    prims_result: List[Tuple[str, str, float]]
) -> bool:
    """
    Verifies that Prim's MST has the same total cost as what Kruskal's would give.
    Both algorithms should produce MSTs with identical total weight.
    
    This function:
      1. Reconstructs an undirected edge list from the input graph.
      2. Runs Kruskal's algorithm to compute an MST and its total cost.
      3. Validates that the Kruskal MST is spanning (i.e., connects all vertices)
         and has exactly |V| - 1 edges.
      4. Compares the total cost of Prim's result to Kruskal's MST cost.
    
    Args:
        graph: Original graph
        prims_result: MST from Prim's algorithm as a list of (u, v, weight)
    
    Returns:
        True if:
          * the graph is connected (so an MST exists),
          * Kruskal's algorithm produces a valid MST, and
          * Prim's and Kruskal's MST total costs match (within a small tolerance).
        False otherwise.
    """
    # Collect all vertices
    vertices: Set[str] = set(graph.keys())
    for neighbors in graph.values():
        vertices.update(neighbors.keys())

    if not vertices:
        # Empty graph: expect no edges from Prim's as well
        return len(prims_result) == 0

    # Build undirected edge list without duplicates: (weight, u, v)
    edges: List[Tuple[float, str, str]] = []
    seen_edges: Set[Tuple[str, str]] = set()
    for u, neighbors in graph.items():
        for v, weight in neighbors.items():
            # Ensure each undirected edge is only added once
            a, b = sorted((u, v))
            key = (a, b)
            if key in seen_edges:
                continue
            seen_edges.add(key)
            edges.append((float(weight), a, b))

    # If there are no edges but there are vertices, the graph is disconnected
    if not edges and len(vertices) > 1:
        return False

    # Disjoint Set Union (Union-Find) for Kruskal
    parent: Dict[str, str] = {v: v for v in vertices}
    rank: Dict[str, int] = {v: 0 for v in vertices}

    def find(x: str) -> str:
        # Path compression
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: str, y: str) -> bool:
        # Union by rank; returns True if union was performed
        root_x = find(x)
        root_y = find(y)
        if root_x == root_y:
            return False
        if rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
        elif rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            parent[root_y] = root_x
            rank[root_x] += 1
        return True

    # Run Kruskal's algorithm
    edges.sort(key=lambda e: e[0])
    kruskal_cost: float = 0.0
    kruskal_edges_count = 0

    for weight, u, v in edges:
        if union(u, v):
            kruskal_cost += weight
            kruskal_edges_count += 1
            # Early stop: MST for connected graph has |V| - 1 edges
            if kruskal_edges_count == len(vertices) - 1:
                break

    # Validate that the graph is connected and we indeed built a spanning tree
    if kruskal_edges_count != len(vertices) - 1:
        # Not enough edges to connect all vertices: graph is disconnected
        return False

   # Ensure all vertices are in a single component
    roots = {find(v) for v in vertices}
    if len(roots) != 1:
        return False

    # Compute Prim's MST total cost from the provided result
    prims_cost: float = sum(float(weight) for _, _, weight in prims_result)

    # Compare costs with a small tolerance to account for floating-point arithmetic
    tolerance = 1e-9
    return abs(prims_cost - kruskal_cost) <= tolerance
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
    vertices = set(graph.keys())
    for neighbors in graph.values():
        vertices.update(neighbors.keys())
    
    mst_cost = sum(weight for _, _, weight in mst_edges)
    total_cost, _, savings_pct = calculate_mst_savings(graph, mst_edges)
    diameter = get_mst_diameter(mst_edges)
    
    # Edge weights statistics
    weights = [weight for _, _, weight in mst_edges]
    
    return {
        'num_vertices': len(vertices),
        'num_mst_edges': len(mst_edges),
        'mst_total_cost': mst_cost,
        'original_total_cost': total_cost,
        'cost_savings_percent': savings_pct,
        'mst_diameter': diameter,
        'min_edge_weight': min(weights) if weights else 0,
        'max_edge_weight': max(weights) if weights else 0,
        'avg_edge_weight': sum(weights) / len(weights) if weights else 0
    }
