"""
Kruskal's Algorithm Implementation
Provides an optimized Minimum Spanning Tree (MST) solution for 
undirected, weighted graphs using the Disjoint Set Union (DSU) pattern.
"""

from typing import List, Tuple, Any

class DisjointSetUnion:
    """
    An optimized DSU (Union-Find) structure.
    Implements Path Compression and Union by Rank to achieve O(alpha(N)) 
    time complexity, where alpha is the inverse Ackermann function.
    """
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, i: int) -> int:
        """Finds the root of the element with path compression."""
        if self.parent[i] == i:
            return i
        # Recursive path compression
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        """
        Merges two sets using rank optimization to keep the tree shallow.
        Returns True if a merge occurred, False if they were already in the same set.
        """
        root_i = self.find(i)
        root_j = self.find(j)
        
        if root_i != root_j:
            # Union by rank: Attach smaller tree under the larger tree
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_i] = root_j
                self.rank[root_j] += 1
            return True
        return False

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