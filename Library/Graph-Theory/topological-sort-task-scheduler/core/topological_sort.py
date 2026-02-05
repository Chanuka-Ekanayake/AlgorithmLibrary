"""
Topological Sort Algorithm Implementation
Uses DFS-based approach to order vertices in a Directed Acyclic Graph (DAG)
"""

from collections import defaultdict, deque


class TopologicalSort:
    """
    Topological Sort implementation for ordering tasks with dependencies
    Supports both DFS and Kahn's (BFS) algorithms
    """
    
    def __init__(self, vertices):
        """
        Initialize the graph
        
        Args:
            vertices (int): Number of vertices in the graph
        """
        self.vertices = vertices
        self.graph = defaultdict(list)
        
    def add_edge(self, u, v):
        """
        Add a directed edge from u to v (u -> v means v depends on u)
        
        Args:
            u (int): Source vertex
            v (int): Destination vertex (depends on u)
        """
        self.graph[u].append(v)
    
    def _dfs_helper(self, vertex, visited, stack):
        """
        Recursive DFS helper for topological sort
        
        Args:
            vertex (int): Current vertex
            visited (list): Visited array
            stack (list): Stack to store the result
        """
        visited[vertex] = True
        
        # Recursively visit all adjacent vertices
        for neighbor in self.graph[vertex]:
            if not visited[neighbor]:
                self._dfs_helper(neighbor, visited, stack)
        
        # Push current vertex to stack after visiting all dependencies
        stack.append(vertex)
    
    def topological_sort_dfs(self):
        """
        Perform topological sort using a DFS-based approach.
        
        This method assumes the graph is a Directed Acyclic Graph (DAG) and
        does not perform cycle detection. If the graph contains a cycle, the
        returned order may be incorrect.
        
        For cycle detection, use `has_cycle()` or `topological_sort_kahn()`.
        
        Returns:
            list: Vertices in topological order.
        """
        visited = [False] * self.vertices
        stack = []
        
        # Visit all vertices
        for vertex in range(self.vertices):
            if not visited[vertex]:
                self._dfs_helper(vertex, visited, stack)
        
        # Reverse the stack to get topological order
        return stack[::-1]
    
    def topological_sort_kahn(self):
        """
        Perform topological sort using Kahn's algorithm (BFS approach)
        Also detects cycles in the graph
        
        Returns:
            list: Vertices in topological order
            None: If graph contains a cycle
        """
        # Calculate in-degree for all vertices
        in_degree = [0] * self.vertices
        for vertex in range(self.vertices):
            for neighbor in self.graph[vertex]:
                in_degree[neighbor] += 1
        
        # Queue for vertices with in-degree 0
        queue = deque([v for v in range(self.vertices) if in_degree[v] == 0])
        result = []
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            
            # Reduce in-degree for all neighbors
            for neighbor in self.graph[vertex]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Check if all vertices are processed (no cycle)
        if len(result) != self.vertices:
            return None  # Cycle detected
        
        return result
    
    def has_cycle(self):
        """
        Check if the graph contains a cycle using DFS
        
        Returns:
            bool: True if cycle exists, False otherwise
        """
        WHITE, GRAY, BLACK = 0, 1, 2
        color = [WHITE] * self.vertices
        
        def dfs_cycle_check(vertex):
            if color[vertex] == GRAY:
                return True  # Back edge found (cycle)
            
            if color[vertex] == BLACK:
                return False  # Already processed
            
            color[vertex] = GRAY
            
            for neighbor in self.graph[vertex]:
                if dfs_cycle_check(neighbor):
                    return True
            
            color[vertex] = BLACK
            return False
        
        for vertex in range(self.vertices):
            if color[vertex] == WHITE:
                if dfs_cycle_check(vertex):
                    return True
        
        return False


def topological_sort_with_names(tasks, dependencies):
    """
    Utility function for topological sort with task names
    
    Args:
        tasks (list): List of task names
        dependencies (list): List of tuples (task1, task2) where task2 depends on task1
    
    Returns:
        list: Tasks in execution order
        None: If circular dependency exists
    """
    # Create task to index mapping
    task_to_idx = {task: idx for idx, task in enumerate(tasks)}
    
    # Create graph
    topo = TopologicalSort(len(tasks))
    for prereq, task in dependencies:
        topo.add_edge(task_to_idx[prereq], task_to_idx[task])
    
    # Check for cycles
    if topo.has_cycle():
        return None
    
    # Get topological order
    order = topo.topological_sort_kahn()
    if order is None:
        return None
    
    # Convert indices back to task names
    return [tasks[idx] for idx in order]
