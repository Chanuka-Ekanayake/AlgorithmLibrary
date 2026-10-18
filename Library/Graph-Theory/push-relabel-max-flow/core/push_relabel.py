"""
Push-Relabel Algorithm (Goldberg-Tarjan Maximum Flow)
An advanced graph theory engine for solving the Maximum Flow and Minimum Cut
problems in dense directed networks.

Unlike augmenting-path algorithms (such as Ford-Fulkerson or Edmonds-Karp),
Push-Relabel works locally on individual vertices by maintaining a "preflow"
and height labels. Active nodes "push" excess flow downhill toward neighbors,
and "relabel" themselves upward when no downhill residual edge is available.
"""

from typing import List, Tuple, Dict, Any
from collections import deque


class Edge:
    """Represents a directed link with capacity, flow, and residual bookkeeping."""
    __slots__ = ['target', 'capacity', 'flow', 'rev_index', 'is_forward']

    def __init__(self, target: int, capacity: float, rev_index: int, is_forward: bool = True):
        self.target: int = target
        self.capacity: float = capacity
        self.flow: float = 0.0
        self.rev_index: int = rev_index
        self.is_forward: bool = is_forward

    @property
    def residual_capacity(self) -> float:
        """Returns the available capacity remaining on this edge."""
        return self.capacity - self.flow


class PushRelabelMaxFlow:
    """
    Goldberg-Tarjan Push-Relabel Maximum Flow Engine.

    Features:
    - Highest-Label Selection: Prioritizes vertices with maximum height for discharge.
    - Gap Heuristic: Accelerates convergence by identifying unreachable disconnected levels.
    - Min-Cut Extraction: Identifies bottleneck boundaries partitioning the network.
    - True Flow Conservation: Guarantees net excess is zero on all intermediate nodes.
    """

    def __init__(self, num_nodes: int):
        if num_nodes < 2:
            raise ValueError("A flow network must contain at least 2 nodes (source and sink).")

        self.n: int = num_nodes
        self.graph: List[List[Edge]] = [[] for _ in range(num_nodes)]
        self.excess: List[float] = [0.0] * num_nodes
        self.height: List[int] = [0] * num_nodes
        self.count: List[int] = [0] * (2 * num_nodes)
        self.current_edge: List[int] = [0] * num_nodes
        self.buckets: List[List[int]] = [[] for _ in range(2 * num_nodes)]
        self.max_height: int = 0
        self.in_bucket: List[bool] = [False] * num_nodes
        self.source: int = -1
        self.sink: int = -1

    def add_edge(self, source: int, target: int, capacity: float) -> None:
        """
        Adds a directed capacity edge between two nodes.

        :param source: Origin vertex index (0-indexed).
        :param target: Destination vertex index (0-indexed).
        :param capacity: Maximum allowable throughput capacity.
        """
        if not (0 <= source < self.n and 0 <= target < self.n):
            raise IndexError(f"Node indices must be within range [0, {self.n - 1}].")
        if source == target:
            raise ValueError("Self-loops are not permitted in flow networks.")
        if capacity < 0:
            raise ValueError("Edge capacity cannot be negative.")

        forward_edge = Edge(target, float(capacity), len(self.graph[target]), is_forward=True)
        reverse_edge = Edge(source, 0.0, len(self.graph[source]), is_forward=False)

        self.graph[source].append(forward_edge)
        self.graph[target].append(reverse_edge)

    def _enqueue(self, u: int) -> None:
        """Enqueues an active node (excess > 0) into its respective height bucket."""
        if not self.in_bucket[u] and self.excess[u] > 1e-9 and self.height[u] < 2 * self.n:
            self.in_bucket[u] = True
            h = self.height[u]
            self.buckets[h].append(u)
            if h > self.max_height:
                self.max_height = h

    def _push(self, u: int, edge: Edge) -> None:
        """
        Pushes excess flow from node u downhill to edge.target.
        Flow can only be pushed if height[u] == height[v] + 1.
        """
        v = edge.target
        rev = self.graph[v][edge.rev_index]
        push_amount = min(self.excess[u], edge.residual_capacity)

        if push_amount > 1e-9 and self.height[u] == self.height[v] + 1:
            edge.flow += push_amount
            rev.flow -= push_amount
            self.excess[u] -= push_amount
            self.excess[v] += push_amount

            # If v became active and is neither source nor sink, enqueue it
            if v != self.source and v != self.sink:
                self._enqueue(v)

    def _relabel(self, u: int) -> None:
        """
        Increases the height of an active node u to enable future pushes.
        Also applies the Gap Heuristic to prune disconnected height tiers.
        """
        old_h = self.height[u]
        self.count[old_h] -= 1
        min_height = 2 * self.n

        for edge in self.graph[u]:
            if edge.residual_capacity > 1e-9:
                min_height = min(min_height, self.height[edge.target])

        new_height = min_height + 1

        # Gap Heuristic:
        # If the old height level has become completely empty and old_h < n,
        # all nodes above this level can no longer reach the sink and can be lifted.
        if self.count[old_h] == 0 and old_h < self.n:
            for i in range(self.n):
                if i != self.source and i != self.sink and old_h < self.height[i] < self.n:
                    self.count[self.height[i]] -= 1
                    self.height[i] = max(self.height[i], self.n + 1)
                    self.count[self.height[i]] += 1

        self.height[u] = new_height
        if new_height < 2 * self.n:
            self.count[new_height] += 1
            self._enqueue(u)

    def _discharge(self, u: int) -> None:
        """
        Repeatedly pushes flow through available downhill edges of node u
        and relabels u when all outgoing residual edges are blocked.
        """
        edges = self.graph[u]
        num_edges = len(edges)

        while self.excess[u] > 1e-9:
            if self.current_edge[u] < num_edges:
                edge = edges[self.current_edge[u]]
                if edge.residual_capacity > 1e-9 and self.height[u] == self.height[edge.target] + 1:
                    self._push(u, edge)
                else:
                    self.current_edge[u] += 1
            else:
                self._relabel(u)
                self.current_edge[u] = 0
                if self.height[u] >= 2 * self.n:
                    break

    def calculate_max_flow(self, source: int, sink: int) -> float:
        """
        Computes the maximum throughput from source to sink across the network.

        :param source: Source node index.
        :param sink: Sink node index.
        :return: Maximum flow value.
        """
        if not (0 <= source < self.n and 0 <= sink < self.n):
            raise IndexError("Source and sink indices must be within valid node bounds.")
        if source == sink:
            raise ValueError("Source and sink cannot be the same node.")

        self.source = source
        self.sink = sink

        # Reinitialize internal state
        self.excess = [0.0] * self.n
        self.height = [0] * self.n
        self.count = [0] * (2 * self.n)
        self.current_edge = [0] * self.n
        self.buckets = [[] for _ in range(2 * self.n)]
        self.max_height = 0
        self.in_bucket = [False] * self.n

        for u in range(self.n):
            for edge in self.graph[u]:
                edge.flow = 0.0

        # Phase 1: Preflow Initialization
        self.height[source] = self.n
        self.count[self.n] = 1
        self.count[0] = self.n - 1

        # Saturate all outgoing edges directly from source
        for edge in self.graph[source]:
            push_amount = edge.capacity
            if push_amount > 0:
                edge.flow += push_amount
                rev = self.graph[edge.target][edge.rev_index]
                rev.flow -= push_amount
                self.excess[edge.target] += push_amount
                self.excess[source] -= push_amount

        # Seed all active non-source/sink vertices into bucket queue
        for v in range(self.n):
            if v != source and v != sink and self.excess[v] > 1e-9:
                self._enqueue(v)

        # Phase 2: Highest-Label Discharge Loop
        while self.max_height >= 0:
            if not self.buckets[self.max_height]:
                self.max_height -= 1
                continue

            u = self.buckets[self.max_height].pop()
            self.in_bucket[u] = False
            self._discharge(u)

        return max(0.0, self.excess[sink])

    def get_min_cut(self, source: int) -> Tuple[List[int], List[int]]:
        """
        Computes the Minimum (S, T) Cut by finding all vertices reachable
        from the source in the residual graph after maximum flow has converged.

        :param source: Source vertex index.
        :return: Tuple of (source_set, sink_set) containing node indices.
        """
        visited = [False] * self.n
        queue = deque([source])
        visited[source] = True

        while queue:
            u = queue.popleft()
            for edge in self.graph[u]:
                if not visited[edge.target] and edge.residual_capacity > 1e-9:
                    visited[edge.target] = True
                    queue.append(edge.target)

        source_partition = [i for i in range(self.n) if visited[i]]
        sink_partition = [i for i in range(self.n) if not visited[i]]
        return source_partition, sink_partition

    def get_edge_flows(self) -> List[Dict[str, Any]]:
        """
        Returns a list of dictionaries detailing the utilization of all forward edges.
        """
        edge_details = []
        for u in range(self.n):
            for edge in self.graph[u]:
                if edge.is_forward:
                    edge_details.append({
                        "from": u,
                        "to": edge.target,
                        "capacity": edge.capacity,
                        "flow": max(0.0, edge.flow),
                        "saturated": abs(edge.capacity - edge.flow) < 1e-9 and edge.capacity > 0
                    })
        return edge_details
