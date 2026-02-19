from collections import deque
from typing import Dict, List, Tuple, Optional, Union

# Define a Type Alias for clarity: A Graph is a Dictionary of Nodes 
# mapped to another Dictionary of {Neighbor: Capacity}
Graph = Dict[str, Dict[str, int]]

def bfs(graph: Graph, source: str, sink: str, parent: Dict[str, Optional[str]]) -> bool:
    """
    Breadth-First Search to find an augmenting path from source to sink.
    
    Args:
        graph: The residual graph where values represent residual capacity.
        source: The starting node.
        sink: The target node.
        parent: A dictionary to store the path (node -> previous_node).
        
    Returns:
        True if a path exists from source to sink, False otherwise.
    """
    visited = set()
    queue = deque([source])
    visited.add(source)
    parent[source] = None
    
    while queue:
        u = queue.popleft()
        
        for v, capacity in graph.get(u, {}).items():
            if v not in visited and capacity > 0:
                queue.append(v)
                visited.add(v)
                parent[v] = u
                if v == sink:
                    return True
    return False

def get_max_flow(graph: Graph, source: str, sink: str) -> Tuple[int, Graph]:
    """
    Calculates the maximum flow from a source to a sink in a flow network
    using the Edmonds-Karp algorithm.
    
    Args:
        graph: The adjacency representation of the network with capacities.
               Note: This graph structure requires backward edges to be initialized 
               with 0 capacity if they don't exist in the input.
        source: The identifier for the source node.
        sink: The identifier for the sink node.
        
    Returns:
        A tuple containing:
        1. max_flow: The maximum flow value.
        2. flow_network: The final state of the residual graph.
    """
    # Create a residual graph. copying logic to avoid mutating the original input if needed
    # We need to ensure every directed edge u->v has a corresponding v->u with 0 capacity if not present
    residual_graph = {u: dict(neighbors) for u, neighbors in graph.items()}
    for u in graph:
        for v in graph[u]:
            if v not in residual_graph:
                residual_graph[v] = {}
            if u not in residual_graph[v]:
                residual_graph[v][u] = 0
                
    max_flow = 0
    parent: Dict[str, Optional[str]] = {}
    
    # Loop while there is an augmenting path from source to sink
    while bfs(residual_graph, source, sink, parent):
        # Find minimum residual capacity of the edges along the path found by BFS.
        path_flow = float('inf')
        s = sink
        while s != source:
            # key error potential if parent[s] is None, but bfs ensures it isn't for the path
            u = parent[s]
            path_flow = min(path_flow, residual_graph[u][s])
            s = parent[s]
            
        # Update residual capacities of the edges and reverse edges along the path
        max_flow += path_flow
        v = sink
        while v != source:
            u = parent[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v][u] += path_flow
            v = parent[v]
            
    return max_flow, residual_graph
