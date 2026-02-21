import heapq
from typing import Dict, List, Tuple, Optional, Union

# Type aliases
Graph = Dict[str, Dict[str, Union[int, float]]]
DistMatrix = Dict[Tuple[str, str], float]
NextMatrix = Dict[Tuple[str, str], Optional[str]]


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: Bellman-Ford on the augmented graph (Johnson's reweighting)
# ─────────────────────────────────────────────────────────────────────────────

def _bellman_ford_reweight(
    graph: Graph,
    vertices: List[str],
    source: str
) -> Optional[Dict[str, float]]:
    """
    Runs Bellman-Ford from a virtual source 's' connected to every vertex
    with edge weight 0.  Returns h[v] = shortest distance from 's' to v,
    or None if a negative cycle is detected.

    LOGIC OVERVIEW:
    Johnson's adds a dummy vertex 's' with zero-weight edges to all vertices.
    Bellman-Ford computes h[v] = dist(s, v).  These h-values are then used
    to reweight every original edge (u→v) to:
        w'(u,v) = w(u,v) + h[u] - h[v]  ≥ 0
    guaranteeing non-negative weights so Dijkstra can run correctly.

    Args:
        graph: Original weighted directed graph.
        vertices: All vertices in the graph.
        source: Name of the virtual source vertex (must not exist in graph).

    Returns:
        Dictionary h[v] of reweighting potentials, or None if negative cycle.
    """
    # Initialize distances: 0 for the virtual source, ∞ for everything else
    h: Dict[str, float] = {v: float('inf') for v in vertices}
    h[source] = 0.0

    # Relax all edges |V| − 1 times
    n = len(vertices)
    for _ in range(n - 1):
        updated = False
        # Virtual source edges to every vertex (weight 0)
        for v in vertices:
            if h[source] + 0 < h[v]:
                h[v] = h[source] + 0
                updated = True
        # Original edges
        for u in graph:
            for v, w in graph[u].items():
                if h[u] != float('inf') and h[u] + w < h[v]:
                    h[v] = h[u] + w
                    updated = True
        if not updated:
            break  # Converged early

    # Negative-cycle check: one more relaxation pass
    for u in graph:
        for v, w in graph[u].items():
            if h[u] != float('inf') and h[u] + w < h[v]:
                return None  # Negative cycle detected

    return h


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: Dijkstra on the reweighted graph (single source)
# ─────────────────────────────────────────────────────────────────────────────

def _dijkstra(
    graph: Graph,
    h: Dict[str, float],
    source: str,
    vertices: List[str]
) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """
    Standard Dijkstra with a min-heap on the reweighted graph.

    Each edge (u→v) with original weight w uses reweighted cost:
        w'(u,v) = w(u,v) + h[u] - h[v]   (always ≥ 0)

    The true shortest distance is recovered at the end by reversing the
    reweighting: dist(u,v) = dijkstra_dist(u,v) - h[u] + h[v]

    Args:
        graph: Original weighted graph.
        h: Reweighting potentials from Bellman-Ford.
        source: Current source vertex.
        vertices: All graph vertices.

    Returns:
        (dist, prev) — distances and predecessor map from source.
    """
    dist: Dict[str, float] = {v: float('inf') for v in vertices}
    prev: Dict[str, Optional[str]] = {v: None for v in vertices}
    dist[source] = 0.0

    # Min-heap: (reweighted_distance, vertex)
    heap: List[Tuple[float, str]] = [(0.0, source)]

    while heap:
        d_u, u = heapq.heappop(heap)
        if d_u > dist[u]:
            continue  # Stale entry

        for v, w in graph.get(u, {}).items():
            # Reweighted edge cost (guaranteed ≥ 0)
            w_prime = w + h[u] - h[v]
            new_dist = dist[u] + w_prime
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))

    return dist, prev


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def johnsons(
    graph: Graph
) -> Tuple[DistMatrix, NextMatrix]:
    """
    Johnson's Algorithm — All-Pairs Shortest Paths for sparse graphs.

    ALGORITHM OVERVIEW (3 phases):
    1. Add a virtual source 's' with 0-weight edges to every vertex.
    2. Run Bellman-Ford from 's' → compute reweighting potentials h[v].
    3. For each real vertex u, run Dijkstra on the reweighted graph,
       then reverse the reweighting to recover true distances.

    HANDLES: Negative edge weights (detects negative cycles).
    BEST FOR: Sparse graphs where E << V², outperforms Floyd-Warshall.
    TIME: O(VE log V + VE) with binary heap (often written as O(VE log V) worst-case).
    SPACE: O(V²) for the all-pairs result matrices.

    Args:
        graph: Adjacency list — {u: {v: weight, ...}, ...}

    Returns:
        Tuple of:
        - distances: {(u, v): shortest_distance}   (float('inf') if unreachable)
        - next_node: {(u, v): first_step_toward_v}  (None if unreachable)

    Raises:
        ValueError: If a negative cycle is detected.
    """
    # --- Collect all vertices ---
    vertices: List[str] = sorted(
        set(graph.keys()) | {v for nbrs in graph.values() for v in nbrs}
    )

    if not vertices:
        return {}, {}

    # --- Phase 1: Reweight via Bellman-Ford ---
    base_virtual_source = "__johnson_source__"
    virtual_source = base_virtual_source
    counter = 0
    # Ensure the virtual source name does not collide with any existing vertex
    while virtual_source in vertices:
        counter += 1
        virtual_source = f"{base_virtual_source}_{counter}"

    h = _bellman_ford_reweight(graph, vertices, virtual_source)
    if h is None:
        raise ValueError(
            "Johnson's Algorithm: Negative cycle detected in graph. "
            "No shortest paths exist."
        )

    # --- Phase 2 & 3: Dijkstra from every vertex, then unweight ---
    distances: DistMatrix = {}
    next_node: NextMatrix = {}

    # Self-distances
    for v in vertices:
        distances[(v, v)] = 0.0
        next_node[(v, v)] = v

    for source in vertices:
        d_reweighted, prev = _dijkstra(graph, h, source, vertices)

        for dest in vertices:
            if dest == source:
                continue

            # Reverse the reweighting: true_dist = d' - h[source] + h[dest]
            if d_reweighted[dest] == float('inf'):
                distances[(source, dest)] = float('inf')
                next_node[(source, dest)] = None
            else:
                distances[(source, dest)] = d_reweighted[dest] - h[source] + h[dest]

                # Build next_node for path reconstruction
                # Trace back from dest through prev to find first step from source
                cur = dest
                while prev.get(cur) is not None and prev[cur] != source:
                    cur = prev[cur]
                next_node[(source, dest)] = cur if prev.get(cur) == source else None

    return distances, next_node


def reconstruct_path(
    next_node: NextMatrix,
    start: str,
    end: str
) -> Optional[List[str]]:
    """
    Reconstructs the shortest path between two vertices.

    Args:
        next_node: Next-node matrix from johnsons().
        start: Source vertex.
        end: Destination vertex.

    Returns:
        Ordered list of vertices on the shortest path, or None if unreachable.
    """
    if start == end:
        return [start]
    if next_node.get((start, end)) is None:
        return None

    path = [start]
    current = start
    visited = set()

    while current != end:
        if current in visited:
            return None  # Cycle guard
        visited.add(current)

        step = next_node.get((current, end))
        if step is None:
            return None
        path.append(step)
        current = step

    return path


def detect_negative_cycle(graph: Graph) -> bool:
    """
    Returns True if the graph contains a negative cycle.
    Runs the Bellman-Ford phase of Johnson's and checks the result.

    Args:
        graph: Weighted directed graph.

    Returns:
        True if a negative cycle exists, False otherwise.
    """
    vertices = sorted(
        set(graph.keys()) | {v for nbrs in graph.values() for v in nbrs}
    )
    virtual_source = "__neg_cycle_check__"
    if virtual_source in vertices:
        base = virtual_source
        suffix = 1
        while virtual_source in vertices:
            virtual_source = f"{base}_{suffix}"
            suffix += 1
    h = _bellman_ford_reweight(graph, vertices, virtual_source)
    return h is None


def get_distance_matrix(graph: Graph) -> DistMatrix:
    """
    Returns only the all-pairs distance matrix (no path data).
    Convenience wrapper around johnsons() for distance-only queries.

    Args:
        graph: Weighted directed graph.

    Returns:
        {(u, v): shortest_distance} for all vertex pairs.
    """
    distances, _ = johnsons(graph)
    return distances


def find_all_shortest_paths_from(
    graph: Graph,
    source: str
) -> Dict[str, Tuple[float, Optional[List[str]]]]:
    """
    Finds shortest paths from a single source to all other vertices.
    Uses Johnson's full computation for consistency; useful when you need
    paths and the graph has negative weights.

    Args:
        graph: Weighted directed graph.
        source: Source vertex.

    Returns:
        {destination: (distance, path_list)} for all destinations.
    """
    distances, next_node = johnsons(graph)
    vertices = sorted(
        set(graph.keys()) | {v for nbrs in graph.values() for v in nbrs}
    )
    result: Dict[str, Tuple[float, Optional[List[str]]]] = {}
    for dest in vertices:
        if dest != source:
            dist = distances[(source, dest)]
            path = reconstruct_path(next_node, source, dest) if dist != float('inf') else None
            result[dest] = (dist, path)
    return result


def get_graph_diameter(graph: Graph) -> float:
    """
    Computes the diameter of the graph (longest shortest path between any pair).

    Args:
        graph: Weighted directed graph.

    Returns:
        Diameter value, or float('inf') if the graph is disconnected.
    """
    distances = get_distance_matrix(graph)
    vertices = sorted(
        set(graph.keys()) | {v for nbrs in graph.values() for v in nbrs}
    )

    diameter = 0.0
    for u in vertices:
        for v in vertices:
            if u != v:
                d = distances.get((u, v), float('inf'))
                if d == float('inf'):
                    return float('inf')
                diameter = max(diameter, d)
    return diameter


def get_graph_center(graph: Graph) -> Tuple[Optional[str], float]:
    """
    Finds the center of the graph: the vertex that minimises its maximum
    distance (eccentricity) to any other reachable vertex.

    Args:
        graph: Weighted directed graph.

    Returns:
        (center_vertex, eccentricity) tuple.
    """
    distances = get_distance_matrix(graph)
    vertices = sorted(
        set(graph.keys()) | {v for nbrs in graph.values() for v in nbrs}
    )

    best_vertex: Optional[str] = None
    best_ecc = float('inf')

    for u in vertices:
        ecc = max(
            (distances.get((u, v), float('inf')) for v in vertices if v != u),
            default=0.0
        )
        if ecc < best_ecc:
            best_ecc = ecc
            best_vertex = u

    return best_vertex, best_ecc
