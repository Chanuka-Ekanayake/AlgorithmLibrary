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

from typing import Any, Dict, List, Tuple, Optional, Set


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
    """
    if not graph:
        return None
    
    # Extract all vertices
    vertices = list(graph.keys())
    num_vertices = len(vertices)
    
    # Edge case: single vertex
    if num_vertices == 1:
        return ([], 0.0)
    
    # Step 1: Extract all edges (avoid duplicates in undirected graph)
    edges: List[Tuple[float, str, str]] = []
    seen_edges: Set[Tuple[str, str]] = set()
    
    for u in graph:
        for v, weight in graph[u].items():
            # Avoid duplicate edges in undirected graph
            edge_id = (u, v) if u < v else (v, u)
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


# Legacy function name for backwards compatibility
def kruskal_mst(edges: List[Tuple[Any, Any, float]], n: int) -> Tuple[List[Tuple], float]:
    """Legacy interface - converts to new format."""
    # Convert old format to new
    graph: Dict[str, Dict[str, float]] = {}
    for u, v, weight in edges:
        u_str, v_str = str(u), str(v)
        if u_str not in graph:
            graph[u_str] = {}
        if v_str not in graph:
            graph[v_str] = {}
        graph[u_str][v_str] = weight
        graph[v_str][u_str] = weight
    
    result = kruskals_mst(graph)
    if result:
        return result
    return ([], 0.0)
class KruskalMST:
    """
    Engine for calculating the Minimum Spanning Tree (MST).
    Suitable for optimizing physical or virtual network connectivity.
    """

    @staticmethod
    def calculate_mst(node_count: int, edges: List[Tuple[int, int, int]]) -> Tuple[List[Tuple[int, int, int]], int]:
        """
        Calculates the MST using a greedy approach.
        
        Args:
            node_count: Total number of vertices in the graph.
            edges: A list of tuples in the format (weight, u, v).
            
        Returns:
            A tuple containing (list_of_mst_edges, total_minimal_cost).
        """
        # 1. Sort all edges in non-decreasing order of their weight
        # This is the "Greedy" step of the algorithm.
        sorted_edges = sorted(edges, key=lambda item: item[0])
        
        dsu = DisjointSetUnion(node_count)
        mst_edges = []
        total_weight = 0

        # 2. Iterate through sorted edges and pick those that don't form a cycle
        for weight, u, v in sorted_edges:
            if dsu.union(u, v):
                mst_edges.append((u, v, weight))
                total_weight += weight
            
            # Optimization: If we have V-1 edges, we have a complete MST
            if len(mst_edges) == node_count - 1:
                break
                
        return mst_edges, total_weight