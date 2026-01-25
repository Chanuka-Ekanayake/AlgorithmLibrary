from typing import Dict, List, Tuple, Optional, Union

# Type alias for clarity: Graph represented as adjacency list
# Each node maps to a list of (neighbor, weight) tuples
Graph = Dict[str, List[Tuple[str, Union[int, float]]]]

def bellman_ford(
    graph: Graph,
    start_node: str
) -> Tuple[Dict[str, float], Dict[str, Optional[str]], bool]:
    """
    Bellman-Ford algorithm for finding shortest paths in weighted graphs,
    including graphs with negative edge weights. Also detects negative cycles.
    
    LOGIC OVERVIEW:
    Unlike Dijkstra's greedy approach, Bellman-Ford uses Dynamic Programming
    to relax all edges |V| - 1 times, guaranteeing optimal paths even with
    negative weights. An additional iteration detects negative cycles.
    
    KEY ADVANTAGE: Can handle negative edge weights and detect negative cycles.
    TRADE-OFF: Slower than Dijkstra (O(V*E) vs O(E log V)) but more versatile.
    
    Args:
        graph: Adjacency list where each node maps to [(neighbor, weight), ...]
        start_node: The source node from which to calculate shortest paths
    
    Returns:
        A tuple containing:
        1. distances: Dictionary mapping each node to its shortest distance from start
        2. predecessors: Dictionary for path reconstruction (node -> previous_node)
        3. has_negative_cycle: Boolean indicating if a negative cycle exists
    """
    
    # --- 1. Initialization ---
    # Start with infinite distances for all nodes except the source
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    
    # Track predecessors for path reconstruction
    predecessors = {node: None for node in graph}
    
    # Get the number of vertices
    num_vertices = len(graph)
    
    # --- 2. Relaxation Phase: Repeat |V| - 1 times ---
    # Each iteration guarantees to find paths of length at most i edges
    for iteration in range(num_vertices - 1):
        # Track if any distance was updated in this iteration
        updated = False
        
        # Check all edges in the graph
        for current_node in graph:
            # Skip if current node is unreachable
            if distances[current_node] == float('inf'):
                continue
            
            # Try to relax each outgoing edge
            for neighbor, weight in graph[current_node]:
                # Calculate potential new distance
                new_distance = distances[current_node] + weight
                
                # If we found a shorter path, update it
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_node
                    updated = True
        
        # Optimization: If no updates occurred, we've found all shortest paths
        if not updated:
            break
    
    # --- 3. Negative Cycle Detection ---
    # If we can still relax any edge, a negative cycle exists
    has_negative_cycle = False
    
    for current_node in graph:
        if distances[current_node] == float('inf'):
            continue
        
        for neighbor, weight in graph[current_node]:
            new_distance = distances[current_node] + weight
            
            # If we can still improve a distance, negative cycle exists
            if new_distance < distances[neighbor]:
                has_negative_cycle = True
                break
        
        if has_negative_cycle:
            break
    
    return distances, predecessors, has_negative_cycle


def reconstruct_path(
    predecessors: Dict[str, Optional[str]],
    start_node: str,
    end_node: str
) -> Optional[List[str]]:
    """
    Reconstructs the shortest path from start to end using predecessors.
    
    Args:
        predecessors: Dictionary mapping each node to its predecessor
        start_node: The source node
        end_node: The destination node
    
    Returns:
        List of nodes representing the path, or None if no path exists
    """
    # Check if the end node is reachable
    if predecessors[end_node] is None and end_node != start_node:
        return None
    
    # Build path by backtracking from end to start
    path = []
    current = end_node
    
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    # Reverse to get path from start to end
    path.reverse()
    
    # Verify the path starts at the correct node
    if path[0] != start_node:
        return None
    
    return path


def detect_negative_cycle_nodes(
    graph: Graph,
    start_node: str
) -> Optional[List[str]]:
    """
    Identifies the nodes that are part of a negative cycle.
    
    Args:
        graph: The graph to analyze
        start_node: The source node for analysis
    
    Returns:
        List of nodes in the negative cycle, or None if no cycle exists
    """
    distances, predecessors, has_cycle = bellman_ford(graph, start_node)
    
    if not has_cycle:
        return None
    
    # Find a node affected by the negative cycle
    affected_node = None
    for current_node in graph:
        if distances[current_node] == float('inf'):
            continue
        
        for neighbor, weight in graph[current_node]:
            if distances[current_node] + weight < distances[neighbor]:
                affected_node = neighbor
                break
        
        if affected_node:
            break
    
    if not affected_node:
        return None
    
    # Trace back to find the cycle
    # Go back |V| steps to ensure we're in the cycle
    cycle_node = affected_node
    for _ in range(len(graph)):
        cycle_node = predecessors[cycle_node]
    
    # Extract the cycle
    cycle = [cycle_node]
    current = predecessors[cycle_node]
    
    while current != cycle_node:
        cycle.append(current)
        current = predecessors[current]
    
    cycle.reverse()
    return cycle
