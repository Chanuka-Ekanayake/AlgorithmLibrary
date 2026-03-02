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

        This implementation is iterative to avoid hitting Python's recursion limit
        on deep level graphs. It mirrors the behavior of the classic recursive
        DFS used in Dinic's algorithm, including the use of start_index for
        dead-end pruning.
        """
        # Each frame represents a node on the current DFS path.
        # For non-root frames, parent_edge_index is the index in the parent's
        # adjacency list that leads to this node.
        stack = [{
            "node": current,
            "flow": current_flow,
            "parent_edge_index": None,
        }]

        while stack:
            frame = stack[-1]
            node = frame["node"]
            flow = frame["flow"]

            # If we've reached the sink, propagate the flow back along the path.
            if node == sink:
                pushed = flow

                # Walk back through the stack, updating forward and reverse edges.
                for idx in range(len(stack) - 1, 0, -1):
                    child_frame = stack[idx]
                    parent_frame = stack[idx - 1]
                    parent_node = parent_frame["node"]
                    edge_index = child_frame["parent_edge_index"]

                    edge = self.graph[parent_node][edge_index]
                    edge.flow += pushed
                    # Update reverse edge flow to maintain residual capacity.
                    self.graph[edge.target][edge.rev_index].flow -= pushed

                return pushed

            # Try to advance from this node along admissible edges.
            i = start_index[node]
            advanced = False

            while i < len(self.graph[node]):
                edge = self.graph[node][i]

                # Data can ONLY flow to a node that is exactly one level deeper
                if self.level[edge.target] == self.level[node] + 1 and edge.flow < edge.capacity:
                    # The maximum flow we can push is the bottleneck of the path
                    bottleneck = min(flow, edge.capacity - edge.flow)

                    # Move forward in the DFS to the target node.
                    stack.append({
                        "node": edge.target,
                        "flow": bottleneck,
                        "parent_edge_index": i,
                    })
                    advanced = True
                    # We do NOT increment start_index[node] yet; if this path
                    # later fails (dead end), we'll advance it when we backtrack.
                    break

                # If we couldn't push flow through this edge, permanently skip it
                # for this phase (dead-end pruning).
                i += 1
                start_index[node] = i

            if advanced:
                # Process the newly added child frame in the next loop iteration.
                continue

            # No more edges to try from this node: backtrack (dead end).
            dead_frame = stack.pop()

            if not stack:
                # Exhausted all paths from the source without reaching the sink.
                break

            # Inform the parent that the edge leading to this dead end is exhausted,
            # so it should move on to the next edge.
            parent_frame = stack[-1]
            parent_node = parent_frame["node"]
            parent_edge_index = dead_frame["parent_edge_index"]

            # Only advance if the parent's start_index is not already beyond this edge.
            if parent_edge_index is not None and start_index[parent_node] <= parent_edge_index:
                start_index[parent_node] = parent_edge_index + 1

        # No augmenting path could be found in the current level graph.
        return 0.0

    def calculate_max_flow(self, source: int, sink: int) -> float:
        """
        Executes Dinic's algorithm to find the absolute maximum network throughput.
        """
        if source < 0 or source >= self.n or sink < 0 or sink >= self.n:
            raise IndexError("Source or sink node index is out of bounds.")

        if source == sink:
            raise ValueError("Source and sink must be different nodes.")
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