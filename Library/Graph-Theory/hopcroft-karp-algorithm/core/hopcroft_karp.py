import collections

class HopcroftKarp:
    def __init__(self, u_nodes, v_nodes):
        """
        Initialize the Hopcroft-Karp algorithm for maximum bipartite matching.
        u_nodes: list of nodes in partition U
        v_nodes: list of nodes in partition V
        """
        self.u_nodes = u_nodes
        self.v_nodes = v_nodes
        self.graph = {u: [] for u in u_nodes}
        
        # pair_u[u] stores the matching node in V for u in U.
        self.pair_u = {u: None for u in u_nodes}
        # pair_v[v] stores the matching node in U for v in V.
        self.pair_v = {v: None for v in v_nodes}
        self.dist = {}

    def add_edge(self, u, v):
        """Add an undirected edge between u in U and v in V."""
        if u in self.u_nodes and v in self.v_nodes:
            self.graph[u].append(v)
        else:
            raise ValueError(f"Nodes must belong to their respective partitions: {u} in U, {v} in V")

    def bfs(self):
        """Breadth-First Search to find augmenting paths."""
        queue = collections.deque()
        for u in self.u_nodes:
            if self.pair_u[u] is None:
                self.dist[u] = 0
                queue.append(u)
            else:
                self.dist[u] = float('inf')
        
        self.dist[None] = float('inf')

        while queue:
            u = queue.popleft()
            if self.dist[u] < self.dist[None]:
                for v in self.graph[u]:
                    if self.pair_v[v] is None:
                        # Found an unmatched vertex in V; update distance to NIL (None)
                        if self.dist[None] == float('inf'):
                            self.dist[None] = self.dist[u] + 1
                    else:
                        if self.dist.get(self.pair_v[v], float('inf')) == float('inf'):
                            self.dist[self.pair_v[v]] = self.dist[u] + 1
                            queue.append(self.pair_v[v])
        return self.dist[None] != float('inf')

    def dfs(self, u):
        """Depth-First Search to augment paths."""
        if u is not None:
            for v in self.graph[u]:
                if self.dist.get(self.pair_v[v], float('inf')) == self.dist[u] + 1:
                    if self.dfs(self.pair_v[v]):
                        self.pair_v[v] = u
                        self.pair_u[u] = v
                        return True
            self.dist[u] = float('inf')
            return False
        return True

    def max_matching(self):
        """
        Finds the maximum matching using the Hopcroft-Karp algorithm.
        Returns:
            matching (int): The number of edges in the maximum matching.
            pair_u (dict): The actual matching mappings from U to V.
        """
        matching = 0
        while self.bfs():
            for u in self.u_nodes:
                if self.pair_u[u] is None:
                    if self.dfs(u):
                        matching += 1
        
        # Filter out None values to return the actual matchings
        final_matching = {u: v for u, v in self.pair_u.items() if v is not None}
        return matching, final_matching

if __name__ == "__main__":
    # Example usage:
    u_nodes = [1, 2, 3, 4]
    v_nodes = ['A', 'B', 'C', 'D']
    
    hk = HopcroftKarp(u_nodes, v_nodes)
    hk.add_edge(1, 'A')
    hk.add_edge(1, 'B')
    hk.add_edge(2, 'A')
    hk.add_edge(3, 'C')
    hk.add_edge(4, 'C')
    hk.add_edge(4, 'D')

    max_edges, matches = hk.max_matching()
    print(f"Maximum matching size: {max_edges}")
    print(f"Matches: {matches}")
