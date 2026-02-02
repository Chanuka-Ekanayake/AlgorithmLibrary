"""
Kruskal's Minimum Spanning Tree Algorithm

This module implements Kruskal's algorithm for finding the Minimum Spanning Tree (MST)
of a weighted undirected graph using the Union-Find (Disjoint Set) data structure.

Algorithm Approach:
- Sort all edges by weight (ascending order)
- Iterate through sorted edges
- Add edge if it doesn't create a cycle (Union-Find checks this)
- Stop when MST has V-1 edges

Time Complexity: O(E log E) where E is the number of edges
Space Complexity: O(V + E) where V is the number of vertices

Author: Algorithm Library
"""

from typing import Dict, List, Tuple, Optional, Set


class UnionFind:
    """
    Union-Find (Disjoint Set Union) data structure with path compression
    and union by rank optimizations.
    
    Used to efficiently detect cycles while building the MST.
    """
    
    def __init__(self, vertices: List[str]):
        """
        Initialize Union-Find structure.
        
        Args:
            vertices: List of vertex names
        """
        self.parent: Dict[str, str] = {v: v for v in vertices}
        self.rank: Dict[str, int] = {v: 0 for v in vertices}
    
    def find(self, vertex: str) -> str:
        """
        Find the root/representative of the set containing vertex.
        Uses path compression for optimization.
        
        Args:
            vertex: Vertex to find root for
            
        Returns:
            Root vertex of the set
        """
        if self.parent[vertex] != vertex:
            # Path compression: make vertex point directly to root
            self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]
    
    def union(self, vertex1: str, vertex2: str) -> bool:
        """
        Union two sets containing vertex1 and vertex2.
        Uses union by rank for optimization.
        
        Args:
            vertex1: First vertex
            vertex2: Second vertex
            
        Returns:
            True if union performed (vertices were in different sets),
            False if already in same set (would create cycle)
        """
        root1 = self.find(vertex1)
        root2 = self.find(vertex2)
        
        # Already in same set - would create cycle
        if root1 == root2:
            return False
        
        # Union by rank: attach smaller tree under larger tree
        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        else:
            self.parent[root2] = root1
            self.rank[root1] += 1
        
        return True
    
    def connected(self, vertex1: str, vertex2: str) -> bool:
        """
        Check if two vertices are in the same connected component.
        
        Args:
            vertex1: First vertex
            vertex2: Second vertex
            
        Returns:
            True if vertices are connected, False otherwise
        """
        return self.find(vertex1) == self.find(vertex2)


def kruskals_mst(graph: Dict[str, Dict[str, float]]) -> Optional[Tuple[List[Tuple[str, str, float]], float]]:
    """
    Find Minimum Spanning Tree using Kruskal's algorithm.
    
    Algorithm:
    1. Extract and sort all edges by weight
    2. Initialize Union-Find for all vertices
    3. For each edge (u, v, weight) in sorted order:
       - If u and v are not connected (different components):
         - Add edge to MST
         - Union the components
    4. Stop when MST has V-1 edges
    
    Args:
        graph: Adjacency list representation {vertex: {neighbor: weight}}
               Must be undirected (symmetric)
    
    Returns:
        Tuple of (mst_edges, total_cost) where:
        - mst_edges: List of (vertex1, vertex2, weight) tuples
        - total_cost: Sum of edge weights in MST
        
        Returns None if graph is empty or disconnected
    
    Time Complexity: O(E log E) for sorting edges
    Space Complexity: O(V + E) for Union-Find and edge list
    
    Example:
        >>> graph = {
        ...     'A': {'B': 4, 'C': 3},
        ...     'B': {'A': 4, 'C': 1, 'D': 2},
        ...     'C': {'A': 3, 'B': 1, 'D': 5},
        ...     'D': {'B': 2, 'C': 5}
        ... }
        >>> edges, cost = kruskals_mst(graph)
        >>> cost
        6.0
        >>> len(edges)
        3
    """
    if not graph:
        return None
    
    # Extract all vertices
    vertices = list(graph.keys())
    num_vertices = len(vertices)
    
    if num_vertices == 0:
        return None
    
    # Edge case: single vertex
    if num_vertices == 1:
        return ([], 0.0)
    
    # Step 1: Extract all edges (avoid duplicates in undirected graph)
    edges: List[Tuple[float, str, str]] = []
    seen_edges: Set[Tuple[str, str]] = set()
    
    for u in graph:
        for v, weight in graph[u].items():
            # Avoid duplicate edges in undirected graph
            edge_id = tuple(sorted([u, v]))
            if edge_id not in seen_edges:
                edges.append((weight, u, v))
                seen_edges.add(edge_id)
    
    # Step 2: Sort edges by weight (key operation - O(E log E))
    edges.sort()
    
    # Step 3: Initialize Union-Find
    uf = UnionFind(vertices)
    
    # Step 4: Build MST by processing edges in sorted order
    mst_edges: List[Tuple[str, str, float]] = []
    total_cost: float = 0.0
    
    for weight, u, v in edges:
        # Try to add edge - only succeeds if doesn't create cycle
        if uf.union(u, v):
            mst_edges.append((u, v, weight))
            total_cost += weight
            
            # Early termination: MST complete when we have V-1 edges
            if len(mst_edges) == num_vertices - 1:
                break
    
    # Verify we found a complete MST (graph was connected)
    if len(mst_edges) != num_vertices - 1:
        # Graph is disconnected - MST doesn't exist
        return None
    
    return (mst_edges, total_cost)


def build_mst_graph(mst_edges: List[Tuple[str, str, float]]) -> Dict[str, Dict[str, float]]:
    """
    Convert MST edge list to adjacency list representation.
    
    Args:
        mst_edges: List of (vertex1, vertex2, weight) tuples
    
    Returns:
        Adjacency list graph representation
    
    Example:
        >>> edges = [('A', 'B', 4), ('B', 'C', 1)]
        >>> graph = build_mst_graph(edges)
        >>> graph['A']
        {'B': 4}
        >>> graph['B']
        {'A': 4, 'C': 1}
    """
    mst_graph: Dict[str, Dict[str, float]] = {}
    
    for u, v, weight in mst_edges:
        if u not in mst_graph:
            mst_graph[u] = {}
        if v not in mst_graph:
            mst_graph[v] = {}
        
        mst_graph[u][v] = weight
        mst_graph[v][u] = weight
    
    return mst_graph


def is_graph_connected(graph: Dict[str, Dict[str, float]]) -> bool:
    """
    Check if graph is connected using DFS.
    
    Args:
        graph: Adjacency list representation
    
    Returns:
        True if all vertices are reachable from any starting vertex
    
    Time Complexity: O(V + E)
    
    Example:
        >>> connected_graph = {'A': {'B': 1}, 'B': {'A': 1, 'C': 2}, 'C': {'B': 2}}
        >>> is_graph_connected(connected_graph)
        True
        >>> disconnected = {'A': {'B': 1}, 'B': {'A': 1}, 'C': {}}
        >>> is_graph_connected(disconnected)
        False
    """
    if not graph:
        return False
    
    # Start DFS from arbitrary vertex
    start = next(iter(graph))
    visited: Set[str] = set()
    stack = [start]
    
    while stack:
        vertex = stack.pop()
        if vertex in visited:
            continue
        
        visited.add(vertex)
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                stack.append(neighbor)
    
    return len(visited) == len(graph)


def find_mst_forest(graph: Dict[str, Dict[str, float]]) -> List[Tuple[List[Tuple[str, str, float]], float]]:
    """
    Find Minimum Spanning Forest for disconnected graph.
    Returns MST for each connected component.
    
    Args:
        graph: Adjacency list (may be disconnected)
    
    Returns:
        List of (mst_edges, total_cost) for each component
    
    Example:
        >>> graph = {
        ...     'A': {'B': 1}, 'B': {'A': 1},
        ...     'C': {'D': 2}, 'D': {'C': 2}
        ... }
        >>> forest = find_mst_forest(graph)
        >>> len(forest)
        2
    """
    if not graph:
        return []
    
    # Find all connected components
    visited: Set[str] = set()
    components: List[List[str]] = []
    
    for vertex in graph:
        if vertex in visited:
            continue
        
        # DFS to find component
        component: List[str] = []
        stack = [vertex]
        
        while stack:
            v = stack.pop()
            if v in visited:
                continue
            
            visited.add(v)
            component.append(v)
            
            for neighbor in graph[v]:
                if neighbor not in visited:
                    stack.append(neighbor)
        
        components.append(component)
    
    # Build MST for each component
    forest: List[Tuple[List[Tuple[str, str, float]], float]] = []
    
    for component in components:
        # Extract subgraph for this component
        subgraph = {v: graph[v] for v in component}
        
        result = kruskals_mst(subgraph)
        if result:
            forest.append(result)
    
    return forest


def compare_edge_weights(mst_edges: List[Tuple[str, str, float]]) -> Dict[str, any]:
    """
    Analyze distribution of edge weights in MST.
    
    Args:
        mst_edges: MST edges
    
    Returns:
        Dictionary with statistics about edge weights
    """
    if not mst_edges:
        return {
            'min_weight': 0,
            'max_weight': 0,
            'avg_weight': 0,
            'total_weight': 0,
            'weight_range': 0
        }
    
    weights = [weight for _, _, weight in mst_edges]
    
    return {
        'min_weight': min(weights),
        'max_weight': max(weights),
        'avg_weight': sum(weights) / len(weights),
        'total_weight': sum(weights),
        'weight_range': max(weights) - min(weights),
        'num_edges': len(weights)
    }


def get_critical_edges(graph: Dict[str, Dict[str, float]], mst_edges: List[Tuple[str, str, float]]) -> List[Tuple[str, str, float]]:
    """
    Identify edges that, if removed, would increase MST cost.
    In an MST, ALL edges are critical (removing any disconnects the tree).
    
    This function returns edges sorted by weight to identify most expensive critical connections.
    
    Args:
        graph: Original graph
        mst_edges: MST edges
    
    Returns:
        MST edges sorted by weight (descending)
    """
    return sorted(mst_edges, key=lambda x: x[2], reverse=True)


def calculate_mst_savings(graph: Dict[str, Dict[str, float]], mst_cost: float) -> float:
    """
    Calculate cost savings of MST vs building all connections.
    
    Args:
        graph: Original graph with all possible edges
        mst_cost: Total cost of MST
    
    Returns:
        Cost savings (total possible cost - MST cost)
    """
    total_possible_cost = sum(
        weight for vertex in graph
        for weight in graph[vertex].values()
    ) / 2  # Divide by 2 since undirected edges counted twice
    
    return total_possible_cost - mst_cost


if __name__ == "__main__":
    # Example usage and testing
    print("Kruskal's MST Algorithm Demo")
    print("=" * 50)
    
    # Example graph
    example_graph = {
        'A': {'B': 4, 'H': 8},
        'B': {'A': 4, 'C': 8, 'H': 11},
        'C': {'B': 8, 'D': 7, 'F': 4, 'I': 2},
        'D': {'C': 7, 'E': 9, 'F': 14},
        'E': {'D': 9, 'F': 10},
        'F': {'C': 4, 'D': 14, 'E': 10, 'G': 2},
        'G': {'F': 2, 'H': 1, 'I': 6},
        'H': {'A': 8, 'B': 11, 'G': 1, 'I': 7},
        'I': {'C': 2, 'G': 6, 'H': 7}
    }
    
    print("\nCalculating MST using Kruskal's algorithm...")
    result = kruskals_mst(example_graph)
    
    if result:
        mst_edges, total_cost = result
        
        print(f"\n✓ MST Found!")
        print(f"Total Cost: {total_cost}")
        print(f"Number of Edges: {len(mst_edges)}")
        print("\nMST Edges (sorted by weight):")
        
        for u, v, weight in sorted(mst_edges, key=lambda x: x[2]):
            print(f"  {u} -- {v}: {weight}")
        
        savings = calculate_mst_savings(example_graph, total_cost)
        print(f"\nCost Savings: {savings:.2f}")
        
        stats = compare_edge_weights(mst_edges)
        print(f"\nEdge Weight Statistics:")
        print(f"  Min: {stats['min_weight']}")
        print(f"  Max: {stats['max_weight']}")
        print(f"  Average: {stats['avg_weight']:.2f}")
    else:
        print("✗ Graph is disconnected - no MST exists")
