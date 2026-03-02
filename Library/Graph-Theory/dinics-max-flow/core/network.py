"""
Dinic's Algorithm (Maximum Flow)
An advanced graph theory engine used to calculate the maximum possible 
throughput in a flow network. It utilizes Level Graphs and Dead-End Pruning 
to achieve highly efficient O(V^2 E) performance.
"""

from typing import List
from collections import deque

class Edge:
    """Represents a directional capacity link between two nodes (servers)."""
    __slots__ = ['target', 'capacity', 'flow', 'rev_index']

    def __init__(self, target: int, capacity: float, rev_index: int):
        self.target = target
        self.capacity = capacity
        self.flow = 0.0
        # Tracks the index of the reverse edge in the target node's adjacency list
        self.rev_index = rev_index 

class DinicMaxFlow:
    """
    Calculates the maximum data throughput from a source node to a sink node.
    """
    
    def __init__(self, num_nodes: int):
        self.n = num_nodes
        # The graph is a list of lists, where graph[i] contains all edges leaving node i
        self.graph: List[List[Edge]] = [[] for _ in range(num_nodes)]
        # Stores the "level" (distance from source) for each node
        self.level = [-1] * num_nodes

    def add_edge(self, source: int, target: int, capacity: float) -> None:
        """
        Adds a directed edge and its corresponding residual (reverse) edge.
        """
        if source == target:
            raise ValueError("Cannot add an edge from a node to itself.")
            
        # The forward edge starts with the given capacity and 0 flow
        forward_edge = Edge(target, capacity, len(self.graph[target]))
        
        # The reverse edge starts with 0 capacity. This is critical for 
        # allowing the algorithm to "undo" bad routing decisions later.
        reverse_edge = Edge(source, 0.0, len(self.graph[source]))
        
        self.graph[source].append(forward_edge)
        self.graph[target].append(reverse_edge)

    def _bfs_build_level_graph(self, source: int, sink: int) -> bool:
        """
        Phase 1: Organizes nodes into strict levels based on distance from the source.
        Returns True if the sink is still reachable, False if the network is fully saturated.
        """
        self.level = [-1] * self.n
        self.level[source] = 0
        
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            
            for edge in self.graph[current]:
                # If the target node hasn't been visited AND the edge has remaining capacity
                if self.level[edge.target] < 0 and edge.flow < edge.capacity:
                    self.level[edge.target] = self.level[current] + 1
                    queue.append(edge.target)
                    
        # If the sink's level is no longer -1, a path exists.
        return self.level[sink] >= 0

    def _dfs_find_blocking_flow(self, current: int, sink: int, current_flow: float, start_index: List[int]) -> float:
        """
        Phase 2: Pushes the maximum possible data forward through the level graph.
        """
        if current == sink:
            return current_flow

        # We use start_index to remember which edges we've already fully saturated.
        # This is "Dead-End Pruning" and prevents infinite loops of checking dead paths.
        for i in range(start_index[current], len(self.graph[current])):
            edge = self.graph[current][i]
            
            # Data can ONLY flow to a node that is exactly one level deeper
            if self.level[edge.target] == self.level[current] + 1 and edge.flow < edge.capacity:
                
                # The maximum flow we can push is the bottleneck of the path
                bottleneck = min(current_flow, edge.capacity - edge.flow)
                
                # Recursively push flow to the next node
                pushed = self._dfs_find_blocking_flow(edge.target, sink, bottleneck, start_index)
                
                if pushed > 0:
                    # Add flow to the forward edge
                    edge.flow += pushed
                    # SUBTRACT flow from the reverse edge (allowing us to "undo" this later)
                    self.graph[edge.target][edge.rev_index].flow -= pushed
                    return pushed
            
            # If we couldn't push flow through this edge, permanently skip it for this phase
            start_index[current] += 1
            
        return 0.0

    def calculate_max_flow(self, source: int, sink: int) -> float:
        """
        Executes Dinic's algorithm to find the absolute maximum network throughput.
        """
        if source < 0 or source >= self.n or sink < 0 or sink >= self.n:
            raise IndexError("Source or sink node index is out of bounds.")
            
        max_flow = 0.0
        
        # Loop until the BFS can no longer find a valid path to the sink
        while self._bfs_build_level_graph(source, sink):
            
            # Reset the Dead-End Pruning array for the new level graph
            start_index = [0] * self.n
            
            while True:
                # Push as much flow as possible until the current level graph is blocked
                pushed = self._dfs_find_blocking_flow(source, sink, float('inf'), start_index)
                if pushed == 0:
                    break
                max_flow += pushed
                
        return max_flow