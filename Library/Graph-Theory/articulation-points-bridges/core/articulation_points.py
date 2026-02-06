"""
Articulation Points and Bridges Algorithm Implementation
Finds critical vertices and edges in an undirected graph using Tarjan's algorithm
"""

from collections import defaultdict


class ArticulationPointsAndBridges:
    """
    Implementation of Tarjan's algorithm to find articulation points and bridges
    in an undirected graph
    
    Articulation Point (Cut Vertex): A vertex whose removal increases the number of connected components
    Bridge (Cut Edge): An edge whose removal increases the number of connected components
    """
    
    def __init__(self, vertices):
        """
        Initialize the graph
        
        Args:
            vertices (int): Number of vertices in the graph
        """
        self.vertices = vertices
        self.graph = defaultdict(list)
        self.time = 0
        
    def add_edge(self, u, v):
        """
        Add an undirected edge between u and v
        
        Args:
            u (int): First vertex
            v (int): Second vertex
        """
        self.graph[u].append(v)
        self.graph[v].append(u)
    
    def _dfs_articulation(self, u, visited, parent, low, disc, ap):
        """
        DFS helper to find articulation points
        
        Args:
            u (int): Current vertex
            visited (list): Visited array
            parent (list): Parent array
            low (list): Low values (earliest visited vertex reachable)
            disc (list): Discovery times
            ap (set): Set to store articulation points
        """
        children = 0
        visited[u] = True
        disc[u] = self.time
        low[u] = self.time
        self.time += 1
        
        for v in self.graph[u]:
            if not visited[v]:
                children += 1
                parent[v] = u
                self._dfs_articulation(v, visited, parent, low, disc, ap)
                
                # Check if subtree rooted at v has connection back to ancestors of u
                low[u] = min(low[u], low[v])
                
                # u is an articulation point in following cases:
                
                # Case 1: u is root and has more than one child
                if parent[u] == -1 and children > 1:
                    ap.add(u)
                
                # Case 2: u is not root and low value of child >= discovery of u
                if parent[u] != -1 and low[v] >= disc[u]:
                    ap.add(u)
                    
            elif v != parent[u]:
                # Update low value for parent function calls (back edge)
                low[u] = min(low[u], disc[v])
    
    def _dfs_bridges(self, u, visited, parent, low, disc, bridges):
        """
        DFS helper to find bridges
        
        Args:
            u (int): Current vertex
            visited (list): Visited array
            parent (list): Parent array
            low (list): Low values (earliest visited vertex reachable)
            disc (list): Discovery times
            bridges (list): List to store bridges
        """
        visited[u] = True
        disc[u] = self.time
        low[u] = self.time
        self.time += 1
        
        for v in self.graph[u]:
            if not visited[v]:
                parent[v] = u
                self._dfs_bridges(v, visited, parent, low, disc, bridges)
                
                # Check if subtree rooted at v has connection back to ancestors of u
                low[u] = min(low[u], low[v])
                
                # If low value of v is greater than discovery of u, then u-v is a bridge
                if low[v] > disc[u]:
                    bridges.append((u, v))
                    
            elif v != parent[u]:
                # Update low value for parent function calls (back edge)
                low[u] = min(low[u], disc[v])
    
    def find_articulation_points(self):
        """
        Find all articulation points (cut vertices) in the graph
        
        Returns:
            list: List of articulation points
        """
        visited = [False] * self.vertices
        disc = [float("inf")] * self.vertices
        low = [float("inf")] * self.vertices
        parent = [-1] * self.vertices
        ap = set()
        
        # Call DFS from all unvisited vertices
        for i in range(self.vertices):
            if not visited[i]:
                self.time = 0
                self._dfs_articulation(i, visited, parent, low, disc, ap)
        
        return sorted(list(ap))
    
    def find_bridges(self):
        """
        Find all bridges (cut edges) in the graph
        
        Returns:
            list: List of tuples representing bridges (u, v)
        """
        visited = [False] * self.vertices
        disc = [float("inf")] * self.vertices
        low = [float("inf")] * self.vertices
        parent = [-1] * self.vertices
        bridges = []
        
        # Call DFS from all unvisited vertices
        for i in range(self.vertices):
            if not visited[i]:
                self.time = 0
                self._dfs_bridges(i, visited, parent, low, disc, bridges)
        
        return bridges
    
    def find_both(self):
        """
        Find both articulation points and bridges in one pass
        
        Returns:
            tuple: (articulation_points, bridges)
        """
        visited = [False] * self.vertices
        disc = [float("inf")] * self.vertices
        low = [float("inf")] * self.vertices
        parent = [-1] * self.vertices
        ap = set()
        bridges = []
        
        def dfs(u):
            children = 0
            visited[u] = True
            disc[u] = self.time
            low[u] = self.time
            self.time += 1
            
            for v in self.graph[u]:
                if not visited[v]:
                    children += 1
                    parent[v] = u
                    dfs(v)
                    
                    low[u] = min(low[u], low[v])
                    
                    # Check for articulation point
                    if parent[u] == -1 and children > 1:
                        ap.add(u)
                    if parent[u] != -1 and low[v] >= disc[u]:
                        ap.add(u)
                    
                    # Check for bridge
                    if low[v] > disc[u]:
                        bridges.append((u, v))
                        
                elif v != parent[u]:
                    low[u] = min(low[u], disc[v])
        
        for i in range(self.vertices):
            if not visited[i]:
                self.time = 0
                dfs(i)
        
        return sorted(list(ap)), bridges


def find_critical_connections_with_names(nodes, edges):
    """
    Utility function to find critical connections using node names
    
    Args:
        nodes (list): List of node names
        edges (list): List of tuples (node1, node2) representing edges
    
    Returns:
        dict: Dictionary with 'articulation_points' and 'bridges' using node names
    """
    # Create node to index mapping
    node_to_idx = {node: idx for idx, node in enumerate(nodes)}
    
    # Create graph
    graph = ArticulationPointsAndBridges(len(nodes))
    for u, v in edges:
        graph.add_edge(node_to_idx[u], node_to_idx[v])
    
    # Find critical connections
    ap_indices, bridge_indices = graph.find_both()
    
    # Convert back to node names
    articulation_points = [nodes[idx] for idx in ap_indices]
    bridges = [(nodes[u], nodes[v]) for u, v in bridge_indices]
    
    return {
        'articulation_points': articulation_points,
        'bridges': bridges
    }


def analyze_network_vulnerability(nodes, edges):
    """
    Analyze network vulnerability by identifying critical points and connections
    
    Args:
        nodes (list): List of node names
        edges (list): List of tuples (node1, node2) representing connections
    
    Returns:
        dict: Comprehensive vulnerability analysis
    """
    result = find_critical_connections_with_names(nodes, edges)
    
    total_nodes = len(nodes)
    total_edges = len(edges)
    critical_nodes = len(result['articulation_points'])
    critical_edges = len(result['bridges'])
    
    # Calculate vulnerability metrics
    node_vulnerability = (critical_nodes / total_nodes * 100) if total_nodes > 0 else 0
    edge_vulnerability = (critical_edges / total_edges * 100) if total_edges > 0 else 0
    
    return {
        'articulation_points': result['articulation_points'],
        'bridges': result['bridges'],
        'statistics': {
            'total_nodes': total_nodes,
            'total_edges': total_edges,
            'critical_nodes': critical_nodes,
            'critical_edges': critical_edges,
            'node_vulnerability_percentage': round(node_vulnerability, 2),
            'edge_vulnerability_percentage': round(edge_vulnerability, 2)
        }
    }
