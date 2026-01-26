from typing import Dict, List, Tuple, Optional, Union, Set
import math

# Type alias for clarity
Graph = Dict[str, Dict[str, Union[int, float]]]

def floyd_warshall(
    graph: Graph
) -> Tuple[Dict[Tuple[str, str], float], Dict[Tuple[str, str], Optional[str]]]:
    """
    Floyd-Warshall algorithm for finding shortest paths between ALL pairs of vertices.
    
    LOGIC OVERVIEW:
    Uses Dynamic Programming with a 3-nested loop structure to iteratively improve
    shortest path estimates by considering intermediate vertices. Unlike single-source
    algorithms (Dijkstra, Bellman-Ford), this computes paths between every pair.
    
    KEY ADVANTAGE: Finds ALL pairs shortest paths in one execution.
    TRADE-OFF: O(V³) complexity makes it less suitable for very large graphs.
    CAN HANDLE: Negative edge weights (but not negative cycles).
    
    Args:
        graph: Adjacency list where each node maps to {neighbor: weight, ...}
    
    Returns:
        A tuple containing:
        1. distances: Dictionary mapping (source, dest) tuples to shortest distance
        2. next_node: Dictionary for path reconstruction (source, dest) -> next node
    """
    
    # --- 1. Extract all vertices ---
    vertices = set(graph.keys())
    for neighbors in graph.values():
        vertices.update(neighbors.keys())
    vertices = sorted(vertices)  # Consistent ordering
    
    # --- 2. Initialize distance and next matrices ---
    # Distance: Start with infinity for all pairs except direct edges
    distances: Dict[Tuple[str, str], float] = {}
    next_node: Dict[Tuple[str, str], Optional[str]] = {}
    
    # Initialize with infinity
    for i in vertices:
        for j in vertices:
            distances[(i, j)] = float('inf')
            next_node[(i, j)] = None
    
    # Distance from vertex to itself is 0
    for v in vertices:
        distances[(v, v)] = 0
    
    # Initialize with direct edges
    for u in graph:
        for v, weight in graph[u].items():
            distances[(u, v)] = weight
            next_node[(u, v)] = v
    
    # --- 3. Floyd-Warshall Main Loop ---
    # Try each vertex as an intermediate point
    for k in vertices:
        # For each pair of vertices
        for i in vertices:
            for j in vertices:
                # Check if path through k is shorter
                # dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
                new_distance = distances[(i, k)] + distances[(k, j)]
                
                if new_distance < distances[(i, j)]:
                    distances[(i, j)] = new_distance
                    # Path from i to j goes through same intermediate as i to k
                    next_node[(i, j)] = next_node[(i, k)]
    
    return distances, next_node


def reconstruct_path(
    next_node: Dict[Tuple[str, str], Optional[str]],
    start: str,
    end: str
) -> Optional[List[str]]:
    """
    Reconstructs the shortest path between two vertices.
    
    Args:
        next_node: Next node dictionary from floyd_warshall
        start: Source vertex
        end: Destination vertex
    
    Returns:
        List of vertices representing the path, or None if no path exists
    """
    if next_node[(start, end)] is None:
        return None
    
    path = [start]
    current = start
    
    while current != end:
        current = next_node[(current, end)]
        if current is None:
            return None
        path.append(current)
    
    return path


def detect_negative_cycle(
    graph: Graph,
    distances: Dict[Tuple[str, str], float]
) -> bool:
    """
    Detects if the graph contains a negative cycle.
    A negative cycle exists if any vertex has a negative distance to itself.
    
    Args:
        graph: The original graph
        distances: Distance matrix from floyd_warshall
    
    Returns:
        True if negative cycle exists, False otherwise
    """
    vertices = set(graph.keys())
    for neighbors in graph.values():
        vertices.update(neighbors.keys())
    
    for v in vertices:
        if distances[(v, v)] < 0:
            return True
    
    return False


def get_distance_matrix(
    graph: Graph
) -> Dict[Tuple[str, str], float]:
    """
    Returns only the distance matrix without path reconstruction data.
    More memory efficient when paths are not needed.
    
    Args:
        graph: The graph to analyze
    
    Returns:
        Dictionary mapping (source, dest) to shortest distance
    """
    distances, _ = floyd_warshall(graph)
    return distances


def get_graph_diameter(
    graph: Graph
) -> float:
    """
    Computes the diameter of the graph (longest shortest path).
    
    The diameter represents the "worst-case" distance in the network,
    useful for analyzing network connectivity and performance.
    
    Args:
        graph: The graph to analyze
    
    Returns:
        The diameter (maximum shortest path length), or inf if graph is disconnected
    """
    distances = get_distance_matrix(graph)
    
    max_distance = 0
    for (i, j), dist in distances.items():
        if i != j and dist != float('inf'):
            max_distance = max(max_distance, dist)
    
    return max_distance if max_distance > 0 else float('inf')


def get_graph_center(
    graph: Graph
) -> Tuple[str, float]:
    """
    Finds the center of the graph (vertex that minimizes maximum distance to others).
    
    The center is useful for optimal placement of servers, warehouses, etc.
    
    Args:
        graph: The graph to analyze
    
    Returns:
        Tuple of (center_vertex, eccentricity)
    """
    distances = get_distance_matrix(graph)
    
    vertices = set(graph.keys())
    for neighbors in graph.values():
        vertices.update(neighbors.keys())
    
    min_eccentricity = float('inf')
    center = None
    
    for v in vertices:
        # Eccentricity: maximum distance from v to any other vertex
        eccentricity = 0
        for u in vertices:
            if v != u and distances[(v, u)] != float('inf'):
                eccentricity = max(eccentricity, distances[(v, u)])
        
        if eccentricity < min_eccentricity:
            min_eccentricity = eccentricity
            center = v
    
    return center, min_eccentricity


def find_all_shortest_paths_from(
    graph: Graph,
    source: str
) -> Dict[str, Tuple[float, Optional[List[str]]]]:
    """
    Finds shortest paths from a source to all other vertices.
    Convenience function for single-source queries using Floyd-Warshall.
    
    Args:
        graph: The graph to analyze
        source: Source vertex
    
    Returns:
        Dictionary mapping destination to (distance, path) tuple
    """
    distances, next_node = floyd_warshall(graph)
    
    vertices = set(graph.keys())
    for neighbors in graph.values():
        vertices.update(neighbors.keys())
    
    result = {}
    for dest in vertices:
        if dest != source:
            dist = distances[(source, dest)]
            path = reconstruct_path(next_node, source, dest) if dist != float('inf') else None
            result[dest] = (dist, path)
    
    return result


def transitive_closure(
    graph: Graph
) -> Dict[Tuple[str, str], bool]:
    """
    Computes the transitive closure of the graph.
    Determines reachability: can we get from i to j through any path?
    
    Uses Floyd-Warshall logic with boolean values instead of distances.
    
    Args:
        graph: The graph to analyze
    
    Returns:
        Dictionary mapping (i, j) to True if path exists, False otherwise
    """
    vertices = set(graph.keys())
    for neighbors in graph.values():
        vertices.update(neighbors.keys())
    vertices = sorted(vertices)
    
    # Initialize reachability matrix
    reach: Dict[Tuple[str, str], bool] = {}
    
    for i in vertices:
        for j in vertices:
            reach[(i, j)] = False
    
    # Vertex can reach itself
    for v in vertices:
        reach[(v, v)] = True
    
    # Direct edges create reachability
    for u in graph:
        for v in graph[u]:
            reach[(u, v)] = True
    
    # Floyd-Warshall for transitive closure
    for k in vertices:
        for i in vertices:
            for j in vertices:
                reach[(i, j)] = reach[(i, j)] or (reach[(i, k)] and reach[(k, j)])
    
    return reach
